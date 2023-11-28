[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10208580.svg)](https://doi.org/10.5281/zenodo.10208580)

# ASAP
**A**uto **S**elected **A**rea diffraction patterns **P**rofiler (ASAP)

ASAP is a Python-based computational method developed for the automated interpretation of selected area diffraction patterns (SADP) in transmission electron microscopy. The approach utilizes advanced computer vision algorithms, including the random sample consensus (RANSAC) algorithm, to automatically generate structural profiles from electron diffraction pattern images.

## Getting Started
### Prerequisites
Make sure you have Python installed on your system. Additionally, install the required packages by running the following command:
```
conda create -n ASAP python=3.11
conda activate ASAP
pip install -r requirements.txt
```

### Running the UI
To run the UI, execute the following command in your terminal or command prompt:
```
python ASAP_UI.py
```

## Usage

<p align="center"><img src="https://github.com/sooyeonLim/ASAP/assets/52401652/debc6310-df45-44b9-a7ab-b0761f77a1ee" width = "90%" height="90%"/>


1. **Load Data:**
    - Click on the icon in the "Load Data" section to open a file dialog.
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

## Author Contributions
H-K.K. designed the work. S.L. and H.-K.K. carried out signal and image processing algorithms. S.L. acquired TEM-SADP images. S.L., H.-K.K., and I.-C.C. wrote the manuscript with contribution from all authors.

## Acknowledgements
We acknowledge financial support from a National Research Foundation of Korea (NRF) grant funded by the Korean government (Ministry of Science and ICT) (2021M3H4A6A02050353). 
