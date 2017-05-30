#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kivy.utils import platform
from kivy.clock import Clock
from threading import Thread
from kivy.lib import osc
from time import sleep
if platform == 'android':
    from android import AndroidService
    

class serviceCom:

    def __init__(self, parent):
        self.parent = parent
        self.port = 44772
        osc.init()
        self.oscid = osc.listen(ipAddr='127.0.0.1', port=self.port)
        osc.bind(self.oscid, self.osc_callback, '/jotube_api')

        self.serviceSTARTED = False
        self.connected = False
        service = None
        self.bindings = {'on_connect': None,'on_disconnect': None}
        if platform != 'android':
            self.serviceSTARTED = True
            self.SERVICEconnect()

    def toggle_service(self,*arg):
        if platform == 'android':
            if self.serviceSTARTED == False:
                service = AndroidService('Jotube service', 'running')
                service.start('service started')
                self.serviceSTARTED = True
                self.service = service
                self.SERVICEconnect()
            else:
                self.parent.data_list.append('stop')
                self.serviceSTARTED = False
                self.connected = False
                self.service.stop()

    def SERVICEconnect(self,*arg):
        if self.connected == False:
            self.send_message('OPEN::')
            self.connected = True
            Thread(target=self.recv_thread).start()
            if self.bindings['on_connect'] != None:
                self.bindings['on_connect']()

    def SERVICEdisconnect(self,*arg):
        if self.connected == True:
            self.send_message('CLOSE::')
            self.connected = False
            if self.bindings['on_disconnect'] != None:
                self.bindings['on_disconnect']()

    def stop(self,*arg):
        self.send_message('STOP::')
        self.send_message('CLOSE::')
        self.connected = False
        self.serviceSTARTED = False

    def recv_thread(self):
        while self.connected:
            osc.readQueue(self.oscid)
            sleep(0.01)

    def osc_callback(self,message,*args):
        data = message[2]
        self.parent.data_list.append(data)

    def send_message(self,text,api='/jotube_api'):
        osc.sendMsg(api, [text], port=44771)

    def bind(self,*args,**kwargs):
        self.bindings.update(kwargs)
        if self.connected:
            if self.bindings['on_connect'] != None:
                self.bindings['on_connect']()
