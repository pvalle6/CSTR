# Labels for Actuators

# button2 = tk.Button(window, text="Button 2")
# button2.place(x=200, y=200)


# designer_frame = tk.Frame(window, borderwidth=1)
# designer_frame.grid()
#
# toolbar_frame = tk.Frame(designer_frame, borderwidth=1, relief="raised")
# toolbar_frame.grid(row=0, column=0, sticky="w")
#
# start_frame = tk.Frame(designer_frame, borderwidth=1)
# start_frame.grid(row=1, column=0)
#
# design_display_frame = tk.Frame(designer_frame, borderwidth=1)
# design_display_frame.grid(row=1, column=1)
#
# button1 = tk.Button(toolbar_frame, text="File", width=10)
# button1.pack(side="left")
#
# button2 = tk.Button(toolbar_frame, text="View", width=10)
# button2.pack(side="left")
#
# button3 = tk.Button(toolbar_frame, text="Edit", width=10)
# button3.pack(side="left")
#
# # design_display_frame.grid_rowconfigure(0, minsize=500)  # Set the minimum height of the frame to 500 pixels
# # design_display_frame.grid_columnconfigure(0, minsize=500)  # Set the minimum width of the frame to 500 pixels
# #
# # start_frame.grid_rowconfigure(0, minsize=500)  # Set the minimum height of the frame to 500 pixels
# # start_frame.grid_columnconfigure(0, minsize=500)  # Set the minimum width of the frame to 500 pixels
#
#
# label = tk.Label(start_frame, text='CSTR Design Wizard')
# label.grid(row=0, column=0)
#
# # start_button = ttk.Button(start_frame, text='Start Simulation')
# # start_button.grid()
#
# # This is the CSTR Designer
# diameter_var = tk.StringVar()
# height_var = tk.StringVar()
#
# diameter_entry_label = tk.Label(start_frame, text='Diameter (m)')
# diameter_entry_label.grid(row=1, column=0)
#
# diameter_entry_box = tk.Entry(start_frame, width=10, textvariable=diameter_var)
# diameter_entry_box.bind('<Return>', lambda event: update_volume_label())
# diameter_entry_box.grid(row=1, column=1)
#
# height_entry_label = tk.Label(start_frame, text='Height (m)')
# height_entry_label.grid(row=2, column=0)
#
# height_entry_box = tk.Entry(start_frame, width=10, textvariable=height_var)
# height_entry_box.bind('<Return>', lambda event: update_volume_label())
# height_entry_box.grid(row=2, column=1)
#
# volume_label_pre = tk.Label(start_frame, text='Volume (m^3): ')
# volume_label_pre.grid(row=3, column=0)
#
# volume_label = tk.Label(start_frame, text ="", relief="sunken", width=10)
# volume_label.grid(row=3, column=1)
# def calculate_volume(diameter, height):
#     return np.pi * ((diameter / 2 ) ** 2) * height
#
# # def draw_cylinder():
# #     diameter = float(diameter_entry_box.get())
# #     height = float(height_entry_box.get())
# #     fig = plt.figure()
# #     ax = fig.add_subplot(111, projection='3d')
# #     x = np.linspace(-diameter/2, diameter/2, 100)
# #     z = np.linspace(0, height, 100)
# #     Xc, Zc = np.meshgrid(x, z)
# #     Yc = np.sqrt((diameter/2)**2-Xc**2)
# #
# #     # Draw parameters
# #     rstride = 20
# #     cstride = 10
# #     ax.plot_surface(Xc, Yc, Zc, alpha=0.2, rstride=rstride, cstride=cstride)
# #     ax.plot_surface(Xc, -Yc, Zc, alpha=0.2, rstride=rstride, cstride=cstride)
# #
# #     ax.set_xlabel("X")
# #     ax.set_ylabel("Y")
# #     ax.set_zlabel("Z")
# #
# #     canvas = FigureCanvasTkAgg(fig, master=design_display_frame)
# #     canvas.draw()
# #     canvas.get_tk_widget().grid()
#
# def update_volume_label():
#     diameter = float(diameter_entry_box.get())
#     height = float(height_entry_box.get())
#     volume = calculate_volume(diameter, height)
#     truncated_volume = int(volume)  # Truncate the volume by converting it to an integer
#     volume_label.config(text=f'{truncated_volume}')
#     # raw_cylinder()
#
#
#
# create_reactor_button = ttk.Button(start_frame, text='Create Reactor', command=update_volume_label, state='disabled')
# create_reactor_button.grid(row=4, column=0)
#
# # Function to check if both fields have a value
# def check_fields(*args):
#     if diameter_var.get() and height_var.get():
#
#         dim = int(diameter_var.get())
#         h = int(height_var.get())
#
#         if dim == 0 or h == 0:
#             create_reactor_button.config(state='disabled')
#
#         elif dim > 20 or h > 25:
#             create_reactor_button.config(state='disabled')
#         else:
#             create_reactor_button.config(state='normal')
#             update_volume_label()
#     else:
#         create_reactor_button.config(state='disabled')
#
# # Call check_fields whenever the entry field values change
# diameter_var.trace_add('write', check_fields)
# height_var.trace_add('write', check_fields)

# canvas = FigureCanvasTkAgg(fig, master=window)
# canvas.draw()
# canvas.get_tk_widget().grid()

# Function to update plot
# def update_plot(history_df):
#     ax.clear()
#     ax.set_xlim([0, 20])
#     ax.set_ylim([0, 1000])
#     ax.plot(history_df['time'], history_df['volume'])
#     canvas.draw()
# #