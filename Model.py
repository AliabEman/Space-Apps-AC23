from Planet import Planet


class Model:

    def __init__(self, planet_data):
        self.planets = []

        # instantiate planet objects to add to the Model list via the CSV data dictionary on initialization
        for data in planet_data:
            if data['name'] != 'name':
                planet = Planet(name=data['name'], mass=data['mass'], distance=data['distance'])
                self.planets.append(planet)

        # create a duplicate list so the original data can be filtered or retrieved without harm
        self.filteredPlanets = []
        self.filteredPlanets = self.planets

        # will probably need some fields to save model data in order to pass it to the algorithm?
        self.selected_planet = None
        self.efficiency_index = 1
