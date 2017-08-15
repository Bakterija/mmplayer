from kivy.properties import (StringProperty, ListProperty, NumericProperty,
                             ObjectProperty, BooleanProperty)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.logger import Logger
from kivy.compat import string_types
from kivy.factory import Factory
from kivy.clock import Clock, mainthread
from databox import DataBox
from kivy.core.window import Window
from time import time


__all__ = ('RecycleDataView', 'RecycleDataBox')


class RecycleDataView(object):
    '''refresh_view_attrs is called every time when DataBox data is updated,
    to update child attributes from that. Inherit from this class to have a
    widget which can work as a DataBox viewclass
    '''
    index = 0
    rv = None

    def refresh_view_attrs(self, rv, index, data):
        '''Attributes are set from data dict keys and values'''
        self.index = index
        self.rv = rv
        
        for k, v in data.iteritems():
            setattr(self, k, v)

    def on_height(self, a, value):
        self.rv.height_cache[self.index] = value


class RecycleDataBox(BoxLayout):
    data = ListProperty()
    '''The data used by DataBox. This is a list of dicts whose
    keys map to the corresponding property names of the viewclass'''

    viewclass = StringProperty()
    '''The viewclass that will be generated from each data dict'''

    use_recycling = False

    scroller = ObjectProperty()

    viewclass_class = None

    last_height = NumericProperty()
    default_height = NumericProperty(100) # default hight of viewclasses
    max_viewclasses = 0 # scroller.height / default_height + margin
    indexed_widgets = False
    can_scroll = 1
    last_scroll = 0.0
    scheduled_scroll = False

    def __init__(self, data=None, **kwargs):
        super(RecycleDataBox, self).__init__(**kwargs)
        self._topwidget = ShellWidget(place='top')
        self._botwidget = ShellWidget(place='bot')
        self.view = BoxLayout(size_hint_y=None, orientation='vertical')
        self.view.bind(minimum_size=self.view.setter('size'))
        self.height_cache = {}
        for widget in self._topwidget, self.view, self._botwidget:
            self.add_widget(widget)

    def on_height(self, _, value):
        self.last_height = value

    def on_scroller(self, _, scroller):
        if scroller:
            if not self.view.children and self.data:
                self.on_data(None, self.data)
            scroller.bind(height=self.on_scroller_height)
            scroller.bind(scroll_y=self.on_scrolling)
            self.on_scroller_height(scroller, scroller.height)

    def on_scroller_height(self, scroller, value):
        self.max_viewclasses = int((value * 2) / self.default_height)


    def fin2(self, *args):
        if not self.scheduled_scroll:
            self.can_scroll = 1
            Clock.schedule_once(lambda *a: self.on_scrolling(
                None, -1, sc=True), 0.1)
            self.scheduled_scroll = True

    @mainthread
    def unlock_scroll(self):
        self.can_scroll = 1
    @mainthread
    def on_scrolling(self, scroller, scroll_y, force=False, move_one=False, sc=False):
        if self.scheduled_scroll:
            self.scheduled_scroll = False
            
        if not self.use_recycling:
            return

        if not self.can_scroll and not force:
            return self.unlock_scroll()

        winheight = Window.system_size[1]
        maxpos, minpos = winheight * 1.2, winheight * -0.2

        center = self.view.children[int(len(self.view.children) / 2)]
        center_pos = center.to_window(*center.pos)[1]
        top = self.view.children[-1]
        top_pos = top.to_window(0, top.top)[1]
        bot = self.view.children[0]
        bot_pos = bot.to_window(0, bot.y)[1]
        
        if not move_one:
            
            if top_pos < minpos - winheight:
                self._topwidget.swap_height(top_pos - winheight)
            elif bot_pos > maxpos + winheight:
                self._botwidget.swap_height(top_pos - winheight)
            else:
                move_one = True
                

        if move_one:
            cnt = 0
            if top_pos <= maxpos:
                self._topwidget.swap_one()
                sc = False
                
            elif bot_pos >= minpos:
                self._botwidget.swap_one()
                sc = False

        self.can_scroll = 0
        self.unlock_scroll()
        if not sc:
            Clock.schedule_once(self.fin2, 0)

    def refresh_indexes(self, data):

        if not self._topwidget.fake_children:
            start_index = 0
        else:
            start_index = self._topwidget.highest_index + 1

        for i, child in enumerate(reversed(self.view.children)):
            i += start_index
            child.refresh_view_attrs(self, i, data[i])

    def move_view_index(self, index):
        for i, child in enumerate(reversed(self.view.children)):
            new_index = i + index
            child.refresh_view_attrs(self, new_index, self.data[new_index])

    def move_view_top(self):
        top = self.view.children[-1]
        bot = self.view.children[0]
        old_index = bot.index
        new_index = top.index - 1
        self.height_cache[bot.index] = bot.height
        self.view.remove_widget(bot)
        self.view.add_widget(bot, index=len(self.view.children))
        bot.refresh_view_attrs(self, new_index, self.data[new_index])
        return new_index, old_index

    def move_view_bot(self):
        top = self.view.children[-1]
        bot = self.view.children[0]
        old_index = top.index
        new_index = bot.index + 1
        self.height_cache[top.index] = top.height
        self.view.remove_widget(top)
        self.view.add_widget(top)
        top.refresh_view_attrs(self, new_index, self.data[new_index])
        return new_index, old_index

    def on_data(self, _, data):
        if self.viewclass_class and self.scroller and self.max_viewclasses:
            data_count = len(data)

            # Use normal behavior when data is short
            if data_count <= self.max_viewclasses:
                self._botwidget.height = 0
                self._topwidget.height = 0
                self.use_recycling = False
                return self.on_data_no_recycle(None, data)

            if not self.use_recycling:
                self.use_recycling = True
                for i in range(self.max_viewclasses):
                    instance = self.viewclass_class()
                    self.view.add_widget(instance)

            children_count = self.get_children_count()

            if children_count != data_count:
                # Add
                if children_count < data_count:
                    for count in range(data_count - children_count):
                        self._botwidget.add_widget()
                # Remove
                else:
                    counter = 0
                    while counter < children_count - data_count:
                        if self._botwidget.fake_children:
                            self._botwidget.remove_widget()
                        else:
                            self._topwidget.remove_widget()
                        counter += 1

            self.refresh_indexes(data)

    def on_data_no_recycle(self, _, data):
        if len(self.view.children) > self.max_viewclasses:
            self.clear_widgets()

        if self.viewclass_class:
            children_count = len(self.view.children)
            data_count = len(data)

            if children_count != data_count:
                if children_count < data_count:
                    for count in range(data_count - children_count):
                        self.view.add_widget(self.viewclass_class())
                else:
                    for count in range(children_count - data_count):
                        self.view.remove_widget(self.view.children[-1])

            if self.view.children:
                for i, child in enumerate(reversed(self.view.children)):
                    child.refresh_view_attrs(self, i, data[i])

    def get_view_count(self):
        return len(self.view.children)

    def get_children_count(self):
        return (
            len(self._topwidget.fake_children) +
            len(self.view.children) +
            len(self._botwidget.fake_children))

    def refresh_from_data(self, *args):
        self.on_data(None, self.data)

    def on_viewclass(self, instance, value):
        if isinstance(value, string_types):
            self.viewclass_class = getattr(Factory, value)
            self.on_data(None, self.data)
        else:
            Logger.error(
                "{}: on_viewclass: {} is not an instance".format(self, e))


class ShellWidget(Widget):
    place = StringProperty()
    other = ObjectProperty()
    default_height = NumericProperty()
    highest_index = None
    lowest_index = None

    def __init__(self, **kwargs):
        super(ShellWidget, self).__init__(**kwargs)
        self.size_hint_y, self.height = None, 0
        self.fake_children = {}

    def on_parent(self, _, parent):
        if self.place == 'top':
            self.other = parent._botwidget
        elif self.place == 'bot':
            self.other = parent._topwidget
        self.default_height = parent.default_height
        self.parent.bind(default_height=self.setter('default_height'))

    def add_widget(self, index=None, height=0):
        if index is None:
            if self.place == 'bot':
                len_other = len(self.other.fake_children)
                len_view = len(self.parent.view.children)
                index = len(self.fake_children) + len_other + len_view
            else:
                index = len(self.fake_children)

        if not self.lowest_index:
            self.lowest_index = index
        if not self.highest_index:
            self.highest_index = index

        if not height:
            if index in self.parent.height_cache:
                height = self.parent.height_cache[index]
            else:
                height = self.default_height

        if index > self.highest_index:
            self.highest_index = index
        elif index <= self.lowest_index:
            self.lowest_index = index

        self.fake_children[index] = {'index': index, 'height': height}
        self.height += height

    def remove_widget(self, index=None):
        if not index:
            if self.place == 'top':
                index = self.highest_index
            else:
                index = self.highest_index

        try:
            self.height -= self.fake_children[index]['height']
            del self.fake_children[index]
        except Exception as e:
            print 'ERROR KEY', e
            print 'LOW', self.lowest_index, 'HIGH', self.highest_index
            raise Exception('NAAV')

        if index == self.highest_index:
            for x in reversed(range(self.lowest_index - 1, self.highest_index)):
                if x in self.fake_children:
                    self.highest_index = x
                    break

        elif index == self.lowest_index:
            for x in range(self.lowest_index - 1, self.highest_index + 1):
                if x in self.fake_children:
                    self.lowest_index = x
                    break

    def remove_widgets_fast(self, start, stop):
        stop = stop + 1
        for index in range(start, stop):
            # print index
            self.height -= self.fake_children[index]['height']
            del self.fake_children[index]

    def clear_widgets(self):
        self.fake_children = {}
        self.height = 0

    def swap_height(self, pos):
        if not self.fake_children:
            return
##        print ('{}: swap_height: {}'.format(self.place.upper(), pos))

        view_count = self.parent.get_view_count()
        child_count = len(self.fake_children)
        pos = abs(pos)
        height_adjust = self.height - pos
        remlist = []
        if self.place == 'bot':
            view_count = -view_count
            view_index = -child_count
            iter_range = range(self.lowest_index, self.highest_index + 1)
        else:
            view_index = child_count
            iter_range = reversed(range(self.lowest_index, self.highest_index + 1))

        height = self.height
        time0 = time()
        for i in iter_range:
            if i not in self.fake_children:
                break
            index, child = i, self.fake_children[i]
            remlist.append(index)
            height -= child['height']
            self.other.add_widget(
                index=index + view_count,
                height=child['height'])
            if height <= height_adjust:
                break


        len_remlist = len(remlist)
        if len_remlist:
            time1 = time() - time0

            if self.place == 'top':
                self.remove_widgets_fast(remlist[-1], remlist[0])
                self.highest_index -= len_remlist
                self.parent.move_view_index(self.highest_index + 1)
            else:
                self.remove_widgets_fast(remlist[0], remlist[-1])
                self.lowest_index += len_remlist
                self.parent.move_view_index(self.other.highest_index + 1)
                self.highest_index = self.lowest_index + len(
                    self.fake_children) - 1

            time2 = time() - time0

    def swap_one(self):
        if not self.fake_children:
            return

        if self.place == 'top':
            rem_index, add_index = self.parent.move_view_top()
        else:
            rem_index, add_index = self.parent.move_view_bot()

##        print ('{}: swap_one: {} to {}'.format(
##            self.place.upper(), rem_index, add_index))

        self.remove_widget(index=rem_index)
        self.other.add_widget(index=add_index)


