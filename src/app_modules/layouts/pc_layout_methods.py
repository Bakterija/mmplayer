from kivy.animation import Animation
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.properties import BooleanProperty
from kivy.logger import Logger


class LayoutMethods(object):
    '''These are methods for large screen desktop computers,
    Inherited by root widget'''
    hovering_side_bar = False
    hovering_lower_bar = False
    video_screen = False
    video_playing = False
    maximized = False
    mouse_inside = BooleanProperty()
    video_animspeed = 0.1

    def init_widgets(self, *args):
        Window.bind(mouse_pos=self.on_mouse_move)
        Window.bind(on_maximize=self.on_maximize)
        Window.bind(on_restore=self.on_restore)
        Window.bind(on_cursor_enter=self.on_cursor_enter)
        Window.bind(on_cursor_leave=self.on_cursor_leave)
        self.bind(size=self.on_size)
        self.bind(sm_area_width=self.on_size)
        self.bind(lower_bar_offset_y=self.on_size)
        self.bind(side_bar_offset_x=self.on_size)
        self.bind(upper_bar_offset_y=self.on_size)
        self.manager.ids.videoframe.full_screen_check = self.is_playing
        self.manager.bind(current=self.restore_window)

    def on_cursor_enter(self, *args):
        self.mouse_inside = True

    def on_cursor_leave(self, *args):
        self.mouse_inside = False
        self.on_mouse_move(None, (-1,-1))

    def restore_window(self, *args):
        Logger.info('ScreenManager: ids:{}'.format(self.manager.ids))
        if self.manager.ids.videoframe.maximized:
            self.manager.ids.videoframe.maximize_borderless_toggle()

    def is_playing(self):
        return self.video_playing

    def on_maximize(self, *args):
        self.maximized = True

    def on_restore(self, *args):
        self.maximized = False

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
        if not self.video_screen or not self.video_playing:
            return

        if self.mouse_inside:
            if not self.hovering_side_bar:
                if pos[0] < self.ids.sidebar.width:
                    self.hovering_side_bar = True
                    self.anim_side_bar_in()

            elif self.hovering_side_bar and not self.ids.sidebar.resizing:
                if pos[0] > self.ids.sidebar.width + dp(30):
                    self.hovering_side_bar = False
                    self.anim_side_bar_out()

            if not self.hovering_lower_bar:
                if pos[1] < self.lower_bar_height:
                    self.hovering_lower_bar = True
                    self.anim_lower_bar_in()

            elif self.hovering_lower_bar:
                if pos[1] > self.lower_bar_height + dp(30):
                    self.hovering_lower_bar = False
                    self.anim_lower_bar_out()
        else:
            if self.hovering_side_bar:
                self.hovering_side_bar = False
                self.anim_side_bar_out()

            if self.hovering_lower_bar:
                self.hovering_lower_bar = False
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
                             d=self.video_animspeed, t='in_quad')
            anim.start(self)
        if not self.hovering_side_bar:
            anim3 = Animation(side_bar_offset_x=self.ids.sidebar.width + 2,
                             d=self.video_animspeed, t='in_quad')
            anim3.start(self)
        anim2 = Animation(upper_bar_offset_y=self.upper_bar_height + 2,
                         d=self.video_animspeed, t='in_quad')
        anim2.start(self)

    def full_window_video_out(self, *args):
        if not self.hovering_lower_bar:
            anim = Animation(lower_bar_offset_y=0,
                             d=self.video_animspeed, t='out_quad')
            anim.start(self)
        if not self.hovering_side_bar:
            anim3 = Animation(side_bar_offset_x=0,
                             d=self.video_animspeed, t='out_quad')
            anim3.start(self)
        anim2 = Animation(upper_bar_offset_y=0,
                         d=self.video_animspeed, t='out_quad')
        anim2.start(self)

    def anim_lower_bar_in(self, *args):
        anim = Animation(lower_bar_offset_y=0,
                         d=self.video_animspeed, t='in_quad')
        anim.start(self)

    def anim_lower_bar_out(self, *args):
        anim = Animation(lower_bar_offset_y=self.lower_bar_height + 2,
                         d=self.video_animspeed, t='out_quad')
        anim.start(self)

    def anim_side_bar_in(self, *args):
        anim = Animation(side_bar_offset_x=0,
                         d=self.video_animspeed, t='out_quad')
        anim.start(self)

    def anim_side_bar_out(self, *args):
        anim = Animation(side_bar_offset_x=self.ids.sidebar.width + 2,
                         d=self.video_animspeed, t='in_quad')
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
