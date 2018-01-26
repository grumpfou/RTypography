from PyQt5 import QtGui, QtCore, QtWidgets

from RTypographyGuiAdditionalFunctions import *
from RTypographyDocument import Document
from RTypographyLanguages import dict_languages,Language


import sys,codecs,os
"""A Gui version of the RTypography"""

list_char_nums = ["⓪","①","②","③","④","⑤","⑥","⑦","⑧","⑨","⑩","⑪","⑫","⑬","⑭","⑮","⑯","⑰","⑱","⑲","⑳"]



class GuiDocument(QtGui.QTextDocument):
	"""
	A reimplementation of QTextDocument with additional languages
	"""

	def __init__(self,language=None,*args,**kargs):
		QtGui.QTextDocument.__init__(self,*args,**kargs)
		self.changeLanguage(language)
		self.list_corrections= []

	def changeLanguage(self,language):

		if issubclass(type(language),Language) or (language is None):
			self.language = language
		else:
			self.language = dict_languages[language]


	def SLOT_highlight_detect_exclude(self):
		doc = Document(self.toPlainText(),language=self.language)

		doc.detect_exclude()

		## RAZ
		cursor = QtGui.QTextCursor(self)
		cursor.select(QtGui.QTextCursor.Document)
		fmt = cursor.charFormat()
		fmt.setForeground(QtCore.Qt.black)
		fmt.setBackground(QtCore.Qt.white)
		fmt.setProperty(QtGui.QTextFormat.UserProperty,None)
		cursor.setCharFormat(fmt)

		for ex in doc.excludes:
			cursor = QtGui.QTextCursor(self)
			cursor.setPosition(ex[0])
			cursor.setPosition(ex[1],QtGui.QTextCursor.KeepAnchor)
			self.inverse_exclude(cursor=cursor)


	def inverse_exclude(self,cursor):
		"""
		force: bool. If True will force to apply the exlusion, otherwise, will
			inverse the style.
		"""
		if cursor.hasSelection():
			fmt = cursor.charFormat()
			id = fmt.property(QtGui.QTextFormat.UserProperty)
			if id == 1:
				fmt.setForeground(QtCore.Qt.black)
				fmt.setBackground(QtCore.Qt.white)
				fmt.setProperty(QtGui.QTextFormat.UserProperty,None)
			else:
				fmt.setForeground(QtCore.Qt.white)
				fmt.setBackground(QtCore.Qt.red)
				fmt.setProperty(QtGui.QTextFormat.UserProperty,1)

			cursor.setCharFormat(fmt)



	def run(self,show_changes=True):
		if self.language==None:
			raise BaseException("Please specify the language via the changeLanguage method")
		cursor = QtGui.QTextCursor(self)
		self.list_corrections= []
		max_iterations = 1000

		def correctionChar():
			r= True
			i = 0
			while r and i<max_iterations :
					r = self.language.correctBetweenChars(cursor)
					if r:
						self.list_corrections.append(r)
					i+=1
			if i==max_iterations: print("Max iteration at position %i"%cursor.position())

		def correctionWord():
			r= True
			i = 0
			while r and i<max_iterations :
					r = self.language.correctAfterWord(cursor)
					if r: self.list_corrections.append(r)
					i+=1
			if i==max_iterations: print("Max iteration at position %i"%cursor.position())

		# We correct all the information in the document
		correctionChar()
		while cursor.movePosition(QtGui.QTextCursor.Right):
			if cursor.charFormat().property(QtGui.QTextFormat.UserProperty)!=1:
				# If it is not in an exclude area
				correctionChar()
				if not cursor.nextChar().isalnum():
					correctionWord()



		# We display the changes if needed
		if show_changes:
			for rule,cursor in self.list_corrections:
				fmt = QtGui.QTextCharFormat()
				fmt.setForeground(QtCore.Qt.darkGreen)
				cursor.insertText(list_char_nums[rule.number],fmt)
				cursor.movePosition(QtGui.QTextCursor.Left,QtGui.QTextCursor.KeepAnchor)

	def removeShowChanges(self):
		for rule,cursor in self.list_corrections:
			cursor.removeSelectedText()

	def clone(self,language=None):
		if language==None: language=self.language
		other = GuiDocument(language=language)
		cursor_old = QtGui.QTextCursor(self)
		cursor_old.select(QtGui.QTextCursor.Document)
		cursor_new = QtGui.QTextCursor(other)
		cursor_new.insertFragment(cursor_old.selection())
		for rule,cursor in self.list_corrections:
			cursor_new = QtGui.QTextCursor(other)
			cursor_new.setPosition(cursor.selectionStart())
			cursor_new.setPosition(cursor.selectionEnd(),QtGui.QTextCursor.KeepAnchor)
			other.list_corrections.append((rule,cursor_new))

		return other

	def setPlainText(self,text):
		for char,char_replace in char_replace_dict.items():
			text = text.replace(char,char_replace)
		QtGui.QTextDocument.setPlainText(self,text)

	def toPlainText(self):
		text = QtGui.QTextDocument.toPlainText(self)
		for char,char_replace in char_replace_dict.items():
			text = text.replace(char_replace,char)
		return text



class GuiMainWindow(QtWidgets.QMainWindow):
	def __init__(self,text="",language=None):
		QtWidgets.QWidget.__init__(self)
		self.filepath = None

		self.inputDocument = GuiDocument(language=language)
		self.inputDocument.setPlainText(text)
		self.inputDocument.SLOT_highlight_detect_exclude()

		self.te_input = QtWidgets.QTextEdit()
		self.te_input.setDocument(self.inputDocument)
		self.te_input.setReadOnly(True)

		self.te_output = QtWidgets.QTextEdit()
		self.te_input.setReadOnly(True)

		self.te_rules = QtWidgets.QTextEdit()
		self.te_rules.setTextColor(QtCore.Qt.darkGreen)
		self.te_rules.setReadOnly(True)

		action_open = QtWidgets.QAction('Open')
		action_detect_exclude = QtWidgets.QAction('Detect Exclude')
		action_highlight = QtWidgets.QAction('Exclude')
		self.action_run = QtWidgets.QAction('Run')
		self.action_save = QtWidgets.QAction('Save')
		self.actions_list = [action_open, action_detect_exclude, action_highlight, self.action_run, self.action_save]

		self.action_run.setIcon(QtGui.QIcon('./icons/run.png'))
		action_open.setIcon(QtGui.QIcon('./icons/open.png'))
		self.action_save.setIcon(QtGui.QIcon('./icons/save.png'))
		action_highlight.setIcon(QtGui.QIcon('./icons/lock_pink.png'))
		languages_list = list(dict_languages.keys())
		languages_list.sort()
		self.combo_language= QtWidgets.QComboBox()
		self.combo_language.addItems(languages_list)
		if language!=None:
			self.combo_language.setCurrentIndex(languages_list.index(language))
		toolbar = self.addToolBar('')
		toolbar.addAction(action_open)
		toolbar.addAction(action_highlight)
		toolbar.addAction(action_highlight)
		toolbar.addWidget(self.combo_language)
		toolbar.addAction(self.action_run)
		toolbar.addAction(self.action_save)

		self.action_run.triggered.connect(self.SLOT_run)
		action_detect_exclude.triggered.connect(self.inputDocument.SLOT_highlight_detect_exclude)
		action_highlight.triggered.connect(self.inverse_exclude)
		action_open.triggered.connect(self.SLOT_open)
		self.action_save.triggered.connect(self.SLOT_save)

		splitter = QtWidgets.QSplitter()
		splitter.addWidget	(self.te_input)
		splitter.addWidget	(self.te_output)

		splitter1 = QtWidgets.QSplitter()
		splitter1.setOrientation(QtCore.Qt.Vertical);
		splitter1.addWidget	(splitter)
		splitter1.addWidget	(self.te_rules)


		self.setCentralWidget(splitter1)
		self.action_run .setEnabled(False)
		self.action_save.setEnabled(False)

	def inverse_exclude(self,cursor=None):
		setcursor = False
		if cursor == None or cursor==False :
			cursor = self.te_input.textCursor()
			setcursor = True
		self.inputDocument.inverse_exclude(cursor=cursor)
		if setcursor:
			cursor.clearSelection()
			self.te_input.setTextCursor(cursor)

	def SLOT_open(self,filepath=None):
		if not filepath:
			dialog= QtWidgets.QFileDialog(self	)
			filepath = dialog.getOpenFileName(self,
					"Select the file to open")[0]
			if not filepath :
				return False
		self.filepath = filepath

		f = codecs.open(filepath, encoding="utf-8",mode='r')
		try:
			self.inputDocument.setPlainText(f.read())
		finally:
			f.close()
		self.inputDocument.SLOT_highlight_detect_exclude()
		self.action_run .setEnabled(True)

	def SLOT_save(self):
		if self.filepath is None:
			raise BaseException("Please specify the filepath by first importing a file")


		outputDocument1 = self.outputDocument.clone()
		outputDocument1.removeShowChanges()
		plaintext = outputDocument1.toPlainText()

		path,ext = os.path.splitext(self.filepath)
		exports_file = os.path.join(path+'_typo'+ext)

		if os.path.exists(exports_file):
			ans = QtWidgets.QMessageBox.question(self,"Overwrite file?","The file %s already exists. Ovewrite?"%exports_file,
				QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
			if ans== QtWidgets.QMessageBox.No:
				return False

		with open(exports_file,'w') as f: f.write(plaintext)






	def SLOT_run(self):
		# we copy the input document

		self.outputDocument = self.inputDocument.clone(language=self.combo_language.currentText())
		self.outputDocument.run()
		self.te_output.setDocument(self.outputDocument)

		self.action_save.setEnabled(True)
		rules = set([rule for rule,cursor in self.outputDocument.list_corrections])
		print("rules",rules)
		rules = [ list_char_nums[rule.number]+' '+rule.title for rule in rules]
		rules.sort()
		self.te_rules.setText('\n'.join(rules ))



if __name__=="__main__":
	app = QtWidgets.QApplication(sys.argv)


	import pathlib
	f = pathlib.Path(__file__).absolute().parent
	f /= "./tests/test_fr.txt"
	# f = d.open()
	# try : inp = f.read()
	# finally: f.close()
	d = GuiMainWindow()
	d.SLOT_open(str(f) )
	# d.SLOT_run()
	d.show()
	sys.exit(app.exec_())
