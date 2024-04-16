from selenium import webdriver
import time
import pickle
import os
from selenium.webdriver.common.by import By
from config import settings

class Concert:
    def __init__(self):
        self.state = 0  # 状态
        self.log_method = 1  # 0{模拟登录,需要手动登录} 1 {cookie}
        self.browser = webdriver.Edge()

    def set_cookies(self):
        self.browser.get(settings.login_url)
        print("### 当前没有生成你的cookie_需要手动登陆 ###")
        time.sleep(25)
        print('Loading Success')
        # cookie.pkl
        pickle.dump(self.browser.get_cookies(), open('cookie.pkl', 'wb'))
        print('cookie Save Success')
        self.browser.get(settings.ticket_url)

    def get_cookie(self):
        cookies = pickle.load(open('cookie.pkl', 'rb'))
        for cookie in cookies:
            cookie_dict = {'domain': '.damai.cn', 'name': cookie.get('name'), 'value': cookie.get('value')}
            self.browser.add_cookie(cookie_dict)
        print('载入cookie成功')

    # TODO:登录
    def log_in(self):
        if self.log_method == 0:
            self.browser.get(settings.login_url)
        elif self.log_method == 1:
            if not os.path.exists('cookie.pkl'):
                self.set_cookies()
            else:
                self.browser.get(settings.ticket_url)
                self.get_cookie()

    """OpenEdge浏览器"""
    def enter_contert(self):
        Log("being daimai.com")
        self.log_in()
        self.browser.refresh()
        self.state = 2
        print('Loading success')
        self.choose_ticket()

    # TODO:选择和下单，根据页面以及需求的不同，需要改变
    def choose_ticket(self):
        if self.state == 2:
            self.states()
#---------------------------------------------票种修改处
            buybutton = self.browser.find_element(By.XPATH,value="//div[contains(text(),'看台980元')]") #根据选择的按钮文本检索。
            self.browser.execute_script("arguments[0].click();", buybutton)
            Log("成功点击1")
#---------------------------------------------

            time.sleep(1)
            buybutton_Forsh = self.browser.find_element(By.XPATH,value="//div[contains(text(), '不，立即预订')]")#选择后，有可能出现这一按钮。
            self.browser.execute_script("arguments[0].click();", buybutton_Forsh)
            Log("成功点击2")
            
            title = self.browser.title
            if title == '选择座位': #根据点击订单之后，跳转出的页面title的key值
                print("你有5秒时间选择你的座位")
                time.sleep(5.0)
                self.state()
                pass
            elif title == '确认购买':
                while True:
                    Log("loading")
                    self.check_order()
                    break

    def states(self) -> None:
        print('-' * 30)
        print()


    def check_order(self):
        print('开始确认订单')
        time.sleep(2)
        try:
            self.browser.find_element(by=By.XPATH, value = '//*[@id="container"]/div/div[2]/div[2]/div[1]/div/label').click()
        except Exception as e:
            print("###购票人信息选中失败，自行查看元素位置###")    #购票人需要为首选人
            print(e)
        time.sleep(0.5)
        self.browser.find_element(by=By.XPATH, value= "//span[contains(text(),'提交订单')]").click()

def Log(get_inp):
    print("Log_out:"+str(get_inp))



if __name__ == '__main__':
    con = Concert()
    con.log_in()
    time.sleep(1)
    con.enter_contert()
    time.sleep(1)
    con.check_order()