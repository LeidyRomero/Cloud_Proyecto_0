# Cloud_Proyecto_0

Proyecto 0 para el curso Desarrollo de soluciones cloud ISIS4426 de la Universidad de los Andes semestre 2021-10.

Desarrollado con el framework Flask y con HTML/CSS. Se incluyen peticiones POST y GET como sustitutas de las peticiones PUT y DELETE pues HTML únicamente soporta dichos metodos. Se realiza la configuración de autenticacion de postman por medio de una autenticación básica, la cual no funciona por lo que fue necesario eliminar los decoradores "@login_required" de la aplicación; de lo anterior hay que aclarar que la aplicación en el navegador funciona correctamente, sin embargo los cambios son necesarios para realizar las pruebas con postman. La seguridad de las contraseñas de la aplicación la maneja la librería werkzeug.

Desarrollo basado en el tutorial: https://flask.palletsprojects.com/en/1.1.x/tutorial/
