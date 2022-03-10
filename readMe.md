# NY City School Explorer
How does the environment influence the graduation rate of New York City High Schools? We are going to enable users to discover the connection between diffferent environmental aspects and the graduation rate of a school. We give the users the possibility to search between different features in the environment, see the results, get predictions of the graduation rate depending on these features and finally choose the high school, which we predict to have a good graduation rate in the New York City. We can also find out which schools are at risk and help discover connections between the environment and the graduation rate.

## Dataset Description

Data Source:
* all data from the NYC OpenData website (https://opendata.cityofnewyork.us/data/)

Data description
* Label: 
  * Graduation Percentages
* Features 
  * Trees 
  * Vehicle crashes
  * Public computers
  * Shootings
  * Arrests
  * After-School programs
  * Public Recycling Bins
 
For each features we need some kind of location (Latitude & longitude)and use location to calculate number of features in the neighborhood of each school.


## Implementation Technologies

### Data preprocessing:
* Pandas 
  * create new attributes, aggregate & connect different datasets
* Location/ finding neighbours
  *  Haversine formula

### Machine Learning:
* Classification
  * scikit: Regression & KNN

### Visualization & Web Application:
* Plotly & Dash
  * Dash for the deployment of the website 
  * Plotly for the visualization
  * Both together to make it interactive


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
### Data Preprocessing
Get all features from the NYC open data API
* Schools & Graduation Rate, trees, vehicle crashes, public computers, shootings, arrests, after-school programs, public recycling bins
Calculate the number of features in the neighboorhood (500m radius) of each school 
* For example: the number of trees in a 500m radius around East Side Community School, repeat for each feature & school
Get average graduation rate for each school
* Because we do not have data from each year for each feature, we use the average graduation rate of a school
Normalize data for Machine Learning
* As all the features are highly diverse in numbers, we normalize all the features using the mean and the standard deviation

### Machine Learning
We use the KNN-Algorthim to classify the graduation rate of each school in 5 steps: very bad, bad, neutral, good, very good. These labels are designed by us and contain the same number of schools. What label a school get, depends on the average graduation rate. For example the top 20% get the label very good.
The trained model is then used to predict the graduation rate of the schools in our dataset and also to predict the graduation rate based on the input from the sliders.

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

## Demonstration
A short demonstration of the project can be found at: https://youtu.be/j1uODC1_F1g

## Ideas for further improvement
#### Data 
Right now we are aggregating the data of each school for each feature, this should be improved, so that we can have each feature for each year. This should also allow a better prediction.
Another improvement would be to automate the data preprocessing, so that if new data is added by New York City, it would be updated automatically.
### Application
It would be nice to have some kind of connection between the different visualizations. For example a school clicked in the map, could also be highlighted in the scatter plot. 
Furthermore the possibility to pick two or more schools on the second page to compare them would be helpfull.

## Contributors
Mahsasadat Nezamabadi
Laura Sielenkemper
Clara Siepmann [GitHub](https://github.com/clara-hue)
