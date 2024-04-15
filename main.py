from selenium import webdriver
import time
import pickle
import os
from selenium.webdriver.common.by import By

login_url = "https://passport.damai.cn/login?ru=https%3A%2F%2Fwww.damai.cn%2F"
damai_url = "https://www.damai.cn/"
ticket_url = "https://detail.damai.cn/item.htm?spm=a2oeg.home.card_0.ditem_2.591b23e15Hyzkn&id=769790806798"

class Concert:
    def __init__(self):
        self.state = 0  # 状态
        self.log_method = 1  # 0{模拟登录,需要手动登录} 1 {cookie}
        self.browser = webdriver.Edge()

    def set_cookies(self):
        self.browser.get(login_url)
        print("### 请扫码登陆 ###")
        time.sleep(25)
        print('登陆成功')
        # cookie.pkl
        pickle.dump(self.browser.get_cookies(), open('cookie.pkl', 'wb'))
        print('cookie保存成功')
        self.browser.get(ticket_url)

    def get_cookie(self):
        cookies = pickle.load(open('cookie.pkl', 'rb'))
        for cookie in cookies:
            cookie_dict = {'domain': '.damai.cn', 'name': cookie.get('name'), 'value': cookie.get('value')}
            self.browser.add_cookie(cookie_dict)
        print('载入cookie成功')

    # TODO:登录
    def log_in(self):
        if self.log_method == 0:
            self.browser.get(login_url)
        elif self.log_method == 1:
            if not os.path.exists('cookie.pkl'):
                self.set_cookies()
            else:
                self.browser.get(ticket_url)
                self.get_cookie()

    """打开浏览器"""
    def enter_contert(self):
        print("进入大麦网")
        self.log_in()
        self.browser.refresh()
        self.state = 2
        print('登陆成功')
        self.choose_ticket()

    # TODO:选票和下单
    def choose_ticket(self):
        if self.state == 2:
            print('=' * 30)
            print()

            # while self.browser.title.find('确认订单') == -1:
            #     buybutton = self.browser.find_element(By.CLASS_NAME,'skuname').text
            #     if buybutton == '看台380元 可预约':
            #         self.browser.refresh()
            #         print("CODE1")
            #     elif buybutton == '看台680元 可预约':
            #         self.browser.find_element(By.CLASS_NAME, 'skuname').click()
            #         print("CODE2")
            #     elif buybutton == '看台880元 可预约':
            #         self.browser.find_element(By.CLASS_NAME, 'skuname').click()
            #         self.state = 4
            #         print("CODE3")
            #     else:
            #         self.state = 100
            #         print(self.state)
            #         print(buybutton)

            buybutton = self.browser.find_element(By.XPATH,value="//div[contains(text(),'看台980元')]")
            self.browser.execute_script("arguments[0].click();", buybutton)
            print("成功点击1")
            
            buybutton_Forsh = self.browser.find_element(By.XPATH,value="//div[contains(text(), '不，立即预订')]")
            self.browser.execute_script("arguments[0].click();", buybutton_Forsh)
            print("成功点击2")
            
            title = self.browser.title
            if title == '选择座位':
                pass
            elif title == '确认购买':
                # 实现下单的操作
                while True:
                    print("正在加载")
                    self.check_order()
                    break

    def check_order(self):
        print('开始确认订单')
        try:
            self.browser.find_element(by=By.XPATH, value = '//*[@id="container"]/div/div[2]/div[2]/div[1]/div/label').click()
        except Exception as e:
            print("###购票人信息选中失败，自行查看元素位置###")    #首选人
            print(e)
        time.sleep(0.5)
        self.browser.find_element(by=By.XPATH, value= '//*[@id="container"]/div/div[9]/button').click()


if __name__ == '__main__':
    con = Concert()
    con.log_in()
    con.enter_contert()
    con.check_order()

