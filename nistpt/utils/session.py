from selenium.webdriver.firefox.webdriver import WebDriver

def terminate_session(callback_menu, driver: WebDriver) -> None:
    print("--\n")
    print("Are you sure you want to terminate your session?: (y[es]/n[o])\n")

    answer = str(input("> "))
    print("\n")

    match answer:
        case "yes":
            driver.quit()
            print("Session Ended\n")
            exit()
        case "y":
            driver.quit()
            print("Session Ended\n")
            exit()
        case "no":
            callback_menu(driver)
        case "n":
            callback_menu(driver)
        case _:
            print("Please choose an available option\n")
            terminate_session(callback_menu(driver), driver)
    return
