#! python3
# paypal_login module for automated login into paypal mx
from selenium import webdriver
from decouple import config
from abc import ABCMeta, abstractstaticmethod
import logging
import traceback
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


logging.basicConfig(handlers=[logging.FileHandler(filename=config('LOGFILE'),
                                                  encoding='utf-8')],
                    level=logging.DEBUG,
                    format="{} - {} - {}".format(
                        '%(asctime)s', '%(levelname)s', '%(message)s'
))
# logging.disable()


class IPaypal(metaclass=ABCMeta):
    @abstractstaticmethod
    def print_data():
        """ Implement in child class """


class PaypalSingleton(IPaypal):
    __instance = None

    @staticmethod
    def get_instance():
        if PaypalSingleton.__instance is None:
            PaypalSingleton()
        return PaypalSingleton.__instance

    def __init__(self):
        if PaypalSingleton.__instance is not None:
            raise Exception("Singleton cannot be instantiated more than once!")
        else:
            self.browser = webdriver.Firefox(
                executable_path=r"{}".format(config('FIREFOX_PATH')))
            PaypalSingleton.__instance = self

    def open_paypal(self):
        self.browser.get(paypal_url)
        PaypalSingleton.__instance = self

    @staticmethod
    def print_data():
        return 'Browser: {}'.format(PaypalSingleton.__instance.browser)

    def fill_form(self):
        login_btn = self.browser.find_element_by_id('ul-btn')
        login_btn.click()
        email_field = self.browser.find_element_by_id('email')
        logging.debug('The value of email is: {} with type: {} '.format(
            email_field.get_attribute('value'), type(email_field.get_attribute('value'))))

        if email_field.get_attribute('value'):
            password_field = self.browser.find_element_by_id('password')
            login_btn = self.browser.find_element_by_id('btnLogin')
            password_field.send_keys(config('PASSWORD'))
            login_btn.submit()

        else:
            email_field.send_keys(config('EMAIL'))
            btn_next = self.browser.find_element_by_id('btnNext')
            btn_next.click()
            try:
                WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.ID, "password"))
                )
                password_field = self.browser.find_element_by_id('password')
                password_field.send_keys(config('PASSWORD'))
            except Exception as err:
                logging.error('Err: {} , traceback : {}'.format(
                    err, traceback.format_exc()))
                sys.exit(1)
            try:
                WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.ID, "btnLogin"))
                )
                login_btn = self.browser.find_element_by_id('btnLogin')
                login_btn.submit()
            except Exception as err:
                logging.error('Err: {} , traceback : {}'.format(
                    err, traceback.format_exc()))
                sys.exit(1)

        logging.info('Successfully logged in!')


if __name__ == '__main__':
    paypal_url = 'http://paypal.com/mx/home'
    try:
        paypal = PaypalSingleton()
        logging.debug(paypal.print_data())
    except Exception as err:
        logging.error('Err: {} , traceback : {}'.format(
            err, traceback.format_exc()))
        sys.exit(1)

    try:
        paypal.open_paypal()
    except Exception as err:
        logging.error('Err: {} , traceback : {}'.format(
            err, traceback.format_exc()))
        sys.exit(1)

    try:
        paypal.fill_form()
    except Exception as err:
        logging.error('Err: {} , traceback : {}'.format(
            err, traceback.format_exc()))
        sys.exit(1)
