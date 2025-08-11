import pyvisa
import time
import csv

def connect_to_scope_usb(resource_string):
    rm = pyvisa.ResourceManager()
    scope = rm.open_resource(resource_string)
    scope.timeout = 2000
    return scope

def measure_voltage_ch1(scope):
    voltage_str = scope.query("MEASure:VMAX? CHAN1").strip()
    try:
        return float(voltage_str)
    except ValueError:
        return None

def main():
    # Ersetze den resource_string mit dem tatsächlichen USB-Resource-String deines Oszilloskops
    # NI-VISA kann den Resource-String anzeigen, wenn du das Oszilloskop verbindest
    resource_string = "USB0::0x1AB1::0x044C::DHO9S264505065::INSTR"
    scope = connect_to_scope_usb(resource_string)

    filename = "oszi_measure.csv"

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Voltage (V)"])

        try:
            while True:
                voltage = measure_voltage_ch1(scope)
                if voltage is not None:
                    # Sicherer Timestamp, den Excel nicht kaputt formatiert
                    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
                    print(f"{timestamp} - Voltage CH1: {voltage:.3f} V")
                    writer.writerow([timestamp, voltage])
                    file.flush()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nFinished measurement.")

if __name__ == "__main__":
    main()
