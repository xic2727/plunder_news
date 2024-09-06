from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import time
import re
import pyautogui

chrome_options = Options()
chrome_options.add_argument("--headless")  # 启用无头模式
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# 使用ChromeDriverManager自动安装并设置webdriver
service = Service(ChromeDriverManager().install())

# 创建一个新的Chrome驱动实例
driver = webdriver.Chrome(service=service, options=chrome_options)

text = ""
img_srcs = []


def seleitum_page(id):
    """
    返回新闻正文和图片列表
    :param id:
    :return:
    """

    try:
        # 获取当前标签页的句柄
        original_window = driver.current_window_handle
        # 打开新标签页
        driver.execute_script("window.open('');")
        # 等待新标签页加载完成
        # WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(-1))
        # 切换到新打开的标签页
        # 切换到新标签页
        driver.switch_to.window(driver.window_handles[-1])

        # for window_handle in driver.window_handles:
        #     if window_handle != original_window:
        #         driver.switch_to.window(window_handle)
        #         break
        driver.get(f"https://www.toutiao.com/article/{id}")
        print(f"https://www.toutiao.com/article/{id}")

        try:

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]//div/article')))
            element = driver.find_elements(By.XPATH, '//*[@id="root"]//div/article')[0]

            try:
                img_elements = driver.find_elements(By.XPATH, '//*[@class="article-content"]//img')
                global img_srcs
                img_srcs = [img.get_attribute('src') for img in img_elements]

            except Exception as e:
                print(f"没有找到图片：{e}")
                img_srcs = []
            global text
            text = element.text
            # print(text)
            # print(len(img_srcs))
            return text, img_srcs
        except NoSuchElementException as e:
            print(f"新闻正文为空：{e}")
            return "", []

    except Exception as e:
            print(f"打开新闻失败，新闻不存在：{e}")
    finally:
        pass


if __name__ == '__main__':
    id = "7411020951456662070"
    # id = "7410993802837639689"
    text, img_srcs = seleitum_page(id)

    print(text)

    print(img_srcs)