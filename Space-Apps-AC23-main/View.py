import tkinter
from tkinter import ttk, scrolledtext

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
        self.name_input = None
        self.range_input = None
        self.mass_input = None
        self.name_submit_button = None
        self.range_submit_button = None
        self.mass_submit_button = None
        self.slider_submit_button = None
        self.efficiency_slider = None

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

        # using canvas for filter, so we can write text on it without background containers
        self.filter_canvas = tkinter.Canvas(self.filter_frame, width=self.FILTER_FRAME_WIDTH,
                                            height=self.FILTER_FRAME_HEIGHT)
        self.filter_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.filter_canvas.create_image(0, 0, image=self.filter_photo, anchor="nw")

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
        self.console_text_output.grid(row=0, column=0, sticky="nsew")
        self.console_text_output.configure(state='disabled')

        # create the clear filters button, stylize it and attach it to controller action
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
                                               height=20, state="readonly")
        self.selection_dropdown.config(font=('Arial', 12), background="white", justify='center')
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
                                          command=self.controller.start_algorithm
                                          # command=self.create_visualization_screen
                                          )

        calculate_button.place(relx=0.1, rely=0.85, relwidth=0.8, relheight=0.05)

        # //// FILTER WIDGETS /////////////////////////////////////////////////////////////////////////////////////////

        # this is super janky because python fucking blows, The spaced strings are to line up the words
        planet_name_label = "Planet Name"
        planet_mass_label = "       Planet Max Mass"
        planet_range_label = "         Planet Max Range"
        efficiency_label = "Efficiency      "

        string_height = 150
        input_width = 30
        input_font = ("Arial", 16)
        submit_font = ("Arial", 28, "bold")
        canvas_font = ("Arial", 36, "bold")
        canvas_text_color = "white"

        # spacing for filter labels
        y1 = self.FILTER_FRAME_HEIGHT / 2 - string_height
        y2 = self.FILTER_FRAME_HEIGHT / 2
        y3 = self.FILTER_FRAME_HEIGHT / 2 + string_height
        y4 = self.FILTER_FRAME_HEIGHT / 2 + (string_height * 1.8)
        input_y1 = y1 - 5
        input_y2 = y2 - 5
        input_y3 = y3 - 5

        # draw labels on canvas
        self.filter_canvas.create_text(self.FILTER_FRAME_WIDTH / 5, y1, text=planet_name_label, font=canvas_font,
                                       fill=canvas_text_color, justify="left")
        self.filter_canvas.create_text(self.FILTER_FRAME_WIDTH / 5, y2, text=planet_range_label, font=canvas_font,
                                       fill=canvas_text_color, justify="left")
        self.filter_canvas.create_text(self.FILTER_FRAME_WIDTH / 5, y3, text=planet_mass_label, font=canvas_font,
                                       fill=canvas_text_color, justify="left")
        self.filter_canvas.create_text(self.FILTER_FRAME_WIDTH / 5, y4, text=efficiency_label, font=canvas_font,
                                       fill=canvas_text_color, justify="left")

        # draw all input boxes
        self.name_input = tkinter.Entry(self.filter_canvas, font=input_font, width=input_width, justify="center")
        # self.name_input.place(x=self.FILTER_FRAME_WIDTH / 2.5 + 10, y=input_y1, anchor="w", height=40)  # Exact place
        self.name_input.place(relx=0.4, rely=0.29, relheight=0.05, relwidth=0.3)  # relative placing

        self.range_input = tkinter.Entry(self.filter_canvas, font=input_font, width=input_width, justify="center")
        # self.range_input.place(x=self.FILTER_FRAME_WIDTH / 2.5 + 10, y=input_y2, anchor="w", height=40) # Exact place
        self.range_input.place(relx=0.4, rely=0.48, relheight=0.05, relwidth=0.3)  # relative placing

        self.mass_input = tkinter.Entry(self.filter_canvas, font=input_font, width=input_width, justify="center")
        # self.mass_input.place(x=self.FILTER_FRAME_WIDTH / 2.5 + 10, y=input_y3, anchor="w",height = 40)  # Exact place
        self.mass_input.place(relx=0.4, rely=0.67, relheight=0.05, relwidth=0.3)  # relative placing

        # draw the filter input submit buttons
        self.name_submit_button = tkinter.Button(self.filter_frame, text="Submit", background="green", relief="raised",
                                                 borderwidth=5, highlightthickness=0, highlightbackground="blue",
                                                 font=submit_font, justify="center",
                                                 command=self.controller.filter_by_name)
        self.name_submit_button.place(relx=0.725, rely=0.29, relwidth=0.2, relheight=0.05)

        self.range_submit_button = tkinter.Button(self.filter_frame, text="Submit", background="green", relief="raised",
                                                  borderwidth=5, highlightthickness=0, highlightbackground="blue",
                                                  font=submit_font, justify="center",
                                                  command=self.controller.filter_by_range)
        self.range_submit_button.place(relx=0.725, rely=0.48, relwidth=0.2, relheight=0.05)

        self.mass_submit_button = tkinter.Button(self.filter_frame, text="Submit", background="green", relief="raised",
                                                 borderwidth=5, highlightthickness=0, highlightbackground="blue",
                                                 font=submit_font, justify="center")
        self.mass_submit_button.place(relx=0.725, rely=0.67, relwidth=0.2, relheight=0.05)

        self.slider_submit_button = tkinter.Button(self.filter_frame, text="Submit", background="green",
                                                   relief="raised",
                                                   borderwidth=5, highlightthickness=0, highlightbackground="blue",
                                                   font=submit_font, justify="center",
                                                   command=self.controller.submit_efficiency)
        self.slider_submit_button.place(relx=0.725, rely=0.82, relwidth=0.2, relheight=0.05)

        # draw the efficiency slider bar
        self.efficiency_slider = tkinter.Scale(self.filter_frame, from_=1, to=100, orient=tkinter.HORIZONTAL, bg="blue",
                                               font=("Arial", 12, "bold"))
        self.efficiency_slider.place(relx=0.4, rely=0.82, relwidth=0.3, relheight=0.05)

    # //// VIEW FUNCTIONS //////////////////////////////////////////////////////////////////////////////////////////////

    # assign controller value to view
    def set_controller(self, controller):
        self.controller = controller

    # instantiate a pygame window for the purposes of visualization.
    # Shows planet data and algorithm results
    # TODO add in visualization of algorithm data
    def create_visualization_screen(self, model, t, calc, starting_velocity, algorithm_results):
        # retrieve planet from model
        selected_planet = self.controller.get_selected_planet()
        efficiency_index = self.controller.get_efficiency_index()

        #  show what is available for visualizing here in the view
        #print(algorithm_results)

        # ensure planet was passed, if object does not exist stop function and do not instantiate pygame
        if selected_planet is None:
            return
        else:

            # define some test data to display
            text = "Selected Planet values:\n Name={}, Range={},mass={} Efficiency: {}\n\nAlgorithm Results\n\nExpansion Time: {}\nCalculation Time: {} Seconds\nStarting Velocity: {} km/s".format(
                selected_planet.name,
                selected_planet.distance,
                selected_planet.mass,
                efficiency_index,
                t,
                calc,
                starting_velocity)

            # define the window
            pygame.init()
            screen = pygame.display.set_mode((800, 800))
            pygame.display.set_caption("SandGlass Visualizer")

            # define the text for display test
            font = pygame.font.SysFont("Arial", 20)
            line_height = font.get_linesize()
            text_render = font.render(text, True, (255, 255, 255))

            # split the text into lines
            lines = text.split("\n")

            # Pygame loop
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                # clear the screen
                screen.fill((0, 0, 0))

                for i in range(len(lines)):
                    line_render = font.render(lines[i], True, (255, 255, 255))
                    screen.blit(line_render, (10, 10 + i * line_height))

                pygame.display.flip()

            pygame.quit()
