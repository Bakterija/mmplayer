from __future__ import print_function


class Media_Seeker(object):
    def __init__(self):
        super(Media_Seeker, self).__init__(**kwargs)

    def touch_seek(self,slider,touch):
        if touch.pos[0] > slider.pos[0] and touch.pos[0] < slider.pos[0]+slider.size[0]:
            if touch.pos[1] > slider.pos[1] and touch.pos[1] < slider.pos[1]+slider.size[1]:
                self.seekLock = True

    def release_seek(self,slider,touch):
        if touch.pos[0] > slider.pos[0] and touch.pos[0] < slider.pos[0]+slider.size[0]:
            if touch.pos[1] > slider.pos[1] and touch.pos[1] < slider.pos[1]+slider.size[1]:
                if self.seekLock:
                    self.mPlayer.seek(self.seek_slider.value)
                    m, s = divmod(int(self.seek_slider.value), 60)
                    s = str(m).zfill(2)+':'+str(s).zfill(2)
                    self.seek_label1.text = s
                    self.skipSeek = 2
                self.seekLock = False

    def func_seek(self,value):
        self.mPlayer.seek(int(value))

    def update_seek(self,*arg):
        try:
            if self.skipSeek == 0:
                values = self.mPlayer.return_pos()
                if self.mPlayer.sound.state == 'play':
                    b = values[0].find('/')
                    self.seek_label1.text = values[0][:b]
                    self.seek_label2.text = values[0][b+1:]
                    if not self.seekLock:
                        self.seek_slider.value = values[1][0]
                        self.seek_slider.max = values[1][1]
            else:
                self.skipSeek -= 1
        except Exception as e:
            print(e)
        Clock.schedule_once(self.update_seek,0.5)
