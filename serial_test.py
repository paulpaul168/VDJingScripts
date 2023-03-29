import serial
import time
import tkinter as tk

# create a tkinter window to display the color
window = tk.Tk()
window.geometry("200x200")
color_square = tk.Canvas(window, width=200, height=200)
color_square.pack()

# open the serial port
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

while True:
    # read a line of data from the serial port
    data = ser.readline().decode().strip()

    # check if the line is in the correct format
    if data.startswith('RGB values: '):
        try:
            # extract the RGB values from the line
            r, g, b = map(int, data[12:].split(','))

            # create a hex color string from the RGB values
            color = f'#{r:02x}{g:02x}{b:02x}'

            # set the background color of the square to the received color
            color_square.configure(bg=color)
            window.update()

        except ValueError:
            # ignore any bad formatted lines
            pass

    # wait a short time before reading the next line of data
    time.sleep(0.01)

# close the serial port
ser.close()
