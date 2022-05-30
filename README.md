# Sprint

Sprint est un projet de gestion numérique à destination des clubs d'athlétisme français. Ses fonctionnalités sont les suivantes :

* Collecte sur https://bases.athle.fr/index.aspx et export des données des athlètes du club (AthleteScraper.py).
* Planification des interclubs et répartition optimisée des athlètes dans les différentes épreuves de la compétition (ISPSolver.py).
* Collecte et export csv des données des compétitions à partir du site https://athle.live/ (AthleliveScraper.py).

En cours de développement :

* Outil d'estimation du potentiel des jeunes athlètes.

## Modules python à installer

* selenium
* xlrd
* xlsxwriter
* scipy.optimize

## Utilisation

Ouvrir ISPTableur_run.xlsm.

![Image](/resources/perfs.png)

On entre dans PerfM (pour les hommes) et PerfW (pour les femmes) toutes les performances connues des athlètes du club dans toutes les épreuves des interclubs. Les bonnes pratiques sont résumées dans l'onglet Bonnes Pratiques. Il est fortement conseillé de le lire.

![Image](/resources/schedule.png)

On entre dans ConflictsHelperM (pour les hommes) et ConflictsHelperW (pour les femmes) les horaires de début d'échauffement et de fin de repos pour chacune des épreuves.

On exécute ensuite ISPSolver.py. Le résultat est contenu dans le fichier Excel ISPSolution.xlsx.

![Image](/resources/result.png)

En haut de AffectationM et AffectationW, on a le tableau des athlètes participants à chaque épreuve. A droite, pour chaque athlète, les épreuves auxquelles il/elle participe. Le total de points est indiqué en haut à gauche. On a également les tables hongroises des performances entrées à disposition dans HungarianTableM et W.
Le but de l'algorithme est de trouver la meilleure répartition possible en prenant en compte les contraintes des interclubs (2 athlètes maximum par épreuve, 2 épreuves maximum par athlète, une course maximum par athlète, et pas de conflit horaire entre épreuves). 

## Exactitude de la solution

La méthode utilisée pour traiter ce problème d'optimisation en nombres entiers est de le relaxer en un problème d'optimisation linéaire. Il est ensuite résolu par la méthode des points intérieurs (variante du célèbre algorithme du simplexe). Expérimentalement, il semble que le résultat de l'optimisation relaxée soit toujours la solution du problème en nombres entiers (les variables convergent toujours vers 0 ou 1, la solution optimale du problème relaxé est donc une solution du problème en nombres entiers, et c'en est par conséquent la solution optimale). La garantie théorique de ce fait n'est pas connue. Toute preuve mathématique serait donc la bienvenue.

## Génération automatique du tableau des performances

Sprint offre la possibilité de générer automatiquement les tableaux de performances PerfW et PerfM
