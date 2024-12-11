import serial
import time
import pandas as pd

serial_port = "/dev/cu.usbmodem101"
serial_baud = 9600

def serial_read(port, baud, num_samples=100):
    """
    Reads impedance data from the serial port.

    Args:
        port (str): Serial port to connect to.
        baud (int): Baud rate for the connection.
        num_samples (int): Number of data samples to read.

    Returns:
        list: List of impedance values.
    """
    impedance = []
    with serial.Serial(port, baud, timeout=3.0) as ser:
        time.sleep(2)
        ser.write(b'C')  # Send command
        time.sleep(2)
        for _ in range(num_samples):
            try:
                data_read = ser.readline().strip()
                impedance.append(float(data_read))
            except ValueError:
                print(f"Invalid data: {data_read}")
    return impedance

def save_to_csv(data, file_name):
    """
    Saves a list of data to a CSV file.

    Args:
        data (list): Data to save.
        file_name (str): Name of the output CSV file.
    """
    pd.DataFrame(data, columns=["Impedance"]).to_csv(file_name, index=False)
    print(f"Impedance data saved to {file_name}")

if __name__ == "__main__":
    impedance_data = serial_read(serial_port, serial_baud)
    save_to_csv(impedance_data, "impedance_data.csv")