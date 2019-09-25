import tkinter as tk
master = tk.Tk()

w = tk.Canvas(master, width=800, height=420)
w.pack()

#w.create_line(0, 0, 200, 100)
#w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))

w.create_rectangle(0, 1, 800, 210, fill="blue")
w.create_rectangle(0, 210, 800, 480, fill="green")

tk.mainloop()
