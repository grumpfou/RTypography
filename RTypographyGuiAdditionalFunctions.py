"""
Part of RTypography Project (the GUI version).
Add some methods to QTextCursor that are used in the Language class.
"""
from PyQt5 import QtGui, QtCore, QtWidgets

word_separators = ["\'","-","’"] # What separetors of words
char_replace_dict = {'\u00A0':'⎵'} # In the gui interface, we replace the non-breackable space by ⎵


def QTextCursor_lastChar(cursor,n=1):
	"""Return the left char at the distance n from the cursor (n=1 means
	the one just on the left)."""
	if cursor.atBlockStart():
		return '\n'
	else :
		cur_tmp=QtGui.QTextCursor(cursor)
		cur_tmp.clearSelection()
		for i in range(n-1):
			cur_tmp.movePosition(QtGui.QTextCursor.Left,
											QtGui.QTextCursor.MoveAnchor)
		if cur_tmp.atBlockStart():
			return '\n'
		cur_tmp.movePosition (QtGui.QTextCursor.Left,
											QtGui.QTextCursor.KeepAnchor)
		return cur_tmp.selectedText ()

def QTextCursor_nextChar(cursor,n=1):
	"""Return the right char at the distance n from the cursor (n=1 means
	the one just on the right)."""
	if cursor.atBlockEnd():
		return '\n'
	else :
		cur_tmp=QtGui.QTextCursor(cursor)
		cur_tmp.clearSelection()
		for i in range(n-1):
			cur_tmp.movePosition(QtGui.QTextCursor.Right,
											QtGui.QTextCursor.MoveAnchor)
		if cur_tmp.atBlockEnd():
			return '\n'
		cur_tmp.movePosition (QtGui.QTextCursor.Right,
										QtGui.QTextCursor.KeepAnchor,n=n)
		return cur_tmp.selectedText ()

def QTextCursor_getWordUnderCursor(cursor):
		"""
		Return the word under the cursor. It uses word_separators  the list of
		the chars that should not be considered as word break (usfull to take
		words like "I'am" or "re-invented").
		"""
		cur_start=QtGui.QTextCursor(cursor)
		cur_start.clearSelection()
		cur_end=QtGui.QTextCursor(cursor)
		cur_end.clearSelection()

		regexp=QtCore.QRegExp("\\b")

		cur_start=cur_start.document().find(regexp,cur_start,
											QtGui.QTextDocument.FindBackward)
		while cur_start.lastChar(  ) in word_separators:
			cur_start.movePosition(QtGui.QTextCursor.Left,
												QtGui.QTextCursor.MoveAnchor)
			cur_start=cur_start.document().find(regexp,cur_start,
											QtGui.QTextDocument.FindBackward)
		cur_end=cur_end.document().find(regexp,cur_end)
		while cur_end.nextChar(  ) in word_separators:
			cur_end.movePosition(QtGui.QTextCursor.Right,
											QtGui.QTextCursor.MoveAnchor,n=2)
			cur_end=cur_end.document().find(regexp,cur_end)

		n=cur_end.position()-cur_start.position()
		cur_final = QtGui.QTextCursor(cur_start)
		cur_final.movePosition(QtGui.QTextCursor.Right,
											QtGui.QTextCursor.KeepAnchor,n=n)
		return cur_final.selectedText(),cur_start

def QTextCursor_delete(cursor): pass

def QTextCursor_copy(cursor):
	return QtGui.QTextCursor(cursor)

QTextCursor_insertText_OLD = QtGui.QTextCursor.insertText
def QTextCursor_insertText(cursor,text,*args,**kargs):
	for char,char_replace in char_replace_dict.items():
		text = text.replace(char,char_replace)
	QTextCursor_insertText_OLD(cursor,text,*args,**kargs)


QTextCursor_selectedText_OLD = QtGui.QTextCursor.selectedText
def QTextCursor_selectedText(cursor,*args,**kargs):
	text = QTextCursor_selectedText_OLD(cursor,*args,**kargs)
	for char,char_replace in char_replace_dict.items():
		text = text.replace(char_replace,char)
	return text


QtGui.QTextCursor.lastChar				= QTextCursor_lastChar
QtGui.QTextCursor.nextChar				= QTextCursor_nextChar
QtGui.QTextCursor.copy					= QTextCursor_copy
QtGui.QTextCursor.delete				= QTextCursor_delete
QtGui.QTextCursor.getWordUnderCursor	= QTextCursor_getWordUnderCursor
QtGui.QTextCursor.insertText			= QTextCursor_insertText
QtGui.QTextCursor.selectedText			= QTextCursor_selectedText
