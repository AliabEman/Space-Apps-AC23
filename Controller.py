import re
import pygame as pygame


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def get_planets(self):
        return self.model.filteredPlanets

    def start_algorithm(self):
        selected_planet = self.get_selected_planet()
        self.model.run_algorithm(self, selected_planet)

    # function to restore the planet selection list to the original DataSet included at initialization.
    def clear_filters(self):

        # reset the filter planet list to the original state
        self.model.filteredPlanets = self.model.planets
        # reset the efficiency index of the application
        self.model.efficiency_index = 1

        # reset the output window text, include welcome message and filter message
        self.view.console_text_output.configure(state='normal')
        self.view.console_text_output.delete(1.0, 'end')
        self.view.console_text_output.insert('end', 'Welcome to SandGlass!\n')
        self.view.console_text_output.insert('end', 'All filters have been removed, Original planet list restored\n')
        self.view.console_text_output.configure(state='disabled')

        # set the option values of the dropdown list
        self.view.selection_dropdown['values'] = self.model.filteredPlanets

        self.view.planet_selection.set("Select a planet")

    # function to parse out the planet names from dataset to be used in selection menu on interface
    def get_planets_names(self):
        selection_dropdown_planet_names = []
        for planet in self.model.filteredPlanets:
            name = planet.name
            selection_dropdown_planet_names.append(name)

    # function to validate planet selection drop down and pass a valid planet selection to the algorithmic module
    def get_selected_planet(self):

        # grab string value from selection drop down menu
        selected_planet = self.view.selection_dropdown.get()

        if selected_planet == "Select a planet":
            self.view.console_text_output.configure(state='normal')
            self.view.console_text_output.insert('end', 'Invalid selection, please choose planet from drop down!\n')
            self.view.console_text_output.configure(state='disabled')
            return

        elif selected_planet == "No results found":
            self.view.console_text_output.configure(state='normal')
            self.view.console_text_output.insert('end', 'No planets are available in the current list, '
                                                        'please clear filters and start again\n')
            self.view.console_text_output.configure(state='disabled')
            return

        else:
            for planet in self.model.planets:
                if planet.name == selected_planet:
                    selected_planet = planet
                    return selected_planet

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
                        return f"{time_in_seconds:.2f} seconds"
                    else:
                        return f"{time_in_hours:.2f} hours"
                else:
                    return f"{time_in_days:.2f} days"
            else:
                return f"{time_in_months:.2f} months"
        elif 1 <= time_in_years < 1000:
            return f"{time_in_years:.2f} years"
        elif 1000 <= time_in_years < 1000000:
            time_in_thousands_of_years = time_in_years / 1000
            return f"{time_in_thousands_of_years:.2f} thousand years"
        elif 1000000 <= time_in_years < 1000000000:
            time_in_millions_of_years = time_in_years / 1000000
            return f"{time_in_millions_of_years:.2f} million years"
        elif time_in_years >= 1000000000:
            time_in_billions_of_years = time_in_years / 1000000000
            return f"{time_in_billions_of_years:.2f} billion years"

    def get_efficiency_index(self):
        return self.model.efficiency_index

    # function to set the efficiency index of the model for calculations and output a client message to console
    def submit_efficiency(self):
        efficiency_value = self.view.efficiency_slider.get()

        self.model.efficiency_index = efficiency_value

        # reset the output window text, include welcome message and filter message
        self.view.console_text_output.configure(state='normal')
        self.view.console_text_output.insert('end',
                                             'Efficiency index of calculation set to %' + str(efficiency_value) +
                                             'factor of calculation increments\n')
        self.view.console_text_output.configure(state='disabled')

    def filter_by_mass(self):
        self.inputted_mass = 0
        self.filtered_mass = []
        self.filtered_mass_planet = []

        try:
            self.inputted_mass_string = self.view.mass_input.get()
            self.inputted_mass = float(self.view.mass_input.get())

            if self.inputted_mass <= 0:
                self.view.console_text_output.configure(state='normal')
                self.view.console_text_output.insert('end',
                                                     '********* Mass value must be greater than zero *********\n')
                self.view.console_text_output.configure(state='disabled')
                return

            self.view.console_text_output.configure(state='normal')
            self.view.console_text_output.insert('end', '********* Mass filter applied *********\n')
            self.view.mass_input.delete(0, 'end')

            for planet in self.model.filteredPlanets:
                if hasattr(planet, 'mass') and float(planet.mass) < self.inputted_mass:
                    self.filtered_mass.append(planet)
                    self.filtered_mass_planet.append(planet.name)

            if len(self.filtered_mass) == 0:
                self.view.console_text_output.insert('end', 'No results found with mass less than ' + str(
                    self.inputted_mass) + '\n')
                self.view.console_text_output.configure(state='disabled')
                self.view.name_input.delete(0, 'end')
                self.view.selection_dropdown.configure(values=self.filtered_mass_planet)
                self.view.planet_selection.set("No results found")
                return

            self.model.filteredPlanets = self.filtered_mass
            self.view.console_text_output.insert('end', str(len(
                self.filtered_mass)) + ' results found with mass less than ' + str(self.inputted_mass) + '\n')
            self.view.console_text_output.configure(state='disabled')
            self.view.name_input.delete(0, 'end')
            self.view.selection_dropdown.configure(values=self.filtered_mass_planet)
            self.view.planet_selection.set("Select a planet")

        except ValueError:
            if not self.inputted_mass_string:
                self.view.console_text_output.configure(state='normal')
                self.view.console_text_output.insert('end', '********* Mass filter value cannot be empty *********\n')
                self.view.console_text_output.configure(state='disabled')
            else:
                self.view.console_text_output.configure(state='normal')
                self.view.console_text_output.insert('end',
                                                     '********* Please enter a valid number for the mass filter *********\n')
                self.view.console_text_output.configure(state='disabled')

    def get_filtered_distance(self):
        self.filtered_distance = []
        self.filtered_distance_string = []

        try:
            self.inputted_distance_string = self.view.range_input.get()
            self.inputted_distance = float(self.view.range_input.get())

            if self.inputted_distance <= 0:
                self.view.console_text_output.configure(state='normal')
                self.view.console_text_output.insert('end',
                                                     '********* Range value must be greater than zero *********\n')
                self.view.console_text_output.configure(state='disabled')
                return

            self.view.console_text_output.configure(state='normal')
            self.view.console_text_output.insert('end', '********* Range filter applied *********\n')
            self.view.range_input.delete(0, 'end')

            for planet in self.model.filteredPlanets:  # Use the filtered_mass list instead of self.model.filteredPlanets
                if hasattr(planet, 'distance') and float(planet.distance) < self.inputted_distance:
                    self.filtered_distance_string.append(planet)
                    self.filtered_distance.append(planet.name)

            if len(self.filtered_distance_string) == 0:
                self.view.console_text_output.insert('end', 'No results found with distance less than ' + str(
                    self.inputted_distance) + '\n')
                self.view.console_text_output.configure(state='disabled')
                self.view.name_input.delete(0, 'end')
                self.view.selection_dropdown.configure(values=self.filtered_distance)
                self.view.planet_selection.set("No results found")
                return

            self.model.filteredPlanets = self.filtered_distance_string
            self.view.console_text_output.insert('end', str(len(
                self.filtered_distance_string)) + ' results found with distance less than ' + str(
                self.inputted_distance) + '\n')
            self.view.console_text_output.configure(state='disabled')
            self.view.name_input.delete(0, 'end')
            self.view.selection_dropdown.configure(values=self.filtered_distance)
            self.view.planet_selection.set("Select a planet")

        except ValueError:
            if not self.inputted_distance_string:
                self.view.console_text_output.configure(state='normal')
                self.view.console_text_output.insert('end', '********* Range filter value cannot be empty *********\n')
                self.view.console_text_output.configure(state='disabled')
            else:
                self.view.console_text_output.configure(state='normal')
                self.view.console_text_output.insert('end',
                                                     '********* Please enter a valid number for the range filter *********\n')
                self.view.console_text_output.configure(state='disabled')

    def filter_by_name(self):
        # Get the name that the user wants to search for
        searchName = self.view.name_input.get().strip().lower()

        # If the user submits without entering a name
        if searchName == "":
            self.view.console_text_output.configure(state='normal')
            self.view.console_text_output.insert('end', '********* Name filter value cannot be empty *********\n')
            self.view.console_text_output.configure(state='disabled')
            # Clear the input field
            self.view.name_input.delete(0, 'end')
            return

        # The longest name in the data is 29 characters (including spaces)
        if len(searchName) > 29:
            self.view.console_text_output.configure(state='normal')
            self.view.console_text_output.insert('end', '********* No results found *********\n')
            self.view.console_text_output.configure(state='disabled')
            # Clear the input field
            self.view.name_input.delete(0, 'end')
            # Set the drop-down list to empty
            self.view.selection_dropdown.configure(values=[])
            self.view.planet_selection.set("********* No results found *********")
            return

        # Check the dataset for the specified string
        else:
            tempPlanets = []

            for planet in self.model.filteredPlanets:
                if hasattr(planet, 'name') and searchName in planet.name.lower():
                    tempPlanets.append(planet)

            if len(tempPlanets) == 0:
                self.view.console_text_output.configure(state='normal')
                self.view.console_text_output.insert('end',
                                                     '********* Name filter applied *********\n no results containing "' + searchName + '" found\n')
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
                if len(tempPlanets) == 1:
                    self.view.console_text_output.insert('end', '********* Name filter applied *********\n ' + str(
                        len(tempPlanets)) + ' result containing "' + searchName + '" found\n')
                    # If there is only one result, set the selected planet to that result
                    self.view.planet_selection.set(tempPlanets[0])
                else:
                    self.view.console_text_output.insert('end', '********* Name filter applied *********\n ' + str(
                        len(tempPlanets)) + ' results containing "' + searchName + '" found\n')
                    self.view.planet_selection.set("Select a planet")
                self.view.console_text_output.configure(state='disabled')
                # Clear the input field
                self.view.name_input.delete(0, 'end')
                # Set the drop-down list to the filtered list
                self.view.selection_dropdown.configure(values=tempPlanets)

    # Function that creates a window with the "about" information of the application
    def about_app(self):
        # define the window
        pygame.init()
        screen = pygame.display.set_mode((800, 500))
        pygame.display.set_caption("About the Application")

        # Function that will send text to the next line when it finds a \n (since pygame can't process them)
        def process_newlines(text_to_split):
            # Create a list where every element is a line of text up to a newline character. Deletes the newline character
            split_text = text_to_split.split('\n')

            # Create a list of surfaces, where each surface in the list is one line of text
            surfaces = []
            for sentence in split_text:
                new_surface = font.render(sentence, True, (255, 255, 255))
                surfaces.append(new_surface)
            return surfaces

        # Define the text to display
        font = pygame.font.SysFont("Arial", 20)
        text = "SandGlass has been created for the NASA SpaceApps 2023 Competition!"
        text += "\n\nSandGlass is an interactive application for interfacing with the NASA Exoplanet archives database in\n" \
                "order to determine the point when an individual planet will leave the currently viewable universe\n" \
                "SandGlass allows the user to filter and select from all known Exoplanets classified by NASA based on the\n" \
                "planets title, current distance from earth in parsecs (pc), and planetary mass in relation to Earth.\n" \
                "Using the current Hubble constant and the maximum distance viewable by the hubble telescope Sandglass\n" \
                "is able to determine how many years it will take for a planet to reach the edge of the viewable universe\n" \
                "based on universal expansion theory."
        text += "\n\nAuthors:\nAlexander Lapierre\nAliab Eman\nDylan Carroll\nGreg Rowat\nJay Patel\nSavas Erturk\n\n"

        # Create an array that will store the lines that fit into the window
        formatted_text = process_newlines(text)

        # Pygame loop
        running = True
        while running:
            yPosition = 10
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Print each surface in the list
            for surface in formatted_text:
                screen.blit(surface, (10, yPosition))
                yPosition += 20  # Increment the y position for blit so each surface prints on a new line
            pygame.display.flip()

        pygame.quit()
