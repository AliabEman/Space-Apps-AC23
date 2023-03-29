import tkinter
from tkinter import Tk, Label, ttk
from PIL import Image, ImageTk


class Splash:

    def __init__(self):
        # Start with a splash window
        self.splash_root = Tk()

        # Hide the title bar for the splash window
        self.splash_root.overrideredirect(True)

        # Define the splash screen frame size
        screen_width = self.splash_root.winfo_screenwidth()
        splash_width = screen_width - 100
        screen_height = self.splash_root.winfo_screenheight()
        splash_height = screen_height - 100
        splash_xposition = (screen_width - splash_width) // 2
        splash_yposition = (screen_height - splash_height) // 2
        self.splash_root.geometry(f"{splash_width}x{splash_height}+{splash_xposition}+{splash_yposition}")

        # # Add the image to the splash screen
        # self.splash_label = Label(self.splash_root)

        # Set the image for the splash screen
        self.splash_image = Image.open("images/Splash Screen.jpg")
        self.resized = self.splash_image.resize((splash_width - 100, splash_height - 100), Image.ANTIALIAS)
        self.splash_photo = ImageTk.PhotoImage(self.resized)
        self.splash_label = ttk.Label(self.splash_root, image=self.splash_photo)
        self.splash_label.pack()

        # Add the progress bar to the splash screen
        self.my_progress = ttk.Progressbar(self.splash_root, orient="horizontal", length=splash_width / 2,
                                           mode="determinate")
        self.my_progress.pack(pady=10)

        # Add the progress label to the splash screen
        self.progress_label = ttk.Label(self.splash_root, text="0%")
        self.progress_label.pack()

    # Define the function to update the progress bar
    # Needs editing to look dynamic as splash screen is "loading the App"
    def update_progress(self):
        progress = 0
        while progress <= 100:
            self.my_progress["value"] = progress
            self.progress_label.config(text=f"{progress}%")
            progress += 1
            self.splash_root.update_idletasks()

    def splash_screen_api(self):
        # Call the update_progress function after 1 second
        self.splash_root.after(1000, self.update_progress)

        # Destroy the splash screen after 3 seconds
        self.splash_root.after(3000, self.splash_root.destroy)

        self.splash_root.mainloop()

        # #Help Needed: Instead of calling a function within the function to destroy the splash screen,
        # #call the destroy function for the splash screen from main (App.py)
        #     def main_window(): #will need to eventually replace with better alternative
        #         splash_root.destroy()
        #
        #     #Call main_window function to destroy the splash
        #     splash_root.after(3000, main_window)