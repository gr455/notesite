1. run `pip3 install -r requirements.txt` to install all requirements

2. go to 'website/settings.py' and change `DEBUG` to True

3. go to 'website/settings.py' and change `SECRET_KEY` to any string of significant length

4. run `python3 manage.py migrate` to run all migrations and setup the database

5. run `python3 manage.py runserver` to start the server at localhost:8000


The app is deployed at <a href = "gr455.pythonanywhere.com">gr455.pythonanywhere.com </a>
