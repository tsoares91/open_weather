# Data Engineer Challange
The scope of this challange was based on the following statemant:
    
    Your team has successfully integrated major data sources such as Web Tracking Data
    capturing user interactions as well as other back-end data sources into a central data
    platform. Data Scientists working with this data would now like to be able to test various
    hypothesis. For this they ask the data engineers to start collecting data from various
    external data sources.

    You have been asked to build a data pipeline to collect daily weather data from a publicly
    available API (https://openweathermap.org/) using Python, the language chosen by your
    team.
    • Include a reasonable set of data fields including date and temperature from
    https://openweathermap.org/current for a list of cities provided in a config file.
    (Data can be stored in local files in a suitable format or a DB.)
    • Please try to provide a well-structured, self-contained and “dockerized” python
    project.


The objective of this challange was to understand better how I code and what approach do I take.
Important consideration were :
  - Unit testing.
  - CI/CD
  - Docker
  - Documentation 
  - OOP Principals
    
To start this off I had to get an account on the openweather and get an api token to be able to request the data from the api. After having access to the API and a list of cities to be called (listofcities.csv) I had to then create the python script.
## Python Script
My main approach was to divide my script in 4 main components.
  - WeatherDataFetcher - here the objective was to create the request to the API based on some variables (City name,API Key and Units) to retrieve a JSON with the information that was required.
  - WeatherDataProcessor - on this function my objective was to first make sure that I was able to fetch the city (the request wasn't sending 404) and then flatten the Json. It is important to note that i've brought all the columns as they existed on the original request, however i've created a new column called 'date_time' that is a transformation on top of the column DT to be easier for they eye to see the date.
  - WeatherDataSaver - this function was responsible for saving the information flattened into a csv file. I had just a few safeguards if the file didn't exist, it would create with a header and if it already existed would only append the new data processed. The file would be created with the name of 'weather_data.csv'
  - WeatherApp - Finally we had the last function that worked as an orchestrator that called the above functions and printed some additional information based if the city was ran or not.
## Unit Test
So having this in mind my approach was to use <a href= "https://docs.python.org/3/library/unittest.html">unittest library</a>. The test itself focus on 2 functionalities and the python is : file ut_unittest.py .
 - test_weather_app: Tests the normal run, ensuring that data for multiple cities is fetched and saved.
 - test_city_not_found: Tests the scenario where a city is not found (404), verifying that the appropriate error message is printed.
## CI/CD 
I used github actions to create a CI/CD Plan. On this plan i had 4 steps:
1. Connect with the docker to run my image
2. Second, run the pep8 to make sure everything is okay according to it
3. If the first step, ran okay then make sure the 'main_opp.py' script ran without any errors
4. Finally, run the ut_unittest.py.
## Docker
I've created this docker image to allow the script to be run independetly of my machine and to make it easier to accomodate the resources required. You can access the image with the following command using <a href= "https://www.docker.com/products/docker-hub/"> Docker </a>:

    docker pull tsoares91/open_weather:latest
    
## Documentation    
For this I've used github to make sure I had all the documentation needed in one place.
## OOP Principals
To achieve this I refactor all the code using the OOP principals(Functions and classes) and I've also included the flake8 to keep the code more lean and cleaner.
    
# Requirements
  - Requests (2.32.3)
  - Pandas (2.2.2)
  - mock (5.1.0)
  - Python (3.12.4)

# Dataset


- On the following file, listofcities.csv make sure to add or change the list of cities to run

- Source Data API - <a href= "https://openweathermap.org/current">Open Weather Current</a>

# How to use    
## Local Machine (repositories)
To run the script, please following steps:

1. Download this repository
2. Change the configuration file of the cities to be run (if needed)
3. Inside the folder open_weather, open terminal and use the following command.
    
        python3 main_opp.py
4. Check the output file, weather_data.csv

## Docker
To run with docker with the default configuration file, you need to open terminal (make sure to have docker running in your machine)
    
Use the following commands:
    	
    1.docker pull tsoares91/open_weather:latest
    2.docker run -it --name wd tsoares91/open_weather:latest /bin/bash
    3.python3 python/main.opp.py


## Credits
### Original Data
* <p> <a href= "https://openweathermap.org/"> OpenWeather
 </a> </p>


