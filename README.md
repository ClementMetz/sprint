# Sprint

Sprint est un projet de gestion numérique à destination des clubs d'athlétisme français. Ses fonctionnalités sont les suivantes :

* Collecte sur https://bases.athle.fr/index.aspx et export des données des athlètes du club (AthleteScraper.py).
* Planification des interclubs et répartition optimisée des athlètes dans les différentes épreuves de la compétition (ISPSolver.py).
* Collecte et export csv des données des compétitions à partir du site https://athle.live/ (AthleliveScraper.py).
* Outil de visualisation graphique de l'évolution d'un athlète (DrawAthleteInfo.py).

En cours de développement :

* Outil d'estimation du potentiel des jeunes athlètes.

## Installation

* Cliquer sur installer.bat
* L'installateur python se lance, choisir les options ci-dessous.

<div align="center">
<p float="center">
  <img src="resources/optional.png" width="360" />
  <img src="resources/advanced.png" width="360"/> 
</p>
</div>

* Une fois l'installation de python terminée, l'installation des modules complémentaires commence.
* L'invite de commandes se ferme, c'est terminé.

## Planification des interclubs

Le but de l'algorithme dont le mode d'utilisation est présenté ci-dessous est de trouver la meilleure répartition possible des athlètes du club dans les épreuves des interclubs en prenant en compte les contraintes de la compétition (2 athlètes maximum par épreuve, 2 épreuves maximum par athlète, une course maximum par athlète, et pas de conflits horaires entre épreuves). L'intérêt de l'algorithme est double : gagner du temps pour l'organisation, et maximiser la somme des points attendus. Une version antérieure de cet algorithme de placement a été testée avec succès dans un cas d'usage réel à l'occasion du deuxième tour des interclubs 2022 de l'AC Boulogne-Billancourt. La compétition s'est soldée par un record de points du club, une victoire en division régionale, et un passage inédit en division N2D.

### Mode d'emploi

Commencer par ouvrir le fichier Excel ISPInput.xlsx.

![Image](/resources/perfs.png)

On entre dans PerfM (pour les hommes) et PerfW (pour les femmes) toutes les performances connues des athlètes du club dans toutes les épreuves des interclubs. Les bonnes pratiques sont résumées dans l'onglet Bonnes Pratiques. Il est fortement conseillé de les lire.

![Image](/resources/schedule.png)

On entre dans ConflictsHelperM (pour les hommes) et ConflictsHelperW (pour les femmes) les horaires de début d'échauffement et de fin de repos pour chacune des épreuves.

On exécute ensuite `ISPSolver.py`. Le résultat est contenu dans le fichier Excel ISPSolution.xlsx.

![Image](/resources/result.png)

En haut de AffectationM et AffectationW, on a le tableau des athlètes participants à chaque épreuve. A droite, pour chaque athlète, les épreuves auxquelles il/elle participe. Le total de points est indiqué en haut à gauche. On a également les tables hongroises des performances entrées à disposition dans HungarianTableM et W.

### Exactitude de la solution

La méthode utilisée pour traiter ce problème d'optimisation en nombres entiers est de le relaxer en un problème d'optimisation linéaire. Il est ensuite résolu par la méthode des points intérieurs (variante du célèbre algorithme du simplexe). Expérimentalement, il semble que le résultat de l'optimisation relaxée soit toujours solution du problème en nombres entiers (les variables convergent toujours vers 0 ou 1, la solution optimale du problème relaxé est donc une solution du problème en nombres entiers, et c'en est par conséquent la solution optimale). La garantie théorique de ce fait n'est pas connue. Toute preuve mathématique serait donc la bienvenue.

### Génération automatique du tableau des performances

Sprint offre la possibilité de générer automatiquement les tableaux de performances PerfW et PerfM. Pour cela, on va dans l'onglet AthleteScraper de ISPInput.xlsx. On remplit les noms, prénoms, sexes et alias des athlètes. On remplit de préférence les numéros de licences, de sorte à éviter les problèmes d'homonymie. 

![Image](/resources/scraper.png)

Une fois cette tâche effectuée, on exécute `AthleteScraper.py`. Les performances qui s'affichent alors dans l'onglet AthleteScraper correspondent aux derniers season bests connus de chaque athlète dans chaque discipline. On peut copier directement ces performances à la suite des tableaux PerfM et PerfW en exécutant la commande `python AthleteScraper.py --fill_perf`. Les noms indiqués dans la colonne de gauche de PerfM et PerfW sont les alias indiqués dans l'onglet AthleteScraper.

## Suivi des compétitions et export CSV

Sprint donne accès à un outil d'export CSV des résultats des compétitions sur https://athle.live/. La commande suivante produit l'export CSV et compte les points par équipe de la compétition en live située à l'adresse https://athle.live/challenge/yourcompetitionurl. Si la compétition a le statut "Résultats", on écrit simplement --competition_status=resultats.

`python AthleliveScraper.py --competition_url=https://athle.live/challenge/yourcompetitionurl --competition_status=live`

On peut ensuite ouvrir le fichier competition.csv. On sélectionne la 1ère colonne du fichier, puis Données -> Convertir, et on sélectionne le séparateur |.

![Image](/resources/csvexport.png)

## Analyse de performances

On peut obtenir les nuages de points et courbes de performances d'un athlète pour les épreuves prises en charge avec la commande suivante (exemple de Solène Ndama) :

`python DrawAthleteInfo.py --name=Ndama --firstname=Solene --gender=W`

Les graphiques sont alors contenus dans le dossier Figures/name. On peut également indiquer le numéro de licence via l'option --licence_nb afin d'éviter les problèmes d'homonymie.

![Image](/resources/60mHWi.png)
