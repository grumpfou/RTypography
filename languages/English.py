

class TLRuleEnglish0001 (TLRuleAbstract):
	title="No space before a space or a break of line"
	description=	\
		"It deletes the space before another space of a break of line\n \n\
		example :	'A  thing' -> 'A thing' \n\
					'end of block. \\n' -> 'end of block.\\n'"
	profile = 0
	in_languges=[u'English']
	def correct(self,last_char,next_char,cursor):
		if last_char==u' ' and next_char in [u' ',u'\n']:
			cursor.deletePreviousChar()
			return True
		return False

class TLRuleEnglish0002 (TLRuleAbstract):
	title="No space or unbreakable space after an unbreakable space"
	description=	\
		"It delete the space or an unbreakable space (\\US) after an "+\
		"unbreakable space. \n"+\
		"example :	'year[US] 2001' -> 'year[US]2001' \n"+\
		"			'year[US][US]2001' -> 'year[US]2001'"
	profile = 0
	in_languges=[u'English']
	def correct(self,last_char,next_char,cursor):
		if last_char==u'\u00A0' and next_char in [u'\u00A0',' ']:
			cursor.deleteChar()
		return False

class TLRuleEnglish0003 (TLRuleAbstract):
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
class TLRuleEnglish0003old (TLRuleAbstract):
	title="No space or break of line after a break of line. "

	description=	\
		"It deletes the space or break of line after a break of line\n"+\
		"example :	'end of block.\\n ' -> 'end of block.\\n'\n"+\
		"				'end of block.\\n\\n' -> 'end of block.\\n'"
	profile = 0
	in_languges=[u'English']
	def correct(self,last_char,next_char,cursor):
		if last_char==u'\n' and next_char in [u' ',u'\n']:
			cursor.deleteChar()
			return True
		return False

class TLRuleEnglish0004 (TLRuleAbstract):
	title="No space or unbreakable space before ',', ';', ':', '!', '?'"
	description=	\
		"Delete a space or an unbreakable space (US) before some "+\
		"ponctuation: ';', ':', '!', '?' or a closing guillemet (CG).\n"+\
		"example :	'Hello !' 		-> 'Hello!'\n"+\
		"			'Hello[US]!'	-> 'Hello!'\n"+\
		"			'Hello ;'	 	-> 'Hello;'\n"+\
		"			'Hello[US];' 	-> 'Hello;'\n"+\
		"			'Hello :'		-> 'Hello:'\n"+\
		"			'Hello ?'		-> 'Hello?'\n"+\
		"			'Hello. [CG]'	-> 'Hello.[CG]'"
	profile = 0
	in_languges=[u'English']
	def correct(self,last_char,next_char,cursor):
		if next_char in [u',',u';',u':',u'!',u'?',u'\201d']:
			if last_char==' ' or last_char==u'\u00A0':
				cursor.deletePreviousChar()
				return True
		return False


class TLRuleEnglish0005 (TLRuleAbstract):
	title="Replace the char [\"] by a opening or closing guillemet"
	description=	\
		"When pressing the char [\"], it replace by : an opening guillemet "+\
		"(OG) if it is preceded by a space, an unbreakable space (US) or a "+\
		"newline ; a closing guillemet (CG) otherwise. It also insert an "+\
		"unbreakable space after the opening guillemet and before the "+\
		"closing guillemet.\n"+\
		"example :	'\"Hello' -> '[OG]Hello'\n"+\
		"			'Bye.\"' -> 'Bye.[CG]'"
	in_languges=[u'English']
	profile = 1
	def correct(self,last_char,next_char,cursor):
		if next_char==u'"':
			if last_char in [u' ',u'\n',u'\u00A0']:
				cursor.deleteChar()
				cursor.insertText(u'\u201c')
			else :
				cursor.deleteChar()
				cursor.insertText(u'\u201d')
			return True

		return False

class TLRuleEnglish0006 (TLRuleAbstract):
	title="No space or unbreakable space after an opening guillemet."
	description=	\
		"It deletes any space or unbreakable space (US) after an opening "+\
		"guillemet (OG).\n"+\
		"example :	'[OG] Hello' 	-> '[OG]Hello'\n"+\
		"			'[OG][US]Hello' -> '[OG]Hello'"
	in_languges=[u'English']
	profile = 1
	def correct(self,last_char,next_char,cursor):
		if last_char==u'\u201c':
			if next_char==' ' or next_char==u'\u00AB':
				cursor.deleteChar()
				return True
		return False

class TLRuleEnglish0007 (TLRuleAbstract):
	title="No space or unbreakable space before an closing guillemet."
	description=	\
		"It deletes any space or unbreakable space (US) before an closing "+\
		"guillemet (CG).\n"+\
		"example :	'Hello [CG]' 	-> 'Hello[CG]'\n"+\
		"			'Hello[US][CG]' -> 'Hello[CG]'"
	profile = 0
	in_languges=[u'English']
	def correct(self,last_char,next_char,cursor):
		if next_char==u'\u201d':
			if last_char==' ' or last_char==u'\u00AB':
				cursor.deletePreviousChar()
				return True
		return False



class TLRuleEnglish0008 (TLRuleAbstract):
	title="A space or a newline after ';', ':', '!' or '?' except if it a "+\
		"closing guillemet (CG) or '!', '?'"
	description=	\
		"Check if there is a newline or a space after ';', ':', '!' or '? "+\
		"and if it is not the case, it inserts one (replacing the "+\
		"unbreakable space is necessary).\n"+\
		"example :	'I agree;and you' -> 'I agree; and you'\n"+\
		"			'I agree:it is coherent' -> 'I agree: it is coherent'\n"+\
		"			'I agree!It is coherent' -> 'I agree! It is coherent'\n"+\
		"			'Do you agree?It is coherent' -> 'Do you agree? It is "+\
																"coherent'\n"+\
		"			'I agree![CG]' -> same\n"+\
		"			'I agree!!' -> same\n"+\
		"			'I agree?!' -> same\n"+\
		"			'I said to him:\n' -> same"
	profile = 0
	in_languges=[u'English']
	def correct(self,last_char,next_char,cursor):
		if last_char in [u';',u':',u'!',u'?'] and \
											(next_char not in [u'\n',u' ']):
			if next_char== u'\u201d' or next_char== u'?' or next_char== u'!':
				return False
			if next_char== u'\u00A0':
				cursor.deleteChar()
			cursor.insertText(u' ')
			return True

		return False

class TLRuleEnglish0009 (TLRuleAbstract):
	title="A space or a newline after '.' or ',' except if it is a figure "+\
		"or a closing guillemet (CG) or another dot"
	description=	\
		"Check if there is a newline or a space after '.' or ',' and if it "+\
		"is not the case, it inserts one (replacing the unbreakable space "+\
		"is necessary. This rule does not apply if the next character is a "+\
		"figure.\n"+\
		"example :	'I agree.And you' -> 'I agree. And you'\n"+\
		"			'I agree,it is coherent' -> 'I agree, it is coherent'\n"+\
		"			'I agree.[CG]' -> same\n"+\
		"			'The speed was 33.7 mph' -> same"+\
		"			'Let's see..' -> same # the goal is to make an ellips"
	profile = 0
	in_languges=[u'English']
	def correct(self,last_char,next_char,cursor):
		ch_list = [u'\n',u' ',u'\u201d',u'.']+[str(i) for i in range(10)]
		if last_char in [u'.',u','] and (next_char not in ch_list):
			if next_char== u'\u00A0':
				cursor.deleteChar()
			cursor.insertText(u' ')
			return True

		return False

class TLRuleEnglish0010 (TLRuleAbstract):
	title="Replace the typewriter apostrophe by a curved apostrophe."
	description=	\
		"Replace a the char ['] by a curved apostrophe (CA).\n\
		example :	'It's me' -> 'It[CA]s me'"
	in_languges=[u'English']
	profile = 1
	def correct(self,last_char,next_char,cursor):
		if next_char==u"'":
			cursor.deleteChar()
			cursor.insertText(u'\u2019')
		return False

class TLRuleEnglish0011 (TLRuleAbstract):
	title="Replace 3 consecutive points by an ellipsis."
	description=	\
		"Replace 3 consecutive points into an ellipsis (E):\n\
		example :	'\"So...' -> 'So[E]'"
	profile = 1
	in_languges=[u'English']
	def correct(self,last_char,next_char,cursor):
		if last_char==u'.' and next_char==u'.':

			if self.language.lastChar(cursor,n=2)==u'.':
				cursor.deleteChar()
				cursor.deletePreviousChar()
				cursor.deletePreviousChar()
				cursor.insertText(u'\u2026')
				return True
		return False



language = Language(name="English",code="en",
	afterCharRules=[TLRuleEnglish0001,
					TLRuleEnglish0002,
					TLRuleEnglish0003,
					TLRuleEnglish0004,
					TLRuleEnglish0005,
					TLRuleEnglish0006,
					TLRuleEnglish0007,
					TLRuleEnglish0008,
					TLRuleEnglish0009,
					TLRuleEnglish0010,
					TLRuleEnglish0011]
					)
