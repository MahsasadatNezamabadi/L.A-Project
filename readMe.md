# NY City School Explorer
here short description of the project

## Dataset Description
## Implementation Technologies
## App Structure
The application is split in two parts: the preprocessing and the application.
### Structure of the application
This is the structure as seen in the main branch. To deploy the application, this is the only needed branch.
* index.py: used to create an application with more than one page, file to execute the application
* app.py: start application server
* final_model.sav: KNN model used to predict graduation rate, the model is generated in the preprocessing part of the application
* datasets: folder which contains all the data necessary for the application. The files are generated in the preprocessing part
  * 2016_DOE_High_School_Directory-2.csv: the locations of the schools
  * dataForScatter.csv: all the data needed for the scatterplot: Features & Borough
  * meanStd.csv: needed to normalize the data, we get from the input of sliders
  * dataForML.csv: normalized featured, used to predict the graduation rate
* assets: additional files for the application, such as css files and images
* apps: folder, contains the webpages
  * ScatterDropDown.py: contains the page Discover the Data with the map & the scatterplot
  * mlPart.py: contains the page Predict the Graduation Rate with the sliders and the graduation cap
  * startPage.py: contains the page shown when the application is loaded
  * getPrediction.py: is the method used to generate a prediction using final_model.sav 
### Structure Pre-processing
Here the datasets and the KNN model is generated. The code for this can be found in the branch basicData
* DataPreprocessing.ipynb: Here the data is fetched from the NYC open data API and all the features are calculated as well as standardized.
* Regression.ipynb: Contains the first idea for a regression model. This was ignored later on, as it did perform poorly (accuray: lower than 0.04)
* classification.ipynb: Here the KNN model is trained. The reached accuracy is still not good, but better than in the regression model (accuracy: 0.4)
* datasets: Here are the generated datasets saved as well as the ones downloaded from the NYC open data api


## Machine Learning Pipeline
## Visualization
The first visualizations are used to give the user an overview of the data. Hence we use a map and a scatterplot.
![Map and Scatterplot from the data of the NYCSchools](https://github.com/MahsasadatNezamabadi/L.A-Project/blob/main/ImagesForReadMe/GraduationRate.png?raw=true)
The second visualization is used to illustrate the predicted graduation rate of the school.
![Visualization of the graduation rate via a color changing graduation hat](https://github.com/MahsasadatNezamabadi/L.A-Project/blob/main/ImagesForReadMe/ScatterPlotMap.png?raw=true)
## Deployment
First make sure that you have installed the following requirements:

```
pip install dash == 2.2.0
pip install dash-bootstrap-components == 1.0.3
pip install plotly == 5.6.0
pip install pandas ==  1.4.1
pip install scikit-learn == 1.0.2
```
Then either clone the repository or download the main-branch. In the folder with the code execute ```python index.py.```
The application should be accessible at http://127.0.0.1:8050/

## Ideas for further improvement
#### Data 
Right now we are aggregating the data of each school for each feature, this should be improved, so that we can have each feature for each year. This should also allow a better prediction.
### Application
It would be nice to have some kind of connection between the different visualizations. For example a school clicked in the map, could also be highlighted in the scatter plot. 
Furthermore the possibility to pick two or more schools on the second page to compare them would be helpfull.
