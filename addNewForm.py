import tkinter as tk
import json

class AddNewForm(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background="white")
        self.main = controller
        self.inputForm = controller.frames[controller.InputForm]
        self.filteredModel = []
        self.filteredKomponen = []
        
        self.exitBtn = tk.Button(
            self,
            command=self.back,
            text="< Keluar"
            ).place(
                x = 10,
                y = 10
                )
        
        self.title = tk.Label(
            self, 
            text="Servis Baru",
            background="white",
            font=("Arial", 20 , "bold")
            ).pack(
                pady=10,
                anchor="n"
                )
        
        self.canvas = tk.Canvas(self, width=controller.root_width, border=0, background="white")
        self.canvas.pack(anchor="w", pady=0)
        self.in_frame = tk.Frame(self.canvas,background="white",)
        self.canvas.create_window((200,10),window=self.in_frame, anchor="nw")
        
        
        self.header = [ 
                       "Nomor Servis", 
                       "Tanggal Terima", 
                       "Pemilik",
                       "Nama Barang",
                       "Kerusakan",
                       "Komponen yang di gunakan"
                       ]
        self.input = []
        self.fields = {}
        
        
        self.noServis = tk.StringVar()
        

        for i in range(len(self.header)):
            var = tk.StringVar()
            self.input.append(var)
            tk.Label(
                self.in_frame, 
                text=self.header[i],
                anchor="w",
                justify="left",
                width=25,
                background="white",
                font=("Arial", 12, "bold")
                ).grid(
                    pady=5,
                    column=0, 
                    row=i,
                    sticky="nsew"
                    )
            tk.Label(
                self.in_frame, 
                text=":",
                anchor="w",
                justify="left",
                background="white",
                font=("Arial", 12, "bold")
                ).grid(
                    pady=5,
                    column=1, 
                    row=i,
                    sticky="nsew"
                    )
            inputs = tk.Entry(
                self.in_frame, 
                background="white",
                width=50,
                font=("Arial", 12),
                state="readonly" if i in(0,3,5) else "normal",
                textvariable=var
                )
            inputs.grid(
                    pady=5,
                    column=2, 
                    row=i
                    )
            
        tk.Button(
            self,
            text="Tambahkan",
            command=self.save
            ).pack(
                anchor="e",
                padx=20,
                pady=(0,0)
                )
            
        self.getNewId()
        self.searchArea = tk.Canvas(self, width=controller.root_width, border=0, background="white")
        self.searchArea.pack(anchor="w", pady=10)
        self.searchFrame = tk.Frame(self.searchArea,background="white",)
        self.searchArea.create_window((0,10),window=self.searchFrame, anchor="nw")
            
            
        self.cariModel = tk.StringVar()
        self.cariModel.trace_add("write", self.searchModel) 
        tk.Label(self.searchFrame, text="Cari model printer : ", background="white").grid(row=0, column=0, sticky = "w")
        tk.Entry(self.searchFrame, textvariable=self.cariModel, background="#d6d6d6").grid(row=0, column=1,  sticky = "e")
        
        self.modelTable = tk.Canvas(self.searchFrame,border=0, width= self.main.root_width/2, background="white")
        self.modelTable.grid(row=1,columnspan=2)
        self.modelTableFrame = tk.Frame(self.modelTable,background="white",)
        self.modelTable.create_window((0,10),window=self.modelTableFrame, anchor="nw")
        
        tk.Label(self.searchFrame, text="Cari Komponen printer : ", background="white").grid(row=0, column=2, sticky = "w")
        tk.Entry(self.searchFrame).grid(row=0, column=3, sticky = "e")
        
        self.komponenTable = tk.Canvas(self.searchFrame,border=0,width= self.main.root_width/2, background="white")
        self.komponenTable.grid(row=1,column=2,columnspan=2)
        self.komponenTableFrame = tk.Frame(self.komponenTable,background="white",)
        self.komponenTable.create_window((0,10),window=self.komponenTableFrame, anchor="nw")
            
            
            
        for col_index in range(6):
            self.in_frame.columnconfigure(col_index, weight=1)
        
        self.searchModel("")
        
        
    def getNewId(self):
        ids = self.inputForm.data["data"][-1:][0]["no_servis"][1:]
        ids = "S"+("000000" + str(int(ids) + 1))[-6:]
        return self.input[0].set(ids)
    
            
    def searchModel(self,*args):
        self.filteredModel.clear()
        self.filteredKomponen.clear()
        count = 0
        for child in self.modelTableFrame.winfo_children():
            child.destroy()
        for child in self.komponenTableFrame.winfo_children():
            child.destroy()
        print(self.cariModel.get())
        for brand in self.main.data["data"]:
            for idx,model in enumerate(brand["model"]):
                if str(self.cariModel.get()).lower() in str(model["model_name"]).lower():
                    if count > 5 : return
                    tk.Button(
                        self.modelTableFrame, 
                        background="#d6d6d6", 
                        width = 20, 
                        height=3,
                        command= lambda model = model: self.setModel(model),
                        text=str(model["model_name"]).split(" ")[1:]
                        ).grid(
                            row=int(count/3),
                            column=int(count%3) ,  
                            pady=3, 
                            padx=3)
                  
                    count += 1
        self.searchKomponen(None)
    
    def searchKomponen(self, key):
        count = 0
        for child in self.komponenTableFrame.winfo_children():
            child.destroy()
        for idx,komponen in enumerate(self.filteredKomponen):
            if True:
                if count > 5 : return
                tk.Button(
                    self.komponenTableFrame, 
                    background="#d6d6d6", 
                    width = 35, 
                    height=3,
                    command= lambda data = (idx,komponen) : self.setKomponen(data[0], data[1]),
                    text=komponen["serial_id"]
                    ).grid(
                        row=int(count/2),
                        column=int(count%2) ,  
                        pady=3, 
                        padx=3)
                
                count += 1
        pass        
    
            
    def save(self):
        if sum([ state.get() == "" for state in self.input]) > 0:
            print("Tak cukup")
            return
        print([ x.get() for x in self.input])
        self.inputForm.data["data"].append({
                "no_servis" : self.input[0].get(),
                "tgl_terima" : self.input[1].get(),
                "pemilik" : self.input[2].get(),
                "nama_barang" : self.input[3].get(),
                "kerusakan" :self.input[4].get(),
                "komponen": self.input[5].get()
            })
        print(json.dumps(self.inputForm.data))
        for inputs in self.input : inputs.set("") 
        self.getNewId()
        with open('./servis.json', 'w+') as saves :
            saves.write(json.dumps(self.inputForm.data))
        self.current_model["komponen"][self.current_komponen]["jumlah"] -= 1
        self.main.save_data()
        self.main.load_data()
            
    def setModel(self, model):
        print(model)
        self.current_model = model
        self.filteredKomponen.clear()
        self.input[3].set(str(model["model_name"]))
        try:
            self.filteredKomponen = model["komponen"].copy() 
            
        except Exception as E:
            print(E)
        self.searchKomponen(self.filteredKomponen)

    def setKomponen(self, idx, komponen):
        self.current_komponen = idx
        self.input[5].set(str(komponen["serial_id"]))
        # komponen["jumlah"] -= 1

    
    def back(self):
        self.main.show_frame(self.main.InputForm)
        