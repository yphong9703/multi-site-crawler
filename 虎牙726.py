

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
