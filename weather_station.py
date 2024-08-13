from time import strftime,localtime
import json
import sqlite3
def weather_station_data(data):
    parsed_data= json.loads(data)
    register_values = parsed_data.get("register_values",[])
    AS3935=parsed_data.get("As")

    mac_id = "84:FC:E6:7B:E0:E8"

    try:
        # Parse the hex data

        wind_speed = register_values[0]
        print(wind_speed)
        wind_speed = round((wind_speed / 100), 2)
        print(wind_speed)

        wind_force = register_values[1]
        wind_force = round(wind_force, 2)

        wind_direction = register_values[2]
        wind_direction = round(wind_direction, 2)

        wind_direction_2 = register_values[3]

        humidity = register_values[4]
        humidity = round((humidity / 10), 2)

        temperature = register_values[5]
        temperature = round((temperature / 10), 2)

        noise = register_values[6]
        noise = round((noise / 10), 2)

        pm_25 = register_values[7]
        pm_10 = register_values[8]

        pressure = register_values[9]
        pressure = round((pressure / 10), 2)

        high_lux = register_values[10]
        low_lux = register_values[11]
        light_lux = register_values[12]
        rain = register_values[13]
        rain = round((rain / 10), 2)

        date_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
        print(f'temperature:{temperature},pressure:{pressure},noise:{noise},wind_speed:{wind_speed},wind_direction:{wind_direction},rain:{rain},humidity:{humidity},date:{date_time}')
        with sqlite3.connect("instance/weather-station-database.sqlite") as connection:
            connection.enable_load_extension(True)
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO weather_station (as3935, mac_id, wind_speed, wind_force, wind_direction, humidity, "
                "temperature, pressure, noise, rain, date_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (AS3935, mac_id, wind_speed, wind_force, wind_direction, humidity, temperature, pressure, noise, rain,
                 date_time))

            connection.commit()

    except Exception as e:
        # Handle the error here, you can print the error message or log it
        # print(f"Error saving data to the database: {e}")
        return e  # I