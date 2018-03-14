import tkinter as tk
import tkinter.messagebox

window = tk.Tk()
window.title('my window')
window.geometry('200x200')

def hit_me():
    #tk.messagebox.showinfo(title='Hi', message='hahahaha')   #提示信息对话窗
    #tk.messagebox.showwarning(title='Hi', message='nononono')   #提出警告对话窗
    #tk.messagebox.showerror(title='Hi', message='No!! never')   #提出错误对话窗
    #print(tk.messagebox.askquestion(title='Hi', message='hahahaha'))   #返回yes和no
    #print(tk.messagebox.askyesno(title='Hi', message='hahahaha'))   #返回true和false
    #print(tk.messagebox.asktrycancel(title='Hi', message='hahahaha'))   #返回true和false
    #print(tk.messagebox.askokcancel(title='Hi', message='hahahaha'))   #返回true和false
    print(tk.messagebox.askyesnocancel(title="Hi", message="haha"))     # return, True, False, None
    #print(tk.messagebox.askyesno(title='Hi', message='hahahaha'))      #返回true和false
    #print(tk.messagebox.askretrycancel(title='Hi', message='hahahaha')) #返回true和false

tk.Button(window, text='hit me', command=hit_me).pack()
window.mainloop()
