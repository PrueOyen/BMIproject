import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

#Creating the Function that will calculate the BMI
def calculate_bmi(weight, height):
    return weight / (height / 100) ** 2

#Creating the Function of the BMI categorizes
def bmi_category(bmi):
    if bmi < 18.5:
        return 'Underweight'
    elif 18.5 <= bmi < 25:
        return 'Normal'
    elif 25 <= bmi < 30:
        return 'Overweight'
    else:
        return 'Obese'

#Creating the Function to save the inputted data and then calculate the BMI
def save_data():
    full_name = fullNameEntry.get()
    try:
        age = int(ageEntry.get())
        height = float(heightEntry.get())
        weight = float(weightEntry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid age, height, and weight.")
        return

    if not full_name or age <= 0 or height <= 0 or weight <= 0:
        messagebox.showerror("Input Error", "Invalid data provided.")
        return

    bmi = calculate_bmi(weight, height)
    category = bmi_category(bmi)

#Writing to BMI file
    headers = ["FULL NAME", "AGE ", "HEIGHT", "WEIGHT"]
    with open("BMI_DataFile.txt", "a") as file:
        file.write(f"{full_name}\t{age}\t{height}\t{weight}\t{bmi:.2f}\t{category}\n")

    messagebox.showinfo("Data Saved", "Thank You! Your BMI data saved successfully.")
#Clearing the fields after successfully saved
    fullNameEntry.delete(0, tk.END)
    ageEntry.delete(0, tk.END)
    heightEntry.delete(0, tk.END)
    weightEntry.delete(0, tk.END)

#Creating Function to show the graph as Pie chart
def show_graph():
    categories = {'Underweight': 0, 'Normal': 0, 'Overweight': 0, 'Obese': 0}
    try:
        with open("BMI_DataFile.txt", "r") as file:
            for line in file:
                #Skipping empty lines and Strip whitespace
                line = line.strip()
                if not line:
                    continue  #Skip processing if line is empty

                data = line.split('\t')
                category = data[-1]  #Expecting the category in the last column

                #Checking if the category is valid before incrementing count
                if category in categories:
                    categories[category] += 1
                else:
                    print(f"Warning: Unexpected category '{category}' found. Skipping.")
    except FileNotFoundError:
        messagebox.showerror("Error", "Data file not found.")
        return
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return

    #Passing the keys as a list
    labels = list(categories.keys())
    sizes = list(categories.values())

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  #The Equal key word ensures that pie is drawn as a circle.
    ax.set_title("Prudence's BMI Category Distribution")  # Setting the title for the plot

    canvas = FigureCanvasTkAgg(fig, master=BMI_window)  #A tk.Drawing Area.
    #canvas.title("Prudence BMI Pie Chart")
    canvas.draw()
    canvas.get_tk_widget().grid(row=5, column=0, columnspan=4)


#Main window configuration
BMI_window = tk.Tk()
BMI_window.title("Prudence's BMI Calculator")

#Entry data for the person's Name field
tk.Label(BMI_window, text="Full Name:").grid(row=0, column=0)
fullNameEntry = tk.Entry(BMI_window)
fullNameEntry.grid(row=0, column=1)

#Entry data for the person's Age field
tk.Label(BMI_window, text="Age:").grid(row=1, column=0)
ageEntry = tk.Entry(BMI_window)
ageEntry.grid(row=1, column=1)

#Entry data for the person's Height (in cm)
tk.Label(BMI_window, text="Height (in cm):").grid(row=2, column=0)
heightEntry = tk.Entry(BMI_window)
heightEntry.grid(row=2, column=1)

#Entry data for the person's Weight (in kg)
tk.Label(BMI_window, text="Weight (in kg):").grid(row=3, column=0)
weightEntry = tk.Entry(BMI_window)
weightEntry.grid(row=3, column=1)

#Creating Save Button
saveButton = tk.Button(BMI_window, text="Save Data", command=save_data)
saveButton.grid(row=4, column=0)

#Showing Graph Button on the same BMI window
graphButton = tk.Button(BMI_window, text="Show Graph", command=show_graph)
graphButton.grid(row=4, column=1)


BMI_window.mainloop()
