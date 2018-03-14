import tkinter as tk

window = tk.Tk()
window.title('my window')
window.geometry('200x200')

canvas = tk.Canvas(window, bg='blue', height=100, width=200)
image_file = tk.PhotoImage(file='ins.gif')
#10,10为图片放入的坐标
#anchor=nw把图片的左上角作为锚定点
image = canvas.create_image(10, 10, anchor='nw', image=image_file)
x0, y0, x1, y1= 50, 50, 80, 80
#从(50,50)到(80,80)画一条直线
line = canvas.create_line(x0, y0, x1, y1)
#创建一个圆,填充色为红色
oval = canvas.create_oval(x0, y0, x1, y1, fill='red')
#从0度到180度画扇形
arc = canvas.create_arc(x0+30, y0+30, x1+30, y1+30, start=0, extent=180)
#创建一个矩形
rect = canvas.create_rectangle(100, 30, 100+20, 30+20)
canvas.pack()

def moveit():
    canvas.move(rect, 0, 2) #触发一次横纵坐标移动0和2

b = tk.Button(window, text='move', command=moveit).pack()


window.mainloop()
