import time
import tkinter
import math
from PIL import Image, ImageTk
from sense_hat import SenseHat

class SimpleApp(object):
    def __init__(self, master, filename, **kwargs):
        self.master = master
        self.filename = filename
        self.canvas = tkinter.Canvas(master, width=900, height=450)
        self.canvas.pack()

        self.process_next_frame = self.draw().__next__  # Using "next(self.draw())" doesn't work
        master.after(1, self.process_next_frame)
        
    def draw(self):
        image = Image.open(self.filename)
        angle = 0
        print(self.process_next_frame)
        sense = SenseHat()
        #sense.set_rotation(180)
        sense.set_imu_config(True, True, False)
        sense.clear()
        while True:
            o = sense.get_orientation()
            pitch = o["pitch"]
            roll = o["roll"]
            yaw = o["yaw"]
            print("RAW - Pitch: {0}, Roll: {1}, Yaw: {2}".format(pitch,roll,yaw))
                  
            rollAngle = self.roundToStablize(roll)
            #rowAngle %= 360
            #print("roll: {0}".format(rollAngle))
            
            pitchAngle = self.roundToStablize(pitch)
            #pitchAngle %= 360
            pitchAngle = pitchAngle+20# - 90
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
        roundTo = 2
        return int(roundTo * round(float(angle)/roundTo));
    
    
root = tkinter.Tk()
app = SimpleApp(root, 'bg.png')
root.mainloop()