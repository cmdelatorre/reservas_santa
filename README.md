# Reserva de habitaciones en Santa

App web para la gestión de reservas diaras de habitaciones.

# Contributing

```
 git clone git@github.com:cmdelatorre/reservas_santa.git
 cd reservas_santa
 pyenv virtualenv 3.7.0 reservas_santa
 pyenv local reservas_santa
 heroku login
 pip install -U pip
 pip install -r dev_requirements.txt
 python manage.py migrate
 ./manage.py runserver
 ```

# Admin

Seguí este tutorial para poner en marcha la app en Heroku:

https://devcenter.heroku.com/articles/getting-started-with-python

De paso, indica todo el tipo de operaciones que se pueden realizar.
