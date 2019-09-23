import time
import tkinter
#import cv2
import math
from PIL import Image, ImageTk
from sense_hat import SenseHat

class GlassAvionics(object):
    pressureSetting = 30.15
    def __init__(self, master, filename, **kwargs):
        self.master = master
        self.filename = filename
        self.root = root;
        self.canvas = tkinter.Canvas(master, width=600, height=400)
        self.canvas.grid(row=0, column=1, columnspan=1, rowspan=4)

        self.process_next_frame = self.draw().__next__  # Using "next(self.draw())" doesn't work
        master.after(1, self.process_next_frame)
        
    def pressureUp(self):
        self.pressureSetting = round(self.pressureSetting+.01,2)
        return;
    
    def pressureDwn(self):
        self.pressureSetting = round(self.pressureSetting-.01,2)
        return;
    
    def draw(self):
        image = Image.open(self.filename)
        v = tkinter.StringVar()
        label = tkinter.Label( root, textvariable=v )
        label.config(font=("Courier", 20))
        label.grid(row=1, column=0)
        v.set("")
        
        vSet = tkinter.StringVar()
        labelSet = tkinter.Label( root, textvariable=vSet )
        labelSet.config(font=("Courier", 12))
        labelSet.grid(row=2, column=0)
        v.set("")
        
        pressureUpBtn = tkinter.Button(root, text="Pressure Up", command=self.pressureUp)
        #pressureUpBtn.bind('<ButtonPress-1>',self.pressureUp)
        pressureUpBtn.grid(row=0, column=0)
        pressureUpBtn = pressureUpBtn.config( height = 3, width = 15 )
        
        pressureDwnBtn = tkinter.Button(root, text="Pressure Down", command=self.pressureDwn)
        #pressureDwnBtn.bind('<ButtonPress-1>',self.pressureDwn)    
        pressureDwnBtn.grid(row=3, column=0)
        pressureDwnBtn = pressureDwnBtn.config( height = 3, width = 15 )
        
        
        angle = 0
        #print(self.process_next_frame)
        sense = SenseHat()
        #sense.set_rotation(180)
        #sense.set_imu_config(True, True, False)
        sense.clear()
        while True:
            pressure = sense.get_pressure()
            #AS = 30.19
            pressInHG = pressure * 0.02953 #convet from milibar to inHG
            print(pressInHG)
            altitude = "ERROR"
            if pressInHG >= 0:
                altitude = round((pow(self.pressureSetting,0.1903) - pow(pressInHG,(1/5.255)))/(1.212*(pow(10,-5))))
            
            #calculate altitude
            #ressInHG is from sensor
            #AS is setting
            vSet.set("Setting:\n{0} inMg".format(self.pressureSetting))
            v.set("Altitude:\n{0}".format(altitude))
            o = sense.get_orientation()
            pitch = o["pitch"]
            roll = o["roll"]
            yaw = o["yaw"]
            #print("RAW - Pitch: {0}, Roll: {1}, Yaw: {2}".format(pitch,roll,yaw))
                  
            rollAngle = self.roundToStablize(roll-90)
            #rowAngle %= 360
            #print("roll: {0}".format(rollAngle))
            
            pitchAngle = self.roundToStablize(pitch)
            #pitchAngle %= 360
            pitchAngle = pitchAngle# - 90
            #center screen with 450 height 225
            pitchOffset = (math.tan(math.radians(pitchAngle)))/0.5
            pitchOffsetPx = pitchOffset * 112 #112 px per inch
            #print("pitch: {0}, offset: {1}, roll: {2}".format(pitchAngle,pitchOffset,rollAngle))
            tkimage = ImageTk.PhotoImage(image.rotate(rollAngle))
        
            canvas_obj = self.canvas.create_image(300, 225+pitchOffsetPx, image=tkimage)
            self.master.after_idle(self.process_next_frame)
            yield
            self.canvas.delete(canvas_obj)
            time.sleep(0.0009)
            
            
    def roundToStablize(self, angle):
        roundTo = 5
        return int(roundTo * round(float(angle)/roundTo));
    
    
root = tkinter.Tk()

app = GlassAvionics(root, 'bg.png')
root.mainloop()