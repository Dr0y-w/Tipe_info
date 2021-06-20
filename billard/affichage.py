from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# importation du module PyOpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import pyqtgraph as pg

# importation du module contenant la class générée par Qtdesigner
from ui import Ui_Dialog

from module import *
from module_math import *

class mainWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.angle = 0  # utilisé pour tourner la camera
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.openGLWidget = self.ui.openGLWidget  # raccourci

        self.ui.graphicsView.setLabel("left", "EC", color='red')  # définit le titre de l'axe y
        self.ui.graphicsView.setLabel("bottom", "temps(s)")  # définit le titre de l'axe x
        self.ui.graphicsView.setBackground((0, 0, 0))  # couleur en rgb du background
        self.pen = pg.mkPen(color=(255, 0, 0), width=3)  # choix du pen définissant les caractéristique du trait

        self.i = 0
        #objet et space
        self.b1 = Ball([0,0],1,10,(255,0,0),[0.1,0.1],2)
        self.b2 = Ball([-2,-2],1,10,(0,255,0),[0.3,-0.3],1)
        self.b3 = Ball([2,2],1,10,(0,0,255),[-0.2,0.3],1)
        #wall
        self.w1 = Wall([-20,-10],[-20,10])
        self.w2 = Wall([-20,10],[-7,15])
        self.w3 = Wall([-7,15],[8,25])
        self.w4 = Wall([8,25],[20,-5])
        self.w5 = Wall([20,-5],[12,-24])
        self.w6 = Wall([12,-24],[-24,-19])
        self.w7 = Wall([-24,-19],[-20,-10])


        self.s = Space([self.b1,self.b2,self.b3],[self.w1,self.w2,self.w3,self.w4,self.w5,self.w6,self.w7])

        self.energie_cinetique = [[energie_cinetique(ball)] for ball in self.s.balls]
        self.temps = [0]
#j'aime max3nce

    def setupUI(self):  # initialisation de la vue et création du timer
        self.openGLWidget.initializeGL() # appelé au premier affichage uniquement
        self.openGLWidget.resizeGL(800, 800)
        self.openGLWidget.paintGL = self.paintGL # raccourci

        timer = QTimer(self)  # Le timer
        timer.timeout.connect(self.openGLWidget.update)  # appelle la fonction en argument (sans parenthèse )
        #timer.timeout.connect(self.graph)
        #ici update appelle la fonction resizeGL et paintGL
        timer.start(10)  # lance le timer pour un temps de 10 ms entre chaque timeout

    def paintGL(self):  # réécriture de la fonction de base pour afficher la scène                # appelé a chaque 'update' lancé par le timer
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(0, 0, 0, 1)  # définition de la couleur du font,le dernier nombre est l'alpha/la transparence
        self.s.collision()

                #affichage des disques
        for i  in range(len(self.s.balls)):
            self.energie_cinetique[i].append(10*energie_cinetique((self.s.balls[i])))
            glBegin(GL_POLYGON) # début de l'affichage des polygones
            glColor(self.s.balls[i].couleur)
            for point in self.s.balls[i].point:
                glVertex2f(*point)
            glEnd() # fin de l'affichage des polygones
        #affichage des walls
        for wall in self.s.walls:
            glBegin(GL_LINES)
            glColor((255,255,255))
            glVertex2f(*wall.p1)
            glVertex2f(*wall.p2)
            glEnd()

        glMatrixMode(GL_PROJECTION)  # charge la matrice de projection
        """ on change ici les options de la projection sur l'écran """
        glLoadIdentity()  # charge une matrice identité
        gluPerspective(45.0, 1, 1, 400000)  # fov , ratio , distance de vue proche, distance de vue de loin

        glMatrixMode(GL_MODELVIEW)  # charge la matrice de caméra
        """ on change ici la position de la caméra """
        glLoadIdentity()  # charge une matrice identité
        gluLookAt(0, 1, 100,
                  0, 0, 0,
                  0, 1, 0)
        # coordonnées de la position de la caméra  ,coordonnées du point vers lequel
        #elle est dirigée, axe vertical de la caméra
        glRotatef(0, 0, 1, 0)  # permet de tourner la caméra autour de l'axe x ,y ,z

        glTranslatef( 0, 0, 0.1)#permet de déplacer la camera ,
        # mais est impacté par la rotation de la camera

    def clear(self):
        self.ui.graphicsView.clear()
    def graph(self):
        self.i += 0.1
        self.ui.graphicsView.setXRange(1, 4+self.i)
        i = len(self.energie_cinetique[0])
        self.temps = [i*0.1 for i in range(i)]
        self.clear()
        for i in range(len(self.energie_cinetique)):
            self.ui.graphicsView.plot(self.temps,self.energie_cinetique[i],pen = self.pen)
app = QApplication(sys.argv)
window = mainWindow()
window.setupUI() # on initialize le Qwidget et le QOpenGLwidget
window.show()
sys.exit(app.exec_())
