import tkinter as tk

window = tk.Tk()
window.title('my window')
window.geometry('400x400')

l = tk.Label(window, bg='yellow', width=20, text='empty')
l.pack()

def print_selection(v):
    l.config(text='you have selected ' + v)

s = tk.Scale(window, label='try me', from_=0, to=10, orient=tk.HORIZONTAL,
             length=400, showvalue=1, #是否在滚动条上方显示数值
             tickinterval=1, #坐标间隔
             resolution=0.01, #保留两位小数
             command=print_selection)
s.pack()

window.mainloop()
