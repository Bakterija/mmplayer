from __future__ import print_function
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.metrics import cm

def get_dict_item(dictio,item,default):
    for k, v in dictio.items():
        if k == item:
            return v
    return default

class Accurate_Seeker:
    def __init__(self,seekFunc): self.seekFunc = seekFunc
    def close(self,*arg): self.frame.dismiss()
    def seek(self,hh,mm,ss):
        hh,mm,ss = int(hh),int(mm),int(ss)
        value = ss+(mm*60)+(hh*60*60)
        self.seekFunc(int(value))

    def get_length_vars(self,values):
        current, max = values[0], values[1]
        if max < 60: return (0,0),(0,0),(current,max)
        if max < 3600:
            m, s = divmod(current, 60)
            m2, s2 = divmod(max, 60)
            return (0,0),(m,m2),(s,59)
        else:
            m, s = divmod(current, 60)
            m2, s2 = divmod(max, 60)
            h, m = divmod(m, 60)
            h2, m2 = divmod(m2, 60)
            return (h,h2),(m,60),(s,59)

    def update(self,*arg):
        hh = str(int(self.sl1.value)).zfill(2)
        mm = str(int(self.sl2.value)).zfill(2)
        ss = str(int(self.sl3.value)).zfill(2)
        self.tlab2.text = hh+':'+mm+':'+ss
        if self.hhLabel.text != '': self.hhLabel.text = 'H '+hh
        if self.mmLabel.text != '': self.mmLabel.text = 'M '+mm
        if self.ssLabel.text != '':  self.ssLabel.text = 'S '+ss

    def open(self,*arg,**kwarg):

        self.frame = Popup(title='Seek', content=StackLayout(),size_hint=(0.95,0.8))
        self.frame.open()

        self.hhLabel = Label(text='H', size_hint=(0.05,0.2))
##        sep5 = Widget(size_hint=(0.05, 0.1))
        self.sl1 = Slider(min=0, max=60, value=0,size_hint=(0.95, 0.2))

        self.mmLabel = Label(text='M', size_hint=(0.05,0.2))
        self.sl2 = Slider(min=0, max=60, value=0,size_hint=(0.95, 0.2))

        self.ssLabel = Label(text='S', size_hint=(0.05,0.2))
        self.sl3 = Slider(min=0, max=60, value=0,size_hint=(0.95, 0.2))
        sep4 = Widget(size_hint=(1,0.1))

        tlab1 = Label(text='Value:', size_hint=(0.1,0.1))
        sep5 = Widget(size_hint=(0.75,0.1))
        self.tlab2 = Label(text='HH:MM:SS', size_hint=(0.1,0.1))

        btn1 = Button(text='Seek', size_hint=(0.5, 0.2))
        btn2 = Button(text='Close', size_hint=(0.5, 0.2))
        btn1.bind(on_press=lambda x: self.seek(self.sl1.value,self.sl2.value,self.sl3.value))
        btn2.bind(on_press=self.close)
##
        for x in self.hhLabel,self.sl1,self.mmLabel,self.sl2,self.ssLabel,self.sl3,sep4,tlab1,sep5,self.tlab2,btn1,btn2:
            self.frame.content.add_widget(x)
        for x in self.sl1,self.sl2,self.sl3:
            x.bind(on_touch_move= self.update)
            x.bind(on_touch_up= self.update)

        (self.sl1.value,self.sl1.max),(self.sl2.value,self.sl2.max),(self.sl3.value,self.sl3.max) = self.get_length_vars(
            get_dict_item(kwarg,'length',0))
        if self.sl1.max == 0:
##            self.frame.content.remove_widget(sep1)
            self.hhLabel.size_hint, self.hhLabel.text = (1,0.2),''
            self.frame.content.remove_widget(self.sl1)
        if self.sl2.max == 0:
            self.mmLabel.size_hint, self.mmLabel.text = (1,0.2),''
            self.frame.content.remove_widget(self.sl2)
