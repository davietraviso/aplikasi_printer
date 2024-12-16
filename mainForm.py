import tkinter as tk
from utils import loadTkImage
from brand_form import BrandForm

class MainForm(tk.Frame):
    def __init__(self, parent, controller):
        self.main = controller
        self.root_width = controller.root_width
        self.root_height = controller.root_height
        tk.Frame.__init__(self, parent, background="#f5f5f5")  # Light modern background

        tk.Label(
            self,
            text="Selamat Datang\nSistem Aplikasi Manajemen Komponen Printer",
            foreground="#006799",  # Blue tone for title
            background="#f5f5f5",  # Match frame background
            font=("Arial", 20, "bold"),
            width=50,
            bd=int(self.root_width * 0.08),
            justify="center",
            wraplength=self.root_width,
            pady=20
        ).grid(row=0, columnspan=2, column=0)

        # Load images with modern scaling
        self.image = loadTkImage("./assets/motherboard.png").subsample(4, 4)
        self.image2 = loadTkImage("./assets/diskette.png").subsample(4, 4)

        # Button size adjustment
        self.button_size = int(self.root_width * 0.15)

        self.button1 = tk.Button(
            self,
            text="Komponen",
            width=self.button_size,
            height=self.button_size,
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10,
            image=self.image,
            compound="top",
            command=self.test,
            background="#4CAF50",  # Green button for a positive feel
            foreground="white",
            activebackground="#45a049",
            activeforeground="white",
            relief="flat",
            bd=0
        ).grid(row=1, column=0, pady=50)

        self.button2 = tk.Button(
            self,
            text="Input Data",
            width=self.button_size,
            height=self.button_size,
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10,
            image=self.image2,
            compound="top",
            command=self.showInputForm,
            background="#2196F3",  # Blue button for navigation
            foreground="white",
            activebackground="#1976D2",
            activeforeground="white",
            relief="flat",
            bd=0
        ).grid(row=1, column=1, pady=50)

    def test(self):
        self.main.show_frame(self.main.BrandForm)
        print("Hallo")

    def showInputForm(self):
        self.main.show_frame(self.main.InputForm)
        pass
