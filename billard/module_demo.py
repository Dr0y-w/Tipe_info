from math import sin, cos , pi , fabs
from module_math import *


class Wall:
    def __init__(self,p1,p2):
        self.p1 = p1
        self.p2 = p2

class Ball:
    def __init__(self,centre,rayon,precision,couleur,vitesse,masse):
        self.vitesse = vitesse #2D
        self.masse = masse
        self.centre = centre #2D
        self.rayon = rayon #1D
        self.precision = precision # en degré
        self.point = self.points()
        self.couleur = couleur #rgb capé a 255

    def refresh(self):
        self.point = self.points()

    def points(self):#gen les points
        points = []
        iteration = int(360/self.precision)
        angle = self.precision*pi/180
        for i in range(iteration):
            p = [self.centre[0]-self.rayon*cos(angle*i),
            self.centre[1]+ self.rayon*sin(angle*i)]
            points.append(p)
        return points

class Space:
    def __init__(self,balls,walls):
        self.balls = balls#liste
        self.walls = walls#liste
    def collision(self):
        for i in range(len(self.balls)):
            ball = self.balls[i]
            collision_m = False #etat de la collision avec les mur
            collision_b = False #etat de la collision avec les balls
            distance_l = []
            lsite_b = []
            for wall in self.walls:
                for p in separation_en_taille([wall.p1,wall.p2],ball.rayon/4):
                    d = distance(ball.centre,p)
                    if d < ball.rayon :
                        distance_l.append([d,wall.p2,p])
                        collision_m = True
                    #test si la distance est plus petite la vitesse
            for j in range(len(self.balls)):
                if j != i:
                    if distance(self.balls[i].centre, self.balls[j].centre) <= self.balls[i].rayon +self.balls[j].rayon :
                        liste_b=[i,j]
                        collision_b = True

            if collision_m:
                l = tri(distance_l)
                p1 = l[1]
                p = l[2]
                v1 = ball.vitesse
                ball.vitesse = vecteur_incident(v1,p,p1)
                self.balls[i].centre = addition_2d(ball.centre,ball.vitesse)
                ball.refresh()
            elif collision_b:
                #gen les deux nouveaux vecteurs des balls
                #on commence par trouvé le point de collision :
                i,j = liste_b
                ball1 = self.balls[i]
                v1 = [ball1.vitesse[0],ball1.vitesse[1]]
                ball2 = self.balls[j]
                v2 = [ball2.vitesse[0],ball2.vitesse[1]]
                c1_c2 = get_vecteur(ball1.centre,ball2.centre)
                p = addition_2d(ball1.centre,multiplication_2d(ball1.rayon, c1_c2)) #point de collision
                # on fait comme pour les murs pour les 2 balles

                #on determine le sens des vecteurs v1 et v2
                #on commence par determiner 2 point sur le plan d'incidence
                vecteur_plan_normal = normale(c1_c2)
                p1 = addition_2d(p,vecteur_plan_normal)
                #on calcule b1
                b1= addition_2d(p,[-v1[0],-v1[1]])
                #on calcul le nouveau sens de v1
                #p et p1 sont =
                v1_f = vecteur_incident(v1,p,p1)

                #on calcule b2
                b2= addition_2d(p,[-v2[0],-v2[1]])
                ##on calcul le nouveau sens de v2
                v2_f = vecteur_incident(v2,p,p1)
                #on determine les nouvelles normes
                """liste_vitesse = vitesse_collision(ball1.masse,ball2.masse, norme(ball1.vitesse), norme(ball2.vitesse) )
                v1_f=multiplication_2d(liste_vitesse[1],v1_f)
                v2_f=multiplication_2d(liste_vitesse[2],v1_f)
                """
                """
                resultat = vitesse_bidimensionel_demo(ball1.vitesse,ball2.vitesse,ball1.masse,ball2.masse)
                v1_f = unitaire(v1_f)
                v2_f = unitaire(v2_f)
                v1_f = [v1_f[0]*resultat[0][0],v1_f[1]*resultat[0][1]]
                v2_f = [v2_f[0]*resultat[1][0],v2_f[1]*resultat[1][1]]
                """
                #on affecte les changement
                ball1.vitesse = v1_f
                ball2.vitesse = v2_f
                ball1.centre = addition_2d(ball1.centre,ball1.vitesse)
                ball2.centre = addition_2d(ball2.centre,ball2.vitesse)
                ball.refresh()
            else:
                self.balls[i].centre = addition_2d(ball.centre,ball.vitesse)
                ball.refresh()
