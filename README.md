# quiz-application
A Quiz Application made with Django and HTMX

## How to install

1. Clone the repository using the following command
```
git clone https://github.com/vivekthedev/quiz-application.git .
```

2. Create a python virtual environment to install dependencies
```
python -m venv env
```

3. Activate the envrionment according to your machine type:
   
  - (Windows) `env\Scripts\activate`
  - (Mac/Linux) `source bin/activate`

4. Install the dependencies in virtual envrionment.
```
pip install -r requirements.txt
```

6. Migrate Database to create tables in SQLite
```
python manage.py migrate
```

6. Run the Django Server
```
python manage.py runserver
```


