import os
import sys

from PyQt5 import QtCore


TEMP_DIR = '{}/'.format(QtCore.QStandardPaths.writableLocation(
    QtCore.QStandardPaths.TempLocation))

DECKS_DIR = '{}/study_and_repeat/decks/'.format(
    QtCore.QStandardPaths.writableLocation(
        QtCore.QStandardPaths.AppDataLocation))

IMG_DIR = 'img/'

DECK_FILE = 'deck.pickle'

ICONS_DIR = 'src/img/fugue-icons-3.5.6/icons-shadowless/'
LOGO_PATH = 'src/img/favicon.ico'
if hasattr(sys, '_MEIPASS'):
    ICONS_DIR = os.path.join(sys._MEIPASS, ICONS_DIR)
    LOGO_PATH = os.path.join(sys._MEIPASS, LOGO_PATH)
