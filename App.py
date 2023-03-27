import tkinter as tk
import pandas

from Controller import Controller
from Model import Model
from View import View
import Splash


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("MVC_CSV_GUI DEMO")
        # currently locking the parent window since the layout does not properly resize with window
        self.resizable(False, False)

        # read all data from CSV
        nasa_data_frame = pandas.read_csv("NASA2.csv")

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


if __name__ == '__main__':
    Splash.splash_screen_api()
    app = App()
    app.mainloop()
