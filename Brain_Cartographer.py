import tkinter as tk
from tkinter import ttk, Text, messagebox
import pandas as pd
import os
import csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AutocompleteEntry(ttk.Combobox):
    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list, key=lambda s: s.lower())
        self._hits = []
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyreleases)
        self['values'] = self._completion_list

    def autocomplete(self):
        current_text = self.get()
        _hits = [item for item in self._completion_list if item.lower().startswith(current_text.lower())]
        if _hits != self._hits:
            self._hits = _hits
            self.position = len(current_text)
            self['values'] = _hits + self._completion_list
            
    def handle_keyreleases(self, event):
        if event.keysym in ('BackSpace', 'Left', 'Right', 'Up', 'Down', 'Shift_R', 'Shift_L'):
            return
        self.autocomplete()

def load_excel_data(file_path):
    if os.path.exists(file_path):
        df = pd.read_excel(file_path, index_col=0)
        return df
    else:
        messagebox.showerror("Error", f"File '{file_path}' not found.")
        return None

def get_source_options(dataframe):
    return dataframe.index.tolist()

def get_target_options(dataframe):
    return dataframe.columns.tolist()

def get_significant_row_names(data, row_name):
    significant_values = calculate_significant_values(data.loc[row_name, :])
    return significant_values.index.tolist()

def get_significant_column_names(data, column_name):
    significant_values = calculate_significant_values(data[column_name])
    return significant_values.index.tolist()

def calculate_significant_values(data):
    std_dev = np.std(data)
    significant_values = data[data > (std_dev * 2)]
    return significant_values

def is_connected(region_source, region_target, data):
    if not region_source or not region_target:
        return False
    
    if region_source not in data.index or region_target not in data.columns:
        print(f"Error: '{region_source}' or '{region_target}' not found in data.")
        return False

    std_dev = data.values.std()  # Calculate the standard deviation of the entire data
    intersection_value = data.loc[region_source, region_target]
    return intersection_value > (2 * std_dev)
#def is_connected(region_source, region_target, excel_data):
    # Placeholder function to check connectivity between regions
 #   return True  # Replace this with your actual logic

def show_blank_plot(source, target, connectivity_paths, excel_data, selected_order):
    print(f"Showing blank plot for {selected_order} connectivity...")

    # Define positions for source and target
    source_position = (0.1, 0.5)  # Position of source
    target_position = (0.9, 0.5)  # Position of target

    # Create a new figure
    fig = plt.Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_title(f"{selected_order} Connectivity Visualization")
    ax.axis('off')  # Remove x-axis and y-axis

    # Plot source and target circles with names
    ax.plot(source_position[0], source_position[1], 'bo', markersize=10, label=source)
    ax.text(source_position[0], source_position[1], source, fontsize=12, ha='right', va='center')

    ax.plot(target_position[0], target_position[1], 'ro', markersize=10, label=target)
    ax.text(target_position[0], target_position[1], target, fontsize=12, ha='left', va='center')

    
    if selected_order == "First Order":
        # Extract unique intermediate regions
        intermediate_regions = list(set(connectivity_paths))

        # Calculate y-axis positions for intermediate regions
        num_regions = len(intermediate_regions)
        y_positions = np.linspace(0.2, 0.8, num_regions)

        # Plot connectivity lines from source to each intermediate region and then to the target
        for i, region in enumerate(intermediate_regions):
            # Define position for intermediate region
            region_position = (0.5, y_positions[i])

            # Plot connectivity line from source to intermediate region
            ax.plot([source_position[0], region_position[0]], [source_position[1], region_position[1]], 'k-')
            ax.text(region_position[0], region_position[1], region, fontsize=10, ha='center', va='bottom')

            # Plot connectivity line from intermediate region to target
            ax.plot([region_position[0], target_position[0]], [region_position[1], target_position[1]], 'k-')

    elif selected_order == "Second Order":
        # Calculate y-axis positions for connectivity paths
        num_paths = len(connectivity_paths)
        y_positions = np.linspace(0.2, 0.8, num_paths)

        for i, path in enumerate(connectivity_paths):
            _, subregion_1, subregion_2, _ = path
            
            # Define positions for subregions
            subregion_1_position = (0.3, y_positions[i])
            subregion_2_position = (0.7, y_positions[i])
            
            # Draw lines from source to subregion_1, subregion_1 to subregion_2, and subregion_2 to target
            ax.plot([source_position[0], subregion_1_position[0], subregion_2_position[0], target_position[0]],
                     [source_position[1], subregion_1_position[1], subregion_2_position[1], target_position[1]], 'k-')
            
            # Add labels for subregions
            ax.text(subregion_1_position[0], subregion_1_position[1], subregion_1, fontsize=10, ha='center', va='bottom')
            ax.text(subregion_2_position[0], subregion_2_position[1], subregion_2, fontsize=10, ha='center', va='bottom')

    elif selected_order == "Third Order":
        # Calculate y-axis positions for connectivity paths
        num_paths = len(connectivity_paths)
        y_positions = np.linspace(0.2, 0.8, num_paths)

        for i, path in enumerate(connectivity_paths):
            _, subregion_1, subregion_2, subregion_3, _, _ = path
            
            # Define positions for subregions
            subregion_1_position = (0.25, y_positions[i])
            subregion_2_position = (0.5, y_positions[i])
            subregion_3_position = (0.75, y_positions[i])
            
            # Draw lines from source to subregion_1, subregion_1 to subregion_2, subregion_2 to subregion_3, and subregion_3 to target
            ax.plot([source_position[0], subregion_1_position[0], subregion_2_position[0], subregion_3_position[0], target_position[0]],
                     [source_position[1], subregion_1_position[1], subregion_2_position[1], subregion_3_position[1], target_position[1]], 'k-')
            
            # Add labels for subregions
            ax.text(subregion_1_position[0], subregion_1_position[1], subregion_1, fontsize=10, ha='center', va='bottom')
            ax.text(subregion_2_position[0], subregion_2_position[1], subregion_2, fontsize=10, ha='center', va='bottom')
            ax.text(subregion_3_position[0], subregion_3_position[1], subregion_3, fontsize=10, ha='center', va='bottom')

    elif selected_order == "Fourth Order":
        # Calculate y-axis positions for connectivity paths
        num_paths = len(connectivity_paths)
        y_positions = np.linspace(0.2, 0.8, num_paths)

        for i, path in enumerate(connectivity_paths):
            _, subregion_1, subregion_2, subregion_3, subregion_4, _, _ = path
            
            # Define positions for subregions
            subregion_1_position = (0.2, y_positions[i])
            subregion_2_position = (0.4, y_positions[i])
            subregion_3_position = (0.6, y_positions[i])
            subregion_4_position = (0.8, y_positions[i])
            
            # Draw lines from source to subregion_1, subregion_1 to subregion_2, subregion_2 to subregion_3, subregion_3 to subregion_4, and subregion_4 to target
            ax.plot([source_position[0], subregion_1_position[0], subregion_2_position[0], subregion_3_position[0], subregion_4_position[0], target_position[0]],
                     [source_position[1], subregion_1_position[1], subregion_2_position[1], subregion_3_position[1], subregion_4_position[1], target_position[1]], 'k-')
            
            # Add labels for subregions
            ax.text(subregion_1_position[0], subregion_1_position[1], subregion_1, fontsize=10, ha='center', va='bottom')
            ax.text(subregion_2_position[0], subregion_2_position[1], subregion_2, fontsize=10, ha='center', va='bottom')
            ax.text(subregion_3_position[0], subregion_3_position[1], subregion_3, fontsize=10, ha='center', va='bottom')
            ax.text(subregion_4_position[0], subregion_4_position[1], subregion_4, fontsize=10, ha='center', va='bottom')
    
    ax.legend()
    ax.grid(False)  # Remove background grid lines
    fig.tight_layout()  # Adjust spacing between subplots

    # Clear the previous plot from the canvas
    for widget in plot_canvas.winfo_children():
        widget.destroy()

    # Create a Tkinter-compatible canvas for the plot
    canvas = FigureCanvasTkAgg(fig, master=plot_canvas)
    canvas.draw()

    # Place the canvas on the Tkinter canvas
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Clear the previous text from the sub_regions_text widget
    sub_regions_text.delete('1.0', tk.END)

    # Insert the connectivity paths into the sub_regions_text widget
    sub_regions_text.insert(tk.END, f"{selected_order} Connectivity Paths:\n\n")
    for path in connectivity_paths:
        path_str = " -- ".join(path)
        sub_regions_text.insert(tk.END, path_str + "\n")


def show_no_connectivity_plot():
    # Create a new figure
    fig = plt.Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_title("No Connectivity Found")
    ax.axis('off')
    # ax.set_xlabel("X Axis")
    # ax.set_ylabel("Y Axis")
    ax.text(0.5, 0.5, "No connectivity found between the selected source and target.", 
            fontsize=12, ha='center', va='center', wrap=True)
    ax.grid(False)  # Remove background grid lines
    fig.tight_layout()  # Adjust spacing between subplots

    # Clear the previous plot from the canvas
    for widget in plot_canvas.winfo_children():
        widget.destroy()

    # Create a Tkinter-compatible canvas for the plot
    canvas = FigureCanvasTkAgg(fig, master=plot_canvas)
    canvas.draw()

    # Place the canvas on the Tkinter canvas
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def on_plot_click():
    selected_option_source = dropdown_var_source.get()
    selected_option_target = dropdown_var_target.get()
    selected_order = dropdown_var_order.get()

    line_number_label.config(text=f"Selected Line Source: {selected_option_source}, Target: {selected_option_target}, Order: {selected_order}")
    print(f"Selected Source option: {selected_option_source}")
    print(f"Selected Target option: {selected_option_target}")
    print(f"Selected Order: {selected_order}")

    # Clear the previous plot from the canvas
    plot_canvas.delete("all")

    significant_source_values = get_significant_row_names(excel_data, selected_option_source) if selected_option_source else []
    significant_target_values = get_significant_column_names(excel_data, selected_option_target) if selected_option_target else []

    if selected_order == "First Order":
        # Check for connected regions
        connected_regions = [region for region in significant_source_values if region in significant_target_values]
        print("Connected Regions:", connected_regions)
        if connected_regions:
            show_blank_plot(selected_option_source, selected_option_target, connected_regions, excel_data, selected_order)
        else:
            show_no_connectivity_plot()
    elif selected_order == "Second Order":
        computed_connectivity = []
        for region_source in significant_source_values:
            for region_target in significant_target_values:
                if region_source != region_target and is_connected(region_source, region_target, excel_data):
                    path = (selected_option_source, region_source, region_target, selected_option_target)
                    if len(set(path)) == len(path):  # Check for unique regions in the path
                        computed_connectivity.append(path)
        
        print("Computed Connectivity:", computed_connectivity)
        
        if computed_connectivity:
            show_blank_plot(selected_option_source, selected_option_target, computed_connectivity, excel_data, selected_order)
        else:
            show_no_connectivity_plot()
    elif selected_order == "Third Order":
        computed_connectivity = []
        for region_source in significant_source_values:
            for intermediate_region_1 in get_significant_column_names(excel_data, region_source):
                for intermediate_region_2 in get_significant_column_names(excel_data, intermediate_region_1):
                    for region_target in significant_target_values:
                        if intermediate_region_2 in get_significant_row_names(excel_data, region_target):
                            path = (selected_option_source, region_source, intermediate_region_1, intermediate_region_2, region_target, selected_option_target)
                            if len(set(path)) == len(path):  # Check for unique regions in the path
                                computed_connectivity.append(path)
        
        print("Computed Connectivity:", computed_connectivity)
        
        if computed_connectivity:
            show_blank_plot(selected_option_source, selected_option_target, computed_connectivity, excel_data, selected_order)
        else:
            show_no_connectivity_plot()
    elif selected_order == "Fourth Order":
        computed_connectivity = []
        for region_source in significant_source_values:
            for intermediate_region_1 in excel_data.columns:
                if excel_data.at[region_source, intermediate_region_1] > 0:
                    for intermediate_region_2 in excel_data.columns:
                        if excel_data.at[intermediate_region_1, intermediate_region_2] > 0:
                            for intermediate_region_3 in excel_data.columns:
                                if excel_data.at[intermediate_region_2, intermediate_region_3] > 0:
                                    for region_target in significant_target_values:
                                        if excel_data.at[intermediate_region_3, region_target] > 0:
                                            path = (selected_option_source, region_source, intermediate_region_1, intermediate_region_2, intermediate_region_3, region_target, selected_option_target)
                                            if len(set(path)) == len(path):  # Check for unique regions in the path
                                                computed_connectivity.append(path)
        
        print("Computed Connectivity:", computed_connectivity)
        
        if computed_connectivity:
            show_blank_plot(selected_option_source, selected_option_target, computed_connectivity, excel_data, selected_order)
        else:
            show_no_connectivity_plot()


def load_user_data():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls"), ("CSV files", "*.csv")])
    if file_path:
        excel_data = load_excel_data(file_path)
        if excel_data is not None:
            # Update dropdown menus with new options based on user's data
            dropdown_var_source.set_completion_list(get_source_options(excel_data))
            dropdown_var_target.set_completion_list(get_target_options(excel_data))
            # Clear the previous plot and text
            plot_canvas.delete("all")
            sub_regions_text.delete('1.0', tk.END)
    else:
        messagebox.showinfo("Info", "No file selected.")

# Load data from excel
excel_data = load_excel_data("density.xlsx")

# Main window
root = tk.Tk()
root.title("GUI Portal")
root.geometry("800x400")

frame = tk.Frame(root)
frame.pack(pady=20, padx=20)

degree_label = tk.Label(frame, text="Order of Connectivity:")
degree_label.grid(row=3, column=0, padx=10, sticky="w")

order_options = ["First Order", "Second Order", "Third Order", "Fourth Order"]
dropdown_var_order = ttk.Combobox(frame, values=order_options)
dropdown_var_order.set(order_options[0])  # Set default value
dropdown_var_order.grid(row=3, column=1, padx=10, sticky="w")

line_number_label = tk.Label(frame, text="Select Region of Brain: ")
line_number_label.grid(row=0, column=0, columnspan=2, padx=10, sticky="w")

#Position of Source label
source_label = tk.Label(frame, text="Source:")
source_label.grid(row=1, column=0, padx=10, sticky="w")

#Position of first drop-down menu
dropdown_var_source = AutocompleteEntry(frame)
dropdown_var_source.set_completion_list(get_source_options(excel_data))
dropdown_var_source.set("")
dropdown_var_source.grid(row=1, column=1, padx=10, sticky="w")

#Creates and Positions the "Target" label
target_label = tk.Label(frame, text="Target:")
target_label.grid(row=2, column=0, padx=10, sticky="w")

#Position of second drop-down menu
dropdown_var_target = AutocompleteEntry(frame)
dropdown_var_target.set_completion_list(get_target_options(excel_data))
dropdown_var_target.set("")
dropdown_var_target.grid(row=2, column=1, padx=10, sticky="w")

sub_regions_text = Text(root, height=20, width=50)
sub_regions_text.pack(pady=20, padx=20)

#Create a canvas to hold the plot
plot_canvas = tk.Canvas(frame, width=600, height=400)
plot_canvas.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

frame.grid_rowconfigure(4, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)

#Create a "Plot" button
plot_button = tk.Button(frame, text="Plot", command=on_plot_click)
plot_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Update Main Window Setup
load_data_button = tk.Button(frame, text="Load Data", command=load_user_data)
load_data_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()