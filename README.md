# Cloud Proyecto 0 2021-10
### Leidy Romero

Proyecto 0 para el curso Desarrollo de soluciones cloud ISIS4426 de la Universidad de los Andes semestre 2021-10.
Desarrollo basado en el tutorial: https://flask.palletsprojects.com/en/1.1.x/tutorial/

### Aclaraciones (Importante leer)
Desarrollado con el framework Flask y con HTML/CSS. Se incluyen peticiones POST y GET como sustitutas de las peticiones PUT y DELETE pues HTML únicamente soporta dichos metodos. Se realiza la configuración de autenticacion de postman por medio de una autenticación básica, la cual no funciona por lo que fue necesario eliminar los decoradores "@login_required" de la aplicación; de lo anterior hay que aclarar que la aplicación en el navegador funciona correctamente, sin embargo los cambios son necesarios para realizar las pruebas con postman. La seguridad de las contraseñas de la aplicación la maneja la librería werkzeug.

En algunas de las peticiones se utiliza el objeto "g" de flask para asociar la solicitud con el usuario actual. Ej Crear un nuevo evento requiere el id del autor en la base de datos. Debido a que no se logró realizar la autenticación en postman, el valor que toma el objeto "g" debe ser remplazado por una cookie en la solicitud llamada "autor" con el valor respectivo.

Debido a que el back y el front no estan separados, las respuestas a las solicitudes son HTML ya que en el codigo se redirige a el template respectivo.
Base de datos en SQLite

### Instalación
Una vez descargado el repositorio y creado el ambiente virtual, se debe ejecutar el comando "pip install -r requirements.txt".

Posteriormente se ejecuta la aplicación con los siguientes comandos (en linux):

export FLASK_APP=ABC

export FLASK_ENV=nombre_ambiente_virtual

flask run

### Ejecución
Servidor en ejecución en: 172.24.98.172:5000


### Documentación Postman
https://documenter.getpostman.com/view/7603343/TW71m6fA
