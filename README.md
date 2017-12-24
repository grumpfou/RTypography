# RTypography

RTypography is a software that correct the typography in text files. It has been
written by Renaud Helbig (Grumpfou). It is published under the license the
license GNU General Public License v3.0. It has been written in Python3.5.2 (and
tested only for this one).


See: https://github.com/grumpfou/RTypography



## Accepted files:

The software has been written to handle markdown files (\*.md, \*.mkd), it
should also work on simple text files (\*.txt).


## Example

Prints the about section:
> python3 RTypography.py --about

Prints the text with in red the section that will not be considered during the
correction:
> python3 RTypography.py --print_exclude foo.txt

Prints the changes on the file foo.txt
> python3 RTypography.py --print_changes foo.txt

Export the text in English, French, etc.
> python3 RTypography.py --language en foo.txt

> python3 RTypography.py --language fr foo.txt

To specify the file to which you want to export:
> python3 RTypography.py --language en --export foo_typo.txt foo.txt
