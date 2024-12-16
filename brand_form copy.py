import tkinter as tk

class BrandForm(tk.Frame):
    def add_item(self,canvas, frame, index):
        """Menambahkan item baru secara horizontal"""
        global current_x, current_y, max_height
        current_x = 10  # Posisi horizontal awal
        current_y = 10  # Posisi vertikal awal
        max_height = 0 

        # Ukuran item (bisa disesuaikan)
        item_width = 100
        item_height = 100
        padding = 10

        # Cek apakah item akan melebihi lebar canvas
        if current_x + item_width > self.canvas.winfo_width():
            current_x = 10  # Reset ke posisi horizontal awal
            current_y += max_height + padding  # Pindah ke baris berikutnya
            max_height = 0  # Reset tinggi maksimum untuk baris berikutnya

        # Buat item (frame dengan label dan tombol)
        item_frame = tk.Frame(self.in_frame, width=item_width, height=item_height, borderwidth=1, relief="solid")
        item_frame.place(x=current_x, y=current_y)

        # Tambahkan konten ke item
        label = tk.Label(item_frame, text=f"Printer {index + 1}", font=("Arial", 10))
        label.pack(expand=True)

        button = tk.Button(item_frame, text="Select", command=lambda i=index: print(f"Selected Printer {i + 1}"))
        button.pack()

        # Update posisi horizontal dan tinggi maksimum
        current_x += item_width + padding
        max_height = max(max_height, item_height)
    
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text= "Pilih brand printer", font=("Arial", 20, "bold"), pady=10).pack(anchor="center")
        
        self.canvas = tk.Canvas(self, background="blue")
        self.canvas.pack(side="left", fill=tk.BOTH, expand=1, anchor="center")
        scrollBar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        scrollBar.pack(side="right", fill="y")
        
        self.canvas.configure(yscrollcommand=scrollBar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.in_frame = tk.Frame(self.canvas)
        self.canvas.create_window((), window=self.in_frame, anchor="center")
        

        global current_x, current_y, max_height
        current_x = 10  # Posisi horizontal awal
        current_y = 10  # Posisi vertikal awal
        max_height = 0  # Tinggi maksimum item pada baris saat ini

        # Tambahkan item secara dinamis
        for i in range(20):  # Total 20 item sebagai contoh
            self.add_item(self.canvas, self.in_frame, i)
        
        
        
    