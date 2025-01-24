# chin-chin-tlacuachin
Aplicación web para el punto de venta de "Chin Chin Tlacuachín"

![](./src/static/img/login.png)

## Instalación de programas necesarios para ejecutar el punto de venta

### Sobre python3
Python3 no permite la instalación de paquetes sin un ambiente virtual, por lo que instalamos pip y venv para poder crear un ambiente virtual e instalar los paquetes que necesitemos.
```bash
$ sudo apt install python3-venv
$ sudo apt install python3-pip
```

Luego creamos el ambiente virtual con:
```bash
$ python3 -m venv <foo>
```

### Ambiente virtual
Activamos el ambiente virtual antes de instalar con pip
**activar**
```bash
$ source env_name/bin/activate
```

**desactivar**
```bash
$ deactivate
```

### Paquetes PIP
Se recomienda instalar manualmente los paquetes para tener la última version disponible
```bash
$ pip install Flask
$ pip install flask-sqlalchemy
$ pip install pymysql
$ pip install cryptography
$ pip install waitress
$ pip install livereload
```

### Verificar lista de paquetes
```bash
$ pip list
```

Los paquetes se pueden instalar automáticamente desde la lista de paquetes de `requirements.txt` como.
```bash
(foo)$ pip install -r requirements.txt
```

O si hay alguna modificación de paquete, guardar con:

```bash
(foo)$ pip freeze > requirements.txt
```

## Ejecutar proyecto

Ejecución en modo desarrollo:
```bash
$ python3 main.py
```

Modo producción. Necesitamos exportar las siguientes variables. Los
parámetros **--host y --port** nos dicen la ip y el puerto.**--call**
para regresar el objeto *Flask(__name__)*

```bash
$ export FLASK_APP=main
$ waitress-serve --host localhost --port=8080 --call main:cafeteria_alina
```



# SQL
Para poder conectarse la base de datos correctamente, se deben especificar correctamente las credenciales en el archivo
config.py
```python
 PORT: 3306 (usually)
 USERNAME: 'root' (usually)
 PASSWORD: 1234 (usually, or whatever the password is)
```
### Acceder desde la terminal
Para acceder a la base de datos desde la terminal (previamente configurada a la hora de instalar mysql)
```bash
$ mysql -u <user> -p 
$ 1234
```

También, ya debe de existir la base de datos antes de ejecutar el programa
```sql
mysql> CREATE DATABASE <database_name> 
```

 PIP libraries:

NPM dependecies

- mathjs
