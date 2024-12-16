import tkinter as tk
import json

class InputForm(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background="#f7f9fc")
        self.main = controller
        self.loadData()
        
        self.inputBtn = tk.Button(
            self,
            command=self.addNew,
            background="#4caf50",
            fg="white",
            text="Input Data",
            font=("Arial", 12, "bold"),
            relief="flat",
            cursor="hand2"
        )
        self.inputBtn.place(
            x=controller.root_width-120,
            y=10
        )
            
        self.exitBtn = tk.Button(
            self,
            command=self.exit,
            background="#f44336",
            fg="white",
            text="< Keluar",
            font=("Arial", 12, "bold"),
            relief="flat",
            cursor="hand2"
        )
        self.exitBtn.place(
            x=10,
            y=10
        )
            
        self.title = tk.Label(
            self, 
            text="Data Servis",
            background="#f7f9fc",
            font=("Arial", 24 , "bold"),
            fg="#333"
        )
        self.title.pack(anchor="n", pady=(20, 10))
            
        self.canvas = tk.Canvas(self, background="#ffffff", width=controller.root_width, highlightthickness=0)
        self.canvas.pack(anchor="n", pady=20)
        
        self.in_frame = tk.Frame(self.canvas, background="#ffffff")
        self.canvas.create_window((controller.root_width//2,10), window=self.in_frame, anchor="n")
        
        self.update()

    def loadData(self):
        with open('./servis.json', "r+") as servis:
            self.data = json.load(servis)

    def update(self):
        self.loadData()

        for child in self.in_frame.winfo_children():
            child.destroy()

        headers = ["No.Servis", "Tgl.Terima", "Pemilik", "Nama Barang", "Kerusakan", "Komponen Digunakan", ""]
        for col_index, header in enumerate(headers):
            tk.Label(
                self.in_frame, 
                text=header, 
                font=("Arial", 12, "bold"), 
                background="#e8f0fe", 
                fg="#333",
                borderwidth=1, 
                relief="solid", 
                padx=10, 
                pady=5
            ).grid(column=col_index, row=0, sticky="nsew")

        for idx, servis in enumerate(self.data["data"]):
            for col, detail in enumerate(servis):
                tk.Label(
                    self.in_frame, 
                    background="#ffffff", 
                    text=str(servis[detail]), 
                    borderwidth=1, 
                    relief="solid",
                    fg="#555",
                    pady=3
                ).grid(column=col, row=idx+1, sticky="nsew")

            tk.Button(
                self.in_frame, 
                background="#f44336", 
                fg="white", 
                text="Hapus", 
                borderwidth=1, 
                relief="solid",
                font=("Arial", 10, "bold"),
                cursor="hand2",
                command=lambda index=idx: self.hapus(index),
                pady=3 
            ).grid(
                column=len(servis), 
                row=idx+1, 
                sticky="nsew"
            )

        for col_index in range(6):
            self.in_frame.columnconfigure(col_index, weight=1)

    def hapus(self, idx):
        try:
            self.data["data"].remove(self.data["data"][idx])
            with open('./servis.json', 'w+') as servis:
                servis.write(json.dumps(self.data))
            self.update()
        except Exception as e:
            print(e)

    def exit(self):
        self.main.show_frame(self.main.MainForm)

    def addNew(self):
        self.main.show_frame(self.main.AddNewForm)
