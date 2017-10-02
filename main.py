#!/usr/bin/env python
# -*- coding:utf-8 -*-
#from docx import Document
#from docx.shared import Cm
import os, sys, codecs

class Remediation():
    '''Classe qui permet de produire le fichier de remédiation.
    Entrées 
    filename     : le fichier qui contient les noms des élèves et leurs niveaux
    comentence  :
    output       : le fichier de sortie au format tex
    notion       : nombre de notions
    Il faudra compiler le fichier avec LaTeX pour obtenir un PDF.
    '''
    def __init__(self, filename = "fichier.csv", competence="comp.csv", output = "output.tex"):
        '''__init__
        Initialisation et génération du fichier de sortie.
        '''
        # Préparation des variables
        self.filename = filename # nom du fichier avec les noms des élèves
        self.output_file = output # nom du fichier de sortie
        self.competence = competence # nom du fichier contenant les compétences


        self.convert_csv_to_array()

        # Chargement des compétences
        self.get_competences()
        # Chargement des élèves dans la liste
        self.get_students()
        # Changement des exercices dans la liste
        self.get_exercises()
        # Géneration du fichier TeX
        self.generateTex()
        
    def convert_csv_to_array(self):
        '''convert_csv_to_array
        Transfert du fichier dans la liste self.content
        '''
        # Chargement du fichier dans Python
        file = codecs.open(self.filename,"r","utf-8") # ouverture du fichier
        self.content = []
        for line in file.readlines():# pour chaque ligne du fichier
            self.content.append(line.replace("\n","").split(";"))# ajouter la ligne du fichier
                                        # découper selon les ;
        file.close() # fermeture du fichier
        print(self.content)

                              
    def get_competences(self):
        '''get_competences
        Transfert de la liste des compétences dans la liste self.Competences
        Transfert de la liste des observables dans la liste 2D self.Observables
        '''
        file = codecs.open(self.competence,"r","utf-8")
        self.Competences = []
        self.Observables = []
        self.exerciseNames = []
        for line in file.readlines():# pour chaque ligne du fichier
                temp = line.replace("\n","").split(";")# ajouter la ligne du fichier
                self.Competences.append(temp[0])
                self.exerciseNames.append(temp[0].replace("é","e"))
                self.Observables.append(temp[1:])
        print(self.exerciseNames)
        file.close()
        self.notions = len(self.Competences) # nombre de notions

        
    def get_students(self):
        '''get_students
        Tranfsert des élèves dans la liste self.Students
        Tous les élèves doivent être dans la première colonne du fichier
        filename.

        '''
        self.Students = [_[0] for _ in self.content]# création de la liste en
                                        # prenant le premier élément de chaque
                                        # item de self.content
                                        
        
    def get_exercises(self):
        '''get_exercicess
        Chargement de la liste des exercices dans la liste self.Exercises.
        Tous les exercices dooivent être des fichiers png dont le nom est de la
        forme

        notion-«numéro de notion»-«niveau de difficulté».png
    
        Les exercices doivent se trouver dans le dossier ex qui est dans le même
        dossier que le fichier remédiation.
        '''
        self.Exercises = [[] for _ in range(self.notions)]
        for _ in os.listdir("./ex"):
            name = _.split("-")
            #self.Exercises[int(name[1])-1].append(_)
#             if "notion" in name:
#                 self.Exercises[int(name[1])-1].append(_)
    
    def generateTex(self):
        '''generateTex
        Génération du fichier TeX.
        Répétition sur le nombre d'élèves pour produire une page personnalisée.
        '''
        string = '''
\\documentclass[french,10pt]{article} 
\\usepackage{ifluatex} 
\\ifluatex 
\\usepackage{fontspec} 
\\usepackage{unicode-math} 
\\setmainfont{Andika New Basic} %
\\setmainfont{Open Dyslexic} 
\\setmathfont{Tex gyre pagella math} 
\\else 
\\usepackage[utf8]{inputenc}
\\usepackage[T1]{fontenc} 
\\usepackage{kpfonts} 
\\usepackage{amsmath, amssymb} 
\\fi 
\\usepackage{float} 
\\usepackage[table,svgnames]{xcolor}
\\usepackage{colortbl}
\\usepackage{graphicx} 
\\usepackage[margin=2cm]{geometry} 
\\usepackage{fancyhdr} 
\\usepackage[french]{babel} 
\\fancyhf{} 
\\fancyhead[L]{Remédiation} 
\\fancyhead[C]{
\\today} 
\\fancyhead[R]{}
\\pagestyle{fancy} 
\\begin{document}'''
        for index in range(len(self.Students)):# répétition sur le nombre
                                        # d'élèves
                                        # utilisation de index
###
            positionnement = ["\\cellcolor{red!25}\\checkmark & & &","& \\cellcolor{yellow!25}\\checkmark & &", "& & \\cellcolor{green!25}\\checkmark &", "& & & \\cellcolor{DarkGreen!25}\\checkmark"]
            endofminipage = 0
            for i in range(self.notions):
                string += "\\begin{center}\n\\begin{tabular}{|p{3cm}|*{4}{>{\\footnotesize}p{3cm}<{}|}}\n\\hline\n"
                string += "& "+ "&".join(self.Observables[i]) + "\\\\"
                string += "\\hline\n"
                string += self.Competences[i] + " & " + positionnement[int(self.content[index][i+1])] + "\\\\"
                string += "\\hline\n"
                string += "\\end{tabular}\\end{center}\n"
###            
            string += "\\subsection*{Remédiation pour "+self.Students[index]+"}\n"#
                                        #Titre avec le nom de l'élève
            minipage = 0# variable pour la manipulation des deux colonnes
            for notion in range(len(self.exerciseNames)):# répétition sur les notions
                                        # utilisation de notion
                lvl = int(self.content[index][notion+1])+1# niveau d'exercice pour la
                                        # notion et l'élève
                string += "\\begin{minipage}{0.8\linewidth}\centering\\includegraphics[width=9cm]{"+'./ex/'+self.exerciseNames[notion]+"-"+str(lvl)+".png}\\end{minipage}\\\\"
                minipage += 1
                if (minipage%2 == 0):# si deux minipage face à face
                        string +="\n\n"# on saute deux lignes
            string += "\\newpage"# nouvelle page pour changement d'élève
        string += "\\end{document}"# fin du document

        file = codecs.open(self.output_file, "w","utf-8")# ouverture du fichier sortie
        file.write(string)# écriture de string dans le fichier de sortie
        file.close()# fermeture du fichier de sortie


    def generateDocx(self):
        '''generateDocx
        À revoir : devrait permettre de créer des fichiers docx
        '''
        document = Document()
        for index in range(len(self.Students)):
            document.add_heading('Remediation pour ',0)#+self.Students[index], 0)
            document.add_paragraph()
            for notion in range(len(self.Exercises)):
                document.add_heading('Notion '+str(notion+1), level=1)
                lvl = self.content[index][notion+1]
                document.add_picture('./ex/notion-'+str(notion+1)+"-"+str(lvl)+".gif")
            document.add_page_break()
            
        document.save('demo.docx')                  
                

def helpMe():
    print('''
    Ce script attend la présence de deux fichiers :
    - eleves.csv
        contient les noms des élèves, puis les positionnement sur les compétences évaluées
        le positionnement est compris entre 0 et 3
        les différents champ sont séparés par des «;»
        exemple :
        nom1;0;1;2;0
        nom2;3;3;3;3
    - comp.csv
        contient le noms des compétences évaluées ainsi que les observables utilisés pour
        l'évaluation
        le nom des compétences doit être le même que celui des exercices de dossier «ex»
        avec les accents en plus
    
    et d'un dossier
    - ex
        contient l'ensemble des exercices au format png
        les noms des exercices sont du types
            competence1-1.png
            ...
            competence1-4.png
        pour les 4 niveaux de maitrise
    ''')
        
if __name__=="__main__":
    if "-h" in sys.argv or "--help" in sys.argv:
        helpMe()
        sys.exit(0)
    
    for file in ["eleves.csv", "comp.csv"]:
        if not file in os.listdir("."):
            print("Le fichier %s est manquant. Merci de l'ajouter ou de modifier le script main.py.\n"%file)
            input("Fin prématurée. Presser une touche.\n")
            sys.exit(1)
    converter = Remediation("eleves.csv", "comp.csv","remediation.tex")
    
#        app = Fenetre()
