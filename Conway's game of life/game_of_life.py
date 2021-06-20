from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


from game_of_life_ui import Ui_Dialog
from module import *

class mainWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.openGLWidget = self.ui.openGLWidget
        self.hauteur = 40
        self.longueur = 40
        self.grid = Grid(self.hauteur,self.longueur)
        self.grid.gen()

    def setupUI(self):
        self.openGLWidget.initializeGL()
        self.openGLWidget.resizeGL(800, 600)
        self.openGLWidget.paintGL = self.paintGL

        timer = QTimer(self)
        timer.timeout.connect(self.openGLWidget.update)
        timer.start(1000)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(0.9, 0.9, 0.9, 1)


        glBegin(GL_QUADS)

        """glColor3f(1, 0, 0)
        for i in range(6):
            for e in carre((i,i)):
                glVertex2fv(e)"""

        for e in self.grid.rang_suivant():
            for f in carre(e[0]):
                if e[1]==1:
                    glColor3f(1, 1, 1)
                    glVertex2fv(f)
                else:
                    glColor3f(0, 0, 0)
                    glVertex2fv(f)
        glEnd()

        glMatrixMode(GL_PROJECTION)

        glLoadIdentity()
        gluPerspective(45.0, 1 , 0, 40000)

        glMatrixMode(GL_MODELVIEW)

        glLoadIdentity()
        gluLookAt(self.longueur/2, self.hauteur/2, 3*max((self.hauteur/2,self.longueur/2)) ,  # 2n+2 bof
        self.longueur/2, self.longueur/2, 0,
        0, 1, 0)
        self.grid.rang_suivant()

app = QApplication(sys.argv)
window = mainWindow()
window.setupUI()
window.show()
sys.exit(app.exec_())
