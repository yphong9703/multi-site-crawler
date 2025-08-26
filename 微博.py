import re,time,json,random
from playwright.sync_api import Playwright, sync_playwright, expect
from bs4 import BeautifulSoup
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="weibo.json")
    text_gengs = []


    with open(r'D:\2024work\weibo_text1.jsonl', 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)
            text = data.get('text', '')
            word = data.get('word', '')
            if not text:
                text_gengs.append(word)

    for kk in text_gengs:
        list222 = []
        try:
            print(kk)
            if 'BGM君' in kk or 'xx等你，不见不散' in kk :
                continue
            if 'xx' in kk:
                if 'xx' in kk[-2:] or 'xx' in kk[:2]:
                    print(kk)
                else:
                    continue
            kk11=kk.replace('"','').replace('xx','')
            print(kk11)

            page = context.new_page()
            time.sleep(2)
            for j in range(1,51):
                try:
                    url_page=f"https://s.weibo.com/weibo?q={kk11}&nodup=1&page={j}"
                    page.goto(url_page)
                    if j > 5 and list222 is None:
                        break
                    time.sleep(2)
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
                    sleep_time1 = random.uniform(1, 3)
                    time.sleep(sleep_time1)
                    html_content=page.content()

                    soup = BeautifulSoup(html_content, 'html.parser')
                  
                    p_tags = soup.find_all('p')
                  
                    for p_tag in p_tags:
                        title_text=p_tag.get_text()
                        if kk11 in title_text:
                            list222.append(title_text)
                    print(list222)

                    time.sleep(2)
                except Exception as e:
                    url222="https://blog.csdn.net/jia666666/article/details/109199875"
                    page.goto(url222)
                    time.sleep(2)
                    print("---------error",kk,j,e)

                    time.sleep(35)
                    if j > 5:
                        break
            print("+++++++",list222)
            list111 = list(set(list222))
            if list111:
                data22 = {
                    "word": kk,
                    "tag": "weibo",
                    "text": list111
                }
                print(len(list111), data22)
                with open(r'D:\2024work\weibo_text1_2.jsonl', 'a+', encoding='utf-8') as jsonl_file:
                    jsonl_file.write(json.dumps(data22, ensure_ascii=False) + '\n')
            else:
                with open(r'D:\2024work\empty_text.txt', 'w', encoding='utf-8') as txt_file:
                    txt_file.write(kk + '\n')
            page.close()
        except Exception as e:
            time.sleep(30)
            print("error keyword:",kk,e)
            print("#######", list222)
            if list222:
                list111 = list(set(list222))
                if list111:
                    data22 = {
                        "word": kk,
                        "tag": "weibo",
                        "text": list111
                    }
                    print(len(list111), data22)
                    with open(r'D:\2024work\weibo_text1_2.jsonl', 'a+', encoding='utf-8') as jsonl_file:
                        jsonl_file.write(json.dumps(data22, ensure_ascii=False) + '\n')
                else:
                    with open(r'D:\2024work\empty_text.txt', 'w', encoding='utf-8') as txt_file:
                        txt_file.write(kk + '\n')


    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
