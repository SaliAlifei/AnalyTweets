# AnalyTweets

## Informations générales surla structure de l'application

* *data* : divers données utilisés dans le projets
* *parm* : contient les variables d'environnement comme les clés Twitter
* *settings* : c'est là que sont settés les variables présents dans parm et les constantes utilisées dans l'application
* *src/dashboard* : correspond au code de l'interface web
* *src/scripts* : repertoire contenant les algorithmes
* *venv* : environnement virtuel python dans lequel vont être installées toutes les bibliothèques de l'application 

## Installation

* Placez-vous à la base du projet (/AnalyTweets/) puis créez un environnement virtuel python et activez-le 

Commande Windows 
```
$ python -m venv venv
$ venv\Scripts\activate
```

Commande Linux
```
$ python -m venv venv
$ source venv/bin/activate
```

* Installer les bibliothèques présentes dans le fichier requirements.txt

```
pip install -r requirements.txt
```

* Modifiez la variable *PATH_TO_ENV_FILE* (dans settings) pour la faire pointer vers le fichier *env_var.env*
* Renseignez vos clés (obtenus en se connectant à l'API Twitter) comme variable d'environnement dans le fichier *env_var.env* du repertoire *parm*
  * *TWITTER_API_KEY*
  * *TWITTER_API_SECRET_KEY*
  * *TWITTER_ACCESS_TOKEN*
  * *TWITTER_ACCESS_TOKEN_SECRET*
  * *TWITTER_BEARER_TOKEN*
* Téléchargez les bibliothèques *nltk* si demandé en faisant

```
$ python
> import nltk
> nltk.download("biblioteque_a_telecharger")
```

## Modification du fonctionnement de l'application

Pour changer le nombre de topics à analyser, modifiez la variable *NB_TOPICS* du repertoire *settings*


