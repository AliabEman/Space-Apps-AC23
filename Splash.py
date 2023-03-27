from tkinter import Tk, Label, ttk
from PIL import Image, ImageTk

def splash_screen_api():
    # Start with a splash window
    splash_root = Tk()

    # Hide the title bar for the splash window
    splash_root.overrideredirect(True)

    # Define the size of the frame for the splash screen
    splash_root.title("Splash Screen!")
    splash_root.geometry("700x700")

    # Add the image to the splash screen
    splash_label = Label(splash_root)

    # Set the image for the splash screen
    splash_image = Image.open("images/Splash Screen.jpg")
    resized = splash_image.resize((600, 600), Image.ANTIALIAS)
    splash_photo = ImageTk.PhotoImage(resized)
    splash_label = ttk.Label(splash_root, image=splash_photo)
    splash_label.pack()

    # Add the progress bar to the splash screen
    my_progress = ttk.Progressbar(splash_root, orient="horizontal", length=400, mode="determinate")
    my_progress.pack(pady=10)

    # Add the progress label to the splash screen
    progress_label = ttk.Label(splash_root, text="0%")
    progress_label.pack()

    # Define the function to update the progress bar
    def update_progress():
        progress = 0
        while progress <= 100:
            my_progress["value"] = progress
            progress_label.config(text=f"{progress}%")
            progress += 1
            splash_root.update_idletasks()

    # Call the update_progress function after 1 second
    splash_root.after(1000, update_progress)

    # Open the main window after 3 seconds
    def main_window():
        splash_root.destroy()

    splash_root.after(3000, main_window)

    splash_root.mainloop()
