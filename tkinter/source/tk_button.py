import tkinter as tk

window = tk.Tk()
window.title('Build Your Roadmap')
#window.geometry('200*100')

on_hit = False  # 默认初始状态为 False
def hit_me():
    global on_hit
    if on_hit == False:     
        on_hit = True
        var.set('you hit me')   
    else:       
        on_hit = False
        var.set('')
        
var = tk.StringVar()    #文字变量储存器
label = tk.Label(window,
    textvariable=var,   #使用textvariable替换text,因为这个可以变化
    #text='Build Your Roadmap',
    bg='grey',
    font=('Arial', 12),     
    width=15, height=2
    #command=hit_me     #点击按钮式执行的命令
    )
label.pack()    #固定窗口位置

button = tk.Button(window,
    text='hit_me',
    width=15,heigh=2,
    command=hit_me)
button.pack()


        
window.mainloop()
