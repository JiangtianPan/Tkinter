import tkinter as tk

window = tk.Tk()
window.title('my window')
window.geometry('200x200')

def insert_point():
    var = entry.get()
    text.insert('insert',var)
    #text.insert(2.2,var) 打印第二行第二列，从0开始

def insert_end():
    var = entry.get()
    text.insert('end',var)
    
button1 = tk.Button(window,text="insert point",width=15,height=2,command=insert_point)
button1.pack()

button2 = tk.Button(window,text="insert end",command=insert_end)
button2.pack()

entry = tk.Entry(window,show='*')
entry.pack()

text = tk.Text(window,height=2)
text.pack()

##显示出来
windo.mainloop()
