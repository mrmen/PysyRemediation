#!/usr/local/bin/python3.7
# -*- coding:utf-8 -*-

##docx##from docx import Document
##docx##from docx.shared import Cm
##docx##from docx.enum.table import WD_TABLE_ALIGNMENT
##docx##from docx.enum.text import WD_ALIGN_PARAGRAPH


import os, sys, codecs
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

class Remediation():
    '''Classe qui permet de produire le fichier de remédiation.
    Entrées 
    filename     : le fichier qui contient les noms des élèves et leurs niveaux
    comentence  :
    output       : le fichier de sortie au format tex
    notion       : nombre de notions
    Il faudra compiler le fichier avec LaTeX pour obtenir un PDF.
    '''
    def __init__(self, filename = "fichier.csv", competence="comp.csv", output = "output.tex",with_solution = 0, with_note = 0):
        '''__init__
        Initialisation et génération du fichier de sortie.
        '''
        # Préparation des variables
        self.filename = filename # nom du fichier avec les noms des élèves
        self.output_file = output # nom du fichier de sortie
        self.competence = competence # nom du fichier contenant les compétences
        self.with_solution = with_solution # booléen pour l'ajout des solutions ou non
        self.with_note = with_note
        
        self.convert_csv_to_array()

        # Chargement des compétences
        self.get_competences()
        # Chargement des élèves dans la liste
        self.get_students()
        # Changement des exercices dans la liste
        if "ex" in os.listdir("."):
            self.get_exercises()
            self.with_remediation = 1
        else:
            self.with_remediation = 0
        # Géneration du fichier TeX
##docx##        self.generateDocx()
        self.generateTex()
        
    def convert_csv_to_array(self):
        '''convert_csv_to_array
        Transfert du fichier dans la liste self.content
        '''
        # Chargement du fichier dans Python
        file = codecs.open(self.filename,"r",encoding="utf-8") # ouverture du fichier
        self.content = []
        for line in file.readlines():# pour chaque ligne du fichier
            #TESTING
            temp = line
            temp = temp.replace("\n","").replace("	",";").replace("\"","").replace("\r","").replace("	",";")
            temp = temp.replace("Maîtrise insuffisante","0")
            temp = temp.replace("Maîtrise fragile","1")
            temp = temp.replace("Maîtrise satisfaisante","2")
            temp = temp.replace("Très bonne maîtrise","3")
            temp = temp.replace("Absent","a")
            temp = temp.replace("Non évalué ","n")
            if "X;X" in temp:
                continue
            if "Élève" in temp:
                continue
#            self.content.append(line.replace("\n","").split(";"))# ajouter la ligne du fichier découper selon les ;
            self.content.append(temp.split(";"))
            #TESTING
        file.close() # fermeture du fichier

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
#        print(self.exerciseNames)
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
\\setmainfont{Andika New Basic} 
\\setmathfont{Tex gyre pagella math} 
\\else 
\\usepackage[utf8x]{inputenc}
\\usepackage[T1]{fontenc} 
\\usepackage{kpfonts} 
\\usepackage{amsmath, amssymb}
\\fi
\\usepackage{rotating}
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
        for self.index in range(len(self.Students)):# répétition sur le nombre
                                        # d'élèves
                                        # utilisation de self.index
###
            positionnement = ["\\cellcolor{red!25}\\checkmark & & &","& \\cellcolor{yellow!25}\\checkmark & &", "& & \\cellcolor{green!25}\\checkmark &", "& & & \\cellcolor{DarkGreen!25}\\checkmark"]
            self.endofminipage = 0
            # valeur maximale que peut avoir l'eleve : 4 points par comp
            self.maxnote = 0
            # note de l'eleve
            self.note = 0
            string_temp = ""
            for i in range(self.notions):
                string_temp += "\\begin{center}\n\\begin{tabular}{|p{3cm}|*{4}{>{\\footnotesize}p{3cm}<{}|}}\n\\hline\n"
                string_temp += "& "+ "&".join(self.Observables[i]) + "\\\\"
                string_temp += "\\hline\n"
                if self.content[self.index][i+1] in ["0","1","2","3"]:
                    string_temp += self.Competences[i] + " & " + positionnement[int(self.content[self.index][i+1])] + "\\\\"
                    # dans ce cas l'eleve est evalue
                    ## on prend le positionnement et on ajoute 1 (evite la note nulle)
                    if self.content[self.index][i+1] == 0:
                        self.note += 0.5
                    else:
                        self.note += int(self.content[self.index][i+1])+1
                    ## on ajoute 4 a la note max
                    self.maxnote += 4
                elif self.content[self.index][i+1] == "a":
                    string_temp += self.Competences[i] + " & " + " Ab. & Ab. & Ab. & Ab." + "\\\\"
                elif self.content[self.index][i+1] == "n":
                    string_temp += self.Competences[i] + " & " + " N.E. & N.E. & N.E. & N.E." + "\\\\"
                string_temp += "\\hline\n"
                string_temp += "\\end{tabular}\\end{center}\n\\bigskip\n"
                ###
            # calcul de la note
            ## on verifie que la note max n'est pas nul
            if self.maxnote == 0:
                self.note = "non noté"
            else:
                self.note = str(int(round(self.note/self.maxnote*20.0)))+"/20"

            if self.with_remediation == 0:
                string += "\\subsection*{"+self.Students[self.index]+"}\n"
                string += string_temp
                string += "\n\n\\bigskip\n\n"
            else:
                if self.with_note == 1:
                    string += "\\subsection*{"+self.Students[self.index]+" ("+note+")}\n"#
                else:
                    string += "\\subsection*{"+self.Students[self.index]+"}\n"#
                string += string_temp + "\\newpage"
                string += self.do_my_remediation()

        string += "\\end{document}"# fin du document

        file = codecs.open(self.output_file, "w","utf-8")# ouverture du fichier sortie
        file.write(string)# écriture de string dans le fichier de sortie
        file.close()# fermeture du fichier de sortie
        if os.name == "posix":
            os.system("pdflatex remediation.tex")
            os.system("open remediation.pdf")
        elif os.name == "nt":
            import subprocess
            subprocess.check_call(["C:\\Program Files\\Miktex\\bin\\x64\\bin\\pdflatex.exe", "remediation.tex"])

    def do_my_remediation(self):
            string = ""
            minipage = 0# variable pour la manipulation des deux colonnes
            for notion in range(len(self.exerciseNames)):# répétition sur les notions
                                        # utilisation de notion
                if self.content[self.index][notion+1] in ["0","1","2","3"]:
                    lvl = int(self.content[self.index][notion+1])+1# niveau d'exercice pour la
                                        # notion et l'élève
                else:
                    lvl = 1
                string += "\\begin{minipage}{0.5\linewidth}\centering\\includegraphics[width=8cm]{"+'./ex/'+self.exerciseNames[notion]+"-"+str(lvl)+".png}\n\n\\underline{"+self.exerciseNames[notion]+"}\\end{minipage}"#\\\\"
                string += "\n"
                minipage += 1
                if (minipage%2 == 0):# si deux minipage face à face
                        string +="\n\n"# on saute deux lignes
            minipage=0
            if self.with_solution:
                string += "\\vfill\n\n"
                for notion in range(len(self.exerciseNames)):# répétition sur les notions
                    bbox = ""
                    if self.content[self.index][i+1] in [0,1,2,3]:
                        lvl = int(self.content[self.index][notion+1])+1# niveau d'exercice pour la
                    else:
                        lvl = 1
                    if self.with_solution==1:
                        current_solution = open('./solutions/'+self.exerciseNames[notion]+"-"+str(lvl),"r")
                        for line in current_solution.readlines():
                            bbox += line
                        current_solution.close()
                    elif self.with_solution==2:
                        bbox += "\\includegraphics[width=4cm]{"+'./solutions/'+self.exerciseNames[notion]+"-"+str(lvl)+"-cor.png}\n"
                    string += "\\begin{minipage}{0.5\\linewidth}\\begin{turn}{180}"+bbox+"\\end{turn}\\end{minipage}\n"
                    minipage+=1
                    if (minipage%2==0):
                            string += "\n\n"
            string += "\n\n\\newpage\n\n"# nouvelle page pour changement d'élève
            return string

    # def generateDocx(self):
    #     '''generateDocx
    #     À revoir : devrait permettre de créer des fichiers docx
    #     '''
    #     document = Document()
    #     for index in range(len(self.Students)):
    #         document.add_heading('Remediation pour ',0)#+self.Students[index], 0)
    #         document.add_paragraph()
    #         for notion in range(len(self.Exercises)):
    #             document.add_heading('Notion '+str(notion+1), level=1)
    #             lvl = self.content[index][notion+1]
    #             document.add_picture('./ex/notion-'+str(notion+1)+"-"+str(lvl)+".gif")
    #         document.add_page_break()
            
    #     document.save('demo.docx')                  
                

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
    file_expected = ["eleves.csv", "comp.csv"]
    '''with_solution : variable sur la présence de solutions
        0 : pas de solution
        1 : solutions dans des fichiers texte
        2 : solutions dans des fichiers png
        '''
    with_solution = 0
    if "-h" in sys.argv or "--help" in sys.argv:
        helpMe()
        sys.exit(0)
    if "-s" in sys.argv or "--solution" in sys.argv:
        file_expected.append("solutions")
        with_solution = 1
    for file in file_expected:
        if not file in os.listdir("."):
            print("Le fichier %s est manquant. Merci de l'ajouter ou de modifier le script main.py.\n"%file)
            input("Fin prématurée. Presser une touche.\n")
            sys.exit(1)
    with_note = 0

    if "-nn" in sys.argv:
        with_note = 0
    else:
        def oui():
            global with_note
            with_note = 1
            fen.destroy()
        def non():
            global with_note
            with_note = 0
            fen.destroy()
        # creating window
        fen = tk.Tk()
        tk.Label(fen, text = "Note ?").pack()
        tk.Button(fen, text = "Oui", command =oui).pack()
        tk.Button(fen, text = "Non", command =non).pack()
        fen.mainloop()

    if with_solution==1:
        sols = os.listdir("./solutions/")
        for file in sols:
            if "png" in file:
                with_solution=2
    converter = Remediation("eleves.csv", "comp.csv","remediation.tex", with_solution, with_note)
    
#        app = Fenetre()
