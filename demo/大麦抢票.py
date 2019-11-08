from selenium import webdriver
from selenium.webdriver import ActionChains
import xlrd
import time
import random
import multiprocessing
# import traceback
import logging

登录地址 = "https://m.damai.cn/damai/minilogin/index.html?returnUrl=https%3A%2F%2Fm.damai.cn%2" \
       "Fdamai%2Fmine%2Fmy%2Findex.html%3Fspm%3Da2o71.home.top.duserinfo%26anchor%3Dhome-mine&isNext=false&spm=a2o71.mydamai.0.0"

开抢时间 = "06月10日 13:18"
目标地址 = "https://m.damai.cn/damai/detail/item.html?itemId=595793324100&spm=a2o71.search.list.ditem_0"
票档条件集 = ["299元", "399元", "599元", "799元", "999元"]
选票条件集 = []
每号抢票数量 = 1
购票人数量 = 0

开抢时间字符串 = "2019-" + 开抢时间.replace("月", "-").replace("日", "") + ":00"

开抢时间 = time.mktime(time.strptime(开抢时间字符串, "%Y-%m-%d %H:%M:%S"))

logging.basicConfig(filename='d:/大麦抢票.log'.format(开抢时间字符串),
                    format='%(asctime)s:  %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %p',
                    level=40)

workbook = xlrd.open_workbook("大麦账号密码表.xlsx")
内容 = workbook.sheet_by_name("账号页")
账号集 = 内容.col_values(0)
密码集 = 内容.col_values(1)
# 姓名集 = 内容.col_values(2)
账号密码集 = dict(zip(账号集, 密码集))


# 密码姓名集 = tuple(zip(密码集, 姓名集))
# 账号密码集 = dict(zip(账号集, 密码姓名集))


class 大麦抢票:
    def 初始化浏览器(self, 账号, 密码, x坐标):
        self.账号 = 账号
        self.密码 = 密码

        self.x坐标 = x坐标

        # 提取IP = requests.get(
        # "http://webapi.http.zhimacangku.com/getip?num=1&type=1&pro=510000&city=0&yys=100017&port=11&time=2&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=").text
        mobileEmulation = random.choice(
            [{
                'deviceName': "iPhone 6/7/8 Plus"}])  # {'deviceName': "iPhone X"}, {'deviceName': "iPad"},{'deviceName': "iPad Pro"}
        options = webdriver.ChromeOptions()
        # options.add_argument("--proxy-server=http://{}".format(提取IP))
        options.add_experimental_option('mobileEmulation', mobileEmulation)
        # 禁止加载图片
        No_Image_loading = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", No_Image_loading)
        # 禁止加载css样式表
        # options.set_preference('permissions.default.stylesheet', 2)

        self.浏览器 = webdriver.Chrome(options=options)

        self.浏览器.set_window_size(442, 1020)
        self.浏览器.set_window_position(x坐标, 0)
        self.登录()

    def 登录(self):
        出错次数 = 0
        self.浏览器.get(登录地址)
        while True:
            try:
                if "退出登录" in self.浏览器.page_source:
                    break
                self.浏览器.switch_to.frame("alibaba-login-box")

                账号密码登录按钮 = self.浏览器.find_elements_by_xpath(
                    "//a[text()='账号密码登录']")  # elements 找多个  element表示只找第一个,没有找到报错.

                if len(账号密码登录按钮) > 0:
                    账号密码登录按钮[0].click()
                    time.sleep(0.5)

                账号输入框 = self.浏览器.find_element_by_xpath("//input[@id='fm-login-id']")
                密码输入框 = self.浏览器.find_element_by_xpath("//input[@id='fm-login-password']")
                账号输入框.send_keys(self.账号)
                密码输入框.send_keys(self.密码)
                登录滑块 = self.浏览器.find_elements_by_xpath("//*[@id='nc_2_n1z']")
                if len(登录滑块) > 0:
                    登录滑块 = 登录滑块[0]
                    self.登录滑块验证(登录滑块)
                登录按钮 = self.浏览器.find_element_by_xpath("//button[text()='登录']")
                登录按钮.click()
                time.sleep(3)
            except:
                # traceback.print_exc()
                if 出错次数 > 10:
                    self.浏览器.quit()
                    self.初始化浏览器(self.账号, self.密码, self.x坐标)
                    break
                else:
                    出错次数 = 出错次数 + 1
                    time.sleep(2)
        self.抢票时间 = False
        self.抢票调度()

    def 登录滑块验证(self, 登录滑块):
        self.操作浏览器 = ActionChains(self.浏览器)
        while True:
            if 登录滑块.get_attribute("class") == "nc_iconfont btn_ok":
                break
            self.操作浏览器.click_and_hold(on_element=登录滑块).move_to_element_with_offset(登录滑块, 1600, 0).perform()
            time.sleep(2)

    """
    开始抢票了
    """

    def 抢票调度(self):
        self.浏览器.get(目标地址)
        抢票错误次数 = 0
        while True:
            页面标题 = self.浏览器.title
            if 页面标题 == "商品详情":
                抢票错误次数 = 0
                返回结果 = self.等待开始抢票()
                if 返回结果 == "接口异常":
                    self.浏览器.get(目标地址)
                    time.sleep(3)
            elif 页面标题 == "订单确认":
                抢票错误次数 = 0
                返回结果 = self.订单确认()
                if 返回结果 == "接口异常":
                    self.浏览器.get(目标地址)
                    time.sleep(5)
            elif 页面标题 == "支付宝":
                print(self.账号, self.密码)
                logging.critical(self.账号 + "-----------" + self.密码 + "-----------" + self.票档条件)
                break
            elif "http" in 页面标题:
                if 抢票错误次数 > 50:
                    self.浏览器.get(目标地址)
                    抢票错误次数 = 0
                else:
                    抢票错误次数 = 抢票错误次数 + 1
                    time.sleep(0.02)
            else:
                self.浏览器.get(目标地址)

    def 等待开始抢票(self):
        if not self.抢票时间:
            while True:
                if 开抢时间 > time.time():
                    time.sleep(0.01)
                else:
                    self.抢票时间 = True
                    break

        while True:
            try:
                立即预定按钮 = self.浏览器.find_element_by_xpath("//div[@class='buy']/div[@class='buy__button']")
                立即预定按钮.click()
                time.sleep(0.2)
            except:
                try:
                    确定按钮 = self.浏览器.find_element_by_xpath("//div[@class='button-container']")
                    for self.选票条件 in 选票条件集:
                        选票按钮 = self.浏览器.find_element_by_xpath("//div[text()='{}']".format(self.选票条件))
                        选票按钮.click()
                        time.sleep(0.1)

                    for self.票档条件 in 票档条件集:
                        票档按钮 = self.浏览器.find_element_by_xpath("//*[@clicktitle='{}']".format(self.票档条件))
                        if 票档按钮.get_attribute("skutype") == "0":
                            票档按钮.click()
                            time.sleep(0.1)
                            if 每号抢票数量 > 1:
                                while True:
                                    当前选定抢票数量 = int(self.浏览器.find_element_by_xpath(
                                        "//div[@class='number-edit']/div[@class='number']").text)
                                    if 每号抢票数量 == 当前选定抢票数量:
                                        break
                                    elif 每号抢票数量 > 当前选定抢票数量:
                                        加票按钮 = self.浏览器.find_element_by_xpath(
                                            "//div[@class='number-edit']/div[text()='+']")
                                        加票按钮.click()
                                        time.sleep(0.1)
                                    else:
                                        减票按钮 = self.浏览器.find_element_by_xpath(
                                            "//div[@class='number-edit']/div[text()='-']")
                                        减票按钮.click()
                                        time.sleep(0.1)
                            确定按钮.click()
                            time.sleep(0.2)
                            break
                    else:
                        return "接口异常"
                    break
                except:
                    try:
                        关闭预览按钮 = self.浏览器.find_element_by_xpath("//span[text()='关闭预览']")
                        关闭预览按钮.click()
                        time.sleep(0.2)
                    except:
                        if "接口异常退出" in self.浏览器.page_source:
                            return "接口异常"
                        else:
                            time.sleep(0.01)

    def 订单确认(self):

        错误次数 = 0
        while True:
            try:
                是否快递 = self.浏览器.find_element_by_xpath(
                    "//div[@class='dm-delivery-way']/div[@class='header']")

                if "自助机取票" in 是否快递.text:
                    修改取票方式按钮 = self.浏览器.find_element_by_xpath(
                        "//div[@class='dm-delivery-way']/div[@class='header']/div")
                    修改取票方式按钮.click()
                    错误次数 = 0
                    time.sleep(0.2)
                while 购票人数量:
                    已选择购票人 = self.浏览器.find_elements_by_xpath(
                        "//i[@class='iconfont icon-yigouxuan1 iconfont-width']")

                    if len(已选择购票人) == 购票人数量:
                        break
                    else:
                        未选择购票人 = self.浏览器.find_elements_by_xpath(
                            "//i[@class='iconfont icon-icon-weigouxuan1 iconfont-width']")

                        未选择购票人[0].click()
                        错误次数 = 0
                        time.sleep(0.1)
                提交订单按钮 = self.浏览器.find_element_by_xpath(
                    "//*[text()='提交订单']")
                提交订单按钮.click()
                time.sleep(2)
                break
            except:
                try:
                    选择快递按钮 = self.浏览器.find_element_by_xpath(
                        "//i[@class='iconfont icon-weigouxuan1']")
                    选择快递按钮.click()
                    错误次数 = 0
                    time.sleep(0.3)
                except:
                    if 错误次数 == 3:
                        if self.浏览器.title == "支付宝":
                            break
                        else:
                            return "接口异常"
                    else:
                        time.sleep(0.5)
                        错误次数 = 错误次数 + 1


开始工作 = 大麦抢票()

x坐标 = 0
if __name__ == '__main__':
    for 账号 in 账号密码集:
        t = multiprocessing.Process(target=开始工作.初始化浏览器, args=(账号, 账号密码集[账号], x坐标), name="大麦抢票" + 账号)
        t.start()
        time.sleep(1)
        x坐标 = x坐标 + 432
# if __name__ == '__main__':
#     for 账号 in 账号密码集:
#         t = multiprocessing.Process(target=开始工作.初始化浏览器, args=("18370762017", "Cao123456", x坐标), name="大麦抢票" + 账号)
#         t.start()
#         break
#         time.sleep(1)
