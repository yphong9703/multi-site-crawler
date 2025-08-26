import os
import re
import time
from playwright.sync_api import sync_playwright

def get_last_reply(page):
    time.sleep(1)
    return page.get_by_test_id("message_text_content").all_text_contents()

def wait_for_reply(page, msg):
    time.sleep(10)
    c = 0
    while True:
        c+=1
        reply = get_last_reply(page)
        button_locator=page.get_by_test_id("message_action_regenerate")
        time.sleep(1)
        if button_locator.is_visible() and msg!=reply[-1].strip():
            time.sleep(1)
            return reply[-1].strip()
        if c>50:
            return ""
def doubao_chat(page, msg,numbers):
    if numbers==1:
        clear_chat(page)
    assert msg != ""
    page.get_by_test_id("chat_input_input").fill(msg)
    page.get_by_test_id("chat_input_send_button").click()
    answer = wait_for_reply(page, msg)
    return answer
def clear_chat(page):
    time.sleep(1)
    page.get_by_test_id("bot_setting_button").click()
    time.sleep(1)
    page.get_by_test_id("clear_context_setting").get_by_text("清除上下文").click()
    time.sleep(1)
    page.get_by_test_id("bot_setting_close").click()
    time.sleep(1)
def run_one(input_msg,numbers,page):
    c=0
    while True:
        try:
            answer = doubao_chat(page, input_msg,numbers)
            answer = answer.replace('\n', '')
            print(answer)
            return answer
        except Exception as e:
            print("run_one error:",e,input_msg,numbers,page)
            c+=1
            if c>50:
                return "Error"

def call_doubao_result(input_msg, numbers,page):
    msg_doubao=run_one(input_msg,numbers,page)
    return msg_doubao
