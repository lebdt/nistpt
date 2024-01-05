from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def selenium_get_table(
    driver: WebDriver,
) -> ([[str]], [str], dict):
    header = [
        "NUMBER",
    ]
    table = []
    url_dict = {}

    col_titles = driver.find_elements(By.CLASS_NAME, "rz-column-title-content")
    WebDriverWait(driver, timeout=2).until(lambda f : col_titles[0].is_displayed())

    for i in range(len(col_titles)):
        title = col_titles[i].text
        header.append(title)
        url_dict[title] = []

    page_summary = driver.find_elements(By.XPATH, "//*[@class='rz-paginator-summary']")

    if page_summary == []:
        page_num = 1
    else:
        page_num = int(
            page_summary[0].text[10]
        )  # text='Page x of y...' | y is the eleventh char (index=10)

    elem_number = 0

    for p in range(page_num):
        rows = driver.find_elements(By.CLASS_NAME, "rz-data-row")

        for i in range(len(rows)):
            elem_number += 1
            cols = rows[i].find_elements(By.CLASS_NAME, "rz-cell-data")
            if cols == [""] * len(cols):
                break
            table_row = [
                str(elem_number),
            ]
            for j in range(len(cols)):
                cell_data = cols[j]
                if cell_data.text != "":
                    table_row.append(cols[j].text)
                else:
                    child_elem = cols[j].find_elements(By.TAG_NAME, "a")[0]
                    url_dict[header[j + 1]].append(child_elem.get_attribute("href"))
                    # table_row.append(child_elem.get_attribute("href"))
                    table_row.append("...")
            table.append(table_row)

            for key in [i for i in url_dict.keys()]:
                if url_dict[key] == []:
                    url_dict.pop(key, None)

        if page_num != 1:
            paginator_next = driver.find_elements(
                By.XPATH, "//a[contains(@class, 'rz-paginator-next')]"
            )
            paginator_next[0].click()

    print("Success")

    return table, header, url_dict


def selenium_get_summary(driver: WebDriver) -> (str, [str], dict):
    current_page_driver = driver
    onepage_summary_btn = current_page_driver.find_elements(
        By.XPATH,
        "//*[contains(@rel, 'noopener') and contains(@title, 'Click for one page')]",
    )[0]
    WebDriverWait(driver, timeout=2).until(lambda f : onepage_summary_btn.is_displayed())
    onepage_summary_btn.click()

    cols = driver.find_elements(
        By.XPATH,
        "//*[@class='row']/div[contains(@class,'col') and not(@class='col col-sm-12')]",
    )

    table = []

    for i in range(0, len(cols) - 1, 2):
        if cols[i + 1].text != "":
            table.append([cols[i].text, cols[i + 1].text])

    return table, [], {}
