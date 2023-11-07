# ASAP
**A**uto **S**elected **A**rea diffraction patterns **P**rofiler (ASAP)

ASAP is a Python-based computational method developed for the automated interpretation of selected area diffraction patterns (SADP) in transmission electron microscopy. The approach utilizes advanced computer vision algorithms, including the random sample consensus (RANSAC) algorithm, to automatically generate structural profiles from electron diffraction pattern images.

## Getting Started
### Prerequisites
Make sure you have Python installed on your system. Additionally, install the required packages by running the following command:
```
pip install -r requirements.txt
```
### Running the UI
To run the UI, execute the following command in your terminal or command prompt:
```
python ASAP_UI.py
```

## Usage
![image](https://github.com/sooyeonLim/ASAP/assets/52401652/ac5976af-0633-4b84-879f-4d17337f29d6)
1. **Load Data:**
    - Click on the magnifying glass icon in the "Load Data" section to open a file dialog.
    - Select one or more .dm files that you want to analyze.
2. **Automated Analysis:**
    - After loading the data, click the "Start" button.
    - The ASAP algorithm will automatically process the loaded .dm files and generate profiles.
3. **Viewing Results:**
    - The analysis results can be viewed directly in the UI window.
    - Explore the original image, restored image, and the calculated radial profile for detailed insights into the material's structure.
4. **Saving Output:**
    - Utilize the buttons in the "Save" section to save images and spectra obtained from the analysis.
    - Click on the respective buttons to save the visualized data in your desired format.

## Test Data
The `/test` folder contains sample electron diffraction pattern images for testing the ASAP algorithm. You can use these images to validate the functionality of the algorithm.
