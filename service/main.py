#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from time import sleep, strftime
from random import randrange
from threading import Thread
from kivy.utils import platform
from sys import path as sysPath
from kivy.lib import osc
from app_modules.media_player.media_player_server import Media_Player_Server as Media_Player
# import app_modules.youtube.yt_loader as YT_Loader
import traceback
if platform == 'android':
    from jnius import autoclass
    from plyer import notification

def play_alarm(text):
    if platform == 'android':
        try:
            path = '/data/data/org.bakterija_git.jotube/files/beep1.wav'
            MediaPlayer = autoclass('android.media.MediaPlayer')
            AudioManager = autoclass('android.media.AudioManager')
            mPlayer = MediaPlayer()
            mPlayer.setAudioStreamType(AudioManager.STREAM_NOTIFICATION)
            mPlayer.setDataSource(path)
            mPlayer.prepare()
            sleep(0.1)
            mPlayer.start()
            sleep(0.1)
            notification.notify('DL pabeidza',text)
            sleep(0.6)
            mPlayer.release()
        except Exception as e: print(e)
    pass

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

def return_path():
    if platform == 'android':
        path = '/storage/emulated/0/github_bakterija/jotube/audio/'
    else:
        path = sysPath[0]+'/service/media/'
    return path

def unfinish(filename):
    try:
        fh = open(return_path()+'unfinished_files', 'ab')
        fh.write('\n'+filename)
        fh.close()
    except Exception as e: print(e)

def finish(filename):
    try:
        fh = readf(return_path()+'unfinished_files')
        for i,x in enumerate(fh):
            if x == filename:
                del fh[i]
        text = fh = '\n'.join(str(e) for e in fh)
        savef(text,return_path()+'unfinished_files')
    except Exception as e: print(e)

class Downloader_Local:
    def __init__(self,ID,link,queue,*arg):
        self.path = return_path()
        self.finished = False
        self.ID = str(ID)
        self.dlformat = 'video'
        b = link.find('http')
        if link[:b].find('audio') != -1: self.dlformat = 'audio'
        self.link = link[b:]
        self.filename = 'n/a'
        self.queue = queue
        queue.append('DL::Downloader-'+self.ID+':Waiting')

    def start(self):
        Thread(target=self.work).start()

    def work(self):
        ID, link, queue, path = self.ID, self.link, self.queue, self.path
        looping, filename = 2, 'noname'+str(randrange(1,10000,1))
        stopped = False
        loggerYT = YT_Loader.MyLogger()
        downloader = YT_Loader.Download_yt(logger=loggerYT,path=path, link=link, dlformat=self.dlformat)
        queue.append('DL::Downloader-'+ID+':Startup')
        dlprogress = 0.0
        filename = 'n/a'
        filename2 = 'n/a'
        sendprg = False
        uldone = False
        while looping > 0:
            sleep(0.2)
            li = loggerYT.return_new()
            for line in li:
                sleep(0.1)
                b = line.find('] Destination: ')
                if b != -1 and b < 20:
                    filename = line[b+15:]
                    queue.append('DL::Downloader-'+ID+':filename='+filename)

                a, b = line.find(' '), line.find('%')
                if a != -1 and b != -1:
                    percentage = float(line[a+1:b])
                    if percentage > dlprogress:
                        dlprogress = percentage
                        sendprg = True

                b = line.find('[YTworker] Stopped')
                if b == 0:
                    looping = 1
                    stopped = True

                if b == -1:
                    ustring = unicode(line)
                    queue.append(u'[color=ff3333][other][/color] '+ustring)

                if sendprg:
                    queue.append('DL::Downloader-'+ID+':DLPRG-'+str(dlprogress))
                    sendprg = False

            if loggerYT.stopped:
                looping -=1

        if loggerYT.success:
            filecnt, found = 1, 0
            for x in loggerYT.list:
                b = x.find('[ffmpeg] Merging formats into "')
                if b == 0: filecnt = 2
            for x in loggerYT.list:
                c = x.find('[download] 100%')
                if c != -1: found += 1
            if filecnt == found:
                b = filename.find(path)
                if b != -1:
                    filename2 = filename[len(path):]
                queue.append('DL::Downloader-'+ID+':filename='+filename2)
                sleep(0.3)
                queue.append('DL::Downloader-'+ID+':ULDONE::')
                uldone = True
            else:
                queue.append('DL::Downloader-'+ID+':Fail-Could not download')
        else:
            queue.append('DL::Downloader-'+ID+':Fail-Worker thread stopped')

        sleep(0.2)
        self.finished = True
        if uldone: queue.append('DL::Downloader-'+ID+':ULDONE::')
        queue.append('Stopped downloader'+ID)

class Service:
    def __init__(self):
        self.media_player = Media_Player()
        self.media_player.set_osc_sender(self.send_message)

        self.cl_connected, self.queue, self.dl_ID = False, [], 0
        self.sender_queue = []
        self.serverlist = []
        self.looping = True
        self.dlmode = 'Sequential'
        osc.init()
        self.eventThread()

    def osc_callback(self,message,*args):
        if message[0] == '/jotube_api':
            data = message[2]
            # print data
            if data[:8] == 'audioCL:':
                self.media_player.osc_callback(data[8:])
            elif data == 'OPEN::':
                self.cl_connected = True
                self.media_player.enable_sender()
            elif data == 'CLOSE::' or data == 'close::':
                self.cl_connected = False
                self.media_player.disable_sender()
            elif data[:10] == 'DOWNLOAD::':
                self.dl_ID += 1
                if self.dlmode == 'Sequential':
                    self.queue.append(['START-DOWNLOADER',(self.dl_ID,data[10:],self.queue,self.serverlist)])
            elif data[:9] == 'DLMODES::':
                self.dlmode = data[9:]
            elif data == 'STOP::':
                self.looping = False

    def send_message(self,text,api='/jotube_api'):
        self.sender_queue.append([api, text])
    def _send_message(self,text,api='/jotube_api'):
        osc.sendMsg(api, [text], port=44772)

    def eventThread(self):
        downloaders, active_downloader = [], False
        buffered = []
        oscid = osc.listen(ipAddr='127.0.0.1', port=44771)
        osc.bind(oscid, self.osc_callback, '/jotube_api')
        while self.looping:
            osc.readQueue(oscid)
            if active_downloader == False:
                if len(downloaders) > 0:
                    active_downloader = downloaders[0]
                    downloaders[0].start()
            else:
                if active_downloader.finished == True:
                    play_alarm(active_downloader.filename)
                    active_downloader = False
                    del downloaders[0]
            if self.cl_connected:
                for x in buffered:
                    osc.sendMsg('/jotube_api', [str(x)], port=44772)
                    del buffered[0]
                    sleep(0.05)
            for x in list(self.queue):
                if x[0] == 'START-DOWNLOADER':
                    if self.dlmode == 'Sequential':
                        dlobj = Downloader_Local(x[1][0],x[1][1],x[1][2],x[1][3])
                        downloaders.append(dlobj)
                else:
                    if self.cl_connected:
                        osc.sendMsg('/jotube_api', [str(x)], port=44772)
                    else: buffered.append(x)
                del self.queue[0]
                sleep(0.05)
            if self.media_player.server_active:
                self.media_player.update(self.cl_connected)
            for api,text in list(self.sender_queue):
                self._send_message(text, api=api)
                del self.sender_queue[0]
                sleep(0.05)
            sleep(0.5)


def main_loop():
    try:
        service = Service()
        osc.dontListen()
    except Exception as e:
        traceback.print_exc()

if __name__ == '__main__':
    main_loop()
