import scipy
# import matplotlib.pyplot as plt
import numpy as np
# import pickle as pkl
# import math
import pandas as pd
import time
from tkinter import filedialog
from PIL import ImageTk, Image
import tkinter as tk
# from tkinter import ttk
# import multiprocessing as mp
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# , NavigationToolbar2Tk
import webbrowser

# Setting up dataframes for simulation
simulation_data = pd.DataFrame(columns=['time', 'flow101', 'flow100', 'cooling_temp',
                                        'reactor_temp', 'feed_temp',
                                        'exit_temp', 'level', 'exit_composition',
                                        'feed_composition', 'jacket_temp_out'])

history_df = pd.DataFrame(columns=['time', 'bulk_a_comp', 'reactor_temp', 'jacket_temp_out'])

# Feed Specifications
feed_comp_a = 0  # mol / m^3
feed_comp_b = 0  # mol / m^3
feed_flow = 0.1  # m^3 / s
feed_temp = 300  # K

# Jacket Specifications
jacket_temp_in = 280  # K
jack_feed_flow = 0.1  # m^3 / s

# jacket_volume = 0.1 # m^3

# Base GUI Tkinter Setup
# TODO: Reorganize this into a application that is initialized on startup
window = tk.Tk()
window.resizable(False, False)

# TODO: Add a splash/startup screen for setting initial parameters as well as loading older simulations or settings.

# Creates the Taskbar at the top of the simulation window
taskbar = tk.Frame(window, height=40)
taskbar.grid(sticky="w")

# Settings a boolean that controls the dynamic simulation
# TODO: Reorganize simulation runs into classes that have the parameters a properties
stopped = True


def stop_simulation():
    """
    This function stops the simulation of the CSTR in dynamic mode.
    :return:
    """
    global stopped
    stopped = True
    print("Simulation Stopped")


def start_timer():
    """
    This function starts the simulation of the CSTR in dynamic mode. It also resets the time.
    :return:
    """
    global stopped
    stopped = False

    print("Simulation Started")
    run_simulation()


def save_as():
    """
    This function saves the simulation data to a CSV file.
    :return:
    """
    global history_df
    filename = filedialog.asksaveasfilename(defaultextension=".csv")
    if filename:
        history_df.to_csv(filename, index=False)


def print_simulation_data():
    """
    This function prints the simulation data to the console.
    :return:
    """
    print(simulation_data)


def show_menu(event):
    """
    This function shows the file menu when the file button is clicked.
    :param event:
    :return:
    """
    file_menu.post(event.x_root, event.y_root)


file_menu = tk.Menu(window, tearoff=0)
file_menu.add_command(label="Save As", command=save_as)


def show_view_menu(event):
    view_menu.post(event.x_root, event.y_root)


view_menu = tk.Menu(window, tearoff=0)
view_menu.add_command(label="Print Simulation Data", command=print_simulation_data)


def open_disturbances_window():
    """
    This function opens the disturbances window.
    :return:
    """
    disturbances_window = tk.Toplevel(window)
    disturbances_window.title("Disturbances")
    disturbances_window.geometry("400x400")
    disturbances_window.resizable(False, False)


file_menu.add_command(label="Disturbances", command=open_disturbances_window)


def open_github():
    webbrowser.open('https://github.com/pvalle6/CSTR')


def open_linkedin():
    webbrowser.open('https://www.linkedin.com/in/peter-v-334609211')


def open_pse():
    webbrowser.open('https://pse.che.lsu.edu/')


def run_simulation():
    """
    This function runs the simulation of the CSTR in dynamic mode.

    :return:
    """
    global history_df
    global simulation_data

    start_time = time.time()
    time_now = 0
    # history_df = pd.DataFrame(columns=['time', 'bulk_a_comp', 'reactor_temp', 'jacket_temp_out'])

    bulk_comp_a = 0
    reactor_temp = 300
    temperate_jacket_out = 300

    sol = scipy.integrate.solve_ivp(system_of_equations, [0, 1],
                                    [bulk_comp_a, reactor_temp, temperate_jacket_out],
                                    args=(feed_flow, jack_feed_flow))
    history_df = pd.DataFrame(
        {'time': 0, 'bulk_a_comp': sol.y[0], "reactor_temp": sol.y[1], "jacket_temp_out": sol.y[2]})

    previous_time_step = 1

    for i in range(0, 1000000):
        sol = scipy.integrate.solve_ivp(system_of_equations, [0, 1],
                                        [history_df['bulk_a_comp'].iloc[-1], history_df['reactor_temp'].iloc[-1],
                                         history_df['jacket_temp_out'].iloc[-1]], args=(feed_flow, jack_feed_flow))
        history_df = pd.concat([history_df, pd.DataFrame(
            {"time": time_now, 'bulk_a_comp': sol.y[0], "reactor_temp": sol.y[1], "jacket_temp_out": sol.y[2]})])

        simulation_data = pd.concat([simulation_data, pd.DataFrame(
            {"time": time_now, "flow101": flow101_indicator.get(),
             "flow100": flow100_indicator.get(), "cooling_temp": cw_temp_indicator.get(),
             "reactor_temp": reactor_temp_indicator.get(), "feed_temp": feed_temp_indicator.get(),
             "exit_temp": exit_temp_indicator.get(), "level": level_indicator.get(),
             "exit_composition": exit_comp_indicator.get(), "feed_composition": feed_comp_indicator.get(),
             "jacket_temp_out": sol.y[2][-1]}, index=[0])])

        previous_time_step += 1
        # print(history_df.tail(1))

        reactor_temp_indicator.set(str(round(sol.y[1][-1], 2)) + " K")
        cool_temp_out_indicator.set(str(round(sol.y[2][-1], 2)) + " K")
        exit_comp_indicator.set(str(round(sol.y[0][-1], 2)) + " mol / m^3")
        window.update()
        time_now = time.time() - start_time
        time.sleep(0.001)
        if stopped:
            break

# def update_time(start_time):
#     """
#     This function updates the time in the GUI.
#     :return:
#     """
#     elapsed_time = str(int(time.time() - start_time))  # Get the number of seconds since the start
#     clock = "Time Elapsed: " + elapsed_time + " seconds"
#     time_var.set(clock)  # Update the time_var with the new time
#     # print(elapsed_time)
#     # window.after(1000, update_time)  # Schedule the function to be called again after 1 second
#
#     return elapsed_time


def open_f101_valve():
    """
    This function opens the FC101 Valve Control Window.
    :return:
    """
    def set_flow_rate():
        global feed_flow
        flow_rate = fc101_flow_entry.get()
        print("Flow Rate Set to: ", flow_rate)
        flow101_indicator.set(flow_rate)
        feed_flow = float(flow_rate)
        # fc101_control_window.destroy()

    print("Opening FC101 Valve Control Window")
    fc101_control_window = tk.Toplevel(window)

    fc101_control_window.title("FC101 Control")
    fc101_control_window.geometry("400x400")
    fc101_control_window.resizable(False, False)

    fc101_flow_label = tk.Label(fc101_control_window, text="Flow Rate (m^3/s)", font="Arial 12 bold")
    fc101_flow_label.grid(row=0, column=0)

    fc101_flow_entry = tk.Entry(fc101_control_window, font="Arial 12 bold")
    fc101_flow_entry.grid(row=0, column=1)

    fc101_set_button = tk.Button(fc101_control_window, text="Set", font="Arial 12 bold", command=set_flow_rate)
    fc101_set_button.grid(row=1, column=0, columnspan=2)


def open_f100_valve():
    """
    This function opens the FC100 Valve Control Window.
    :return:
    """
    def set_flow_rate():
        global jack_feed_flow
        flow_rate = fc100_flow_entry.get()
        print("Flow Rate Set to: ", flow_rate)
        flow100_indicator.set(flow_rate)
        jack_feed_flow = float(flow_rate)
        # fc101_control_window.destroy()

    print("Opening FC100 Valve Control Window")
    fc100_control_window = tk.Toplevel(window)

    fc100_control_window.title("FC101 Control")
    fc100_control_window.geometry("400x400")
    fc100_control_window.resizable(False, False)

    fc100_flow_label = tk.Label(fc100_control_window, text="Flow Rate (m^3/s)", font="Arial 12 bold")
    fc100_flow_label.grid(row=0, column=0)

    fc100_flow_entry = tk.Entry(fc100_control_window, font="Arial 12 bold")
    fc100_flow_entry.grid(row=0, column=1)

    fc100_set_button = tk.Button(fc100_control_window, text="Set", font="Arial 12 bold", command=set_flow_rate)
    fc100_set_button.grid(row=1, column=0, columnspan=2)


# def open_sensor_graph(sensor_name):
#     """
#     This function opens a graph of a particular sensor's data.
#     :return:
#     """
#     print("Opening Sensor Graph")
#
#     if sensor_name == "Feed Composition":
#         feed_comp_window = tk.Toplevel(window)
#         feed_comp_window.title("Feed Composition Sensor")
#         feed_comp_window.geometry("450x450")
#         # feed_comp_window.resizable(False, False)
#
#         feed_comp_graph = Figure(figsize=(5, 4), dpi=100)
#         feed_comp_plot = feed_comp_graph.add_subplot(111)
#         feed_comp_plot.plot(simulation_data["time"], simulation_data['feed_composition'])
#         feed_comp_plot.set_xlabel("Time (s)")
#         feed_comp_plot.set_ylabel("Concentration (mol/m^3)")
#         feed_comp_canvas = FigureCanvasTkAgg(feed_comp_graph, feed_comp_window)
#         feed_comp_canvas.get_tk_widget().pack()
#         feed_comp_canvas.draw()
#
#     elif sensor_name == "Feed Temperature":
#         feed_temp_window = tk.Toplevel(window)
#         feed_temp_window.title("Feed Temperature Sensor")
#         feed_temp_window.geometry("450x450")
#         # feed_temp_window.resizable(False, False)
#
#         feed_temp_graph = Figure(figsize=(5, 4), dpi=100)
#         feed_temp_plot = feed_temp_graph.add_subplot(111)
#         feed_temp_plot.plot(simulation_data["time"], simulation_data['feed_temp'])
#         feed_temp_plot.set_xlabel("Time (s)")
#         feed_temp_plot.set_ylabel("Feed Temperature (K)")
#         feed_temp_canvas = FigureCanvasTkAgg(feed_temp_graph, feed_temp_window)
#         feed_temp_canvas.get_tk_widget().pack()
#         feed_temp_canvas.draw()
#
#     elif sensor_name == "Coolant Temperature":
#         cool_temp_window = tk.Toplevel(window)
#         cool_temp_window.title("Coolant Temperature Sensor")
#         cool_temp_window.geometry("450x450")
#         # cool_temp_window.resizable(False, False)
#
#         cool_temp_graph = Figure(figsize=(5, 4), dpi=100)
#         cool_temp_plot = cool_temp_graph.add_subplot(111)
#         cool_temp_plot.plot(simulation_data["time"], simulation_data['cooling_temp'])
#         cool_temp_plot.set_xlabel("Time (s)")
#         cool_temp_plot.set_ylabel("Coolant Temperature (K)")
#         cool_temp_canvas = FigureCanvasTkAgg(cool_temp_graph, cool_temp_window)
#         cool_temp_canvas.get_tk_widget().pack()
#         cool_temp_canvas.draw()
#
#     elif sensor_name == "Reactor Temperature":
#         reactor_temp_window = tk.Toplevel(window)
#         reactor_temp_window.title("Reactor Temperature Sensor")
#         reactor_temp_window.geometry("450x450")
#         # reactor_temp_window.resizable(False, False)
#
#         reactor_temp_graph = Figure(figsize=(5, 4), dpi=100)
#         reactor_temp_plot = reactor_temp_graph.add_subplot(111)
#         reactor_temp_plot.plot(simulation_data["time"], simulation_data['reactor_temp'])
#         reactor_temp_plot.set_xlabel("Time (s)")
#         reactor_temp_plot.set_ylabel("Reactor Temperature (K)")
#
#         reactor_temp_canvas = FigureCanvasTkAgg(reactor_temp_graph, reactor_temp_window)
#         reactor_temp_canvas.get_tk_widget().pack()
#         reactor_temp_canvas.draw()
#
#     elif sensor_name == "Jacket Temperature":
#         jacket_temp_window = tk.Toplevel(window)
#         jacket_temp_window.title("Jacket Temperature Sensor")
#         jacket_temp_window.geometry("450x450")
#         # jacket_temp_window.resizable(False, False)
#
#         jacket_temp_graph = Figure(figsize=(5, 4), dpi=100)
#         jacket_temp_plot = jacket_temp_graph.add_subplot(111)
#         jacket_temp_plot.plot(simulation_data["time"], simulation_data['jacket_temp_out'])
#         jacket_temp_plot.set_xlabel("Time (s)")
#         jacket_temp_plot.set_ylabel("Jacket Temperature (K)")
#         jacket_temp_canvas = FigureCanvasTkAgg(jacket_temp_graph, jacket_temp_window)
#         jacket_temp_canvas.get_tk_widget().pack()
#         jacket_temp_canvas.draw()
#
#     elif sensor_name == "Exit Composition":
#         exit_comp_window = tk.Toplevel(window)
#         exit_comp_window.title("Exit Composition Sensor")
#         exit_comp_window.geometry("450x450")
#         # exit_comp_window.resizable(False, False)
#
#         exit_comp_graph = Figure(figsize=(5, 4), dpi=100)
#         exit_comp_plot = exit_comp_graph.add_subplot(111)
#         exit_comp_plot.plot(simulation_data["time"], simulation_data['exit_composition'])
#         exit_comp_plot.set_xlabel("Time (s)")
#         exit_comp_plot.set_ylabel("Exit Composition (mol/m^3)")
#         exit_comp_canvas = FigureCanvasTkAgg(exit_comp_graph, exit_comp_window)
#         exit_comp_canvas.get_tk_widget().pack()
#         exit_comp_canvas.draw()

# TODO: Refactor this into a function that creates a sensor button

def create_sensor_button(frame_, image, text, x, y, command):
    button = tk.Button(frame_, image=image, text=text, compound="center", bg="white",
                       fg="black", font="Arial 12 bold", border=0, relief="raised")
    button.config(command=command)
    button.place(x=x, y=y)
    return button


def open_sensor_graph(sensor_name, data=simulation_data):
    print(f"Opening {sensor_name} Sensor Window")
    sensor_window = tk.Toplevel(window)
    sensor_window.title(f"{sensor_name} Sensor")
    sensor_window.geometry("450x450")

    sensor_graph = Figure(figsize=(5, 4), dpi=100)
    sensor_plot = sensor_graph.add_subplot(111)
    sensor_plot.plot(data["time"], data[sensor_name])
    sensor_plot.set_xlabel("Time (s)")
    sensor_plot.set_ylabel(f"{sensor_name} (units)")

    sensor_canvas = FigureCanvasTkAgg(sensor_graph, sensor_window)
    sensor_canvas.get_tk_widget().pack()
    sensor_canvas.draw()


# Here is many of the buttons are initialized and placed on the taskbar
file_button = tk.Button(taskbar, text="File", width=8, height=2, bg="white", fg="black", font="Arial 12 bold",)
file_button.grid(row=0, column=0, sticky="w")

file_button.bind("<Button-1>", show_menu)

edit_button = tk.Button(taskbar, text="Edit", width=8, height=2, bg="white", fg="black", font="Arial 12 bold")
edit_button.grid(row=0, column=1, sticky="w")

view_button = tk.Button(taskbar, text="View", width=8, height=2, bg="white", fg="black", font="Arial 12 bold")
view_button.grid(row=0, column=1, sticky="w")
view_button.bind("<Button-1>", show_view_menu)
start_button = tk.Button(taskbar, text="Start", width=8, height=2, bg="white", fg="black", font="Arial 12 bold",
                         command=start_timer)
start_button.grid(row=0, column=2, sticky="w")

stop_button = tk.Button(taskbar, text="Stop", width=8, height=2, bg="white", fg="black", font="Arial 12 bold",
                        command=stop_simulation)
stop_button.grid(row=0, column=3, sticky="w")

help_button = tk.Button(taskbar, text="Help", width=8, height=2, bg="white", fg="black", font="Arial 12 bold")
help_button.grid(row=0, column=4, sticky="w")

help_menu = tk.Menu(window, tearoff=0)
help_menu.add_command(label="GitHub", command=open_github)
help_menu.add_command(label="Linkedin", command=open_linkedin)
help_menu.add_command(label="PSE", command=open_pse)


def show_help_menu(event):
    help_menu.post(event.x_root, event.y_root)


help_button.bind("<Button-1>", show_help_menu)
# title = tk.Label(taskbar, text="CSTR Simulation", font="Arial 16 bold", fg="black")
# title.grid(row=1)

# Here is where the Process Simulation Window is initialized
frame = tk.Frame(window)
frame.grid()
# Setting up GUI Images
circle_image = tk.PhotoImage(file="reactor_image/circle.png")
img = Image.open("reactor_image/test_2.png")
photo = ImageTk.PhotoImage(img)
diagram = tk.Label(frame, image=photo)
diagram.grid()
# start_time = time.time()  # Get the time at the start of the program
time_var = tk.StringVar()  # Create a StringVar to hold the time
time_label = tk.Label(taskbar, textvariable=time_var)
time_label.grid(row=0, column=5)  # Adjust the position as needed

# Setting up the Control Interface for the CSTR
fc100_button = tk.Button(frame, text="FC100", width=8, height=2, bg="white", fg="black", font="Arial 12 bold",
                         relief="raised", borderwidth=2, command=open_f100_valve)
fc100_button.place(x=20, y=285)
fc101_button = tk.Button(frame, text="FC101", width=8, height=2, bg="white", fg="black", font="Arial 12 bold",
                         relief="raised", borderwidth=2, command=open_f101_valve)
fc101_button.place(x=500, y=115)

# fc102_button = tk.Button(frame, text="FC102", width=8, height=2, bg="white", fg="black", font="Arial 12 bold",
#                     relief="raised", borderwidth=2)
# fc102_button.place(x=592, y=325)

# Here is where many of the sensor display and GUI elements are initialized

"""
['time', 'flow101', 'flow100', 'cooling_temp', 'reactor_temp', 'feed_temp',
                                        'exit_temp', 'level', 'exit_composition', 'feed_composition', 'jacket_temp_out']
                                        """


def on_feed_comp_sensor(x):
    print("Opening Feed Composition Sensor Window")
    open_sensor_graph("Feed Composition")


feed_c_button = tk.Button(frame, image=circle_image, text="FC", compound="center", bg="white",
                          fg="black", font="Arial 12 bold", border=0, relief="raised")
feed_c_button.config(command=lambda: on_feed_comp_sensor(1))
feed_c_button.place(x=410, y=255)


def on_feed_temp_sensor(args):
    print("Opening Feed Temperature Sensor Window")
    open_sensor_graph("feed_temp")


feed_t_button = tk.Button(frame, image=circle_image, text="FT", compound="center", bg="white",
                          fg="black", font="Arial 12 bold", border=0, relief="raised")
feed_t_button.config(command=lambda: on_feed_temp_sensor(1))
feed_t_button.place(x=375, y=12)


def on_coolant_temp_sensor(x):
    print("Opening Coolant Temperature Sensor Window")
    open_sensor_graph("cooling_temp")


cool_t_button = tk.Button(frame, image=circle_image, text="CT", compound="center", bg="white",
                          fg="black", font="Arial 12 bold", border=0, relief="raised")
cool_t_button.config(command=lambda: on_coolant_temp_sensor(1))
cool_t_button.place(x=105, y=192)


def on_reactor_temp_sensor(x):
    print("Opening Reactor Temperature Sensor Window")
    open_sensor_graph("reactor_temp")


reactor_t_button = tk.Button(frame, image=circle_image, text="RT", compound="center", bg="white",
                             fg="black", font="Arial 12 bold", border=0, relief="raised")
reactor_t_button.config(command=lambda: on_reactor_temp_sensor(1))
reactor_t_button.place(x=90, y=510)


def on_jacket_temp_sensor(x):
    print("Opening Jacket Temperature Sensor Window")
    open_sensor_graph("jacket_temp_out")


jacket_t_button = tk.Button(frame, image=circle_image, text="TC Out", compound="center", bg="white",
                            fg="black", font="Arial 12 bold", border=0, relief="raised")
jacket_t_button.config(command=lambda: on_jacket_temp_sensor(1))
jacket_t_button.place(x=505, y=300)


def on_exit_comp_sensor(x):
    print("Opening Exit Composition Sensor Window")
    open_sensor_graph("exit_composition")


exit_c_button = tk.Button(frame, image=circle_image, text="Cout", compound="center", bg="white",
                          fg="black", font="Arial 12 bold", border=0, relief="raised")
exit_c_button.config(command=lambda: on_exit_comp_sensor(1))
exit_c_button.place(x=680, y=510)

flow100_indicator = tk.StringVar()
flow100_indicator.set("0")
flow100_label = tk.Label(frame, textvariable=flow100_indicator, font="Arial 12 bold")
flow100_label.place(x=110, y=300)

flow101_indicator = tk.StringVar()
flow101_indicator.set("0")
flow101_label = tk.Label(frame, textvariable=flow101_indicator, font="Arial 12 bold")
flow101_label.place(x=590, y=130)

cw_temp_indicator = tk.StringVar()
cw_temp_indicator.set("0")
cooling_temp_label = tk.Label(frame, textvariable=cw_temp_indicator, font="Arial 12 bold")
cooling_temp_label.place(x=180, y=210)

reactor_temp_indicator = tk.StringVar()
reactor_temp_indicator.set("0")
reactor_temp_label = tk.Label(frame, textvariable=reactor_temp_indicator, font="Arial 12 bold")
reactor_temp_label.place(x=70, y=487)

feed_temp_indicator = tk.StringVar()
feed_temp_indicator.set("0")
feed_temp_label = tk.Label(frame, textvariable=feed_temp_indicator, font="Arial 12 bold")
feed_temp_label.place(x=460, y=20)

exit_temp_indicator = tk.StringVar()
exit_temp_indicator.set("0")
exit_temp_label = tk.Label(frame, textvariable=exit_temp_indicator, font="Arial 12 bold")
exit_temp_label.place(x=570, y=550)

level_indicator = tk.StringVar()
level_indicator.set("CONSTANT")
level_label = tk.Label(frame, textvariable=level_indicator, font="Arial 12 bold")
level_label.place(x=450, y=500)

exit_comp_indicator = tk.StringVar()
exit_comp_indicator.set("0")
exit_composition_label = tk.Label(frame, textvariable=exit_comp_indicator, font="Arial 12 bold")
exit_composition_label.place(x=670, y=470)

feed_comp_indicator = tk.StringVar()
feed_comp_indicator.set("0")
feed_composition_label = tk.Label(window, textvariable=feed_comp_indicator, font="Arial 12 bold")
feed_composition_label.place(x=450, y=270)

cool_temp_out_indicator = tk.StringVar()
cool_temp_out_indicator.set("0")
cool_temp_out_label = tk.Label(frame, textvariable=cool_temp_out_indicator, font="Arial 12 bold")
cool_temp_out_label.place(x=550, y=270)


def system_of_equations(t, y, feed_flow, jack_feed_flow):
    # y[0] = bulk_a_comp
    # y[1] = reactor_temp
    # y[2] = temperature_jacket_out

    # Constants
    reactor_volume = 0.2  # m^3
    k1 = 0.1  # rate constant for reaction 1
    jacket_volume = 0.1  # m^3
    heat_transfer_coefficient = 0.1  # W / m^2 K
    area_of_transfer = 0.1  # m^2

    # constants that later should be dynamically changed
    feed_flow = feed_flow  # m^3 / s
    feed_a_comp = 0.5  # mol / m^3
    feed_temp = 300  # K

    energy_activation = 0.1  # J / mol
    R = 8.314  # J / mol K

    enthalpy_change = 0.1  # J / mol
    density = 0.1  # kg / m^3
    heat_capacity = 0.1  # J / kg K

    jacket_flow = jack_feed_flow  # m^3 / s

    # Differential Equations
    dCadt = ((feed_flow / reactor_volume * feed_a_comp) - (feed_flow / reactor_volume * y[0])
             - k1 * np.exp(-energy_activation / (R * y[1])) * y[0])

    dTdt = ((((feed_flow / reactor_volume) * (feed_temp - y[1])) +
            ((-enthalpy_change / (density * heat_capacity)) * k1 * np.exp(-energy_activation / (R * y[1])) * y[0]))
            - ((heat_transfer_coefficient * area_of_transfer / (density * heat_capacity * reactor_volume)) *
               (y[1] - y[2])))

    dTjdt = ((jacket_flow / jacket_volume) * (jacket_temp_in - y[2]) +
             (heat_transfer_coefficient * area_of_transfer / (density * heat_capacity * jacket_volume)) * (y[1] - y[2]))

    return [dCadt, dTdt, dTjdt]


# Setting up the initial values for the simulation
flow101_indicator.set(str(jack_feed_flow))
flow100_indicator.set(str(feed_flow))
cw_temp_indicator.set(str(jacket_temp_in))
feed_temp_indicator.set(str(feed_temp))
feed_comp_indicator.set(str(feed_comp_a))
level_indicator.set("CONSTANT")

while True:
    window.update()
