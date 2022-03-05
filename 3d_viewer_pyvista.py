import os

import pyvista as pv
from pyvistaqt import QtInteractor, MainWindow
from pyvista import examples
import random

from PyQt5 import *
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import*
from PyQt5.QtGui import *
import pyautogui
import pyiges
pid={};glob={'color':{},'pidname':{}}

def png(x):
    def resource_path(relative_path):
        try:base_path = sys._MEIPASS
        except Exception:base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    return resource_path('png/'+x+'.png').replace('\\','/')

def msgbox(text="",Type=0):
   msgBox = QMessageBox()
   msgBox.setIcon(QMessageBox.Information)
   msgBox.setText(text)
   if Type==1: msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
   returnValue = msgBox.exec()
   if returnValue == QMessageBox.Ok:return 1
   else:return 0

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
'return', 'try', 'while', 'with', 'yield','self','print','printx']
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
                if tc.selectedText() in keywords:charf.setForeground(QtGui.QColor(0, 0, 255));tc.setCharFormat(charf)
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


def bpress(b):
    if b.text()=='prop':dock.setVisible(dock.isVisible()==False)
    elif b.text()=='open':load_stl_f()
    elif b.text()=='edge':edge_visibility()
    elif b.text()=='color':random_color()
    elif b.text()=='fit':plotter.reset_camera()
    elif b.text()=='invert':invert()
    elif b.text()=='hide':hide()
    elif b.text()=='show':show()
    elif b.text()=='capture':capture()
    elif b.text()=='locate':locate()
    elif b.text()=='showonly':showonly()
    elif b.text()=='isometric':isometric()
    elif b.text()=='front':front()
    elif b.text()=='point':point_info()
    elif b.text()=='cell':cell_info()
    elif b.text()=='actor':actor_info()
    elif b.text()=='marker':marker()
    elif b.text()=='delete':delete_actor()
    elif b.text()=='BG':bgcolor()

def marker():
    return
def new():
    try:
        try:plotter.remove_background_image()
        except:pass
        plotter.clear()
        pid.clear();prop.clear();glob['pidname'].clear()
    except Exception as e:print(e)
    return

def delete_actor():
    try:
        for x in prop.selectedItems():
            plotter.remove_actor(pid[x.text()])
            del(pid[x.text()]);del glob['pidname'][pid[x.text()]]
            prop.takeItem(prop.row(x))
    except Exception as e:print(e)
def merge():

    try:
        filenames=QFileDialog.getOpenFileNames(window,'VTK File','','*.stl;*.vtk;*.obj')
        if filenames[0]==[]:return
        for filename in filenames[0]:
            (name,ext)=os.path.splitext(os.path.basename(filename))
            if name in pid:msgbox('duplicate file name found');continue

            mesh = pv.PolyData(filename)
            actor=plotter.add_mesh(mesh,style='surface', show_edges=True,color=[0.3,0.8,0.5])
            prop.addItem(name);pid[name]=actor;glob['pidname'][actor]=name
            if 'datas' in glob:glob['datas'].append(mesh)
            else:glob['datas']=[mesh]
    except Exception as e:print(e)
    return

def load_stl_f():
    try:
        folder=QFileDialog.getExistingDirectory()
        if folder=='':return

        for filename in os.listdir(folder):
            if not filename.endswith('.stl'):continue
            mesh = pv.PolyData(folder+'/'+filename)
            actor=plotter.add_mesh(mesh,style='surface', show_edges=True,color=[0.3,0.8,0.5],pickable=True)

            pid[filename.replace('.stl','')]=actor;prop.addItem(filename.replace('.stl',''));glob['pidname'][actor]=filename.replace('.stl','')
            if 'datas' in glob:glob['datas'].append(mesh)
            else:glob['datas']=[mesh]
    except Exception as e:print(e)


def Export():
    try:
        filename=QFileDialog.getSaveFileName(None, 'Save File','','*.stl;;*.vtk;;*.obj')
        outformat=filename[1]
        if filename[0]=='':return

        if len(glob['datas'])>1:merged=glob['datas'][0].merge(glob['datas'][1:])
        elif len(glob['datas'])==1:merged=glob['datas'][0]
        else:return

        merged.save(filename[0])
    except Exception as e:print(e)
    return
def importiges():

    try:
        filenames=QFileDialog.getOpenFileNames(window,'IGES File','','*.iges;*.igs')
        if filenames[0]==[]:return
        for filename in filenames[0]:
            dir=os.path.dirname(filename)
            (name,ext)=os.path.splitext(os.path.basename(filename))

            iges = pyiges.read(filename)
            mesh = iges.to_vtk(bsplines=True, surfaces=True, merge=True)

            actor=plotter.add_mesh(mesh,style='surface', show_edges=True,color=[0.3,0.8,0.5])
            pid[name]=actor;prop.addItem(name)
            if 'datas' in glob:glob['datas'].append(mesh)
            else:glob['datas']=[mesh]
    except Exception as e:print(e)

def bgcolor():
    try:
        col = QColorDialog.getColor()
        (r,g,b,a)=col.getRgb()
        plotter.set_background([r/255,g/255,b/255])
    except Exception as e:print(e)
def bgi():
    try:
        try:plotter.remove_background_image()
        except:pass
        f=QFileDialog.getOpenFileName(window,'Single File','image','*png;*.jpg;*.jpeg')[0]
        if f=='':
            try:plotter.remove_background_image()
            except:pass
        else:plotter.add_background_image(f)
    except Exception as e:print(e)
def capture():
    try:
        filename=QFileDialog.getSaveFileName(window,"","","png Files (*png)")[0]
        plotter.screenshot(filename=filename, transparent_background=None, return_img=True, window_size=None)
    except Exception as e:print(e)
def edge_visibility():
    try:
        x=[1,0][list(pid.values())[0].GetProperty().GetEdgeVisibility()]
        for k,v in pid.items():v.GetProperty().SetEdgeVisibility(x)
    except:return
def hide():
    for x in prop.selectedItems():pid[x.text()].SetVisibility(False)

def show():
    for x in prop.selectedItems():pid[x.text()].SetVisibility(True)

def invert():
    for k,v in pid.items():v.SetVisibility(v.GetVisibility()==0)

def isometric():plotter.view_isometric(negative=False)

def front():plotter.view_xy(negative=False)

def showonly():
    selected=[x.text() for x in prop.selectedItems()]
    for k,v in pid.items():
        if k in selected:v.SetVisibility(True)
        else:v.SetVisibility(False)

def showall():
    for k,v in pid.items():v.SetVisibility(True)

def hideall():
    for k,v in pid.items():v.SetVisibility(False)

def visible_actors():return[v for k,v in pid.items() if v.GetVisibility()==1]


def locate():
    va=visible_actors()
    selected=[x.text() for x in prop.selectedItems()]
    for k,v in pid.items():
        if k in selected:v.SetVisibility(True)
        else:v.SetVisibility(False)
    plotter.reset_camera()
    for v in va:v.SetVisibility(True)

def propselected():

    for k,v in pid.items():
        v.GetProperty().SetColor(1,1,1)
        v.GetProperty().SetOpacity(0.5)
    for x in prop.selectedItems():
        pid[x.text()].GetProperty().SetColor(1,0,0)
        pid[x.text()].GetProperty().SetOpacity(1)

def random_color():
    for k,v in pid.items():
        if k not in glob['color']:glob['color'][k]=[random.randint(0,255)/255,random.randint(0,255)/255,random.randint(0,255)/255]
        v.GetProperty().SetColor(glob['color'][k][0],glob['color'][k][1],glob['color'][k][2])
        v.GetProperty().SetOpacity(1)
    prop.clearSelection()
def colorEdit():
    try:
        col = QColorDialog.getColor()
        (r,g,b,a)=col.getRgb()
        for x in prop.selectedItems():glob['color'][x.text()]=[r/255,g/255,b/255]
        random_color()
    except Exception as e:print(e)
    return

def show_grid(x):grid.SetVisibility(int(x))

def ex1():
    poly = examples.download_nefertiti()
    actor=plotter.add_mesh(poly, color='w')
    plotter.enable_cell_picking()
    pid['Example1']=actor
    prop.addItem('Example1')
    return

def create_sphere():
    try:
        actor=plotter.add_mesh(pv.Sphere(), color="tan", show_edges=True)
        plotter.reset_camera()
        pid['Sphere']=actor
        prop.addItem('Sphere')
    except Exception as e:print(e)

app = QtWidgets.QApplication([])
window=QMainWindow()
window.setWindowTitle("3D viewer")

#menu bar
menu= window.menuBar()
file = menu.addMenu("File")
#sub-menu
b=QAction(QtGui.QIcon(png('open')),"New/Clear",window);b.triggered.connect(new);file.addAction(b)
b=QAction(QtGui.QIcon(png('open')),"Import/Merge",window);b.triggered.connect(merge);file.addAction(b)
b=QAction(QtGui.QIcon(png('open')),"STL-import-folder",window);b.triggered.connect(load_stl_f);file.addAction(b)
file.addSeparator()
b=QAction(QtGui.QIcon(png('open')),"Export",window);b.triggered.connect(Export);file.addAction(b)

file.addSeparator()
b=QAction(QtGui.QIcon(png('open')),"Import_iges",window);b.triggered.connect(importiges);file.addAction(b)

view = menu.addMenu("View")
b=QAction(QtGui.QIcon(png('open')),"view_xy",window);b.triggered.connect(lambda:plotter.view_xy(negative=False));view.addAction(b)
b=QAction(QtGui.QIcon(png('open')),"view_xz",window);b.triggered.connect(lambda:plotter.view_xz(negative=False));view.addAction(b)
b=QAction(QtGui.QIcon(png('open')),"view_yx",window);b.triggered.connect(lambda:plotter.view_yx(negative=False));view.addAction(b)
b=QAction(QtGui.QIcon(png('open')),"view_yz",window);b.triggered.connect(lambda:plotter.view_yz(negative=False));view.addAction(b)
b=QAction(QtGui.QIcon(png('open')),"view_zx",window);b.triggered.connect(lambda:plotter.view_zx(negative=False));view.addAction(b)
b=QAction(QtGui.QIcon(png('open')),"view_zy",window);b.triggered.connect(lambda:plotter.view_zy(negative=False));view.addAction(b)

create = menu.addMenu("Create")
b=QAction(QtGui.QIcon(png('open')),"sphere",window);b.triggered.connect(create_sphere);create.addAction(b)

Example = menu.addMenu("Example")
b=QAction(QtGui.QIcon(png('open')),"Example1",window);b.triggered.connect(ex1);Example.addAction(b)




#3d window
centralwidget = QWidget(window)
window.setCentralWidget(centralwidget)
verticalLayout = QVBoxLayout(centralwidget)

frame = QFrame();verticalLayout.addWidget(frame)
vl = QVBoxLayout();frame.setLayout(vl)

plotter = QtInteractor(frame)
vl.addWidget(plotter.interactor)
plotter.show_axes()


grid=plotter.show_grid();grid.VisibilityOff()
#window.signal_close.connect(plotter.close)



def clicked(event):
    try:
        picker = pv._vtk.vtkPropPicker()
        picker.PickProp(event[0], event[1],plotter.ren_win.GetRenderers().GetFirstRenderer())
        actor=picker.GetActor()
        if actor!=None and actor in glob['pidname']:
            name=glob['pidname'][actor]
            for item in prop.findItems(name,Qt.MatchExactly):
                prop.setCurrentItem(item)
    except Exception as e:print(e)

plotter.track_click_position(callback=clicked,side='left', viewport=True)
#toolbar
fileToolBar = window.addToolBar("view")
fileToolBar.addAction(QAction(QtGui.QIcon(png('prop')),"prop",window))
fileToolBar.addAction(QAction(QtGui.QIcon(png('open')),"open",window))
fileToolBar.addAction(QAction(QtGui.QIcon(png('mesh')),"edge",window))
fileToolBar.addAction(QAction(QtGui.QIcon(png('color')),"color",window))
b=QAction(QtGui.QIcon(png('colorEdit')),"colorEdit",window);fileToolBar.addAction(b);b.triggered.connect(colorEdit)
fileToolBar.addAction(QAction(QtGui.QIcon(png('fit')),"fit",window))
fileToolBar.addAction(QAction(QtGui.QIcon(png('invert')),"invert",window))
b=QAction(QtGui.QIcon(png('showall')),"showall",window);fileToolBar.addAction(b);b.triggered.connect(showall)
fileToolBar.addAction(QAction(QtGui.QIcon(png('hide')),"hide",window))
fileToolBar.addAction(QAction(QtGui.QIcon(png('show')),"show",window))
fileToolBar.addAction(QAction(QtGui.QIcon(png('showonly')),"showonly",window))
fileToolBar.addAction(QAction(QtGui.QIcon(png('locate')),"locate",window))
fileToolBar.addAction(QAction(QtGui.QIcon(png('capture')),"capture",window))
fileToolBar.addAction(QAction(QtGui.QIcon(png('isometric')),"isometric",window))
fileToolBar.addAction(QAction(QtGui.QIcon(png('front')),"front",window))
fileToolBar.addAction(QAction(QtGui.QIcon(png('create')),"create",window))

fileToolBar.addAction(QAction(QtGui.QIcon(png('marker')),"marker",window))
fileToolBar.addAction(QAction(QtGui.QIcon(png('bin')),"delete",window))
fileToolBar.addAction(QAction("BG",window))
b=QAction("BGI",window);fileToolBar.addAction(b);b.triggered.connect(bgi)
fileToolBar.actionTriggered[QAction].connect(bpress)

b=QAction(QtGui.QIcon(png('measure')),"measure",window,checkable=True);fileToolBar.addAction(b);b.triggered.connect(show_grid)


#prop doc
dock = QDockWidget("Properties",window)
prop = QListWidget()
prop.setStyleSheet('''QListWidget::item:selected:!active {background: lightBlue;color: black;}''')
dock.setWidget(prop)
window.addDockWidget(Qt.LeftDockWidgetArea,dock)
dock.setFeatures(QDockWidget.DockWidgetMovable|QDockWidget.DockWidgetClosable)
prop.itemClicked.connect(propselected)
prop.setSelectionMode(QAbstractItemView.ExtendedSelection)

#info dock
dock2 = QDockWidget("info",window)
info_win = QPlainTextEdit()
dock2.setWidget(info_win)
window.addDockWidget(Qt.BottomDockWidgetArea,dock2)
dock2.setFeatures(QDockWidget.DockWidgetMovable|QDockWidget.DockWidgetClosable)

#info dock
dock3 = QDockWidget("Script",window)
sw=QWidget()
vl=QVBoxLayout(sw)
dock3.setWidget(sw)


script_win = QCodeEditor();vl.addWidget(script_win)
script_win.setLineWrapMode(QPlainTextEdit.NoWrap)

def gotoLine():

    try:
        text,ok= QInputDialog.getInt(script_win, 'GoTo', 'Enter Line number:')
        if not ok:return
        n = int(text)
        if n < 1:print("The number must be greater than 1");return
        doc = script_win.document()
        script_win.setFocus()
        if n > doc.blockCount():script_win.moveCursor(QTextCursor.End)
        else:cursor = QTextCursor(doc.findBlockByLineNumber(n - 1));script_win.setTextCursor(cursor)
    except Exception as e:printx(e)

def mergeFormatOnWordOrSelection(format):
    cursor = script_win.textCursor()
    if not cursor.hasSelection():
        cursor.select(QTextCursor.WordUnderCursor)
    cursor.mergeCharFormat(format)
    script_win.mergeCurrentCharFormat(format)
def find(text):
    try:
        col =QtGui.QColor(0, 0, 255)
        fmt = QTextCharFormat()
        fmt.setForeground(col)
        script_win.moveCursor(QTextCursor.Start)
        countWords = 0
        while script_win.find(text, QTextDocument.FindWholeWords):      # Find whole words
            mergeFormatOnWordOrSelection(fmt)
    except Exception as e:printx(e)

def find2():
    text,ok= QInputDialog.getText(script_win, 'Find', 'Enter Word to find:')
    if not ok:return
    if text=='':return
    try:
        script_win.moveCursor(QTextCursor.Start)
        while script_win.find(text, QTextDocument.FindWholeWords):      # Find whole words
            ans=msgbox('for next word press ok',1)
            if ans==0:return
    except Exception as e:printx(e)



def replace():
    text,ok= QInputDialog.getText(script_win, 'Find', 'Enter Word to find|replace:')
    if not ok:return
    try:
        [old,new]=text.split('|')
        script_win.textCursor().beginEditBlock()
        doc = script_win.document()
        cursor = QtGui.QTextCursor(doc)
        while True:
            cursor = doc.find(old)
            if cursor.isNull():break
            cursor.insertText(new)
        script_win.textCursor().endEditBlock()
    except Exception as e:printx(e)

def printx(x):info_win.appendPlainText(str(x))
def run():
    try:exec(script_win.toPlainText());info_win.appendPlainText('script run completed')
    except Exception as e:info_win.appendPlainText(str(e))
def openpy():
    try:
        f=QFileDialog.getOpenFileName(window,'Single File','python','*.py')[0]
        script_win.clear()
        script_win.appendPlainText(open(f,'r').read())
    except Exception as e:info_win.appendPlainText(str(e))

    try:
        for text in keywords:find(text)
    except Exception as e:print(str(e))
def savepy():
    try:
        filename=QFileDialog.getSaveFileName(None, 'Save File','',"Python Files (*.py)")
        f=open(filename[0],'w');f.write(script_win.toPlainText());f.close()
    except Exception as e:info_win.appendPlainText(str(e))

hl=QHBoxLayout();vl.addLayout(hl)
pb=button(function=run,icon=png('run'),w=25,h=25);hl.addWidget(pb)
pyb=button(function=openpy,icon=png('open'),w=25,h=25);hl.addWidget(pyb)
pys=button(function=savepy,icon=png('save'),w=25,h=25);hl.addWidget(pys)
gob=button(function=gotoLine,icon=png('goto'),w=25,h=25);hl.addWidget(gob)
findb=button(function=find2,icon=png('find'),w=25,h=25);hl.addWidget(findb)
reb=button(function=replace,icon=png('replace'),w=25,h=25);hl.addWidget(reb)
reb=button(function=lambda:script_win.clear(),icon=png('clear'),w=25,h=25);hl.addWidget(reb)
hl.addStretch()

window.addDockWidget(Qt.BottomDockWidgetArea,dock3)
dock3.setFeatures(QDockWidget.DockWidgetMovable|QDockWidget.DockWidgetClosable)

sb=window.statusBar()
sb.setStyleSheet('background-color : lightgray')
window.show()
app.exec_()