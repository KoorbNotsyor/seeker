#! python3
#

import sys
import logging
import mmap
import re

from kivy.app import App
from kivy.uix.layout import Layout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import ObjectProperty

usage = '''
- Usage:
-        py.exe seeker.py <ile path> <seek text> <seek delta> <length> <stdout=<found-1>\n<found-2>\n...>
-
'''


def printUsage():
    print(usage)


class Interface(BoxLayout):

    def exitButton(self):
        print('EXIT!!!')
        sys.exit(0)


    def dumpContainerMetrics(self, info, widget):
        ''' Called for a container...  '''
        def doWidget(w):
            print('-'*100)
            print('[{1}]-[{0}]'.format(w, w.uid))

            if isinstance(w, Layout):
                print('LAYOUT: orientation [{0}]'.format(w.orientation))
                str = ''
                if hasattr(w, 'padding'):
                    str += ' padding [{0}]'.format(w.padding)
                if hasattr(w, 'spacing'):
                    str += ' spacing [{0}]'.format(w.spacing)
                if hasattr(w, 'minimum_size'):
                    str += ' minimum_size [{0}]'.format(w.minimum_size)
                if len(str) > 0:
                    print('{0}'.format(str))

            if isinstance(w, ToggleButton):
                print('TOGGLEBUTTON:')
            elif isinstance(w, Button):
                print('BUTTON:')
            elif isinstance(w, Label):
                print('LABEL:')

            if hasattr(w, 'text'):
                print(' text [{0}]'.format(w.text))
                print(' text_size [{0}] halign [{1}] valign [{2}] padding [{3}]'.format(w.text_size,
                                                                                        w.halign,
                                                                                        w.valign,
                                                                                        w.padding
                                                                                        ))
                print(' texture_size [{0}] texture [{1}]'.format(w.texture_size, w.texture))

            print(' pos_hint: [{0}] size_hint: [{1}] size_hint_max: [{2}] size_hint_min: [{3}]'.format(w.pos_hint,
                                                                                                       w.size_hint,
                                                                                                       w.size_hint_max,
                                                                                                       w.size_hint_min
                                                                                                       ))
            print(' x [{0}] y [{1}] W [{2}] H [{3}] size: [{4}]'.format(w.x, w.y, w.width, w.height, w.size))


        print('===>{0}...'.format(info))
        for w in widget.walk(restrict=True):
            doWidget(w)

    def doSize(self, args):
        print('+'*100)
        print('SIZE event: [{0}]'.format(args))
        self.dumpContainerMetrics(' @sized', self)

    def doTouch(self, args):
        print('+'*100)
        print('TOUCH event: [{0}] pos=[{1}]'.format(args[0], args[1].pos))
        self.dumpContainerMetrics(' @touched', self)


class seekerApp(App):

    exit_button = ObjectProperty()

    def build(self):
        ui = Interface()
        #  ---ui.dumpContainerMetrics(' @end of build', ui)
        return ui


def seekerCLI():

    # What to do?
    if len(sys.argv) != 5:
        printUsage()
        return -1

    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    filepath = sys.argv[1]
    seektext = sys.argv[2]
    seekdelta = sys.argv[3]
    seeklength = sys.argv[4]

    try:

        pattern = re.compile(rb'(\.\W+)?([^.]?video[^.]*?\.)', re.DOTALL | re.IGNORECASE | re.MULTILINE)

        with open(filepath, 'r', encoding='utf-8') as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as m:
                for match in pattern.findall(m):
                    print(match[1].replace(b'\n', b' '))

    except Exception as e:
        logging.exception('!!! Unexpected exception !!! [{0}]'.format(e))

    return 0


if __name__ == '__main__':
    seekerApp().run()

