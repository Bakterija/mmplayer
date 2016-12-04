#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.label import Label
from multi_line_label import MultiLineLabel
from kivy.uix.image import Image
from kivy.metrics import cm

class Youtube_View(StackLayout):
    def __init__(self,*args,**kwargs):
        super(Youtube_View, self).__init__(**kwargs)
        self.bind(minimum_height= self.setter('height'))
        self.size_hint_y = None
        self.video_values = {}
        MoreStacks = StackLayout(size_hint_y=None)
        MoreStacks.bind(minimum_height= MoreStacks.setter('height'))

        self.wd_thumbnail = Image(size_hint=(1, None), height=cm(0), allow_stretch=True)
        self.wd_title = MultiLineLabel(text='', font_size='26sp')

        self.wd_uploader = MultiLineLabel(text='')
        self.wd_duration = Label(text='', size_hint=(0.24, None), height=cm(1))
        self.wd_view_count = Label(text='', size_hint=(0.24, None), height=cm(1))
        self.wd_like_count = Label(text='', size_hint=(0.24, None), height=cm(1))
        self.wd_dislike_count = Label(text='', size_hint=(0.24, None), height=cm(1))
        self.wd_description = MultiLineLabel(text='')

        self.add_widget(self.wd_thumbnail)
        self.add_widget(MoreStacks)
        for x in (self.wd_title, self.wd_uploader, self.wd_duration,
                    self.wd_view_count, self.wd_like_count, self.wd_dislike_count, self.wd_description):
            MoreStacks.add_widget(x)

    def resize_wd_widgets(self,*args):
        self.wd_thumbnail.width = self.wd_title.width
        self.wd_thumbnail.height = self.wd_title.width*0.7
        self.wd_thumbnail.texture_size = self.wd_thumbnail.size

    def reload_image(self,*args):
        self.wd_thumbnail.reload()

    def set_title(self,string):
        self.wd_title.text = string

    def set_thumbnail(self,string):
        self.wd_thumbnail.height = cm(3)
        self.wd_thumbnail.source = string

    def set_uploader(self,string):
        self.wd_uploader.text = string

    def set_view_count(self,string):
        self.wd_view_count.text = str(string)

    def set_like_count(self,string):
        self.wd_like_count.text = str(string)

    def set_duration(self,string):
        self.wd_duration.text = str(string)

    def set_dislike_count(self,string):
        self.wd_dislike_count.text = str(string)

    def set_description(self,string):
        self.wd_description.text = string
