import cv2
import numpy as np
from skimage.filters import threshold_isodata,rank
from skimage.segmentation import clear_border
from skimage.morphology import opening, closing, disk, square
from skimage.feature import canny
from skimage.measure import ransac, CircleModel, label, regionprops
from scipy.ndimage import rotate
from scipy.signal import find_peaks
from math import sqrt
from hyperspy.io import load as hsload

class ASAP():
	def __init__(self, filename):
		self.filename = filename
		s = hsload(self.filename)
		axes = s.axes_manager.as_dictionary()
		self.scale = next((item.get('scale') for item in axes.values() if item.get('name')=='x'),1)
		self.org_image = s.data.copy().astype(np.float64)
		self.distance_limit = int(s.data.shape[0]/16)
		# for cropping beamstop
		self.kernel_blur = int(s.data.shape[0]/32)
		self.smallradii = int(self.kernel_blur/10) if int(self.kernel_blur/10)>1 else 2
		self.kernel_beamstop = int(s.data.shape[0]/1024) if s.data.shape[0]>1024 else 1
		self.kernel_beamstop = 3
		self.find_circle_ratio = 2 # 2.2 sigma

	def remove_beamstop(self, beamstop=None, iteractions=10):
		if beamstop is not None:
			self.kernel_beamstop = beamstop
		self.reduced_image = self.org_image.copy()
		img = self.org_image
		img -= img.min()
		img /= img.max()
		img *= 255
		img[img<=5] = 0
		img = img.astype(np.uint8)
		bimg = (img<=1).astype(np.uint8)
		self.binary = bimg
		kernel = np.ones((self.kernel_beamstop,self.kernel_beamstop),np.uint8)
		# dilation_img = cv2.dilate(bimg, kernel, iterations=iteractions)
		opening_img = cv2.morphologyEx(bimg,cv2.MORPH_OPEN,kernel)
		dilation_img = cv2.dilate(opening_img, kernel, iterations=iteractions)
		self.dilation_image = dilation_img
		self.beamstop = dilation_img>0
		self.reduced_image[self.beamstop] = 0

	def find_center(self, threshold=20, mins=20, trials=3000):
		# find transmitted beam first
		img = (self.reduced_image/self.reduced_image.max()*255).astype(np.uint8)
		img_blurred = cv2.blur(img,(self.kernel_blur,self.kernel_blur))
		img_max, img_mean, img_std = img_blurred.max(), img_blurred.mean(), img_blurred.std()
		img[img<(self.smallradii/2+img_mean*2+img_std*2)*np.exp(img_max/255)] = 0
		self.f1 = img

		thresh_img = threshold_isodata(img)
		bw_img = closing(img > thresh_img, square(1))
		cleared_img = clear_border(bw_img)
		label_img = label(cleared_img)
		self.f2 = label_img
		props = regionprops(label_img, intensity_image=img)
		area = [item.area for item in props]
		area_idx = np.argsort(area)[::-1]
		largest_area = props[area_idx[0]]

		# except transmitted beam, remove all 
		miny, minx, maxy, maxx = largest_area.bbox
		mask = np.zeros((img.shape),dtype=bool)
		mask[miny-self.distance_limit:maxy+self.distance_limit,minx-self.distance_limit:maxx+self.distance_limit] = True
		for p in props:
			if p.area >= largest_area.area:
				continue
			pminy, pminx, pmaxy, pmaxx = p.bbox
			mask[pminy:pmaxy, pminx:pmaxx] = False
		masked = img*mask
		cropped_img = img[miny-self.distance_limit:maxy+self.distance_limit,minx-self.distance_limit:maxx+self.distance_limit]
		self.cropped_image = cropped_img.copy()

		check_img = masked[miny:maxy,minx:maxx]
		check_blurred = cv2.blur(check_img,(self.smallradii,self.smallradii))
		check_max, check_mean, check_std = check_blurred.max(), check_blurred.mean(), check_blurred.std()
		# check_add = abs(check_std-check_mean)*abs(check_max-check_mean-check_std*2)/255*50
		if check_img.max() < 200:
			self.has_to_refine = True
		else:
			self.has_to_refine = False

		# create bw image
		thresh_img = threshold_isodata(cropped_img)
		bw_img = opening(cropped_img > thresh_img, disk(1))
		bw_img = rank.minimum(rank.maximum(bw_img.astype(np.uint8),disk(1)),disk(2))
		cleared_img = bw_img
		label_img = label(cleared_img)
		props = regionprops(label_img, intensity_image=cropped_img)
		area = [item.area for item in props]
		area_idx = np.argsort(area)[::-1]
		largest_area = props[area_idx[0]]
		second_area = largest_area
		for p in np.array(props)[area_idx][1:]:
			if p.max_intensity < check_max and p.major_axis_length < largest_area.major_axis_length*2:
				second_area = p
				distance = (sqrt(((np.array(second_area.weighted_centroid) - np.array(largest_area.weighted_centroid))**2).sum()))
				if distance >= self.distance_limit or second_area.area<largest_area.area/100:
					continue
				else:
					break
		self.largest_area = largest_area
		self.second_area = second_area
		miny_t, minx_t, maxy_t, maxx_t = largest_area.bbox
		miny_ts, minx_ts, maxy_ts, maxx_ts = second_area.bbox
		mask_img = cleared_img.copy().astype('bool')
		for p in props:
			if p is second_area or p is largest_area:
				continue
			pminy, pminx, pmaxy, pmaxx = p.bbox
			mask_img[pminy:pmaxy, pminx:pmaxx] = mask_img[pminy:pmaxy, pminx:pmaxx] & ~p.image
		self.mask_image = mask_img
		self.y1 = miny-self.distance_limit
		self.y2 = maxy+self.distance_limit
		self.x1 = minx-self.distance_limit
		self.x2 = maxx+self.distance_limit

		# find circle, via ransac algorithm
		bw_closing = rank.maximum(rank.minimum(mask_img.astype(np.uint8),square(1)),square(1))
		bw_opening = rank.minimum(rank.maximum(bw_closing.astype(np.uint8),disk(int(self.kernel_beamstop/2))),disk(int(self.kernel_beamstop/2)))
		self.bw_opening = bw_opening
		edges = canny(bw_opening.astype(np.float64),sigma=1)
		points = np.array(np.nonzero(edges)).T

		cropped_beamstop = self.beamstop[miny-self.distance_limit:maxy+self.distance_limit, minx-self.distance_limit:maxx+self.distance_limit]
		beamstop_p = np.array(list(zip(*np.where(cropped_beamstop))))
		indices = []
		for i,p in enumerate(points):
			dis = np.sqrt(np.sum((p-beamstop_p)**2, axis=1)).min()
			if dis<5:
				indices.append(i)
		points = np.delete(points, indices, axis=0)
		self.points = points

		thresh_ransac = np.mean(np.absolute(edges-np.mean(edges)))*10000
		if thresh_ransac<1:
			thresh_ransac = thresh_ransac*3
		thresh_ransac = threshold
		min_samples = len(points)//mins if len(points)//mins>3 else 3
		model_robust, inliers = ransac(points, CircleModel, min_samples=min_samples, residual_threshold=thresh_ransac, max_trials=trials)
		cy, cx, r = model_robust.params
		self.center = (cx + minx - self.distance_limit, cy + miny - self.distance_limit)

		self.edges = edges
		self.points = points
		self.thresh_ransac = thresh_ransac
		self.cy, self.cx, self.r = cy, cx, r
		self.minx, self.maxx, self.miny, self.maxy = minx, maxx, miny, maxy

	def get_sum(self, image, cx, cy, r):
		xx, yy = np.mgrid[:image.shape[1], :image.shape[0]]
		circle = np.sqrt((xx-cx)**2+(yy-cy)**2)
		ring = np.logical_and(circle<(r+25), circle>(r-25))
		return image[~ring].sum()
	
	def refine_center(self, thresh=20, step=2):
		_,y = self.radial_profile(image=self.aligned_image)
		p,_ = find_peaks(y/y.max(), prominence=0.1, distance=100)
		p_1st = p[p>self.aligned_image.shape[0]/40][0]

		min_y, min_x = 0, 0
		cy, cx = (np.array(self.aligned_image.shape)/2).astype(int)
		sum_min = self.get_sum(self.aligned_image, cx, cy, p_1st)
		for p_x in range(-thresh, thresh+1, step):
			for p_y in range(-thresh, thresh+1, step):
				# for p_r in range(-thresh, thresh+1, step):
				s = self.get_sum(self.aligned_image, cx+p_x, cy+p_y, p_1st)
				if s < sum_min:
					min_x = p_x
					min_y = p_y
					sum_min = s
		print(f"Refined by moving {min_x, min_y}")
		self.center = np.array(self.center)+np.array([min_y, min_x])
		self.merge()

	def merge(self):
		self.remove_beamstop(iteractions=10)
		size_y, size_x = self.org_image.shape
		translation_matrix = np.float32([ [1,0,size_x/2-self.center[0]], [0,1,size_y/2-self.center[1]] ])

		aligned_img = cv2.warpAffine(self.org_image, translation_matrix, (size_x,size_y))
		aligned_ref = cv2.warpAffine(self.reduced_image, translation_matrix, (size_x,size_y))
		aligned_beamstop = cv2.warpAffine(np.uint8(self.beamstop), translation_matrix, (size_x,size_y)).astype(bool)
		aligned_img[(aligned_img<=0) & (~aligned_beamstop)] = np.median(aligned_img)
		aligned_ref[(aligned_ref<=0) & (~aligned_beamstop)] = np.median(aligned_ref)
		rotated_img = rotate(aligned_ref,180)

		img = aligned_ref.copy()
		img[aligned_beamstop] = rotated_img[aligned_beamstop]
		
		self.aligned_image = aligned_img
		self.merged_image = img.copy()

	def radial_profile(self, image=None, center=None, scale=1, divide=False):
		if image is None:
			image = self.merged_image
		if center is None:
			center = list(map(lambda x: x/2, image.shape))
		y, x = np.indices((image.shape))
		r = np.sqrt((x - center[0])**2 + (y - center[1])**2)
		r = r.astype(np.int32)
		tbin = np.bincount(r.ravel(), image.ravel())
		nr = np.bincount(r.ravel())
		if divide:
			radialprofile = tbin / nr
		else:
			radialprofile = tbin
		x = np.arange(0,len(radialprofile))*scale
		y = radialprofile
		return (x,y)

	def save_to_csv(self,x=None, y=None, filename='results.csv'):
		if x is None or y is None:
			x = self.x
			y = self.y
		np.savetxt(filename, np.column_stack([x, y]), delimiter=',')

	def auto_profile(self):
		self.remove_beamstop()
		self.find_center() 
		self.merge()
		if self.has_to_refine:
			self.refine_center()
		self.x,self.y = self.radial_profile()

