# README


## Description des scripts python

`main.py` permet de télécharger les mails reçus et d'en extraire le code HTML.

`extract_items.py` scanne les fichiers HTML des mails et en extrait des informations qui seront compilées dans le fichier `items.json`


`annonces.py` parse le fichier `items.json` et regarde si l'annonce a été téléchargée dans le répertoire `annonces`, si ce n'est pas le cas elle le met sur un tas de X items qui seront ouvertes par firefox.

Avec Firefox il faut récupérer le bout d'url qui va bien et telecharger la page web unqiueemtn dans le repertoire annonce



`enrich_items.py` ce script va parser les annonces telechargées en l'etat et va enrichir le json avec les infos dedans : annonces desactivée ou pas, et les critères de l'annonce