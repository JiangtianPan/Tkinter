import tkinter as tk

window = tk.Tk()
window.title('Build a RoadMap')
window.geometry('1000x1000')

canvas_width = 500
canvas_height = 500
canvas = tk.Canvas(window, bg='grey', height=canvas_height, width=canvas_width)
image_file = tk.PhotoImage(file='ins.gif')
#10,10为图片放入的坐标
#anchor=nw把图片的左上角作为锚定点
#image = canvas.create_image(10, 10, anchor='nw', image=image_file)
x0, y0, x1, y1= 50, 50, 80, 80


def checkered(canvas, line_distance):
   # vertical lines at an interval of "line_distance" pixel
   for x in range(line_distance,canvas_width,line_distance):
      canvas.create_line(x, 0, x, canvas_height, fill="#476042")
   # horizontal lines at an interval of "line_distance" pixel
   for y in range(line_distance,canvas_height,line_distance):
      canvas.create_line(0, y, canvas_width, y, fill="#476042")

canvas.pack()

checkered(canvas,10)

def add_X():
    points = [100,100,120,100,120,80,140,80,140,100,160,100,
              160,120,140,120,140,140,120,140,120,120,100,120]
    #for i in ()
    X_cross = canvas.create_polygon(points, outline='green',
                                    fill='yellow',width=1)
    global obj
    obj = X_cross  
    return obj

def add_Y():
    sqrt3 = (3)**0.5
    points = [100,100,120,100,130,100-10*sqrt3,
              130+10*sqrt3,110-10*sqrt3,120+10*sqrt3,110,130+10*sqrt3,110+10*sqrt3,
              130,120+10*sqrt3,120,120,100,120]
    Y_cross = canvas.create_polygon(points, outline='green',
                                    fill='yellow',width=1)
    global obj
    obj = Y_cross  
    return obj

def add_T():
    points = [100,100,160,100,160,120,140,120,
              140,160,120,160,120,120,100,120]
    T_cross = canvas.create_polygon(points, outline='green',
                                    fill='yellow',width=1)
    global obj
    obj = T_cross
    return obj 


def moveit_left():
    canvas.move(obj, -10, 0) #触发一次横纵坐标移动0和2
def moveit_right():
    canvas.move(obj, 10, 0)
def moveit_up():
    canvas.move(obj, 0, -10)
def moveit_down():
    canvas.move(obj, 0, 10)

button_up = tk.Button(window, text='up', command=moveit_up).pack()
#button_up.place(x=570, y=530)
button_down = tk.Button(window, text='down', command=moveit_down).pack()
#button_down.place(x=570, y=730)
button_left = tk.Button(window, text='left', command=moveit_left).pack()
#button_left.place(x=510, y=630)
button_right = tk.Button(window, text='right', command=moveit_right).pack()
#button_right.place(x=610, y=630)

button_X = tk.Button(window, text='X cross', command=add_X).pack()
#button_X.place(x=510, y=830)
button_Y = tk.Button(window, text='Y cross', command=add_Y).pack()
#button_Y.place(x=570, y=830)
button_T = tk.Button(window, text='T cross', command=add_T).pack()
#button_T.place(x=630, y=830)


window.mainloop()
