import time
import tkinter
import math
from PIL import Image, ImageTk
from sense_hat import SenseHat

class GlassAvionics(object):
    pressureSetting = 30.00
    bankOffset = 0
    pitchOffset = 0
    
    def __init__(self, master, filename, plane, **kwargs):
        self.master = master
        self.filename = filename
        self.plane = plane
        self.root = root
        self.canvas = tkinter.Canvas(master, width=650, height=400)
        self.canvas.grid(row=0, column=2, columnspan=3, rowspan=7)

        self.process_next_frame = self.draw().__next__  # Using "next(self.draw())" doesn't work
        master.after(1, self.process_next_frame)
        
    def pressureUp(self):
        self.pressureSetting = round(self.pressureSetting+.01,2)
        return;
    
    def pressureDwn(self):
        self.pressureSetting = round(self.pressureSetting-.01,2)
        return;
        
    def bankLeft(self):
        self.bankOffset = self.bankOffset + 1
        return
    
    def bankRight(self):
        self.bankOffset = self.bankOffset - 1
        return
        
    def pitchUp(self):
        self.pitchOffset = self.pitchOffset + 1
        return
        
    def pitchDwn(self):
        self.pitchOffset = self.pitchOffset - 1
        return
    
    
    def draw(self):
        image = Image.open(self.filename)
        imagePlane = Image.open(self.plane)
        v = tkinter.StringVar()
        label = tkinter.Label( root, textvariable=v )
        label.config(font=("Courier", 20))
        label.grid(row=1, column=0, columnspan=2, rowspan=1)
        v.set("")
        
        vSet = tkinter.StringVar()
        labelSet = tkinter.Label( root, textvariable=vSet )
        labelSet.config(font=("Courier", 12))
        labelSet.grid(row=2, column=0, columnspan=2, rowspan=1)
        v.set("")
        
        pressureUpBtn = tkinter.Button(root, text="Pressure Up", command=self.pressureUp)
        pressureUpBtn.grid(row=0, column=0, columnspan=2)
        pressureUpBtn = pressureUpBtn.config( height = 3, width = 15 )
        
        pressureDwnBtn = tkinter.Button(root, text="Pressure Down", command=self.pressureDwn)    
        pressureDwnBtn.grid(row=3, column=0, columnspan=2)
        pressureDwnBtn = pressureDwnBtn.config( height = 3, width = 15 )
        
        bankLeftBtn = tkinter.Button(root, text="< Roll", command=self.bankLeft)    
        bankLeftBtn.grid(row=5, column=0, columnspan=1)
        bankLeftBtn = bankLeftBtn.config( height = 1, width = 5 )
        
        bankRightBtn = tkinter.Button(root, text="Roll >", command=self.bankRight)    
        bankRightBtn.grid(row=5, column=1)
        bankRightBtn = bankRightBtn.config( height = 1, width = 5 )
        
        pitchUpBtn = tkinter.Button(root, text="+Pitch", command=self.pitchUp)    
        pitchUpBtn.grid(row=4, column=0)
        pitchUpBtn = pitchUpBtn.config( height = 1, width = 5 )
        
        pitchDwnBtn = tkinter.Button(root, text="-Pitch", command=self.pitchDwn)    
        pitchDwnBtn.grid(row=4, column=1)
        pitchDwnBtn = pitchDwnBtn.config( height = 1, width = 5 )
        
        ##showHideBtn = tkinter.Button(root, text="Hide", command=self.showHide)    
        #showHideBtn.grid(row=4, column=0)
        #showHideBtn = showHideBtn.config( height = 3, width = 15 )
    
        angle = 0
        #print(self.process_next_frame)
        sense = SenseHat()
        #sense.set_rotation(180)
        sense.set_imu_config(True, True, True)
        sense.clear()
        while True:
            pressure = sense.get_pressure()
            #AS = 30.19
            pressInHG = pressure * 0.02953 #convet from milibar to inHG
            #print(pressInHG)
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
                  
            rollAngle = self.roundToStablize(roll-90) + self.bankOffset
            #rowAngle %= 360
            #print("roll: {0}".format(rollAngle))
            
            pitch = pitch%180
            pitchAngle = pitch#self.roundToStablize(pitch)
            #pitchAngle %= 360
            pitchAngle = pitchAngle + self.pitchOffset
            #center screen with 450 height 225
            pitchOffset = (math.tan(math.radians(pitchAngle)))*2
            pitchOffsetPx = pitchOffset * 112 #112 px per inch
            #print("pitch: {0}, offset: {1}, roll: {2}".format(pitchAngle,pitchOffset,rollAngle))
            tkimage = ImageTk.PhotoImage(image.rotate(rollAngle))
            planeImage = ImageTk.PhotoImage(imagePlane)        
            canvas_obj = self.canvas.create_image(300, 225+pitchOffsetPx, image=tkimage)
            canvas_obj2 = self.canvas.create_image(325, 200, image=planeImage)
            self.master.after_idle(self.process_next_frame)
            yield
            self.canvas.delete(canvas_obj)
            time.sleep(0.0009)
            
            
    def roundToStablize(self, angle):
        roundTo = 5
        return int(roundTo * round(float(angle)/roundTo));
    
    
root = tkinter.Tk()

app = GlassAvionics(root, 'bg.png', 'plane.png')
root.mainloop()
