from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon, QPixmap
from mydesign import Ui_MainWindow
from pprint import pprint

import requests
import json
import pokemon
import string
import urllib.request
import googleAuth

errorText = ''
successText = ''

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        #launch the UI
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #gain access to spreadsheet
        googleAuth.googleAuth()
        
        #initialize/reset values
        self.resetVariables()
        
        #set images to be scaled
        self.ui.sftImage.setScaledContents(True)
        self.ui.aftImage.setScaledContents(True)
        self.ui.shinyImage.setScaledContents(True)
        self.ui.battleImage.setScaledContents(True)

        #connect buttons to their utility methods
        self.ui.pokemonLineEdit.returnPressed.connect(self.getPokemon)
        self.ui.sftSubmitPushButton.clicked.connect(self.submitSft)
        self.ui.aftSubmitPushButton.clicked.connect(self.submitAft)
        self.ui.shinySubmitPushButton.clicked.connect(self.submitShiny)
        self.ui.battleSubmitPushButton.clicked.connect(self.submitBattler)
        self.ui.updateRowsButton.clicked.connect(self.updateRowCounters)

        #Update the current empty rows
        self.updateRowCounters()
        
        
    #Method to search api for a pokemon using the search line
    def getPokemon(self):
        #get the name of the requested pokemon and search the api for it
        poke = self.ui.pokemonLineEdit.text().lower()
        pokeUrl = 'https://pokeapi.co/api/v2/pokemon/' + poke + '/'
        try:
            response = requests.get(pokeUrl)
            mon = response.json()
        except:
            setError(mywindow, "Pokemon Not Found or max API calls reached")
            return

        #using the info from the api, get the proper species name, its sprite, and create its icon command
        self.dex = str(mon.get("id"))
        if len(self.dex) == 2:
            self.dex = '0' + self.dex
        elif len(self.dex) == 1:
            self.dex = '00' + self.dex

        self._icon = '=image("https://www.serebii.net/swordshield/pokemon/' + self.dex + '.png")'
        self._species = string.capwords(mon.get('name'))
        imageUrl = 'https://www.serebii.net/pokemon/art/' + self.dex + '.png'
        image = urllib.request.urlopen(imageUrl).read()
        
        #place the sprite image into the UI
        pixmap = QPixmap()
        pixmap.loadFromData(image)
        self.ui.sftImage.setPixmap(pixmap)
        self.ui.aftImage.setPixmap(pixmap)
        self.ui.shinyImage.setPixmap(pixmap)
        self.ui.battleImage.setPixmap(pixmap)
        

        #Clear the ability drop downs and then set them with the proper abilities
        self.ui.sftAbilityDropdown.clear()
        self.ui.aftAbilityDropdown.clear()
        self.ui.shinyAbilityDropdown.clear()
        self.ui.battleAbilityDropdown.clear()
        self.isAbilityHidden.clear()

        abilities = ['']
        for ability in mon.get('abilities'):
            name = ability.get('ability').get('name')
            hidden = ability.get('is_hidden')
            name = string.capwords(name.replace('-', ' '))
            self.isAbilityHidden[name] = hidden
            abilities.append(name)

        abilities.sort()    
        self.ui.sftAbilityDropdown.addItems(abilities)
        self.ui.aftAbilityDropdown.addItems(abilities)
        self.ui.shinyAbilityDropdown.addItems(abilities)
        self.ui.battleAbilityDropdown.addItems(abilities)
        global successText
        successText = 'Pokemon Found'
        self.setSuccess()

    #Utility Method for submitting a "Shiny for Trade"
    def submitSft(self):
        #Set all arguements
        self._ball = self.ui.sftBallDropdown.currentText()
        self._ability = self.ui.sftAbilityDropdown.currentText()
        self._nature = self.ui.sftNatureDropdown.currentText()
        self._gmax = self.ui.sftGMaxRadioButton.isChecked()
        self._zeroSpeed = self.ui.sftZeroSpeedRadioButton.isChecked()
        if not self.checkAbility():
            return -1

        self._ivs = [self.ui.sftHpRadioButton.isChecked(), self.ui.sftAtkRadioButton.isChecked(), self.ui.sftDefRadioButton.isChecked(),
        self.ui.sftSpaRadioButton.isChecked(), self.ui.sftSpdRadioButton.isChecked(), self.ui.sftSpeRadioButton.isChecked()]
            
        self._ot = self.ui.sftOtLineEdit.text()
        self._id = self.ui.sftIdLineEdit.text()
        self._obtained = self.ui.sftObtainedLineEdit.text()
        self._icon = '=image("https://www.serebii.net/Shiny/SWSH/' + self.dex + '.png")'
        self._gender = self.ui.sftGenderComboBox.currentText()
        self._sType = self.ui.sftSTypeComboBox.currentText()

        #Create the sft pokemon object
        sftMon = pokemon.sftPokemon(self._species, self._ball, self._ability, self._nature, self._gmax, self._zeroSpeed, self._ha, self._icon, self._ivs, self._ot, self._id, self._obtained, self._gender, self._sType)

        #Validate all arguements are acceptable
        if not sftMon.validateMon():
            self.setError()
            return -1

        #Trim nature down to just one word, change the ball variable to be the proper value, update gender and shiny symbols
        temp = sftMon.nature.split(' ', 1)
        sftMon.nature = temp[0]
        sftMon.setBallField()
        sftMon.setGenderSymbol()
        sftMon.setSTypeSymbol()
        

        #Once pokemon is validated and submitted to the google doc, clear fields
        googleAuth.addSFT(sftMon)
        self.setSuccess()
        self.resetFields('sft')
        
    #Utility Method for submitting an "Aprimon for Trade"
    def submitAft(self):
        #Set all arguements
        self._ball = self.ui.aftBallDropdown.currentText()
        self._ability = self.ui.aftAbilityDropdown.currentText()
        self._nature = self.ui.aftNatureDropdown.currentText()
        self._gmax = self.ui.aftGMaxRadioButton.isChecked()
        self._zeroSpeed = self.ui.aftZeroSpeedRadioButton.isChecked()
        if not self.checkAbility():
                return -1
        self._ivs = self.ui.aftIvDropdown.currentText()
        self._stock = self.ui.aftStockSpinBox.value()

        #Create the aft pokemon object
        aftMon = pokemon.aftPokemon(self._species, self._ball, self._ability, self._nature, self._gmax, self._zeroSpeed, self._ha, self._icon, self._ivs, self._stock)

        #Validate all arguements are acceptable
        if not aftMon.validateMon():
            self.setError()
            return -1

        #Trim nature down to just one word, alter the ball to the proper input
        temp = aftMon.nature.split(' ', 1)
        aftMon.nature = temp[0]
        aftMon.aftBallHelper()

        #Once pokemon is validated and submitted to the google doc, clear fields
        googleAuth.addAFT(aftMon)
        self.setSuccess()
        self.resetFields('aft')
    
    #Utility Method for submitting a Shiny
    def submitShiny(self):
        #Set all arguements
        self._ball = self.ui.shinyBallDropdown.currentText()
        self._ability = self.ui.shinyAbilityDropdown.currentText()
        self._nature = self.ui.shinyNatureDropdown.currentText()
        self._gmax = self.ui.shinyGMaxRadioButton.isChecked()
        self._zeroSpeed = self.ui.shinyZeroSpeedRadioButton.isChecked()
        if not self.checkAbility():
                return -1

        self._ivs = [self.ui.shinyHpRadioButton.isChecked(), self.ui.shinyAtkRadioButton.isChecked(), self.ui.shinyDefRadioButton.isChecked(),
        self.ui.shinySpaRadioButton.isChecked(), self.ui.shinySpdRadioButton.isChecked(), self.ui.shinySpeRadioButton.isChecked()]

        self._nickname = self.ui.shinyNicknameLineEdit.text()
        self._icon = '=image("https://www.serebii.net/Shiny/SWSH/' + self.dex + '.png")'
        self._gender = self.ui.shinyGenderComboBox.currentText()
        self._sType = self.ui.shinySTypeComboBox.currentText()

        #Create the shiny pokemon object
        shinyMon = pokemon.shinyPokemon(self._species, self._ball, self._ability, self._nature, self._gmax, self._zeroSpeed, self._ha, self._icon, self._ivs, self._nickname, self._gender, self._sType)

        #Validate all arguements are acceptable
        if not shinyMon.validateMon():
            self.setError()
            return -1

        #Trim nature down to just one word, change the ball variable to be the proper value
        temp = shinyMon.nature.split(' ', 1)
        shinyMon.nature = temp[0]
        shinyMon.setBallField()
        shinyMon.setGenderSymbol()
        shinyMon.setSTypeSymbol()

        #Once pokemon is validated and submitted to the google doc, clear fields
        googleAuth.addShiny(shinyMon)
        self.setSuccess()
        self.resetFields('shiny')

    #Utility Method for submitting a Battler
    def submitBattler(self):
        #Set all arguements
        self._ball = self.ui.battleBallDropdown.currentText()
        self._ability = self.ui.battleAbilityDropdown.currentText()
        self._nature = self.ui.battleNatureDropdown.currentText()
        self._gmax = self.ui.battleGMaxRadioButton.isChecked()
        self._zeroSpeed = self.ui.battleZeroSpeedRadioButton.isChecked()
        if not self.checkAbility():
                return -1

        self._ivs = [self.ui.battleHpRadioButton.isChecked(), self.ui.battleAtkRadioButton.isChecked(), self.ui.battleDefRadioButton.isChecked(),
        self.ui.battleSpaRadioButton.isChecked(), self.ui.battleSpdRadioButton.isChecked(), self.ui.battleSpeRadioButton.isChecked()]

        self._nickname = self.ui.battleNicknameLineEdit.text()
        isShiny = self.ui.battleShinyRadioButton.isChecked()
        self._moves[0] = self.ui.battleMove1LineEdit.text()
        self._moves[1] = self.ui.battleMove2LineEdit.text()
        self._moves[2] = self.ui.battleMove3LineEdit.text()
        self._moves[3] = self.ui.battleMove4LineEdit.text()
        self._gender = self.ui.battleGenderComboBox.currentText()
        self._sType = self.ui.battleSTypeComboBox.currentText()

        #change icon if shiny
        if isShiny:
            self._icon = '=image("https://www.serebii.net/Shiny/SWSH/' + self.dex + '.png")'

        #Create the shiny pokemon object
        battleMon = pokemon.battlePokemon(self._species, self._ball, self._ability, self._nature, self._gmax, self._zeroSpeed, self._ha, self._icon, self._ivs, self._nickname, self._moves, self._gender, self._sType, isShiny)

        #Validate all arguements are acceptable
        if not battleMon.validateMon():
            self.setError()
            return -1

        #Trim nature down to just one word, change the ball variable to be the proper value
        temp = battleMon.nature.split(' ', 1)
        battleMon.nature = temp[0]
        battleMon.setBallField()
        battleMon.setGenderSymbol()
        battleMon.setSTypeSymbol()

        #If the battle Pokemon is also shiny, make a shiny pokemon object
        if isShiny:
            battleShiny = pokemon.shinyPokemon(battleMon.species, battleMon.ball, battleMon.ability, battleMon.nature, battleMon.gmax, battleMon.zeroSpeed, battleMon.ha, battleMon.icon, battleMon.ivs, battleMon.nickname, battleMon.gender, battleMon.sType)
            googleAuth.addShiny(battleShiny)

        #Once pokemon is validated and submitted to the google doc, clear fields
        googleAuth.addBattle(battleMon)
        self.setSuccess()
        self.resetFields('battle')

    #Helper function that sets all class variables back to their "neutral" states: None, empty string, or 0
    def resetVariables(self):
        self.dex = ''
        self._icon = None
        self._species = ''
        self.mon = None
        self._ball = ''
        self._ability = ''
        self._ha = False 
        self._nature = ''
        self._moves = ['','','','']
        self._ivs = None
        self._gmax = False
        self._zeroSpeed = False
        self._nickname = ''
        self._ot = ''
        self._id = ''
        self._obtained = ''
        self._stock = 0
        self._gender = ''
        self._sType = ''
        self.isAbilityHidden = {}

    #Helper function that resets the fields of a tab based on the arguement given: 'sft', 'aft, 'shiny', or 'battle'
    def resetFields(self, type):
        if type == 'sft':
            self.ui.sftNatureDropdown.setCurrentIndex(0)
            self.ui.sftBallDropdown.setCurrentIndex(0)
            self.ui.sftAbilityDropdown.setCurrentIndex(0)
            self.ui.sftOtLineEdit.clear()
            self.ui.sftIdLineEdit.clear()
            self.ui.sftObtainedLineEdit.clear()
            self.ui.sftHpRadioButton.setChecked(False)
            self.ui.sftAtkRadioButton.setChecked(False)
            self.ui.sftDefRadioButton.setChecked(False)
            self.ui.sftSpaRadioButton.setChecked(False)
            self.ui.sftSpdRadioButton.setChecked(False)
            self.ui.sftSpeRadioButton.setChecked(False)
            self.ui.sftGMaxRadioButton.setChecked(False)
            self.ui.sftZeroSpeedRadioButton.setChecked(False)
            self.ui.sftGenderComboBox.setCurrentIndex(0)
            self.ui.sftSTypeComboBox.setCurrentIndex(0)

        elif type == 'aft':
            self.ui.aftNatureDropdown.setCurrentIndex(0)
            self.ui.aftBallDropdown.setCurrentIndex(0)
            self.ui.aftAbilityDropdown.setCurrentIndex(0)
            self.ui.aftIvDropdown.setCurrentIndex(0)
            self.ui.aftGMaxRadioButton.setChecked(False)
            self.ui.aftZeroSpeedRadioButton.setChecked(False)
            self.ui.aftStockSpinBox.setValue(0)

        elif type == 'shiny':
            self.ui.shinyNatureDropdown.setCurrentIndex(0)
            self.ui.shinyBallDropdown.setCurrentIndex(0)
            self.ui.shinyAbilityDropdown.setCurrentIndex(0)
            self.ui.shinyHpRadioButton.setChecked(False)
            self.ui.shinyAtkRadioButton.setChecked(False)
            self.ui.shinyDefRadioButton.setChecked(False)
            self.ui.shinySpaRadioButton.setChecked(False)
            self.ui.shinySpdRadioButton.setChecked(False)
            self.ui.shinySpeRadioButton.setChecked(False)
            self.ui.shinyGMaxRadioButton.setChecked(False)
            self.ui.shinyZeroSpeedRadioButton.setChecked(False)
            self.ui.shinyNicknameLineEdit.clear()
            self.ui.shinyGenderComboBox.setCurrentIndex(0)
            self.ui.shinySTypeComboBox.setCurrentIndex(0)

        elif type == 'battle':
            self.ui.battleNatureDropdown.setCurrentIndex(0)
            self.ui.battleBallDropdown.setCurrentIndex(0)
            self.ui.battleHpRadioButton.setChecked(False)
            self.ui.battleAtkRadioButton.setChecked(False)
            self.ui.battleDefRadioButton.setChecked(False)
            self.ui.battleSpaRadioButton.setChecked(False)
            self.ui.battleSpdRadioButton.setChecked(False)
            self.ui.battleSpeRadioButton.setChecked(False)
            self.ui.battleGMaxRadioButton.setChecked(False)
            self.ui.battleZeroSpeedRadioButton.setChecked(False)
            self.ui.battleNicknameLineEdit.clear()
            self.ui.battleMove1LineEdit.clear()
            self.ui.battleMove2LineEdit.clear()
            self.ui.battleMove3LineEdit.clear()
            self.ui.battleMove4LineEdit.clear()
            self.ui.battleGenderComboBox.setCurrentIndex(0)
            self.ui.battleSTypeComboBox.setCurrentIndex(0)
            self.ui.battleShinyRadioButton.setChecked(False)
    
    #Helper Function for keeping track of the current free row on all sheets
    def updateRowCounters(self):
        googleAuth.sftRow = googleAuth.nextAvailableRow(googleAuth.sheet.get_worksheet(0))
        googleAuth.aftRow = googleAuth.nextAvailableRow(googleAuth.sheet.get_worksheet(1))
        googleAuth.shinyRow = googleAuth.nextAvailableRow(googleAuth.sheet.get_worksheet(2))
        googleAuth.battleRow = googleAuth.nextAvailableRow(googleAuth.sheet.get_worksheet(3))
        global successText
        successText = 'First empty rows for each sheet found'
        self.setSuccess()    

    #Helper function to set error message in GUI
    def setError(self):
        self.ui.errorLabel.setStyleSheet('color: red')
        self.ui.errorLabel.setText(errorText)
    
    #Helper function to set success message in GUI
    def setSuccess(self):
        self.ui.errorLabel.setStyleSheet('color: green')
        self.ui.errorLabel.setText(successText)

    #Check if ability is hidden
    def checkAbility(self):
        try:
            self._ha = self.isAbilityHidden[self._ability]
            return True
        except:
            global errorText
            errorText = "Error: Please select an ability"
            self.setError()
            return False



