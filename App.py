import tkinter as tk
import pandas

from Controller import Controller
from Model import Model
from View import View

   
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        #Function called if the CSV requires reformatting 
        def cleanup_csv(nasa_data_frame):
           nasa_data_frame = pandas.read_csv(csvName)
           # Check the first 25 rows and columns for instances of the old column names or comments
           n_rows, n_cols = nasa_data_frame.shape
           for i in range(min(n_rows, 25)):
               for j in range(min(n_cols, 25)):
                   if nasa_data_frame.iloc[i, j] == 'pl_name':
                       nasa_data_frame.iloc[i, j] = 'name'
                   elif nasa_data_frame.iloc[i, j] == 'pl_bmasse' or nasa_data_frame.iloc[i, j] == 'pl_masse':
                       nasa_data_frame.iloc[i, j] = 'mass'
                   elif nasa_data_frame.iloc[i, j] == 'sy_dist':
                       nasa_data_frame.iloc[i, j] = 'distance'
                   elif '#' in str(nasa_data_frame.iloc[i, j]):
                       nasa_data_frame = nasa_data_frame.drop(i)
                   elif nasa_data_frame.columns[j] == 'name' and nasa_data_frame.iloc[i, j] == 'name':
                       nasa_data_frame = nasa_data_frame.drop(i)
                       
           nasa_data_frame.to_csv(csvName, index=False) # Write the changes into the CSV
           nasa_data_frame.reset_index(drop=True, inplace=True)
           return nasa_data_frame# Function end
        
        
        self.title("MVC_CSV_GUI DEMO")
        # currently locking the parent window since the layout does not properly resize with window
        self.resizable(False, False)
        
        # read all data from CSV 
        csvName = "NASA_PRODUCTION.csv"
        nasa_data_frame = pandas.read_csv(csvName)
        
        # check if the name column is already in the correct location
        if 'name' in nasa_data_frame.columns:
            nasa_data_frame = pandas.read_csv(csvName)
        else:
            # Check if the first row contains "#", if it does, call cleanup function to remove it as comments remain from download
            if nasa_data_frame.iloc[0].str.contains("#").any():
                nasa_data_frame = cleanup_csv(nasa_data_frame)
        
        # The File can have header issues, especially when downloaded so accounting for column headers out of place is required
        header_row = None
        for i in range(len(nasa_data_frame)): # parsing without modification has minimal effeciency impact
            row = nasa_data_frame.loc[i]
            if 'name' in row.values and 'mass' in row.values and 'distance' in row.values:
                header_row = i
                break
                
        # if the header row was found, set it as the column names and delete all previous rows
        if header_row is not None:
            nasa_data_frame.columns = nasa_data_frame.loc[header_row]
        
        # convert dataframe to data dictionary to be passed to model constructor
        planet_data = nasa_data_frame.to_dict('records')
        model = Model(planet_data)

        # initialize the parent ttk frame which will have our 3 frame layout attached
        view = View(self)

        # draw the view onto the Parent window to take up the full space
        view.grid(row=0, column=0, sticky="nsew")

        controller = Controller(model, view)

        # assign controller to the view ( Not the best practice but it works for now )
        view.set_controller(controller)

        # draw the GUI on top of the layout, Must come after the controller in oder to assign values to widgets from
        # model
        view.draw_widgets()


if __name__ == '__main__':
    app = App()
    app.mainloop()



    