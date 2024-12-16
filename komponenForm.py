import tkinter as tk
import json

class KomponenForm(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background="#f5f5f5")  # Updated background for modern aesthetic
        self.main = controller
        self.modelForm = self.main.frames[self.main.ModelForm]
        self.scrolled = True
        
        self.exitBtn = tk.Button(
            self,
            command=self.exit,
            text="< Keluar",
            background="#ff6666",  # Highlighted exit button
            font=("Arial", 12, "bold"),
            foreground="white",
            activebackground="#ff4d4d",
            activeforeground="white",
            relief="flat",
            bd=0
        ).place(
            x=10,
            y=10
        )
        
        self.judul = tk.StringVar()
        self.judul.set(
            f"Daftar Komponen\nBrand {self.main.getFrame(1).getBrandData()['brand']} model {self.main.getFrame(3).getModelData()['model_name']}"
        )
        self.title = tk.Label(
            self,
            textvariable=self.judul,
            background="#f5f5f5",
            font=("Arial", 20, "bold"),
            foreground="#333"
        ).pack(
            anchor="n",
            pady=10
        )
        
        self.canvas = tk.Canvas(self, background="#f5f5f5", highlightthickness=0)
        self.canvas.pack(side="left", fill=tk.BOTH, expand=1, anchor="n", padx=70)
        
        self.scrollBar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollBar.pack(side="right", fill=tk.Y)
        
        self.canvas.configure(yscrollcommand=self.scrollBar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.in_frame = tk.Frame(self.canvas, background="#ffffff", relief="groove", bd=2)
        self.canvas.create_window((0, 0), window=self.in_frame, anchor="nw")
        
        for i in range(100):
            tk.Label(
                self.in_frame,
                text="Hallo ges david disini!",
                justify="left",
                background="#ffffff",
                font=("Arial", 12),
                pady=10
            ).grid(row=i, sticky="nsew", pady=10)

    def update(self):
        self.judul.set(
            f"Daftar Komponen\nBrand {self.main.getFrame(1).getBrandData()['brand']} model {self.main.getFrame(3).getModelData()['model_name']}"
        )
        for col in self.in_frame.winfo_children():
            col.destroy()

        self.stock = []
        
        try:            
            self.data = self.modelForm.getModelData()["komponen"]
            for i, komponen in enumerate(self.data):
                index = i * 4
                detail = tk.StringVar()
                detail.set(
                    f"ID: {komponen['serial_id']} | Stok : {komponen['jumlah']} | Note : "
                    f"{'Stok aman !' if komponen['jumlah'] >= 3 else 'Stok Darurat !'}"
                )
                self.stock.append(detail)
                
                tk.Label(
                    self.in_frame,
                    text=f"- Komponen {i}",
                    justify="left",
                    font=("Arial", 12, "bold"),
                    background="#ffffff",
                    foreground="#333",
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
                    background="#ffffff",
                    font=("Arial", 10),
                    foreground="#555"
                ).grid(
                    row=index + 1,
                    pady=(0, 20),
                    padx=10,
                    sticky="w"
                )
                
                tk.Label(
                    self.in_frame,
                    text="Tambah Komponen",
                    justify="left",
                    background="#ffffff",
                    font=("Arial", 10, "italic"),
                    foreground="#777"
                ).grid(
                    row=index + 2,
                    pady=(0, 20),
                    padx=10,
                    sticky="w"
                )
                
                tk.Button(
                    self.in_frame,
                    text="+",
                    width=2,
                    command=lambda index=i: self.addKomponen(index, 1),
                    background="#4CAF50",  # Green button for adding
                    font=("Arial", 12, "bold"),
                    foreground="white",
                    activebackground="#45a049",
                    activeforeground="white",
                    relief="flat"
                ).grid(
                    row=index + 3,
                    pady=(0, 20),
                    padx=10,
                    sticky="w"
                )
                
                tk.Button(
                    self.in_frame,
                    text="-",
                    command=lambda index=i: self.addKomponen(index, -1),
                    width=2,
                    background="#ff6666",  # Red button for subtracting
                    font=("Arial", 12, "bold"),
                    foreground="white",
                    activebackground="#ff4d4d",
                    activeforeground="white",
                    relief="flat"
                ).grid(
                    row=index + 3,
                    column=0,
                    pady=(0, 20),
                    padx=50,
                    sticky="w"
                )
        except Exception as e:
            print(e)

    def addKomponen(self, id, value=1):
        self.modelForm.getModelData()["komponen"][id]["jumlah"] += value
        self.stock[id].set(
            f"ID: {self.data[id]['serial_id']} | Stok : {self.modelForm.getModelData()['komponen'][id]['jumlah']} | Note : "
            f"{'Stok aman !' if self.modelForm.getModelData()['komponen'][id]['jumlah'] >= 3 else 'Stok Darurat !'}"
        )
        print(self.modelForm.getModelData()["komponen"][id])
        with open('./printer.json', 'w+') as printer:
            printer.write(json.dumps(self.main.frames[self.main.BrandForm].data))

    def exit(self):
        self.main.show_frame(self.main.ModelForm)
