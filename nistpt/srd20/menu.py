from selenium.webdriver.firefox.webdriver import WebDriver
from nistpt.srd20.panes import *
from nistpt.utils.session import terminate_session
# from nistpt.srd20 import SRD20


def compounds_menu(driver: WebDriver) -> None:

    COMPOUNDS_PATH = "/ChemicalName"
    SRD20_PREFIX = "https://srdata.nist.gov/xps"

    if driver.current_url != SRD20_PREFIX + COMPOUNDS_PATH:
        driver.get(SRD20_PREFIX + COMPOUNDS_PATH)

    print("Compounds Menu")

    search = str(input("Search: "))
    # print("\n")

    res, url_dict = compounds(driver, search)
    if res == "":
        print("Compound Not Found. Please try another one\n--\n")
        compounds_menu(driver)

    print(res)

    def extend_compound_menu(url_dict) -> None:
        option_str = "Get "
        key_list = [key for key in url_dict.keys()]

        def option(option_str=option_str, key_list=key_list):
            if len(key_list) > 1:
                option_count = 0
                option_str += "("
                for key in key_list:
                    option_count += 1
                    if option_count % 2 == 0:
                        option_str += " / "
                    option_str += f"{option_count}. {key}"
                # print("\n")
                option_str += ")"
                print(option_str)
                option = str(input("> "))
                print("\n")
            else:
                option = 1
            return option, option_str


        while True:
            try:
                setting = option()
                option_str = f"Get {key_list[int(setting[0])-1]} from compound NUMBER:"
                break
            except Exception as e:
                print(e)

        print(option_str)

        extend = str(input("> "))
        print("\n")

        match extend:
            case "q":
                terminate_session(compounds_menu(driver), driver)
            case "quit":
                terminate_session(compounds_menu(driver), driver)
            case _:
                try:
                    if extend == "0":
                        extend = "1"
                    res, url_dict = compound_details(
                        driver, int(extend), int(setting[0]), url_dict
                    )
                    print(res)
                    while url_dict != {}:
                        extend_compound_menu(url_dict)
                except Exception:
                    print("Input must be equal to corresponding number or q[uit]\n")
                    extend_compound_menu(url_dict)
        return

    extend_compound_menu(url_dict)

    return


def menu_controller(driver: WebDriver) -> None:
    try:
        compounds_menu(driver)
    except Exception as e:
        print(e)
        driver.quit()
    return
