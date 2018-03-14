import tkinter as tk

window = tk.Tk()
window.geometry('200x200')

canvas = tk.Canvas(window, height=150, width=500)
canvas.grid(row=1, column=1)
image_file = tk.PhotoImage(file='ins.gif')
image = canvas.create_image(0, 0, anchor='nw', image=image_file)

#Pack
#tk.Label(window, text='1').pack(side='top')
#tk.Label(window, text='1').pack(side='bottom')
#tk.Label(window, text='1').pack(side='left')
#tk.Label(window, text='1').pack(side='right')

#Grid
#padx为左右间距，pady为上下间距
#for i in range(4):
#    for j in range(4):
#        tk.Label(window, text='+').grid(row=i, column=j, padx=10, pady=5) 
        
#Place:用精确的坐标来定位
#anchor='nw':锚定点是西北角
tk.Label(window, text=1).place(x=200, y=100, anchor='se')

window.mainloop()
