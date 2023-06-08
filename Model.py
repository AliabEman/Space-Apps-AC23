from Planet import Planet
import time

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
        self.efficiency_index = 1  # TODO have this reflect the actual selected slider value

    # function that takes in the selected planet
    # calls convert_time_unit in controller to clean up algorithm results
    # calls create_visualization in the view with algorithm results to display
    def run_algorithm(self, controller_reference, selected_planet):
        hubble_constant = 69.8  # Current value for hubble constant
        max_distance = 9.461 * 10 ** 12  # Edge of observable universe (updated 2023-05-17)
        distance = selected_planet.distance  # pull selected planets distance
        t = 0  # this is to count years for the final result
        starting_velocity = hubble_constant * distance  # For informational purposes in the view, get the starting velocity
        step = 9999999 - (self.efficiency_index*9999)  # Cause more calculations if higher efficient index is selected. This must be a large value. Be careful changing
        start_time = time.time()  # Start the timer
        data = []  # This is a list to store algorithm results for visualization

        #  In increments of distance equal to step, calculate the time that was taken to reach the next increment
        #  Then recalculate the new velocity and repeat. The speed will increase with distance.
        while distance < max_distance:
            velocity = hubble_constant * distance  # recalculate as the distance increases, thus its expansion rate must increase
            time_taken = 0  # This must reset as it is the time taken for this current step
            time_taken += step / velocity  # Estimate the time taken for the current step -> T=D/V

            #  The data is being stored in a list for later visualization.
            #  This will also be passed to the view
            data.append({
                'distance': distance,
                'velocity': velocity,
            })
            distance += step  # the distance will increase by the step amount each iteration
            t += time_taken  # building to total time this has taken
        print(data)  # print out list within measured time
        end_time = time.time()  # Stop the timer
        calc = end_time - start_time
        #  Send the value in years to a formatter function
        t = controller_reference.convert_time_unit(self, t)
        #  Send formatted value to view
        print("t =", t)
        print("calc =", calc)
        print("SV =", starting_velocity)
        print("data =", data.__sizeof__)
        controller_reference.view.create_visualization_screen(self, t, calc, starting_velocity, data)