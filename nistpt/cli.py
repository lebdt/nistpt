from __future__ import print_function
import os
import argparse

from selenium.webdriver.firefox.webdriver import WebDriver
from nistpt.srd20.menu import *


parser = argparse.ArgumentParser()

parser.add_argument("--opt", help="printout the first arg")

args = parser.parse_args()


def initialize_webdriver():
    os.environ["MOZ_HEADLESS"] = "1"
    driver = WebDriver()
    driver.implicitly_wait(4)
    return driver


def main():
    print(args.opt)
    menu_controller(initialize_webdriver())
    return


if __name__ == "__main__":
    main()
