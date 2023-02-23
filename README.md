# Reserva de habitaciones en Santa

App web para la gestión de reservas diaras de habitaciones.

# Contributing

```
 git clone git@github.com:cmdelatorre/reservas_santa.git
 cd reservas_santa
 pyenv virtualenv 3.10.3 reservas_santa
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

## Para desplegar en PythonAnywhere

https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/

Luego siguiendo esto: https://help.pythonanywhere.com/pages/environment-variables-for-web-apps

Hace falta un `reservas_santa/website/.env` con las envvars para producción.

# DB


### TBD
1. Cuenta definitiva en PythonAnywhere
  1. Crear cuenta
  2. Configurar app
    1. Voy por acá: https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/#additional-configuration
1. Migrar datos
  1. Usuarios
  2. Reservas. Ojo con las relaciones, que cambiarán los IDs ?
  3. Scriptearlo para dsps hacerlo de una en la cuenta definitiva. ?


Esto:
```
?: (mysql.W002) MySQL Strict Mode is not set for database connection 'default'
        HINT: MySQL's Strict Mode fixes many data integrity problems in MySQL, such as data truncation upon insertion, by escalating warnin
gs into errors. It is strongly recommended you activate it. See: https://docs.djangoproject.com/en/2.2/ref/databases/#mysql-sql-mode
```
