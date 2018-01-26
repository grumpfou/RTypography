
from RTypographyLanguages import *
import re
max_iterations = 1000
class Cursor:
	def __init__(self,document,pos=0):
		self.pos = pos
		self.d = document

	def atBlockEnd(self):
		if self.pos==len(self.d.text) or self.d.text[self.pos]=="\n":
			return True
		return False
	def atBlockStart(self):
		if self.pos==0 or self.d.text[self.pos-1]=="\n":
			return True
		return False
	def atEnd(self):
		if self.pos==0: return True
		return False
	def atStart(self):
		if self.pos==len(self.d.text): return True
		return False

	def block(self):
		begin = self.d.text.rfind('\n',0,self.pos)
		if begin==-1: begin==0
		end = self.d.text.rfind('\n',self.pos)
		if end==-1: end==len(self.d.text)
		return self.d.text[begin:end]

	def	deleteChar(self):
		if self.pos<len(self.d.text):
			self.d.text = self.d.text[:self.pos]+self.d.text[self.pos+1:]
			self.d.decay_cursors(self.pos,-1)

	def	deletePreviousChar(self):
		if self.pos>0:
			self.d.text = self.d.text[:self.pos-1]+self.d.text[self.pos:]
			self.d.decay_cursors(self.pos-1,-1)

	def	document(self):
		return self.d

	def insertBlock(self):
		self.d.text = self.d.text[:self.pos]+"\n"+self.d.text[self.pos:]
		self.d.decay_cursors(self.pos-1,1)


	def insertText(self, text):
		self.d.text = self.d.text[:self.pos]+text+self.d.text[self.pos:]
		self.d.decay_cursors(self.pos-1,len(text))

	def position(self):
		return self.pos

	def nextChar(self,n=1):
		assert n>0
		res = self.d.text[self.pos+n-1:self.pos+n]
		if len(res)<n:
			res+='\n'
		return res

	def lastChar(self,n=1):
		assert n>0
		if self.pos<n: # if we ask a char before the begining of the text
			return ''

		res = self.d.text[self.pos-n:self.pos-n+1]
		return res

	def delete(self):
		self.d.cursors.remove(self)
		self.d=None

	def getWordUnderCursor(self):
		begin_cursor = self.d.new_cursor(self.pos)
		while begin_cursor.lastChar().isalnum():
			begin_cursor.pos-=1
		end_cursor = self.d.new_cursor(self.pos)
		while end_cursor.nextChar().isalnum():
			end_cursor.pos+=1
		endpos = end_cursor.pos
		end_cursor.delete()
		return self.d.text[begin_cursor.pos:end_cursor.pos],begin_cursor

	def copy(self):
		return self.d.new_cursor(self.pos)



class Document:
	# tags of the framgent that will be excluded from the analysis
	list_exclude_tags_block = [
		( "<figure>", " <figcaption>"),
		("</figcaption>","</figure>"),
		(r"\begin{equation}",r"\end{equation}")]

	# for tags in the following list, the tag has to be close before the end
	# of the line is order to be taken into account
	list_exclude_tags_line = [
		( "$", "$"),
		("<https://",">"),
		("<http://",">"),
		("(http://",")"),
		("(https://",")")]

	# if is match the following regular expressions, will exclude from the
	# analysis
	list_exclude_re = ["[0-9]{4};[0-9]+:[A-Z0-9]+-[A-Z0-9]+", # to match bibliographies number 2008;26:86-97
			# "https?://[^ \n]*[ \n]",
			"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
			"www\.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
			"\n *- ", # to match the begining of the lists
			"\[\^[0-9]+\]\:",# to notes
			"\]\((?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\)",
			"!\[",
			]



	def __init__(self,text,language=None):
		"""
		- text: the text to analyse
		- language: the language of the Document. Should be in
			["ca","es","en","fr"]
		"""
		self.text = text
		self.changeLanguage(language)

	def lastChar(self,cursor,n=1):
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

	def nextChar(self,cursor,n=1):
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

		self.originalText = text[:]
		if language != None:
			self.changeLanguage(language)

	def resetText(self):
		self.text = self.originalText[:]
		self.cursors = []

	def changeLanguage(self,language):

		if issubclass(type(language),Language) or (language is None):
			self.language = language
		else:
			self.language = dict_languages[language]

		self.cursors = []

	def add_cursor(self,c):
		assert 0<=c.pos<=len(self.text)
		c.d = self
		self.cursors.append(c)

	def new_cursor(self,pos=0):
		c =  Cursor(self,pos)
		self.add_cursor(c)
		return c

	def decay_cursors(self,pos,delta=1):
		for c in self.cursors:
			if c.pos>pos:
				c.pos += delta

	def detect_exclude(self):
		"""
		will search the portion in self?text to be excluded from the analysis
		will compute self.excludes = [(i0,j0),(i1,j1),...] where i0<j0<i1<j1<...
		and that text between i0 and j0, i1 and j1, etc. has to be excluded from
		the anaylsis.

		The tags that determine which fragment has to be excluded are defined in
		list_exclude_tags_blocks and list_exclude_tags_lines.
		"""
		self.excludes = []
		i = 0
		while i<len(self.text):
			i0 = len(self.text)
			to_exclude = None
			for tags in self.list_exclude_tags_block:
				begin = self.text.find(tags[0],i)
				if begin>0 and begin<i0:
					end = self.text.find(tags[1],begin+1)
					if end>0:
						end += len(tags[1])
						i0 = begin
						to_exclude = (begin,end)

			for tags in self.list_exclude_tags_line:
				begin = self.text.find(tags[0],i)
				if begin>0 and begin<i0:
					end_line = self.text.find("\n",begin)
					if end_line==-1 : end_line=len(self.text)

					end = self.text.find(tags[1],begin+1)
					if end>0 and end<end_line:
						end += len(tags[1])
						i0 = begin
						to_exclude = (begin,end)

			for motif in self.list_exclude_re:
				for found in re.finditer(motif, self.text[i:]):
					begin,end = found.span()
					begin += i
					end += i
					if begin<i0:
						i0 = begin
						to_exclude = (begin,end)



			if i0<len(self.text):
				self.excludes.append(to_exclude)

			### cleaning self.excludes
			if len(self.excludes)>0:
				new_excludes = [self.excludes[0]]
				for ex in self.excludes[1:]:
					if ex[0]<=new_excludes[-1][1]:
						new_excludes[-1] = (new_excludes[-1][0],ex[1])
					else:
						new_excludes.append(ex)
				self.excludes = new_excludes

			i = i0+1






	def print_exclude(self):
		self.detect_exclude()
		i0 = 0
		res = ""
		for i,j in self.excludes:
			res += self.text[i0:i]
			res += '\x1b[0;30;41m' +self.text[i:j]+'\x1b[0m'
			i0 = j
		res += self.text[j:]
		print(res)
		return res

	def run(self,i0=0,remove_exclude=True,show_changes=False):
		"""
		i0 :  position where to begin the analysis
		remove_exclude : if True will exclude what is in between the tags
			defined in list_exclude_tags_blocks and list_exclude_tags_lines.
		show_changes: if True, will display the changes in green
		"""
		list_corr = []



		if self.language==None:
			raise BaseException("Please specify the language via the changeLanguage method")
		if remove_exclude:
			i = i0
			res = self.text[:i0]
			lres = len(res)

			# only the excludes after i0
			excludes = [a for a in self.excludes if a[0]>i0]
			for ex  in excludes:
				doc_tmp = Document(self.text[i:ex[0]],language=self.language)
				doc_tmp.run(remove_exclude=False,show_changes=show_changes)
				res += doc_tmp.text
				res += self.text[ex[0]:ex[1]]
				i = ex[1]
				list_corr += [(rule,self.new_cursor(cursor.pos+lres)) for rule,cursor in doc_tmp.list_corr]
				lres = len(res)
			doc_tmp = Document(self.text[i:],language=self.language)
			doc_tmp.run(remove_exclude=False,show_changes=show_changes)
			res += doc_tmp.text

			self.text = res

			if show_changes:

				desc = self.language.getDescriptionRules()
				self.text  += "\n\n"+"\x1b[4;30;42m"+desc+"\x1b[0m"


		else:
			A = self.text[:]
			# A = re.sub('\n *\n','\n\n',A)
			# # First, remove the non needed newlines
			# A = self.text.split("\n\n")

			# motif = " "

			# A = [A[0]]+[a for a in A[1:-1] if len(a.strip())>0]+[A[-1]]
			# # I treat differently A[0] and A[1] is order to keep the newlines
			# # junctions

			# for i,a in enumerate(A):
			# 	B = a.split("\n")
			# 	for j,b in enumerate(B[:-1]):

			# 		if len(b.strip())>0 and b.strip()[0] in '#-': # is it is a title or a list
			# 			B[j+1] = '\n'+B[j+1]
			# 	A[i] = ' '.join(B)

			# self.text="\n\n".join(A)

			c = self.new_cursor(i0)

			while c.pos<len(self.text):
				r= True
				i = 0
				while r and i<max_iterations :
					r = self.language.correctBetweenChars(c)
					if r: list_corr.append(r)
					i+=1
				if i==max_iterations: print("Max iteration at position %i"%c.pos)
				if not c.nextChar().isalnum():
					i = 0
					r= True
					while r and i<max_iterations :
						r = self.language.correctAfterWord(c)
						if r: list_corr.append(r)
						i+=1
					if i==max_iterations: print("Max iteration at position %i"%c.pos,r[0].title)
				c.pos+=1

			if show_changes: # we add the color marks if we have to show the rules
				new_text = ""
				i = 0
				for rule,cursor in list_corr:
					new_text += self.text[i:cursor.pos] +'\x1b[4;30;42mRule%i\x1b[0m'%rule.number
					i=cursor.pos
				new_text += self.text[i:]
				self.text = new_text

		self.list_corr = list_corr
		return self.text




if __name__=="__main__":
	import pathlib
	d = pathlib.Path(__file__).absolute().parent
	d /= "./.tests/init.txt"
	f = d.open()
	try : inp = f.read()
	finally: f.close()
	d = Document(inp,"fr")
	d.print_exclude()
	d.run()
	print("d.text",d.text)
