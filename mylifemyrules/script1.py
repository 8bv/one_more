from threading import Thread
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd


data = pd.read_excel('123 — копия.xlsx')


def parser(start, step):
    driver = webdriver.Chrome()
    driver.get("https://kaplife.ru/company/agents/")

    for i in range(start, len(data), step):
        try:
            driver.find_element_by_name("number").send_keys(data['ФИО'][i])
        except ElementNotInteractableException:
            print(i)
            pass
        driver.find_element_by_link_text("Искать").click()

        try:
            driver.find_element_by_class_name("agentbase__success")
            data['АД'][i-step] = driver.find_element_by_css_selector('p.agentbase--title').get_attribute('textContent')[8:27]
            data['дата заключения'][i-step] = driver.find_element_by_css_selector('p.agentbase--date').get_attribute('textContent')[:10]
        except NoSuchElementException:
            pass

        driver.wait = WebDriverWait(driver, 10)
        driver.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "paginationBlock")))

        driver.find_element_by_link_text("Проверить другого агента").click()
        if i % 101 == 0:
            data.to_excel('123.xlsx', index=False)

    driver.quit()
    data.to_excel('123.xlsx', index=False)


def main(amount):
    print('начальная точка, это опционально, можно просто пропустить')
    try:
        start = int(input("нажав кавишу 'Enter': "))
    except ValueError:
        start = 0
    finally:
        threads = []
        for thread in range(amount):
            t = Thread(target=parser, args=(thread+start, amount, ))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        print("Выполнение потоков звершено")


if __name__ == '__main__':
    amount = int(input('количество потоков: '))
    main(amount)
