from random import random
import tkinter as tk
from math import sin, cos
from time import sleep

w, h, z = 1000, 1000, 1000
n_parts = 100
n_type = 3
friction = 0.995
br_motion = 0.01
speed = 0.04
radius = 2
m_step = 0.05
scale = 1
s_step = 1.2

parts = [[random()*w-w/2, random()*h-h/2, random()*z-z/2, 0, 0, 0, i%n_type] for i in range(n_parts)] # position, speed and type

angle = [[1,0,0],[0,1,0],[0,0,1]]
def left(event):
    global angle
    angle = [[ang[0]*cos(m_step)+ang[2]*sin(m_step), ang[1], -ang[0]*sin(m_step)+ang[2]*cos(m_step)] for ang in angle]
def right(event):
    global angle
    angle = [[ang[0]*cos(m_step)-ang[2]*sin(m_step), ang[1], ang[0]*sin(m_step)+ang[2]*cos(m_step)] for ang in angle]
def up(event):
    global angle
    angle = [[ang[0], ang[1]*cos(m_step)+ang[2]*sin(m_step), -ang[1]*sin(m_step)+ang[2]*cos(m_step)] for ang in angle]
def down(event):
    global angle
    angle = [[ang[0], ang[1]*cos(m_step)-ang[2]*sin(m_step), ang[1]*sin(m_step)+ang[2]*cos(m_step)] for ang in angle]
def zin(event):
    global scale
    scale *= s_step
def zout(event):
    global scale
    scale /= s_step

# initialize tkinter
root = tk.Tk()
root.bind('<Left>', left)
root.bind('<Right>', right)
root.bind('<Up>', up)
root.bind('<Down>', down)
root.bind('<Button-4>', zin)
root.bind('<Button-5>', zout)
canvas = tk.Canvas(root, width=w, height=h, borderwidth=0, highlightthickness=0, bg="black")
canvas.grid()

# main loop
while True:
    for i in range(n_parts):
        for j in range(i): #for every pair of particles
            dx = parts[i][0] - parts[j][0]
            dy = parts[i][1] - parts[j][1]
            dz = parts[i][2] - parts[j][2]
            d3 = (dx**2 + dy**2 + dz**2)**1.5 #distance
            tx = dx/d3
            ty = dy/d3
            tz = dz/d3
            if parts[i][6] == parts[j][6] or d3 < 4000: #update speeds
                parts[i][3] += radius*tx
                parts[j][3] -= radius*tx
                parts[i][4] += radius*ty
                parts[j][4] -= radius*ty
                parts[i][5] += radius*tz
                parts[j][5] -= radius*tz
            else: #bounce if closer than radius
                parts[i][3] -= tx
                parts[j][3] += tx
                parts[i][4] -= ty
                parts[j][4] += ty
                parts[i][5] -= tz
                parts[j][5] += tz
    
    canvas.delete('all')
    for part in parts: # update positions
        part[3] += speed/(part[0]-w/2) + speed/(part[0]+w/2) + (random()-0.5)*br_motion
        part[4] += speed/(part[1]-h/2) + speed/(part[1]+h/2) + (random()-0.5)*br_motion
        part[5] += speed/(part[2]-z/2) + speed/(part[2]+z/2) + (random()-0.5)*br_motion
        if part[0] < -w/2 or part[0] > w/2: # bounce of borders
            part[3] = -part[3]
        if part[1] < -z/2 or part[1] > h/2:
            part[4] = -part[4]
        if part[2] < -z/2 or part[2] > z/2:
            part[5] = -part[5]
        part[3] *= friction
        part[4] *= friction
        part[5] *= friction
        part[0] += part[3]
        part[1] += part[4]
        part[2] += part[5]
    
    for part in sorted(parts, key=lambda part: -sum([angle[i][2]*part[i] for i in range(3)])):
        size = 1500/(z/2+400+scale*(sum([angle[i][2]*part[i] for i in range(3)])))
        if size > 0:
            px = w/2+scale*(sum([angle[i][0]*part[i] for i in range(3)])) #position on image
            py = h/2+scale*(sum([angle[i][1]*part[i] for i in range(3)])) #position on image
            if part[6] == 0:
                canvas.create_oval(px-size, py-size, px+size, py+size, outline="", fill="blue")
            elif part[6] == 1:
                canvas.create_oval(px-size, py-size, px+size, py+size, outline="", fill="red")
            elif part[6] == 2:
                canvas.create_oval(px-size, py-size, px+size, py+size, outline="", fill="green")
            elif part[6] == 3:
                canvas.create_oval(px-size, py-size, px+size, py+size, outline="", fill="yellow")
            elif part[6] == 4:
                canvas.create_oval(px-size, py-size, px+size, py+size, outline="", fill="purple")
            elif part[6] == 5:
                canvas.create_oval(px-size, py-size, px+size, py+size, outline="", fill="white")
            else:
                canvas.create_oval(px-size, py-size, px+size, py+size, outline="", fill="cyan")
    root.update()
