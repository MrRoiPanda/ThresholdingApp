from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import numpy as np


class ThresholdingApp:
    def __init__(self, root):
        self.root = root
        self.x = None  # Attribut de classe pour stocker la valeur de x

        self.root.title("Thresholding")
        self.root.geometry("1280x1080+300+150")
        self.root.resizable(width=True, height=True)

        btn_open = Button(self.root, text='Open Image', command=self.open_img)
        btn_open.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        btn_save = Button(self.root, text='Save Image',
                          command=self.save_image)
        btn_save.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.w = Scale(self.root, from_=0, to=255, orient=HORIZONTAL,
                       command=self.update_threshold)
        self.w.set(124)  # Définir la valeur par défaut du curseur
        self.w.grid(row=1, column=0, columnspan=2, padx=10, pady=10)


        self.panel = Label(self.root)
        self.panel.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Configurer le placement des boutons
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=1)

    def openfn(self):
        filename = filedialog.askopenfilename(title='open')
        return filename

    def open_img(self):
        self.x = self.openfn()
        img = Image.open(self.x)
        basewidth = 500
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), resample=Image.Resampling.LANCZOS)

        self.img_tk = ImageTk.PhotoImage(img)

        self.panel.configure(image=self.img_tk)
        self.panel.image = self.img_tk

        self.update_threshold(self.w.get())

    def update_threshold(self, value):
        if self.x is None:
            return

        img_gray = np.array(Image.open(self.x).convert("L"))
        thresh_value = int(value)
        binary_img = img_gray > thresh_value

        img = Image.fromarray(binary_img.astype(np.uint8) * 255)
        self.img_tk = ImageTk.PhotoImage(img)

        self.panel.configure(image=self.img_tk)
        self.panel.image = self.img_tk

    def save_image(self):
        if self.x is None:
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".webp", filetypes=[
                                                 ("WebP", "*.webp"), ("PNG", "*.png"), ("JPEG", "*.jpg")])
        if not save_path:
            return

        original_img = Image.open(self.x)
        img_gray = np.array(original_img.convert("L"))
        thresh_value = int(self.w.get())
        binary_img = img_gray > thresh_value
        save_img = Image.fromarray(binary_img.astype(np.uint8) * 255)

        save_img.save(save_path, "PNG")



app = ThresholdingApp(Tk())
app.root.mainloop()
