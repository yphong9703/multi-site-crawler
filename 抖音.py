import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pywinauto.application import Application
import win32clipboard as w
from selenium.webdriver.common.by import By
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
from moviepy.editor import VideoFileClip, AudioFileClip

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    "cookie": "ttwid=1%7CEzn32wS9r5_EUzCzGKlyr8VViL8XSZQhQDGCrF5tJTo%7C1715691400%7C6e66c4ad244a0f3b0589599a56a47fb4f5beee5e8b6ac2213bf165a16a8a7d6d; UIFID_TEMP=973a3fd64dcc46a3490fd9b60d4a8e663b34df4ccc4bbcf97643172fb712d8b0c0bf1665e15d59e8a9788c4ecc300c2c535c48146d53273057b5f10ed796cb39375720b06011771b30ac2fc9cd1bc790; s_v_web_id=verify_lzanlu8i_k7iBXX7l_rtyq_4Bwu_BXtS_clSCN7TQ78Mx; xgplayer_user_id=35646065260; fpk1=U2FsdGVkX19orXaByVx9V/TO0e5vJRwhROUVaeCS97KudLhU5jAYptDekL4mEPog7fLgH1+ZleKnRNMK7jG5cw==; fpk2=362d7fe3d8b2581bffa359f0eeda7106; passport_csrf_token=49b9066ba3d8ecb63375da70357686a4; passport_csrf_token_default=49b9066ba3d8ecb63375da70357686a4; bd_ticket_guard_client_web_domain=2; UIFID=973a3fd64dcc46a3490fd9b60d4a8e663b34df4ccc4bbcf97643172fb712d8b0fb04e53efaecac7469ae6b4249247b5330238d939fe24b21eadbb9cc56f2f8b168136c85b29f8ef991d0be9daf7489ce7f8c706c791f98540d0127006b242cba5d252b4049adc401f6252c5636dcd0840953bbf7c6d26b558e8bb67b76ba255a6a2de5d8feb011adb0f1103e2101e3a8d2d2d58fe2580328aace96b2cde5b8d3; SEARCH_RESULT_LIST_TYPE=%22single%22; d_ticket=b458770358808cdf6e50730965af429639dee; passport_assist_user=ClADGhvUiVD7srawftSRTXxPdY0MLYGeuf5C2QnCmHuXePNPRH-Sy4boKM5wMujnqNTrdrpd7R45q1K6BgDPSKjPRhRrEIYdDyLZaEWX3yEvHRpKCjyp4GR19sixq90pHxNgDdw4GDbXCpXgWKEprSVvWDURQTTH-PBdvZdRWUxQrXVd4lzwmIr983mD8d4RiGsQjZfYDRiJr9ZUIAEiAQNfCWr-; n_mh=9-mIeuD4wZnlYrrOvfzG3MuT6aQmCUtmr8FxV8Kl8xY; sso_uid_tt=9cd8b16058abf46c8b9abc7fe8431993; sso_uid_tt_ss=9cd8b16058abf46c8b9abc7fe8431993; toutiao_sso_user=2e7789a07483f87da71618b4e17cf888; toutiao_sso_user_ss=2e7789a07483f87da71618b4e17cf888; sid_ucp_sso_v1=1.0.0-KGViZDQ2NjI1YWFmNzcyMzMwYTg3MGU2YWVkNGZkYzgzYThmMWM2Y2UKIQib8-C-yMypBhDh5au1BhjvMSAMMIr7obIGOAZA9AdIBhoCaGwiIDJlNzc4OWEwNzQ4M2Y4N2RhNzE2MThiNGUxN2NmODg4; ssid_ucp_sso_v1=1.0.0-KGViZDQ2NjI1YWFmNzcyMzMwYTg3MGU2YWVkNGZkYzgzYThmMWM2Y2UKIQib8-C-yMypBhDh5au1BhjvMSAMMIr7obIGOAZA9AdIBhoCaGwiIDJlNzc4OWEwNzQ4M2Y4N2RhNzE2MThiNGUxN2NmODg4; passport_auth_status=5beb4773c140a9e0e650ad2f79863361%2C; passport_auth_status_ss=5beb4773c140a9e0e650ad2f79863361%2C; uid_tt=7c7f94788dfad9c1efd95f847462b54c; uid_tt_ss=7c7f94788dfad9c1efd95f847462b54c; sid_tt=0372684d669a5f18942cc8e42a7d9b23; sessionid=0372684d669a5f18942cc8e42a7d9b23; sessionid_ss=0372684d669a5f18942cc8e42a7d9b23; is_staff_user=false; _bd_ticket_crypt_doamin=2; _bd_ticket_crypt_cookie=965ebc8db818843dd1348d4463ea420c; __security_server_data_status=1; sid_guard=0372684d669a5f18942cc8e42a7d9b23%7C1722479339%7C5183993%7CMon%2C+30-Sep-2024+02%3A28%3A52+GMT; sid_ucp_v1=1.0.0-KDc0MDA3NGY1ODlhNzA5MTNhMjRjZWMzYzc2M2U0Y2FhMzJhZTA0YzkKGwib8-C-yMypBhDr5au1BhjvMSAMOAZA9AdIBBoCaGwiIDAzNzI2ODRkNjY5YTVmMTg5NDJjYzhlNDJhN2Q5YjIz; ssid_ucp_v1=1.0.0-KDc0MDA3NGY1ODlhNzA5MTNhMjRjZWMzYzc2M2U0Y2FhMzJhZTA0YzkKGwib8-C-yMypBhDr5au1BhjvMSAMOAZA9AdIBBoCaGwiIDAzNzI2ODRkNjY5YTVmMTg5NDJjYzhlNDJhN2Q5YjIz; store-region=cn-gd; store-region-src=uid; dy_swidth=2560; dy_sheight=1440; strategyABtestKey=%221723190437.754%22; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.5%7D; download_guide=%223%2F20240809%2F0%22; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; pwa2=%220%7C0%7C3%7C0%22; WallpaperGuide=%7B%22showTime%22%3A1723191517009%2C%22closeTime%22%3A0%2C%22showCount%22%3A1%2C%22cursor1%22%3A12%2C%22cursor2%22%3A0%7D; __ac_nonce=066b5d3ab002933c82296; __ac_signature=_02B4Z6wo00f01pLpzwAAAIDDTpBQtl45lPqSycuAAMIbx7UF5Q4fj4rGnMnWO5.-aj4FTNzlp1yuCtC-eX145AskHMD8-P2PxYxM1DlkUoDPORu-JUCOV4HeHSGAQwFQLD935n7zRUvqeEYw96; csrf_session_id=46ca670094bf54269de9f857028c7234; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAbK2Vj5gCOQxS8PRizagpOI6i_4WuCB5mxewC07FlclR_nfgjRbYj72rUcabMi0T3%2F1723219200000%2F0%2F1723192371035%2F0%22; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A2560%2C%5C%22screen_height%5C%22%3A1440%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A16%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A2.45%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A100%7D%22; publish_badge_show_info=%220%2C0%2C0%2C1723192392075%22; odin_tt=a70336bd0e258570046b25559ed7c07964487135e1d37380377a361fd7e84bd87b153b43ad94e673a398f45d459bc180; IsDouyinActive=true; home_can_add_dy_2_desktop=%221%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCRlNxUjkrWCtQQXNvRTcyNGxwRW53aE0wZ2VYeDI2V1dxY2NGTnAxOVRETFZELzFyY1dKZlJpaTNoMVh4TDZBUU1wTzkzak8xT014RkQzUzE1NHB1eTQ9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; passport_fe_beating_status=true",
    'Origin': 'https://www.douyin.com/',

    }
#
#
# def setText(aString):
#     w.OpenClipboard()
#     w.EmptyClipboard()
#     w.SetClipboardText(aString)
#     w.CloseClipboard()


def run_Chrome():
    app = Application().start(
        r'c:\WINDOWS\System32\cmd.exe /c cd xxxxxxxxxxxxxxx\\Application && start chrome.exe --remote-debugging-port=9999',
        create_new_console=True, wait_for_idle=False)
    time.sleep(3)

    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9999")

    driver = webdriver.Chrome(options=options)

    try:

        # window = app.top_window()

        window_handles = driver.window_handles

        driver.switch_to.window(window_handles[1])
        driver.implicitly_wait(3)
        driver.get("https://www.douyin.com/")
        driver.implicitly_wait(3)
        window.wait('ready')
        time.sleep(3)
        window.close()
    except Exception as e:
        print("Error occurred while getting top window:", e)

    return driver


def get_user_browser():
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9999")
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.douyin.com/')
    time.sleep(15)
    driver.get(url)
    time.sleep(15)
    return driver

def extract_audio(audio_file_path, mp3_path):
    video_clip = None
    audio = None
    try:
        video_clip = VideoFileClip(audio_file_path)
        audio = video_clip.audio
        audio.write_audiofile(mp3_path)
    # except Exception as e:
    #     print(f"An error occurred: {e}")
    finally:
        if video_clip is not None:
            video_clip.close()
        if audio is not None:
            audio.close()


def generate_random_code(length=5):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def run(url):
    driver = run_Chrome()
    driver.get(url)
    # for j in range(100):
    #     driver.execute_script("document.documentElement.scrollTop=100000")
    #     driver.execute_script("document.documentElement.scrollTop=100000")
    #     time.sleep(1)
    # result = []
    #
    # for i in driver.find_element(By.CSS_SELECTOR, "[class='LPv6KBIL']").find_elements(By.TAG_NAME, "li"):
    #
    #     if '//www.douyin.com/video/' in i.find_element(By.TAG_NAME, "a").get_attribute('href') and i.find_element(
    #             By.TAG_NAME, "a").get_attribute('href') not in result:
    #         result.append(i.find_element(By.TAG_NAME, "a").get_attribute('href'))
    # print(len(result))

    # with open(r"D:\2024work\zhou\douyin.txt", 'a+', encoding='utf-8') as f:
    #     for rr in result:
    #         f.write(f'{rr}\n')

    jsonl_file_path = r"D:\2024work\zhou\douyin_gemini_bu.jsonl"


    existing_urls = set()
    with open(jsonl_file_path, 'r', encoding='utf-8') as jsonl_file:
        for line in jsonl_file:
            data = json.loads(line)
            existing_urls.add(data.get('url'))
    with open(r"D:\2024work\zhou\douyin.txt", 'r', encoding='utf-8') as file:

        for line in file:

            url = line.strip()

            if url not in existing_urls:

                driver.get(url)
                print(url)
                time.sleep(3)
                try:
                    for v in driver.find_element(By.XPATH,
                                                 '//*[@id="douyin-right-container"]/div[2]/div/div[1]/div[2]/div/xg-video-container/video').find_elements(
                            By.TAG_NAME, "source"):

                        try:
                            name = driver.find_element(By.XPATH,
                                                       '//*[@id="douyin-right-container"]/div[2]/div/div[1]/div[3]/div/div[1]/div/h1/span/span[2]/span/span[1]/span/span/span').text
                            print(name)
                            time_post=""
                            desc_post=""
                            try:
                                time_post = driver.find_element(By.CSS_SELECTOR, "span[class='D8UdT9V8']").text
                                print(time_post)
                                desc_post = driver.find_element(By.CSS_SELECTOR, "h1[class='hE8dATZQ']").text
                                print(desc_post)
                            except Exception as e:
                                print(e)
                            name_s=f'{name}_{generate_random_code()}'
                            audio_file_path = os.path.join(r"D:\2024work\zhou\douyin\mp4", f"{name_s}.mp4")
                            url111 = v.get_attribute('src')
                            print(url111)
                            r = requests.get(url111, headers=headers)
                            with open(audio_file_path, 'wb') as f:
                                f.write(r.content)
                            mp3_path = os.path.join(r"D:\2024work\zhou\douyin\mp3", f"{name_s}.mp3")
                            try:
                                extract_audio(audio_file_path, mp3_path)
                                data={
                                    'url': url,
                                    'title': name,
                                    'title_tags': desc_post,
                                    'time': time_post,
                                    'audio_path': f"{name_s}.mp3",
                                    'tag': 'gemini人设'
                                }
                                with open(r'D:\2024work\zhou\douyin_gemini_bu_813.jsonl', 'a', encoding='utf-8') as jsonl_file:
                                    jsonl_file.write(json.dumps(data, ensure_ascii=False) + '\n')
                            except:
                                print("pass+++++")
                            break
                        except Exception as e:
                            print(e)
                except Exception as e:
                    print(e)
    driver.close()
    window.close()


if __name__ == "__main__":
    user = "gemini"
    url = "https://www.douyin.com/user/MS4wLjABAAAAoFmglaGcFrTPo9j0VUbhQUp7ePcminnSX1Vcxb08RXY"
    run(url)