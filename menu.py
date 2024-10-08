from extract_text import img_preprocess,read_text
from welcome import Ui_welcomeWindow
from PyQt5.QtGui import QIcon,QFont,QMovie
from PyQt5.QtWidgets import QDialog,QApplication,QMainWindow,QVBoxLayout,QLabel,QWidget
from PyQt5.QtCore import QSize
import sys,os
import main_ui
class Window(QMainWindow, Ui_welcomeWindow ):
    def __init__(self,app, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon('Icons/Glossgen.png'))
        self.app=app
        self.mini_game.setIcon(QIcon('Icons/game.png'))
        self.mini_game.setIconSize(QSize(30,30))
        self.pdf.setIcon(QIcon('Icons/pdf.png'))
        self.pdf.setIconSize(QSize(30,30))
        self.summarise_text.setIcon(QIcon('Icons/summary.png'))
        self.summarise_text.setIconSize(QSize(30,30))
        self.setAcceptDrops(True)
        self.pdf.clicked.connect(self.pdf_to_img)
        

    def dragEnterEvent(self, event):
        print('drag-enter')
        if event.mimeData().hasUrls():
            print('has urls')
            event.accept()
        else:
            event.ignore()
            
    def dropEvent(self, event):
         m=event.mimeData()
         dirname = os.path.dirname(__file__)
         self.current_img = os.path.join(dirname, m.urls()[0].toLocalFile())
         #print(self.current_img)
         img_preprocess(self.current_img)
         self.hide()
         main_ui.main()
         
         
         
    def pdf_to_img(self):
        self.animation=AnimatedWebP('Icons/drag.webp')
        self.animation.show()
        

class AnimatedWebP(QWidget):
    def __init__(self, webp_file):
        super().__init__()
        self.setWindowIcon(QIcon('Icons/Glossgen.png'))
        self.label = QLabel(self)
        self.movie = QMovie(webp_file)

        self.label.setMovie(self.movie)
        
        self.movie.start()
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.setWindowTitle('GlossGen')
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        print('drag-enter')
        if event.mimeData().hasUrls():
            print('has urls')
            event.accept()
        else:
            event.ignore()
            
    def dropEvent(self, event):
         m=event.mimeData()
         self.current_img=m.urls()[0].toLocalFile()
         

def main():
    app=QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])
    window=Window(app)
    app.setStyleSheet('''QMainWindow {
        background-color:#1e1d23;
	}
	QDialog {
		background-color:#1e1d23;
	}
	QColorDialog {
		background-color:#1e1d23;
	}
	QTextEdit {
		background-color:#1e1d23;
		color: #a9b7c6;
	}
	QPlainTextEdit {
		selection-background-color:#007b50;
		background-color:#1e1d23;
		border-style: solid;
		border-top-color: transparent;
		border-right-color: transparent;
		border-left-color: transparent;
		border-bottom-color: transparent;
		border-width: 1px;
		color: #a9b7c6;
	}
	QPushButton{
		border-style: solid;
		border-top-color: transparent;
		border-right-color: transparent;
		border-left-color: transparent;
		border-bottom-color: transparent;
		border-width: 1px;
		border-style: solid;
		color: #a9b7c6;
		padding: 2px;
		background-color: #1e1d23;
	}
	QPushButton::default{
		border-style: inset;
		border-top-color: transparent;
		border-right-color: transparent;
		border-left-color: transparent;
		border-bottom-color: #04b97f;
		border-width: 1px;
		color: #a9b7c6;
		padding: 2px;
		background-color: #1e1d23;
	}
	QToolButton:hover{
		border-style: solid;
		border-top-color: transparent;
		border-right-color: transparent;
		border-left-color: transparent;
		border-bottom-color: #37efba;
		border-bottom-width: 2px;
		border-style: solid;
		color: #FFFFFF;
		padding-bottom: 1px;
		background-color: #1e1d23;
	}
	QPushButton:hover{
		border-style: solid;
		border-top-color: transparent;
		border-right-color: transparent;
		border-left-color: transparent;
		border-bottom-color: #37efba;
		border-bottom-width: 1px;
		border-style: solid;
		color: #FFFFFF;
		padding-bottom: 2px;
		background-color: #1e1d23;
	}
	QPushButton:pressed{
		border-style: solid;
		border-top-color: transparent;
		border-right-color: transparent;
		border-left-color: transparent;
		border-bottom-color: #37efba;
		border-bottom-width: 2px;
		border-style: solid;
		color: #37efba;
		padding-bottom: 1px;
		background-color: #1e1d23;
	}
	QPushButton:disabled{
		border-style: solid;
		border-top-color: transparent;
		border-right-color: transparent;
		border-left-color: transparent;
		border-bottom-color: #808086;
		border-bottom-width: 2px;
		border-style: solid;
		color: #808086;
		padding-bottom: 1px;
		background-color: #1e1d23;
	}
	QLineEdit {
		border-width: 1px; border-radius: 4px;
		border-color: rgb(58, 58, 58);
		border-style: inset;
		padding: 0 8px;
		color: #a9b7c6;
		background:#1e1d23;
		selection-background-color:#007b50;
		selection-color: #FFFFFF;
	}
	QLabel {
		color: #a9b7c6;
	}
					
	QListWidget{
		color:rgb(240, 240, 240);
		background-color: #1e1d23; 
		selection-background-color:#007b50;
	}
					
	QProgressBar {
		text-align: center;
		color: rgb(240, 240, 240);
		border-width: 1px; 
		border-radius: 10px;
		border-color: rgb(58, 58, 58);
		border-style: inset;
		background-color:#1e1d23;
	}
	QProgressBar::chunk {
		background-color: #04b97f;
		border-radius: 5px;
	}

	QComboBox {
		color: #a9b7c6;	
		background: #1e1d23;
	}
	QComboBox:editable {
		background: #1e1d23;
		color: #a9b7c6;
		selection-background-color: #1e1d23;
	}
	QComboBox QAbstractItemView {
		color: #a9b7c6;	
		background: #1e1d23;
		selection-color: #FFFFFF;
		selection-background-color: #1e1d23;
    }
    QComboBox: !editable:on, QComboBox::drop-down:editable:on {
        color: #a9b7c6;	
        background: #1e1d23;
    }
    ''')
    app.setStyle("Fusion")
    window.show()
    app.exec()
     
if __name__=="__main__":
	main()
