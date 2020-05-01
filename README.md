# WebSem_EmoSentiMovieOnt
Work done in the course of Semantic Web, in which we perform an sentiment and emotion extraction from movie synopsis to populate marl, and onyx ontologies joined with the DBPedia movie ressource. Data is then displayed in a simple web app using Django.

#Structure:
    app_images - Directory of images showing the app
    MyStore - rdflib graph for data storage
    webproject - Django files
        * catalog - Files for webapp, includes templates and backend logic
        * webproject - Django settings specifications
    DataProcessing.py - Movie data extraction, emotion and sentiment assignment using NRC lexicon
    newData.csv - Dataset used
    nrc_lex.csv - Available [here](https://saifmohammad.com/WebPages/NRC-Emotion-Lexicon.htm)
    requirements.txt - Modules used for this project
    WebSemantica.pdf - PDF file written in Portuguese describing all the work done
    
#Instructions:
    1. Use DataProcessing for creating processed data of movie sysnopsis with its sentiment and emotion assigned. Requires NRC Lexicon
    2. Start Django server by going to webproject directory and performs the command: python manage.py runserver
    3. Acess the web app by opening a browser and acess 127.0.0.1
    4. Enjoy
    
#App examples:
![Homepage](/app_images/img1.png)
![Results](/app_images/img2.png)
![QueryResults](/app_images/img3.png)
