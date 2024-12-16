import tkinter as tk
import json

class InputForm(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background="white")
        self.main = controller
        self.loadData()
        
        # tk.Label().winfo_screenwidth
        
        # self.Navbar = tk.Frame(self).pack(side="top",anchor="center")
        self.inputBtn = tk.Button(
            self,
            command=self.addNew,
            background="white",
            text="Input Data"
            ).place(
                x = controller.root_width-100,
                y = 10
                )
            
        self.exitBtn = tk.Button(
            self,
            command=self.exit,
            background="white",
            text="< Keluar"
            ).place(
                x = 10,
                y = 10
                )
            
        
            
        self.title = tk.Label(
            self, 
            text="Data Servis",
            background="white",
            font=("Arial", 20 , "bold")
            ).pack(
                anchor="n"
                )
            
        self.canvas = tk.Canvas(self,background="white", width=controller.root_width)
        self.canvas.pack(anchor="n", pady=20)
        self.in_frame = tk.Frame(self.canvas,background="white")
        self.canvas.create_window((controller.root_width//2,10),window=self.in_frame, anchor="n")
        self.update()
        
            
    def loadData(self):
        with open('./servis.json', "r+") as servis:
            self.data = json.load(servis)
            
    
            
    def update(self):
        self.loadData()

        for child in self.in_frame.winfo_children():
            child.destroy()    
        
        tk.Label(self.in_frame, text="No.Servis", font=("Arial", 12, "bold"), background="white", borderwidth=1, relief="solid", padx=10, pady=5).grid(column=0, row=0, sticky="nsew",)
        tk.Label(self.in_frame, text="Tgl.Terima", font=("Arial", 12, "bold"), background="white", borderwidth=1, relief="solid", padx=10, pady=5).grid(column=1, row=0, sticky="nsew")
        tk.Label(self.in_frame, text="Pemilik", font=("Arial", 12, "bold"), background="white", borderwidth=1, relief="solid", padx=10, pady=5).grid(column=2, row=0, sticky="nsew")
        tk.Label(self.in_frame, text="Nama Barang", font=("Arial", 12, "bold"), background="white", borderwidth=1, relief="solid", padx=10, pady=5).grid(column=3, row=0, sticky="nsew")
        tk.Label(self.in_frame, text="Kerusakan", font=("Arial", 12, "bold"), background="white", borderwidth=1, relief="solid", padx=10, pady=5).grid(column=4, row=0, sticky="nsew")
        tk.Label(self.in_frame, text="Komponen Digunakan", font=("Arial", 12, "bold"), background="white",borderwidth=1, relief="solid", padx=10, pady=5).grid(column=5, row=0, sticky="nsew")
        tk.Label(self.in_frame,  font=("Arial", 12, "bold"), background="white",borderwidth=1, relief="solid", padx=10, pady=5).grid(column=6, row=0, sticky="nsew")
        
        for idx, servis in enumerate(self.data["data"]):
            for col, detail in enumerate(servis):
                print(detail)
                tk.Label(self.in_frame, background="white", text=str(servis[detail]), borderwidth=1, relief="solid",pady=3 ).grid(column=col, row=idx+1, sticky="nsew")
            tk.Button(
                self.in_frame, 
                background="white", 
                text="Hapus", 
                borderwidth=1, 
                relief="solid",
                command= lambda index = idx : self.hapus(index) ,
                pady=3 
                ).grid(
                    column=len(servis), 
                    row=idx+1, 
                    sticky="nsew")
            
        for col_index in range(6):
            self.in_frame.columnconfigure(col_index, weight=1)
            
            
    def hapus(self, idx):
        print(idx)
        try : 
            self.data["data"].remove(self.data["data"][idx])
            with open('./servis.json', 'w+') as servis:
                servis.write(json.dumps(self.data))
            self.update()
        except Exception as e:
            print(e)
        print(self.data)
        
       
        
    def exit(self):
        self.main.show_frame(self.main.MainForm)
        
    def addNew(self):
        self.main.show_frame(self.main.AddNewForm)
        
        