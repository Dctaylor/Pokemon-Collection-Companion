import string
import mywindow

ballNumbers = {
    'Beast Ball': '6',
    'Cherish Ball': '7',
    'Dive Ball': '8',
    'Dream Ball': '9',
    'Dusk Ball': '10',
    'Fast Ball': '11',
    'Friend Ball': '12',
    'Great Ball': '13',
    'Heal Ball': '14',
    'Heavy Ball': '15',
    'Level Ball': '16',
    'Love Ball': '17',
    'Lure Ball': '18',
    'Luxury Ball': '19',
    'Master Ball': '20',
    'Moon Ball': '21',
    'Nest Ball': '22',
    'Net Ball': '23',
    'Park Ball': '24',
    'Poke Ball': '25',
    'Premier Ball': '26',
    'Quick Ball': '27',
    'Repeat Ball': '28',
    'Safari Ball': '29',
    'Sport Ball': '30',
    'Timer Ball': '31',
    'Ultra Ball': '32'
}

ballColumns = {
    'Beast Ball': 'E',
    'Dream Ball': 'F',
    'Fast Ball': 'G',
    'Friend Ball': 'H',
    'Heavy Ball': 'I',
    'Level Ball': 'J',
    'Love Ball': 'K',
    'Lure Ball': 'L',
    'Moon Ball': 'M'
}

class pokemon():
    def __init__(self, _species, _ball, _ability, _nature, _gmax, _zeroSpeed, _ha, _icon, _ivs):
        self.species = _species
        self.ball = _ball
        self.ability = _ability
        self.nature = _nature
        self.gmax = _gmax
        self.zeroSpeed = _zeroSpeed
        self.ha = _ha
        self.icon = _icon
        self.ivs = _ivs

    def setBallField(self):
        self.ball = '=Pokeballs!C' + ballNumbers.get(self.ball)
        
    
    #Method to valid that proper input has been obtained
    def validateMon(self):
        if self.species == None or self.species == '':
            mywindow.errorText = 'Error: Invalid Species'
            return False
        if self.ball == None or self.ball == '':
            mywindow.errorText = 'Error: Please select a Ball'
            return False
        if self.ability == None or self.ability == '':
            mywindow.errorText = 'Error: Please select an ability'
            return False
        if self.nature == None or self.nature == '':
            mywindow.errorText = 'Error: Please select a Nature'
            return False
        return True
        
class sftPokemon(pokemon):
    def __init__(self, _species, _ball, _ability, _nature, _gmax, _zeroSpeed, _ha, _icon, _ivs, _ot, _id, _obtained, _gender, _sType):
        super().__init__(_species, _ball, _ability, _nature, _gmax, _zeroSpeed, _ha, _icon, _ivs)
        self.ot = _ot
        self.id = _id
        self.obtained = _obtained
        self.gender = _gender
        self.sType = _sType

    def validateMon(self):
        if not super().validateMon():
            return False
        if self.ot == None or self.ot == '' or self.ot.isspace():
            mywindow.errorText = 'Error: Please input the name of the original Trainer'
            return False
        if self.id == None or self.id == '' or self.id.isspace():
            mywindow.errorText = 'Error: Please input the id of the original Trainer'
            return False
        elif not self.id.isdigit():
            mywindow.errorText = 'Error: Please input only numbers for the Trainer id'
            return False
        if self.obtained == None or self.obtained == '' or self.obtained.isspace():
            mywindow.errorText = 'Error: Please input how this shiny was obtained'
            return False
        if self.sType == None or self.sType == '':
            mywindow.errorText = "Error: Please select if it's a Star or Square Shiny"
            return False
        if self.gender == None or self.gender == '':
            mywindow.errorText = "Error: Please select a gender"
            return False
        return True
    
    def setGenderSymbol(self):
        if self.gender == "Male":
            self.gender = '♂'
            return
        elif self.gender == 'Genderless':
            self.gender = ''
            return
        self.gender = '♀'
    
    def setSTypeSymbol(self):
        if self.sType == 'Star':
            self.sType = '★'
            return
        self.sType = '□'
        
class aftPokemon(pokemon):
    def __init__(self, _species, _ball, _ability, _nature, _gmax, _zeroSpeed, _ha, _icon, _ivs, _stock):
        super().__init__(_species, _ball, _ability, _nature, _gmax, _zeroSpeed, _ha, _icon, _ivs)
        self.stock = _stock
    
    def validateMon(self):
        if not super().validateMon():
            return False
        if self.stock == None or not self.stock > 0:
            mywindow.errorText = 'Error: Please input the stock for this Pokemon'
            return False
        if self.ivs == None or self.ivs == '':
            mywindow.errorText = 'Error: Please select the amount of perfect Ivs this/these pokemon have'
            return False
        return True
    
    def aftBallHelper(self):
        self.ball = ballColumns.get(self.ball)

class shinyPokemon(pokemon):
    def __init__(self, _species, _ball, _ability, _nature, _gmax, _zeroSpeed, _ha, _icon, _ivs, _nickname, _gender, _sType):
        super().__init__(_species, _ball, _ability, _nature, _gmax, _zeroSpeed, _ha, _icon, _ivs)
        self.nickname = _nickname
        self.gender = _gender
        self.sType = _sType
    
    def validateMon(self):
        if not super().validateMon():
            return False
        if self.sType == None or self.sType == '':
            mywindow.errorText = "Error: Please select if it's a Star or Square Shiny"
            return False
        if self.gender == None or self.gender == '':
            mywindow.errorText = "Error: Please select a gender"
            return False
    
    def setGenderSymbol(self):
        if self.gender == "Male":
            self.gender = '♂'
            return
        elif self.gender == 'Genderless':
            self.gender = ''
            return
        self.gender = '♀'
    
    def setSTypeSymbol(self):
        if self.sType == 'Star':
            self.sType = '★'
            return
        self.sType = '□'
        
class battlePokemon(pokemon):
    def __init__(self, _species, _ball, _ability, _nature, _gmax, _zeroSpeed, _ha, _icon, _ivs, _nickname, _moves, _gender, _sType, _isShiny):
        super().__init__(_species, _ball, _ability, _nature, _gmax, _zeroSpeed, _ha, _icon, _ivs)
        self.nickname = _nickname
        self.moves = _moves
        self.gender = _gender
        self.sType = _sType
        self.isShiny = _isShiny
    
    def validateMon(self):
        if not super().validateMon():
            return False
        if self.isShiny == True and (self.sType == None or self.sType == ''):
            mywindow.errorText = "Error: Please select if it's a Star or Square Shiny"
            return False
        if self.gender == None or self.gender == '':
            mywindow.errorText = "Error: Please select a gender"
            return False
        
        #only check if first move is empty, as there only needs to be a minimum of 1 move
        if self.moves[0] == None or self.moves[0] == '' or self.moves[0].isspace():
            mywindow.errorText = 'Please input atleast one move'
            return False

        return True
    
    def setGenderSymbol(self):
        if self.gender == "Male":
            self.gender = '♂'
            return
        elif self.gender == 'Genderless':
            self.gender = ''
            return
        self.gender = '♀'
    
    def setSTypeSymbol(self):
        if self.sType == "Star":
            self.sType = '★'
            return
        self.sType = '□'
