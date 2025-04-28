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
![ZIP](https://github.com/debby019/RespondITE/blob/ba4ab87f3263b444f53e4fbbc5f4cc6b18b347dd/Img/main.png)

### Instalación de dependencias
En la terminal, dentro de la carpeta backend, instala las siguientes dependencias:

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
![instalacion de libreria](https://github.com/debby019/RespondITE/blob/ba4ab87f3263b444f53e4fbbc5f4cc6b18b347dd/Img/instalacion.png) <br/>

### Archivo .env
Dentro de la carpeta **backend**, crea un archivo llamado .env con las siguientes claves
````
SUPABASE_URL=https://nulsoiwjscvaxzxyjfgm.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im51bHNvaXdqc2N2YXh6eHlqZmdtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDI0NDgzMzcsImV4cCI6MjA1ODAyNDMzN30.WeWkC1Migmn8QKYI3XjvQ0CEnHo4eizH5_XImTvHfzw

````
## EJECUCIÓN DEL PROGRAMA
Dirígete a la carpeta backend desde la terminal y ejecuta el siguiente comando:
````
uvicorn main:app --reload 
````
**EJEMPLO** <br/>
![Ejecucion main](https://github.com/debby019/RespondITE/blob/ba4ab87f3263b444f53e4fbbc5f4cc6b18b347dd/Img/main.png)<br/>


Si la ejecución fue exitosa, deberías ver algo como lo siguiente:<br/>
![Ejecucion main2](https://github.com/debby019/RespondITE/blob/ba4ab87f3263b444f53e4fbbc5f4cc6b18b347dd/Img/ejecucion.png)<br/>

Una vez que el servidor esté corriendo, abre el archivo index.html, ubicado en la carpeta ResponditeFront/html, en tu navegador.<br/>
![index](https://github.com/debby019/RespondITE/blob/ba4ab87f3263b444f53e4fbbc5f4cc6b18b347dd/Img/index.png)<br/>


## INTEGRANTES

* Angel Gabriel Angulo Martinez
* Devorah Alonso Hernandez
* Coral Castillo Escareño
* Cindy Geraldine Gaynor Zurita
* Eduardo Isidro Zerega Navarro


## DOCUMENTACION DEL PROYECTO
https://docs.google.com/document/d/10h7pLpEBXtmWTo4oB6SFLlp6qxqKaanPCsaNdrUysp4/edit?usp=sharing
https://docs.google.com/document/d/1Ni4Il5Mt78Dfs0u8sqNUp94qgDhu4KBvLK2cK7gzpLs/edit?usp=sharing
