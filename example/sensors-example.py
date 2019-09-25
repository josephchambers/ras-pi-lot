from sense_hat import SenseHat

sense = SenseHat()
sense.clear()
blue = (0, 0, 255)
yellow = (255, 255, 0)
while True:
    acceleration = sense.get_accelerometer_raw()
    x = acceleration['x']
    y = acceleration['y']
    z = acceleration['z']

    x=round(x, 0)
    y=round(y, 0)
    z=round(z, 0)

    print("x={0}, y={1}, z={2}".format(x, y, z))
    
    pressure = sense.get_pressure()
    print(pressure)
    #sense.show_message(str(pressure), text_colour=yellow, back_colour=blue, scroll_speed=0.05)
    
    o = sense.get_orientation()
    pitch = o["pitch"]
    roll = o["roll"]
    yaw = o["yaw"]
    print("pitch {0} roll {1} yaw {2}".format(pitch, roll, yaw))

    dir = sense.get_compass()
    print("direction {0}".format(dir))
