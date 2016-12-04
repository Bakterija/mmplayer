from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import cm
from kivy.utils import platform
import os

def return_path():
    if platform == 'android':
        d = os.path.dirname('/sdcard/github_bakterija/jotube/')
        if not os.path.exists(d): return ''
        return '/sdcard/github_bakterija/jotube/'
    else: return ''

def readf(filename):
    file = filename
    try:
        f = open(file, 'rU')
    except:
        savef('',filename)
        f = open(file, 'rU')
    a = f.read()
    a = str.splitlines(a)
    f.close()
    return a

def savef(text,file):
    f = open(file, 'w')
    f.write(text)
    f.close()

def edit_settings(text,text_find,new_value):
    count = 0
    newlist = []
    for lines in text:
        b = lines.find(text_find)
        if b is not -1:
            c = text_find + '=' + str(new_value)
            newlist.append(c)
        else:
            newlist.append(lines)
        count+=1
    count = 1
    return newlist

def get_settings(text,text_find,default_value):
    for lines in text:
        b = lines.find(text_find)
        if b is not -1:
            c = lines[len(text_find):]
    ## Checks if it exists and appends something, if not
    try:
        if c == '':
            c = default_value
            if default_value != '':
                write_settings(text_find[:-1],'\n'+c)
    except:
        path = return_path()
        c = default_value
        fh = open(path+'settings.ini', 'a')
        fh.write('\n'+str(text_find)+str(c))
        fh.close()
    return c

def read_settings(*arg):
    path = return_path()
    a = readf(path+'settings.ini')
    a = get_settings(a,arg[0],arg[1])
    return a

def write_settings(text_find,new_value):
    path = return_path()
    a = readf(path+'settings.ini')
    a = edit_settings(a,text_find,new_value)
    text = a = '\n'.join(str(e) for e in a)
    savef(text,path+'settings.ini')

class Setting_handler:
    def __init__(self,parent,settings,var,label,cbuttons):
        parentparent = parent
        parent = BoxLayout(orientation='horizontal', size_hint_y=None)
        parentparent.add_widget(parent)
        self.sett = (settings,var)
        self.height = cm(1)
        self.clickFunc = []
        labelWidth = 0.3
        buttonWIdth = (1 - labelWidth)/len(cbuttons)
        self.selectedColor = (0.65,0.65,0.9,1)

        self.buttons, self.settings = [], settings
        setting_label = Label(text= label, size_hint=(labelWidth, 1))
        parent.add_widget(setting_label)
        for x in cbuttons:
            btn = Button(text=x, size_hint=(buttonWIdth, 1))
            self.buttons.append(btn)
            btn.bind(on_press= lambda btn=btn: self.set_value(btn))
            parent.add_widget(btn)
            if self.sett[0][self.sett[1]] == x: btn.isSelected = True
            else: btn.isSelected = False
        Clock.schedule_once(self.set_button_colors, 0)
        Clock.schedule_once(self.set_height, 0)
        self.parent = parent

    def set_height(self,*arg): self.parent.height = self.height
    def set_button_colors(self,*arg):
        def selected(button): button.background_color= self.selectedColor
        for x in self.buttons:
            if x.isSelected: selected(x)
            else: x.background_color=(0.96,0.96,0.96,1)

    def set_value(self,btn):
        self.sett[0][self.sett[1]] = btn.text
        write_settings(self.sett[1], btn.text)
        for x in self.buttons: x.isSelected = False
        btn.isSelected = True
        Clock.schedule_once(self.set_button_colors, 0.1)
        if self.clickFunc != []:
            for x in self.clickFunc:
                x(btn.text)

    def get_value(self):
        for x in self.buttons:
            if x.isSelected: return x.text

    def bind_click(self,func,run=False):
        self.clickFunc.append(func)
        if run:
            for x in self.buttons:
                if x.isSelected:
                    func(x.text)
