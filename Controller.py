import sys


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
        test = selected_planet

    def get_filtered_planet_mass(self):
        self.inputted_mass = 0
        self.filtered_mass = []
        #print(self.model.smallest_planet.mass)
        try:
            self.inputted_mass_string = self.view.mass_input.get()
            #print(self.inputted_mass_string)
            self.inputted_mass = float(self.view.mass_input.get())
            #print("Decimal number inputted!!!")
            print(type(self.inputted_mass))
            if 0 < self.inputted_mass < sys.float_info.max and float(self.view.mass_input.get()) >= self.model.smallest_planet.mass:
                self.view.console_text_output.configure(state='normal')
                self.view.console_text_output.insert('end', '********* Mass filter applied *********\n')
                for planet in self.model.planets:
                    if planet.mass < self.inputted_mass:
                        self.filtered_mass.append([planet.name, planet.mass, planet.distance])
                        self.view.console_text_output.insert('end', ' ' + str(planet.name) + ' - ' + str(
                            planet.mass) + ' - ' + str(planet.distance) + '\n')
                # self.view.console_text_output.insert('end',"************** Printing Original Data Explicitly ************\n")
                # for planet in self.model.planets:
                #         self.filtered_mass.append([planet.name, planet.mass, planet.distance])
                #         self.view.console_text_output.insert('end', ' ' + str(planet.name) + ' - ' + str(
                #             planet.mass) + ' - ' + str(planet.distance) + '\n')
                # self.view.console_text_output.configure(state='disabled')
                if len(self.filtered_mass) == 0:
                    self.view.console_text_output.configure(state='normal')
                    self.view.console_text_output.insert('end', '********* No Results found *********\n')
                    self.view.console_text_output.configure(state='disabled')
            elif self.inputted_mass >= sys.float_info.max:
                self.view.console_text_output.configure(state='normal')
                self.view.console_text_output.insert('end', '********* Mass input exceeeds system maximums *********\n')
                self.view.console_text_output.configure(state='disabled')
            else:
                self.view.console_text_output.configure(state='normal')
                self.view.console_text_output.insert('end',
                                                     '********* Value inserted is too small ********* \n')
                self.view.console_text_output.configure(state='disabled')
        except ValueError:
            if not self.inputted_mass_string:
                self.view.console_text_output.configure(state='normal')
                self.view.console_text_output.insert('end','********* Mass Filter Cannot be Null *********\n')
                self.view.console_text_output.configure(state='disabled')
            else:
                self.view.console_text_output.configure(state='normal')
                self.view.console_text_output.insert('end', '********* Please enter a number only *********\n')
                self.view.console_text_output.configure(state='disabled')
                print("Input number only!!!!!!")



