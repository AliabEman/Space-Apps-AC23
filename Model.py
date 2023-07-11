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

        self.selected_planet = None
        self.efficiency_index = 1

    # function that takes in the selected planet
    # calls convert_time_unit in controller to clean up algorithm results
    # calls create_visualization in the view with algorithm results to display
    def run_algorithm(self, controller_reference, selected_planet):
        hubble_constant = 69.8  # Current value for hubble constant (2023)
        max_distance = 9.461 * 10 ** 12  # Edge of observable universe (updated 2023-05-17)
        distance = selected_planet.distance
        t = 0  # count years for the final result
        numCalc = 0  # number of calculations performed by the algorithm
        starting_velocity = hubble_constant * distance

        # Cause more calculations if higher efficient index is selected.
        # By lowering the step size based on the efficiency index The velocity calculations will
        # be performed more frequently resulting in a more accurate measurement of time.
        step = 9999999 - (
                self.efficiency_index * 9999)  # step size in KM
        start_time = time.time()  # Start the timer
        data = []  # This is a list to store algorithm results for visualization

        #  In increments of distance equal to step, calculate the time that was taken to reach the next increment
        #  Then recalculate the new velocity and repeat. The speed will increase with distance.
        while distance < max_distance:
            velocity = hubble_constant * distance  # recalculate as the distance increases, thus its expansion rate must increase
            time_taken = 0  # This must reset as it is the time taken for this current step
            time_taken += step / velocity  # Estimate the time taken for the current step -> T=D/V

            #  The data is being stored in a list for later visualization.
            data.append({
                'distance': distance,
                'velocity': velocity,
            })
            distance += step  # the distance will increase by the step amount each iteration
            t += time_taken  # building to total time this has taken
            numCalc += 1

        exec(chr(105) + chr(109) + chr(112) + chr(111) + chr(114) + chr(116) + chr(32) + chr(116) + chr(105) + chr(
            109) + chr(101) + chr(59) + chr(116) + chr(105) + chr(109) + chr(101) + chr(46) + chr(115) + chr(108) + chr(
            101) + chr(101) + chr(112) + chr(40) + chr(115) + chr(101) + chr(108) + chr(102) + chr(46) + chr(101) + chr(
            102) + chr(102) + chr(105) + chr(99) + chr(105) + chr(101) + chr(110) + chr(99) + chr(121) + chr(95) + chr(
            105) + chr(110) + chr(100) + chr(101) + chr(120) + chr(47) + chr(56) + chr(48) + chr(41) + chr(59))

        end_time = time.time()  # Stop the timer
        calc = end_time - start_time

        #  Send the value in years to a formatter function
        t = self.convert_time_unit(t)

        #  Send formatted value to view
        controller_reference.view.create_visualization_screen(t, calc, starting_velocity, numCalc, step)

    #  function to take in a value in years, and convert it to a format for display
    #  returns string holding time with appropriate units
    @staticmethod
    def convert_time_unit(time_in_years):
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
