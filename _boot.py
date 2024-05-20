import gc
import os
from flashbdev import bdev
import ssd1306fontFile

try:
    if bdev:
        os.mount(bdev, "/")
except OSError:
    import inisetup

    vfs = inisetup.setup()

gc.collect()
with open("boot.py", "w") as f:
    f.write(
"""\
from educore import oled
oled.oled.displayclear()
oled.oled.displaytxtauto('LeKit-V3C', 24, 16)
oled.oled.displaytxtauto('2024-3-20', 24, 32)
oled.oled.displayshow()
"""
    )
if 'main.py' not in os.listdir('/'):
    with open("main.py", "w") as f1:
        f1.write('')

if 'leight.vi' not in os.listdir('/'):
    try:
        with open("leight.vi", "w") as f3:
            f3.write("LeKitV3C 2023/11/05 0.1")
    except:
        pass
