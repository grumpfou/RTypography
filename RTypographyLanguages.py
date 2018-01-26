
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
				return (rule,cursor.copy())
		return False

	def correctAfterWord(self,cursor):
		word,cursor_begin = cursor.getWordUnderCursor()
		if word.strip(): #if it is not empty
			for rule in self.afterWordRules:

				new_word=rule.correct(word,cursor)
				if new_word:
					for i in range(len(word)):
						cursor_begin.deleteChar()
					cursor_begin.delete()
					cursor.insertText(new_word)
					return rule, cursor.copy()
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
