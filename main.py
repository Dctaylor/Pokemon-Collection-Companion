from PyQt5 import QtWidgets
import qtmodern.styles
import qtmodern.windows
import mywindow
import sys, os
#os.chdir(sys._MEIPASS)

def main():
	app = QtWidgets.QApplication([])
	application = mywindow.mywindow()
	qtmodern.styles.dark(app)
	mw = qtmodern.windows.ModernWindow(application)
	mw.show()
	sys.exit(app.exec())

if __name__ == '__main__':
	main()
