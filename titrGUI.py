import tkinter as tk
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter and Matplotlib Example")

        # Create a left frame for buttons and spinboxes
        self.left_frame = tk.Frame(root)
        self.left_frame.grid(row=0, column=0, sticky="n")

        # Create a button to open file dialog
        self.open_button = tk.Button(self.left_frame, text="Open File", command=self.open_file)
        self.open_button.grid(row=0, column=0, pady=5, padx=5)

        # Create Spinboxes with trace on their variables
        self.spinbox1_label = tk.Label(self.left_frame, text="Value 1:")
        self.spinbox1_label.grid(row=1, column=0, pady=5, padx=5)
        
        self.spinbox1_var = tk.StringVar()
        self.spinbox1 = tk.Spinbox(self.left_frame, from_=0, to=100, textvariable=self.spinbox1_var, command=self.spinbox_changed)
        self.spinbox1.grid(row=2, column=0, pady=5, padx=5)
        self.spinbox1_var.trace_add("write", lambda *args: self.spinbox_changed())

        self.spinbox2_label = tk.Label(self.left_frame, text="Value 2:")
        self.spinbox2_label.grid(row=3, column=0, pady=5, padx=5)
        
        self.spinbox2_var = tk.StringVar()
        self.spinbox2 = tk.Spinbox(self.left_frame, from_=0, to=100, textvariable=self.spinbox2_var, command=self.spinbox_changed)
        self.spinbox2.grid(row=4, column=0, pady=5, padx=5)
        self.spinbox2_var.trace_add("write", lambda *args: self.spinbox_changed())

        # Create checkbox for DChrj
        self.dchrj_var = tk.BooleanVar()
        self.dchrj_checkbox = tk.Checkbutton(self.left_frame, text="DChrj", variable=self.dchrj_var)
        self.dchrj_checkbox.grid(row=5, column=0, pady=5, padx=5)

        # Create entries for additional parameters
        self.layer_thickness_label = tk.Label(self.left_frame, text="Толщина слоя:")
        self.layer_thickness_label.grid(row=6, column=0, pady=5, padx=5)
        self.layer_thickness_entry = tk.Entry(self.left_frame)
        self.layer_thickness_entry.grid(row=7, column=0, pady=5, padx=5)

        self.current_label = tk.Label(self.left_frame, text="Сила тока:")
        self.current_label.grid(row=8, column=0, pady=5, padx=5)
        self.current_entry = tk.Entry(self.left_frame)
        self.current_entry.grid(row=9, column=0, pady=5, padx=5)

        self.time_step_label = tk.Label(self.left_frame, text="Время шага:")
        self.time_step_label.grid(row=10, column=0, pady=5, padx=5)
        self.time_step_entry = tk.Entry(self.left_frame)
        self.time_step_entry.grid(row=11, column=0, pady=5, padx=5)

        # Create a button for calculation
        self.calculate_button = tk.Button(self.left_frame, text="Расчет", command=self.open_file)
        self.calculate_button.grid(row=12, column=0, pady=10, padx=5)

        # Create a right frame for the matplotlib figure
        self.figure_frame = tk.Frame(root)
        self.figure_frame.grid(row=0, column=1, sticky="nsew")

        # Initialize the figure
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)

        # Add the figure to the Tkinter frame
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.figure_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas.draw()

        # Configure grid to make the right frame expand
        root.columnconfigure(1, weight=1)
        root.rowconfigure(0, weight=1)

    def open_file(self):
        # Open file dialog and get the selected file path
        file_path = filedialog.askopenfilename()
        if file_path:
            print(f"File selected: {file_path}")
            # You can add code here to handle the selected file

    def spinbox_changed(self):
        # Function to handle spinbox value changes
        value1 = self.spinbox1_var.get()
        value2 = self.spinbox2_var.get()
        print(f"Spinbox 1: {value1}, Spinbox 2: {value2}")
        # Add code to handle the new values from the spinboxes

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
