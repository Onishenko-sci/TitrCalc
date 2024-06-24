import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
import numpy as np
import os

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter and Matplotlib Example")

        self.curves = 0
        self.file_name = ''
        self.row_count = 0

        # Create a left frame for buttons and spinboxes
        self.left_frame = tk.Frame(root)
        self.left_frame.grid(row=0, column=0, sticky="n")

        # Create a button to open file dialog
        self.open_button = tk.Button(self.left_frame, text="Open File", command=self.open_file)
        self.open_button.grid(row=0, column=0, pady=5, padx=5)

        # Create Spinboxes with trace on their variables
        self.spinbox1_label = tk.Label(self.left_frame, text="Первый шаг:")
        self.spinbox1_label.grid(row=1, column=0, pady=5, padx=5)
        
        self.spinbox1_var = tk.StringVar()
        self.spinbox1 = tk.Spinbox(self.left_frame, from_=0, to=1000, textvariable=self.spinbox1_var, command=self.spinbox_changed)
        self.spinbox1.grid(row=2, column=0, pady=5, padx=5)
        self.spinbox1_var.trace_add("write", lambda *args: self.spinbox_changed())

        self.spinbox2_label = tk.Label(self.left_frame, text="Последний шаг:")
        self.spinbox2_label.grid(row=3, column=0, pady=5, padx=5)
        
        self.spinbox2_var = tk.StringVar()
        self.spinbox2 = tk.Spinbox(self.left_frame, from_=0, to=1000, textvariable=self.spinbox2_var, command=self.spinbox_changed)
        self.spinbox2.grid(row=4, column=0, pady=5, padx=5)
        self.spinbox2_var.trace_add("write", lambda *args: self.spinbox_changed())

        # Create checkbox for DChrj
        self.dchrj_var = tk.BooleanVar()
        self.dchrj_checkbox = tk.Checkbutton(self.left_frame, text="Разряд", variable=self.dchrj_var)
        self.dchrj_checkbox.grid(row=5, column=0, pady=5, padx=5)

        # Create entries for additional parameters
        self.layer_thickness_label = tk.Label(self.left_frame, text="Толщина слоя:")
        self.layer_thickness_label.grid(row=6, column=0, pady=5, padx=5)
        self.layer_thickness_entry = tk.Entry(self.left_frame)
        self.layer_thickness_entry.grid(row=7, column=0, pady=5, padx=5)
        self.layer_thickness_entry.insert(0, "0.054")

        # Create a button for calculation
        self.calculate_button = tk.Button(self.left_frame, text="Расчет", command=self.calculate)
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
        self.file_name = os.path.basename(file_path)

        mode = 'Rest'
        with open(file_path, 'r') as file:
            # Create a CSV reader object
            csv_reader = csv.reader(file, delimiter=',')
            self.row_count = sum(1 for row in csv_reader)
            data = np.zeros((3, self.row_count-1))
            i = 0
            file.seek(0)
            # Iterate over each row in the CSV file
            for row in csv_reader:
                # Each row is a list of values corresponding to the columns
                if i != 0:
                    data[0, i-1] = int(row[0])
                    data[1, i-1] = float(row[9] + '.' + row[10])
                    if mode != row[4]:
                        mode = row[4]
                        data[2, i-2] = 1
                i += 1
        
        indexes = np.where(data[2, :] == 1)[0]
        self.points = data[:, indexes]
        last_point = self.points.shape[1]-1

        self.curves = data
        self.spinbox1_var.set(0)
        self.spinbox2_var.set(last_point)

        self.spinbox1.config(to=last_point)
        self.spinbox2.config(to=last_point)

        self.update_plot()

    def update_plot(self):
        if self.file_name == '':
            print("No chosen file")
            return
        # Function to update the plot
        self.ax.clear()
        # Example: Generating a simple plot based on the input parameters
        # In a real application, you would use the parameters to calculate data to plot
        value1 = int(self.spinbox1_var.get())
        value2 = int(self.spinbox2_var.get())

        drow = self.curves
        print(self.points[:,2])
        self.ax.plot(drow[0,:], drow[1,:], linestyle='-', color='b')
        self.ax.scatter(self.points[0, :], self.points[1, :], marker='o', color='r')

        self.ax.axvline(self.points[0,value1], color='g', linestyle='--', linewidth=2)
        self.ax.axvline(self.points[0,value2], color='y', linestyle='--', linewidth=2)

        self.ax.set_title(self.file_name)
        self.ax.legend()
        self.canvas.draw()

    def calculate(self):
        data = self.curves
        self.L =float(self.layer_thickness_entry.get())

        value1 = int(self.spinbox1_var.get())
        value2 = int(self.spinbox2_var.get())

        indexes = np.where(data[2, :] == 1)[0]

        points = data[:, indexes]
        ir_hop = data[:, indexes+2]
        max1 = points[:, ::2]
        min3 = points[:, 1::2]
        ir_hop2 = ir_hop[:, ::2]
        ir_hop0 = ir_hop[:, 1::2]
        print(f'L=;{self.L};')
        print('n;0;1;2;3;dEt;dEs;D;Critical factor (>>t_step);')
        diff_data = []
        for i in range(max1.shape[1]-1):
            if self.dchrj_var.get():
                dEs = max1[1, i]-max1[1, i+1]
                dEt = ir_hop2[1, i]-min3[1, i]
            else:
                dEs = min3[1, i+1]-min3[1, i]
                dEt = max1[1, i]-ir_hop0[1, i]

            D = (4*self.L**2)/(np.pi*3600)*(dEs/dEt)**2
            crit = self.L**2/D
            diff_data.append([i+1, ir_hop0[1, i], max1[1, i], ir_hop2[1, i], min3[1, i], dEt, dEs, D, crit])
            print(i+1, ' ;', ir_hop0[1, i], ';', max1[1, i], ' ;', ir_hop2[1, i], ' ;',
                min3[1, i], ' ;', dEt, ' ;', dEs, ' ;', D, ' ;', crit, ';')
        
        diff_data = np.array(diff_data)

        # Create a new top-level window
        new_window = tk.Toplevel(self.root)
        new_window.title(self.file_name)

        # Add a table to the new window
        columns = ("N", "0", "1", "2", "3", "dEt", "dEs", "D", "Critical factor")
        tree = ttk.Treeview(new_window, columns=columns, show="headings")
        tree.heading("N", text="N")
        tree.heading("0", text="0")
        tree.heading("1", text="1")
        tree.heading("2", text="2")
        tree.heading("3", text="3")
        tree.heading("dEt", text="dEt")
        tree.heading("dEs", text="dEs")
        tree.heading("D", text="D")
        tree.heading("Critical factor", text="Critical factor")

        for row in diff_data:
            formatted_row = [int(row[0])] + ["{:.4f}".format(value) if isinstance(value, float) else value for value in row[1:7]] + ["{:.7g}".format(row[7]), "{:.7g}".format(row[8])]
            tree.insert("", tk.END, values=formatted_row)

        tree.pack(pady=10)

        # Add a Matplotlib graph to the new window
        fig, ax = plt.subplots()
        ax.plot(diff_data[:,0], diff_data[:,7], linestyle='' , marker='o', color='r')
        ax.set_title(self.file_name)

        canvas = FigureCanvasTkAgg(fig, master=new_window)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

        # Close button for the new window
        close_button = tk.Button(new_window, text="Close", command=new_window.destroy)
        close_button.pack(pady=10)

        close_button = tk.Button(new_window, text="Save in CSV", command=self.save_to_csv)
        close_button.pack(pady=10)

    def save_to_csv(self):
        # Открываем диалоговое окно для выбора места сохранения файла
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        
        if file_path:
            # Сохраняем данные в CSV файл
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                # Записываем заголовок
                writer.writerow(["L = " + str(self.L)])
                writer.writerow(["N", "0", "1", "2", "3", "dEt", "dEs", "D", "Critical factor"])
                # Записываем данные
                for row in self.output_array:
                    writer.writerow(row)


    def spinbox_changed(self):
        self.update_plot()
        # Add code to handle the new values from the spinboxes




if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
