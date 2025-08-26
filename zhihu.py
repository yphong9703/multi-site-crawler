import time
from selenium import webdriver
import json
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from pywinauto.application import Application

import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pywinauto.application import Application
import win32clipboard as w


# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
#         'cookie:':'_zap=f8f28845-1870-405c-a9d6-90160ebcfbbc; d_c0=ADBTvP49hxePTt15OIEresYhwA_A56eavv0=|1696992939; __snaker__id=HjizDe0voNg4tVdN; YD00517437729195%3AWM_NI=beIffLmdz%2Bd3epqzPHRimTvwzXmN6JFmT0Gl7824zO8hGsM7oFXG7WXh3uZ%2Bn%2F6xMzEhhuZxnmPk0apjn4rO8cpqQcwIAQ%2FmZCjQg0sux0nElKU7lHuLLSi0xYyxzDEUVGI%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eed7ae45f396a8b3fc6af4868aa2c54e979f9e83d563edbfa885f23fa190fb90d92af0fea7c3b92aa2bb8787e548afbcb6cce739a7b0bf9bd34492b7a3b5f57dba88a3afb54286b39cd1c668f5e8fed5f945fcb88994d03dad9a98a8b65d9cb8fd96d921aef1fa99d07287b8a896d974aeb3a08cb36bb4b6a2d5f145fcbdc092d469b5978fb2ae679a9da6b2e63cb1abb8d1ed4fb0959bd8ef44b79484b4ec3cbc87b799f950878b9aa8cc37e2a3; YD00517437729195%3AWM_TID=htSKlSSSor5EFBVBVVeVzrbxN49db99c; q_c1=a380b8f32e14407c98f2562bba58c86b|1700209055000|1700209055000; _xsrf=UU0so3Vk0eKxqx7CZl0p8gQuJlO3jSMF; HMACCOUNT=7FDB3E31E646D28E; __zse_ck=001_sJUk7G7sWK7fCU7emAogWRxw+5V43VlySYqTX5SMZ8rFRojkP4HWgDYD4Idk5d+MdP8Lppe5oMQHL5t3QzIsIHzOaZ6V=uQ0RfNMLQrocXj6if45O8GfiF6efaVzqTyt; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1722936659,1724837952; z_c0=2|1:0|10:1724838152|4:z_c0|80:MS4xVTg5M0VBQUFBQUFtQUFBQVlBSlZUVUEtdkdjeEU5X2dTdmlqb3dSWHVhMlhFMU52VGMwYTJBPT0=|3f7c297548d423cc95d37c9017c018382d28d6c14f56494eefa6d7f6d791c071; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1725244731; BEC=d6322fc1daba6406210e61eaa4ec5a7a'
#         }


app = Application().start(
    r'c:\WINDOWS\System32\cmd.exe /c cd xxxxxxxxxxxx\\Application && start chrome.exe --remote-debugging-port=9222',
    create_new_console=True, wait_for_idle=False)
time.sleep(3)
try:
    window = app.top_window()
    window.wait('ready')
    time.sleep(3)
    window.close()
except Exception as e:
    print("Error occurred while getting top window:", e)
options = Options()
# options.add_argument("")
options.add_experimental_option("debuggerAddress", "127.0.0.1:9999")
driver = webdriver.Chrome(options=options)
driver.get('https://www.zhihu.com/')

list11=['https://www.zhihu.com/question/64123299/answer/2306692503','https://www.zhihu.com/question/37192167/answer/2225938236','https://www.zhihu.com/question/583744950']
data=[]
for i in list11:
    # driver.get(kk)
    # time.sleep(3)
    #
    # list1=[]
    # url_list = driver.find_element(By.CSS_SELECTOR, "div[class='RichText ztext Post-RichText css-1ygg4xu']").find_elements(By.CSS_SELECTOR, "a")
    # for k in url_list:
    #     url=k.get_attribute("href")
    #     print(url)
    #     if url not in list1:
    #         list1.append(url)
    # for i in list1:
    driver.get(i)
    time.sleep(0.7)
    try:
        if "zhuanlan" in i:
            title = driver.find_element(By.CSS_SELECTOR, "h1[class='Post-Title']").text
            text = driver.find_element(By.CSS_SELECTOR, "div[class='RichText ztext Post-RichText css-1ygg4xu']").text
            # 将文本列表转换成字典形式，准备写入JSON
            data_1 = {"url": driver.current_url,
                    "type": "让子弹飞-张麻子",
                    "content": f'{title}\n{text}',
                    }
            data.append(data_1)
            print(data_1)
        if "question" in i:
            title = driver.find_element(By.XPATH, '//*[@id="root"]/div/main/div/div/div[1]/div[2]/div/div[1]/div[1]/h1').text
            # text = driver.find_element(By.CSS_SELECTOR, "div[class='css-376mun']").text
            titles_text=[]
            for p in range(3):
                print(p)
                # 获取当前的滚动位置
                current_position = driver.execute_script("return window.pageYOffset;")
                # 定义上滑的距离
                scroll_amount = -100  # 您可以根据需要调整这个值
                # 计算新的滚动位置
                new_position = max(0, current_position + scroll_amount)
                # 执行上滑操作
                driver.execute_script(f"window.scrollTo(0, {new_position});")
                time.sleep(0.5)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                try:
                    lip=driver.find_elements(By.CSS_SELECTOR, "div[class='List-item']")
                    for kk in lip:
                        kk.find_element(By.CSS_SELECTOR, "button[class='Button ContentItem-rightButton ContentItem-expandButton FEfUrdfMIKpQDJDqkjte Button--plain fEPKGkUK5jyc4fUuT0QP']").click()
                        time.sleep(0.5)
                except Exception as e:
                    pass

                titleee = driver.find_elements(By.CSS_SELECTOR, "div[class='css-376mun']")
                for t in titleee:
                    ans = t.text
                    if ans and ans not in titles_text:
                        titles_text.append(ans)
                        print("ans===========", ans[:10])
            data_1 = {"url": driver.current_url,
                    "type": "让子弹飞-张麻子",
                    "content": f'{title}\n{titles_text}',
                    }
            data.append(data_1)
            print(data_1)
            with open('zhihu.jsonl', 'a', encoding='utf-8') as f:
                for result in data:
                    json.dump(result, f, ensure_ascii=False)
                    f.write('\n')
    except:
        print("==============",i)
