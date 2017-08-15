from kivy.properties import StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.logger import Logger
from kivy.compat import string_types
from kivy.factory import Factory


class DataView(object):
    '''refresh_view_attrs is called every time when DataBox data is updated,
    to update child attributes from that. Inherit from this class to have a
    widget which can work as a DataBox viewclass
    '''

    def refresh_view_attrs(self, rv, index, data):
        '''Attributes are set from data dict keys and values'''
        for k, v in data.iteritems():
            setattr(self, k, v)


class DataBox(BoxLayout):
    data = ListProperty()
    '''The data used by DataBox. This is a list of dicts whose
    keys map to the corresponding property names of the viewclass
    '''

    viewclass = StringProperty()
    '''
    The viewclass that will be generated from each data dict
    '''

    viewclass_class = None

    def __init__(self, **kwargs):
        super(DataBox, self).__init__(**kwargs)

    def on_data(self, instance, value):
        if self.viewclass_class:
            children_count = len(self.children)
            value_count = len(value)
            if children_count != value_count:
                if children_count < value_count:
                    for count in range(0, value_count - children_count):
                        self.add_widget(self.viewclass_class())
                else:
                    for count in range(0, children_count - value_count):
                        self.remove_widget(self.children[-1])

            if self.children:
                try:
                    for i, child in enumerate(reversed(self.children)):
                        child.refresh_view_attrs(self, i, value[i])
                except AttributeError as e:
                    # Force update viewclass which doesn't have a
                    # refresh_view_attrs method
                    if str(
                        e).find("has no attribute 'refresh_view_attrs'") != -1:
                            for i, child in enumerate(reversed(self.children)):
                                for k, v in value[i].iteritems():
                                    setattr(child, k, v)


    def on_viewclass(self, instance, value):
        if isinstance(value, string_types):
            self.viewclass_class = getattr(Factory, value)
            self.on_data(None, self.data)
        else:
            Logger.error(
                "{}: on_viewclass: {} is not an instance".format(self, e))

    def refresh_from_data(self, *args):
        self.on_data(None, self.data)


if __name__ == '__main__':
    from kivy.app import App
    from kivy.uix.button import Button
    from kivy.uix.scrollview import ScrollView
    from kivy.metrics import cm


    class DataButton(DataView, Button):
        print_text = StringProperty()
        def __init__(self, **kwargs):
            super(DataButton, self).__init__(**kwargs)
            self.size_hint_y = None
            self.height = cm(1)

        def on_release(self, *args):
            print(self.print_text)


    class DataBoxExample(App):
        def build(self):
            scroller = ScrollView()
            data_box = DataBox(orientation='vertical', viewclass='DataButton', size_hint_y=None)
            data_box.bind(minimum_height=data_box.setter('height'))
            scroller.add_widget(data_box)
            for i in range(0, 20):
                data_box.data.append(
                    {'text': 't' + str(i), 'print_text': str(i * 3 + 2)})
            return scroller

    app = DataBoxExample()
    app.run()
