# [valereobei.com](https://github.com/flavien-hugs/vobapp/)&nbsp;

![valereobei.com](https://github.com/flavien-hugs/vobapp/blob/main/scrennshot.png)

[valereobei.com](https://github.com/flavien-hugs/vobapp/) une application web de vente en ligne (ecommerce), de blogging et e-learning basé sur les framework [Django](https://docs.djangoproject.com/).

### Fonctionalité et prise en main
La plateforme fournit les fonctionnalité comme :

    - Un moteur de recherche basé sur haystack
    - Un moteur de blogging
    - Un mote de commerce electronique
    - Un sustème de paiment
    - Un système de récommandation
### Installation & Exécution du projet en local

    - git clone https://github.com/flavien-hugs/vobapp/
    - cd vobapp
    - Activer l'environnement virtuel puis installer les dépendances avec la commande `make install`
    - Faire la migrations de la base de données avec la commande `make migrate`
    - Changer les données par défauts `make loaddata'
    - Enfin lancer le serveur interne de django avec `./manage runserver` puis naviguer jusqu'à `<http://localhost:8000>`

Comment contribuer
------------------

Faites un Fork et travaillez sur votre propre branche, soumettez des améliorations.

La principale branche de travail est [vobapp/main](https://github.com/flavien-hugs/vobapp/tree/main).


### Credit

Code: [flavien-hugs](https://twitter.com/flavien_hugs)
