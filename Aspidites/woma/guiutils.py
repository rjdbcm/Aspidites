import dearpygui.dearpygui as dpg

import sys
this = sys.modules[__name__]

for i in dir(dpg):
    setattr(this, i, getattr(dpg, i))
