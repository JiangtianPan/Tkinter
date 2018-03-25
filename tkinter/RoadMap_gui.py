from tkinter import *
from tkinter.colorchooser import askcolor
import pickle


class map_generator(object):

    DEFAULT_ENTRY_SIZE = 10
    sud_width_ratio = 5
    DEFAULT_COLOR = 'black'
    intersection = ['T intersection with stop sign','T intersection with traffic lights',
                    'Four way intersection with traffic lights','Four way stop sign',
                    'Four way intersection with two ways stop sign']
    def __init__(self):
        self.root = Tk()

        self.draw_button = Button(self.root, text='road', command=self.use_draw)
        self.draw_button.grid(row=0, column=0)

        self.intersection_button = Button(self.root, text='interaction', command=self.use_interaction)
        self.intersection_button.grid(row=0, column=1)
        
        self.type_intersection = StringVar() # intersection variable 
        self.type_intersection.set("intersection type") 
        OptionMenu(self.root, self.type_intersection, *map_generator.intersection).grid(row=0, column=2)
        
        self.height_intersection = StringVar()
        self.height_intersection.set('0')        # height of intersection
        Entry(self.root,textvariable=self.height_intersection, relief=SUNKEN, 
              width=map_generator.DEFAULT_ENTRY_SIZE).grid(row=0, column=3)

        self.sub_node_button = Button(self.root, text='subnode', command=self.use_subnode)
        self.sub_node_button.grid(row=0, column=4)

        self.rotation_button = Button(self.root, text='undo', command=self.undo)
        self.rotation_button.grid(row=0, column=5)

        self.clear_button = Button(self.root, text='clear', command=self.use_erase)
        self.clear_button.grid(row=0, column=6)

        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=7)
        
        self.generate_button = Button(self.root, text='generate', command=self.use_generate)
        self.generate_button.grid(row=0, column=8)

        self.c = Canvas(self.root, bg='white', width=600, height=600)
        self.c.grid(row=1, column=0, columnspan = 5)
        
        self.c2 = Canvas(self.root, bg='white', width=600, height=600)
        self.c2.grid(row=1, column=6, columnspan = 5)

        self.dummy = 1
        self.delete_queue = []
        
        self.stack_draw = []
        self.stack_op = []
        
        self.road_pos = []
        self.intersection_pos = []
        self.subnode_pos = []

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.intersection = False
        self.active_button = self.draw_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def use_draw(self):
        self.activate_button(self.draw_button)

    def use_interaction(self, width = 5):
        self.activate_button(self.intersection_button, intersection=True)
        
    def use_subnode(self, width = 5):
        self.activate_button(self.sub_node_button, subnode=True)

    def undo(self):
        tmp = self.stack_op.pop()
        if tmp[0]:
            self.c.after(1, self.c.delete, self.stack_draw.pop())
            if tmp[1]==1:
                self.intersection_pos.pop()
            else:
                self.subnode_pos.pop()
        
        else:
            self.c.after(1, self.c.delete, self.stack_draw.pop())
            self.c.after(1, self.c.delete, self.stack_draw.pop())
            self.road_pos.pop()
            
        print('remove element')
        print(self.road_pos)
        print(self.intersection_pos)
        print(self.subnode_pos)

    def use_generate(self):
        '''
            process self.road_pos, self.intersection_pos, self.subnode_pos
        '''
        dict_info = {'road': self.road_pos, 'intersection':self.intersection_pos, 'subnode':self.subnode_pos}
        print(dict_info)
        
        filehandler = open('data_structure.pkl', 'wb') 
        pickle.dump(dict_info, filehandler) 
        filehandler.close()
        
        image1 = PhotoImage(file = "app_gui.gif")
        self.c2.create_image(0,0,anchor='nw',image=image1)
        self.c2.image = image1

    def use_erase(self):
        self.c.delete("all")
        self.c2.delete("all")


    def activate_button(self, some_button, intersection=False, subnode = False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.intersection = intersection
        self.sub_n = subnode

    def draw_element(self,event, temp = True, width = 20):
        width = self.choose_size_button.get()*5
        self.line_width = 3
        paint_color = self.color
        if self.intersection==False and self.sub_n==False:
            if self.old_x and self.old_y and self.dummy==0:
                tmp_x, tmp_y = self.neighbor(event.x, event.y)
                canvas_id1 = self.c.create_line(self.old_x, self.old_y, 
                                            tmp_x, tmp_y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
            
                canvas_id2 = self.c.create_line(self.old_x+width, self.old_y+width, 
                                            tmp_x+width, tmp_y+width,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
            
                self.delete_queue.append(canvas_id1)
                self.delete_queue.append(canvas_id2)
            
            while len(self.delete_queue)>2:
                self.c.after(1, self.c.delete, self.delete_queue.pop(0))
                self.c.after(1, self.c.delete, self.delete_queue.pop(0))
                
        elif self.sub_n:
            tmp_x, tmp_y = event.x, event.y
            id_rect = self.c.create_rectangle(tmp_x, tmp_y, 
                                            tmp_x+width/self.sud_width_ratio, 
                                            tmp_y+width/self.sud_width_ratio, width=self.line_width)

            self.delete_queue.append(id_rect)
            while len(self.delete_queue)>1:
                self.c.after(1, self.c.delete, self.delete_queue.pop(0))
                
        else:
            tmp_x, tmp_y = self.neighbor(event.x, event.y)
            id_rect = self.c.create_rectangle(tmp_x, tmp_y, 
                                            tmp_x+width, tmp_y+width, width=self.line_width)

            self.delete_queue.append(id_rect)
            while len(self.delete_queue)>1:
                self.c.after(1, self.c.delete, self.delete_queue.pop(0))


    def paint(self, event):        
        if self.dummy == 1:
            self.old_x = event.x
            self.old_y = event.y
            self.dummy = 0
            self.old_x, self.old_y = self.neighbor(self.old_x, self.old_y)
            
        self.draw_element(event)
        
    def neighbor(self, x, y):
        # self.road_pos, self.intersection_pos, self.subnode
        tx = x
        ty = y
        if len(self.road_pos) == 0 and len(self.intersection_pos) == 0:
            tx = x
            ty = y
        else:
            candidate_x_y = [0,0]
            distance = 100000
            for i in range(len(self.road_pos)):
                r1x = self.road_pos[i][0]
                r1y = self.road_pos[i][1]
                r2x = self.road_pos[i][2]
                r2y = self.road_pos[i][3]
                d1 = ((r1x-x)*(r1x-x)+(r1y-y)*(r1y-y))
                d2 = ((r2x-x)*(r2x-x)+(r2y-y)*(r2y-y))
                if d1 < distance:
                    distance = d1
                    candidate_x_y = [r1x,r1y]
 
                if d2 < distance:
                    distance = d2
                    candidate_x_y = [r2x,r2y]
                
            for i in range(len(self.intersection_pos)):
                ix = self.intersection_pos[i][0]
                iy = self.intersection_pos[i][1]
                d1 = ((ix-x)*(ix-x)+(iy-y)*(iy-y))
                if d1 < distance:
                    distance = d1
                    candidate_x_y = [ix,iy]
                
            if distance<900:
                tx = candidate_x_y[0]
                ty = candidate_x_y[1]
            
        return tx,ty
        

    def reset(self, event): 
        self.draw_element(event, temp = False)
        self.stack_draw = self.stack_draw + self.delete_queue
        self.delete_queue = []
        if self.intersection==False and self.sub_n ==False:
            tmp_x, tmp_y = self.neighbor(event.x, event.y)
            self.road_pos.append((self.old_x, self.old_y, tmp_x, tmp_y))
        elif self.sub_n:
            self.subnode_pos.append((event.x, event.y))
        else:
            tmp_x, tmp_y = self.neighbor(event.x, event.y)
            self.intersection_pos.append((tmp_x, tmp_y, 
                                          self.type_intersection.get(),
                                          int(self.height_intersection.get())))
        
        dummy = 0
        if self.intersection:
            dummy = 1 
        self.stack_op = self.stack_op + [(self.intersection or self.sub_n, dummy)]
        print('add element')
        print('road element',self.road_pos)
        print('inttersection element',self.intersection_pos)
        print('subnode element',self.subnode_pos)
        self.old_x, self.old_y = None, None
        self.dummy = 1

if __name__ == '__main__':
    ge = map_generator()
