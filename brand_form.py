import tkinter as tk
import json
import asyncio as aio
from threading import Thread
from utils import loadTkImage

class BrandForm(tk.Frame):
    def resize_listbox(self, event):
        self.config(width=self.main.winfo_width(), height=self.main.winfo_height())
        self.canvas.config(width=self.main.winfo_width(), height=self.main.winfo_height())
        self.in_frame.config(width=self.main.winfo_width(), height=self.main.winfo_height())
        self.canvas.anchor = "center"
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background="white")
        self.main = controller
        """Load Data Printer"""
        # with open("./printer.json", "r") as model:
        #     self.data = json.load(model)
        self.printerModel = self.main.data["data"]
        self.data = self.main.data
        tk.Button(self, 
                  background="white",
                  text="< Kembali", 
                  command=self.kembali,
                  font=("Arial", 14, "bold")
                  ).pack(padx=20,anchor="nw", pady=20)
        
        tk.Label(self, 
                 background="white",
                 text= "Pilih Brand Printer", 
                 font=("Arial", 24, "bold"), 
                 pady=10
                 ).pack(anchor="center", pady=(50,0))
        

        
        self.canvas = tk.Canvas(self,background="white", )
        self.canvas.pack(side="left", fill=tk.BOTH, expand=1, anchor="center")
        
        scrollBar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        scrollBar.pack(side="right", fill=tk.Y)
        
        self.canvas.configure(yscrollcommand=scrollBar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.in_frame = tk.Frame(self.canvas,background="white")
        self.canvas.create_window((self.winfo_screenwidth()//2,self.winfo_screenheight()*.5//2), window=self.in_frame, anchor="center")
        self.image = [tk.PhotoImage()] * len(self.printerModel)
        self.brand = 0

        for i in range(len(self.printerModel)):  # Total 20 tombol sebagai contoh
            btn = tk.Button(self.in_frame, 
                            font=("Arial", 12, "bold"),
                            command=lambda index=i: self.next(index),
                            text=self.printerModel[i]["brand"], width=100, height=100, 
                            image=self.image[i], compound="top", padx=10, pady=10)
            btn.grid(row=(i // 7) + 1, column=i % 7, padx=10, pady=20)
        
        
        self.bind("<Configure>", self.resize_listbox)
        
    def kembali(self):
        self.main.show_frame(self.main.MainForm)
        
    def startLoad(self):
        thread = Thread(target=self.loadImage)
        thread.start()
        
    def next(self, index):
        self.brand = index
        print("Printer Model dengan index" , index)
        self.main.show_frame(self.main.ModelForm)
            
    def loadImage(self):
        for i in range(len(self.printerModel)):
            print("Print")
            image = loadTkImage('./assets/motherboard.png').subsample(4,4)
            self.after(0, self.update_button_image, i, image)
            
    def update_button_image(self, index, image):
        self.image[index] = image  # Simpan referensi gambar
        buttons = self.in_frame.grid_slaves()  # Mendapatkan semua widget di grid
        buttons[len(buttons) - index - 1].configure(image=image) 
    
    def getBrandData(self):
        return self.printerModel[self.brand]
        
        
    