"""
@author: Aslan
"""

import numpy as np  
import matplotlib.pyplot as plt
import numpy.random as alea

def visu_point(matPoint,style):
    # matPoint contient les coordonnées des points
    x = matPoint[0, :]
    y = matPoint[1, :]
    plt.plot(x, y, style)
    
def visu_segment(P1,P2,style):
    # attention P1 et P2 sont des tableaux (2,1)
    matP = np.concatenate((P1,P2),1)
    visu_point(matP,style)
    
def mat_rotation(origine, matrice, theta):
    # si pas besoin des coordonnées homogènes
    mat = np.dot(np.array([[1,0,-origine[0]],
                           [0,1,-origine[1]],
                           [0,0,1]]), matrice)
    mat = np.dot(np.array([[np.cos(theta), -np.sin(theta), 0],
                    [np.sin(theta), np.cos(theta), 0],
                    [0,0,1]]), mat)
    mat = np.dot(np.array([[1,0,origine[0]],
                           [0,1,origine[1]],
                           [0,0,1]]), mat)
    return mat

def visu_BezierQuad(matPointControl,str):
    
    n=50
    mt = np.linspace(0,1.,n)
    matt = np.ones((3,n))  # que des 1
    matt[1,:] = mt  # ligne avec les t
    matt[2,:] = mt*mt  # ligne avec les t*t
    
    matBezier3 = np.array([[1, 0, 0],
                           [-2, 2, 0],
                           [1, -2, 1]])

    matPointligne = np.dot(np.dot(matt.T,matBezier3),matPointControl.T)
    matPoint=matPointligne.T  # on transpose

    visu_point(matPoint,str)


def toileAraignee(origine, nbFormes, nbCourbes, distanceEntreCourbes, parametrePivot, style):
    angleForme = 360/nbFormes
    demiAngle = angleForme/2;
    
    #Les coordonnes en extremite de chaque courbe
    extremiteCourbesDroite = [[],[],[]]
    extremiteCourbesGauche = [[],[],[]]
    for i in range(1, nbCourbes+1):
        extremiteCourbesDroite[0].append(origine[0]) # en x c'est meme chose
        extremiteCourbesDroite[1].append(origine[1]-i*distanceEntreCourbes)
        extremiteCourbesDroite[2].append(1)
        extremiteCourbesGauche[0].append(origine[0]) # en x c'est meme chose
        extremiteCourbesGauche[1].append(origine[1]-i*distanceEntreCourbes)
        extremiteCourbesGauche[2].append(1)
    #Tournons ces segments en demi angle
    extremiteCourbesDroite = mat_rotation(origine, extremiteCourbesDroite, np.radians(-demiAngle))
    extremiteCourbesGauche = mat_rotation(origine, extremiteCourbesGauche, np.radians(demiAngle))
    
    #Formons une liste des pivots pour chaque courbe de Bezier
    pivots = [[origine[0]],[origine[1]], [1]]
    for i in range(nbCourbes-1):
        pivots[0].append(origine[0]) # en x il a meme position qu'origine
        pivots[1].append(extremiteCourbesDroite[1][i])
        pivots[2].append(1)
        
    #Dessinons tous les formes
    for forme in range(nbFormes):
        pivotsAlea = pivots.copy()
        for i in range(2):
            for j in range(len(pivotsAlea[i])):
                pivotsAlea[i][j] = (pivotsAlea[i][j] + (alea.rand()-0.5) * parametrePivot)
        #affichage de 2 segments
        visu_point(np.array([[extremiteCourbesDroite[0][-1],origine[0],extremiteCourbesGauche[0][-1]],[extremiteCourbesDroite[1][-1],origine[1], extremiteCourbesGauche[1][-1]]]), style)

        #Dessinons des courbes
        for courbe in range(nbCourbes):
            #Toutes les coordonnees dont on a besoin pour faire une courbe
            droitePosX = extremiteCourbesDroite[0][courbe]
            droitePosY = extremiteCourbesDroite[1][courbe]
            pivotPosX = pivotsAlea[0][courbe]
            pivotPosY = pivotsAlea[1][courbe]
            gauchePosX = extremiteCourbesGauche[0][courbe]
            gauchePosY = extremiteCourbesGauche[1][courbe]
            
            #enfin, la courbe, apres avoir formé les coordonnees
            pointsForme = np.array([[droitePosX,pivotPosX,gauchePosX],[droitePosY,pivotPosY, gauchePosY]])
            visu_BezierQuad(pointsForme, style)
        
        #Tournons tous les coordonnes par angle de forme, pour le prochain affichage
        extremiteCourbesDroite = mat_rotation(origine, extremiteCourbesDroite, np.radians(angleForme))
        extremiteCourbesGauche = mat_rotation(origine, extremiteCourbesGauche, np.radians(angleForme))
        pivots = mat_rotation(origine, pivots, np.radians(angleForme))
    #Fin de fonction toileAraignee
    

#pour afficher le graphique
plt.axis('scaled') 
taille=20
plt.xlim(-0.25, taille+0.25)  
plt.ylim(-0.25, taille+0.25)


nombreDeFormes = 15
nombreDeCourbes = 10
distanceEntreCourbes = 0.8
parametrePivot = 0.4;
toileAraignee(np.array([17,15]), nombreDeFormes, nombreDeCourbes, distanceEntreCourbes, parametrePivot, 'black')

nombreDeFormes = 11
nombreDeCourbes = 7
distanceEntreCourbes = 0.8
parametrePivot = 0;
toileAraignee(np.array([0,19]), nombreDeFormes, nombreDeCourbes, distanceEntreCourbes, parametrePivot, 'black')

nombreDeFormes = 12
nombreDeCourbes = 7
distanceEntreCourbes = 0.8
parametrePivot = 0;
toileAraignee(np.array([5,6]), nombreDeFormes, nombreDeCourbes, distanceEntreCourbes, parametrePivot, 'black')

nombreDeFormes = 9
nombreDeCourbes = 5
distanceEntreCourbes = 0.8
parametrePivot = 0.9;
toileAraignee(np.array([17.5,1.5]), nombreDeFormes, nombreDeCourbes, distanceEntreCourbes, parametrePivot, 'black')

