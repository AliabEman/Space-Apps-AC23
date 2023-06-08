import re
import pygame as pygame

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
                
    # END Filter by name function

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
        text = "Authors:\nAlexander Lapierre\nAliab Eman\nDylan Carroll\nGreg Rowat\nJay Patel\nSavas Erturk\n\n"
        text += "This app has been created for the NASA SpaceApps Competition!"
        text += "\n\nDev note: More text will be added here to define the algorithm"
        
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
                yPosition += 20 # Increment the y position for blit so each surface prints on a new line
            pygame.display.flip()

        pygame.quit()