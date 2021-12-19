# Investigacion final Independiente Reddit Sentiment Analysis
Universidad de Puerto Rico Recinto de Rio Piedras<br>
Departamento de Ciencias de Computo<br>
CCOM3031: Introduccion a la Ciencia de Datos<br>

## Introduccion

Este proyecto incluye loa implementacion de un programa que utiliza el API de Reddit para recoger informacion de una comunidad dentro de Reddit (estas se llaman subreddits).Con esta informacion y la ayuda del paquete NLTK para python y su modelo entrenado llamado VADER se hace analisis de sentimiento sobre las publicaciones de esta comunidad. Esto permite determinar si una comunidad tiene publicaciones predominantemete positivas, negativas o neutrales. Esto da informacion a los usuarios sobre como es la naturaleza de las publicaciones en una comunidad antes de unirse a ella a traves de graficas e imagenes. En este proyecto tambien se hizo uso de la capacidad del programa para generar archivos .csv sobre los datos que recoge. Se tomaron datos de comunidades politicas y se analizo estos datos para probar la utilidad de este tipo de datos de una manera aplicada a unas comunidades especificas. Este analisis se presentara en google collab a traves de un Jupityer Notebook. 

En un intento por facilitar el proceso de inteactuar con el codigo para probarlo con distintos nombres de comunidades y poder apreciar los resultados se creo una pagina web utilizando flask para ligarla al codigo fuente de este proyecto. Esto permite correr el programa desde una sencilla pero funcional interfaz grafica en la intenet. El mismo es publicado utilizandfo un servicio gratis llamado herokuapp la cual tiene sus limitaciones por lo cual es un poco lento, sin embargo, sigue siendo totalmente funcional para ver elprograma en accion. Para utilizarlo solo se pone el nombre de la comunidad (subbreddit) y la cantidad de pubicaciones que se quieren analizar dentro de esa comunidad.

Enlace:
[Enlace para la solucion web](https://redditanalisys.herokuapp.com/)
[Github de la pagina web](https://github.com/jasielrt95/Reddit-Flask-Website)

Los componentes implementados son:
- La definicion de la clase RedditAnalysis dentro de reddit_analysis.py
- La aplicacion haciendo uso de la instancia de la clase para analizar los datos del subreddit
- Una Jupyter Notebook con el analisis sobre los subreddits politicos
- Un folder llamado Data que contiene los datos necesarios para correr el Jupiter Notebook en google collab

### reddit_analysis.py

Este archivo contiene la definicion de la clase que se utlizan en el archivo de la applicacion para realizar los analisis aobre los datos obtenidos de Reddit. Las funciones definidias dento de la clase RedditAnalysis son: 

* self 
    Funcion constructora para la clase. Tambien obtiene las credenciales del API de Reddit y se conecta con el. 
* subreddit_info 
    Esta funcion recoge, organiza y depura los datos obtenidos de la comunidad dada en Reddit.
* subreddit_sentiment
    Esta funcion genera un diccionario que clasifica las publicaciones de acuerdo a su sentimiento.
* subreddit_word_frequency
    Genra un diccionario on la informacion de cuantas veces se repite cada palabra dentro de la informacion recogida. 
* top_words_graph
    Genra un grafica de barras que representa las palabras mas populares dentro de la comunidad. 
* get_positive_posts
    Esta funcion busca todas las publicaciones positivas y las guarda en una lista
* get_negative_posts
    Esta funcion busca todas las publicaciones negativas y las guarda en una lista
* get_neutral_posts
    Esta funcion busca todas las publicaciones neutrales y las guarda en una lista
* get_top_posts
    Esta funcion busca todas las publicaciones para identificar las mas populares/recientes y las guarda en una lista
* subreddit_wordcloud
    Esta funcion genera una imagen que tiene un word cloud donde las palabras mas grandes son mas frecuentes y las mas pequenas son menos frecuentes.
* subreddit_sentiment_piechart
    Esta funcion geera una grafica circular que representa en terminos de porciento cuantas publicaciones del total son positivas, negativas y neutrales
* makeCSVFile
    Crea un archivo .csv con los datos del subreddit
* makeCSVFileForFreq
    Crea un archivo .csv especificamente para los datos recopilados de frecuencia
* getWordsRepeatedSubreddits
    Obtiene las palabras informacion de las palabas repetidas ya sean positivas o negativas
     
### app.py.

Este archivo es el que hace correr la aplicaion. Contiene el uso de todas las funciones de la clase creada en redit_analysis.py a traves de una instancia de la clase que se utiliza para analizar los datos del subreddit seleccionado

### Reddit_Project.ipynb.

Contiene analisis de datos sobre algunas de las comunidades politicas dentro de reddit. Especificamente, politics,world news, conservative, libertarian y democrats. 

Para correr esta libreta de Jupyter en google collab se deben anadir todos los archivos dentro del folder llamado "Data" qu se encuentra entre los archivos del proyecto.

### RevisionLiteraria

Este archivo contiene el trabajo escrito de investigacion que se ralizo como "background" o base para realizar este proyecto.

### requirements.txt

IMPORTANTE. Este archivo contiene todas paquetes que se deben instalar con pip install a python para que el programa pueda correr en un ambiente de programacion (IDE) de manera local. (se le recuerda al lector que existe una solucion web para probar el programa sin tener que pasar por este proceso).

Se debera usar:

pip insatll requiremets.txt 


### Como correr el programa de manera local 

Dentro de los archivos del proyecto se encuentra todo lo necesario para correr el programa de manera local en una computadora. Primero se necesitara tener instalada en la maquina una version de Python 3.  Luego se tendra que utilizar

pip install requirements.txt 

para instalar todos los paquetes necesarios para que el programa corra. Una vez este proceso se haya completado con exito entonces se visita el archivo app.py. En el mismo en la linea 18 en el primer parametro para la llamada a la funcion subreddit_info utilizando las comillas "" pondra el nombre de la comunidad (subreddit) que desea analizar. Una vez esto sea completado y guardado se debe correr el archivo app.py y le debe salir todas las graficas resultantes de la busqueda y el analisis sobre la comunidad que selecciono.

Si no desea hacer todo esto, una vez mas puede utilizar la alternativa en el internet (web based) para correr el programa accediendo en:

[Enlace para la solucion web](https://redditanalisys.herokuapp.com/)
