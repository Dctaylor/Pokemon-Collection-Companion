import gspread
import mywindow
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint


# If modifying these scopes, delete the file token.pickle.
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

# The ID and range of a sample spreadsheet.
spreadsheetID = '1st0NNMj-jp91KW1ypU02eiPapkDnXNI3SivHo10K8y4'
creds = None
client = None
sheet = None
sftRow = 2
aftRow = 2
shinyRow = 2
battleRow = 2

def googleAuth():
    #Tell function that we are using the global variables
    global creds 
    global client 
    global sheet

    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheetID)  # Open the spreadhseet

def addSFT(pokemon):
    global sftRow

    # Call the Sheets API and add the SFT
    sftSheet = sheet.get_worksheet(0)
    sftSheet.update_acell('A' + str(sftRow), pokemon.icon)
    sftSheet.update_acell('B' + str(sftRow), pokemon.ball)
    sftSheet.update_acell('C' + str(sftRow), pokemon.species)
    sftSheet.update_acell('D' + str(sftRow), pokemon.gender)
    sftSheet.update_acell('E' + str(sftRow), pokemon.nature)
    sftSheet.update_acell('F' + str(sftRow), pokemon.ability)
    sftSheet.update_acell('G' + str(sftRow), pokemon.ivs[0])
    sftSheet.update_acell('H' + str(sftRow), pokemon.ivs[1])
    sftSheet.update_acell('I' + str(sftRow), pokemon.ivs[2])
    sftSheet.update_acell('J' + str(sftRow), pokemon.ivs[3])
    sftSheet.update_acell('K' + str(sftRow), pokemon.ivs[4])
    sftSheet.update_acell('L' + str(sftRow), pokemon.ivs[5])
    sftSheet.update_acell('N' + str(sftRow), pokemon.gmax)
    sftSheet.update_acell('O' + str(sftRow), pokemon.ha)
    sftSheet.update_acell('P' + str(sftRow), pokemon.zeroSpeed)
    sftSheet.update_acell('Q' + str(sftRow), pokemon.sType)
    sftSheet.update_acell('R' + str(sftRow), pokemon.ot)
    sftSheet.update_acell('S' + str(sftRow), pokemon.id)
    sftSheet.update_acell('T' + str(sftRow), pokemon.obtained)
    mywindow.successText = pokemon.species + ' added to Shinies for Trade Sheet Row ' + sftRow
    sftRow += 1

def addAFT(pokemon):
    global aftRow

    # Call the Sheets API and add the AFT
    aftSheet = sheet.get_worksheet(1)
    aftSheet.update_acell('A' + str(aftRow), pokemon.icon)
    aftSheet.update_acell('B' + str(aftRow), pokemon.species)
    aftSheet.update_acell('C' + str(aftRow), pokemon.nature)
    aftSheet.update_acell('D' + str(aftRow), pokemon.ability)
    aftSheet.update_acell(pokemon.ball + str(aftRow), True)
    aftSheet.update_acell('O' + str(aftRow), pokemon.gmax)
    aftSheet.update_acell('P' + str(aftRow), pokemon.ha)
    aftSheet.update_acell('Q' + str(aftRow), pokemon.ivs)
    aftSheet.update_acell('R' + str(aftRow), pokemon.zeroSpeed)
    aftSheet.update_acell('S' + str(aftRow), pokemon.stock)
    mywindow.successText = pokemon.species + ' added to Aprimon for Trade Sheet Row ' + aftRow
    aftRow += 1

def addShiny(pokemon):
    global shinyRow

    # Call the Sheets API and add the Shiny
    shinySheet = sheet.get_worksheet(2)
    shinySheet.update_acell('A' + str(shinyRow), pokemon.icon)
    shinySheet.update_acell('B' + str(shinyRow), pokemon.ball)
    shinySheet.update_acell('C' + str(shinyRow), pokemon.species)
    shinySheet.update_acell('D' + str(shinyRow), pokemon.nickname)
    shinySheet.update_acell('E' + str(shinyRow), pokemon.gender)
    shinySheet.update_acell('F' + str(shinyRow), pokemon.nature)
    shinySheet.update_acell('G' + str(shinyRow), pokemon.ability)
    shinySheet.update_acell('H' + str(shinyRow), pokemon.ivs[0])
    shinySheet.update_acell('I' + str(shinyRow), pokemon.ivs[1])
    shinySheet.update_acell('J' + str(shinyRow), pokemon.ivs[2])
    shinySheet.update_acell('K' + str(shinyRow), pokemon.ivs[3])
    shinySheet.update_acell('L' + str(shinyRow), pokemon.ivs[4])
    shinySheet.update_acell('M' + str(shinyRow), pokemon.ivs[5])
    shinySheet.update_acell('O' + str(shinyRow), pokemon.gmax)
    shinySheet.update_acell('P' + str(shinyRow), pokemon.ha)
    shinySheet.update_acell('Q' + str(shinyRow), pokemon.zeroSpeed)
    shinySheet.update_acell('R' + str(shinyRow), pokemon.sType)
    mywindow.successText = pokemon.species + ' added to Shinies Sheet Row ' + shinyRow
    shinyRow += 1
   
def addBattle(pokemon):
    global battleRow

    # Call the Sheets API and add the Battler
    battleSheet = sheet.get_worksheet(3)
    battleSheet.update_acell('A' + str(battleRow), pokemon.icon)
    battleSheet.update_acell('B' + str(battleRow), pokemon.ball)
    battleSheet.update_acell('C' + str(battleRow), pokemon.species)
    battleSheet.update_acell('D' + str(battleRow), pokemon.nickname)
    battleSheet.update_acell('E' + str(battleRow), pokemon.gender)
    battleSheet.update_acell('F' + str(battleRow), pokemon.nature)
    battleSheet.update_acell('G' + str(battleRow), pokemon.ability)
    battleSheet.update_acell('H' + str(battleRow), pokemon.ivs[0])
    battleSheet.update_acell('I' + str(battleRow), pokemon.ivs[1])
    battleSheet.update_acell('J' + str(battleRow), pokemon.ivs[2])
    battleSheet.update_acell('K' + str(battleRow), pokemon.ivs[3])
    battleSheet.update_acell('L' + str(battleRow), pokemon.ivs[4])
    battleSheet.update_acell('M' + str(battleRow), pokemon.ivs[5])
    battleSheet.update_acell('O' + str(battleRow), pokemon.gmax)
    battleSheet.update_acell('P' + str(battleRow), pokemon.isShiny)
    battleSheet.update_acell('Q' + str(battleRow), pokemon.ha)
    battleSheet.update_acell('R' + str(battleRow), pokemon.zeroSpeed)
    battleSheet.update_acell('T' + str(battleRow), pokemon.moves[0])
    battleSheet.update_acell('U' + str(battleRow), pokemon.moves[1])
    battleSheet.update_acell('V' + str(battleRow), pokemon.moves[2])
    battleSheet.update_acell('W' + str(battleRow), pokemon.moves[3])
    mywindow.successText = pokemon.species + ' added to Battlers/Keeps Sheet Row ' + battleRow
    battleRow += 1

def nextAvailableRow(worksheet):
    str_list = list(filter(None, worksheet.col_values(3)))
    return len(str_list)+1
