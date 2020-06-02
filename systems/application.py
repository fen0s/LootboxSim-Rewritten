import tkinter as tk
from PIL import ImageTk, Image
import random
from systems.engine import Engine
from systems.inventory import Inventory
from data.prefstuff import quality_colors 
from winsound import PlaySound, SND_FILENAME
class Application():
    def __init__(self, engine, inventory):
        self.root = tk.Tk()
        self.engine = engine
        self.inventory = inventory
        
        imgbg_path = './imgs/bg.png'
        imglootbox_path = './imgs/lbox.png'
        bg = ImageTk.PhotoImage(Image.open(imgbg_path))
        lbimage = ImageTk.PhotoImage(Image.open(imglootbox_path).resize(size=(170, 150)))
        
        #background and lootbox image placing
        panel = tk.Label(self.root, image=bg)
        panel.place(relx=0.89, rely=0.07, anchor=tk.CENTER)
        img = tk.Label(self.root, image = lbimage)
        img.place(relx=0.5, rely=0.5,anchor=tk.CENTER)
        
        self.root.geometry('600x400')
        
        #statistics text
        self.stats = tk.Label(self.root,
                    text = self.engine.statistics,
                    width=17, height=3,
                    bg='#e07ef9',
                    font='arial 10')
        self.stats.place(relx=0.89, rely=0.07, anchor=tk.CENTER)
        
        #lootbox opening button
        self.open_button = tk.Button(self.root,
                    text = f'Buy lootbox for ${self.engine.price}',
                    width=16, height=2,
                    bg = "#bd7ad8", fg='#6900b6', font='arial 13')
        self.open_button.place(relx=0.5, rely=0.9, anchor=tk.S)
        self.open_button.bind('<Button-1>', self.open_lootbox)
        
        #inventory window button
        invbutton = tk.Button(self.root,
                        text = 'Open inventory',
                        width=20, height = 1,
                        bg = "#e07ef9", fg='purple', font='arial 10')
        
        invbutton.bind('<Button-1>', self.openinv)
        invbutton.place(relx=0.1, rely=0.02, anchor=tk.CENTER)
        
        #balance label
        self.balancelabel = tk.Label(self.root,
                            text=engine.balancestr,
                            width=20, height=1,
                            bg='#bd7ad8', fg='#59d327', font='arial 10')
        self.balancelabel.place(relx = 0.1, rely = 0.97, anchor = tk.CENTER)
        
        self.root.mainloop()
    
    def update_statistics(self):
        self.stats.configure(text=self.engine.statistics)
    
    def update_balance(self):
        self.balancelabel.configure(text=str(self.engine.balancestr))
    
    def open_lootbox(self, event):
            if self.open_button['state'] == tk.NORMAL:
                self.open_button['state'] = tk.DISABLED
                
                self.engine.opened += 1
                self.engine.spent += self.engine.price
                self.engine.balance -= self.engine.price
                
                self.update_statistics()
                self.update_balance()
                self.root.update()
                
                #lootbox opening window
                lbwindow = tk.Toplevel()
                lbwindow.geometry('200x100')
                lbwindtext = tk.Label(lbwindow,
                                text='Opening lootbox... \nPlease wait...',
                                width=17, height=2,
                                font='arial 10')
                lbwindtext.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
                lbwindow.after(1300, lambda: self.get_loot(lbwindow))

    def get_loot(self, opening_window):
                self.open_button['state'] = tk.NORMAL
                opening_window.destroy()

                lootwindow = tk.Toplevel()
                lootwindow.geometry('600x400')
                lootlb = tk.Label(lootwindow,
                            text='Congratulations! You got...',
                            width=20, height=3,
                            font='arial 14')
                lootlb.pack(side='top')
                
                loot = self.inventory.generate_loot()
                self.inventory.add_to_inventory(loot[1], loot[2])
                tier = loot[0]
                item = loot[1]
                
                #loot text
                loot = tk.Label(lootwindow,
                            text=item,
                            width=35, height=2,
                            fg = quality_colors.get(tier),
                            font='arial 19')
                #quality text
                qual = tk.Label(lootwindow,
                            text=tier.upper() + ' Quality!',
                            fg=quality_colors.get(tier),
                            width=20, height=2,
                            font='arial 22')
                loot.place(rely=0.9, relx=0.5, anchor=tk.CENTER)
                qual.place(rely=0.5, relx=0.5, anchor=tk.CENTER)
                
                
                PlaySound('l.wav', SND_FILENAME)

    def sell(self, event):
        self.inventory.sell_inventory()
        
        self.update_balance()
        self.update_statistics()
        self.root.update()
        
        #just opens "items sold" window to notify user that the thing gone successfuly
        sold = tk.Toplevel()
        sold.geometry('50x50')
        soldlabel = tk.Label(sold,
                        text='Items sold!',
                        width=10, height=1,
                        font='arial 10')
        soldlabel.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def openinv(self, event):
        inv_window = tk.Toplevel()
        inv_window.geometry('1000x500')
        
        inv_title = tk.Label(inv_window,
                        text='YOUR ITEMS:',
                        width = 30, height = 2,
                        font='arial 22')
        inv_title.pack(side='top')
        
        itemlist_label = tk.Label(inv_window,
                            text=self.inventory.all_items,
                            width=100, height=40,
                            font='arial 14')
        itemlist_label.pack(side='top')
        
        sellbutton = tk.Button(inv_window,
                            text=f'Sell items for price of {self.inventory.inventory_price}$?',
                            width=40, height=1,
                            font='arial 15')
        sellbutton.place(relx=0.5, rely=0.95, anchor=tk.CENTER)
        sellbutton.bind('<Button-1>', self.sell)