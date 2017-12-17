
class TLRuleFrench0001 (TLRuleAbstract):
	title="No space before a space or a break of line"
	description=	\
		"It deletes the space before another space of a break of line\n"+\
		"example :	'A  thing' -> 'A thing' \n"+\
		"			'end of block. \\n' -> 'end of block.\\n'"
	profile = 0
	in_languges=[u'French']

	def correct(self,last_char,next_char,cursor):
		if last_char==u' ' and next_char in [u' ',u'\n']:
			cursor.deletePreviousChar()
			return True
		return False

class TLRuleFrench0002 (TLRuleAbstract):
	title="No space or unbreakable space after an unbreakable space"
	description=	\
		"It delete the space or an unbreakable space (\\US) after an "+\
		"unbreakable space. \n"+\
		"example :	'year[US] 2001' -> 'year[US]2001' \n"+\
		"			'year[US][US]2001' -> 'year[US]2001'"
	profile = 0
	in_languges=[u'French']
	def correct(self,last_char,next_char,cursor):
		if last_char==u'\u00A0' and next_char in [u'\u00A0',' ']:
			cursor.deleteChar()
		return False

class TLRuleFrench0003 (TLRuleAbstract):
	title="No space or unbreakable space  after a break of line."

	description=	\
		"It deletes the space after a break of line\n"+\
		"example :	'end of block.\\n ' -> 'end of block.\\n'\n"+\
		"example :	'end of block.\\n[US]' -> 'end of block.\\n'\n"
	in_languges=[u'French']
	profile = 0
	def correct(self,last_char,next_char,cursor):
		if last_char==u'\n' and next_char in [u' ',u'\u00A0']:
			cursor.deleteChar()
			return True
		return False
class TLRuleFrench0003_old (TLRuleAbstract):
	title="No space, unbreakable space or break of line after a break of line."

	description=	\
		"It deletes the space or break of line after a break of line\n"+\
		"example :	'end of block.\\n ' -> 'end of block.\\n'\n"+\
		"example :	'end of block.\\n[US]' -> 'end of block.\\n'\n"+\
		"			'end of block.\\n\\n' -> 'end of block.\\n'"
	in_languges=[u'French']
	profile = 0
	def correct(self,last_char,next_char,cursor):
		if last_char==u'\n' and next_char in [u' ',u'\n',u'\u00A0']:
			cursor.deleteChar()
			return True
		return False
class TLRuleFrench0004 (TLRuleAbstract):
	title="An unbreakable space before ';', ':', '!', '?', and closing "+\
		"guillemets."
	description=	\
		"Put an unbreakable space (US) before some ponctuation : ';', ':', "+\
		"'!', '?' and the french closing guillemets.\n"+\
		"example :	'Bonjour! ' -> 'Bonjour[US]!'\n"+\
		"			'Bonjour; ' -> 'Bonjour[US];'\n"+\
		"			'Bonjour: ' -> 'Bonjour[US]:'\n"+\
		"			'Bonjour? ' -> 'Bonjour[US]?'\n"+\
		"			'Bonjour ! ' -> 'Bonjour[US]!'\n"+\
		"			'Bonjour ? ' -> 'Bonjour[US]?'"
	profile = 1
	in_languges=[u'French']
	def correct(self,last_char,next_char,cursor):
		if next_char in [u';',u':',u'!',u'?',u'\u00BB']:
			if last_char==' ':
				cursor.deletePreviousChar()
				cursor.insertText(u'\u00A0')
				return True
			if last_char!=u'\u00A0':
				cursor.insertText(u'\u00A0')
				return True
		return False

class TLRuleFrench0005 (TLRuleAbstract):
	title="An unbreakable space after an opening guillemet"
	description=	\
		"It puts an unbreakable space (US) after an opening gullemet (OG) "+\
		"(or replace the simple space that was there).\n"+\
		"example :	'[OG] Bonjour' -> '[OG][US]Bonjour'\n"+\
		"			'[OG]Bonjour' -> '[OG][US]Bonjour'"
	profile = 1
	in_languges=[u'French']
	def correct(self,last_char,next_char,cursor):
		if last_char==u'\u00AB':
			if next_char==' ':
				cursor.deleteChar()
				cursor.insertText(u'\u00A0')
				return True
			if next_char!=u'\u00A0':
				cursor.insertText(u'\u00A0')
				return True
		return False

class TLRuleFrench0006 (TLRuleAbstract):
	title="No unbreakable space if it is not before a ponctuation or after "+\
			"an oppening guillemet or after a dialog dash, or a number."
	description=	\
		"Usually we prevent using an unbreakable space (US) if it is not "+\
		"before a ponctuation like ';', ':', '!', '?', or a closing "+\
		"guillemet or a dialog dash or a number. It can also be used after "+\
		"an opening guillemet. It replaces the unbreakable space by a "+\
		"simple space.\n"+\
		"example :	'Je[US]suis' -> 'Je suis'\n"+\
		"			'[OG][US]\\Bonjour' -> same\n"+\
		"			'Bonjour[US]!' -> same\n"+\
		"			'[DD][US]Salut -> same\n"+\
		"			'200[US]000 -> same"
	profile = 1
	in_languges=[u'French']
	def correct(self,last_char,next_char,cursor):
		if last_char==u'\u00A0' and (next_char not in \
											[u';',u':',u'!',u'?',u'\u00BB']+\
											[str(i) for i in range(10)]):
			last_last_char=self.language.lastChar(cursor,n=2)
			# we cheak it caused by an oppening "guillemet":
			if last_last_char not in [u'\u00AB' , u'\u2014']:
				cursor.deletePreviousChar()
				cursor.insertText(u' ')
				return True
		return False

class TLRuleFrench0007 (TLRuleAbstract):
	title="No space before a point or a comma."
	description=	\
		"It deletes a space or an unbreakable space (US) before a comma.\n"+\
		"example :	'I agree .' -> 'I agree.'\n"+\
		"			'I agree[US].' -> 'I agree.'\n"+\
		"			'Charles , you and me.' -> 'Charles, you and me.'"
	profile = 0
	in_languges=[u'French']
	def correct(self,last_char,next_char,cursor):
		if last_char in [u' ', u'\u00A0'] and next_char in [u'.',u',']:
			cursor.deletePreviousChar()
			return True
		return False

class TLRuleFrench0008 (TLRuleAbstract):
	title="A space or a newline after ';' or ':'."
	description=	\
		"Check if there is a newline or a space after ';' or ':' and if it "+\
		"is not the case, it inserts one (replacing the unbreakable space "+\
		"is necessary.\n"+\
		"example :	'I agree;and you' -> 'I agree; and you'\n"+\
		"			'I agree:it is coherent' -> 'I agree: it is coherent'\n"+\
		"			'I said to him:\n' -> same"
	profile = 0
	in_languges=[u'French']
	def correct(self,last_char,next_char,cursor):
		if last_char in [u';',u':'] and (next_char not in [u'\n',u' ']):
			if next_char== u'\u00A0':
				cursor.deleteChar()
			cursor.insertText(u' ')
			return True

		return False

class TLRuleFrench0009 (TLRuleAbstract):
	title="Replace the typewriter apostrophe by a curved apostrophe."
	description=	\
		"Replace a the char ['] by a curved apostrophe (CA).\n\
		example :	'It's me' -> 'It[CA]s me'"
	profile = 1
	in_languges=[u'French']
	def correct(self,last_char,next_char,cursor):
		if next_char==u"'":
			cursor.deleteChar()
			cursor.insertText(u'\u2019')
		return False

class TLRuleFrench0010 (TLRuleAbstract):
	title="Replace the char [\"] by a opening or closing guillemet"
	description=	\
		"When pressing the char [\"], it replace by : an opening guillemet "+\
		"(OG) if it is preceded by a space, an unbreakable space (US) or a "+\
		"newline ; a closing guillemet (CG) otherwise. It also insert an "+\
		"unbreakable space after the opening guillemet and before the "+\
		"closing guillemet.\n"+\
		"example :	'\"Bonjour' -> '[OG][US]Bonjour'"+\
		"			'Salut.\"' -> 'Salut.[US][CG]'"
	profile = 1
	in_languges=[u'French']
	def correct(self,last_char,next_char,cursor):
		if next_char==u'"':
			if last_char in [u' ',u'\n',u'\u00A0']:
				cursor.deleteChar()
				cursor.insertText(u'\u00AB\u00A0')
			else :
				cursor.deleteChar()
				cursor.insertText(u'\u00A0\u00BB')
			return True

		return False

class TLRuleFrench0011 (TLRuleAbstract):
	title='''Replace '"' by an openning/closing guillement'''
	description='''Replace '"' by an openning/closing guillement'''
	in_languges=[u'French']
	profile = 1
	def correct(self,last_char,next_char,cursor):

		if last_char==u'"':
			if next_char==u' ':
				cursor.deletePreviousChar()
				cursor.insertText(u'\u00A0\u00BB')
			else :
				cursor.deletePreviousChar()
				cursor.insertText(u'\u00AB\u00A0')
			return True
		return False

class TLRuleFrench0012 (TLRuleAbstract):
	title="Replace 3 consecutive points by an ellipsis."
	description=	\
		"Replace 3 consecutive points into an ellipsis (E):\n"+\
		"example :	'\"So...' -> 'So[E]'"
	profile = 1
	in_languges=[u'French']
	def correct(self,last_char,next_char,cursor):
		if last_char==u'.' and next_char==u'.':

			if self.language.lastChar(cursor,n=2)==u'.':
				cursor.deleteChar()
				cursor.deletePreviousChar()
				cursor.deletePreviousChar()
				cursor.insertText(u'\u2026')
				return True
		return False

class TLRuleFrench0013 (TLRuleAbstract):
	title="An unbreakable space before after a diolog dash."
	description=	\
		"It puts an unbreakable space (US) after a diolog dash (DD) (or "+\
		"replace the simple space that was there).\n\
		example :	'[DD] Bonjour' -> '[DD][US]Bonjour'\n\
					'[DD]Bonjour' -> '[DD][US]Bonjour"
	profile = 1

	in_languges=[u'French']
	def correct(self,last_char,next_char,cursor):
		if last_char==u'\u2014' and next_char!=u'\u00A0':
			if next_char==' ':
				cursor.deleteChar()
				cursor.insertText(u'\u00A0')
				return True
			if next_char!=u'\u00A0':
				cursor.insertText(u'\u00A0')
				return True
		return False

class TLWordCorrectionRuleFrench0001 (TLRuleAbstract):
	title=u"Replace the 'oe' by 'u'\u0153''"
	description=	\
		"In French, most of the word with 'oe' have an elision"
	profile = 1
	in_languges=[u'French']

	def correct(self,last_word,cursor):
		if last_word.find(u'oe')!=-1:
			if last_word not in {'moelle'}:
				return last_word.replace(u'oe',u'\u0153')
		return False

language = Language(
	name="French",
	code="fr",
	afterCharRules=[	TLRuleFrench0001,
						TLRuleFrench0002,
						TLRuleFrench0003,
						TLRuleFrench0004,
						TLRuleFrench0005,
						TLRuleFrench0006,
						TLRuleFrench0007,
						TLRuleFrench0008,
						TLRuleFrench0009,
						TLRuleFrench0010,
						TLRuleFrench0011,
						TLRuleFrench0012,
						TLRuleFrench0013],
	afterWordRules = [ TLWordCorrectionRuleFrench0001 ]

					)
