import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from .board_widget import Board_Widget

def start_QApplication():
    if not QApplication.instance():
        return QApplication(sys.argv)
        # return QApplication([]) 
            # if there's no chance of command-line arguments
    else:
        return QApplication.instance()

class GUI(QMainWindow):
    resized = pyqtSignal() # the signal if the window is resized
    
    def __init__(self, parent=None):        
        super(GUI, self).__init__(parent) # initialize
        self.do_close = False
        self.setWindowTitle("Checkers!") # set title
        
        # add an PumpInterface, which contains all the other widgets
        self.widget = Board_Widget(self) 
        self.setCentralWidget(self.widget) 
        self.setStyleSheet('background-color: black;')

        
            
    # send a signal whenever the window is resized (for resizing the image)
    def resizeEvent(self, event):
        self.resized.emit()
        if self.height() != self.width():
            self.resize(self.height()-25, self.height())
        # print(self.height())
        # self.set_width(3)
        return super(GUI, self).resizeEvent(event)