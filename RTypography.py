import sys
import os
import argparse
from RTypographyLanguages import *
from RTypographyDocument import *

__version__ = "1.0alpha"
about = """
RTypography is a software that correct the typography in text files. It has been
written by Renaud Helbig (Grumpfou). It is published under the license the
license GNU General Public License v3.0.

Software version %s.

See: https://github.com/grumpfou/RTypography
"""%__version__

def testPyQt():
	try:
		import PyQt5
	except:
		return False
	return True


class ConsoleInterpret:
	"""
	Will be the console version of the software, it uses the function
	contained in AWCore to open, save, export etc. the files
	"""
	class Error(Exception):pass

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

		self.parser.add_argument("--gui",
			help="Graphical interface (need PyQt5)",
			dest='gui',action="store_true")

		self.parser.add_argument("--print_excludes",
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
		if self.args.gui:
			if not testPyQt():
				raise self.Error("You should first install the library PyQt5.")
			import RTypographyGuiDocument
			from PyQt5 import  QtWidgets
			app = QtWidgets.QApplication(sys.argv)
			d = RTypographyGuiDocument.GuiMainWindow(language=self.args.language)
			if not self.args.file is None:
				d.SLOT_open(self.args.file)
			d.show()
			sys.exit(app.exec_())
			return True



		if self.args.file==None:
			raise self.Error("the following arguments are required: file")


		with open(self.args.file,'r') as f: 	text = f.read()

		d = Document(text)

		if self.args.print_excludes:
			d.print_excludes()
			return True

		if self.args.language==None:
			raise self.Error("the following arguments are required: language")
		d.changeLanguage(self.args.language)


		if self.args.print_changes:
			d.detect_exclude()
			print(d.run(show_changes=True))
			return True

		d.detect_exclude()
		new_text = d.run()
		if self.args.export:
			exports_file = self.args.export
		else:
			path,ext = os.path.splitext(self.args.file)
			exports_file = path+'_typo'+ext

		if os.path.exists(exports_file):
			ans = input('The file %s already exists. Ovewrite? (yes,no) '%exports_file).lower()
			while ans not in {"yes","no"}:
				ans = input('Please answer by `yes` or `no`. ').lower()
			if ans=='no': return False

		with open(exports_file,'w') as f: f.write(new_text)


if __name__ == '__main__':
	cons = ConsoleInterpret()
	cons.perfom_command()
