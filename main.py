import tkinter as tk
from obd import OBD, commands

class OBDInterface:
    def __init__(self, master):
        self.master = master
        master.title("OBD-II Interface")
        port = "COM3"

        self.connection = OBD(port)

        # GUI elements
        self.label = tk.Label(master, text="OBD-II Interface")
        self.label.pack()

        self.error_button = tk.Button(master, text="Błędy DTC", command=self.display_errors)
        self.error_button.pack()

        self.data_button = tk.Button(master, text="Pobierz dane", command=self.display_data)
        self.data_button.pack()

    def display_errors(self):
        errors = self.connection.query(commands.GET_DTC)
        error_message = "Błędy DTC:\n" + "\n".join(str(error) for error in errors)
        self.show_popup("Błędy DTC", error_message)

    def display_data(self):
        speed = self.connection.query(commands.SPEED)
        rpm = self.connection.query(commands.RPM)
        throttle_position = self.connection.query(commands.THROTTLE_POS)

        data_message = f"Prędkość: {speed} km/h\nObroty silnika: {rpm} RPM\nPozycja gazu: {throttle_position}%"
        self.show_popup("Dane OBD-II", data_message)

    def show_popup(self, title, message):
        popup = tk.Toplevel(self.master)
        popup.title(title)
        popup.geometry("300x150")

        label = tk.Label(popup, text=message)
        label.pack()

        ok_button = tk.Button(popup, text="OK", command=popup.destroy)
        ok_button.pack()


if __name__ == "__main__":
    root = tk.Tk()
    obd_interface = OBDInterface(root)
    root.mainloop()