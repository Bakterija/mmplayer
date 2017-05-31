from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty, ListProperty


class ConditionLayout(BoxLayout):
    '''This layout adds widgets to itself only when it's
    condition BooleanProperty is True

    Unadded children are kept in conditional_children ListProperty
    '''

    condition = BooleanProperty(False)
    '''BooleanProperty. Children are added when it is True
    and hidden when it is False'''

    conditional_children = ListProperty()
    '''ListProperty where hidden children are stored'''

    def on_condition(self, _, value):
        '''Adds or hides children depending on self.condition'''
        if self.condition:
            for widget in self.conditional_children:
                super(ConditionLayout, self).add_widget(widget, index=0)
        else:
            for widget in self.conditional_children:
                super(ConditionLayout, self).remove_widget(widget)

    def add_widget(self, widget, index=0):
        '''Modified method to hide children when condition is False'''
        self.conditional_children.append(widget)
        if self.condition:
            super(ConditionLayout, self).add_widget(widget, index=index)

    def remove_widget(self, widget):
        '''Modified method to remove hidden children when condition is False
        '''
        if self.conditional_children:
            super(ConditionLayout, self).remove_widget(widget)
        self.conditional_children.remove(widget)

    def clear_widgets(self, children=None):
        '''Modified method to also clear self.conditional_children'''
        super(ConditionLayout, self).clear_widgets(children=None)
        self.conditional_children = []
