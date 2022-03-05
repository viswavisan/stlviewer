from PyQt5 import *
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import*
from PyQt5.QtGui import *

#import pyiges



import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import os
import random
import csv


pid={}
pidname={}
glob={'cdir':os.getcwd()}

def msgbox(text="",Type=0):
   msgBox = QMessageBox()
   msgBox.setIcon(QMessageBox.Information)
   msgBox.setText(text)
   if Type==1: msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
   returnValue = msgBox.exec()
   if returnValue == QMessageBox.Ok:return 1
   else:return 0

def button(text='',function=None,icon=None,h=None,w=None,flat=False,tip=None,curser=None):
    print(icon)
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
    elif b.text()=='color':random_color_1()
    elif b.text()=='colorEdit':colorEdit()
    elif b.text()=='fit':ren.ResetCamera();ren_inter.Initialize()
    elif b.text()=='invert':invert()
    elif b.text()=='hide':hide()
    elif b.text()=='show':show()
    elif b.text()=='capture':capture()
    elif b.text()=='locate':locate()
    elif b.text()=='showonly':showonly()
    elif b.text()=='isometric':isometric()
    elif b.text()=='front':front()
    elif b.text()=='create':createsphere()
    elif b.text()=='point':point_info()
    elif b.text()=='cell':cell_info()
    elif b.text()=='actor':actor_info()
    elif b.text()=='measure':measure()
    elif b.text()=='marker':marker()
    elif b.text()=='delete':delete_actor()
    elif b.text()=='BG':bgcolor()
def colorEdit():
    try:
        col = QColorDialog.getColor()
        (r,g,b,a)=col.getRgb()
        for x in prop.selectedItems():glob['color'][x.text()]=[r/255,g/255,b/255]
        random_color_1()
    except Exception as e:print(e)
    return
def marker():
    return
def new():
    ren.RemoveAllViewProps()
    pid.clear();prop.clear();glob['datas'].clear()
    ren.ResetCamera()
    return
def importiges():


    filenames=QFileDialog.getOpenFileNames(window,'IGES File','','*.iges;*.igs')
    if filenames[0]==[]:return
    for filename in filenames[0]:
        dir=os.path.dirname(filename)
        (name,ext)=os.path.splitext(os.path.basename(filename))

        iges = pyiges.read(filename)
        mesh = iges.to_vtk(bsplines=False, surfaces=True, merge=True)
        mesh.save(dir+'/'+name+'/.vtk')

        reader = vtk.vtkPolyDataReader()
        reader.SetFileName(dir+'/'+name+'/.vtk')
        reader.Update()
        actor = vtk.vtkActor();ren.AddActor(actor)

        mapper = vtk.vtkPolyDataMapper();actor.SetMapper(mapper)
        mapper.SetInputConnection(reader.GetOutputPort())
        ren.ResetCamera()

        if 'datas' in glob:glob['datas'].append(reader)
        else:glob['datas']=[reader]
        prop.addItem(name);pid[name]=actor;pidname[actor]=name

        if os.path.exists(dir+'/'+name+'/.vtk'):os.remove(dir+'/'+name+'/.vtk')

def merge():

    try:
        filenames=QFileDialog.getOpenFileNames(window,'VTK File','','*.stl;*.vtk;*.obj')
        if filenames[0]==[]:return
        for filename in filenames[0]:
            (name,ext)=os.path.splitext(os.path.basename(filename))
            if name in pid:msgbox('duplicate file name found');continue

            if ext=='.stl':reader = vtk.vtkSTLReader()
            elif ext=='.vtk':reader = vtk.vtkPolyDataReader()

            reader.SetFileName(filename)
            reader.Update()
            actor = vtk.vtkActor();ren.AddActor(actor)

            mapper = vtk.vtkPolyDataMapper();actor.SetMapper(mapper)
            mapper.SetInputConnection(reader.GetOutputPort())
            ren.ResetCamera()

            if 'datas' in glob:glob['datas'].append(reader)
            else:glob['datas']=[reader]
            prop.addItem(name);pid[name]=actor;pidname[actor]=name
    except Exception as e:print(e)
    return



def load_stl_f():
    try:
        folder=QFileDialog.getExistingDirectory()
        if folder=='':return
        glob['cdir']=folder
        ren.RemoveAllViewProps()
        pid.clear();prop.clear()

        for filename in os.listdir(folder):
            if not filename.endswith('.stl'):continue
            prop.addItem(filename.replace('.stl',''))
            reader = vtk.vtkSTLReader()
            reader.SetFileName(folder+'/'+filename)
            reader.Update()

            actor = vtk.vtkActor();ren.AddActor(actor);pid[filename.replace('.stl','')]=actor
            pidname[actor]=filename.replace('.stl','')
            mapper = vtk.vtkPolyDataMapper();actor.SetMapper(mapper)
            mapper.SetInputConnection(reader.GetOutputPort())

            if 'datas' in glob:glob['datas'].append(reader)
            else:glob['datas']=[reader]
            ren.ResetCamera()
        random_color()
    except Exception as e:print(e)


def Export():
    try:
        filename=QFileDialog.getSaveFileName(None, 'Save File','','*.stl;;*.vtk;;*.obj')
        outformat=filename[1]
        if filename[0]=='':return

        vtkappend = vtk.vtkAppendPolyData()
        for data in glob['datas']:vtkappend.AddInputData(data.GetOutput())
        vtkappend.Update()

        if outformat=='*.stl':writer = vtk.vtkSTLWriter()
        elif outformat=='*.vtk':writer = vtk.vtkPolyDataWriter()
        elif outformat=='*.obj':writer = vtk.vtkMNIObjectWriter()
        elif outformat=='*.tag':writer = vtk.vtkMNITagPointWriter()

        writer.SetInputData(vtkappend.GetOutput())
        writer.SetFileName(filename[0])
        writer.Write()
    except Exception as e:print(e)
    return
def bgcolor():
    col = QColorDialog.getColor()
    (r,g,b,a)=col.getRgb()
    ren.SetBackground(r/255,g/255,b/255)
def point_info():
    def clicked(obj,event):
        clickPos = mouse.GetInteractor().GetEventPosition()
        picker = vtk.vtkPointPicker()
        picker.Pick(clickPos[0], clickPos[1], 0,mouse.GetDefaultRenderer())
        if picker.GetPointId()!=-1:
            info_win.appendPlainText(str(picker.GetPointId())+':'+str(picker.GetMapperPosition()))
            mouse.RemoveAllObservers()
        mouse.OnLeftButtonDown()
    mouse.RemoveAllObservers()
    mouse.AddObserver("LeftButtonPressEvent", clicked)

def cell_info():
    def clicked(obj,event):
        clickPos = mouse.GetInteractor().GetEventPosition()
        picker = vtk.vtkCellPicker()
        picker.Pick(clickPos[0], clickPos[1], 0,mouse.GetDefaultRenderer())
        if picker.GetCellId()!=-1:
            info_win.appendPlainText(str(picker.GetCellId())+':'+str(picker.GetMapperPosition()))
            mouse.RemoveAllObservers()
        mouse.OnLeftButtonDown()
    mouse.RemoveAllObservers()
    mouse.AddObserver("LeftButtonPressEvent", clicked)

def actor_info():
    def clicked(obj,event):
        clickPos = mouse.GetInteractor().GetEventPosition()
        picker = vtk.vtkPropPicker()
        picker.PickProp(clickPos[0], clickPos[1], mouse.GetDefaultRenderer())
        actor=picker.GetActor()
        if actor!=None:
            prop.setCurrentItem(prop.findItems(pidname[actor],Qt.MatchExactly)[0])
            info_win.appendPlainText(pidname[actor])
            mouse.RemoveAllObservers()
        mouse.OnLeftButtonDown()
    mouse.RemoveAllObservers()
    mouse.AddObserver("LeftButtonPressEvent", clicked)



def measure():
    widget = vtk.vtkDistanceWidget()
    widget.SetInteractor(ren_inter)
    widget.CreateDefaultRepresentation()
    widget.On()




def capture():
    filename=QFileDialog.getSaveFileName(window,"","","png Files (*png)")[0]
    w2if =vtk.vtkWindowToImageFilter()
    w2if.SetInput(render_window)
    w2if.Update()
    writer = vtk.vtkPNGWriter()
    writer.SetFileName(filename)
    writer.SetInputData(w2if.GetOutput())
    writer.Write()
    return
def edge_visibility():
    try:
        x=[1,0][list(pid.values())[0].GetProperty().GetEdgeVisibility()]
        for k,v in pid.items():v.GetProperty().SetEdgeVisibility(x)
        ren_inter.Render()
    except:return
def hide():
    for x in prop.selectedItems():pid[x.text()].SetVisibility(False)
    ren_inter.Render()

def show():
    for x in prop.selectedItems():pid[x.text()].SetVisibility(True)
    ren_inter.Render()
def showonly():
    selected=[x.text() for x in prop.selectedItems()]
    for k,v in pid.items():
        if k in selected:v.SetVisibility(True)
        else:v.SetVisibility(False)
    ren_inter.Render()
def showall():
    for k,v in pid.items():v.SetVisibility(True)
    ren_inter.Render()
def hideall():
    for k,v in pid.items():v.SetVisibility(False)
    ren_inter.Render()

def visible_actors():return[v for k,v in pid.items() if v.GetVisibility()==1]

def delete_actor():
    for x in prop.selectedItems():
        ren.RemoveActor(pid[x.text()])
        del(pid[x.text()])
        prop.takeItem(prop.row(x))

def locate():
    va=visible_actors()
    selected=[x.text() for x in prop.selectedItems()]
    for k,v in pid.items():
        if k in selected:v.SetVisibility(True)
        else:v.SetVisibility(False)
    ren.ResetCamera()
    for v in va:v.SetVisibility(True)
    ren_inter.Render()

def front():
    ren .GetActiveCamera().SetFocalPoint(0,1,0)
    ren .GetActiveCamera().SetPosition(0,0,0)
    ren .GetActiveCamera().SetViewUp(0,0,1)
    ren.ResetCamera()
    ren_inter.Render()

def isometric():
    ren .GetActiveCamera().SetFocalPoint(1,1,-1)
    ren .GetActiveCamera().SetPosition(0,0,0)
    ren .GetActiveCamera().SetViewUp(0,0,1)
    ren.ResetCamera()
    ren_inter.Render()



def invert():
    for k,v in pid.items():v.SetVisibility(v.GetVisibility()==0)
    ren_inter.Render()

def propselected():

    for k,v in pid.items():
        v.GetProperty().SetColor(1,1,1)
        v.GetProperty().SetOpacity(0.5)
    for x in prop.selectedItems():
        pid[x.text()].GetProperty().SetColor(1,0,0)
        pid[x.text()].GetProperty().SetOpacity(1)
    ren_inter.Render()

def create_pidcolor():
    try:
        color=glob['cdir']+'/pidcolor'
        file=open(color, 'w', newline='')
        writer = csv.writer(file)
        data=[[k,random.randint(0,255)/255,random.randint(0,255)/255,random.randint(0,255)/255]for k,v in pid.items()]
        C= {line[0]:line[1:] for line in data}
        writer.writerows(data)
        file.close()
        for k,v in pid.items():
            v.GetProperty().SetColor(float(C[k][0]),float(C[k][1]),float(C[k][2]))
            v.GetProperty().SetOpacity(1)
            ren_inter.Render()
    except Exception as e:print(e)
def random_color_1():
    try:
        C=glob['color']
        for k,v in pid.items():
            v.GetProperty().SetColor(float(C[k][0]),float(C[k][1]),float(C[k][2]))
            v.GetProperty().SetOpacity(1)
            ren_inter.Render()
    except Exception as e:
        random_color()
        print(e)
def random_color():
    try:
        color=glob['cdir']+'/pidcolor'
        file=open(color)
        data = csv.reader(file)
        C={line[0]:line[1:] for line in data}
        glob['color']=C
        file.close()
        for k,v in pid.items():
            v.GetProperty().SetColor(float(C[k][0]),float(C[k][1]),float(C[k][2]))
            v.GetProperty().SetOpacity(1)
            ren_inter.Render()

    except Exception as e:
        create_pidcolor()
        print(e)

def createsphere():
    def cylinder():
        cylinderSource = vtk.vtkCylinderSource()
        cylinderSource.SetCenter(0.0, 0.0, 0.0)
        cylinderSource.SetRadius(5.0)
        cylinderSource.SetHeight(7.0)
        cylinderSource.SetResolution(100)
        return cylinderSource
    def circle():
        polygonSource = vtk.vtkRegularPolygonSource()
        polygonSource.GeneratePolygonOff()
        polygonSource.SetNumberOfSides(50)
        polygonSource.SetRadius(5.0)
        polygonSource.SetCenter(0.0, 0.0, 0.0)
        return polygonSource
    def point():
        src = vtk.vtkPointSource()
        src.SetCenter(0, 0, 0)
        src.SetNumberOfPoints(1)
        src.SetRadius(0)
        src.Update()
        return src
    def line():
        line = vtk.vtkLineSource()
        line.SetPoint1(0,0,0)
        line.SetPoint2(0,0,1)
        line.Update()
        return line
    def plane():
        planeSource = vtk.vtkPlaneSource()
        planeSource.SetCenter(1.0, 0.0, 0.0)
        planeSource.SetNormal(0.0, 1.0, 0.0)
        planeSource.SetPoint1(10.0, 0.0, 0.0 );
        planeSource.SetPoint2(0.0, 0.0, 10.0 );
        planeSource.Update()
        return planeSource


    def cone():
        cone = vtk.vtkConeSource()
        cone.SetHeight(3.0)
        cone.SetRadius(1.0)
        cone.SetResolution(10)
        return cone
    def sphere():
        source = vtk.vtkSphereSource()
        source.SetRadius(float(r))
        source.SetCenter(float(x), float(y), float(z))
        source.SetPhiResolution(11)
        source.SetThetaResolution(21)
        return source

    def create():
        (x,y,z)=LE1.text().split(',')
        r=LE2.text()
        source=point()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(source.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        pid['plane']=actor
        prop.addItem('plane')

        actor.GetProperty().SetDiffuseColor(0.5,0.5, 0.5)
        actor.GetProperty().SetDiffuse(.8)
        actor.GetProperty().SetSpecular(.5)
        actor.GetProperty().SetSpecularColor(1.0,1.0,1.0)
        actor.GetProperty().SetSpecularPower(30.0)

        ren.AddActor(actor)
        ren.ResetCamera()
        w2.close()
    w2= QDialog()
    GL = QGridLayout();w2.setLayout(GL)
    GL.addWidget(QLabel('Coordinates'),0,0)
    GL.addWidget(QLabel('radius'),1,0)
    LE1=QLineEdit('0,0,0');GL.addWidget(LE1,0,1)
    LE2=QLineEdit('5');GL.addWidget(LE2,1,1)
    pb = QPushButton('ok');GL.addWidget(pb,2,1)
    pb.clicked.connect(create)
    w2.exec()


app = QApplication([])
window= QMainWindow()
window.setWindowTitle("3D viewer")

#menu bar
menu= window.menuBar()
file = menu.addMenu("File")
script = menu.addMenu("Script")
#sub-menu
b=QAction(QtGui.QIcon("png/open.png"),"New/Clear",window);b.triggered.connect(new);file.addAction(b)
b=QAction(QtGui.QIcon("png/open.png"),"Import/Merge",window);b.triggered.connect(merge);file.addAction(b)
b=QAction(QtGui.QIcon("png/open.png"),"STL-import-folder",window);b.triggered.connect(load_stl_f);file.addAction(b)
file.addSeparator()
b=QAction(QtGui.QIcon("png/open.png"),"Export",window);b.triggered.connect(Export);file.addAction(b)

file.addSeparator()
b=QAction(QtGui.QIcon("png/open.png"),"Import_iges",window);b.triggered.connect(importiges);file.addAction(b)

#3d window
centralwidget = QWidget(window)
window.setCentralWidget(centralwidget)
verticalLayout = QVBoxLayout(centralwidget)

frame = QFrame();verticalLayout.addWidget(frame)
vl = QVBoxLayout();frame.setLayout(vl)

ren_inter = QVTKRenderWindowInteractor(frame);vl.addWidget(ren_inter)
render_window=ren_inter.GetRenderWindow()
ren = vtk.vtkRenderer();render_window.AddRenderer(ren)
ren.SetBackground(1/255,20/255,40/255)
#ren.SetBackground(1,1,1)

axes = vtk.vtkAxesActor()
axesxyz=vtk.vtkOrientationMarkerWidget()
axesxyz.SetOrientationMarker(axes)
axesxyz.SetInteractor(ren_inter)
axesxyz.EnabledOn()
axesxyz.InteractiveOn()

mouse=vtk.vtkInteractorStyleTrackballCamera()
mouse.SetDefaultRenderer(ren)
ren_inter.SetInteractorStyle(mouse)

ren_inter.Start()

#toolbar
fileToolBar = window.addToolBar("view")
fileToolBar.addAction(QAction(QtGui.QIcon("png/prop.png"),"prop",window))
fileToolBar.addAction(QAction(QtGui.QIcon("png/open.png"),"open",window))
fileToolBar.addAction(QAction(QtGui.QIcon("png/mesh.png"),"edge",window))
fileToolBar.addAction(QAction(QtGui.QIcon("png/color.png"),"color",window))
fileToolBar.addAction(QAction(QtGui.QIcon("png/colorEdit.png"),"colorEdit",window))
fileToolBar.addAction(QAction(QtGui.QIcon("png/fit.png"),"fit",window))
fileToolBar.addAction(QAction(QtGui.QIcon("png/invert.png"),"invert",window))
fileToolBar.addAction(QAction(QtGui.QIcon("png/hide.png"),"hide",window))
fileToolBar.addAction(QAction(QtGui.QIcon("png/show.png"),"show",window))
fileToolBar.addAction(QAction(QtGui.QIcon("png/showonly.png"),"showonly",window))
fileToolBar.addAction(QAction(QtGui.QIcon("png/locate.png"),"locate",window))
fileToolBar.addAction(QAction(QtGui.QIcon("png/capture.png"),"capture",window))
fileToolBar.addAction(QAction(QtGui.QIcon("png/isometric.png"),"isometric",window))
fileToolBar.addAction(QAction(QtGui.QIcon("png/front.png"),"front",window))
fileToolBar.addAction(QAction(QtGui.QIcon("png/create.png"),"create",window))
fileToolBar.addAction(QAction(QtGui.QIcon("png/measure.png"),"measure",window))
fileToolBar.addAction(QAction(QtGui.QIcon("png/marker.png"),"marker",window))
fileToolBar.addAction(QAction(QtGui.QIcon("png/bin.png"),"delete",window))
fileToolBar.addAction(QAction("BG",window))
fileToolBar.actionTriggered[QAction].connect(bpress)

infoToolBar = window.addToolBar("info")
b=QAction(QtGui.QIcon("png/point.png"),"point",window);infoToolBar.addAction(b)
#b.setVisible(False)
infoToolBar.addAction(QAction(QtGui.QIcon("png/cell.png"),"cell",window))
infoToolBar.addAction(QAction(QtGui.QIcon("png/actor.png"),"actor",window))
infoToolBar.actionTriggered[QAction].connect(bpress)
#prop doc
dock = QDockWidget("Properties",window)
prop = QListWidget()
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

def clear():script_win.clear()

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
        clear()
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
pb=button(function=run,icon='png/run.png',w=25,h=25);hl.addWidget(pb)
pyb=button(function=openpy,icon='png/open.png',w=25,h=25);hl.addWidget(pyb)
pys=button(function=savepy,icon='png/save.png',w=25,h=25);hl.addWidget(pys)
gob=button(function=gotoLine,icon='png/goto.png',w=25,h=25);hl.addWidget(gob)
findb=button(function=find2,icon='png/find.png',w=25,h=25);hl.addWidget(findb)
reb=button(function=replace,icon='png/replace.png',w=25,h=25);hl.addWidget(reb)
reb=button(function=clear,icon='png/clear.png',w=25,h=25);hl.addWidget(reb)
hl.addStretch()

window.addDockWidget(Qt.BottomDockWidgetArea,dock3)
dock3.setFeatures(QDockWidget.DockWidgetMovable|QDockWidget.DockWidgetClosable)

sb=window.statusBar()
sb.setStyleSheet('background-color : lightgray')
window.show()
app.exec_()