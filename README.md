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

En haut de AffectationM et AffectationW, on a le tableau des athlètes participants à chaque épreuve. A droite, pour chaque athlète, les épreuves auxquelles il/elle participe. On a également les tables hongroises des performances entrées à disposition dans HungarianTableM et W.
