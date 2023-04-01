import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pandas
import multiprocessing

from Controller import Controller
from Model import Model
from View import View


class Splash(tk.Toplevel):

    def __init__(self, root):
        super().__init__()

        # Hide the title bar for the splash window
        self.overrideredirect(True)

        # Define the splash screen frame size
        screen_width = self.winfo_screenwidth()
        splash_width = screen_width - 100
        screen_height = self.winfo_screenheight()
        splash_height = screen_height - 100
        splash_xposition = (screen_width - splash_width) // 2
        splash_yposition = (screen_height - splash_height) // 2
        self.geometry(f"{splash_width}x{splash_height}+{splash_xposition}+{splash_yposition}")
        self.progress = 0

        # # Add the image to the splash screen
        # self.splash_label = Label(self.splash_root)

        # Set the image for the splash screen
        self.splash_image = Image.open("images/Splash Screen.jpg")
        self.resized = self.splash_image.resize((splash_width - 100, splash_height - 100))
        self.splash_photo = ImageTk.PhotoImage(self.resized)
        self.splash_label = ttk.Label(self, image=self.splash_photo)
        self.splash_label.pack()

        # Add the progress bar to the splash screen
        self.my_progress = ttk.Progressbar(self, orient="horizontal", length=splash_width / 2,
                                           mode="determinate")
        self.my_progress.pack(pady=10)

        # Add the progress label to the splash screen
        self.progress_label = ttk.Label(self, text="0%")
        self.progress_label.pack()

    # Define the function to update the progress bar
    # Needs editing to look dynamic as splash screen is "loading the App"
    def update_progress(self):

        if self.progress <= 101:
            self.my_progress["value"] = self.progress
            self.progress_label.config(text=f"{self.progress}%")
            self.progress += 2
            self.after(1)

    def destroy_splash_screen(self):
        self.destroy()


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.splash = None
        self.start_up_app()

        self.title("MVC_CSV_GUI DEMO")
        # currently locking the parent window since the layout does not properly resize with window
        self.resizable(False, False)

        self.mainloop()

    def start_up_app(self):
        self.show_splash_screen()

        # load db in separate process
        process_startup = multiprocessing.Process(target=App.startup_process(self))
        process_startup.start()

        while process_startup.is_alive():
            self.splash.update()
            self.splash.update_progress()

        self.splash.my_progress["value"] = 100
        self.splash.progress_label.config(text="100")
        self.after(1000)
        self.remove_splash_screen()

    def show_splash_screen(self):
        self.withdraw()
        self.splash = Splash(self)

    @staticmethod
    def startup_process(self):
        # read all data from CSV
        nasa_data_frame = pandas.read_csv("NASA_PRODUCTION.csv")

        # convert dataframe to data dictionary to be passed to model constructor
        planet_data = nasa_data_frame.to_dict('records')
        model = Model(planet_data)

        # initialize the parent ttk frame which will have our 3 frame layout attached
        view = View(self)

        # draw the view onto the Parent window to take up the full space
        view.grid(row=0, column=0, sticky="nsew")

        controller = Controller(model, view)

        # assign controller to the view ( Not the best practice but it works for now )
        view.set_controller(controller)

        # draw the GUI on top of the layout, Must come after the controller in oder to assign values to widgets from
        # model
        view.draw_widgets()

    def remove_splash_screen(self):
        self.splash.destroy_splash_screen()
        del self.splash
        self.deiconify()


if __name__ == '__main__':
    App()
