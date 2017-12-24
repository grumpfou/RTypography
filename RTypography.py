import sys
import os
import argparse
from RTypographyLanguages import *
from RTypographyDocument import *

__version__ = "0.9"
about = """
RTypography is a software that correct the typography in text files. It has been
written by Renaud Helbig (Grumpfou). It is published under the license the
license GNU General Public License v3.0.

Software version %s.

See: https://github.com/grumpfou/RTypography
"""%__version__


class ConsoleInterpret:
	"""
	Will be the console version of the software, it uses the function
	contained in AWCore to open, save, export etc. the files
	"""
	class Error(Exception):
		def __init__(self,message):
			self.message = message
		def __str__(self):
			print(self.message)

	def __init__(self):
		self.argv =	sys.argv

		self.parser = argparse.ArgumentParser()

		self.parser.add_argument("--language",
			help="Select the language for the typography should be in " +\
								str(list(dict_languages.keys())),
			nargs='?')

		self.parser.add_argument("file",
			nargs='?',
			help="File to execute")

		self.parser.add_argument("--export",
			help="The file where to export",
			nargs='?')

		self.parser.add_argument("--print_exclude",
			help="Will show on the document the exclusions",
			action="store_true")

		self.parser.add_argument("--print_changes",
			help="Will show on the document the changes without saving the file",
			action="store_true")

		self.parser.add_argument("--about",
			help="Print the description of the software",
			dest='about',action="store_true")

		self.args = self.parser.parse_args()


	def perfom_command(self):
		if self.args.about:
			print(about)
			return True

		if self.args.file==None:
			raise self.Error("the following arguments are required: file")


		with open(self.args.file,'r') as f: 	text = f.read()

		d = Document(text)

		if self.args.print_exclude:
			d.print_exclude()
			return True

		if self.args.language==None:
			raise self.Error("the following arguments are required: language")
		d.changeLanguage(self.args.language)


		if self.args.print_changes:
			print(d.run(show_changes=True))
			return True

		new_text = d.run()
		if self.args.export:
			exports_file = self.args.export
		else:
			path,ext = os.path.splitext(self.args.file)
			exports_file = os.path.join(path+'_typo'+ext)

		with open(exports_file,'w') as f: f.write(new_text)


if __name__ == '__main__':
	cons = ConsoleInterpret()
	cons.perfom_command()
