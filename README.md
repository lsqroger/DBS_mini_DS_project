# Music Genre Classification Project

## Project Overview
The objective of this project is to build a classifier to classify music genres of provided music pieces that are stored as structured data. Linear and non-linear machine learning models were explored, and a best model was selected as final classifer based on test performance. Subsequently, a web application utilizing FastAPI and sqlite database is built with the final classifier incorporated, to serve as a lite music genre classifier. The application is also containerized through Docker for maintainability and extendability.

<br />

## Installation & Requirements
Docker 20.10.7 <br />
Python 3.8.8

pandas==1.2.4<br />
numpy==1.20.1<br />
scikit-learn==0.23.2<br />
uvicorn==0.14.0<br />
fastapi==0.67.0<br />
xgboost==1.4.2<br />
lightgbm==3.2.1<br />
python-multipart==0.0.5

<br />

## Usage
In the root directory:<br /> 
'app' folder wraps the classifier web application.<br /> 
Inside 'app' folder:
* 'models' folder:  contains the final ML model and other related serialized objects for implementing the web service.
* 'tests.py': for unit tests of the web application.
* 'music.db': sqlite database for the web application<br /> 

'notebook' folder contains the jupyter notebook for data exploration and modelling experimentation.<br /> 
'Dockerfile' is for the containerized web application.<br /> 


To run the containerized web application:<br /> 
1. Build docker image and run container (port==8000) using 'Dockerfile'.
2. Open the prompted url (i.e. 'http//127.0.0.1:8000').
3. Divert to the homepage of API by adding suffix '/docs' (i.e. '127.0.0.1:8000/docs').
4. 3 functions provided by the web application are displayed:<br />![a](./others/screenshots/im1.png)<br />
5. Function 'Get Titles of Selected Genre' will return a list of song titles that belongs to the provided genre. To use the funtion, a genre name needs to be given as input.<br />![a](./others/screenshots/im2.png)<br /> Example of output:<br />![a](./others/screenshots/im5.png)<br /> 
6. Function 'List of Classified Genres' will show all classified/predicted genres for songs that are already input to and analyzed by the classifier. No user inputs are needed here.<br /> Example of output: <br />![a](./others/screenshots/im4.png)<br />
7. Function 'Predict' will predict the genres of songs provided by the user. The input format should be an external .csv file that will be uploaded to the website (Only single file upload is valid). As illustrated below:<br />![a](./others/screenshots/im3.png)<br /> Example of output: <br />![a](./others/screenshots/im6.png)<br />
8. Once 'Predict' function is performed successfully, titles of provided songs and corresponding classified genres will be stored to the database automatically.

