

import os
import json
import requests
import threading
import re
import string
import random
import time
from urllib.parse import unquote
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

# 初始化锁
lock = threading.Lock()
jsonl_lock = threading.Lock()


def load_processed_urls(output_jsonl_path):
    """
    加载已处理的 URL 列表
    """
    processed_urls = set()
    if os.path.exists(output_jsonl_path):
        with open(output_jsonl_path, 'r', encoding='utf-8') as jsonl_file:
            for line in jsonl_file:
                data = json.loads(line.strip())
                processed_urls.add(data['source'])
    return processed_urls


def extract_info_from_html(html, url):
    """
    从 HTML 中提取所需信息
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')

        # 提取video-title
        title = soup.find('h1', class_='video-title').get_text(strip=True)
        print("title",title)
        # 提取detail-desc
        desc = soup.find('p', class_='detail-desc').get_text(strip=True)
        print("desc",desc)
        # 提取detail-date
        time_content = soup.find('span', class_='detail-date').get_text(strip=True)
        print("time_content",time_content)#'text': "",
        return {
            'title': title,
            'title_tags': desc,

            'time': time_content,
            'source': url,
            'tag': 'gemini人设'
        }
    except Exception as e:
        print(f'Error extracting info from {url}: {e}')
        return None


def generate_random_code(length=5):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


# 定义重试装饰器
def retry(max_retries=5, delay=12):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries <= max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Error occurred: {e}. Retrying...")
                    retries += 1
                    if retries > max_retries:
                        print(f"Max retries ({max_retries}) exceeded. Skipping this URL.")
                        raise
                    time.sleep(delay)

        return wrapper

    return decorator



def extract_video_id(url):
    # 找到最后一个"/"的位置
    last_slash_index = url.rfind('/')

    # 找到最后一个"."的位置
    last_dot_index = url.rfind('.')

    # 提取两个位置之间的内容
    content = url[last_slash_index + 1:last_dot_index]

    return content

def extract_audio(audio_file_path, mp3_path):
    """从视频文件中提取音频并保存为MP3文件"""
    try:
        video_clip = VideoFileClip(audio_file_path)
        audio = video_clip.audio
        audio.write_audiofile(mp3_path)
    finally:
        # 确保资源被释放
        if video_clip is not None:
            video_clip.close()
        if audio is not None:
            audio.close()

@retry(max_retries=5, delay=2)
def process_url(url, headers, processed_urls, output_jsonl_path, audio_output_path):
    """
    处理单个 URL
    """
    if url in processed_urls:
        print(f"URL 已处理: {url}")
        return

    try:
        # 获取页面内容
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"无法访问 URL: {url}, 状态码: {response.status_code}")
            return

        # 提取信息
        data = extract_info_from_html(response.text, url)
        if not data:
            return

        video_id = extract_video_id(url)
        print(video_id)
        link = f'https://liveapi.huya.com/moment/getMomentContent?videoId={video_id}&uid=&_=1665144759951'
        response_1 = requests.get(url=link, headers=headers)
        title = response_1.json()['data']['moment']['title']
        video_url = response_1.json()['data']['moment']['videoInfo']['definitions'][0]['url']
        video_content = requests.get(url=video_url).content

        name_s=f'{title}_{generate_random_code()}'
        # 保存音频
        audio_file_path = os.path.join(audio_output_path, f"{name_s}.mp4")
        with open(audio_file_path, mode='wb') as f:
            f.write(video_content)
        mp3_path = os.path.join(audio_output_path, f"{name_s}.mp3")
        extract_audio(audio_file_path, mp3_path)

        data['audio_path'] = mp3_path

        with jsonl_lock:
            with open(output_jsonl_path, 'a+', encoding='utf-8') as jsonl_file:
                jsonl_file.write(json.dumps(data, ensure_ascii=False) + '\n')

        print(f"已处理: {url}")

    except Exception as e:
        print(f"处理 {url} 时发生错误: {e}")


def main(input_txt_path, output_jsonl_path, audio_output_path):
    with open(input_txt_path, 'r', encoding='utf-8') as file:
        urls = [line.strip() for line in file if line.strip()]

    processed_urls = load_processed_urls(output_jsonl_path)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': f'https://www.huya.com/',
        'Origin': 'https://www.huya.com/',
        'Connection': 'keep-alive',
        'Cookie': "buvid3=14086547-7351-0E5D-5794-95FF6249BA5136607infoc; b_nut=1702370836; _uuid=3AE381DD-4E46-929C-9934-106D674D4B7DB37251infoc; rpdid=|(k||Yuklk~|0J'u~|kJ~|)J); enable_web_push=DISABLE; header_theme_version=CLOSE; DedeUserID=431609313; DedeUserID__ckMd5=3f2960dd97e3ea09; buvid4=14771EC0-0BC2-BC98-9F5B-0060CA37FB2852373-023100816-k%2FJvGgN8nEjw%2B9TNNErXWQ%3D%3D; FEED_LIVE_VERSION=V8; PVID=4; CURRENT_BLACKGAP=0; CURRENT_FNVAL=4048; CURRENT_QUALITY=80; buvid_fp_plain=undefined; fingerprint=d07d1b47c482f100fe8f1bdd32a86780; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjI0OTI5NDMsImlhdCI6MTcyMjIzMzY4MywicGx0IjotMX0.rcUyT0hxo5CejmjLDKh3tS3OPQwXLdin4A6-GAS7z1E; bili_ticket_expires=1722492883; SESSDATA=809c41d8%2C1737789131%2C135b7%2A71CjA15cwmw2yYaTM3g2ku9G4f4faO0snK18gmtYWf5UeNemIxFknavqsLyCprGZoKa4wSVnEzWU40N0xhbTJ1b2UxRDhZZjRRaGE2cEZ2Tnd0OWQ2MjdNWTFXRkZBalBSc3lpcV9xRThIZGdrRzNlek1SUC13MXNZZnlsMl9Gd25LVi1NQ0xaRUlRIIEC; bili_jct=780e3c0c492954c8934bb5a60ec430bd; sid=6l1kl5ix; bp_t_offset_431609313=959829971231047680; buvid_fp=d07d1b47c482f100fe8f1bdd32a86780; home_feed_column=4; browser_resolution=1357-946; b_lsid=1DB55B7D_19106A000C0",
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
    }
    with ThreadPoolExecutor(max_workers=30) as executor:
        for url in urls:
            executor.submit(process_url, url, headers, processed_urls, output_jsonl_path, audio_output_path)


if __name__ == '__main__':
    input_txt_path = r'D:\2024work\zhou\huya_gemini.txt'
    output_jsonl_path = r'D:\2024work\zhou\huya_gemini.jsonl'
    audio_output_path = r'D:\2024work\zhou\huya_gemini'

    main(input_txt_path, output_jsonl_path, audio_output_path)


# from moviepy.editor import VideoFileClip
# import requests
# import re
#
# # headers = {
# #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
# #     'Accept': 'application/json, text/plain, */*',
# #     'Accept-Language': 'en-US,en;q=0.5',
# #     'Referer': f'https://www.huya.com/',
# #     'Origin': 'https://www.huya.com/',
# #     'Connection': 'keep-alive',
# #     'Cookie': "__yamid_new=CAA9A725D73000014EA9A8B11A7013D2; __yamid_tt1=0.4780408106702305; udb_guiddata=6059598ea1cf4fe99a865ff8ea2f35ac; udb_deviceid=w_819968737599504384; sdidshorttest=test; SoundValue=0.50; alphaValue=0.80; game_did=VK8uSxdVtxZje1DTOf4-ZL4ScAsWBsG8o9c; guid=0a7d1d594110f0654301e614e714f07b; hiido_ui=0.5233017171819556; isInLiveRoom=true; sdid=0UnHUgv0_qmfD4KAKlwzhqTo0L7QAO0c26JlRkUhZB_p13BvtnOJCLC5hveIcIeXxVXha6F9ocNekCYn6p1gumqDh4wT1gD8SOv0gMMouh_jWVkn9LtfFJw_Qo4kgKr8OZHDqNnuwg612sGyflFn1dqtd9okZStSM9FxmdvUTd8ehOpTagv9yEgqHf10MiuNf; sdidtest=0UnHUgv0_qmfD4KAKlwzhqTo0L7QAO0c26JlRkUhZB_p13BvtnOJCLC5hveIcIeXxVXha6F9ocNekCYn6p1gumqDh4wT1gD8SOv0gMMouh_jWVkn9LtfFJw_Qo4kgKr8OZHDqNnuwg612sGyflFn1dqtd9okZStSM9FxmdvUTd8ehOpTagv9yEgqHf10MiuNf; Hm_lvt_51700b6c722f5bb4cf39906a596ea41f=1721811703,1721893492,1721990536,1722414086; HMACCOUNT=EAD429051243B61E; __yasmid=0.4780408106702305; _yasids=__rootsid%3DCAD709418E9000016BEA347019DCE900; udb_passdata=3; Hm_lpvt_51700b6c722f5bb4cf39906a596ea41f=1722414092; rep_cnt=7",
# #     'Sec-Fetch-Dest': 'empty',
# #     'Sec-Fetch-Mode': 'cors',
# #     'Sec-Fetch-Site': 'same-site',
# # }
#
# # url = 'https://www.huya.com/video/play/991815098.html'
# #
# # response = requests.get(url=url, headers=headers)
# #
# # video_id='991815098'
# # link = f'https://liveapi.huya.com/moment/getMomentContent?videoId={video_id}&uid=&_=1665144759951'
# #
# # response_1 = requests.get(url=link, headers=headers)
# # print(response_1.json())
# # title = response_1.json()['data']['moment']['title']
# # print(response_1.json())
# # video_url = response_1.json()['data']['moment']['videoInfo']['definitions'][0]['url']
# # print(video_url)
# # video_content = requests.get(url=video_url).content
# # print(video_content)
# # with open(title + '.mp4', mode='wb') as f:
# #
# #     f.write(video_content)
# # print(title, video_url)
# #
# #
# #
# # def extract_audio(video_path, mp3_path):
# #     video_clip = VideoFileClip(video_path)
# #     audio = video_clip.audio
# #     audio.write_audiofile(mp3_path)
# #
# #
# # video_path = 'D:\\2024work\\zhou\\#我一定红透半边天的#gemini郭家毅 因为热爱所以坚持！.mp4'  # 输入的MP4文件路径
# # mp3_path = 'D:\\2024work\\zhou\\output.mp3'  # 输出的MP3文件路径
# # extract_audio(video_path, mp3_path)
#
#
#
#
#
# import pandas as pd
# import cv2,time
# import numpy as np
# from selenium import webdriver
# from selenium.webdriver import ActionChains
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys
# from pywinauto.application import Application
# import win32clipboard as w
# import time
# import json,os
# import pyautogui,time
# import pyautogui
# from pynput.mouse import Listener
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.select import Select
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import pyautogui,time
# import pyautogui
# from pynput.mouse import Listener
#
# updated_data = []
# class LinkProcessor:
#     driver = None
#
#
#     @classmethod
#     def initialize_driver(cls):
#         # 启动Chrome浏览器
#         app = Application().start(
#             r'c:\WINDOWS\System32\cmd.exe /c cd C:\\Users\\tobyfyang\\AppData\\Local\\Google\\Chrome\\Application && start chrome.exe --remote-debugging-port=9999',
#             create_new_console=True, wait_for_idle=False)
#         time.sleep(3)  # 等待Chrome启动
#         try:
#             # 尝试获取顶层窗口
#             window = app.top_window()
#             window.wait('ready')
#             time.sleep(3)  # 等待窗口就绪
#             window.close()
#         except Exception as e:
#             print("Error occurred while getting top window:", e)
#
#         # 设置Chrome WebDriver选项
#         options = Options()
#         options.add_experimental_option("debuggerAddress", "127.0.0.1:9999")
#
#         # 初始化WebDriver
#         cls.driver = webdriver.Chrome(options=options)
#         cls.driver.get('https://yuba.douyu.com/discussion/22169/video')
#         cls.driver.implicitly_wait(3)
#         time.sleep(3)
#
#         return cls.driver
#
#     @classmethod
#     def get_chrome_options(cls):
#         options = Options()
#         options.add_experimental_option("debuggerAddress", "127.0.0.1:9999")
#         return options
#
#
#     @classmethod
#     def process_linkedin_url(cls):
#         list1=[]
#         cls.driver.get(f"https://yuba.douyu.com/discussion/22169/video")
#         for i in range(1,1000000):
#             print(i)
#             for i in range(3000):
#                 # 模拟滚动浏览器窗口
#                 cls.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#                 # 模拟滚动浏览器窗口
#                 cls.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#                 # 模拟滚动浏览器窗口
#                 cls.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#
#             try:
#
#                 time.sleep(2)
#
#                 text_area = WebDriverWait(cls.driver, 3).until(
#                     EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='list__mlUlq']"))
#                 )
#                 shipin2=text_area.find_elements(By.TAG_NAME, "a")
#                 for k in shipin2:
#                     shipin_url = k.get_attribute('href')
#                     print(shipin_url)
#                     time_str = k.find_element(By.CSS_SELECTOR, "div[class='duration__yoE87']").text
#                     print(time_str)
#                     try:
#                         hours, minutes, seconds = map(int, time_str.split(':'))
#
#                         # 计算总秒数
#                         total_seconds = hours * 3600 + minutes * 60 + seconds
#
#                         # 输出总秒数
#                         print("Total seconds:", total_seconds)
#                     except:
#                         minutes, seconds = map(int, time_str.split(':'))
#                         total_seconds = minutes * 60 + seconds
#                         print("Total seconds2:", total_seconds)
#                     if total_seconds > 1800:
#                         print("时间：",total_seconds)
#                     # 输出总秒数
#                     print("Total seconds:", total_seconds)
#                     if shipin_url not in list1:
#                         list1.append(shipin_url)
#                         with open(r"D:\2024work\zhou\\douyu.txt", 'a+', encoding='utf-8') as f:
#                             f.write(f'{shipin_url}\n')
#
#
#                 i+=1
#
#             except Exception as e:
#                 print(e)
#                 cls.driver.get(url)
#                 time.sleep(2)
#         #
#         # with open(r'D:\2024work\zhou\huya_gemini.txt', 'r', encoding='utf-8') as file:
#         #     # 逐行读取文件内容
#         #     for line in file:
#         #         # 去除每行末尾的换行符（如果有的话）
#         #         url = line.strip()
#         #         # 输出URL
#         #         print(url)
#         #         try:
#         #             cls.driver.get(url)
#         #             # time_str = WebDriverWait(cls.driver, 1).until(
#         #             #     EC.visibility_of_element_located((By.CSS_SELECTOR, "span[class='bpx-player-ctrl-time-duration']"))).text
#         #             # print(time_str)
#         #             #
#         #             # minutes, seconds = map(int, time_str.split(':'))
#         #             # total_seconds = minutes * 60 + seconds
#         #
#         #             # # 检查时间是否大于10分钟（600秒）
#         #             # if total_seconds > 1800:
#         #             #     print("时间：",total_seconds)
#         #             #     time.sleep(1)
#         #             title_bi=WebDriverWait(cls.driver, 1).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="viewbox_report"]/div[1]/div/h1'))).text
#         #             print(title_bi)
#         #             time_bi = WebDriverWait(cls.driver, 1).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='pubdate-ip-text']"))).text
#         #             print(time_bi)
#         #             try:
#         #                 desc_bi = WebDriverWait(cls.driver, 1).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='basic-desc-info']"))).text
#         #                 print(desc_bi)
#         #             except Exception as e:
#         #                 # print(e)
#         #                 desc_bi=""
#         #
#         #
#         #             # 构建JSONL格式的数据
#         #             data = {
#         #                 'title': title_bi,
#         #                 'title_tags': desc_bi,
#         #                 'text': "",
#         #                 'time': time_bi,
#         #                 'source': url,
#         #                 'tag': 'gemini人设'
#         #             }
#         #
#                     # # 写入JSONL文件
#                     # with open(r'D:\2024work\zhou\huya_gemini.jsonl', 'a', encoding='utf-8') as jsonl_file:
#                     #     jsonl_file.write(json.dumps(data, ensure_ascii=False) + '\n')
#         #
#         #         except Exception as e:
#         #             print(e)
#
#
# def setText(aString):
#     w.OpenClipboard()
#     w.EmptyClipboard()
#     w.SetClipboardText(aString)
#     w.CloseClipboard()
#
# def main():
#
#     LinkProcessor.initialize_driver()
#     LinkProcessor.process_linkedin_url()
#
#
# if __name__ == "__main__":
#     main()