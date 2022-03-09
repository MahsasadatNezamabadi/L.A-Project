# NY City School Explorer
here short description of the project

## Dataset Description
## Implementation Technologies
## App Structure
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
