import tkinter
from tkinter import ttk, PhotoImage, scrolledtext

import pygame as pygame
from PIL import Image, ImageTk


# View class Main Layout and Widgets of GUI
class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # parent is the TK() root window of the app
        self.parent = parent

        # can declare references to widgets that will need controller and model functionality
        # then build the widget on reference in the Build GUI method
        self.console_text_output = None
        self.selection_dropdown = None
        self.planet_selection = None

        # empty reference will be set after controller is instantiated in APP
        self.controller = None

        # Define the parent frame size
        self.WIDTH = self.winfo_screenwidth() - 100
        self.HEIGHT = self.winfo_screenheight() - 100

        # define the layout frame sizes
        # for some reason the console frame is not sizing correctly, I managed to force it by sizing the TEXT area
        # but this is a work around not a solution
        self.MENU_FRAME_WIDTH = self.WIDTH // 4
        self.CONSOLE_FRAME_HEIGHT = self.HEIGHT // 5
        self.FILTER_FRAME_WIDTH = self.WIDTH - self.MENU_FRAME_WIDTH
        self.FILTER_FRAME_HEIGHT = (self.HEIGHT - self.CONSOLE_FRAME_HEIGHT)
        self.MENU_FRAME_HEIGHT = (self.HEIGHT - self.CONSOLE_FRAME_HEIGHT)

        # image sizes for logo and mission statement
        self.LOGO_WIDTH = (self.MENU_FRAME_WIDTH // 4)
        self.LOGO_HEIGHT = (self.MENU_FRAME_HEIGHT // 8)
        self.MISSION_STATEMENT_WIDTH = (self.MENU_FRAME_WIDTH - self.LOGO_WIDTH)
        self.MISSION_STATEMENT_HEIGHT = self.MENU_FRAME_HEIGHT // 8

        # layout frames
        self.menu_frame = ttk.Frame(self, height=self.MENU_FRAME_HEIGHT, width=self.MENU_FRAME_WIDTH)
        self.filter_frame = ttk.Frame(self, height=self.FILTER_FRAME_HEIGHT, width=self.FILTER_FRAME_WIDTH)
        self.console_frame = ttk.Frame(self, height=self.CONSOLE_FRAME_HEIGHT, width=self.WIDTH)

        # Set menu background
        self.menu_image = Image.open("images/menu.jpg")
        self.menu_image = self.menu_image.resize((self.MENU_FRAME_WIDTH, self.MENU_FRAME_HEIGHT))
        self.menu_photo = ImageTk.PhotoImage(self.menu_image)
        self.menu_label = ttk.Label(self.menu_frame, image=self.menu_photo)
        # self.menu_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.menu_label.grid(row=0, column=0, sticky="nsew")

        # Set Menu Logo
        self.logo_image = Image.open("images/logo.jpg")
        self.logo_image = self.logo_image.resize((self.LOGO_WIDTH, self.LOGO_HEIGHT))
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = ttk.Label(self.menu_frame, image=self.logo_photo)
        self.logo_label.place(relx=0, rely=0, relwidth=0.26, relheight=0.128)

        # Set Mission statement background
        self.mission_statement_image = Image.open("images/mission.jpg")
        self.mission_statement_image = self.mission_statement_image.resize(
            (self.MISSION_STATEMENT_WIDTH, self.MISSION_STATEMENT_HEIGHT))
        self.mission_statement_photo = ImageTk.PhotoImage(self.mission_statement_image)
        self.mission_statement_label = ttk.Label(self.menu_frame, image=self.mission_statement_photo)
        self.mission_statement_label.place(relx=0.25, rely=0, relwidth=0.75, relheight=0.128)

        # set filter frame background
        self.filter_image = Image.open("images/galaxy.jpg")
        self.filter_image = self.filter_image.resize((self.FILTER_FRAME_WIDTH, self.FILTER_FRAME_HEIGHT))
        self.filter_photo = ImageTk.PhotoImage(self.filter_image)
        self.filter_label = ttk.Label(self.filter_frame, image=self.filter_photo)
        self.filter_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        # place child frames
        self.menu_frame.grid(row=0, column=0, rowspan=3, sticky="nsew")
        self.filter_frame.grid(row=0, column=1, rowspan=3, sticky="nsew")
        self.console_frame.grid(row=4, column=0, columnspan=2, sticky="nsew")

        # configure the grid layout of the parent tkk frame (this is the view frame not the root)
        self.grid_rowconfigure(0, weight=10)
        self.grid_rowconfigure(1, weight=10)
        self.grid_rowconfigure(2, weight=10)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=3)

        self.menu_frame.grid_columnconfigure(0, weight=1)
        self.menu_frame.grid_columnconfigure(1, weight=4)

        # further configure the console window to have its own grid
        self.console_frame.grid_columnconfigure(0, weight=8)
        self.console_frame.grid_columnconfigure(1, weight=0)
        self.console_frame.grid_columnconfigure(2, weight=2)

    # This method will draw all widgets onto the layout, must be called after instantiation and assignment of controller
    # in APP
    def draw_widgets(self):

        # ///////// CONSOLE WIDGETS ///////////////////////////////////////////////////////////////////////////////////

        # instantiate a read only not clickable text box to act as Console output
        self.console_text_output = scrolledtext.ScrolledText(self.console_frame, wrap='word', width=30, height=10,
                                                             bg='black',
                                                             fg='white',
                                                             bd=10,
                                                             relief='solid',
                                                             highlightbackground="white",
                                                             font=('Arial', 13),
                                                             takefocus=False)

        # the console text output needs to be enabled to edit the text and disabled to make it read only, This
        # will need to be done in all update methods for this widget. There may be better options then this out there
        # console_text_output.configure(state='enabled')
        self.console_text_output.insert('end', 'Welcome to SandGlass!\n')
        self.console_text_output.insert('end', 'This Is a new insert of text, this is how we do the filter text\n')
        self.console_text_output.grid(row=0, column=0, sticky="nsew")
        self.console_text_output.configure(state='disabled')

        # create the clear filters button, stylize it and attach it to controller action

        # ****** WE HAVE A CHOICE OF THIS STYLIZED GREY BUTTON THAT HIGHLIGHTS AND SUCH *****
        # clear_button_style = ttk.Style()
        # clear_button_style.configure('ClearFilterButton.TButton', font=('Arial', 20), background='#9A9AC0',
        #                              foreground='black')
        # clear_filter_button = ttk.Button(self.console_frame, text="clear Filters", style='ClearFilterButton.TButton',
        #                                  command=self.controller.clear_filters)

        # ******* OR THIS SIMPLE BUTTON THAT WE CAN CONTROL THE COLOR BUT ITS FLAT *******
        clear_filter_button = tkinter.Button(self.console_frame, text="clear Filters", bg="#9A9AC0", fg="black",
                                             font=("Arial", 20),
                                             bd=3,
                                             relief="raised",
                                             borderwidth=3,
                                             highlightthickness=0,
                                             command=self.controller.clear_filters)

        clear_filter_button.grid(row=0, column=2, sticky="nsew")

        # ///////// MENU WIDGETS ///////////////////////////////////////////////////////////////////////////////////

        # define a variable value for the selection box
        self.planet_selection = tkinter.StringVar()
        self.planet_selection.set("Select a planet")

        # build scrollable combo box using Model data
        self.selection_dropdown = ttk.Combobox(self.menu_frame, textvariable=self.planet_selection,
                                               values=self.controller.get_planets(),
                                               height=5)
        self.selection_dropdown.config(font=('Arial', 12), background="white", justify='center')
        # self.selection_dropdown['values'] = self.controller.get_planets_names()
        self.selection_dropdown.place(relx=0.5, rely=0.30, relwidth=0.8, relheight=0.05, anchor='n')

        # create quit button
        quit_button = tkinter.Button(self.menu_frame, text="Quit", bd=3, relief="raised",
                                     borderwidth=5, highlightthickness=0,
                                     highlightbackground="blue",
                                     font=("Arial", 20, "bold"),
                                     background="red",
                                     command=self.parent.destroy)

        quit_button.place(relx=0.1, rely=0.18, relwidth=0.25, relheight=0.08)

        # create calculate button
        calculate_button = tkinter.Button(self.menu_frame, text="Calculate", bd=3, relief="raised",
                                          borderwidth=5, highlightthickness=0,
                                          highlightbackground="blue",
                                          font=("Arial", 20, "bold"),
                                          background="green",
                                          command=self.create_visualization_screen
                                          )

        calculate_button.place(relx=0.1, rely=0.85, relwidth=0.8, relheight=0.05)

        # //// FILTER WIDGETS /////////////////////////////////////////////////////////////////////////////////////////

    # assign controller value to view
    def set_controller(self, controller):
        self.controller = controller

    # instantiate a pygame window for the purposes of visualization. This could change over development time
    def create_visualization_screen(self):

        # retrieve planet from model
        selected_planet = self.controller.get_selected_planet()

        # ensure planet was passed, if object does not exist stop function dont instantiate pygame
        if selected_planet is None:
            return
        else:

            # define some test data to display
            text = "Selected Planet values: Name={}, Range={}, mass={}".format(selected_planet.name,
                                                                               selected_planet.distance,
                                                                               selected_planet.mass)
            # define the window
            pygame.init()
            screen = pygame.display.set_mode((800, 800))
            pygame.display.set_caption("SandGlass Visualizer")

            # define the text for display test
            font = pygame.font.SysFont("Arial", 20)
            text_render = font.render(text, True, (255, 255, 255))

            # Pygame loop
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                screen.blit(text_render, (10, 10))
                pygame.display.flip()

            pygame.quit()
