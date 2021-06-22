def cube(taille,centre):

    xc,yc,zc = centre
    B = (xc+0.5*taille,yc-0.5*taille,zc+0.5*taille)
    C = (xc+0.5*taille,yc-0.5*taille,zc-0.5*taille)
    D = (xc-0.5*taille,yc-0.5*taille,zc-0.5*taille)
    E = (xc-0.5*taille,yc-0.5*taille,zc+0.5*taille)
    F = (xc+0.5*taille,yc+0.5*taille,zc+0.5*taille)
    G = (xc+0.5*taille,yc+0.5*taille,zc-0.5*taille)
    H = (xc-0.5*taille,yc+0.5*taille,zc-0.5*taille)
    I = (xc-0.5*taille,yc+0.5*taille,zc+0.5*taille)

    segments = [[B,C],[B,E],[E,D],[D,C],[E,I],[I,F],[F,B],[C,G],[F,G],[D,H],[I,H],[H,G]]
    faces = [[B,C,D,E],[F,B,C,G],[D,E,I,H],[I,F,G,H],[C,D,H,G]]
    return segments,faces
