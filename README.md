# RespondITE


## DESCRIPCION

Chat IA dirigido al área de Servicios Escolares. Brinda respuestas automáticas a preguntas frecuentes de estudiantes (credenciales, constancias, etc). El sistema permite a los alumnos comunicarse de forma rápida y sencilla con Servicios Escolares, resolviendo sus dudas.

## Requisitos previos:
Antes de comenzar asegúrate de tener instalado:
* Python 3.10 o superior
* pip (el gestor de paquetes de Python)
* Un navegador web (como Chrome, Edge, etc.)

### PYTHON Y PIP:
Python puede ser intalado de manera gratuita desde la siguiente pagina:
````
https://www.python.org/downloads/
````
Una vez dentro debe de seleccionar la siguiente opción:


![Pagina de descarga para python](https://github.com/debby019/RespondITE/blob/f026fd8aba9887962a6eb3795746fe7ef05d5920/Img/pythonw.png)


Al momento de la instalación es necesario seleccionar `add python.exe to PATH` como se muestra en la siguiente imagen:


![Añadir python al path](https://github.com/debby019/RespondITE/blob/f026fd8aba9887962a6eb3795746fe7ef05d5920/Img/py.png)


## PROCEDIMIENTO DE LA INSTALACION
Para comenzar a utilizar el proyecto de sebe de descargar o clonar el repositorio en su computadora:
(imagen de repositorio)

Posteriormente, dentro de la carpeta **Backend** se deben de instalar las siguientes dependencias:

1. fastapi
````
pip install fastapi
````
2. Uvicorn (servidor ASGI para correr FastAPI)
````
pip install uvicorn
````
3. bcrypt 3.2.2 (cifrado de contraseñas)
````
pip install bcrypt==3.2.2
````
4. passlib 
````
pip install passlib
````
5. python-multipart (para manejar datos tipo formulario)
````
pip install python-multipart
````
### EJEMPLO:
(Imagen de ejemplo)

### .env
Dentro de la carpeta **backend** debemos de crear un archivo .env el cual contendra las siguientes claves
````
SUPABASE_URL=https://nulsoiwjscvaxzxyjfgm.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im51bHNvaXdqc2N2YXh6eHlqZmdtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDI0NDgzMzcsImV4cCI6MjA1ODAyNDMzN30.WeWkC1Migmn8QKYI3XjvQ0CEnHo4eizH5_XImTvHfzw

````
## EJECUCION DEL PROGRAMA
Para acceder a la pagina se debe de ejecutar el backend utilizando el siguiente comando 
````
uvicorn main:app --reload 
````
**EJEMPLO**

Si se ejecuto correctamente se debe de mostrar algo como lo siguiente:

Una vez realizado esto abrimos el index.html ubicado en ResponditeFront/html:

## BASE DE DATOS


## INTEGRANTES

* Angel Gabriel Angulo Martinez
* Devorah Alonso Hernandez
* Coral Castillo Escareño
* Cindy Geraldine Gaynor Zurita
* Eduardo Isidro Zerega Navarro


## DOCUMENTACION DEL PROYECTO
https://docs.google.com/document/d/10h7pLpEBXtmWTo4oB6SFLlp6qxqKaanPCsaNdrUysp4/edit?usp=sharing
https://docs.google.com/document/d/1Ni4Il5Mt78Dfs0u8sqNUp94qgDhu4KBvLK2cK7gzpLs/edit?usp=sharing
