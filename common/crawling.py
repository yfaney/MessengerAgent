import time
import pyautogui
import pyperclip


def crawl_chat_from_kakao(x=100, y=350):
    pyautogui.click(x=x, y=y)  # 카카오톡 대화창창 좌표 (수동 측정 필요)
    time.sleep(1)  # 커서 및 창 활성화 대기
    pyautogui.hotkey("ctrl", "a")  # 전체 선택
    time.sleep(1)  # 전체 선택 대기
    pyautogui.hotkey("ctrl", "c")  # 클립보드에 대화내용 복사
    time.sleep(1)  # 클립보드 복사 대기

    chat_history = pyperclip.paste()  # 클립보드 내용 가져오기
    return chat_history
