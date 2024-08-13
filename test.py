import time
import board
import digitalio
import modbus_tk
import modbus_tk.modbus_rtu as modbus_rtu
import serial
import json
import requests

# Set up GPIO 17 as an input with a pull-down resistor
button = digitalio.DigitalInOut(board.D17)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.DOWN

# Initialize Modbus RTU client
master = modbus_rtu.RtuMaster(
    serial.Serial(port='/dev/serial0', baudrate=4800, bytesize=8, parity='N', stopbits=1)
)
master.set_timeout(5.0)  # Set a timeout for the response
master.set_verbose(True)  # Enable verbose mode for debugging

def read_and_send_registers():
    try:
        # Read holding registers
        response = master.execute(1, modbus_tk.defines.READ_HOLDING_REGISTERS, 500, 14)
        data = {'register_values': response}
        json_data = json.dumps(data)
        print(f"Register values: {json_data}")

        # Send data via API call
        url = f'http://192.168.1.111:5000/weatherdata?data={json_data}'
        response = requests.get(url)
        print(f"Server response: {response.text}")

        # Write register to reset optical rainfall sensor
        write_command = [0x5A]
        master.execute(1, modbus_tk.defines.WRITE_SINGLE_REGISTER, 0x6002, output_value=write_command[0])
        print("Optical rainfall sensor reset.")

    except modbus_tk.modbus.ModbusError as e:
        print(f"Modbus Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

# Initial states
last_button_state = button.value
last_read_time = time.monotonic()

while True:
    current_time = time.monotonic()
    button_state = button.value

    # Check if the button was pressed
    if button_state and not last_button_state:
        print("Button pressed! Triggering register read...")
        read_and_send_registers()
        last_read_time = current_time  # Reset last read time on button press

    # Perform register read every 3 minutes
    if (current_time - last_read_time) >= 180:
        print("3 minutes elapsed. Triggering register read...")
        read_and_send_registers()
        last_read_time = current_time  # Update last read time

    # Update the last button state
    last_button_state = button_state
    time.sleep(0.1)  # Small delay to avoid busy-waiting
