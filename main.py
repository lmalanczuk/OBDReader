import tkinter as tk
from obd import OBD, commands

class OBDInterface:
    def __init__(self, master):
        self.master = master
        master.title("OBD-II Interface")
        self.port = "COM3"

        # Inicjalizacja połączenia OBD
        self.connection = OBD(self.port)

        # Utworzenie etykiety nagłówkowej
        self.label = tk.Label(master, text="OBD-II Interface", bg="blue", fg="white", font=("Helvetica", 24, "bold"))
        self.label.pack()

        # Przyciski do obsługi różnych funkcji OBD
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

        # Etykiety dla danych w czasie rzeczywistym
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

        # Zmienne do obliczeń zużycia paliwa
        self.last_fuel_level = None
        self.total_fuel_consumed = 0.0

        # Aktualizacja danych w czasie rzeczywistym
        self.update_real_time_data()

    def update_real_time_data(self):
        # Pobranie danych z OBD i aktualizacja etykiet
        speed = self.connection.query(commands.SPEED).value
        rpm = self.connection.query(commands.RPM).value
        throttle_position = self.connection.query(commands.THROTTLE_POS).value
        fuel_level = self.connection.query(commands.FUEL_LEVEL).value
        oil_temp = self.connection.query(commands.COOLANT_TEMP).value

        self.speed_label.config(text=f"Prędkość: {speed} km/h")
        self.rpm_label.config(text=f"Obroty silnika: {rpm} RPM")
        self.throttle_label.config(text=f"Pozycja gazu: {throttle_position}%")
        self.fuel_label.config(text=f"Poziom paliwa: {fuel_level}%")
        self.coolant_label.config(text=f"Temperatura płynu chłodniczego: {oil_temp} °C")

        # Sprawdzenie, czy mamy poprzedni odczyt poziomu paliwa do obliczeń
        if self.last_fuel_level is not None:
            fuel_consumed = self.last_fuel_level - fuel_level
            self.total_fuel_consumed += fuel_consumed

        # Aktualizacja ostatniego odczytu poziomu paliwa do następnego obliczenia
        self.last_fuel_level = fuel_level

        # Zaplanowanie kolejnej aktualizacji po 1000 milisekundach (1 sekunda)
        self.master.after(1000, self.update_real_time_data)

    def display_errors(self):
        try:
            errors = self.connection.query(commands.GET_DTC)
            if len(errors) == 0:
                error_message = "Brak błędów DTC."
            else:
                error_message = "Błędy DTC:\n" + "\n".join(str(error.value) for error in errors)

            self.show_popup("Błędy DTC", error_message)
        except Exception as e:
            # Obsługa błędu podczas pobierania błędów DTC
            error_message2 = f"Błąd podczas pobierania błędów DTC: {e}"
            self.show_popup("Błąd", error_message2)

    def clear_errors(self):
        try:
            self.connection.query(commands.CLEAR_DTC)
            self.show_popup("Usuwanie błędów DTC", "Błędy DTC zostały usunięte.")
        except Exception as e:
            # Obsługa błędu podczas usuwania błędów DTC
            print(f"Błąd podczas usuwania błędów DTC: {e}")
            self.show_popup("Usuwanie błędów DTC", f"Błąd podczas usuwania błędów DTC: {e}")

    def display_data(self):
        # Pobranie danych OBD i wyświetlenie ich w oknie popup
        speed = self.connection.query(commands.SPEED).value
        rpm = self.connection.query(commands.RPM).value
        throttle_position = self.connection.query(commands.THROTTLE_POS).value

        data_message = f"Prędkość: {speed} km/h\nObroty silnika: {rpm} RPM\nPozycja gazu: {throttle_position}%"
        self.show_popup("Dane OBD-II", data_message)

    def display_fuel_level(self):
        # Wyświetlenie poziomu paliwa w oknie popup
        fuel_level = self.connection.query(commands.FUEL_LEVEL).value
        self.show_popup("Poziom paliwa", f"Poziom paliwa: {fuel_level}%")

    def display_coolant_temperature(self):
        # Wyświetlenie temperatury płynu chłodniczego w oknie popup
        oil_temp = self.connection.query(commands.COOLANT_TEMP).value
        self.show_popup("Temperatura płynu chłodniczego", f"Temperatura płynu chłodniczego: {oil_temp} °C")

    def display_throttle_position(self):
        # Wyświetlenie pozycji gazu w oknie popup
        throttle_position = self.connection.query(commands.THROTTLE_POS).value
        self.show_popup("Pozycja gazu", f"Pozycja gazu: {throttle_position}%")

    def calculate_fuel_consumption(self):
        if self.total_fuel_consumed == 0.0:
            self.show_popup("Spalone paliwo", "Brak danych do obliczeń.")
        else:
            self.show_popup("Spalone paliwo", f"Spalone paliwo: {self.total_fuel_consumed:.2f} litrów")

    def show_popup(self, title, message):
        # Wyświetlenie okna popup z odpowiednim tytułem i wiadomością
        popup = tk.Toplevel(self.master)
        popup.title(title)
        popup.geometry("400x250")

        label = tk.Label(popup, text=message, font=("Helvetica", 14))
        label.pack()

        ok_button = tk.Button(popup, text="OK", command=popup.destroy, bg="blue", fg="white", font=("Helvetica", 14))
        ok_button.pack()

if __name__ == "__main__":
    # Uruchomienie głównego okna programu
    root = tk.Tk()
    obd_interface = OBDInterface(root)
    root.geometry("800x600")  # Ustawienie początkowego rozmiaru okna
    root.mainloop()
