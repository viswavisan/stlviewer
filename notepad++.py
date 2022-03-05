from PyQt5 import *
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import*
from PyQt5.QtGui import *
import sys

def button(text='',function=None,icon=None,h=None,w=None,flat=False,tip=None,curser=None):
    pushbutton = QPushButton(text)
    pushbutton.setFlat(flat)
    if w!=None: pushbutton.setFixedWidth(w)
    if h!=None: pushbutton.setFixedHeight(h)
    if function!=None:pushbutton.clicked.connect(function)
    if icon!=None:pushbutton.setStyleSheet("border-image : url("+icon+")")
    if curser=='hand':pushbutton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
    if tip!=None:
        pushbutton.setToolTip('<div style="background-color:white">'+tip+'</div>')
    return pushbutton

keywords=['False', 'None', 'True', 'and', 'as', 'assert', 'async','await', 'break', 'class', 'continue', 'def', 'del', 'elif',
'else', 'except', 'finally', 'for', 'from', 'global','if', 'import', 'in', 'is', 'lambda','nonlocal', 'not', 'or', 'pass', 'raise',
'return', 'try', 'while', 'with', 'yield']
class QLineNumberArea(QWidget):
    def __init__(self, editor):super().__init__(editor);self.codeEditor = editor
    def sizeHint(self):return QSize(self.editor.lineNumberAreaWidth(), 0)
    def paintEvent(self, event):self.codeEditor.lineNumberAreaPaintEvent(event)

class QCodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = QLineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.updateLineNumberAreaWidth(0)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:max_value /= 10;digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:self.lineNumberArea.scroll(0, dy)
        else:self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))


    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), Qt.lightGray)
        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignRight, number)
            block = block.next();top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def keyPressEvent(self, event):
        tc=self.textCursor();self.setTextCursor(tc);charf=tc.charFormat()
        #intent
        if event.key()==Qt.Key_Return:
            try:
                intent=''
                tc.select(tc.LineUnderCursor)
                for x in tc.selectedText():
                    if x not in ['','\t']:break
                    intent+=x
                if str(tc.selectedText()).endswith(':'):intent=intent+'    '
                super(QCodeEditor, self).keyPressEvent(event)
                self.insertPlainText(intent)
            except Exception as e:print(e)
            return
        #color key
        else:
            try:
                super(QCodeEditor, self).keyPressEvent(event)
                tc.select(tc.WordUnderCursor)
                if tc.selectedText() in keywords:charf.setForeground(QtGui.QColor(255, 0, 0));tc.setCharFormat(charf)
                else:charf.setForeground(QtGui.QColor(0, 0, 0));tc.setCharFormat(charf)
            except Exception as e:print(e)

    def highlightCurrentLine(self):
        try:
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(QtGui.QColor(Qt.yellow).lighter(160))
            selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            self.setExtraSelections([selection])
        except Exception as e:print(e)

def gotoLine():

    try:
        text=input('Enter line number')
        n = int(text)
        if n < 1:print("The number must be greater than 1");return
        doc = script_win.document()
        script_win.setFocus()
        if n > doc.blockCount():self.insertPlainText("\n" * (n - doc.blockCount()))
        cursor = QTextCursor(doc.findBlockByLineNumber(n - 1))
        script_win.setTextCursor(cursor)
    except Exception as e:print(e)

def mergeFormatOnWordOrSelection(format):
    cursor = script_win.textCursor()
    if not cursor.hasSelection():
        cursor.select(QTextCursor.WordUnderCursor)
    cursor.mergeCharFormat(format)
    script_win.mergeCurrentCharFormat(format)
def find(text):
    if text=='':return
    try:
        col =QtGui.QColor(0, 0, 255)
        fmt = QTextCharFormat()
        fmt.setForeground(col)
        script_win.moveCursor(QTextCursor.Start)
        countWords = 0
        while script_win.find(text, QTextDocument.FindWholeWords):      # Find whole words
            mergeFormatOnWordOrSelection(fmt)
            countWords += 1

        print('count:'+str(countWords))

    except Exception as e:print(e)


def replace(old,new):
    try:
        script_win.textCursor().beginEditBlock()
        doc = script_win.document()
        cursor = QtGui.QTextCursor(doc)
        while True:
            cursor = doc.find(old)
            if cursor.isNull():break
            cursor.insertText(new)
        script_win.textCursor().endEditBlock()
    except Exception as e:print(e)

app = QApplication(sys.argv)

sw=QWidget()
vl=QVBoxLayout(sw)


script_win = QCodeEditor();vl.addWidget(script_win)
script_win.setLineWrapMode(QPlainTextEdit.NoWrap)
info_win = QPlainTextEdit();vl.addWidget(info_win)

def printx(x):info_win.appendPlainText(x)
def run():
    try:exec(script_win.toPlainText());info_win.appendPlainText('script run completed')
    except Exception as e:info_win.appendPlainText(str(e))
def openpy():
    try:
        f=QFileDialog.getOpenFileName(sw,'Single File','python','*.py')[0]
        script_win.appendPlainText(open(f,'r').read())
    except Exception as e:print(str(e))
    try:
        for text in keywords:find(text)
    except Exception as e:print(str(e))

def savepy():
    try:
        filename=QFileDialog.getSaveFileName(None, 'Save File','',"Python Files (*.py)")
        f=open(filename[0],'w');f.write(script_win.toPlainText());f.close()
    except Exception as e:info_win.appendPlainText(str(e))
hl=QHBoxLayout();vl.addLayout(hl)
pb=button(function=run,icon='png/run.png',w=25,h=25);hl.addWidget(pb)
pyb=button(function=openpy,icon='png/open.png',w=25,h=25);hl.addWidget(pyb)
pys=button(function=savepy,icon='png/save.png',w=25,h=25);hl.addWidget(pys)
gob=button(function=gotoLine,icon='png/goto.png',w=25,h=25);hl.addWidget(gob)
findb=button(function=find,icon='png/find.png',w=25,h=25);hl.addWidget(findb)
reb=button(function=replace,icon='png/replace.png',w=25,h=25);hl.addWidget(reb)
hl.addStretch()


sw.show()
sys.exit(app.exec_())