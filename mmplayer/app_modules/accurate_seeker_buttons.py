from __future__ import print_function
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout
from kivy.metrics import cm


class Seeker_Button(Button):
    def __init__(self): pass


class Accurate_Seeker:
    def __init__(self,seekFunc): self.seekFunc = seekFunc
    def close(self,*arg): self.frame.dismiss()
    def seek(self,value):
        try:
            value = value.zfill(6)
            hh,mm,ss = int(value[:2]),int(value[2:4]),int(value[4:])
            value = ss+(mm*60)+(hh*60*60)
            self.seekFunc(int(value))
        except: pass

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

    def add(self,label,text):
        if len(self.value) < 6:
            self.value
            if text == ':00' or text == ':30':
                if len(self.value) == 0:
                    if text == ':00': self.value += '00'
                    else: self.value += '30'
                elif len(self.value) == 1 or len(self.value) == 3:
                    self.value += ' '
                    if text == ':00': self.value += '00'
                    else: self.value += '30'
                elif len(self.value) == '5':
                    if text == ':00': self.value += '0'
                    else: self.value += '3'
                else:
                    if text == ':00': self.value += '00'
                    else: self.value += '30'
            else:
                self.value += text
            label.text = self.value
            self.update_label(label)

    def update_label(self,label):
        if len(self.value) > 4:
            label.text = label.text[:-4]+'h'+' '+label.text[-4:-2]+'m'+' '+label.text[-2:]+'s'
        elif len(self.value) > 2:
            label.text = label.text[:-2]+'m'+' '+label.text[-2:]+'s'
        elif len(self.value) < 3 and self.value != '':
            label.text += 's'
        else:
            label.text = '0s'

    def delete(self,label):
        self.value = self.value[:-1]
        label.text = self.value
        self.update_label(label)

    def open(self,*arg,**kwarg):
        self.frame = Popup(title='Seek', content=StackLayout(),size_hint=(0.9,0.9))
        self.frame.open()
        self.value = ''

        inLabel = Label(text='0s', size_hint=(1,0.25), font_size='40sp', font='Arial')
        self.frame.content.add_widget(inLabel)
        inLabel.bind(on_press=self.frame.dismiss)

        for x in '1','2','3','4','5','6','7','8','9', ':00','0',':30':
            btn = Button(text=x, size_hint=(0.33,0.15))
            btn.bind(on_release= lambda btn=btn: self.add(inLabel,btn.text))
            self.frame.content.add_widget(btn)
        cbtn = Button(text='Close', size_hint=(0.33,0.15))
        dbtn = Button(text='Delete', size_hint=(0.33,0.15))
        sbtn = Button(text='Seek', size_hint=(0.33,0.15))
        cbtn.bind(on_release= self.close)
        dbtn.bind(on_release= lambda x: self.delete(inLabel))
        sbtn.bind(on_release= lambda x: self.seek(self.value))
        for x in cbtn, dbtn, sbtn:
            self.frame.content.add_widget(x)
