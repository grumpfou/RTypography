QTextCursor::NoMove:0:
QTextCursor::Start:1:
QTextCursor::StartOfLine:3:
QTextCursor::StartOfBlock:4:
QTextCursor::StartOfWord:5:
QTextCursor::PreviousBlock:6:
QTextCursor::PreviousCharacter:7
QTextCursor::PreviousWord:8
# QTextCursor::Up:2:Move up one line.
QTextCursor::Left:9:
QTextCursor::WordLeft:10:
QTextCursor::End:11:
QTextCursor::EndOfLine:13:
QTextCursor::EndOfWord:14:
QTextCursor::EndOfBlock:15:
QTextCursor::NextBlock:16:
QTextCursor::NextCharacter:17:
QTextCursor::NextWord:18:
QTextCursor::Down:12:
QTextCursor::Right:19:
QTextCursor::WordRight:20:
# QTextCursor::NextCell	21	Move to the beginning of the next table cell inside the current table. If the current cell is the last cell in the row, the cursor will move to the first cell in the next row.
# QTextCursor::PreviousCell	22	Move to the beginning of the previous table cell inside the current table. If the current cell is the first cell in the row, the cursor will move to the last cell in the previous row.
# QTextCursor::NextRow	23	Move to the first new cell of the next row in the current table.
# QTextCursor::PreviousRow	24



class Cursor:
    def __init__(self,document,pos=0):
        self.pos = pos
        self.sel = []
        self._document = document
        self.text = self._document.text

    def atBlockEnd(self):
        if self.pos==len(self.text) or self.text[self.pos]=="\n"
            return True
        return False
    def atBlockStart(self):
        if self.pos==0 or self.text[self.pos-1]=="\n"
            return True
        return False
    def atEnd(self):
        if self.pos==0: return True
        return False
    def atStart(self):
        if self.pos==len(self.text): return True
        return False
    def block(self):
        begin = self.text.rfind('\n',0,self.pos)
        if begin==-1: begin==0
        end = self.text.rfind('\n',self.pos)
        if end==-1: end==len(self.text)
    # int 	blockNumber(self):
    def	clearSelection(self):
        self.sel = []
    # def columnNumber(self):
    def	deleteChar(self):
        self.text = self.text[:self.pos]+self.text[self.pos+1:]
    def	deletePreviousChar(self):
        self.text = self.text[:self.pos-1]+self.text[self.pos:]
    def	document(self):
        return self._document
    def hasSelection(self):
        if len(self.sel)!=0: return True
        return False
    def insertBlock(self):
        self.text = self.text[:self.pos]+"\n"+self.text[self.pos+1:]
        self.pos += 1
    def insertFragment(self, fragment):
        self.insertText(fragment)
    def insertText(self, text):
        self.text = self.text[:self.pos]+text+self.text[self.pos+1:]
        self.pos += len(text)
    def joinPreviousEditBlock(self):
        old_pos = self.pos
        pos = self.text.rfind("\n",0,self.pos)
        if pos>=0:
            self.pos = pos
            self.deleteChar()
            self.pos = old_pos-1
    def movePosition(self,operation, mode = 0, n = 1):
        if operation == 0: pass
        if o
int 	position(self):
int 	positionInBlock(self):
void 	removeSelectedText(self):
void 	select(SelectionType selection)
void 	selectedTableCells(int * firstRow, int * numRows, int * firstColumn, int * numColumns)
QString 	selectedText(self):
QTextDocumentFragment 	selection(self):
int 	selectionEnd(self):
int 	selectionStart(self):
void 	setBlockCharFormat( QTextCharFormat & format)
void 	setBlockFormat( QTextBlockFormat & format)
void 	setCharFormat( QTextCharFormat & format)
void 	setKeepPositionOnInsert(bool
b)
void 	setPosition(int pos, MoveMode m = MoveAnchor)
void 	setVerticalMovementX(int x)
void 	setVisualNavigation(bool b)
int 	verticalMovementX(self):
bool 	visualNavigation(self):
bool 	operator!=( QTextCursor & other)
bool 	operator<( QTextCursor & other)
bool 	operator<=( QTextCursor & other)
QTextCursor & 	operator=( QTextCursor & cursor)
bool 	operator==( QTextCursor & other)
bool 	operator>( QTextCursor & other)
bool 	operator>=( QTextCursor & other)
