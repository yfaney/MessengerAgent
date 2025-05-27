import sys
import os

import pyperclip
import pyautogui

import time

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from common.crawling import crawl_chat_from_kakao
from common.util.text_util import truncate_text
from common.util.debug_util import is_debug_mode


COORD_CRAWL_X = 350 # 카카오톡 대화창 좌표 (수동 측정 필요)
COORD_CRAWL_Y = 300 # 카카오톡 대화창 좌표 (수동 측정 필요)
COORD_SEND_X = 300 # 카카오톡 입력창 좌표 (수동 측정 필요)
COORD_SEND_Y = 420 # 카카오톡 입력창 좌표 (수동 측정 필요)


def send_to_kakao(message):
    pyperclip.copy(message)  # 메시지를 클립보드에 복사
    time.sleep(1)  # 클립보드 복사 대기
    pyautogui.click(x=COORD_SEND_X, y=COORD_SEND_Y)  # 카카오톡 입력창 좌표 (수동 측정 필요)
    # pyautogui.write("" % string_to_unicode_sequence(message))
    pyautogui.hotkey("ctrl", "v")  # 클립보드 내용 붙여넣기
    pyautogui.press("enter")


def using_crawling():
    return crawl_chat_from_kakao(x=COORD_CRAWL_X, y=COORD_CRAWL_Y)  # 카카오톡 대화창 좌표 (수동 측정 필요)


def tail_text(text: str, n=1):
    lines = text.strip().split('\n')
    """리스트의 마지막 n개 줄을 반환"""
    return '\n'.join(lines[-n:]) if len(lines) > n else text


def get_chat_history():
    text = using_crawling()
    print(f"[감지된 채팅]\n{truncate_text(text) if not is_debug_mode() else text}")
    return text


if __name__ == "__main__":
    print("Not used for cli. Use module.")
