from tkinter import *
from math import *

points = []
line_startend = []
line = []
add_info = []

OPTIONS = { 'DDA Line Drawing':1,
    'Bresenham Line Drawing':2,
    'Midpoint Line Drawing':3,
    'Midpoint Circle Drawing':4,
    'Translate':5,
    'Rotate':6,
    'Scale':7 }
OPTIONS_key = list(OPTIONS.keys())
OPTIONS_values = list(OPTIONS.values())

class popupWindow(object):
    def __init__(self,master):

        top=self.top=Toplevel(master)

        self.label_one = Label(top, text="Enter pattern, tx, sx, or theta: ")
        self.first_value = StringVar()
        self.label_one.pack()
        self.entry_one = Entry(top, textvariable = self.first_value)
        self.entry_one.pack()
        self.label_two = Label(top, text="Enter width, ty or sy: ")
        self.second_value = StringVar()
        self.label_two.pack()
        self.entry_two = Entry(top, textvariable = self.second_value)
        self.entry_two.pack()
        self.b1 = Button(top ,text='Enter',command=self.cleanup)
        self.b1.pack()

    def cleanup(self):
        onevalue = self.first_value.get()
        twovalue = self.second_value.get()
        add_info.append((onevalue, twovalue))
        self.top.destroy()


class CG:

    x1, y1, x2, y2 = 0, 0, 0, 0

    def __init__(self):

        # ---------- SETTING VARIABLES ----------

        win_width = 800
        win_height = 650
        canvas_width = 700
        canvas_height = 500

        self.object_list = []

        # ---------- SETTING WINDOW ----------

        window = Tk()
        window.title("Computer Graphics App")
        window.resizable(width=False, height=False)
        window.geometry('{}x{}'.format(win_width, win_height))

        self.option = StringVar(window)
        self.option.set(OPTIONS_key[0])

        menu = OptionMenu(window, self.option, *OPTIONS_key)
        menu.pack()

        # ---------- SETTING CANVAS AND IMAGE ----------

        self.canvas = Canvas(window, width=canvas_width, height=canvas_height, bg="#ffffff")
        self.canvas.pack()

        self.canvas.create_line(350, 0, 350, 500)
        self.canvas.create_line(0, 250, 700, 250)

        self.canvas.bind("<Button-1>", self.callback)

        self.master = frame = Frame(window)
        frame.pack()

        # ---------- TEXT INPUTS ---------
        label_two = Label(frame, text="Enter values(0-F) for pattern: ").grid(row = 3, column = 1, padx=0, pady=5)
        self.pattern_value = StringVar()
        Entry(frame, textvariable = self.pattern_value).grid(row = 3, column = 2)

        label_three = Label(frame, text="Enter values for thickness: ").grid(row = 4, column = 1, padx=0, pady=5)
        self.thickness_value = StringVar()
        Entry(frame, textvariable = self.thickness_value).grid(row = 4, column = 2)

        # ---------- ACTIONS FOR BUTTONS ----------

        dda_button = Button(frame, text="Draw", command = self.draw_item)
        dda_button.grid(row = 5, column = 1)

        dda_button = Button(frame, text="Transform", command = self.transformation)
        dda_button.grid(row = 5, column = 2)

        self.tr_button = tr_button = Button(frame, text="Parameters", command = self.popup)
        tr_button.grid(row = 5, column = 3)

        clear_button = Button(frame, text="Clear", command = self.clear_canvas)
        clear_button.grid(row = 5, column = 4)

        # ---------- EVENT LOOP ----------

        window.mainloop()

    def popup(self):
        self.w = popupWindow(self.master)
        self.tr_button["state"] = "disabled"
        self.master.wait_window(self.w.top)
        self.tr_button["state"] = "normal"

    def draw_dda(self):
        pattern_list = {'0':'0000', '1':'0001', '2':'0010', '3':'0011', '4':'0100', '5':'0101',
        '6':'0110', '7':'0111', '8':'1000', '9':'1001', 'A':'1010', 'B':'1011', 'C':'1100',
        'D':'1101', 'E':'1110', 'F':'1111'}

        pattern = self.pattern_value.get()
        thickness = int(self.thickness_value.get())

        line_startend = points
        x1, y1 = line_startend[len(line_startend) - 2]
        x2, y2 = line_startend[len(line_startend) - 1]
        coordinates = (x1 - 350, y1 - 250, x2 - 350, y2 - 250)

        self.object_list = [x1 - 350, y1 - 250, x2 - 350, y2 - 250, pattern, thickness, "dda"]

        dx = x2 - x1
        dy = y2 - y1

        steps, x, y = 0, x1, y1

        if abs(dx) > abs(dy):
            steps = abs(dx)
        else:
            steps = abs(dy)

        x_increment = dx/steps
        y_increment = dy/steps

        for i in range(steps):
            p = pattern_list[pattern]

            line.append((x - 350, y - 250))

            if p[i%4] == '1':

                self.canvas.create_rectangle(round(x), round(y), round(x)+1, round(y)+1)

                for j in range(1, thickness):
                    self.canvas.create_rectangle(round(x), round(y)-j, round(x), round(y)-j+1)

            x += x_increment
            y += y_increment


        print (self.object_list)

    def draw_symm_dda(self):

        pattern_list = {'0':'0000', '1':'0001', '2':'0010', '3':'0011', '4':'0100', '5':'0101',
        '6':'0110', '7':'0111', '8':'1000', '9':'1001', 'A':'1010', 'B':'1011', 'C':'1100',
        'D':'1101', 'E':'1110', 'F':'1111'}

        pattern = self.pattern_value.get()
        thickness = int(self.thickness_value.get())

        line_startend = points
        x1, y1 = line_startend[len(line_startend) - 2]
        x2, y2 = line_startend[len(line_startend) - 1]
        coordinates = (x1 - 350, y1 - 250, x2 - 350, y2 - 250)

        self.object_list = [x1 - 350, y1 - 250, x2 - 350, y2 - 250, pattern, thickness, "dda_symm"]

        dx = x2 - x1
        dy = y2 - y1

        max, x, y = 0, x1, y1

        if abs(dx) > abs(dy):
            max = abs(dx)
        else:
            max = abs(dy)

        steps = 2 ** (math.floor(math.log(max, 2)))

        x_increment = dx/steps
        y_increment = dy/steps

        '''for i in range(steps):
            x += x_increment
            y += y_increment
            self.canvas.create_rectangle(round(x), round(y), round(x)+1, round(y)+1)'''

        for i in range(steps):
            p = pattern_list[pattern]

            line.append((x - 350, y - 250))

            if p[i%4] == '1':

                self.canvas.create_rectangle(round(x), round(y), round(x)+1, round(y)+1)

                for j in range(1, thickness):
                    self.canvas.create_rectangle(round(x), round(y)-j, round(x), round(y)-j+1)

            print (x, y)

            x += x_increment
            y += y_increment

        print (self.object_list)


    def draw_bresenham(self):

        pattern_list = {'0':'0000', '1':'0001', '2':'0010', '3':'0011', '4':'0100', '5':'0101',
        '6':'0110', '7':'0111', '8':'1000', '9':'1001', 'A':'1010', 'B':'1011', 'C':'1100',
        'D':'1101', 'E':'1110', 'F':'1111'}

        pattern = self.pattern_value.get()
        thickness = int(self.thickness_value.get())

        line_startend = points
        x1, y1 = line_startend[len(line_startend) - 2]
        x2, y2 = line_startend[len(line_startend) - 1]
        coordinates = (x1 - 350, y1 - 250, x2 - 350, y2 - 250)

        self.object_list = [x1 - 350, y1 - 250, x2 - 350, y2 - 250, pattern, thickness, "bresenham"]

        x, y = x1, y1

        self.canvas.create_rectangle(x, y, x+1, y+1)

        dx = x2 - x1
        dy = y2 - y1
        x_inc, y_inc = 0, 0

        if dx < 0:
            dx *= -1
            x_inc = -1
        else:
            x_inc = 1

        if dy < 0:
            dy *= -1
            y_inc = -1
        else:
            y_inc = 1

        if (dx > dy):
            p = 2*dy - dx
            c1 = 2*(dy - dx)
            c2 = 2*dy

            for i in range(abs(dx)):
                line.append((x - 350, y - 250))

                x += x_inc
                if p < 0:
                    p += c2
                else:
                    p += c1
                    y += y_inc

                pt = pattern_list[pattern]

                line.append((x - 350, y - 250))

                if pt[i%4] == '1':
                    self.canvas.create_rectangle(x, y, x+1, y+1)

                    for j in range(1, thickness):
                        self.canvas.create_rectangle(x, y-j, x, y-j+1)

        else:
            p = 2*dx - dy
            c1 = 2*(dx - dy)
            c2 = 2*dx

            for i in range(abs(dy)):
                line.append((x - 350, y - 250))
                y += y_inc
                if p < 0:
                    p += c2
                else:
                    p += c1
                    x += x_inc

                pt = pattern_list[pattern]

                if pt[i%4] == '1':
                    self.canvas.create_rectangle(x, y, x+1, y+1)

                    for j in range(1, thickness):
                        self.canvas.create_rectangle(x, y-j, x, y-j+1)


        print (self.object_list)


    def draw_midpoint(self):
        pattern_list = {'0':'0000', '1':'0001', '2':'0010', '3':'0011', '4':'0100', '5':'0101',
        '6':'0110', '7':'0111', '8':'1000', '9':'1001', 'A':'1010', 'B':'1011', 'C':'1100',
        'D':'1101', 'E':'1110', 'F':'1111'}

        pattern = self.pattern_value.get()
        thickness = int(self.thickness_value.get())

        line_startend = points
        x1, y1 = line_startend[len(line_startend) - 2]
        x2, y2 = line_startend[len(line_startend) - 1]
        coordinates = (x1 - 350, y1 - 250, x2 - 350, y2 - 250)

        self.object_list = [x1 - 350, y1 - 250, x2 - 350, y2 - 250, pattern, thickness, "midpoint"]

        x, y = x1, y1

        self.canvas.create_rectangle(x, y, x+1, y+1)

        dx = x2 - x1
        dy = y2 - y1
        x_inc, y_inc = 0, 0

        if dx < 0:
            dx *= -1
            x_inc = -1
        else:
            x_inc = 1

        if dy < 0:
            dy *= -1
            y_inc = -1
        else:
            y_inc = 1

        if (dx > dy):
            p = 2*dy - dx
            c1 = dy - dx
            c2 = dy

            for i in range(dx):
                line.append((x - 350, y - 250))
                x += x_inc
                if (p < 0):
                    p += c2
                else:
                    p += c1
                    y += y_inc

                pt = pattern_list[pattern]

                line.append((x - 350, y - 250))

                if (pt[i%4] == '1'):
                    self.canvas.create_rectangle(x, y, x+1, y+1)
                    for j in range(1, thickness):
                        self.canvas.create_rectangle(x, y-j, x, y-j+1)

        else:
            p = 2*dx - dy
            c1 = dx - dy
            c2 = dx

            for i in range(dy):
                line.append((x - 350, y - 250))
                y += y_inc
                if (p < 0):
                    p += c2
                else:
                    p += c1
                    x += x_inc

                pt = pattern_list[pattern]

                line.append((x - 350, y - 250))

                if (pt[i%4] == '1'):
                    self.canvas.create_rectangle(x, y, x+1, y+1)

                    for j in range(1, thickness):
                        self.canvas.create_rectangle(x, y-j, x, y-j+1)

        print (self.object_list)

    def draw_circle(self):

        line_startend = points
        cx, cy = line_startend[len(line_startend) - 2]
        x, y = line_startend[len(line_startend) - 1]
        radius = sqrt(pow((x - cx), 2) + pow((y - cy), 2))

        self.object_list = [cx - 350, cy - 250, x - 350, y - 250, "circle"]

        x = 0
        y = int(radius)
        p = 1.25 - radius
        self.draw_symmetric(x, y, cx, cy)

        while x < y:
            if p < 0:
                p += 2 * x + 1
            else:
                p += 2 * (x - y) + 1
                y = y - 1
            x = x + 1
            self.draw_symmetric(x, y, cx, cy)

        print (self.object_list)

    def draw_symmetric(self, x, y, cx, cy):

        self.canvas.create_rectangle((cx + x), (cy + y), (cx + x)+1, (cy + y)+1)
        self.canvas.create_rectangle((cx + x), (cy - y), (cx + x)+1, (cy - y)+1)
        self.canvas.create_rectangle((cx - x), (cy + y), (cx - x)+1, (cy + y)+1)
        self.canvas.create_rectangle((cx - x), (cy - y), (cx - x)+1, (cy - y)+1)
        self.canvas.create_rectangle((cx + y), (cy + x), (cx + y)+1, (cy + x)+1)
        self.canvas.create_rectangle((cx + y), (cy - x), (cx + y)+1, (cy - x)+1)
        self.canvas.create_rectangle((cx - y), (cy + x), (cx - y)+1, (cy + x)+1)
        self.canvas.create_rectangle((cx - y), (cy - x), (cx - y)+1, (cy - x)+1)

    def translate(self):

        if self.object_list[4] != "circle":
            tx = int(add_info[-1][0])
            ty = int(add_info[-1][1])

            new_x1 = self.object_list[0] + tx + 350
            new_y1 = self.object_list[1] + ty + 250
            new_x2 = self.object_list[2] + tx + 350
            new_y2 = self.object_list[3] + ty + 250

            self.object_list[0] = new_x1 - 350
            self.object_list[1] = new_y1 - 250
            self.object_list[2] = new_x2 - 350
            self.object_list[3] = new_y2 - 250

            points.append((new_x1, new_y1))
            points.append((new_x2, new_y2))

            if self.object_list[6] == "dda":
                self.draw_dda()
            elif self.object_list[6] == "bresenham":
                self.draw_bresenham()
            elif self.object_list[6] == "midpoint":
                self.draw_midpoint()

        else:
            tx = int(add_info[-1][0])
            ty = int(add_info[-1][1])
            new_x1 = self.object_list[0] + tx + 350
            new_y1 = self.object_list[1] + ty + 250
            new_x2 = self.object_list[2] + 350
            new_y2 = self.object_list[3] + 250

            self.object_list[0] = new_x1 - 350
            self.object_list[1] = new_y1 - 250
            self.object_list[2] = new_x2 - 350
            self.object_list[3] = new_y2 - 250

            points.append((new_x1, new_y1))
            points.append((new_x2, new_y2))

            self.draw_circle()

    def scale(self):

        if self.object_list[4] != "circle":
            sx = int(add_info[-1][0])
            sy = int(add_info[-1][1])

            new_x1 = self.object_list[0] * sx + 350
            new_y1 = self.object_list[1] * sy + 250
            new_x2 = self.object_list[2] * sx + 350
            new_y2 = self.object_list[3] * sy + 250

            self.object_list[0] = new_x1 - 350
            self.object_list[1] = new_y1 - 250
            self.object_list[2] = new_x2 - 350
            self.object_list[3] = new_y2 - 250

            points.append((new_x1, new_y1))
            points.append((new_x2, new_y2))

            if self.object_list[6] == "dda":
                self.draw_dda()
            elif self.object_list[6] == "bresenham":
                self.draw_bresenham()
            elif self.object_list[6] == "midpoint":
                self.draw_midpoint()

        else:
            sx = int(add_info[-1][0])
            sy = int(add_info[-1][1])

            new_x1 = self.object_list[0] + 350
            new_y1 = self.object_list[1] + 250
            new_x2 = self.object_list[2] * sx + 350
            new_y2 = self.object_list[3] * sy + 250

            self.object_list[0] = new_x1 - 350
            self.object_list[1] = new_y1 - 250
            self.object_list[2] = new_x2 - 350
            self.object_list[3] = new_y2 - 250

            points.append((new_x1, new_y1))
            points.append((new_x2, new_y2))

            self.draw_circle()

    def rotate(self):
         rt = int(add_info[-1][0])
         rt = radians(rt)

         m = (self.object_list[3] - self.object_list[1])/(self.object_list[2] - self.object_list[0])
         phi = atan(m)

         '''new_x2 = int((self.object_list[2]) * cos(rt)) - int((self.object_list[3]) * sin(rt)) + 350
         new_y2 = int((self.object_list[2]) * sin(rt)) - int((self.object_list[3]) * cos(rt)) + 250
         new_x1 = int((self.object_list[0]) * cos(rt)) - int((self.object_list[1]) * sin(rt)) + 350
         new_y1 = int((self.object_list[0]) * sin(rt)) - int((self.object_list[1]) * cos(rt)) + 250'''

         new_x1 = int(self.object_list[0] * cos(rt + phi) + 350)
         new_y1 = int(self.object_list[1] * sin(rt + phi) + 250)
         new_x2 = int(self.object_list[2] * cos(rt + phi) + 350)
         new_y2 = int(self.object_list[3] * sin(rt + phi) + 250)

         self.object_list[0] = new_x1 - 350
         self.object_list[1] = new_y1 - 250
         self.object_list[2] = new_x2 - 350
         self.object_list[3] = new_y2 - 250

         points.append((new_x1, new_y1))
         points.append((new_x2, new_y2))

         if self.object_list[6] == "dda":
             self.draw_dda()
         elif self.object_list[6] == "circle":
             self.draw_circle()
         elif self.object_list[6] == "bresenham":
             self.draw_bresenham()
         elif self.object_list[6] == "midpoint":
             self.draw_midpoint()

    def rect(self):

        x1, y1 = line_startend[len(line_startend) - 2]
        x2, y2 = line_startend[len(line_startend) - 1]

        self.canvas.create_rectangle(x1, y1, x2, y2)

    def floodfill(self, x, y, oldColor, newColor):

        if oldColor == newColor:
            self.canvas.create_rectangle(x, y, x+1, y+1, fill="blue")


    def draw_item(self):
        selected = self.option.get()
        if OPTIONS[selected] == 1:
            self.draw_dda()
        elif OPTIONS[selected] == 2:
            self.draw_bresenham()
        elif OPTIONS[selected] == 3:
            self.draw_midpoint()
        elif OPTIONS[selected] == 4:
            self.draw_circle()

    def transformation(self):
        selected = self.option.get()
        if OPTIONS[selected] == 5:
            self.translate()
        elif OPTIONS[selected] == 6:
            self.rotate()
        elif OPTIONS[selected] == 7:
            self.scale()

    # ---------- CLEAR CANVAS ----------

    def clear_canvas(self):
        self.object_list = []
        self.canvas.delete(ALL)

        self.canvas.create_line(350, 0, 350, 500)
        self.canvas.create_line(0, 250, 700, 250)

        self.pattern_value.set("")
        self.thickness_value.set("")

    def callback(self, event):
        print ("clicked at", event.x - 350, event.y - 250)
        point = (event.x, event.y)
        points.append(point)
        self.canvas.create_rectangle(event.x, event.y, event.x + 1, event.y + 1)
#def onclick(self, event):
#item = self.canvas.find_closest(event.x, event.y)


cg_app = CG()
