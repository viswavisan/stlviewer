from PyQt5 import *
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import*
from PyQt5.QtGui import *
import os


def stored(x):
    try:base_path = sys._MEIPASS
    except Exception:base_path = os.path.abspath(".")
    return os.path.join(base_path,'stored/'+x).replace('\\','/')


class QLineNumberArea(QWidget):
    def __init__(self, editor):super().__init__(editor);self.codeEditor = editor
    def sizeHint(self):return QSize(self.editor.lineNumberAreaWidth(), 0)
    def paintEvent(self, event):self.codeEditor.lineNumberAreaPaintEvent(event)

class QCodeEditor(QPlainTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.info_win=None
        self.lineNumberArea = QLineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.updateLineNumberAreaWidth(0)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.keywords=['False', 'None', 'True', 'and', 'as', 'assert', 'async','await', 'break', 'class', 'continue', 'def', 'del', 'elif',
'else', 'except', 'finally', 'for', 'from', 'global','if', 'import', 'in', 'is', 'lambda','nonlocal', 'not', 'or', 'pass', 'raise',
'return', 'try', 'while', 'with', 'yield']

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
                if tc.selectedText() in self.keywords:charf.setForeground(QtGui.QColor(255, 0, 0));tc.setCharFormat(charf)
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

    def gotoLine(self):
        try:
            n, ok = QInputDialog.getInt(self, 'input dialog', 'Enter Line number')
            if n < 1:self.printx("The number must be greater than 1");return
            doc = self.document()
            self.setFocus()
            if n > doc.blockCount():self.insertPlainText("\n" * (n - doc.blockCount()))
            cursor = QTextCursor(doc.findBlockByLineNumber(n - 1))
            self.setTextCursor(cursor)
        except Exception as e:print(e)

    def Find(self,text):
        if text=='':return
        try:
            col =QtGui.QColor(0, 0, 255)
            fmt = QTextCharFormat()
            fmt.setForeground(col)
            self.moveCursor(QTextCursor.Start)
            countWords = 0
            while self.find(text, QTextDocument.FindWholeWords):      # Find whole words
                self.mergeFormatOnWordOrSelection(fmt)
                countWords += 1
            self.printx('count:'+str(countWords))
        except Exception as e:print(e)

    def mergeFormatOnWordOrSelection(self,format):
        cursor = self.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(format)
        self.mergeCurrentCharFormat(format)

    def replace(self,old,new):
        try:
            self.textCursor().beginEditBlock()
            doc = self.document()
            cursor = QtGui.QTextCursor(doc)
            while True:
                cursor = doc.Find(old)
                if cursor.isNull():break
                cursor.insertText(new)
            self.textCursor().endEditBlock()
        except Exception as e:print(e)

    def printx(self,x):
        if self.info_win!=None:self.info_win.appendPlainText(x)
        print(x)

    def run(self):
        try:exec(self.toPlainText());info_win.appendPlainText('script run completed')
        except Exception as e:info_win.appendPlainText(str(e))
    def openpy(self):
        try:
            f=QFileDialog.getOpenFileName(self,'Single File','python','*.py')[0]
            self.appendPlainText(open(f,'r').read())
        except Exception as e:print(str(e))
        try:
            for text in self.keywords:self.Find(text)
        except Exception as e:print(str(e))

    def savepy(self):
        try:
            filename=QFileDialog.getSaveFileName(None, 'Save File','',"Python Files (*.py)")
            f=open(filename[0],'w');f.write(script_win.toPlainText());f.close()
        except Exception as e:self.printx.appendPlainText(str(e))

class script_editor(QMainWindow):
    def __init__(self,parent=None):
        super().__init__()
        self.page=QCodeEditor();self.setCentralWidget(self.page)

        ToolBar = self.addToolBar("view")
        b=QAction(QtGui.QIcon(stored("goto.png")),"goto",self);ToolBar.addAction(b);b.triggered.connect(lambda:self.page.gotoLine())
        b=QAction(QtGui.QIcon(stored("find.png")),"find",self);ToolBar.addAction(b);b.triggered.connect(lambda:self.page.Find())
        b=QAction(QtGui.QIcon(stored("replace.png")),"replace",self);ToolBar.addAction(b);b.triggered.connect(lambda:self.page.replace())
        b=QAction(QtGui.QIcon(stored("open.png")),"open",self);ToolBar.addAction(b);b.triggered.connect(lambda:self.page.openpy())
        b=QAction(QtGui.QIcon(stored("run.png")),"run",self);ToolBar.addAction(b);b.triggered.connect(lambda:self.page.run())
        b=QAction(QtGui.QIcon(stored("save.png")),"save",self);ToolBar.addAction(b);b.triggered.connect(lambda:self.page.savepy())




if __name__ == '__main__':
    app = QApplication([])
    window=script_editor()
    window.showMaximized()
    app.exec_()