__all__ = ('AppProgressBar', )

from kivy.properties import NumericProperty, AliasProperty
from kivy.uix.widget import Widget
from kivy.lang import Builder

Builder.load_string('''
<AppProgressBar>:
    canvas:
        Color:
            rgb: 1, 1, 1
        BorderImage:
            border: (12, 12, 12, 12)
            pos: self.x, self.center_y - 12
            size: self.width, 24
            source: 'atlas://data/images/defaulttheme/progressbar_background'
        BorderImage:
            border: [int(min(self.width * (self.value / float(self.max)) if self.max else 0, 12))] * 4
            pos: self.x, self.center_y - 12
            size: self.width * (self.value / float(self.max)) if self.max else 0, 24
            source: 'atlas://data/images/defaulttheme/progressbar'
''')


class AppProgressBar(Widget):
    '''Class for creating a progress bar widget.

    See module documentation for more details.
    '''

    def __init__(self, **kwargs):
        self._value = 0.
        super(AppProgressBar, self).__init__(**kwargs)

    def _get_value(self):
        return self._value

    def _set_value(self, value):
        value = max(0, min(self.max, value))
        if value != self._value:
            self._value = value
            return True

    value = AliasProperty(_get_value, _set_value)
    '''Current value used for the slider.

    :attr:`value` is an :class:`~kivy.properties.AliasProperty` that
    returns the value of the progress bar. If the value is < 0 or >
    :attr:`max`, it will be normalized to those boundaries.

    .. versionchanged:: 1.6.0
        The value is now limited to between 0 and :attr:`max`.
    '''

    def get_norm_value(self):
        d = self.max
        if d == 0:
            return 0
        return self.value / float(d)

    def set_norm_value(self, value):
        self.value = value * self.max

    value_normalized = AliasProperty(get_norm_value, set_norm_value,
                                     bind=('value', 'max'))
    '''Normalized value inside the range 0-1::

        >>> pb = ProgressBar(value=50, max=100)
        >>> pb.value
        50
        >>> pb.value_normalized
        0.5

    :attr:`value_normalized` is an :class:`~kivy.properties.AliasProperty`.
    '''

    max = NumericProperty(100.)
    '''Maximum value allowed for :attr:`value`.

    :attr:`max` is a :class:`~kivy.properties.NumericProperty` and defaults to
    100.
    '''


if __name__ == '__main__':

    from kivy.base import runTouchApp
    runTouchApp(AppProgressBar(value=50))
