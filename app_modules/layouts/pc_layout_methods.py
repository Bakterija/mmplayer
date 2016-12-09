from kivy.animation import Animation
from kivy.core.window import Window
from kivy.metrics import dp

class LayoutMethods(object):
    hovering_side_bar = False
    hovering_lower_bar = False
    video_screen = False
    video_playing = False

    def init_widgets(self, *args):
        Window.bind(mouse_pos=self.on_mouse_move)
        self.bind(size=self.on_size)
        self.bind(sm_area_width=self.on_size)
        self.bind(lower_bar_offset_y=self.on_size)
        self.bind(side_bar_offset_x=self.on_size)
        self.bind(upper_bar_offset_y=self.on_size)

    def on_size(self, *args):
        if not self.video_screen:
            self.ids.sm_area.size = (self.sm_area_width, self.sm_area_height)
            self.ids.sm_area.pos = (
                self.ids.sidebar.width, self.lower_bar_height)
        else:
            self.ids.sm_area.size = self.size
            self.ids.sm_area.pos = (0, 0)
            # Default behavior is to have video screen take the whole Window,
            # the commented out script would make it less space when side bar,
            # lower bar or upper bar are in window
            # self.ids.sm_area.size = (
            #     self.sm_area_width + self.side_bar_offset_x,
            #     self.sm_area_height + self.lower_bar_offset_y +
            #     self.upper_bar_offset_y)
            # self.ids.sm_area.pos = (
            #     self.side_bar_width - self.side_bar_offset_x,
            #     self.lower_bar_height - self.lower_bar_offset_y)

    def on_mouse_move(self, obj, pos):
        if pos[0] < self.ids.sidebar.width:
            if not self.hovering_side_bar:
                self.hovering_side_bar = True
                if self.video_screen and self.video_playing:
                    self.anim_side_bar_in()

        elif self.hovering_side_bar and not self.ids.sidebar.resizing:
            if pos[0] > self.ids.sidebar.width + dp(30):
                self.hovering_side_bar = False
                if self.video_screen and self.video_playing:
                    self.anim_side_bar_out()

        if pos[1] < self.lower_bar_height:
            if not self.hovering_lower_bar:
                self.hovering_lower_bar = True
                if self.video_screen and self.video_playing:
                    self.anim_lower_bar_in()

        elif self.hovering_lower_bar:
            if pos[1] > self.lower_bar_height + dp(30):
                self.hovering_lower_bar = False
                if self.video_screen and self.video_playing:
                    self.anim_lower_bar_out()

    def on_video_screen(self, screen, playing):
        if screen and playing:
            self.full_window_video_in()
        else:
            self.full_window_video_out()
        self.video_screen = screen
        self.video_playing = playing

    def full_window_video_in(self, *arg):
        if not self.hovering_lower_bar:
            anim = Animation(lower_bar_offset_y=self.lower_bar_height + 2,
                             d=0.2, t='in_quad')
            anim.start(self)
        if not self.hovering_side_bar:
            anim3 = Animation(side_bar_offset_x=self.ids.sidebar.width + 2,
                             d=0.2, t='in_quad')
            anim3.start(self)
        anim2 = Animation(upper_bar_offset_y=self.upper_bar_height + 2,
                         d=0.2, t='in_quad')
        anim2.start(self)

    def full_window_video_out(self, *args):
        if not self.hovering_lower_bar:
            anim = Animation(lower_bar_offset_y=0,
                             d=0.2, t='in_quad')
            anim.start(self)
        if not self.hovering_side_bar:
            anim3 = Animation(side_bar_offset_x=0,
                             d=0.2, t='in_quad')
            anim3.start(self)
        anim2 = Animation(upper_bar_offset_y=0,
                         d=0.2, t='in_quad')
        anim2.start(self)

    def anim_lower_bar_in(self, *args):
        anim = Animation(lower_bar_offset_y=0,
                         d=0.2, t='in_quad')
        anim.start(self)

    def anim_lower_bar_out(self, *args):
        anim = Animation(lower_bar_offset_y=self.lower_bar_height + 2,
                         d=0.2, t='in_quad')
        anim.start(self)

    def anim_side_bar_in(self, *args):
        anim = Animation(side_bar_offset_x=0,
                         d=0.2, t='in_quad')
        anim.start(self)

    def anim_side_bar_out(self, *args):
        anim = Animation(side_bar_offset_x=self.ids.sidebar.width + 2,
                         d=0.2, t='in_quad')
        anim.start(self)

    def on_touch_down(self, touch):
        if self.video_screen and self.video_playing:
            if not self.hovering_side_bar and not self.hovering_lower_bar:
                if touch.button == 'scrollup':
                    self.ids.playback_bar.volume_decrease()
                    return True
                elif touch.button == 'scrolldown':
                    self.ids.playback_bar.volume_increase()
                    return True
        super(LayoutMethods, self).on_touch_down(touch)
