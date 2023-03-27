from tkinter import Tk, Label, ttk
from PIL import Image, ImageTk

def splash_screen_api():
    # Start with a splash window
    splash_root = Tk()

    # Hide the title bar for the splash window
    splash_root.overrideredirect(True)

    # Define the size of the frame for the splash screen
    splash_root.title("Splash Screen!")

    #Define the splash screen frame size
    screen_width = splash_root.winfo_screenwidth()
    splash_width = screen_width - 100
    screen_height = splash_root.winfo_screenheight()
    splash_height = screen_height - 100
    splash_xposition = (screen_width - splash_width) // 2 
    splash_yposition = (screen_height - splash_height) // 2 
    splash_root.geometry(f"{splash_width}x{splash_height}+{splash_xposition}+{splash_yposition}")

    # Add the image to the splash screen
    splash_label = Label(splash_root)

    # Set the image for the splash screen
    splash_image = Image.open("images/Splash Screen.jpg")
    resized = splash_image.resize((splash_width -100, splash_height - 100), Image.ANTIALIAS)
    splash_photo = ImageTk.PhotoImage(resized)
    splash_label = ttk.Label(splash_root, image=splash_photo)
    splash_label.pack()

    # Add the progress bar to the splash screen
    my_progress = ttk.Progressbar(splash_root, orient="horizontal", length=splash_width / 2, mode="determinate")
    my_progress.pack(pady=10)

    # Add the progress label to the splash screen
    progress_label = ttk.Label(splash_root, text="0%")
    progress_label.pack()

    # Define the function to update the progress bar
    #Needs editing to look dynamic as splash screen is "loading the App"
    def update_progress():
        progress = 0
        while progress <= 100:
            my_progress["value"] = progress
            progress_label.config(text=f"{progress}%")
            progress += 1
            splash_root.update_idletasks()

    # Call the update_progress function after 1 second
    splash_root.after(1000, update_progress)

#Help Needed: Instead of calling a function within the function to destroy the splash screen,
#call the destroy function for the splash screen from main (App.py) 
    def main_window(): #will need to eventually replace with better alternative
        splash_root.destroy()

    #Call main_window function to destroy the splash
    splash_root.after(3000, main_window)

    splash_root.mainloop()
