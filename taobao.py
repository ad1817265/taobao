from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
from pyquery import PyQuery as pq
from urllib.parse import quote
import requests

key_word=('书包')
chrome=webdriver.Chrome()
def login():
    page=1
    chrome.get('https://login.taobao.com/member/login.jhtml')
    chrome.maximize_window()
    chrome.find_element_by_id('fm-login-id').send_keys('****')
    time.sleep(2)
    chrome.find_element_by_id('fm-login-password').send_keys('******')
    time.sleep(2)
    slider_square = chrome.find_element_by_id('nc_1_n1z')
    # 判断方块是否显示，是则模拟鼠标滑动，否则跳过
    if slider_square.is_displayed():
        # 鼠标点击滑块并保持
        ActionChains(chrome).click_and_hold(slider_square).perform()
        # 鼠标多次向右移动随机距离
        for i in range(0,5):
            ActionChains(chrome).move_by_offset(random.randint(60,80), 5).perform()
        # 抬起鼠标左键
        ActionChains(chrome).release()
        # 等待随机时间，以免被反爬虫
        time.sleep(random.uniform(0, 1))  
    chrome.find_element_by_class_name('fm-btn').click()
    # url='https://s.taobao.com/search?q='+quote(key_word)
    # chrome.get(url)

        
def get_product():
    html = chrome.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('data-src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)

def main():
    login()
    for i in range(1,5):
        next_url='https://s.taobao.com/search?q=%E4%B9%A6%E5%8C%85&bcoffset=-3&ntoffset=-3&p4ppushleft=1%2C48&s={}'.format((i-1)*44)
        chrome.get(next_url)
        print("当前页-------------------------",i)
        get_product()
        time.sleep(5)
    
    
    
if __name__=='__main__':
    main()


