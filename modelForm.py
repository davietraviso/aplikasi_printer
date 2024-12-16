import tkinter as tk
import json
import asyncio as aio
from threading import Thread
from utils import loadTkImage

class ModelForm(tk.Frame):
    def resize_listbox(self, event):
        width = self.main.winfo_width() * 0.9
        height = self.main.winfo_height()

        self.config(width=width, height=height)
        self.canvas.config(width=width - 50, height=height)

        self.in_frame.update_idletasks()  # Ensure all elements are updated
        self.in_frame.config(width=width, height=self.in_frame.winfo_reqheight())

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.scrollBar.pack(side="right", fill=tk.Y)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background="#f5f5f5")  # Light modern background
        self.main = controller
        self.brandForm = self.main.frames[self.main.BrandForm]
        self.model = 0
        self.scrolled = True

        with open("./printer.json", "r") as model:
            self.printerModel = json.load(model)["data"][self.main.frames[self.main.BrandForm].brand]["model"]

        self.title = tk.Label(
            self,
            background="#f5f5f5",
            text="Pilih Model Printer",
            font=("Arial", 20, "bold"),
            pady=10,
            foreground="#006799"
        )
        self.title.pack(anchor="center", pady=50)

        tk.Button(
            self,
            background="#2196F3",  # Blue button for navigation
            foreground="white",
            activebackground="#1976D2",
            activeforeground="white",
            font=("Arial", 10, "bold"),
            text="< Kembali",
            command=self.backToBrand,
            padx=20,
            relief="flat",
            bd=0
        ).pack(anchor="w", padx=70)

        self.canvas = tk.Canvas(self, background="#ffffff", highlightthickness=0)  # White background for clarity
        self.canvas.pack(side="left", fill=tk.BOTH, expand=1, anchor="n", padx=70)

        self.scrollBar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollBar.pack(side="right", fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollBar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.in_frame = tk.Frame(self.canvas, background="#ffffff")
        self.canvas.create_window((0, 0), window=self.in_frame, anchor="nw")

        self.image = [tk.PhotoImage()] * len(self.printerModel)
        self.btn = [tk.Button()] * len(self.printerModel)

        tk.Button(
            self.in_frame,
            font=("Arial", 10, "bold"),
            text="test",
            width=100, height=100,
            compound="top",
            padx=10, pady=10
        ).grid(column=0, row=0)

        self.bind("<Configure>", self.resize_listbox)

    def backToBrand(self):
        self.main.show_frame(self.main.BrandForm)

    def loadImage(self):
        self.title.config(text="Pilih Model Printer - " + self.brandForm.getBrandData()["brand"])
        for btn in self.in_frame.winfo_children():
            btn.destroy()

        self.image = [tk.PhotoImage()] * len(self.brandForm.getBrandData()["model"])
        self.btn = [tk.Button()] * len(self.brandForm.getBrandData()["model"])
        self.canvas.xview_scroll(0, "units")

        for i in range(len(self.brandForm.getBrandData()["model"])):
            wrapped = self.wrap_text(self.brandForm.getBrandData()["model"][i]["model_name"], 10)
            self.btn[i] = tk.Button(
                self.in_frame,
                font=("Arial", 10, "bold"),
                text=wrapped,
                command=lambda index=i: self.displayComponent(index),
                width=100, height=100,
                image=self.image[i],
                background="#4CAF50",  # Green for a positive feel
                foreground="white",
                activebackground="#45a049",
                activeforeground="white",
                compound="top",
                padx=10, pady=10,
                relief="flat",
                bd=0
            )
            self.btn[i].grid(row=(i // 6) + 1, column=i % 6, padx=10, pady=20)

        for i in range(len(self.brandForm.getBrandData()["model"])):
            image = loadTkImage('./assets/motherboard.png').subsample(4, 4)
            self.after(0, self.update_button_image, i, image)
        for col_index in range(6):
            self.in_frame.columnconfigure(col_index, weight=1)
        self.resize_listbox(None)

    def getModelData(self):
        if not self.brandForm.getBrandData()["model"][self.model]:
            return None
        return self.brandForm.getBrandData()["model"][self.model]

    def startLoad(self):
        thread = Thread(target=self.loadImage)
        thread.start()

    def update_button_image(self, index, image):
        self.image[index] = image  # Save image reference
        self.btn[index].configure(image=image)

    def displayComponent(self, index):
        self.model = index
        self.main.show_frame(self.main.KomponenForm)

    def wrap_text(self, text, width):
        words = text.split()
        wrapped_text = ""
        line = ""
        for word in words:
            if len(line) + len(word) + 1 <= width:
                line += word + " "
            else:
                wrapped_text += line.strip() + "\n"
                line = word + " "
        wrapped_text += line.strip()
        return wrapped_text
