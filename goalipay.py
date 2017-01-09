#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author leo hao
# os windows 7

import os
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from bs4 import BeautifulSoup

from business import Business, UserInfo
from sysevent import SysEvent


class Alipay:
    def __init__(self, loginname, pwd):
        self._loginname = loginname
        self._pwd = pwd

        self.__chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = self.__chromedriver
        self.__driver = webdriver.Chrome(self.__chromedriver)

    def do_work(self):
        try:
            self.__login()
            # self.__goentrance()
            self.__gopayment()

            # time.sleep(86400)
            self.__driver.close()
            self.__driver.quit()
        except Exception as e:
            print(e)
            self.__driver.close()
            self.__driver.quit()
        finally:
            pass

    def __login(self):
        self.__driver.get("https://authsu18.alipay.com/login/index.htm")
        self.__driver.maximize_window()

        name_ele = self.__driver.find_element_by_id("J-input-user")
        name_ele.send_keys(self._loginname)

        pwd_ele = self.__driver.find_element_by_id("password_rsainput")
        pwd_ele.send_keys(self._pwd)

        self.__driver.find_element_by_id("J-login-btn").send_keys(Keys.RETURN)

    def __goentrance(self):
        time.sleep(random.uniform(1, 2))
        userlist = Business.getuser()
        for u in userlist:
            self.__driver.get("https://custweb.alipay.com/appeal/entrance")
            time.sleep(random.uniform(1, 2))
            name_ele = self.__driver.find_element_by_name('userName')
            name_ele.send_keys(u.UserName)
            time.sleep(random.uniform(1, 2))
            cartno_ele = self.__driver.find_element_by_name('certNo')
            cartno_ele.send_keys(u.CertNo)
            time.sleep(random.uniform(1, 2))
            # self.__driver.find_element_by_id("submit").send_keys(Keys.RETURN) 这里报错
            code = """
                  document.getElementById('submit').click()
                   """
            self.__driver.execute_script(code)

            while self.__driver.current_url.find("https://custweb.alipay.com/appeal/choose") <= -1:
                time.sleep(random.uniform(1, 2))

            form = self.__driver.find_element_by_name('choose')
            form_content = form.text
            print(form_content)

    def __gopayment(self):
        for i in range(5):
            time.sleep(random.uniform(1, 2))
            # self.__driver.get("https://shenghuo.alipay.com/send/payment/fill.htm")
            self.__driver.get("https://shenghuo.alipay.com/transfer/otmpay/fill.htm")

            # 添加到20个收款人
            code = """
                            for (var i=0; i<=15; i++)
                            {
                                 setTimeout(function(){
                                    document.getElementById('addUser').click()
                                 }, {0});
                            }
                  """
            code = code.replace('{0}', str(random.uniform(3, 5)))
            self.__driver.execute_script(code)

            # 录入电话号码
            phones = Business.getphones()
            for index, p in enumerate(phones):
                time.sleep(random.uniform(1, 3))

                se = SysEvent()
                se.mouse_click(800, 800)

                code = """
                            setTimeout(function(){

                                var ev = document.createEvent("MouseEvents");
                                ev.initEvent("click", true, true);
                                document.querySelector("#main").dispatchEvent(ev);

                                document.getElementsByClassName("i-text account-display")[{0}].focus();
                                document.getElementsByClassName("i-text account-display")[{0}].value = '{1}'
                                document.getElementsByClassName("i-text account-display")[{0}].blur();

                                document.getElementsByClassName("i-text i-prize amount")[{0}].focus();
                            }, {2})
                        """
                code = code.replace('{0}', str(index))
                code = code.replace('{1}', p.Phone)
                code = code.replace('{2}', str(random.uniform(1, 2)))
                self.__driver.execute_script(code)

                # ele = self.__driver.find_element_by_id('ipt-search-key')
                # ele.send_keys('')
                # ele.send_keys(p)
                #
                # m_ele = self.__driver.find_element_by_name('payAmount')
                # m_ele.send_keys('')
                # m_ele.send_keys(random.randint(1000, 2000))

            self.__analysis_dom()

    def __analysis_dom(self):
        time.sleep(random.uniform(1, 3))
        ele = self.__driver.find_element_by_id("payers")

        soup = BeautifulSoup(ele.get_attribute("outerHTML"), 'lxml')
        li_eles = soup.select("li")
        for li in li_eles:
            try:
                phone = self.__get_elements_first(li.select('input[name="optEmails"]')).attrs["value"]
                realname = self.__get_elements_first(li.select('input[name="realname"]')).attrs["value"]
                # optUserIds = self.__get_elements_first(li.select('input[name="optUserIds"]'))
                print('%s %s' % (phone, realname))
                # 正常请求 phone realname 都会不为空，没有不操作，下次继续获取
                if phone is not None and phone != '' and realname is not None and realname != '':
                    Business.updateRealNameByPhone(phone, realname)
            except Exception as e:
                print(e)

    @staticmethod
    def __get_elements_first(root_ele):
        return (lambda x: None if len(x) <= 0 else x[0])(root_ele)

    @staticmethod
    def __get_element_by_index(root_ele, index):
        return (lambda x: None if len(x) < index else x[index])(root_ele)


if __name__ == "__main__":
    # loginName = sys.argv[1]
    # password = sys.argv[2]
    loginName = 'shiniujin9374@yeah.net'
    password = 'wxx261'
    # loginName = '18516291436'
    # password = '1qazXDR%'
    if loginName is not None and loginName != '' and password is not None and password != '':
        bt = Alipay(loginName, password)
        bt.do_work()
