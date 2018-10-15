# Jonathan J
# October 2018

'''
cifero.ciferomain

cifero.ciferomain.main() runs the GUI program
PyQt generated interface files are in cifero.ciferogui
'''


import sys

from PyQt5.QtWidgets import QMainWindow,QDialog,QApplication,QAction,QShortcut
from PyQt5.QtGui import QKeySequence

import cifero.ciferogui.main
import cifero.ciferogui.settings
import cifero.ciferogui.about
import cifero.ciferogui.ciphers

from pathlib import Path
import pyperclip # TextEdit's .copy() doesn't work for some reason

import cifero.translit as tl

class Application(object):
    '''Parent class to store Application data'''
    def __init__(self):
        self._default_syll_sep = "'"
        self._default_sent_sep = " "

        self.syll_sep = "'"
        self.word_sep = " "
        pass

class MainWindow(QMainWindow, Application):
    base_app = Application()

    def __init__(self):
        # defaults
        self.modes = sorted(list(tl.sheets.sheetsdict.keys())+['English'])

        super().__init__()
        self.ui = cifero.ciferogui.main.Ui_CiferoMain()
        self.ui.setupUi(self)
        self.show()

        self.ui.InputModeCombo.addItems(self.modes)
        self.ui.OutputModeCombo.addItems(self.modes)

        # set initial combobox
        i = self.ui.InputModeCombo.findText('Key')
        self.ui.InputModeCombo.setCurrentIndex(i)
        i = self.ui.OutputModeCombo.findText('Cipher')
        self.ui.OutputModeCombo.setCurrentIndex(i)

        self.ui.OutputTextEdit.setReadOnly(True)

        # this works
        self.actionTest = QAction()
        self.actionTest.setText('About')
        self.actionTest.setToolTip('Shift+Ctrl+A')
        self.actionTest.triggered.connect(self.open_about)
        self.ui.menuBar.addAction(self.actionTest)

        # some more shortcuts
        QShortcut(QKeySequence('Shift+Ctrl+A'), self, self.open_about)
        QShortcut(QKeySequence('Ctrl+Q'), self, self.quit)
        QShortcut(QKeySequence('Ctrl+W'), self, self.swap)
        QShortcut(QKeySequence('Ctrl+E'), self, self.clear)
        QShortcut(QKeySequence('Ctrl+R'), self, self.raw_transliterate)
        QShortcut(QKeySequence('Ctrl+T'), self, self.transliterate)
        QShortcut(QKeySequence('Ctrl+D'), self, self.open_settings)
        QShortcut(QKeySequence('Ctrl+F'), self, self.open_ciphers)
        QShortcut(QKeySequence('Shift+Ctrl+S'), self, self.strip)
        QShortcut(QKeySequence('Shift+Ctrl+V'), self, self.paste)
        QShortcut(QKeySequence('Shift+Ctrl+C'), self, self.copy)

        QShortcut(QKeySequence('Ctrl+1'),self, self.cycle_input_mode)
        QShortcut(QKeySequence('Ctrl+2'),self, self.cycle_output_mode)
        QShortcut(QKeySequence('Ctrl+Space'),self,self.ui.InputTextEdit.setFocus)

        # hover tooltips
        self.ui.InputModeCombo.setToolTip(
            'Input mode (Ctrl+1)')
        self.ui.OutputModeCombo.setToolTip(
            'Output mode (Ctrl+2)')
        self.ui.InputTextEdit.setToolTip(
            'Input text (Ctrl+Space)')
        self.ui.TransliterateButton.setToolTip(
            'Transliterates, applying syllable and word separators (Ctrl+T)')
        self.ui.SwapButton.setToolTip(
            'Swaps input and output text, as well as their modes (Ctrl+W)')
        self.ui.RawTransliterateButton.setToolTip(
            'Transliterates, using spaces to separate words and ignoring syllable separators (Ctrl+R)')
        self.ui.StripButton.setToolTip(
            '''Strips punctuation, removing :;,.!?[](){}"'<> and *+-/~_, ignoring &#$%@=` (Shift+Ctrl+S)''')
        self.ui.PasteButton.setToolTip(
            'Pastes the text from the system clipboard to the input (Shift+Ctrl+V)')
        self.ui.CopyButton.setToolTip(
            'Copies the text in the output to the system clipboard (Shift+Ctrl+C)')
        self.ui.ClearButton.setToolTip(
            'Clears both input and output textboxes (Ctrl+E)')
        self.ui.SettingsButton.setToolTip(
            'Opens the settings dialog (Ctrl+D)')
        self.ui.CiphersButton.setToolTip(
            'Opens the documentation for the default cipher sheets (Ctrl+F)')
        self.ui.QuitButton.setToolTip(
            'Closes the program (Ctrl+Q)')
    

        # connect buttons to functions
        self.ui.TransliterateButton.clicked.connect(self.transliterate)
        self.ui.SwapButton.clicked.connect(self.swap)
        self.ui.RawTransliterateButton.clicked.connect(self.raw_transliterate)
        self.ui.StripButton.clicked.connect(self.strip)
        self.ui.PasteButton.clicked.connect(self.paste)
        self.ui.CopyButton.clicked.connect(self.copy)
        self.ui.ClearButton.clicked.connect(self.clear)

        self.ui.SettingsButton.clicked.connect(self.open_settings)
        self.ui.CiphersButton.clicked.connect(self.open_ciphers)
        self.ui.QuitButton.clicked.connect(self.quit)

    def cycle_input_mode(self):
        i = self.ui.InputModeCombo.currentIndex()
        self.ui.InputModeCombo.setCurrentIndex(i+1)

    def cycle_output_mode(self):
        i = self.ui.OutputModeCombo.currentIndex()
        self.ui.OutputModeCombo.setCurrentIndex(i+1)

    def transliterate(self):
        input_text = self.ui.InputTextEdit.toPlainText()
        input_mode = self.ui.InputModeCombo.currentText()
        output_mode = self.ui.OutputModeCombo.currentText()

        try:
            output_text = tl.transliterate(input_text,
                                        input_mode,
                                        output_mode, 
                                        syll_sep=self.base_app.syll_sep,
                                        word_sep=self.base_app.word_sep)
        except TypeError:
            output_text = 'Something went wrong.'
            self.ui.statusBar.showMessage('ERROR: Bad input.')
        except tl.cmudict.WordNotFound:
            output_text = 'English word not found in dictionary.'
            self.ui.statusBar.showMessage('ERROR: Word not found in dictionary.')
        else:
            # this is run only if the excepts didn't catch anything
            self.ui.statusBar.showMessage('Transliterated from {} to {}.'.format(
                input_mode, output_mode))
        # should finally: be used here?

        self.ui.OutputTextEdit.setText(output_text)

    def swap(self):
        '''Swaps contents of input and output TextEdit's as well as their modes'''
        output_text = self.ui.OutputTextEdit.toPlainText()
        input_text = self.ui.InputTextEdit.toPlainText()

        self.ui.OutputTextEdit.clear()
        self.ui.OutputTextEdit.setPlainText(input_text)
        self.ui.InputTextEdit.clear()
        self.ui.InputTextEdit.setPlainText(output_text)

        output_mode = self.ui.OutputModeCombo.currentIndex()
        input_mode = self.ui.InputModeCombo.currentIndex()
        self.ui.OutputModeCombo.setCurrentIndex(input_mode)
        self.ui.InputModeCombo.setCurrentIndex(output_mode)

    def raw_transliterate(self):
        '''calls transliterate, then remove syllable separators, BUT NOT
        SENTENCE SEPARATORS, they are changed to spaces'''
        input_text = self.ui.InputTextEdit.toPlainText()
        input_mode = self.ui.InputModeCombo.currentText()
        output_mode = self.ui.OutputModeCombo.currentText()

        try:
            output_text = tl.raw_transliterate(input_text,
                                        input_mode,
                                        output_mode, 
                                        syll_sep=self.base_app.syll_sep,
                                        word_sep=self.base_app.word_sep)
        except TypeError:
            output_text = 'Something went wrong.'
            self.ui.statusBar.showMessage('ERROR: Bad input.')
        except tl.cmudict.WordNotFound:
            output_text = 'English word not found in dictionary.'
            self.ui.statusBar.showMessage('ERROR: Word not found in dictionary.')
        else:
            # this is run only if the excepts didn't catch anything
            self.ui.statusBar.showMessage('Raw Transliterated from {} to {}.'.format(
                input_mode, output_mode))
        # should finally: be used here?

        self.ui.OutputTextEdit.setPlainText(output_text)
        self.ui.statusBar.showMessage('Raw transliterated from {} to {}.'.format(
            input_mode, output_mode))

    def strip(self):
        '''Simply removes marks and symbols from input and puts them in output'''
        input_text = self.ui.InputTextEdit.toPlainText()
        self.ui.OutputTextEdit.setPlainText(tl.strip_marks_and_symbols(input_text))
        self.ui.statusBar.showMessage('''Stripped :;,.!?[](){}"'<> from input.''')

    def paste(self):
        '''Pastes contents of system clipboard to input TextEdit'''
        self.ui.InputTextEdit.setPlainText(pyperclip.paste())
        self.ui.statusBar.showMessage('Pasted from clipboard to input.')

    def copy(self):
        '''Copy contents of output TextEdit to system clipboard'''
        output_text = self.ui.OutputTextEdit.toPlainText()
        pyperclip.copy(output_text)
        self.ui.statusBar.showMessage('Copied from input to clipboard.')

    def clear(self):
        self.ui.OutputTextEdit.clear()
        self.ui.InputTextEdit.clear()
        self.ui.statusBar.showMessage('Cleared both input and output.')

    def open_about(self):
        self.AboutUi = AboutDialog()

    def open_ciphers(self):
        # Ciphers Dialog is read-only for now, no need to inherit data
        self.CiphersUi = CiphersDialog()

    def open_settings(self):
        self.SettingsUi = SettingsDialog(self.base_app)

    def quit(self):
        sys.exit()

class SettingsDialog(QDialog):
    def __init__(self, base_app):
        super().__init__()
        self.ui = cifero.ciferogui.settings.Ui_SettingsDialog()
        self.ui.setupUi(self)
        self.show()

        self.base_app = base_app

        # initial values remembered in case changes are cancelled
        self.init_sentSep = base_app.word_sep
        self.init_syllSep = base_app.syll_sep

        self.ui.SentSepLineEdit.setText(base_app.word_sep)
        self.ui.SyllSepLineEdit.setText(base_app.syll_sep)

        self.ui.ResetButton.clicked.connect(self.reset_to_defaults)
        self.ui.buttonBox.accepted.connect(self.update_settings)
        self.ui.buttonBox.rejected.connect(self.close_without_update)
    
    def reset_to_defaults(self):
        # update base_app data
        self.base_app.syll_sep = self.base_app._default_syll_sep
        self.base_app.word_sep = self.base_app._default_sent_sep
        # update view
        self.ui.SentSepLineEdit.setText(self.base_app.word_sep)
        self.ui.SyllSepLineEdit.setText(self.base_app.syll_sep)

    def update_settings(self):
        self.base_app.syll_sep = self.ui.SyllSepLineEdit.text()
        self.base_app.word_sep = self.ui.SentSepLineEdit.text()

    def close_without_update(self):
        self.base_app.syll_sep = self.init_syllSep
        self.base_app.word_sep = self.init_sentSep
        self.done(0)

class CiphersDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = cifero.ciferogui.ciphers.Ui_CiphersDialog()
        self.ui.setupUi(self)
        self.show()

class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = cifero.ciferogui.about.Ui_AboutDialog()
        self.ui.setupUi(self)
        self.show()

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())   

if __name__ == "__main__":
    main()  