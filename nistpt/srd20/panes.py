from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from nistpt.utils.tables import *
from tabulate import tabulate
# from nistpt.srd20 import SRD20


def compounds(
    driver: WebDriver or None, compound: str, exact: bool = False
) -> (str, dict):
    SRD20_PREFIX = "https://srdata.nist.gov/xps"

    current_page_driver = driver
    current_page_driver.implicitly_wait(2)

    SELENIUM = 1
    COMPOUNDS_PATH = "/ChemicalName"
    if SELENIUM == 1:
        if driver.current_url != SRD20_PREFIX + COMPOUNDS_PATH:
            current_page_driver.get(SRD20_PREFIX + COMPOUNDS_PATH)

        # sleep(1)

        if (
            current_page_driver.find_elements(
                By.CLASS_NAME,
                "rz-chkbox modified valid rz-state-empty".replace(" ", "."),
            )
            == []
        ):
            checkbox_active = True
        else:
            checkbox_active = False

        if exact == (not checkbox_active):
            # sleep(1)
            exact_checkbox = current_page_driver.find_elements(
                By.CLASS_NAME, "rz-chkbox-box"
            )[0].click()

        search_box = current_page_driver.find_elements(
            By.XPATH, "//*[contains(@class,'rz-textbox') and contains(@class, 'w-50')]"
        )[0]
        search_box.clear()
        search_box.send_keys(compound)
        search_box.send_keys(Keys.RETURN)
        
        results_table, header, url_dict = selenium_get_table(current_page_driver)

    if results_table == []:
        return ("", {})
    else:
        return (
            tabulate(
                results_table,
                headers=header,
                tablefmt="fancy_grid",
                maxcolwidths=[30] * len(header),
            ),
            url_dict,
        )


def compound_details(
    driver: WebDriver, compound: int, option: int, url_dict: dict
) -> (str, dict):
    current_page_driver = driver
    details_url = url_dict

    chosen_option = [key for key in details_url.keys()][option - 1]

    follow_url = details_url[chosen_option][compound - 1]
    current_page_driver.get(follow_url)

    title_header = current_page_driver.find_elements(By.CLASS_NAME, "TitleHeader")[0]
    print(title_header.text, f" ({follow_url})")

    if title_header.text == "Details Summary:":
        results_table, header, new_dict = selenium_get_summary(current_page_driver)
    else:
        results_table, header, new_dict = selenium_get_table(current_page_driver)

    return (
        tabulate(
            results_table,
            headers=header,
            tablefmt="fancy_grid",
            maxcolwidths=[40] * len(results_table[0]),
        ),
        new_dict,
    )
