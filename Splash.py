# YouTube Reference Video: https://youtu.be/LTVvHObxc4

#from tkinter import ttk, PhotoImage, Tk, Label, mainloop
from tkinter import *
from PIL import Image, ImageTk

#Start with a splash window
splash_root = Tk()
splash_root.title("Splash Screen!")
splash_root.geometry("300x200")

#Timing the splash screen
splash_label = Label(splash_root, text="Splash Screen!", font=("Arial",18))
splash_label.pack(pady=20)

#Setting Image for Splash Screen
#splash_root.splash_image = Image.open("images/Splash Screen.jpg")
#splash_root.splash_image = splash_root.splash_image.resize((300, 200))
#splash_root.splash_photo = ImageTk.PhotoImage(splash_root.splash_image)
#splash_label = splash_label.Label(splash_root.splash_frame, image=splash_root.splash_photo)

def main_window():
    splash_root.destroy()
    root = Tk()
    root.title("Splash Screen")
    root.geometry("500x550")

#Splash Screen Timer
splash_root.after(4000, main_window)

mainloop()