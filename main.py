#!/usr/bin/env python
# -*- coding:utf-8 -*-
#from docx import Document
#from docx.shared import Cm
import os, sys

if sys.version_info[0]==2:
    import Tkinter as tk
    from Tkinter import filedialog
    from Tkinter import *
else:
    import tkinter as tk
    from tkinter import filedialog
    from tkinter import *


#TODO: - support de docx
#TODO: - possibilité de changer le dossier ex
#TODO: - changement du nombre de notions

class Fenetre():
        def __init__(self):
                self.filename = None
                self.output = None
                self.fenetre = tk.Tk()
                self.fenetre.title("Outils de remédiation")
                self.filename_entry = tk.Entry(self.fenetre)
                self.output_entry = tk.Entry(self.fenetre)
                self.filename_button = tk.Button(self.fenetre, text = "Sélectionner le fichier source", command = self.get_filename)
                self.output_button = tk.Button(self.fenetre, text = "Sélectionner le fichier de sortie", command = self.get_output)
                self.notions = tk.Entry(self.fenetre)
                self.label_notions = tk.Label(self.fenetre, text = "Nombre de notions")
                self.send_button = tk.Button(self.fenetre, text = "Créer les feuilles...", command = self.send)
                self.place_widgets()
                self.__mainloop__()
                
        def place_widgets(self):
                self.filename_entry.grid(row=1,column=0,columnspan=2)
                self.filename_button.grid(row=1,column=3,columnspan=1)
                self.output_entry.grid(row=2,column=0,columnspan=2)
                self.output_button.grid(row=2,column=3,columnspan=1)
                self.send_button.grid(row=4, column=0,columnspan = 4,sticky=EW)
                self.notions.insert(0,"4")                
                self.notions.grid(row = 3, column=0,columnspan=2)
                self.label_notions.grid(row = 3, column=3, columnspan=2)
                
        def get_filename(self):
                self.filename = tk.filedialog.askopenfilename()
                self.filename_entry.insert(0,self.filename)
    
        def get_output(self):
                self.output = tk.filedialog.asksaveasfilename()
                self.output_entry.insert(0,self.output)

        def send(self):
                if self.filename and self.output:
                        converter = Remediation(self.filename, "comp.csv",self.output)
                else:
                        top = tk.Toplevel()
                        top.title("Erreur sur les noms de fichiers.")
                        tk.Message(top, text = "L'un des noms de fichiers n'a pas été renseigné…").pack()
                        tk.Button(top, text = "Ok", command = top.destroy).pack()
                        top.width=600
                
        def __mainloop__(self):
                self.fenetre.lift()
                self.fenetre.attributes("-topmost", True)
                self.fenetre.mainloop()
                
                
######
###
######


class Remediation():
    '''Classe qui permet de produire le fichier de remédiation.
    Entrées 
    filename     : le fichier qui contient les noms des élèves et leurs niveaux
    comentence  :
    output       : le fichier de sortie au format tex
    notion       : nombre de notions
    Il faudra compiler le fichier avec LaTeX pour obtenir un PDF.
    '''
    def __init__(self, filename = "", competence="comp.csv", output = "output.tex"):
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
        file = open(self.filename,"r") # ouverture du fichier
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
        file = open(self.competence,"r")
        self.Competences = []
        self.Observables = []
        for line in file.readlines():# pour chaque ligne du fichier
                temp = line.replace("\n","").split(";")# ajouter la ligne du fichier
                self.Competences.append(temp[0])
                self.Observables.append(temp[1:])
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
            if "notion" in name:
                self.Exercises[int(name[1])-1].append(_)
    
    def generateTex(self):
        '''generateTex
        Génération du fichier TeX.
        Répétition sur le nombre d'élèves pour produire une page personnalisée.
        '''
        string = '''
\\documentclass[french,12pt]{article} 
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
            positionnement = ["\\cellcolor{red!25} & & &","& \\cellcolor{yellow!25} & &", "& & \\cellcolor{green!25} &", "& & & \\cellcolor{DarkGreen!25}"]
            endofminipage = 0
            for i in range(self.notions):
                string += "\\begin{center}\n\\begin{tabular}{|*{5}{p{2cm}|}}\n\\hline\n"
                string += "& "+ "&".join(self.Observables[i]) + "\\\\"
                string += "\\hline\n"
                string += self.Competences[i] + " & " + positionnement[int(self.content[index][i+1])] + "\\\\"
                string += "\\hline\n"
                string += "\\end{tabular}\\end{center}\n"
###            
            string += "\\subsection*{Remédiation pour "+self.Students[index]+"}\n"#
                                        #Titre avec le nom de l'élève
            minipage = 0# variable pour la manipulation des deux colonnes
            for notion in range(len(self.Exercises)):# répétition sur les notions
                                        # utilisation de notion
                lvl = int(self.content[index][notion+1])+1# niveau d'exercice pour la
                                        # notion et l'élève
                string += "\\begin{minipage}{0.5\linewidth}\centering\\includegraphics[width=8cm]{"+'./ex/notion-'+str(notion+1)+"-"+str(lvl)+".png}\\end{minipage}"
                minipage += 1
                if (minipage%2 == 0):# si deux minipage face à face
                        string +="\n\n"# on saute deux lignes
            string += "\\newpage"# nouvelle page pour changement d'élève
        string += "\\end{document}"# fin du document

        file = open(self.output_file, "w")# ouverture du fichier sortie
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
                

if __name__=="__main__":
    converter = Remediation("eleves.csv", "competences.csv","remediation.tex")
#        app = Fenetre()
