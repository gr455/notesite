**NORMAL INSTALLATION**

1. run `pip3 install -r requirements.txt` to install all requirements

2. copy settings.py.example into settings.py `cp website/settings.py.example website/settings.py` from the root directory

3. go to 'website/settings.py' and change `DEBUG` to True

4. go to 'website/settings.py' and change `SECRET_KEY` to any string of significant length

5. run `python3 manage.py migrate` to run all migrations and setup the database

6. run `python3 manage.py runserver` to start the server at localhost:8000


**DOCKER INSTALLATION**

1. install Docker

2. go to 'website/settings.py' and change `DEBUG` to True

3. go to 'website/settings.py' and change `SECRET_KEY` to any string of significant length

4. run `docker build -t notesite .`

5. run `docker run -it -p 8000:8000 notesite`

6. the server will start at localhost:8000


The app is deployed at <a href = "http://gr455.pythonanywhere.com">gr455.pythonanywhere.com </a>

Note that the e-mail feature will not work in your local fork.