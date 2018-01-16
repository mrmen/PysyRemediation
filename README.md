# PysyRemediation : Remédiation avec Python

Ce script a pour but de générer des feuilles de remédiation à l'aide d'images d'exercices.

En proposant une liste d'élèves positionnés sur quelques compétences, le programme va générer une feuille au format LaTeX en s'aidant d'une liste d'exercices listés dans un répertoire donnée.
La feuille peut ensuite être compilée au format PDF. Chaque élève aura alors à son nom une grille de positionnement, ainsi qu'une liste d'exercices correspondant à ses réussites.

## Logiciel requis

* LaTeX
    Une distribution LaTeX est attendue ainsi que les packages suivants :
    * kpfonts
    * colortbl
    
    MacTeX, MikTeX ou TexLive sont fonctionnelles. Un éditeur pourra aussi être installé pour éviter la compilation en ligne de commande. On pourra penser à TeXMaker sur Windows en le configurant pour utiliser l'utf-8.
    
    
* Python
    Une version 3 est à prioriser pour le support de l'utf-8, mais avec quelques adaptations, la version 2 peut convenir.

* Pour utiliser la génération de fichier docx, il est nécessaire d'installer la librairie [python-docx](https://python-docx.readthedocs.io/en/latest/) et de supprimer les ##docx## devant chaque ligne concernée.


## Fichiers requis

Le script est basé sur la présence de deux fichiers.

* **eleves.csv**
    Il contient les noms des élèves ainsi que leur positionnement de 0 à 3. Chaque champ est séparé par un «; ». L'ordre des compétences doit correspondre au fichier «comp.csv».
* **comp.csv**
    Il contient le nom des compétences évaluées ainsi que les observables pour chaque niveau de maîtrise. Les champs sont séparés par des «;».

Un dossier doit aussi être créé ainsi que son contenu.

* **ex**
    C'est un dossier qui contient tous les exercices de remédiation. Pour chaque compétence, il faut créer **4** exercices dont le nom est du type suivant 

    >competence1-?.png
    
    où ? est un chiffre entre 0 et 3. Les accents doivent être absents des noms de fichiers.

## Utilisation

Si tous les éléments nécessaires à la réalisation de la feuille de remédiation sont présents, il suffit de lancer le script **main.py** (à l'aide d'un terminal ou en double-cliquant si cette option est disponible).

Un fichier **remediation.tex** devrait être créé, et il suffit alors de le compiler.

Le fichier **remediation.pdf** en résultera alors.

## Modifications

1. Il est possible de modifier les noms de fichiers nécessaires dans le script assez facilement.
2. Le nom des exercices est stocké dans la liste self.exerciceNames.
3. La largeur des images est dans l'option «width» de \includegraphics.
4. Pour obtenir des images en face à face, modifier «minipage» pour avoir 0.5\linewidth et supprimer le saut de ligne à la fin ("\\\\").
