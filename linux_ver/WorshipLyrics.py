# -*- coding: utf-8 -*-
import sys, os, string, codecs
from PyQt4.QtGui import *
from PyQt4 import *
from PyQt4.QtCore import Qt
#import ctypes


class Frame(QtGui.QFrame):
    
    def __init__(self, parent = None):
        QtGui.QFrame.__init__(self,parent)
        self.storageType = 0 # 0 for default, 1 for input
        self.count = -1
        self.fontSize = 30
        self.lyrics = []
        self.content = []
        self.hided = False
        self.borderless = False
        self.listing = False
        self.mouseTrack = True
        self.initUI()
        
        
    def initUI(self):
        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.windowed = """
        QFrame{
            Background: #151515;
            border-radius: 0px
        }
        QLabel{
            font-weight:bold;
            color: white;
        }
        QLineEdit{
            Background: #FFFFFF;
            color:#151515
        }
        QListWidget{
            Background: #FFFFFF;
            color: #151515
        }
        """
        
        self.fullscreen = """
        QFrame{
            Background: #151515;
            border-radius: 0px
        }
        QLabel{
            font-weight:bold;
            color: white;
        }
        QLineEdit{
            Background: #FFFFFF;
            color:#151515
        }
        QListWidget{
            Background: #FFFFFF;
            color: #151515
        }
        """
        self.setStyleSheet(self.windowed) 
        
        vbox=QtGui.QVBoxLayout(self);

        layout=QtGui.QVBoxLayout();
        layout.setMargin(5);
        layout.setSpacing(5);
        vbox.addLayout(layout)
        
        # Set the Font
        self.font = QFont()
        self.fontsize = 30
        self.font.setPointSize(self.fontSize)
        
        # Set the displayArea
        self.displayArea = QLabel(self)
        self.displayArea.setAlignment(Qt.AlignCenter)

        self.displayArea.setFont(self.font)
        
        # Set the InputBox
        self.inputBox = QLineEdit(self)
        self.inputBox.setFixedSize(500,20)
        self.inputBox.setAlignment(Qt.AlignCenter)
        self.inputBox.returnPressed.connect(self.getText)

        # Set the list view
        self.listdir = QListWidget(self)
        line = ''
        dirs = os.listdir(self.resource_path('src/lyrics'))
        for filename in dirs:
            filename = self.cleanFilename(filename)
            path = self.resource_path('src/lyrics/' + filename)
            with codecs.open(path,'r', 'utf-8') as f:
                line = f.readline()
                line = line.replace('\n','')
                self.listdir.addItem(line)
        self.listdir.sortItems(Qt.AscendingOrder)
        self.listdir.close()
        self.listdir.setCurrentRow(0)
        self.listdir.itemActivated.connect(self.retrieveList)
        
        self.iBox = QtGui.QGridLayout()
        self.iBox.addWidget(self.inputBox,1,0)

        self.resize(800,600)
        self.center()
        
        layout.addWidget(self.displayArea)
        layout.addLayout(self.iBox)
        layout.addWidget(self.listdir)
        
        # Set the File Prompt
        self.filePrompt = QFileDialog()
        
        # Set the window
        self.setWindowTitle('Worship Lyrics')
        self.setWindowIcon(QtGui.QIcon(self.resource_path('src/icon/logo.ico')))
        
        # Window only
        #myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
        #ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        
        self.show()
    
    # Get the center
    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    
    # Get text from input box
    def getText(self):        
        self.initDisplay(self.inputBox.text())
            
    # Get text from list
    def retrieveList(self):
        self.initDisplay(self.listdir.currentItem().text())
        
    # init display
    def initDisplay(self, name):
        self.closeList()
        
        if (name == ''):
                return
        
        if self.storageType == 0:
            filename= ''
            
            filename = self.cleanFilename(name)
            filename = filename + '.txt'
            path = self.resource_path('src/lyrics/' + filename)
            
            self.readFile(path, name)
        elif self.storageType == 1:
            self.readFile(name, name)
       
    # read file
    def readFile(self, path, name):
        if os.path.exists(path):
            self.count = -1
            self.content = []
            self.lyrics = []
            with codecs.open(path, 'r', 'utf-8') as f:
                self.content = f.readlines()
            self.parse()
            self.display(self.read_down())
            self.inputBox.clear()
        else:
            self.display(name + " not found.")

    # parse data
    def parse(self):
        self.content.append('\n')
        info = ''
        for line in self.content:
            if line != '\n':
                info = info +  line
            else:
                info.encode('utf-8')
                if self.checkEmpty(info) == False:
                    self.lyrics.append(info)
                info = ''
        return info        
    
    # Clean file name
    def cleanFilename(self, filename):
        filename = str(filename).lower()
        filename = filename.replace(' ','')
        filename = filename.replace(',','')
        filename = filename.replace('(','')
        filename = filename.replace(')','')
        filename = filename.replace('[','')
        filename = filename.replace(']','')
        filename = filename.replace('"','')
        return filename
    
    # display all song
    def checkDisplayList(self):
        if self.listing == False:
            self.displayList()
        elif self.listing == True:
            self.closeList()
            
    def displayList(self):
        self.displayArea.close()
        self.inputBox.show()
        self.listdir.show()
        self.listing = True
        self.mouseTrack = False
            
    # Close list
    def closeList(self):
        self.displayArea.show()
        self.listdir.close()
        self.inputBox.hide()
        self.listing = False
        self.mouseTrack = True
    
    # display 
    def display(self, info):
        if self.checkEmpty(info) == False:
            self.displayArea.setText(info)
        
    # check fullscreen        
    def checkFullscreen(self):
        if (self.borderless == False):
            self.enterFullscreen()
        elif (self.borderless == True):
            self.enterWindowed()
    
    # Enter fullscreen
    def enterFullscreen(self):
        self.changeFont('fixed',40)
        self.hideInputBox()
        self.setStyleSheet(self.fullscreen) 
        self.showFullScreen()
        self.borderless = True
    
    # Enter Normal
    def enterWindowed(self):
        self.changeFont('fixed',30)
        self.setStyleSheet(self.windowed)
        self.showNormal()
        self.resize(800,600)
        self.center()
        self.borderless = False  
    # Show or hide the input box        
    def checkInputBox(self):
        if self.hided == True:
            self.showInputBox()
        elif self.hided == False:
            self.hideInputBox()
    
    # hide input box    
    def hideInputBox(self):
        self.inputBox.hide()
        self.inputBox.setReadOnly(1)
        self.inputBox.clear()
        self.hided = True
     
    # show input box 
    def showInputBox(self):
        self.inputBox.show()
        self.inputBox.setReadOnly(0)
        self.hided = False

    # read down
    def read_down(self):
        info = ''
        if (self.count + 1 > len(self.lyrics) - 1):
            self.count = len(self.lyrics) - 1
        else:
            self.count = self.count + 1
        if (len(self.lyrics) > self.count and self.count != -1):
            info = self.lyrics[self.count]
        return info
    
    # read up
    def read_up(self):
        info = ''
        if (self.count - 1 < 0):
            self.count = 0
        else:
            self.count = self.count - 1
            
        if (len(self.lyrics) > self.count and self.count != -1):
            info = self.lyrics[self.count]
        return info
    
    # Check empty line
    def checkEmpty(self, line):
        if line == '\n' or line == '':
            return True
        else:
            return False
    
    # locate the temp src path
    def resource_path(self, relative):
        if hasattr(sys, "_MEIPASS"):
            return sys._MEIPASS + '/' + relative
        return relative
    
    # change font size            
    def changeFont(self, type, factor):
        if self.fontSize + factor < 0 and self.fontSize + factor > 80:
            return
        if type == 'dynamic':
            self.fontSize += factor
        elif type == 'fixed':
            self.fontSize = factor
            
        self.font.setPointSize(self.fontSize)
        self.displayArea.setFont(self.font)
    
    # Increase Font size
    def increaseFontSize(self):
        self.changeFont('dynamic', 5)
    
    # Decrease Font size
    def decreaseFontSize(self):
        self.changeFont('dynamic', -5)
        
    # Key pressed
    def keyPressEvent(self, event):
        key = event.key()
        
        if key == Qt.Key_Down:
            self.display(self.read_down())
            
        if key == Qt.Key_Up:
            self.display(self.read_up())
            
        if key == Qt.Key_F11:
            self.checkFullscreen()
            
        if key == Qt.Key_F1:
            self.checkDisplayList()
            
        if key == Qt.Key_F3:
            self.increaseFontSize()
        
        if key == Qt.Key_F4:
            self.decreaseFontSize()
        
        if key == Qt.Key_F5:
            self.clear()
            
        if key == Qt.Key_F2:
            self.storageType = 1
            filename = self.filePrompt.getOpenFileName()
            self.initDisplay(filename)
   
            
        if key == Qt.Key_Escape:
            self.enterWindowed()
            
        if key == Qt.Key_Return:
            self.checkInputBox()
            
        if key >= Qt.Key_A and key <= Qt.Key_Z:
            self.inputBox.show()
            self.inputBox.setReadOnly(0)
            self.hided = False
            self.inputBox.insert(QKeySequence(key).toString())
            #self.showInputBox

    # Mouse clicked
    def mousePressEvent(self, event):
        if self.mouseTrack == True:
            self.checkInputBox()      
        
        
def main():
    app = QtGui.QApplication(sys.argv)
    ex = Frame()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    