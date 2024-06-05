import tkinter as tk
from time import sleep
from mouv import Tyr
import mapList

def getWindows(r, w, s, p, m):
    global root, window, height, player, moneyLabel
    root = r
    window = w
    height = s
    player = p
    moneyLabel = m

def goGraph(p, pA):
    pA.grid(column=p.x, row=p.y)

def unlockLevel():
    if player.map == player.unlockedMap:
        player.unlockedMap += 1

def mouvementGraph():
    #print('ok')
    #print(player.nextY, player.nextX)
    for i in range(player.nextY[0]):
        player.y -= 1
        goGraph(player, playerAvatar)
        root.update()
        player.checkStat()
        sleep(0.1)
    player.nextY[0] = 0
    for i in range(player.nextX[0]):
        if player.nextX[1]:
            player.x += 1
        else:
            player.x -= 1
        goGraph(player, playerAvatar)
        root.update()
        player.checkStat()
        sleep(0.1)
    player.nextX[0] = 0
    for i in range(player.nextY[1]):
        player.y += 1
        goGraph(player, playerAvatar)
        root.update()
        player.checkStat()
        sleep(0.1)
    player.nextY[1] = 0
    
    if player.gameCondition == True:
        unlockLevel()
        player.money += 1.5 * (player.map + 1)
        moneyLabel.config(text=player.money)
        player.start()
        goGraph(player, playerAvatar)
        root.update()
    if player.gameCondition == False:
        player.start()
        goGraph(player, playerAvatar)
        root.update()
        
    
def mouvement():
    #print('ok')
    #print(player.nextY, player.nextX)
    for i in range(player.nextY[0]):
        player.y -= 1
        player.checkStat()
    player.nextY[0] = 0
    for i in range(player.nextX[0]):
        if player.nextX[1]:
            player.x += 1
        else:
            player.x -= 1
        player.checkStat()
    player.nextX[0] = 0
    for i in range(player.nextY[1]):
        player.y += 1
        player.checkStat()
    player.nextY[1] = 0

def onKeyPress(event,):
    moneyLabel.config(text=player.money)
    if player.nextY[1] == 0 and player.nextY[0] == 0 and player.nextX[0] == 0:
        match event.char:
            case 'w':
                player.Jump('sky')
                goGraph(player, playerAvatar)
            case 'e':
                player.Jump('r')
                goGraph(player, playerAvatar)
            case 'q':
                player.Jump('l')
                goGraph(player, playerAvatar)
            case 'a':
                player.goLeft()
                goGraph(player, playerAvatar)
            case 's':
                player.goDown()
                goGraph(player, playerAvatar)
            case 'd':
                player.goRight()
                goGraph(player, playerAvatar)
        mouvementGraph()
    
def clear():
    for widget in root.winfo_children():
        widget.grid_forget()
        
def nextMap():
    if player.map + 1 <= len(mapList.maps)-1 and player.unlockedMap >= player.map + 1:
        clear()
        player.map += 1
        startGame(mapList.maps[player.map])

def prevMap():
    if player.map - 1 >= 0:
        clear()
        player.map -= 1
        startGame(mapList.maps[player.map])

def startGame(gameMap = mapList.maps[0]):
    global root, window, player, playerAvatar

    getNum = len(gameMap)
    try: size = int(height // getNum)
    except: size = int(700 // getNum)
    
    for y in range(getNum):
        for x in range(getNum):
            match gameMap[y][x]:
                case 'sky':
                    tk.Canvas(root, width=size, height=size, bg='blue').grid(column=x, row=y)
                case 'floor':
                    tk.Canvas(root, width=size, height=size, bg='grey').grid(column=x, row=y)
                case 'void':
                    tk.Canvas(root, width=size, height=size, bg='black').grid(column=x, row=y)
                case 'door':
                    tk.Canvas(root, width=size, height=size, bg='yellow').grid(column=x, row=y)
                case 'start':
                    tk.Canvas(root, width=size, height=size, bg='green').grid(column=x, row=y)
        
    playerAvatar = tk.Canvas(root, width=size-10, height=size-10, bg='white')

    player.board = gameMap
    player.start()
    goGraph(player, playerAvatar)

    window.bind("<KeyPress>", onKeyPress)

    
    
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('700x700')
    window = root
    player = Tyr(mapList.maps[0])
    
    startGame(mapList.maps[2])
    
    root.mainloop()