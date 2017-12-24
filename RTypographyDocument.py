
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
		res = self.d.text[self.pos:self.pos+n]
		if len(res)<n:
			res+='\n'
		return res

	def lastChar(self,n=1):
		assert n>0
		nn = min(self.pos,n)
		res = self.d.text[self.pos-nn:self.pos]
		if len(res)<n:
			res='\n'+res
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



class Document:
	# tags of the framgent that will be excluded from the analysis
	list_exclude_tags_block = [( "<figure>", " <figcaption>"),
		("</figcaption>","</figure>"), (r"\begin{equation}",r"\end{equation}")]

	# for tags in the following list, the tag has to be close before the end
	# of the line is order to be taken into account
	list_exclude_tags_line = [( "$", "$"),("<https://",">"),("<http://",">"),
		("(http://",")"),("(https://",")")]

	# if is match the following regular expressions, will exclude from the
	# analysis
	list_exclude_re = ["[0-9]{4};[0-9]+:[A-Z0-9]+-[A-Z0-9]+", # to match bibliographies number 2008;26:86-97
			"https?://[^ \n]*"
			]



	def __init__(self,text,language=None):
		"""
		- text: the text to analyse
		- language: the language of the Document. Should be in
			["ca","es","en","fr"]
		"""
		self.text = text
		if language != None:
			self.changeLanguage(language)

	def changeLanguage(self,language):

		if issubclass(type(language),Language):
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
			self.detect_exclude()
			i = i0
			res = self.text[:i0]

			# only the excludes after i0
			excludes = [a for a in self.excludes if a[0]>i0]

			for ex  in excludes:
				doc_tmp = Document(self.text[i:ex[0]],language=self.language)
				doc_tmp.run(remove_exclude=False,show_changes=show_changes)
				res += doc_tmp.text
				res += self.text[ex[0]:ex[1]]
				i = ex[1]

			doc_tmp = Document(self.text[i:],language=self.language)
			doc_tmp.run(remove_exclude=False,show_changes=show_changes)
			res += doc_tmp.text
			self.text = res

			if show_changes:

				desc = self.language.getDescriptionRules()
				desc = ["\x1b[4;30;42m"+d+"\x1b[0m" for d in desc.split("\n")]
				self.text  += "\n\n"+"\n".join(desc)


		else:
			# First, remove the non needed newlines
			A = self.text.split("\n\n")
			motif = " "
			A = [a.replace("\n"," ") for a in A]
			A = [A[0]]+[a for a in A[1:-1] if len(a.strip())>0]+[A[-1]]
			# I treat differently A[0] and A[1] is order to keep the newlines
			# junctions
			self.text="\n\n".join(A)

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
				for rule,pos in list_corr:
					new_text += self.text[i:pos] +'\x1b[4;30;42mRule%i\x1b[0m'%rule.number
					i=pos
				new_text += self.text[i:]
				self.text = new_text


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
