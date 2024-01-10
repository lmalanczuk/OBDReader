import obd
import tkinter as tk

connection = obd.OBD()

cmd = obd.commands.SPEED # select an OBD command (sensor)

response = connection.query(cmd) # send the command, and parse the response
print(response.value) # returns unit-bearing values thanks to Pint