#/usr/bin/env python3
#-*- coding:utf-8 -*-
from PyQt5 import QtWidgets
from mainwindow import Ui_MainWindow
import sys, os, codecs
import pysybeta

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setMeUp()

    def directory_clicked(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select directory')
        self.ui.line_directory.insert(path)
        
    def setMeUp(self):
        # edit part
        self.ui.line_directory.setReadOnly(1)
        self.ui.text_comp.setReadOnly(1)
        self.ui.text_eleves.setReadOnly(1)
        # checked part
        self.ui.spin_size.setValue(5)
        self.ui.radio_comp_auto.setChecked(1)
        self.ui.radio_eleves_auto.setChecked(1)
        self.ui.radio_solutions_no.setChecked(1)
        self.ui.radio_side_no.setChecked(1)
        self.ui.radio_note_no.setChecked(1)
        # connect part
        self.ui.button_directory.clicked.connect(self.directory_clicked)
        self.ui.radio_comp_auto.clicked.connect(lambda: self.ui.text_comp.setReadOnly(1))
        self.ui.radio_eleves_auto.clicked.connect(lambda: self.ui.text_eleves.setReadOnly(1))
        self.ui.radio_comp_man.clicked.connect(lambda: self.ui.text_comp.setReadOnly(0))
        self.ui.radio_eleves_man.clicked.connect(lambda: self.ui.text_eleves.setReadOnly(0))
        self.ui.button_go.clicked.connect(self.go)
    def go(self):
        retvalue = 0
        for fun in [self.get_path(), self.get_comp(), self.get_eleves()]:
            retvalue += fun
        if retvalue!=0:
            return None
        self.size = str(self.ui.spin_size.value())
        self.side = self.ui.radio_side_yes.isChecked()
        self.solutions = 0
        self.note = self.ui.radio_note_yes.isChecked()
        converter = pysybeta.Remediation("eleves.csv", "comp.csv", "remediation.tex", self.solutions, self.note, self.side, self.size)
        
    def get_comp(self):
        if self.ui.radio_comp_auto.isChecked():
            if os.path.isfile(self.path+"/comp.csv"):
                1
            else:
                self.mydialog("Recherche fichier comp.csv")
        else:
            content = self.ui.text_comp.document()
            if os.path.isfile(self.path+"/comp.csv"):
                1
            else:
                f = codecs.open("comp.csv", "w", "utf-8")
                f.write(content.toPlainText())
                f.close()
        return 0
    def get_eleves(self):
        if self.ui.radio_eleves_auto.isChecked():
            if os.path.isfile(self.path+"/eleves.csv"):
                1
            else:
                self.mydialog("Recherche fichier comp.csv")
        else:
            content = self.ui.text_eleves.document()
            if os.path.isfile(self.path+"/eleves.csv"):
                1
            else:
                f = codecs.open("eleves.csv", "w", "utf-8")
                f.write(content.toPlainText())
                f.close()
        return 0
    def get_path(self):
        self.path = self.ui.line_directory.text()
        if self.path == "":
            self.mydialog("Choix dossier")
            return 1
        return 0
    def mydialog(self, errtype):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("%s invalide"%errtype)
        msg.setInformativeText("Merci de corriger l'erreur.")
        msg.setWindowTitle("Erreur")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()
            
def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.setWindowTitle("PysyRemédiation")
    application.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
