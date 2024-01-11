import tkinter as tk
from obd import OBD, commands

class OBDInterface:
    def __init__(self, master):
        self.master = master
        master.title("OBD-II Interface")
        self.port = "COM3"

        self.connection = OBD(self.port)

        # GUI elements
        self.label = tk.Label(master, text="OBD-II Interface", bg="blue", fg="white", font=("Helvetica", 24, "bold"))
        self.label.pack()

        self.error_button = tk.Button(master, text="Błędy DTC", command=self.display_errors, bg="red", fg="white", font=("Helvetica", 16))
        self.error_button.pack()

        self.clear_errors_button = tk.Button(master, text="Usuń błędy DTC", command=self.clear_errors, bg="orange", fg="white", font=("Helvetica", 16))
        self.clear_errors_button.pack()

        self.data_button = tk.Button(master, text="Pobierz dane", command=self.display_data, bg="green", fg="white", font=("Helvetica", 16))
        self.data_button.pack()

        self.fuel_button = tk.Button(master, text="Poziom paliwa", command=self.display_fuel_level, bg="orange", fg="white", font=("Helvetica", 16))
        self.fuel_button.pack()

        self.coolant_button = tk.Button(master, text="Temperatura płynu chłodniczego", command=self.display_coolant_temperature, bg="purple", fg="white", font=("Helvetica", 16))
        self.coolant_button.pack()

        self.throttle_button = tk.Button(master, text="Pozycja gazu", command=self.display_throttle_position, bg="brown", fg="white", font=("Helvetica", 16))
        self.throttle_button.pack()

        self.calculate_consumption_button = tk.Button(master, text="Oblicz spalone paliwo", command=self.calculate_fuel_consumption, bg="blue", fg="white", font=("Helvetica", 16))
        self.calculate_consumption_button.pack()

        # Real-time data labels
        self.speed_label = tk.Label(master, text="Prędkość: ", bg="lightgray", font=("Helvetica", 18))
        self.speed_label.pack()

        self.rpm_label = tk.Label(master, text="Obroty silnika: ", bg="lightgray", font=("Helvetica", 18))
        self.rpm_label.pack()

        self.throttle_label = tk.Label(master, text="Pozycja gazu: ", bg="lightgray", font=("Helvetica", 18))
        self.throttle_label.pack()

        self.fuel_label = tk.Label(master, text="Poziom paliwa: ", bg="lightgray", font=("Helvetica", 18))
        self.fuel_label.pack()

        self.coolant_label = tk.Label(master, text="Temperatura płynu chłodniczego: ", bg="lightgray", font=("Helvetica", 18))
        self.coolant_label.pack()

        # Variables for calculating fuel consumption
        self.last_fuel_level = None
        self.total_fuel_consumed = 0.0

        # Update real-time data periodically
        self.update_real_time_data()

    def update_real_time_data(self):
        speed = self.connection.query(commands.SPEED).value
        rpm = self.connection.query(commands.RPM).value
        throttle_position = self.connection.query(commands.THROTTLE_POS).value
        fuel_level = self.connection.query(commands.FUEL_LEVEL).value
        coolant_temp = self.connection.query(commands.COOLANT_TEMP).value

        self.speed_label.config(text=f"Prędkość: {speed} km/h")
        self.rpm_label.config(text=f"Obroty silnika: {rpm} RPM")
        self.throttle_label.config(text=f"Pozycja gazu: {throttle_position}%")
        self.fuel_label.config(text=f"Poziom paliwa: {fuel_level}%")
        self.coolant_label.config(text=f"Temperatura płynu chłodniczego: {coolant_temp} °C")

        # Check if we have a previous fuel level reading to calculate consumption
        if self.last_fuel_level is not None:
            fuel_consumed = self.last_fuel_level - fuel_level
            self.total_fuel_consumed += fuel_consumed

        # Update last fuel level for the next calculation
        self.last_fuel_level = fuel_level

        # Schedule the next update after 1000 milliseconds (1 second)
        self.master.after(1000, self.update_real_time_data)

    def display_errors(self):
        try:
            errors = self.connection.query(commands.GET_DTC)
            error_message = "Błędy DTC:\n" + "\n".join(str(error.value) for error in errors)
            self.show_popup("Błędy DTC", error_message)
        except Exception as e:
            print(f"Error retrieving DTC: {e}")

    def clear_errors(self):
        try:
            self.connection.query(commands.CLEAR_DTC)
            self.show_popup("Usuwanie błędów DTC", "Błędy DTC zostały usunięte.")
        except Exception as e:
            print(f"Error clearing DTC: {e}")
            self.show_popup("Usuwanie błędów DTC", f"Błąd podczas usuwania błędów DTC: {e}")

    def display_data(self):
        speed = self.connection.query(commands.SPEED).value
        rpm = self.connection.query(commands.RPM).value
        throttle_position = self.connection.query(commands.THROTTLE_POS).value

        data_message = f"Prędkość: {speed} km/h\nObroty silnika: {rpm} RPM\nPozycja gazu: {throttle_position}%"
        self.show_popup("Dane OBD-II", data_message)

    def display_fuel_level(self):
        fuel_level = self.connection.query(commands.FUEL_LEVEL).value
        self.show_popup("Poziom paliwa", f"Poziom paliwa: {fuel_level}%")

    def display_coolant_temperature(self):
        coolant_temp = self.connection.query(commands.COOLANT_TEMP).value
        self.show_popup("Temperatura płynu chłodniczego", f"Temperatura płynu chłodniczego: {coolant_temp} °C")

    def display_throttle_position(self):
        throttle_position = self.connection.query(commands.THROTTLE_POS).value
        self.show_popup("Pozycja gazu", f"Pozycja gazu: {throttle_position}%")

    def calculate_fuel_consumption(self):
        if self.total_fuel_consumed == 0.0:
            self.show_popup("Spalone paliwo", "Brak danych do obliczeń.")
        else:
            self.show_popup("Spalone paliwo", f"Spalone paliwo: {self.total_fuel_consumed:.2f} litrów")

    def show_popup(self, title, message):
        popup = tk.Toplevel(self.master)
        popup.title(title)
        popup.geometry("400x250")

        label = tk.Label(popup, text=message, font=("Helvetica", 14))
        label.pack()

        ok_button = tk.Button(popup, text="OK", command=popup.destroy, bg="blue", fg="white", font=("Helvetica", 14))
        ok_button.pack()

if __name__ == "__main__":
    root = tk.Tk()
    obd_interface = OBDInterface(root)
    root.geometry("800x600")  # Set the initial window size
    root.mainloop()
