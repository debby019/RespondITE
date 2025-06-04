# RespondITE


## DESCRIPCIÓN

Chat IA dirigido al área de Servicios Escolares. Brinda respuestas automáticas a preguntas frecuentes de estudiantes (credenciales, constancias, etc). El sistema permite a los alumnos comunicarse de forma rápida y sencilla con Servicios Escolares, resolviendo sus dudas.

## REQUISITOS PREVIOS
Antes de comenzar asegúrate de tener instalado:
* Python 3.10 o superior
* pip (gestor de paquetes de Python)
* Un navegador web (Chrome, Edge, etc.)

### INSTALACIÓN DE PYTHON Y PIP
Python puede instalarse de manera gratuita desde:
````
https://www.python.org/downloads/
````
Una vez dentro de la página seleccione la siguiente opción:

![Pagina de descarga para python](https://github.com/debby019/RespondITE/blob/f026fd8aba9887962a6eb3795746fe7ef05d5920/Img/pythonw.png)


Es importante seleccionar la opción **Add Python to PATH** durante la instalación, como se muestra en la siguiente imagen:


![Añadir python al path](https://github.com/debby019/RespondITE/blob/f026fd8aba9887962a6eb3795746fe7ef05d5920/Img/py.png)


## PROCEDIMIENTO DE INSTALACIÓN
Para comenzar a utilizar el proyecto, primero debes descargar o clonar el repositorio en tu computadora.
![ZIP](https://github.com/debby019/RespondITE/blob/aaca716c133c71c7ca929c538dba4a88160eb131/Img/descargar.png)

### Instalación de dependencias
En la terminal, dentro de la carpeta backend, instala las siguientes dependencias:

1. fastapi
````
pip install fastapi
````
2. supabase-py
````
pip install supabase
````
3. Uvicorn (servidor ASGI para correr FastAPI)
````
pip install uvicorn
````
4. bcrypt 3.2.2 (cifrado de contraseñas)
````
pip install bcrypt==3.2.2
````
5. passlib 
````
pip install passlib
````
6. python-multipart (para manejar datos tipo formulario)
````
pip install python-multipart
````
7. python-jose[cryptography] (JWT)
````
pip install python-jose[cryptography]
````
8. python-dotenv
````
pip install python-dotenv
````
9. pydantic
````
pip install pydantic
````
10. pip install requests
````
pip install requests
````

### EJEMPLO:
![instalacion de libreria](https://github.com/debby019/RespondITE/blob/6ca8a59e610d15c3e203c966aa511affc01948aa/Img/libreria.png) <br/>

### Archivo .env
Dentro de la carpeta **principal**, crea un archivo llamado .env con las siguientes claves
````
API_URL="url_ejemplo" 
API_KEY="key_ejemplo"

SUPABASE_URL="https://nulsoiwjscvaxzxyjfgm.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im51bHNvaXdqc2N2YXh6eHlqZmdtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDI0NDgzMzcsImV4cCI6MjA1ODAyNDMzN30.WeWkC1Migmn8QKYI3XjvQ0CEnHo4eizH5_XImTvHfzw"
SUPABASE_SERVICE_ROLE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im51bHNvaXdqc2N2YXh6eHlqZmdtIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0MjQ0ODMzNywiZXhwIjoyMDU4MDI0MzM3fQ.E74aXQZ8YJAIuWmt-5S7TmvlH6Qa5Pfwl20GiLzJ9oM"

SECRET_KEY="YGT1ayDJVyrsuLzFq-AY8P7iTJAGgMw584xA4rYPJ24"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=120
````
## EJECUCIÓN DEL PROGRAMA
Dirígete a la carpeta principal desde la terminal y ejecuta el siguiente comando:
````
uvicorn backend.main:app --reload 
````


Si la ejecución fue exitosa, deberías ver algo como lo siguiente:<br/>
![Ejecucion main2](https://github.com/debby019/RespondITE/blob/ba4ab87f3263b444f53e4fbbc5f4cc6b18b347dd/Img/ejecucion.png)<br/>

Una vez que el servidor esté corriendo, abre el archivo index.html, ubicado en la carpeta ResponditeFront/html, en tu navegador.<br/>
![index](https://github.com/debby019/RespondITE/blob/ba4ab87f3263b444f53e4fbbc5f4cc6b18b347dd/Img/index.png)<br/>


**Alternativa:**
<br/>
Otra forma de correr el servidor es:
Abrir una terminal y dirigirse a la carpeta principal del proyecto. Luego ejecutar el backend con el siguiente comando:
````
py -m backend.main
````
![Ejecucion back](https://github.com/debby019/RespondITE/blob/4482d212dfbd30b41ed56ac0830b47272625c2f1/Img/servidorBackend.png)<br/>
Posteriormente abrir una segunda terminal en la misma carpeta principal del proyecto y ejecutar el siguiente comando para iniciar un servidor local que sirva los archivos HTML:
````
py -m http.server 8000
````
![Ejecucion html](https://github.com/debby019/RespondITE/blob/4482d212dfbd30b41ed56ac0830b47272625c2f1/Img/servidorpython.png)<br/>

Una vez hecho esto, podras ingresar al sitio desde la siguiente dirección en tu navegador:
```` 
http://localhost:8000/ResponditeFront/html/index.html
````

### Base de Datos
La base de datos está alojada en Supabase, por lo que no es necesario importar ningún script SQL en un gestor local.  
El archivo `database_postgresql.sql` (ubicado en la raíz del proyecto) contiene las sentencias SQL usadas para crear las tablas, pero se incluye únicamente como referencia.  
La conexión a Supabase se gestiona automáticamente a través de las credenciales definidas en el archivo `.env`.

## INTEGRANTES

* Angel Gabriel Angulo Martinez
* Devorah Alonso Hernandez
* Coral Castillo Escareño
* Cindy Geraldine Gaynor Zurita
* Eduardo Isidro Zerega Navarro


## DOCUMENTACIÓN DEL PROYECTO
* DOCUMENTACIÓN DE REQUISITOS: https://docs.google.com/document/d/10h7pLpEBXtmWTo4oB6SFLlp6qxqKaanPCsaNdrUysp4/edit?usp=sharing
* DISEÑO DE SOFTWARE:  https://docs.google.com/document/d/1Ni4Il5Mt78Dfs0u8sqNUp94qgDhu4KBvLK2cK7gzpLs/edit?usp=sharing
* MANUAL TÉCNICO:  https://docs.google.com/document/d/1xZq7Lhf_lKsX-uqdW2Vm9_qiPsQswDNf5PnkB9H4Uyo/edit?tab=t.0
* MANUAL DE USUARIO:  https://docs.google.com/document/d/1HQe3x6ScGVsx00adY3QO4vtzWe2GkOsx/edit
