import tkinter as tk
from tkinter import messagebox
from utils import loadTkImage
from brand_form import BrandForm
from mainForm import MainForm
from inputForm import InputForm
from modelForm import ModelForm
from addNewForm import AddNewForm
from komponenForm import KomponenForm
import json

# Fungsi untuk tombol
def on_button_click():
    messagebox.showinfo("Informasi", "Halo, ini adalah aplikasi GUI!")
    

class windows(tk.Tk):
    def resize_canvas(self,event):
        
        new_width = event.width
        new_height = event.height
        self.frame.config(width=new_width)
        
        
    def __init__(self, *args, **kwargs):
        self.BrandForm = BrandForm
        self.ModelForm = ModelForm
        self.AddNewForm = AddNewForm
        self.MainForm = MainForm
        self.InputForm = InputForm
        self.KomponenForm = KomponenForm
        self.root_width = 1050
        self.root_height = 600
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Project Akhir Data Mining")
        self.geometry(f"{self.root_width}x{self.root_height}")
        self.center_window()
        
        self.load_data()
        

        panel = tk.Frame(self, width=self.root_width, height=self.root_height)
        panel.grid()
        panel.pack(side="top", fill="both", expand=True)
        panel.grid_rowconfigure(0, weight=1)
        panel.grid_columnconfigure(0, weight=1)


        self.frames = {}
        for F in (BrandForm, MainForm, ModelForm, InputForm, AddNewForm, KomponenForm):
            frame = F(panel, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(MainForm)
        
        self.bind_all("<MouseWheel>", self._on_mousewheel)
        
        
    def _on_mousewheel(self, event):
        try:
            if self.frame.scrolled : self.frame.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except Exception as e:
            print("There is no canvas")
        
    def show_frame(self, cont):
        print("Hallo")
        self.frame = self.frames[cont]
        if cont == BrandForm : 
            self.frame.startLoad()
        if cont == ModelForm:
            self.frame.resize_listbox(None)
            self.frame.startLoad()
        if cont == KomponenForm:
            self.frame.update()
        #self.geometry(f"{self.winfo_screenwidth()}x{int(self.winfo_screenheight()* 0.9)}+0+0")
        if self.frame.update() : self.frame.update
        self.frame.tkraise()
        
    def getFrame(self, idx):
        if idx==0 : return self.frames[MainForm]
        if idx==1 : return self.frames[BrandForm]
        if idx==2 : return self.frames[InputForm]
        if idx==3 : return self.frames[ModelForm]
        if idx==4 : return self.frames[AddNewForm]
        if idx==5 : return self.frames[KomponenForm]
        
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y-50}")
        
    def load_data(self):
        with open("./printer.json", "r+") as data:
            self.data = json.load(data)        

    def save_data(self):
        with open("./printer.json", "w+") as printer:
            printer.write(json.dumps(self.data))


    def getData(self):
        return self.data


if __name__ == "__main__":
    testObj = windows()
    testObj.bind('<Configure>', testObj.resize_canvas)

    testObj.mainloop()
