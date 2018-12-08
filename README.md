# Fydlyty2 deployment instructions (Mac, Windows, Linux)

1. checkout project from repository
2. configure your database settings in settings.py and create a database
3. install packages from requirements.txt using pip install -r requirements.txt
4. run ./manage.py syncdb
5. run ./manage.py migrate
6. run development server using ./manage.py runserver 0.0.0.0:8080
