import fix_qt_import_error
import sys, os, PyQt5.QtWidgets, json, json, pathlib, urllib, subprocess
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMenu, QMessageBox
from reclistbuilderUI import *
from datetime import date

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.app = app

        self.ui.SaveConfigAsMenuButton.triggered.connect(self.saveConfiguration)
        self.ui.LoadConfigMenuButton.triggered.connect(self.loadConfiguration)
        self.ui.RecordingStyleRadioButtonOne.toggled.connect(self.styleChanged)
        self.ui.GenerateStartCVCheckBox.toggled.connect(self.genCV)
        self.ui.GenerateEndVCCheckBox.toggled.connect(self.genVC)
        self.ui.NumberLinesCheckBox.toggled.connect(self.toggleLineNumberPanel)
        self.ui.GenerateReclistButton.pressed.connect(self.generateList)

        
    # functions for shitt
    def generateList(self):
        if self.ui.RecordingStyleRadioButtonOne.isChecked():
            self.generateReclistStyle1()
        if self.ui.RecordingStyleRadioButtonTwo.isChecked():
            self.generateReclistStyle2()
        if self.ui.RecordingStyleRadioButtonThree.isChecked():
            self.generateReclistStyle3()

    # Generate list type 1 =========================================================== #
    # ================================================================================ #
    def generateReclistStyle1(self):
        # create table with all vowels
        vowels = self.ui.VowelsInput.text().split(" ")
        # create a table with the consonsants
        consonants = self.ui.UnvoicedConsonantInput.text().split(" ") + self.ui.VoiceConsonantInput.text().split(" ")
        startConsonants = self.ui.StartConsonantInput.text().split(" ")
        endConsonants = self.ui.EndConsonantIput.text().split(" ")

        # list lines
        reclist = []

        # current syllable
        syllable = 0

        # blank line
        line = ""

        # generate CVVC section
        for v in vowels:
            for c in consonants:
                if c in startConsonants:
                    reclist.append(c+v+"-"+c+v)
                elif c in endConsonants:
                    reclist.append(v+"-"+c+v+"-"+c)
                else:
                    reclist.append(c+v+"-"+c+v+"-"+c)

        # generate start CV, and CC(C)V
        for i, vowel in enumerate(vowels):
            for c in self.ui.StartClusterInput.text().split(" "):
                if syllable < self.ui.MaxSyllablesInput.value():
                    line += c+vowel+"_"
                    syllable += 1
                else:
                    if line[-1] == "_":
                        line = line[:-1]
                    reclist.append(line)
                    syllable = 1
                    line = c+vowel+"_"
    
        if line != "":
            if line[-1] == "_":
                line = line[:-1]
            reclist.append(line)
            syllable = 0
            line = ""

        # generate ending VC and VCC(C)

        for i, vowel in enumerate(vowels):
            for c in self.ui.EndClusterInput.text().split(" "):
                if syllable < self.ui.MaxSyllablesInput.value():
                    line += vowel+"-"+c+"_"
                    syllable += 1
                else:
                    if line[-1] == "_":
                        line = line[:-1]
                    reclist.append(line)
                    syllable = 1
                    line = vowel+"-"+c+"_"

        if line != "":
            if line[-1] == "_":
                line = line[:-1]
            reclist.append(line)
            
        line = vowels[0] + "-"
        syllable = 1

        # generate CCs
        c1s = [c for c in consonants if c not in startConsonants]
        c2s = [c for c in startConsonants if c not in endConsonants]

        for c1 in c1s:
            for c2 in c2s:
                if not self.ui.GeneratePureUnvoicedConsonantCheckbox.isChecked():
                    if c1 in self.ui.UnvoicedConsonantInput.text().split(" ") and c2 in self.ui.UnvoicedConsonantInput.text().split(" "):
                        continue
                if syllable < self.ui.MaxSyllablesInput.value():
                    line += c1 + "-" + c2 + vowels[0] + "-"
                    syllable += 1
                else:
                    if line[-1] == "-":
                        line = line[:-1]
                    reclist.append(line)
                    syllable = 2
                    line = vowels[0] + "-" + c1 + "-" + c2 + vowels[0] + "-"

        with open("test.txt", "w") as f:
                for i,l in enumerate(reclist):
                    ln = ""
                    if(self.ui.NumberLinesCheckBox.isChecked()):
                        ln = ln + str(i).zfill(3) + self.ui.PrefixOfNumber.text()
                    if(self.ui.PrefixLinesWithUnderscoreCheckbox.isChecked()):
                        ln = "_" + ln
                    ln = ln + l
                    f.write("%s\n" % ln)

        return
    # Generate list type 2 =========================================================== #
    # ================================================================================ #
    def generateReclistStyle2(self):
        return

    # Generate list type 3 =========================================================== #
    # ================================================================================ #
    def generateReclistStyle3(self):
        # create table with all vowels
        vowels = self.ui.VowelsInput.text().split(" ")
        # create a table with the consonsants
        consonants = self.ui.UnvoicedConsonantInput.text().split(" ") + self.ui.VoiceConsonantInput.text().split(" ")
        startConsonants = [c for c in consonants if c not in self.ui.EndConsonantIput.text().split(" ")] + self.ui.StartClusterInput.text().split(" ")
        endConsonants = [c for c in consonants if c not in self.ui.StartConsonantInput.text().split(" ")] + self.ui.EndClusterInput.text().split(" ")
        consonants += self.ui.StartClusterInput.text().split(" ")

        # list lines
        reclist = []

        # current syllable
        syllable = 0

        # blank line
        line = ""

        # generate CVVC section
        for vowel in vowels:
            if line != "":
                if line[-1] == "-":
                    line = line[:-1]
                reclist.append(line)
                line = ""
                syllable = 0
            line = vowel + "-"
            syllable += 1
            # for each consonant
            for consonant in consonants:
                if syllable >= self.ui.MaxSyllablesInput.value():
                    line = line[:-1]
                    reclist.append(line)
                    syllable = 2
                    line = vowel + "-" + consonant + vowel + "-"
                else:
                    line += consonant + vowel + "-"
                    syllable += 1

        if line != "":
            if line[-1] == "-":
                line = line[:-1]
            reclist.append(line)
            syllable = 0
            line = ""

        if self.ui.GenerateStartCVCheckBox.isChecked() or self.ui.GenerateStartingConsonantsCheckBox.isChecked():
            # generate start CV, and CC(C)V

            for i, vowel in enumerate(vowels):
                if i>0 and not self.ui.GenerateStartCVCheckBox.isChecked():
                    break
                for c in startConsonants:
                    if syllable < self.ui.MaxSyllablesInput.value():
                        line += c+vowel+"_"
                        syllable += 1
                    else:
                        if line[-1] == "_":
                            line = line[:-1]
                        reclist.append(line)
                        syllable = 1
                        line = c+vowel+"_"
        
        if line != "":
            if line[-1] == "-":
                line = line[:-1]
            reclist.append(line)
            syllable = 0
            line = ""

        if self.ui.GenerateEndVCCheckBox.isChecked() or self.ui.GenerateEndingConsonantsCheckbox.isChecked():
            # generate ending VC and VCC(C)

            for i, vowel in enumerate(vowels):
                if i>0 and not self.ui.GenerateEndVCCheckBox.isChecked():
                    break
                for c in endConsonants:
                    if syllable < self.ui.MaxSyllablesInput.value():
                        line += vowel+"-"+c+"_"
                        syllable += 1
                    else:
                        if line[-1] == "_":
                            line = line[:-1]
                        reclist.append(line)
                        syllable = 1
                        line = vowel+"-"+c+"_"

        if line != "":
            if line[-1] == "-":
                line = line[:-1]
            reclist.append(line)
            
        line = vowels[0] + "-"
        syllable = 1

        # generate CCs
        c1s = [c for c in endConsonants if c not in self.ui.EndClusterInput.text().split(" ")]
        c2s = [c for c in startConsonants if c not in self.ui.StartClusterInput.text().split(" ")]

        for c1 in c1s:
            for c2 in c2s:
                if not self.ui.GeneratePureUnvoicedConsonantCheckbox.isChecked():
                    if c1 in self.ui.UnvoicedConsonantInput.text().split(" ") and c2 in self.ui.UnvoicedConsonantInput.text().split(" "):
                        continue
                if syllable < self.ui.MaxSyllablesInput.value():
                    line += c1 + "-" + c2 + vowels[0] + "-"
                    syllable += 1
                else:
                    if line[-1] == "-":
                        line = line[:-1]
                    reclist.append(line)
                    syllable = 2
                    line = vowels[0] + "-" + c1 + "-" + c2 + vowels[0] + "-"

        with open("test.txt", "w") as f:
                for i,l in enumerate(reclist):
                    ln = ""
                    if(self.ui.NumberLinesCheckBox.isChecked()):
                        ln = ln + str(i).zfill(3) + self.ui.PrefixOfNumber.text()
                    if(self.ui.PrefixLinesWithUnderscoreCheckbox.isChecked()):
                        ln = "_" + ln
                    ln = ln + l
                    f.write("%s\n" % ln)
        return

    # toggle line number panel ======================================================= #
    # ================================================================================ #
    def toggleLineNumberPanel(self):
        self.ui.NumberLinesPanel.setEnabled(self.ui.NumberLinesCheckBox.isChecked())
        return

    # Enable style checkboxes ======================================================== #
    # ================================================================================ #
    def styleChanged(self):
        self.ui.GenerateStartCVCheckBox.setEnabled(not self.ui.RecordingStyleRadioButtonOne.isChecked())
        self.ui.GenerateEndVCCheckBox.setEnabled(not self.ui.RecordingStyleRadioButtonOne.isChecked())
        return

    # Include clusters checkbox for starting CVs ===================================== #
    # ================================================================================ #
    def genCV(self):
        self.ui.CVIncludeClustersCheckBox.setEnabled(self.ui.GenerateStartCVCheckBox.isChecked())
        return

    # Include clusters checkbox for ending VCs ======================================= #
    # ================================================================================ #
    def genVC(self):
        self.ui.VCIncludeClustersCheckBox.setEnabled(self.ui.GenerateEndVCCheckBox.isChecked())
        return

    # load configuration ============================================================= #
    # ================================================================================ #
    def loadConfiguration(self):
        # read file
        configData = {}
        fileName, _ = QFileDialog.getOpenFileName(self, "Load configuration...", "", "json file (*.json)", options=QFileDialog.Options())
        if fileName:
            with open(fileName, "r") as f:
                configData = json.load(f)
        
        # load into window
        self.ui.VowelsInput.setText(configData["Phonemes"]["Vowels"])
        self.ui.UnvoicedConsonantInput.setText(configData["Phonemes"]["UnvoicedConsonants"])
        self.ui.VoiceConsonantInput.setText(configData["Phonemes"]["VoicedConsonants"])
        self.ui.StartConsonantInput.setText(configData["Phonemes"]["StartConsonants"])
        self.ui.EndConsonantIput.setText(configData["Phonemes"]["EndConsonants"])
        self.ui.StartClusterInput.setText(configData["Phonemes"]["StartClusters"])
        self.ui.EndClusterInput.setText(configData["Phonemes"]["EndClusters"])
        self.ui.MaxSyllablesInput.setValue(configData["Settings"]["MaxSyllables"])
        # select the right index for style
        if configData["Settings"]["Style"]["Type"] == 0:
            self.ui.RecordingStyleRadioButtonOne.setChecked(True)
        elif configData["Settings"]["Style"]["Type"] == 1:
            self.ui.RecordingStyleRadioButtonTwo.setChecked(True)
        elif configData["Settings"]["Style"]["Type"] == 2:
            self.ui.RecordingStyleRadioButtonThree.setChecked(True)
        self.ui.GenerateStartCVCheckBox.setChecked(configData["Settings"]["Style"]["GenerateStartCV"])
        self.ui.GenerateEndVCCheckBox.setChecked(configData["Settings"]["Style"]["GenerateEndVC"])
        self.ui.NumberLinesCheckBox.setChecked(configData["Settings"]["NumberLines"]["Enabled"])
        # select the lines mode
        if configData["Settings"]["NumberLines"]["Mode"] == 0:
            self.ui.PrefixLinesRadioButton.setChecked(True)
        elif configData["Settings"]["NumberLines"]["Mode"] == 1:
            self.ui.SuffixLinesRadioButton.setChecked(True)
        self.ui.PrefixOfNumber.setText(configData["Settings"]["NumberLines"]["PrefixForNumber"])
        self.ui.SuffixUppercasePlusCheckbox.setChecked(configData["Settings"]["SuffixUppercaseWithPlus"])
        self.ui.PrefixLinesWithUnderscoreCheckbox.setChecked(configData["Settings"]["PrefixLinesWithUnderscore"])
        self.ui.OtoOffsetInput.setValue(configData["Settings"]["Oto"]["Offset"])
        self.ui.OtoBpmInput.setValue(configData["Settings"]["Oto"]["BPM"])
        # select phoneme separation mode
        if configData["Settings"]["Oto"]["PhonemeSeparation"] == 0:
            self.ui.SpaceSeparatedPhonemesRadioButton.setChecked(True)
        elif configData["Settings"]["Oto"]["PhonemeSeparation"] == 1:
            self.ui.NoSpacesRadioButton.setChecked(True)
        elif configData["Settings"]["Oto"]["PhonemeSeparation"] == 2:
            self.ui.OnlySpaceSeparateVCRadioButton.setChecked(True)
        elif configData["Settings"]["Oto"]["PhonemeSeparation"] == 3:
            self.ui.DoubleAliasRadioButton.setChecked(True)

        self.ui.GeneratePureUnvoicedConsonantCheckbox.setChecked(configData["Settings"]["SeparatePureUnvoicedCCs"])
        self.ui.GenerateStartingConsonantsCheckBox.setChecked(configData["Settings"]["GenerateStartConsonants"])
        self.ui.GenerateEndingConsonantsCheckbox.setChecked(configData["Settings"]["GenerateEndConsonants"])

        return

    # save configuration ============================================================= #
    # ================================================================================ #
    def saveConfiguration(self):
        confJson = {"Phonemes":{},"Settings":{"Style":{},"NumberLines":{},"Oto":{}}}
        confJson["Phonemes"]["Vowels"] = self.ui.VowelsInput.text()
        confJson["Phonemes"]["UnvoicedConsonants"] = self.ui.UnvoicedConsonantInput.text()
        confJson["Phonemes"]["VoicedConsonants"] = self.ui.VoiceConsonantInput.text()
        confJson["Phonemes"]["StartConsonants"] = self.ui.StartConsonantInput.text()
        confJson["Phonemes"]["EndConsonants"] = self.ui.EndConsonantIput.text()
        confJson["Phonemes"]["StartClusters"] = self.ui.StartClusterInput.text()
        confJson["Phonemes"]["EndClusters"] = self.ui.EndClusterInput.text()
        confJson["Settings"]["MaxSyllables"] = self.ui.MaxSyllablesInput.value()
        # get the index of the radio button selected
        styleIndex = 0
        if self.ui.RecordingStyleRadioButtonTwo.isChecked():
            styleIndex = 1
        elif self.ui.RecordingStyleRadioButtonThree.isChecked():
            styleIndex = 2
        confJson["Settings"]["Style"]["Type"] = styleIndex
        confJson["Settings"]["Style"]["GenerateStartCV"] = self.ui.GenerateStartCVCheckBox.isChecked()
        confJson["Settings"]["Style"]["GenerateEndVC"] = self.ui.GenerateEndVCCheckBox.isChecked()
        confJson["Settings"]["NumberLines"]["Enabled"] = self.ui.NumberLinesCheckBox.isChecked()
        # get the current selected lines mode
        confJson["Settings"]["NumberLines"]["Mode"] = 0
        if self.ui.SuffixLinesRadioButton.isChecked():
            confJson["Settings"]["NumberLines"]["Mode"] = 1
        confJson["Settings"]["NumberLines"]["PrefixForNumber"] = self.ui.PrefixOfNumber.text()
        confJson["Settings"]["SuffixUppercaseWithPlus"] = self.ui.SuffixUppercasePlusCheckbox.isChecked()
        confJson["Settings"]["PrefixLinesWithUnderscore"] = self.ui.PrefixLinesWithUnderscoreCheckbox.isChecked()
        confJson["Settings"]["Oto"]["Offset"] = self.ui.OtoOffsetInput.value()
        confJson["Settings"]["Oto"]["BPM"] = self.ui.OtoBpmInput.value()
        # get the current selected phoneme separation mode
        phonemeSeparationMode = 0
        if self.ui.NoSpacesRadioButton.isChecked():
            phonemeSeparationMode = 1
        elif self.ui.OnlySpaceSeparateVCRadioButton.isChecked():
            phonemeSeparationMode = 2
        elif self.ui.DoubleAliasRadioButton.isChecked():
            phonemeSeparationMode = 3
        confJson["Settings"]["Oto"]["PhonemeSeparation"] = phonemeSeparationMode
        confJson["Settings"]["SeparatePureUnvoicedCCs"] = self.ui.GeneratePureUnvoicedConsonantCheckbox.isChecked()
        confJson["Settings"]["GenerateStartConsonants"] = self.ui.GenerateStartingConsonantsCheckBox.isChecked()
        confJson["Settings"]["GenerateEndConsonants"] = self.ui.GenerateEndingConsonantsCheckbox.isChecked()

        # save file dialog :)
        fileName, _ = QFileDialog.getSaveFileName(self, "Save configuration...", "", "json file (*.json)", options=QFileDialog.Options())
        if fileName:
            with open(fileName, "w") as f:
                json.dump(confJson, f)

        return

    # wait for window the fully start ================================================ #
    # ================================================================================ #
    def applicationStarted(self):
        return
        

def main():
    app = QApplication(sys.argv)
    w = MainWindow(app)
    w.show()
    t = QtCore.QTimer()
    t.singleShot(0,w.applicationStarted)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()