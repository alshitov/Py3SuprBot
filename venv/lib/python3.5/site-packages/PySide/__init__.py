from __future__ import absolute_import
from __future__ import print_function

import qt_backport as _qt_backport

if _qt_backport.CURRENT_EMULATOR is not None:
    raise ImportError("qt_backport emulator already running: '%s'" % \
                      _qt_backport.CURRENT_EMULATOR)

emulator = __name__
wrapper = _qt_backport.PYQT5
_qt_backport.emulate(emulator, wrapper)

del emulator, wrapper
