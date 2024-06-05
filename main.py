import game
import gameIA
import frame_plus
import tkinter as tk
from mouv import Tyr

def funcSlider(v, i):
    player.aiVar[i][6] = float(v)
    print(player.aiVar)
    
def upSlider(i):
    if player.money >=2 ** player.aiVar[i][3] * player.aiVar[i][5]:
        player.money -= player.aiVar[i][3] * player.aiVar[i][5]
        player.aiVar[i][3] += 1
        player.aiVar[i][1] += player.aiVar[i][4]
        sl[i].config(to=player.aiVar[i][1])
        up[i].config(text=f"upgrade level {int(player.aiVar[i][3] + 1)} ({2 ** player.aiVar[i][3] * player.aiVar[i][5]} coin)")
        moneyLabel.config(text=player.money)
        print(player.aiVar)

def fillSlider():
    global moneyLabel, sl, bu, up
    
    t = []
    sl = []
    bu = []
    up = []
    
    for i in range(0,5):
        b = tk.Button(top_left, text=f" {player.aiVar[i][0]}", command = quit)
        b.configure(width = 10)
        b.place(x=10, y=10 + (i+1)*55)
        bu.append(b)
        label = tk.Label(top_left, text=f"upgrade level {int(player.aiVar[i][3] + 1)} ({2 ** player.aiVar[i][3] * player.aiVar[i][5]} coin)")
        label.configure(width = 22)
        label.place(x=130, y=15 + (i+1)*55)
        up.append(label)
        def slider_changed(value):  
            v=value
            
        current_value = tk.DoubleVar()
        slider = tk.Scale(
            top_left,
            from_=0,
            to=player.aiVar[i][1],
            digit=3,
            resolution = player.aiVar[i][2],
            orient='horizontal',
            variable=current_value,
            command=slider_changed
        )
        sl.append(slider)
        slider.configure(width = 10)
        slider.place(x=300, y=5 + (i+1)*55)

    bu[0].configure(command=lambda : upSlider(0))
    bu[1].configure(command=lambda : upSlider(1))
    bu[2].configure(command=lambda : upSlider(2))
    bu[3].configure(command=lambda : upSlider(3))
    bu[4].configure(command=lambda : upSlider(4))
        
    sl[0].configure(command=lambda value: funcSlider(value, 0))
    sl[1].configure(command=lambda value: funcSlider(value, 1))
    sl[2].configure(command=lambda value: funcSlider(value, 2))
    sl[3].configure(command=lambda value: funcSlider(value, 3))
    sl[4].configure(command=lambda value: funcSlider(value, 4))
    
    moneyLabel = tk.Label(top_left, text=player.money)
    moneyLabel.place(x=10, y=10)
    print(moneyLabel)
        
def fill():
    bouton_quitter = tk.Button(bot_left, text='quit', command=quit)
    bouton_quitter.configure(width = 10)
    bouton_quitter_win = bot_left.create_window(10, 10, anchor='nw', window=bouton_quitter)
    
    bouton_previous = tk.Button(bot_left, text='previous level', command=game.prevMap)
    bouton_previous.configure(width = 10)
    bouton_previous_win = bot_left.create_window(10, 55, anchor='nw', window=bouton_previous)
    
    bouton_next = tk.Button(bot_left, text='next level', command=game.nextMap)
    bouton_next.configure(width = 10)
    bouton_next_win = bot_left.create_window(10, 100, anchor='nw', window=bouton_next)
    
    bouton_train = tk.Button(bot_left, text='train', command= lambda : exec("gameIA.ia_train(player)\nmoneyLabel.config(text=player.money)"))
    bouton_train.configure(width = 10)
    bouton_train_win = bot_left.create_window(10, 145, anchor='nw', window=bouton_train)
    
        
def start():
    global top_left, bot_left, player
    
    root = tk.Tk()
    root.title('The World Of Idlia')
    root.attributes('-fullscreen', True)
    
    player = Tyr()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    top_left = tk.Canvas(master=root,bg='#b5f7f7', height=screen_height*0.7, width=screen_width-screen_height -15)
    top_left.grid(column=0, row=0)
    fillSlider()
    
    bot_left = tk.Canvas(master=root, bg='#b442b4', height=screen_height*0.3, width=screen_width-screen_height - 15)
    bot_left.grid(column=0, row=1)
    fill()
    
    gameBoard = tk.Canvas(root, width=screen_height, height=screen_height)
    gameBoard.grid(column=1, row=0, rowspan=2)
    game.getWindows(gameBoard, root, screen_height, player, moneyLabel)
    game.startGame()

    root.mainloop()
    
start()