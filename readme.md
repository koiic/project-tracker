## Project Tracker

This is a project and task management tool built with flask and postgresql .

## Description

The **Project Tracker application** keeps tracks of users tasks based on priority/ and also gives the manager the ability to assign task.

## Key Application features

1. Manage Projects
2. Manage Task
3. Assign User to projects and tasks

## Technology Used
 * Python(Flask)
 * Postgresql
 * Docker
 * SQLALCHEMY
 * MARSHMALLOW
  
 ## Implementation Details
 1. Managing project
    - creating a new project
        - url : http://localhost:5000/api/v1/5000/projects
        - example request data 
        - `{
            "title":"mevron 1003",
             "description": "user authentication",
             "due_date": "2020-07-23 00:00:00",
              "assignees": []
	     }`


## Set Up Development With Docker 

1. Download Docker from [here](https://docs.docker.com/)
2. Set up an account on Docker
3. Install Docker after download
4. Go to your terminal run the command `docker login`
5. Input your Docker email and password

To setup for development with Docker after cloning the repository please do/run the following commands in the order stated below:

-   `cd <project dir>` to check into the dir
-   `docker-compose build` to build the application images
-   `docker-compose up -d` to start the api after the previous command is successful

The `docker-compose build` command builds the docker image where the api and its postgres database would be situated.
Also this command does the necessary setup that is needed for the API to connect to the database.

The `docker-compose up -d` command starts the application while ensuring that the postgres database is seeded before the api starts.

To stop the running containers run the command `docker-compose down`


**To Clean Up After using docker do the following**

1. run this command `docker ps` to view all docker images
2. run `docker stop ${image-id}`
2. run `docker rm ${image-id}`

**URGENT WARNING** PLEASE DO NOT RUN THE CLEAN-UP COMMAND ABOVE UNLESS YOU ARE ABSOLUTELY SURE YOU ARE DONE WITH THAT DEVELOPMENT SESSION AND HAVE NO DATA THAT WOULD BE LOST IF CLEAN-UP IS DONE!


### Alternative Development set up
    ##### BACKEND SET UP
     -   Clone the favorite-things repo and cd into it:
            git clone https://github.com/koiic/favorite-things
        
    -   CD into server folder 
    
    -   Create a .env file using the sample from .env.sample
    
    -   Check that python 3 is installed:
    
        ```
        python --version
        >> Python 3.7
        ```
    
    -   Install pipenv:
    
        ```
        brew install pipenv
        ```
    
    -   Check pipenv is installed:
        ```
        pipenv --version
        >> pipenv, version 2018.6.25
        ```
    -   Check that mysql is installed:
    
        ```
        postgresql --version
        postgres (PostgreSQL) 12.2
        ```
    
    -   Install dependencies:
    
        ```
        pipenv install
        ```
    
    
    -   Make a copy of the .env.sample file  and rename it to .env and update the variables accordingly:
    
        ```
        FLASK_ENV = "development" # Takes either development, production, testing
        DATABASE_URI = "postgres://YOUR_DB_USER:YOUR_DB_PASSWORD@YOUR_HOST/YOUR_DATABASE_NAME" # Development and production mySql db uri
        TEST_DATABASE_URI = "mysql+pymsql://YOUR_DB_USER:YOUR_DB_PASSWORD@YOUR_HOST/YOUR_TEST_DATABASE_NAME" # Testing mySql db uri
        JWT_SECRET_KEY_STAGING = "" # your prefered secret key
        API_BASE_URL_V1 = "" # The base url for V1 of the API
        ```
    
    -   Activate a virtual environment:
    
        ```
        pipenv shell
        ```
    
    -   Apply migrations:
        ```
        flask db init or python manage.py db init
        ```
    
        ```
        flask db upgrade or python manage.py db upgrade
        ```
        
        ```
        flask db migrate or python manage.py db migrate
        ```
    
    
    
    -   Run the application with either commands:
    
        ```
        python manage.py runserver 
        ```
        or
        ```
        flask run
        ```
    
    -   Should you make changes to the database models, run migrations as follows
    
        -   Migrate database:
    
            ```
            flask db migrate
            ```
    
        -   Upgrade to new structure:
            ```
            flask db upgrade
            ```
    
    -   Deactivate the virtual environment once you're done:
            ```
            exit
            ```  

 ##### TEST RUNNER
    -   CD into server folder 
    
    -   run test with the command below:
    
        ```
        pytest
        ```
 
 
 
  ### Step taken to autolint code

    For the server side I made use of PYLINT:
        this is a linting tool for python that help me follow the python style guide