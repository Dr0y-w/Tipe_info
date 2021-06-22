from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Figure import cube



# importation du module PyOpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# importation du module contenant la class générée par Qtdesigner
from untitled import Ui_Dialog

segments,faces = cube(1, (0, 0,0 ))

class mainWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.angle = 0  # utilisé pour tourner la camera
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.openGLWidget = self.ui.openGLWidget  # raccourci

    def setupUI(self):  # initialisation de la vue et création du timer
        self.openGLWidget.initializeGL() # appelé au premier affichage uniquement
        self.openGLWidget.resizeGL(800, 600)
        self.openGLWidget.paintGL = self.paintGL # raccourci

        timer = QTimer(self)  # Le timer
        timer.timeout.connect(self.openGLWidget.update)  # appelle la fonction en argument (sans parenthèse )
        #ici update appelle la fonction resizeGL et paintGL
        timer.start(10)  # lance le timer pour un temps de 10 ms entre chaque timeout

    def paintGL(self):  # réécriture de la fonction de base pour afficher la scène
                        # appelé a chaque 'update' lancé par le timer
        self.angle += 1
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(0, 0, 0, 1)  # définition de la couleur du font,le dernier nombre est l'alpha/la transparence


        glBegin(GL_QUADS)
        glColor3f(1,1,1)
        for i in range(len(faces)):
            glVertex3fv(faces[i][0])
            glVertex3fv(faces[i][1])
            glVertex3fv(faces[i][2])
            glVertex3fv(faces[i][3])
        glEnd()

        glBegin(GL_LINES)

        for i in range(len(segments)):
            glColor3f(0, 0, 0)
            glVertex3fv(segments[i][0])
            glVertex3fv(segments[i][1])


        glEnd()
        """glBegin() et glEnd() ne sont pas très optimisées
         Il existe des manières plus efficace pour faire la même chose mais plus complexe
         chercher 'modern OpenGL' et  'VAO' ou 'VBO'
         """

        glMatrixMode(GL_PROJECTION)  # charge la matrice de projection
        """ on change ici les options de la projection sur l'écran """
        glLoadIdentity()  # charge une matrice identité
        gluPerspective(45.0, 1, 1, 40)  # fov , ratio , distance de vue proche, distance de vue de loin

        glMatrixMode(GL_MODELVIEW)  # charge la matrice de caméra
        """ on change ici la position de la caméra """
        glLoadIdentity()  # charge une matrice identité
        gluLookAt(0, 1, -4,
                  0, 0, 0,
                  0, 1, 0)
        # coordonnées de la position de la caméra  ,coordonnées du point vers lequel elle est dirigée, axe vertical de la caméra
        glRotatef(0.4*self.angle,1 , 1, 1)  # permet de tourner la caméra autour de l'axe x ,y ,z

        #glTranslatef( 0, 0, 0.01*self.angle)#permet de déplacer la camera ,
        # mais est impacté par la rotation de la camera



app = QApplication(sys.argv)
window = mainWindow()
window.setupUI() # on initialize le QOpenGLwidget
window.show()
sys.exit(app.exec_())