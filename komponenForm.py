import tkinter as tk
import json

class KomponenForm(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background="white")
        self.main = controller
        self.modelForm = self.main.frames[self.main.ModelForm]
        self.scrolled = True
        self.exitBtn = tk.Button(
            self,
            command=self.exit,
            background="white",
            text="< Keluar"
            ).place(
                x = 10,
                y = 10
                )
            
        self.judul= tk.StringVar()
        self.judul.set("Daftar Komponen\nBrand " + self.main.getFrame(1).getBrandData()["brand"] + " model " +  self.main.getFrame(3).getModelData()["model_name"])
        self.title = tk.Label(
            self, 
            textvariable=self.judul,
            background="white",
            font=("Arial", 20 , "bold")
            ).pack(
                anchor="n",
                pady=10
                )
            
        self.canvas = tk.Canvas(self, background="white")
        self.canvas.pack(side="left", fill=tk.BOTH, expand=1, anchor="n", padx=70)
        
        self.scrollBar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollBar.pack(side="right", fill=tk.Y)
        
        self.canvas.configure(yscrollcommand=self.scrollBar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.in_frame = tk.Frame(self.canvas,background="white",)
        self.canvas.create_window((0,0), window=self.in_frame, anchor="nw")
        
            
        for i in range(100):
            tk.Label(self.in_frame, text="Hallo ges david disini!", justify="left", background="white", pady=10).grid(row=i, sticky="nsew", pady=10)
       
    def update(self):
        self.judul.set("Daftar Komponen\nBrand " + self.main.getFrame(1).getBrandData()["brand"] + " model " +  self.main.getFrame(3).getModelData()["model_name"])
        for col in self.in_frame.winfo_children():
            col.destroy()

        self.stock = []
        
        try:            
            self.data = self.modelForm.getModelData()["komponen"]
            for i,komponen in enumerate(self.data):
                index = i * 4
                detail = tk.StringVar()
                detail.set("ID: " + str(komponen["serial_id"]) + " | Stok : " + str(komponen["jumlah"])  + " | Note : " + ("Stok aman !" if komponen["jumlah"] >=3 else "Stok Darurat !"))
                self.stock.append(detail)
                tk.Label(
                    self.in_frame, 
                    text="- Komponen " +str(i) , 
                    justify="left", 
                    font=("Arial", 12, "bold"),
                    background="white", 
                    pady=5
                    ).grid(
                        row=index,  
                        pady=10, 
                        padx=10,
                        sticky="w"
                        )
                    
                tk.Label(
                    self.in_frame, 
                    textvariable=self.stock[i], 
                    justify="left", 
                    background="white", 
                    ).grid(
                        row=index+1, 
                        pady=(0,20), 
                        padx=10,
                        sticky="w"
                        )
                    
                tk.Label(
                    self.in_frame,
                    text = "Tambah Komponen",
                    justify="left",
                    background="white",
                ).grid(
                    row = index + 2,
                    pady=(0,20),
                    padx = 10,
                    sticky= "w"
                )
                
                tk.Button(
                    self.in_frame,
                    text="+",
                    width=2,
                    command =lambda index=i: self.addKomponen(index, 1),
                    background="white",
                    font=("Arial", 12, "bold")
                ).grid(
                    row=index + 3,
                    pady=(0, 20),
                    padx = 10,
                    sticky="w"
                )
                
                
                tk.Button(
                    self.in_frame,
                    text="-",
                    command =lambda index=i: self.addKomponen(index, -1),
                    width=2,
                    background="white",
                    font=("Arial", 12, "bold")
                ).grid(
                    row=index + 3,
                    column=0,
                    pady=(0, 20),
                    padx = 50,
                    sticky="w"
                )
                
                
        
        except Exception as E:
            print(E)
            pass
        
    def addKomponen(self, id , value = 1):
        self.modelForm.getModelData()["komponen"][id]["jumlah"] += value
        self.stock[id].set("ID: " + str(self.data[id]["serial_id"]) + " | Stok : " + str(self.modelForm.getModelData()["komponen"][id]["jumlah"])  + " | Note : " + ("Stok aman !" if self.modelForm.getModelData()["komponen"][id]["jumlah"] >=3 else "Stok Darurat !"))

        print(self.modelForm.getModelData()["komponen"][id])
        with open('./printer.json', 'w+') as printer:
            printer.write(json.dumps(self.main.frames[self.main.BrandForm].data))
            
            
    def exit(self):
        self.main.show_frame(self.main.ModelForm)