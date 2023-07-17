from Planet import Planet
import time
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

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
        hubble_constant = 69.8  # Current value for hubble constant
        max_distance = 439999652819071048e+23 # Distance to Observable Universe Edge in KM 
        distance = selected_planet.distance  # Distance to selected planet in Parsecs
        #Converted distances to planet being observed#
        distanceKM = distance *(3.0857 * 10 ** 13) # Convert distance from PC to KM for loop
        distanceMPC = distance / 1000000 # Convert distance from PC to MPC for velocity calculations


        numCalc = 0 # This is the number of calculations performed by the algorithm

        velocity = hubble_constant * distanceMPC  # Calculate the starting velocity
        starting_velocity = velocity              #save initial velocity for display

        max_distance = max_distance - distanceKM  # get just the distance from the planet to obervational universe edge, ignoring distance from earth to the planet
      
        #Step size in km for how long the planet will travel before each recalculation
        step = (max_distance/2000000/(self.efficiency_index*0.1))              # Divides by index to lower km for recalculations the larger the index

        t = 0                                     # this is to count years for the final result
        start_time = time.time()                  # Start the timer
        data = []                                 # This is a list to store algorithm results for visualization

        #variables for graphing
        counter = 0
        interval_distances_km = []
        interval_velocities_km_s = [] 
        #  loop that increments of distance equal to step, calculates the time that was taken to reach the next increment
        #  Then recalculate the new velocity and repeat. The speed will increase with distance.
        while distanceKM < max_distance:
            
            distanceKM += step  # Planet moves step KM away from earth
            delta_t = 0 
            delta_t = step / velocity  # Time taken to reach the next increment
            # recalculate as the distance increases, thus its expansion rate must increase
            velocity = hubble_constant * (distanceKM *3.2407792896664E-20)  #since distanceKM contains current distance, this is used and converted to mpc as appropriate
            t += delta_t  # Add the time taken for the current step to the total elapsed time
        
            #  The data is being stored in a list for later visualization.
            #  This will also be passed to the view
            data.append({
                'distance': distance,
                'velocity': velocity,
            })
            #Appending values for the graph, using each 1000th value
            if counter % 1000 == 0:
              interval_distances_km.append(distanceKM) # stores distances
              interval_velocities_km_s.append(velocity) # stores velocity
            #  The data is being stored in a list for later visualization.
            #  This will also be passed to the view
            data.append({
                'distance': distance,
                'velocity': velocity,
            })
            numCalc +=1
            counter +=1
        end_time = time.time()  # Stop the timer
        t = '{:.5g}'.format(t) # format scientific notation of time to be limited to 5 digits
        t = str(t) + " years"
        end_time = time.time()  # Stop the timer
        calc = end_time - start_time

        step = '{:.5g}'.format(step) # format scientific notation representing step size to be limited to 5 digits
        step = str(step) 
        
        #  Send formatted value to view
        
        # size graph
        plt.figure(figsize=(15, 10))
        # this will take all of the distances and velocities and plot them
        plt.plot(interval_distances_km, interval_velocities_km_s, label='Velocity', color='blue', linestyle='-')
        plt.xlabel('Distance (km)') # label x axis
        plt.ylabel('Velocity (km/s)') # label y axis
        plt.title(str(selected_planet) + ': Velocity vs Distance')
        plt.grid(True) # set to grid 

        plt.xscale('log') # logarithmic scale to spread out data evenly(many points very close together)
        #why log scale? to spread out points and make the pattern more clear
        #this aids in visualization with large data sets

        #add information about the velocity and effeciency index to the graph
        plt.plot([], [], label=f'Starting Velocity: {starting_velocity:.2e} km/s', color='black', linestyle='-')
        plt.plot([],[],   label=f'Effeciency Index:{self.efficiency_index}',color='black', linestyle='-')
        #plot the legend
        plt.legend()


        #the function of these next two code blocks are to improve the readability
        #of the graph, forcing even spacing on the axis and helping spread data points
        num_x_ticks = 5  # Number of ticks on the x-axis
        x_ticks = np.logspace(np.log10(interval_distances_km[0]), np.log10(max_distance), num=num_x_ticks)
        plt.xticks(x_ticks, ['{:.1e}'.format(x) for x in x_ticks])#set x-axis position

        num_y_ticks = 5  # Number of ticks on the y-axis
        y_ticks = np.linspace(0, max(interval_velocities_km_s), num=num_y_ticks)
        plt.yticks(y_ticks, ['{:.1e}'.format(y) for y in y_ticks])#set y axis position



        # Force the limits for each axis. Set from 0 to max distance / velocity
        plt.xlim(0, max_distance)
        plt.ylim(0,max(interval_velocities_km_s))

       
        # Show the plot
        plt.show()
        controller_reference.view.create_visualization_screen(t, calc, starting_velocity, numCalc, step)