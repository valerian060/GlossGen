from PyQt5.QtWidgets import QDialog,QApplication,QMainWindow,QLabel,QVBoxLayout,QListWidgetItem,QWidget
from PyQt5.QtGui import QIcon,QFont,QMovie,QPixmap
from PyQt5.QtCore import QSize,QThread,pyqtSignal
from word_display import Ui_Dialog
from main_window import Ui_MainWindow
from welcome import Ui_welcomeWindow
from mini import Ui_minigame
from process_text import Text
from extract_text import img_preprocess,read_text,select_text
import sys,os,pickle,webbrowser,pdf2image,random
from gemini import Summarise

class Window(QMainWindow, Ui_welcomeWindow ):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon('Icons/Glossgen.png'))
        self.mini_game.setIcon(QIcon('Icons/game.png'))
        self.mini_game.setIconSize(QSize(30,30))
        self.pdf.setIcon(QIcon('Icons/pdf.png'))
        self.pdf.setIconSize(QSize(30,30))
        self.summarise_text.setIcon(QIcon('Icons/summary.png'))
        self.summarise_text.setIconSize(QSize(30,30))
        self.setAcceptDrops(True)
        self.pdf.clicked.connect(self.pdf_to_img)
        self.mini_game.clicked.connect(self.launch_game)
        self.summarise_text.clicked.connect(self.sum)
        

    def dragEnterEvent(self, event):
        print('drag-enter')
        if event.mimeData().hasUrls():
            print('has urls')
            event.accept()
        else:
            event.ignore()
    def dropEvent(self, event):	
        dirname = os.path.dirname(__file__)
        m=event.mimeData()
        self.current_img = os.path.join(dirname, m.urls()[0].toLocalFile())
        img_preprocess(self.current_img)
        self.hide()
        self.window=Window2(self,self.current_img)
        self.window.show()
    def pdf_to_img(self):
        self.animation=AnimatedWebP('Icons/drag.webp')
        self.animation.show()
        
    def launch_game(self):
        self.game=MiniGame()
        self.game.show()

    def sum(self):
        self.dialog=SummaryDialog()
        self.dialog.show()

			
class SummaryDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Summary")
        self.setWindowIcon(QIcon('Icons/Glossgen.png'))
        self.resize(300, 300)
        self.layout = QVBoxLayout()
        self.summary_label = QLabel()
        self.label = QLabel(self)
        self.movie = QMovie('Icons/drag.webp')
        self.label.setMovie(self.movie)   
        self.movie.start()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.setAcceptDrops(True)
        self.summary_label.setWordWrap(True)
        
	
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
         print(self.current_img)
         self.load_summary()
    def load_summary(self):
        self.label.close()
        self.label = QLabel(self)
        self.movie = QMovie('Icons/loading.webp')
        self.label.setMovie(self.movie) 
        self.movie.start()
        self.layout.addWidget(self.label)
        self.worker=Worker(self.current_img)
        self.worker.start()
        self.worker.result_signal.connect(self.update)

    def update(self,result):
         self.label.close()
         self.layout.addWidget(self.summary_label)
         self.summary_label.setText(result)
         

	

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
         print(self.current_img)
         images = pdf2image.convert_from_path(self.current_img,poppler_path = r"C:\Users\muham\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin")
         self.image_paths=[]
         for i in range(len(images)):
                images[i].save('pdf\page'+ str(i) +'.jpg', 'JPEG')
                self.image_paths.append('pdf\page'+str(i)+'.jpg')
         self.worker=Worker2(len(images),self.image_paths)
         self.worker.start()
         self.loading=AnimatedWebP('Icons\loading.webp')
         self.loading.show()
         self.worker.complete_signal.connect(self.display) 
    def display(self):
         self.loading.close()
         self.text_window=Window2()
         self.text_window.show()
               


class Window2(QMainWindow, Ui_MainWindow ):

	def __init__(self, parent=None, current_img=''):
		super().__init__(parent)
		self.setupUi(self)
		#self.window=window
		self.current_img=current_img
		self.setWindowTitle('GlossGen')
		self.setWindowIcon(QIcon('Icons/Glossgen.png'))
		self.select_roi.setIcon(QIcon('Icons/icon2.png'))
		self.select_roi.setText('')
		self.select_roi.setIconSize(QSize(60, 60))
		self.back.setIcon(QIcon('Icons/home.png'))
		self.back.setIconSize(QSize(30,30))
		self.load_text()
		self.update_list()
		self.word_list.currentRowChanged.connect(self.select_word)
		self.select_roi.clicked.connect(self.select)
		#self.back.clicked.connect(self.go_home)

	def load_text(self):
		self.glossary,self.meanings=Text().run()
		print(self.glossary)
			
	
	def update_list(self):
		for word in self.glossary:
			self.word_list.addItem(QListWidgetItem(word.capitalize()))
			
	def select_word(self,item):
			word=self.glossary[item]
			self.dialog=dialog(word,self.meanings[word][0])
			self.dialog.show()
	
	def select(self):
		read_text(select_text(self.current_img))
		self.word_list.clear()
		self.load_text()
		self.update_list()
	
	'''def go_home(self):
		self.hide()
		self.window.show()'''
          
class MiniGame(QDialog, Ui_minigame):
	
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi(self)
		self.setWindowTitle("GlossGen")
		font = QFont()
		font.setPointSize(15)
		self.word.setFont(font)
		self.next.setText('')
		self.total_score=0
		self.score.setText(str(self.total_score))
		self.next.setIcon(QIcon('Icons/next.png'))
		self.next.setIconSize(QSize(16,16))
		self.load_bookmarks()
		self.find_synonyms_antonyms()
		self.setWindowIcon(QIcon("Icons/game.png"))
		self.play()      
	def load_bookmarks(self):
		filename='data/bookmarks.pkl'
		if os.path.exists(filename):
			with open(filename, 'rb') as f:
				self.loaded_bookmarks = pickle.load(f)
    
	def find_synonyms_antonyms(self):
				self.antonyms={}
				self.synonyms={}
				with open('merged.pkl', 'rb') as f:
						self.word_info = pickle.load(f)
				
				for word in self.loaded_bookmarks:
					try:  
						if self.word_info[word.upper()]['ANTONYMS']:
							self.antonyms[word.capitalize()]=self.word_info[word.upper()]['ANTONYMS']
					except KeyError:
						pass
					try:
						if self.word_info[word.upper()]['SYNONYMS']:
							self.synonyms[word.capitalize()]=self.word_info[word.upper()]['SYNONYMS']
					except KeyError:
						pass

	def play(self):
						pixmap = QPixmap('Icons/question.png').scaled(16, 16)  
						self.right_wrong.setPixmap(pixmap)
						self.previous_words=[]
						choice=random.choice(['antonyms','synonyms'])
						self.question.setText(choice.capitalize())
						if choice=='antonyms':
								current_dict=self.antonyms
						else:
								current_dict=self.synonyms
						words=list(current_dict.keys())
						self.correct=random.choice(words)
						available_words = [word for word in words if word not in self.previous_words]
						wrong_word=random.choice(available_words)
						self.option1=option1=random.choice([self.correct,wrong_word])
						self.option2=option2=wrong_word if option1==self.correct else self.correct
						self.word.setText(self.correct)
						option1=current_dict[option1][random.randint(0,len(current_dict[option1])-1)]
						option2=current_dict[option2][random.randint(0,len(current_dict[option2])-1)]
						self.option_1.setText(option1.capitalize().replace('_',' '))
						self.option_2.setText(option2.capitalize().replace('_',' '))
						self.option_1.clicked.connect(self.verify_1)
						self.option_2.clicked.connect(self.verify_2)
						self.next.clicked.connect(self.play)
	def verify_1(self):
		if self.option1 == self.correct:
			pixmap = QPixmap('Icons/accept.png').scaled(16, 16)  
			self.right_wrong.setPixmap(pixmap)
			self.total_score+=10
			self.score.setText(str(self.total_score))
		else:
			pixmap = QPixmap('Icons/delete.png').scaled(16, 16)  
			self.right_wrong.setPixmap(pixmap)
	def verify_2(self):
		if self.option2 == self.correct:
			pixmap = QPixmap('Icons/accept.png').scaled(16, 16)  
			self.right_wrong.setPixmap(pixmap)
			self.total_score+=10
			self.score.setText(str(self.total_score))
		else:
			pixmap = QPixmap('Icons/delete.png').scaled(16, 16)  
			self.right_wrong.setPixmap(pixmap)
			
              
class dialog(QDialog,Ui_Dialog):
      
		def __init__(self,word,info,parent=None):
			super().__init__(parent)
			self.setupUi(self)
			self.setWindowTitle('Your Word')
			self.selected_word=word
			self.word_info=info    
			self.setWindowIcon(QIcon('Icons/Glossgen.png'))
			self.google.setIcon(QIcon('Icons/explore.png'))
			self.google.setIconSize(QSize(30, 30))
			self.bookmark.setIcon(QIcon('Icons/bookmark.png'))
			self.bookmark.setIconSize(QSize(30, 30))
			self.google.setText('')
			self.bookmark.setText('')
			self.word.setText(word.capitalize())
			self.word.setStyleSheet("font-weight: bold")
			self.word.setFont(QFont('Arial', 10))
			self.info.setText(info) 
			self.info.setWordWrap(True)             
			self.bookmark.clicked.connect(self.add_to_bookmarks)
			self.google.clicked.connect(self.search)
				
		def add_to_bookmarks(self):
					filename='data/bookmarks.pkl'
					if os.path.exists(filename):
							with open(filename, 'rb') as f:
									loaded_bookmarks = pickle.load(f)
									print(loaded_bookmarks)
									loaded_bookmarks.add(self.selected_word)
							with open(filename, 'wb') as f:
								pickle.dump(loaded_bookmarks,f)

					else:
							loaded_bookmarks={self.selected_word}
							with open(filename, 'wb') as f:
								pickle.dump(loaded_bookmarks,f)
		def search(self):
			webbrowser.open(f'https://en.wiktionary.org/wiki/{self.selected_word}')
                     

class Worker(QThread):
    def __init__(self, img_path):
        super().__init__()
        self.img = img_path
    result_signal = pyqtSignal(str) 
    def run(self):
        result = Summarise().upload_image(self.img)
        self.result_signal.emit(result)
        

class Worker2(QThread):
    def __init__(self, len,img_paths):
        super().__init__()
        self.len = len
        self.paths=img_paths
    complete_signal = pyqtSignal() 
    def run(self):
         file = open("data/recognized.txt", 'w+')
         file.write("")
         file.close()

         for i in range(self.len):
                 img_preprocess(self.paths[i],'a+')
        
         self.complete_signal.emit()
        
              

def main():
	app=QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])
	window=Window()
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