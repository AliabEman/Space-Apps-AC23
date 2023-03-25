class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def get_planets(self):
        return self.model.filteredPlanets

    def clear_filters(self):

        # test = ["test1", "test2", "test3"]

        # reset the filter planet list to the original state
        self.model.filteredPlanets = self.model.planets

        # reset the output window text, include welcome message and filter message
        self.view.console_text_output.configure(state='normal')
        self.view.console_text_output.delete(1.0, 'end')
        self.view.console_text_output.insert('end', 'Welcome to SandGlass!\n')
        self.view.console_text_output.insert('end', 'All filters have been removed, Original planet list restored\n')
        self.view.console_text_output.configure(state='disabled')

        # self.view.selection_dropdown['values'] = test
        # set the option values of the dropdown list
        self.view.selection_dropdown['values'] = self.model.filteredPlanets

        self.view.planet_selection.set("Select a planet")

    def get_planets_names(self):
        selection_dropdown_planet_names = []
        for planet in self.model.filteredPlanets:
            name = planet.name
            selection_dropdown_planet_names.append(name)

    # function to be replaced by calculation and visualization, For now it just retrieves the selected planet from the
    # list and passes some information to the Pygame window for testing purposes.
    def get_selected_planet(self):

        # grab string value from selection drop down menu
        selected_planet = self.view.selection_dropdown.get()

        if selected_planet == "Select a planet":
            self.view.console_text_output.configure(state='normal')
            self.view.console_text_output.insert('end', 'Invalid selection, please choose planet from drop down!\n')
            self.view.console_text_output.configure(state='disabled')
            return

        else:
            for planet in self.model.planets:
                if planet.name == selected_planet:
                    selected_planet = planet
                    return selected_planet

    def get_efficiency_index(self):
        return self.model.efficiency_index

    # function to set the efficiency index of the model for calculations and output a client message to console
    def submit_efficiency(self):
        efficiency_value = self.view.efficiency_slider.get()

        self.model.efficiency_index = efficiency_value

        # reset the output window text, include welcome message and filter message
        self.view.console_text_output.configure(state='normal')
        self.view.console_text_output.insert('end',
                                             'Efficiency index of calculation set to ' + str(efficiency_value) + '\n')
        self.view.console_text_output.configure(state='disabled')
