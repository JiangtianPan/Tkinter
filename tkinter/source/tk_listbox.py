import tkinter as tk

window = tk.Tk()
window.title('my window')
window.geometry('200x200')

var1 = tk.StringVar()
l = tk.Label(window, bg='yellow', width=4, textvariable=var1)
l.pack()

def print_selection(): #按钮的点击事件
    value = listbox.get(listbox.curselection())
    var1.set(value)

button1 = tk.Button(window, text='print selection', width=15,
              height=2, command=print_selection)
button1.pack()

var2 = tk.StringVar()
var2.set((11,22,33,44))
listbox = tk.Listbox(window, listvariable=var2)
list_items = [1,2,3,4]
for item in list_items:
    listbox.insert('end', item)
listbox.insert(1, 'first')
listbox.insert(2, 'second')
#listbox.delete(2)
listbox.pack()

window.mainloop()
