from math import sin, cos , pi ,sqrt , atan , fabs

#opération sur les listes/tuples 2D
def addition_2d(l1,l2):
    return [l1[0]+l2[0],l1[1]+l2[1]]

def multiplication_2d(scalaire,l1):
    return [scalaire*l1[0],scalaire*l1[1]]

#operation sur les points
def distance(p1,p2):#calcul la distance entre deux points
    return sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)

def get_vecteur(p1,p2):#permet d'obtenir le vecteur entre deux points
#vecteur dirgé de p1 vers p2
    return (p2[0]-p1[0],p2[1]-p1[1])
#operation sur les vecteurs

def colineaire(v1,v2):#v1 et v2 des vecteurs:
    rapport = v1[0]*v2[1]-v1[1]*v2[0]
    if rapport == 0:
        return True
    return False

def norme(v1):#calcul la norme d'un vecteur
    return sqrt(v1[0]**2 + v1[1]**2)

def vecteur_to_2points(v):#v un vecteur cartesien_polaire
    return [[0,0],v]

def normale(v1):#calcul le vecteur normale
    return [-v1[1],v1[0]]

def cartesien_polaire(v1):#un vecteur en cartesien: [x,y]
    return norme(v1),atan(v1[1]/v1[0])

def polaire_cartesien(v1):#un vecteur en polaire : [norme,angle(en rad)]
    x = v1[0]*cos(v1[1])
    y = v1[0]*sin(v1[1])
    return x,y


#opération sur les segments

def separation_en_taille(s,taille):#segment = [p1,p2]
    p1,p2 = s
    d = distance(p1,p2)
    pas = int((d/taille))
    vect = get_vecteur(s[0],s[1])
    points = []
    for i in range(pas):
        v  = multiplication_2d(taille*i/10,vect)
        p = addition_2d(p1,v)
        if not(distance(p1,p)>distance(p1,p2)):
            points.append(p)
    return points
def separation_en_taille_demo(s,taille):#segment = [p1,p2]
    p1,p2 = s
    d = distance(p1,p2)
    pas = int((d/taille))
    vect = get_vecteur(s[0],s[1])
    points = []
    for i in range(pas):
        v  = multiplication_2d(taille*i/20,vect)
        p = addition_2d(p1,v)
        if not(distance(p1,p)>distance(p1,p2)):
            points.append(p)
    return points

def tri(liste):#prend une liste dont on va trié les elements
#par la premiere element de chaque sous listes on retourneras l'indices du plus petit element
    cursor = liste[0]
    for i in range(1,len(liste)):
        if cursor[0] > liste[i][0]:
            cursor = liste[i]
    return cursor

def unitaire(v1):
    n = norme(v1)
    return [v1[0]/n, v1[1]/n]

def produit_scalaire(v1,v2): #produit scalaire entre deux vecteurs
    return (v1[0]*v2[0] + v1[1]*v2[1])

def projette_orthogonale(u,b,a):#projete orthogonal de a sur la droite de vecteur directeur u passant par b
    bh = ((a[0]-b[0])*u[0] +(a[1]-b[1])*u[1])/sqrt(u[0]**2 +u[1]**2)
    xh = b[0] + (bh/sqrt(u[0]**2 +u[1]**2))*u[0]
    yh = b[1] + (bh/sqrt(u[0]**2 +u[1]**2))*u[1]
    return [xh,yh]


def vecteur_incident(v1,p,p1):#v1 = vitesse init, p = point d'intersection, p1 un point du wall droite
    b = addition_2d(p,[-v1[0],-v1[1]])
    u = get_vecteur(p,p1)
    """if norme(u) != 0:
        h = projette_orthogonale(u,p,b)
        ph = get_vecteur(p,h)
        add = multiplication_2d(-2,ph)
        c1 = addition_2d(b,add)
        return get_vecteur(p,c1)
    else :
        return [0.000001,0.0000001]"""
    h = projette_orthogonale(u,p,b)
    ph = get_vecteur(p,h)
    add = multiplication_2d(-2,ph)
    c1 = addition_2d(b,add)
    return get_vecteur(p,c1)

def vitesse_collision(m1,m2,v1,v2):
    a = (m2*m2)/m1
    b = 2*m2*v1 + 2*(m2*m2*v2)/m1
    c = ((m2*m2)*(v2*v2))/(m1) + 2*m2*v1*v2 - m2*v2*v2
    delta = b*b - 4*a*c

    v2B = (-b -(delta)**0.5)/(2*a)
    v2A = (-b +(delta)**0.5)/(2*a)
    v1A = v1 +(m2/m1)*(v2 - v2A)
    v1B = v1 +(m2/m1)*(v2 - v2B)
    #v1a v2b sont les vitesse correcte
    return v1A,v1B,v2A,v2B

def vitesse_unidimensionel(v1,v2,m1,m2):#une seule dimension
    """v1_a = ((m1-m2)/(m1+m2))*v1 + 2*v2*m2/(m1+m2)
    v2_a = ((2*m1)/(m1+m2))*v1 + ((m2-m1)/(m1+m2))*v2"""
    v1_a = m2/(m1+m2)
    v2_a = m1/(m1+m2)
    return v1_a,v2_a

def vitesse_bidimensionel(v1,v2,m1,m2): #2 dimension
    r1 = vitesse_unidimensionel(v1[0],v2[0],m1,m2)
    r2 = vitesse_unidimensionel(v1[1],v2[1],m1,m2)
    v1_a_x = fabs(r1[0])
    v1_a_y = fabs(r2[0])
    v2_a_x = fabs(r1[1])
    v2_a_y = fabs(r2[1])
    return [v1_a_x,v1_a_y],[v2_a_x,v2_a_y]

def energie_cinetique(ball):
    return 0.5*ball.masse* norme(ball.vitesse)**2
