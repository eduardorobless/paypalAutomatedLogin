#! python3
# paypal_login module for automated login into paypal mx
from selenium import webdriver
from decouple import config
from abc import ABCMeta, abstractstaticmethod
import logging
import traceback
import sys
logging.basicConfig(handlers=[logging.FileHandler(filename='paypal.txt',
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
        self.browser.get(paypal)
        PaypalSingleton.__instance = self

    @staticmethod
    def print_data():
        return 'Browser: {}'.format(PaypalSingleton.__instance.browser)


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
