
# -*- encoding=utf8 -*-
import time
# -*- encoding=utf8 -*-
import os,pyperclip
from airtest.core.api import auto_setup, device

auto_setup(__file__, devices=[
    "Android:///",
])

__author__ = "xxx"

# from airtest.core.api import *

# auto_setup(__file__)

from poco.drivers.android.uiautomation import AndroidUiautomationPoco

poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)


for s in range(3):
    try:
        poco("com.tencent.mm:id/lyt").click()
    except:
        pass

    try:
        time.sleep(2)
        elements = poco("com.tencent.mm:id/cs")
        time.sleep(2)
        # 循环点击每个元素
        for element in elements:
            try:
                time.sleep(2)
                element.click()
                time.sleep(6)
                # try:
                #     poco(text="微信").click()
                #     time.sleep(2)
                # except:
                #     pass

                poco("com.tencent.mm:id/eo").click()
                time.sleep(2)
                poco("android.widget.FrameLayout").child("android.widget.FrameLayout").offspring("com.tencent.mm:id/ahk").child(
                    "com.tencent.mm:id/iwc")[8].offspring("com.tencent.mm:id/f1j").click()
                time.sleep(2)
                poco("com.tencent.mm:id/g1").click()  # 关闭
                time.sleep(2)
                # try:
                #     poco(text="微信").click()
                #     time.sleep(2)
                # except:
                #     pass
                poco("com.tencent.mm:id/ep").click()
                time.sleep(2)
                poco("com.tencent.mm:id/cd7").click()
                time.sleep(3)

                # os.environ['ANDROID_HOME'] = r'D:\Androidandroid-sdk'
                adb_path = r'D:\app\AirtestIDE-win-1.2.15\AirtestIDE\airtest\core\android\static\adb\windows\adb.exe'
                # 使用 adb 命令模拟粘贴事件
                os.system(f'{adb_path} shell input keyevent KEYCODE_PASTE')

                link = poco("com.tencent.mm:id/cd7").get_text()
                print(link)
                time.sleep(2)
                poco("com.tencent.mm:id/b1").click()
                time.sleep(2)

                with open('url_airtest.txt', 'r', encoding='utf-8') as f:
                    content_exists = link in f.read()

                if not content_exists:
                    with open('url_airtest.txt', 'a', encoding='utf-8') as f:
                        f.write(link + '\n')
                        print("已写入", link)
                else:
                    print("已存在")
            except:
                try:
                    poco(text="微信").click()
                    time.sleep(2)
                except:
                    pass
    except:
            pass
    poco("com.tencent.mm:id/bj2").swipe([-0.2, -0.5])
    time.sleep(2)
