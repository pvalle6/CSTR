import scipy
import matplotlib.pyplot as plt
import numpy as np
import pickle as pkl
import math
import pandas as pd
import time

from PIL import ImageTk, Image
import tkinter as tk
from tkinter import ttk
import multiprocessing as mp
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


df = pd.DataFrame(columns=['flow101', 'flow100', 'cooling_temp', 'reactor_temp', 'feed_temp', 'exit_temp', 'level', 'exit_composition', 'feed_composition'])

# Create tkinter window
window = tk.Tk()
# window.geometry("800x700")
window.resizable(False, False)

taskbar = tk.Frame(window, height=40)
taskbar.grid(sticky="w")

stopped = True
def stop_simulation():
    global stopped
    stopped = True
    print("Simulation Stopped")

def start_timer():
    global stopped
    stopped = False

    print("Simulation Started")
    run_simulation()


def run_simulation():
    start_time = time.time()
    update_time()
    # history_df = pd.DataFrame(columns=['time', 'bulk_a_comp', 'reactor_temp', 'jacket_temp_out'])

    bulk_comp_a = 0
    reactor_temp = 300
    temperate_jacket_out = 300

    sol = scipy.integrate.solve_ivp(system_of_equations, [0, 1], [bulk_comp_a, reactor_temp, temperate_jacket_out], args=(feed_flow,))
    history_df = pd.DataFrame(
        {'bulk_a_comp': sol.y[0], "reactor_temp": sol.y[1], "jacket_temp_out": sol.y[2]})

    previous_time_step = 1

    for i in range(0, 1000000):
        sol = scipy.integrate.solve_ivp(system_of_equations, [0, 1],
                                        [history_df['bulk_a_comp'].iloc[-1], history_df['reactor_temp'].iloc[-1],
                                         history_df['jacket_temp_out'].iloc[-1]], args=(feed_flow,))
        history_df = pd.concat([history_df, pd.DataFrame(
            {'bulk_a_comp': sol.y[0], "reactor_temp": sol.y[1], "jacket_temp_out": sol.y[2]})])
        previous_time_step += 1
        print(history_df.tail(1))

        reactor_temp_indicator.set(str(round(sol.y[1][-1], 2)) + " K")
        cool_temp_out_indicator.set(str(round(sol.y[2][-1], 2)) + " K")
        exit_comp_indicator.set(str(round(sol.y[0][-1], 2)) + " mol / m^3")
        time.sleep(0.01)
        window.update()
        if stopped:
            break

def update_time():
    elapsed_time = str(int(time.time() - start_time))  # Get the number of seconds since the start
    clock = "Time Elapsed: " + elapsed_time + " seconds"
    time_var.set(clock)  # Update the time_var with the new time
    # print(elapsed_time)
    window.after(1000, update_time)  # Schedule the function to be called again after 1 second




def open_f101_valve():

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

    def set_flow_rate():
        global feed_flow
        flow_rate = fc100_flow_entry.get()
        print("Flow Rate Set to: ", flow_rate)
        flow100_indicator.set(flow_rate)
        feed_flow = float(flow_rate)
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


file_button = tk.Button(taskbar, text="File", width=8, height=2, bg="white", fg="black", font="Arial 12 bold",)
file_button.grid(row=0, column=0, sticky="w")

edit_button = tk.Button(taskbar, text="Edit", width=8, height=2, bg="white", fg="black", font="Arial 12 bold")
edit_button.grid(row=0, column=1, sticky="w")

view_button = tk.Button(taskbar, text="View", width=8, height=2, bg="white", fg="black", font="Arial 12 bold")
view_button.grid(row=0, column=1, sticky="w")

start_button = tk.Button(taskbar, text="Start", width=8, height=2, bg="white", fg="black", font="Arial 12 bold",
                         command=start_timer)
start_button.grid(row=0, column=2, sticky="w")

stop_button = tk.Button(taskbar, text="Stop", width=8, height=2, bg="white", fg="black", font="Arial 12 bold",
                        command=stop_simulation)
stop_button.grid(row=0, column=3, sticky="w")

help_button = tk.Button(taskbar, text="Help", width=8, height=2, bg="white", fg="black", font="Arial 12 bold")
help_button.grid(row=0, column=4, sticky="w")


# title = tk.Label(taskbar, text="CSTR Simulation", font="Arial 16 bold", fg="black")
# title.grid(row=1)

frame = tk.Frame(window)
frame.grid()

start_time = time.time()  # Get the time at the start of the program

time_var = tk.StringVar()  # Create a StringVar to hold the time

# Create a Label to display the time
time_label = tk.Label(taskbar, textvariable=time_var)
time_label.grid(row=0,column=5)  # Adjust the position as needed



# Setting up the Control Interface
img = Image.open("reactor_image/test_2.png")

photo = ImageTk.PhotoImage(img)

diagram = tk.Label(frame, image=photo)
diagram.grid()

fc100_button = tk.Button(frame, text="FC100", width=8, height=2, bg="white", fg="black", font="Arial 12 bold",
                    relief="raised", borderwidth=2, command=open_f100_valve)
fc100_button.place(x=20, y=285)

fc101_button = tk.Button(frame, text="FC101", width=8, height=2, bg="white", fg="black", font="Arial 12 bold",
                    relief="raised", borderwidth=2, command=open_f101_valve)
fc101_button.place(x=500, y=115)

# fc102_button = tk.Button(frame, text="FC102", width=8, height=2, bg="white", fg="black", font="Arial 12 bold",
#                     relief="raised", borderwidth=2)
# fc102_button.place(x=592, y=325)

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
reactor_temp_label.place(x=70, y=500)

feed_temp_indicator = tk.StringVar()
feed_temp_indicator.set("0")
feed_temp_label = tk.Label(frame, textvariable=feed_temp_indicator, font="Arial 12 bold")
feed_temp_label.place(x=450, y=20)

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
exit_composition_label.place(x=670, y=500)

feed_comp_indicator = tk.StringVar()
feed_comp_indicator.set("0")
feed_composition_label = tk.Label(window, textvariable=feed_comp_indicator, font="Arial 12 bold")
feed_composition_label.place(x=450, y=270)

cool_temp_out_indicator = tk.StringVar()
cool_temp_out_indicator.set("0")
cool_temp_out_label = tk.Label(frame, textvariable=cool_temp_out_indicator, font="Arial 12 bold")
cool_temp_out_label.place(x=550, y=270)

# Tank Specifications
# tank_diameter = 0.5 # m
# tank_height = 1 # m
# tank_volume = math.pi * (tank_diameter/2)**2 * tank_height

# Feed Specifications
feed_comp_a = 0 # mol / m^3
feed_comp_b = 0 # mol / m^3
feed_flow = 0.1 # m^3 / s

# Jacket Specifications
jacket_temp_in = 300 # K
jack_feed_flow = 0.1 # m^3 / s

# jacket_volume = 0.1 # m^3

def system_of_equations(t,y, feed_flow):
    # y[0] = bulk_a_comp
    # y[1] = reactor_temp
    # y[2] = temperature_jacket_out

    # Constants
    reactor_volume = 0.2 # m^3
    k1 = 0.1 # rate constant for reaction 1
    jacket_volume = 0.1 # m^3
    heat_transfer_coefficient = 0.1 # W / m^2 K
    area_of_transfer = 0.1 # m^2

    # constants that later should be dynamically changed
    feed_flow = feed_flow # m^3 / s
    feed_a_comp = 0.5 # mol / m^3
    feed_temp = 300 # K

    energy_activation = 0.1 # J / mol
    R = 8.314 # J / mol K

    enthalpy_change = 0.1 # J / mol
    density = 0.1 # kg / m^3
    heat_capacity = 0.1 # J / kg K

    jacket_flow = 0.1 # m^3 / s

    # Differential Equations
    dCadt = ((feed_flow / reactor_volume * (feed_a_comp)) - (feed_flow / reactor_volume * y[0])
             - k1 * np.exp(-energy_activation / (R * y[1])) * y[0])

    dTdt = ((((feed_flow / reactor_volume) * (feed_temp- y[1])) +
            ((-enthalpy_change / (density * heat_capacity)) * k1 * np.exp(-energy_activation / (R * y[1])) * y[0]))
            - ((heat_transfer_coefficient * area_of_transfer / (density * heat_capacity * reactor_volume)) *
               (y[1] - y[2])))

    dTjdt = ((jacket_flow / jacket_volume) * (jacket_temp_in - y[2]) +
             (heat_transfer_coefficient * area_of_transfer / (density * heat_capacity * jacket_volume)) * (y[1] - y[2]))



    return [dCadt, dTdt, dTjdt]

flow101_indicator.set(0.1)
flow100_indicator.set(0.1)
cw_temp_indicator.set(300)
feed_temp_indicator.set(300)
feed_comp_indicator.set(0.5)
level_indicator.set("CONSTANT")


while(True):
    window.update()