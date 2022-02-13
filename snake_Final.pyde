from random import randint

TAILLE_GRILLE = 40
TAILLE_CASE = 16
top = [5,4,3,2,1]

x_pomme = TAILLE_GRILLE/2
y_pomme =  TAILLE_GRILLE/2
xs = 0
ys = 0
snake = [(xs,ys)]
d = "droite"

affichage = 'accueil'
nom = ''
score = 0
score_final = 0
s = open("save.txt","r")#fichier où se trouve le classement
record = [(s.readline().strip('\n'),int(s.readline().strip('\n'))),(s.readline().strip('\n'),int(s.readline().strip('\n'))),(s.readline().strip('\n'),int(s.readline().strip('\n'))),(s.readline().strip('\n'),int(s.readline().strip('\n'))),(s.readline().strip('\n'),int(s.readline().strip('\n')))]
s.close()
rang = 0
h = 0
clic = ''



def setup():
    global TAILLE_GRILLE, TAILLE_CASE
    size(TAILLE_CASE*TAILLE_GRILLE,TAILLE_CASE*TAILLE_GRILLE)
    frameRate(7) # Pour que  le cycle de jeux ne soit pas trop rapide
    rectMode(CENTER)
    textAlign(CENTER)
        
def draw():
    global xs, ys, TAILLE_GRILLE, snake, affichage
    background(0)
    
    if affichage == 'accueil' :
        clic = ecran_titre()
        if clic == 'JOUER' : 
            affichage = 'jeu'
        elif clic == 'QUITTER' : 
            exit()
            
    elif affichage == 'jeu' :
        if snake_est_vivant(xs,ys,TAILLE_GRILLE,snake) :
            jeu()
        else :
            affichage = 'mort'
            
    elif affichage == 'mort':
        if score > record[0][1] :
            clic = record_battu()
            if clic == "SUIVANT":
                gameover()
            
        else :
            gameover()
        


def record_battu():
    global record, score, rang, clic, nom, score_final
    for i,valeur in enumerate(record) :
        if score > valeur[1] :
            rang = i
    clic = ecran_record_battu()
    if  clic :
        for i in range(0,rang):
            record[i]=record[i+1]
        record[rang] = (nom,score)
        nom = ''
        score_final = score
        score = 0
        return "SUIVANT"
    else:
        ecran_record_battu()
        nom = choix_nom()
        
def jeu():
    global d, xs, ys, snake, x_pomme, y_pomme, score, TAILLE_CASE
    change_dir = entree_clavier()
    d = nouvelle_direction(d, change_dir)
    (xs,ys) = avancer(xs, ys, d)
    snake = [(xs,ys)] + snake
    if mange_pomme(xs, ys, x_pomme, y_pomme) :
        (x_pomme,y_pomme) = nouvelle_pomme(TAILLE_GRILLE, x_pomme, y_pomme, snake)
        score = score + 25
    else :
        snake.pop()
        
    afficher_pomme(x_pomme,y_pomme,TAILLE_CASE)
    afficher_snake(TAILLE_CASE,snake)

def gameover():
    global clic, affichage
    background(0)
    clic = ecran_perdu()
    if clic == 'REJOUER' : # Le joueur choisi de jouer
        initial()
        affichage = 'jeu'
    elif clic == 'QUITTER' : # Le joueur choisi de quitter le jeu
        s = open("save.txt","w")
        for i in range(0,len(record)):
            s.write(str(record[i][0])+"\n")
            s.write(str(record[i][1])+"\n")
        s.close()
        exit()



def initial():
    global xs, ys, snake, d, x_pomme, y_pomme, score, clic
    (xs,ys) = (0,0) 
    snake = [(xs,ys)]
    d = "droite"
    (x_pomme,y_pomme) = nouvelle_pomme(TAILLE_GRILLE,x_pomme,y_pomme,snake)
    score = 0
    clic = ''
    rang = 0

def afficher_pomme(x_pomme,y_pomme,TAILLE_CASE) :
    fill(255,0,0)
    noStroke()
    ellipse(x_pomme*TAILLE_CASE+TAILLE_CASE/2, y_pomme*TAILLE_CASE+TAILLE_CASE/2, TAILLE_CASE, TAILLE_CASE)

def afficher_snake(TAILLE_CASE,snake):
    stroke(0)
    strokeWeight(1)
    for i in range(len(snake)):
        x = snake[i][0]
        y = snake[i][1]
        fill(255)
        rect(x*TAILLE_CASE+TAILLE_CASE/2, y*TAILLE_CASE+TAILLE_CASE/2, TAILLE_CASE, TAILLE_CASE)

def avancer(xs,ys,d):
    """
    La fonction qui fait avancer le snake.
    * xs : int, colonne où se situe le snake ;
    * ys : int, la ligne où se situe le snake ;
    * d : string, la direction du snake ("droite", "haut", "gauche" ou "bas")
    """
    
    if d == "haut":
        ys = ys - 1
    elif d == "bas":
        ys = ys +1
    elif d == "droite":
        xs = xs + 1
    elif d == "gauche":
        xs = xs - 1
    return(xs,ys)
    
def tourner_gauche(d):
    """
    La fonction qui fait le snake à gauche. Elle renvoie la nouvelle direction
    du snake.
    Entrée :
    * d : string, la direction du snake ("droite", "haut", "gauche" ou "bas")
    Sortie :
    string , la nouvelle direction du snake ("droite", "haut", "gauche" ou "bas").
    """
    if d == "droite":
        d = "haut"
    elif d == "gauche":
        d = "bas"
    elif d == "haut":
        d = "gauche"
    elif d == "bas":
        d = "droite"
    return(d)

def tourner_droite(d):
    """
    La fonction qui fait le snake à droite. Elle renvoie la nouvelle direction
    du snake.
    Entrée :
    * d : string, la direction du snake ("droite", "haut", "gauche" ou "bas")
    Sortie :
    string , la nouvelle direction du snake ("droite", "haut", "gauche" ou "bas").
    """
    if d == "droite":
        d = "bas"
    elif d == "gauche":
        d = "haut"
    elif d == "haut":
        d = "droite"
    elif d == "bas":
        d = "gauche"
    return(d)
    
def nouvelle_direction(d,change_dir):
    if change_dir == "droite" :
        d = tourner_droite(d)
    elif change_dir== "gauche" :
        d = tourner_gauche(d)
    
    return(d)
    
def mange_pomme(xs, ys, x_pomme, y_pomme):
    """
    La fonction vérifie si le snake mange la pomme.
    Entrées :
    * xs,ys : position du snake
    * x_pomme, y_pomme : position de la pomme
    Sortie : Booléen
    """
    if (xs,ys) == (x_pomme,y_pomme):
        return(True) 
    else :
        return(False)
    
def nouvelle_pomme(TAILLE_GRILLE, x_pomme, y_pomme, snake):
    x_pomme = randint(1,TAILLE_GRILLE-1)
    y_pomme = randint(1,TAILLE_GRILLE-1)
    for i in range(len(snake)):
        while (x_pomme,y_pomme) == snake[i]:
            x_pomme = randint(1,TAILLE_GRILLE-1)
            y_pomme = randint(1,TAILLE_GRILLE-1)
    return(x_pomme,y_pomme)

def snake_est_vivant(xs, ys, TAILLE_GRILLE, snake):
    """
    Fonction qui teste si le snake sort ou non de la grille.
    Entrées :
    * xs,ys : position du snake
    * taille_grille : la longueur du côté de la grille carrée.
    Sortie : Booléen
    """
    for i in range(len(snake)) :
            if snake[0] == snake[i] and i != 0 :
                return False
    if xs >= TAILLE_GRILLE or xs < 0 :
        return False
    elif ys >= TAILLE_GRILLE or ys < 0 :
        return False
    else :
        return True 

def entree_clavier():
    if keyPressed :
        if key == 'c':
            return "droite"
        elif key == 'w' :
            return "gauche" 
        else :
            return "aucun"

def choix_nom() : 
    global nom
    if keyPressed :
        if key == '\x08' :
            nom = nom[:-1]
        else :
            nom = nom + key
    return nom





def ecran_titre():
    """
    Fonction qui affiche l'ecran d'accueil
    """
    global nom, record, clic, h, top
#rectangle principal
    fill(0)
    strokeWeight(7)
    stroke(59,26,255)
    rect(width/2,height/2,width-32,height-32,7)
    fill(255,0,0)
#boutons   
    stroke(0,232,36)
    if bouton(190,528,220,64,'JOUER',[100,232,132],[0,232,36]) ==True:
        clic = 'JOUER'
    stroke(255,0,0)
    if bouton(480,528,220,64,'QUITTER',[255,100,100],[255,0,0]) == True :
        clic = 'QUITTER'
#écritures
    fill(255)
    font = createFont("simson", 80)
    textFont(font, 80)
    textSize(145)
    text("SNAKE",width/2,165)
    font = loadFont("ArialRoundedMTBold-80.vlw")
    textFont(font, 80)
    textSize(20)
    text(" W = Gauche ",100,250)
    text(" C = Droite    ",100,280)
    text(" 1 pomme = +25pts",130,310)
#tableau des score
    stroke(255)
    fill(0)
    rect(460,325,280,250,7)
    fill(255)
    text('Tableau des scores :',440,240)
    textAlign(LEFT)
    h = 430
    for i in range(0,len(record)):
        text(str(top[i])+" :   "+record[i][0]+".........."+str(record[i][1]), 340, h)
        h = h - 35
    noStroke()
    textAlign(CENTER)
    
    return clic
    
def ecran_perdu():
    """
    Fonction qui affiche une fenêtre 'Game Over'
    """
    global score, record, clic, rang, top, score_final
#rectangle principale
    fill(0)
    strokeWeight(7)
    stroke(0,0,255)
    rect(width/2,height/2,440,440,7)
#boutons
    stroke(0,255,0)
    if bouton(230,452,160,64,'REJOUER',[120,255,120],[0,255,0]):
        clic = 'REJOUER'
    stroke(255,0,0)
    if bouton(425,452,160,64,'QUITTER',[255,100,100],[255,0,0]):
        clic = 'QUITTER'
    noStroke()
#écritures
    font = createFont("simson", 80)
    textFont(font, 80)
    textSize(80)
    fill(255)
    text("GAME OVER",width/2,220)
    font = loadFont("ArialRoundedMTBold-80.vlw")
    textFont(font, 80)
    textSize(40)
    text("Votre score : " + str(score_final), 300, 300)
    textSize(30)
    text("Record : " + str(record[4][0])+" "+str(record[4][1]),340,340)
    
    return clic

def ecran_record_battu():
    global score, record, nom, rang, clic
#rectangle principale
    fill(0)
    strokeWeight(7)
    stroke(0,0,255)
    rect(width/2,height/2,490,490,7)
#écritures
    fill(255)
    font = createFont("simson", 80)
    textFont(font, 80)
    textSize(65)
    text("RECORD BATTU",width/2,220)
    font = loadFont("ArialRoundedMTBold-80.vlw")
    textFont(font, 80)
    stroke(255,0,0)
    line(110,230,500,230)
    textSize(40)
    text("Votre score : " + str(score),300,300)
    textSize(30)
    text("Ancien record : "+str(record[rang][1])+"(top "+str(top[rang])+")",300,340)
    fill(0)
#case nom
    stroke(0,0,255)
    rect(width/2,410,350,70,7)
    fill(255)
    textSize(35)
    textAlign(LEFT)
    text("Nom : " + str(nom),200,420)
    textAlign(CENTER)
    fill(0)
#bouton
    stroke(0,255,0)
    clic = bouton(450,517,180,64,'SUIVANT',[120,255,120],[0,255,0])
    
    return clic
    
def bouton(x,y,largeur,hauteur,texte,couleur,couleur2):
    """
    Fonction qui affiche un bouton qui change de couleur quand la souris passe dessus.
    x,y : coordonnées du bouton
    largeur,hauteur : dimension du bouton
    couleur : couleur du bouton quand la souris passe dessus
    couleur2 : couleur du bouton
    """
    textSize(32)
    if  x - largeur/2 < mouseX < x + largeur/2 and  y-hauteur/2 < mouseY < y + hauteur/2 :
        fill (couleur[0],couleur[1],couleur[2])
        rect(x,y,largeur,hauteur,20)
        fill(0,0,0)
        text(texte,x,y+hauteur*0.28)
        if mousePressed :
            return True
    else:
        fill (couleur2[0],couleur2[1],couleur2[2])
        rect(x,y,largeur,hauteur,20)
        fill(0,0,0)
        text(texte,x,y+hauteur*0.28)
    return False
        
