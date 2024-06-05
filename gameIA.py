import tkinter as tk
import mapList
import mouv
from time import sleep
import game
import numpy as np
from tqdm import tqdm
from math import sqrt




def redo(t):
    print(True,t)
    player.start()
    for _ in tqdm(range(t)):
        action_n = np.argmax(case_action[player.y][player.x])
        if action_n == 0:  # droite
            player.goRight()
            game.goGraph(player, game.playerAvatar)

        elif action_n == 1:  # bas
            player.goDown()
            game.goGraph(player, game.playerAvatar)

        elif action_n == 2:  # gauche
            player.goLeft()
            game.goGraph(player, game.playerAvatar)
        
        elif action_n == 3:  # gauche - haut
            player.Jump('l')
            game.goGraph(player, game.playerAvatar)
            
            
        elif action_n == 4:  # droite - haut
            player.Jump('r')
            game.goGraph(player, game.playerAvatar)
        
        else:  # haut
            player.Jump('sky')
            game.goGraph(player, game.playerAvatar)
            
        game.mouvementGraph()
        
    

#tk.Button(root, text='redo', command=redo).grid(column=99, row=99)
    
    
    
def choix_action():
    '''choisit entre l'exploration et l'exploitation d'information
    l'exploration pourcentage epsilon de chance de faire un mouvement alléatoire
    l'exploitation récupère le mouvement le plus aventageux d'après ces calculs
    '''
    global case_action, epsilon
    if np.random.uniform() < epsilon:
        action = np.random.choice(6)  # renvoi un mouvement alléatoire
    else:
        # renvoile meuilleure mouvement calculé
        action = np.argmax(case_action[player.y][player.x])
        
    return action    
    
def ia_train(p):
    '''répète le shéma d'aprentissage pour minimiser le nombre de tours
    '''
    
    global epsilon,case_action, player
    
    player = p
    gameMap = mapList.maps[player.map]

    for i in range(len(gameMap)):
        for j in range(len(gameMap[0])):
            if gameMap[i][j] == 'door': 
                dx=j
                dy=i
    gamma = player.aiVar[1][6]
    alpha = player.aiVar[0][6]
    epsilon = player.aiVar[3][6]
    Ly = len(gameMap)
    Lx = len(gameMap[0])
    # création de la matrice a 3 dimention pour stoqué les valeur des mouvement
    case_action = np.zeros((Ly, Lx, 6))
    player1 = mouv.Tyr()
    player1.board = gameMap
    for _ in tqdm(range(((Lx*Ly)**2//8)*int(player.aiVar[2][6]))):
        player.start()# remise a zéro
        player.gameCondition = None  # remise a zéro
        time = 0  # remise a zéro
        player1.start()  # remise a zéro
        while player.gameCondition == None and 100 >= time:
            action_n = choix_action()
            player1.x = player.x  # garde le précédant état
            player1.y = player.y  # garde le précédant état

            if action_n == 0:  # droite
                player.goRight()
                game.goGraph(player, game.playerAvatar)

            elif action_n == 1:  # bas
                player.goDown()
                game.goGraph(player, game.playerAvatar)

            elif action_n == 2:  # gauche
                player.goLeft()
                game.goGraph(player, game.playerAvatar)
            
            elif action_n == 3:  # gauche - haut
                player.Jump('l')
                game.goGraph(player, game.playerAvatar)
                
            elif action_n == 4:  # droite - haut
                player.Jump('r')
                game.goGraph(player, game.playerAvatar)
            
            else:  # haut
                player.Jump('sky')
                game.goGraph(player, game.playerAvatar)

            game.mouvement()
            


            if player.gameCondition == True: reward = player.aiVar[4][6] * 3
            elif player.gameCondition ==None:
                reward = player.aiVar[4][6]/sqrt((dx-player1.x)**dy+player1.y**2)
            else:reward = player.aiVar[4][6]
            
            case_action[player1.y, player1.x, action_n] = case_action[player1.y, player1.x, action_n] + alpha * (reward + gamma * np.max(case_action[player.y, player.x]) - case_action[player1.y, player1.x, action_n])
            time += 1
        if epsilon > 0.1:  # réduit le pourcentage d'exploration
            epsilon /= player.aiVar[3][6] + 1
    print(player.gameCondition)
    print(case_action)
    print(time)
    
    redo(time)
    
    return time   
    

if __name__ == '__main__':
    startGame(gameMap)
    