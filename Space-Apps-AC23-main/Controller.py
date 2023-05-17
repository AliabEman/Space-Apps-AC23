import re


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def get_planets(self):
        return self.model.filteredPlanets

    def start_algorithm(self):
        print("validate button modification")
        selected_planet = self.get_selected_planet()
        self.model.run_algorithm(self, selected_planet)

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

    #  function to take in a value in years, and convert it in a way appropriate to display
    #  returns string holding time with appropriate units
    @staticmethod
    def convert_time_unit(temp, time_in_years):
        if time_in_years < 1:
            time_in_months = time_in_years * 12
            if time_in_months < 1:
                time_in_days = time_in_months * 30
                if time_in_days < 1:
                    time_in_hours = time_in_days * 24
                    if time_in_hours < 1:
                        time_in_seconds = time_in_hours * 3600
                        return f"{time_in_seconds:.5f} seconds"
                    else:
                        return f"{time_in_hours:.5f} hours"
                else:
                    return f"{time_in_days:.5f} days"
            else:
                return f"{time_in_months:.5f} months"
        elif 1 <= time_in_years < 1000:
            return f"{time_in_years:.5f} years"
        elif 1000 <= time_in_years < 1000000:
            time_in_thousands_of_years = time_in_years / 1000
            return f"{time_in_thousands_of_years:.5f} thousand years"
        elif 1000000 <= time_in_years < 1000000000:
            time_in_millions_of_years = time_in_years / 1000000
            return f"{time_in_millions_of_years:.5f} million years"
        elif time_in_years >= 1000000000:
            time_in_billions_of_years = time_in_years / 1000000000
            return f"{time_in_billions_of_years:.5f} billion years"
        elif time_in_years >= 1000000000000:
            time_in_trillions_of_years = time_in_years / 1000000000000
            return f"{time_in_trillions_of_years:.5f} trillion years"

    # function to be replaced by calculation and visualization, For now it just retrieves the selected planet from the
    # list and passes some information to the Pygame window for testing purposes.
    def get_selected_planet(self):

        # grab string value from selection drop down menu
        selected_planet = self.view.selection_dropdown.get()

        if selected_planet == "Select a planet" or selected_planet == "No results found":
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

    # Function to filter the list of planets based on the name entered by the user
    def filter_by_name(self):
        # Get the name that the user wants to search for
        searchName = self.view.name_input.get().strip().lower()

        # If the user submits without entering a name
        if searchName == "":
            self.view.console_text_output.configure(state='normal')
            self.view.console_text_output.insert('end',
                                                 'Name filter submitted with no text entered\n')
            self.view.console_text_output.configure(state='disabled')
            # Clear the input field
            self.view.name_input.delete(0, 'end')
            return
        # The longest name in the data is 29 characters (including spaces)
        if (len(searchName) > 29):
            self.view.console_text_output.configure(state='normal')
            self.view.console_text_output.insert('end',
                                                 'No results found\n')
            self.view.console_text_output.configure(state='disabled')
            # Clear the input field
            self.view.name_input.delete(0, 'end')
            # Set the drop-down list to empty
            self.view.selection_dropdown.configure(values=[])
            self.view.planet_selection.set("No results found")
            return

        # Check the dataset for the specified string
        else:
            tempPlanets = [x for x in self.model.planets if searchName in x.name.lower()]

            if (len(tempPlanets) == 0):
                self.view.console_text_output.configure(state='normal')
                self.view.console_text_output.insert('end',
                                                     'Name filter applied, no results containing \"' + searchName + '\" found\n')
                self.view.console_text_output.configure(state='disabled')
                # Clear the input field
                self.view.name_input.delete(0, 'end')
                # Set the drop-down list to the filtered list
                self.view.selection_dropdown.configure(values=tempPlanets)
                self.view.planet_selection.set("No results found")
                return
            else:
                self.model.filteredPlanets = tempPlanets
                self.view.console_text_output.configure(state='normal')
                if (len(tempPlanets) == 1):
                    self.view.console_text_output.insert('end',
                                                         'Name filter applied, ' + str(
                                                             len(tempPlanets)) + ' result containing \"' + searchName + '\" found\n')
                    # If there is only one result, set the selected planet to that result
                    self.view.planet_selection.set(tempPlanets[0])
                else:
                    self.view.console_text_output.insert('end',
                                                         'Name filter applied, ' + str(
                                                             len(tempPlanets)) + ' results containing \"' + searchName + '\" found\n')
                    self.view.planet_selection.set("Select a planet")
                self.view.console_text_output.configure(state='disabled')
                # Clear the input field
                self.view.name_input.delete(0, 'end')
                # Set the drop-down list to the filtered list
                self.view.selection_dropdown.configure(values=tempPlanets)

    def filter_by_range(self):
        # Get the mass value  that the user wants to search for
        rangeValue = self.view.range_input.get()

        # If the user submits entering  empty
        if rangeValue == "":
            self.view.console_text_output.configure(state='normal')
            self.view.console_text_output.insert('end', 'Range filter submitted with no data entered\n')
            self.view.console_text_output.configure(state='disabled')
            self.view.mass_input.delete(0, 'end')
            return

        # if re.match('^[0-9\.]*$', rangeValue):
        # Check if rangeValue is a valid float value
        # if re.match('^[0-9]*\.?[0-9]+$', rangeValue):

        # This regular expression pattern checks if the rangeValue variable contains a valid floating point number.
        if re.match(r'^\d+\.?\d*$', rangeValue):
            rangeValue = float(rangeValue)
            self.view.mass_input.delete(0, 'end')
            self.view.console_text_output.configure(state='normal')
            self.view.console_text_output.insert('end', 'Valid number entered!: ' + str(rangeValue) + '\n')
            self.view.console_text_output.configure(state='disabled')

            tempPlanetsRange = [x for x in self.model.planets if float(x.distance) == float(rangeValue)]
            if (len(tempPlanetsRange) == 0):
                self.view.console_text_output.configure(state='normal')
                self.view.console_text_output.insert('end',
                                                     'Did not find any matches for range: ' + str(rangeValue) + '\n')
                self.view.console_text_output.configure(state='disabled')
            else:
                self.model.filteredPlanets = tempPlanetsRange
                self.view.console_text_output.configure(state='normal')
                if (len(tempPlanetsRange) == 1):
                    self.view.console_text_output.insert('end', 'Range filter applied, ' + str(
                        len(tempPlanetsRange)) + ' result containing \"' + str(rangeValue) + '\" found\n')
                else:
                    self.view.console_text_output.insert('end', 'Range filter applied, ' + str(
                        len(tempPlanetsRange)) + ' results containing \"' + str(rangeValue) + '\" found\n')
                self.view.console_text_output.configure(state='disabled')
                # Clear the input field
                self.view.name_input.delete(0, 'end')
                # Set the drop-down list to the filtered list
                self.view.selection_dropdown.configure(values=tempPlanetsRange)
                # Check if the entered mass matches exactly. 
                # If it does, set the selected drop-down list item to the matched mass
                matches = False
                for planet in tempPlanetsRange:
                    if (planet.mass == rangeValue):
                        self.view.planet_selection.set(planet.name)
                        matches = True
                        break
                # If it doesn't match, set the selected drop-down list item to the default
                if (matches == False):
                    self.view.planet_selection.set("Select a planet")
        else:
            # The input is not a valid number, display an error message
            self.view.console_text_output.configure(state='normal')
            self.view.console_text_output.insert('end', 'Incorrect datatype please enter numbers.\n')
            self.view.console_text_output.configure(state='disabled')
            self.view.range_input.delete(0, 'end')

            # print("Error: Incorrect data type. Please enter a valid number.")
