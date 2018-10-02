from __future__ import absolute_import
from __future__ import print_function

import sys
import os

_this_dir = os.path.abspath(os.path.dirname(__file__))
_ver_path = os.path.join(_this_dir, "VERSION")
__version__ = open(_ver_path, "r").read().strip()
del _this_dir, _ver_path

PYQT4 = "PyQt4"
PYQT5 = "PyQt5"
PYSIDE = "PySide"

EMULATORS = (PYQT4, PYSIDE)
QT_WRAPPERS = (PYQT5, ) #Currently the only Qt5 wrapper available!

#Values below are changed on import of either PyQt4 or PySide
CURRENT_EMULATOR = None #not imported yet
CURRENT_WRAPPER = None
CURRENT_WRAPPER_VERSION_TUPLE = None
CURRENT_WRAPPER_VERSION_STR = None
CURRENT_QT_VERSION_TUPLE = None
CURRENT_QT_VERSION_STR = None

def _create_base_qt4_emulator_with_pyqt5(emulator_module):
    try:
        import PyQt5
    except ImportError:
        install_url = \
            "http://pyqt.sourceforge.net/Docs/PyQt5/installation.html"
        raise ImportError(("qt_backport requires PyQt5 in order to function. "
                           "To install it, please see: %s" % install_url))
    from PyQt5 import QtCore as _Qt5Core
    from . import qt5_backport as _qt5_backport
    _qt5_backport.load_modules(emulator_module)
    _qt5_backport.reassemble_QtGui(emulator_module)
    _qt5_backport.patch_api(emulator_module)
    
    #Values below depend on the Qt wrapper and Qt lib in use..
    global CURRENT_WRAPPER
    global CURRENT_WRAPPER_VERSION_TUPLE
    global CURRENT_WRAPPER_VERSION_STR
    CURRENT_WRAPPER = PYQT5
    CURRENT_WRAPPER_VERSION_TUPLE = tuple(_Qt5Core.PYQT_VERSION_STR.split("."))
    CURRENT_WRAPPER_VERSION_STR = \
        "%s v%s" % (CURRENT_WRAPPER, ".".join(CURRENT_WRAPPER_VERSION_TUPLE))
    
def _emulate_pyside_with_pyqt5(emulator_module):
    _create_base_qt4_emulator_with_pyqt5(emulator_module)
    from PySide import QtCore
    QtCore.Signal = QtCore.pyqtSignal
    QtCore.Slot = QtCore.pyqtSlot
    QtCore.__version__ = QtCore.QT_VERSION_STR

def _emulate_pyqt4_with_pyqt5(emulator_module):
    _create_base_qt4_emulator_with_pyqt5(emulator_module)

emulation_dispatcher = {
    #emulator, wrapper
    (PYQT4   , PYQT5): _emulate_pyqt4_with_pyqt5,
    (PYSIDE  , PYQT5): _emulate_pyside_with_pyqt5,
}

def emulate(emulator, wrapper):
    if emulator not in EMULATORS:
        raise ValueError(("emulator not one of supported "
                          "EMULATORS: '%s'") % emulator)
    if wrapper not in QT_WRAPPERS:
        raise ValueError(("wrapper not one of supported "
                          "QT_WRAPPERS: '%s'") % wrapper)
    
    emulator_module = sys.modules[emulator] #should be in there already
    emulation_dispatcher[(emulator, wrapper)](emulator_module)
    
    #Set the qt_backport constants that depended on us importing...
    from PyQt5 import QtCore as _Qt5Core
    global CURRENT_EMULATOR
    global CURRENT_QT_VERSION_TUPLE
    global CURRENT_QT_VERSION_STR
    CURRENT_EMULATOR = emulator
    CURRENT_QT_VERSION_TUPLE = tuple(_Qt5Core.QT_VERSION_STR.split("."))
    CURRENT_QT_VERSION_STR = ".".join(CURRENT_QT_VERSION_TUPLE)
