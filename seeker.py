#! python3

# TODO manage default locations/options for filebrowser
# TODO open specified file using mmap technique
# TODO search...
# TODO save results to CSV(?)
# TODO do regex search
# TODO build stand-alone for w10, linux, android

# To get Kivy Garden FileBrowser...
# In terminal within project IDE:
#
#    pip install https://github.com/kivy-garden/filebrowser/archive/master.zip
#

import sys

# Set up some kivy config...
import configKivy

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.label import Label
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import Button
from kivy.properties import NumericProperty, BooleanProperty, ListProperty, ObjectProperty, ColorProperty
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.core.window import Window

from kivy.uix.popup import Popup
from kivy_garden.filebrowser import FileBrowser

# TODO move to config
NO_OF_DATA_ROWS = 500

# ----- TODO Move to AZWidgets.py ASAP!!!! -----

class AZLeftButton(Button):
    """ Wotsit ? """

class AZRecycleRow(RecycleDataViewBehavior, BoxLayout):
    """ Wotsit ? """

    index = None

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(AZRecycleRow, self).refresh_view_attrs(rv, index, data)

    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view. """
        self.selected = is_selected
#        if is_selected:
#            print("ROW selection changed to {0}".format(rv.data[index]))
#        else:
#            print("ROW selection removed for {0}".format(rv.data[index]))

# ------------------------------------------


class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior, RecycleGridLayout):
    """ Adds selection and focus behaviour to the view. """


class SelectableButton(RecycleDataViewBehavior, Button):
    """ Add selection support to the Label """
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        """ Add selection on touch down """
        print('x {0} , right {1} , y {2} , top {3} : hit x {4} y {5} [{6}] index [{7}]'.format(
                                                            self.x, self.right,
                                                            self.y, self.top,
                                                            touch.x, touch.y,
                                                            self.text,
                                                            self.index
                                                            ))
        if super(SelectableButton, self).on_touch_down(touch):
            print('>touched [r={2}, c={3}] : index [{1}]=[{0}]'.format(self.text,
                                                                 self.index,
                                                                 self.row,
                                                                 self.col
                                                                ))
            return True
        if self.collide_point(*touch.pos):
            if self.selectable:
                return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view. """
        self.selected = is_selected
        if is_selected:
            print("ITEM selection changed to {0}".format(rv.data[index]))
        else:
            print("ITEM selection removed for {0}".format(rv.data[index]))

class Interface(BoxLayout):

    # see getResults()...
    results = ListProperty()

    column_headings = ObjectProperty(None)

    targetString = ''
    targetIsRegex = False
    saveResultsFilepath = ''

    def initialise(self):
        # ####self.ui_getresults_button.disabled = True
        self.ui_saveresults_button.disabled = True
        self.setDataColumnHeadings()
        self.setEmptyDataGrid(0)
        # ---self.setDummyDataGrid(0)

    def setDataColumnHeadings(self):
        for heading in ('Offset', 'Length'):
            w = Button(text=heading, background_color=[1, 0, 1, 1])
            self.ui_column_headings.add_widget(w)
        w = AZLeftButton(text='Data', background_color=[1, 0, 1, 1])
        self.ui_column_headings.add_widget(w)

    def setEmptyDataGrid(self, start):
        for i in range(start, NO_OF_DATA_ROWS):
            self.results.append([['', i, 0], [''], ['']])

    def setDummyDataGrid(self, start):
        for i in range(start, NO_OF_DATA_ROWS):
            self.results.append([[str(i), i, 0], ['100'], ['--some data {0} -'.format(str(i))]])

    def exitApp(self):
        print('EXIT!!!')
        sys.exit(0)

    def doCancel(self, instance):
        self._popup.dismiss()

    # this is a callback from the 'Choose' button
    def chooseFile(self, *args):
        self._fbrowser = FileBrowser(select_string='Choose')
        self._fbrowser.bind(on_success=self.setChosenFile,
                            on_canceled=self.doCancel
                            )
        self._popup = Popup(title='Choose target file',
                            content=self._fbrowser,
                            size_hint=(0.9, 0.9),
                            auto_dismiss=False
                            )
        self._popup.open()
        return

    def setChosenFile(self, instance):
        self.ui_target_filepath.text = instance.filename
        self.ui_getresults_button.disabled = False
        self._popup.dismiss()

    # this is a callback from the 'Search' button
    def getResults(self, *args):
        print('GET RESULTS!!!')

        self.results.clear()

        rows = [(55, 100, '# ... this is here....'),
                (258, 100, '---------------------@'),
                (3710, 100, '+    what here?          ~##'),
                ]

        row_count = 0
        for row in rows:
            self.results.append([[str(row[0]), row_count], [str(row[1])], [str(row[2])]])
            row_count += 1

        self.setEmptyDataGrid(row_count)
        # ---self.setDummyDataGrid(row_count)

    # this is a callback from the 'Save' button
    def saveResults(self, *args):
        self._fbrowser = FileBrowser(select_string='Save')
        self._fbrowser.bind(on_success=self.doSaveResults,
                            on_canceled=self.doCancel)

        self._popup = Popup(title='Save results to...', content=self._fbrowser,
                            size_hint=(0.9, 0.9), auto_dismiss=False)

        self._popup.open()

    def doSaveResults(self, instance):
        saveFilepath = instance.filename
        # ... wrtite results to file ...
        print('Saving results to [{0}]'.format(saveFilepath))
        self._popup.dismiss()


class seekerApp(App):

    _filepath = ''
    _target = ''
    _regex = False
    _offset = 0
    _length = 100
    _resultspath = ''

    def setFilepath(self, path):
        self._filepath = path

    def setTarget(self, target):
        self._target = target

    def setRegex(self, regexYN):
        self._regex = True if regexYN in ('Y','y') else False

    def setOffset(self, offset):
        self._offset = offset

    def setLength(self, length):
        self._length = length

    def setResultsPath(self, path):
        self._resultspath = path

    def getFilepath(self):
        return self._filepath

    def getTarget(self):
        return self._target

    def getRegex(self):
        if self._regex:
            return 'Y'
        else:
            return 'N'

    def getOffset(self):
        return self._offset

    def getLength(self):
        return self._length

    def getResultsPath(self):
        return self._resultspath

    def applyConfig(self):
        config = self.config
        self.setFilepath(config.get('target', 'filepath'))
        self.setTarget(config.get('target' , 'target'))
        self.setRegex(config.get('target' , 'regexYN'))
        self.setOffset(config.getint('target' , 'offset'))
        self.setLength(config.getint('target' , 'length'))
        self.setResultsPath(config.get('results', 'filepath'))

    def saveConfig(self):
        config = self.config
        config.set('target','filepath',self.getFilepath())
        config.set('target','target',self.getTarget())
        config.set('target','regexYN',self.getRegex())
        config.set('target','offset',self.getOffset())
        config.set('target','length',self.getLength())
        config.set('results','filepath',self.getResultsPath())
        config.write()

    def get_application_config(self):
        return super(seekerApp, self).get_application_config( '~/.%(appname)s.ini')

    def build_config(self, config):
        # have to set something to trigger creation/loading of .ini file...
        config.setdefaults('target', {'filepath': '.',
                                      'target': '<target>',
                                      'regexYN': 'N',
                                      'offset': '0',
                                      'length': '100'
                                      })
        config.setdefaults('results', {'filepath': '.'})

    def build(self):

        # TODO move to config ASAP
        # --- Window.size = (600,300)
        Window.clearcolor = (0, 0, 0, 1)    # black background

        self.title = 'Seek and ye shall find...'
        self.icon = 'app_icon.png'
#        self.user_data_dir = '~/.%(appname)'

        ui = Interface()
        ui.initialise()

        print('Window size [{0}]'.format(Window.size))

        return ui


if __name__ == '__main__':
    seekerApp().run()

