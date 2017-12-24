"""
Part of the  project AthenaWriter. Written by Renaud Dessalles
Contains the class that deal with the typography.
The LanguageAbstract class is the model class of all the language class
below. It must not be used directly, only subclass should be used.

There is two ways of correcting the typography of the user :
- by cheaking during the editing : every time the cursor moves (a char is
inserted or a the user moves the cursor), the software is cheking if the chars
around the place leaved by the cursor are correct, and correct them if
necessary. The method used to do so is correct_between_chars.
- after a word is written : to correct the previous word etc. The method used
to do so is wordCorrection.
The class can also contain some pluggin usefull in the language :
- the shortcuts_insert dict allow to insert specific text after a shortcut
- the shortcuts_correction_plugins dict allow to do a more complex modification
of the text.

When creating a new Language class, it must contain :
- the encoding
- the name of the language (in the language)
- possibly the shortcuts_insert (a dictionary where the key is a tuple
containing the sequence of the shortcut and the value is the string to insert.
_ a __init__ method with :
	a dictionary shortcuts_correction_plugins dict :
		key : shortcuts_correction_plugins
		value : the name of the pluggin method
	self.rules : the list of the rules (contained in the file
		WolfWriterLanguagesRules.py) that will be check by the
		correct_between_chars method. Note that the order of the list is the
		same in which the rule will be checked.
- a possibly reimplementation of the wordCorrection method
- the possibly method mentioned in the values of the
	shortcuts_correction_plugins
"""

class TLRuleAbstract:
	number = -1
	title="None"
	description="None"
	profile = 0
	in_languges=[]
	def __init__(self,language):
		self.language=language
		pass

	def __str__(self):
		return self.title+'\n'+self.description

	def correct(self,last_char,next_char,cursor):
		raise NotImplementedError
		return False



class Language:
	def __init__(self,name,code,afterCharRules=[],afterWordRules=[]):
		"""
		name: name of the Language (e.g.: "English" or "French")
		code: code of the language (e.g.: "en" for English, "fr" for French)
		afterCharRules : list of TLRuleAbstract subclass that need to be check
			after each char.
		afterWordRules : list of TLRuleAbstract subclass that need to be check
			after each words.
		"""
		for rule in afterCharRules : assert issubclass(rule,TLRuleAbstract)
		for rule in afterWordRules : assert issubclass(rule,TLRuleAbstract)
		self.afterCharRules = [rule(language=self) for rule in afterCharRules]
		self.afterWordRules = [rule(language=self) for rule in afterWordRules]
		self.name = name
		self.code = code
	def correctBetweenChars(self,cursor):
		"""Function that will be called every time the cursor moves. It
		check the respect of all the typography rules of the two char of
		both sides of the position that the cursor has just left."""

		last_char=self.lastChar(cursor)
		next_char=self.nextChar(cursor)

		for rule in self.afterCharRules:
			res=rule.correct(last_char,next_char,cursor)
			if res :
				return (rule,cursor.position())
		return False

	def correctAfterWord(self,cursor):
		word,cursor_begin = cursor.getWordUnderCursor()
		for rule in self.afterWordRules:
			new_word=rule.correct(word,cursor)
			if new_word:
				for i in range(len(word)):
					cursor_begin.deleteChar()
				cursor_begin.delete()
				cursor.insertText(new_word)
			return new_word
		return False


	def getWordUnderCursor(self,cursor):
		self.cursor.getWordUnderCursor()

	def lastChar(self,cursor,n=1):
		"""Return the left char at the distance n from the cursor (n=1 means
		the one just on the left)."""
		return cursor.lastChar(n=n)

	def nextChar(self,cursor,n=1):
		"""Return the right char at the distance n from the cursor (n=1 means
		the one just on the right)."""
		return cursor.nextChar(n=n)


	def getDescriptionRules(self):
		"""Returns a summary of all the rules of the language"""
		rules = self.afterCharRules + self.afterWordRules

		res = "\n".join(["Rule %i: %s"%(r.number,r.title) for r in rules])
		# 	+= "\n".join(["\x1b[4;30;42Rule %i: %s\x1b[0m"%(r.number,r.title) for r in rules])
		return res


dict_languages = dict()
import pathlib
f = pathlib.Path(__file__).absolute().parent
f /= "./languages/"
for lang_file in f.glob('*.py'):
	with lang_file.open() as ff:
		exec(ff.read())
		dict_languages[language.code] = language
