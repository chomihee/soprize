import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

def paralympic_crawler():
    # 옵션 생성
    options = webdriver.ChromeOptions()
    # 창 숨기는 옵션 추가
    options.add_argument("headless")

    driver = webdriver.Chrome('/Users/mhcho/chromedriver', options=options)
    driver2 = webdriver.Chrome('/Users/mhcho/chromedriver', options=options)
    driver.get('https://olympics.com/tokyo-2020/paralympic-games/en/results/all-sports/athletes.htm')
    time.sleep(5)

    # 페이지 지정
    paralympic_athletes = {}
    athletes_no = 1
    # 다음 페이지 이동
    while True:
        if athletes_no == 100:
            break
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        # 게시판 1번부터 19번까지 이동하면서 링크 가져오면서 이동 새 페이지 이동!
        for i in range(0, 20):
            temp = {}
            link = soup.select('#entries-table > tbody >tr')[i].select('td')[0].select('a')[0]['href']

            name = soup.select('#entries-table > tbody >tr')[i].select('td')[0].select('a')[0].select('span')[1].text
            print(name)
            noc = soup.select('#entries-table > tbody >tr')[i].select('td')[1].select('a')[0]['title'].split('\n')[1]
            driver2.get('https://olympics.com/tokyo-2020/paralympic-games/en/results' + link)
            time.sleep(5)
            temp['name'] = name
            temp['NOC'] = noc
            # 이동한 페이지에 정보를 긁어옴
            #  정보 긁어옴
            basic_infos = driver2.find_elements_by_class_name('col-md-6')
            for basic_info in basic_infos[0].find_elements_by_tag_name('div'):
                if basic_info.text != "":
                    temp[basic_info.text.split(': ')[0]] = basic_info.text.split(': ')[1]

            temp[basic_infos[1].text.split(': ')[0]] = basic_infos[1].text.split(': ')[1]

            # 추가 정보
            add_infos = driver2.find_elements_by_class_name('form-group')  # 길이만큼 가져와야함
            for info in add_infos:
                if ':' in info.text.split('\n')[0]:
                    label = info.text.split('\n')[0].replace(":", "")
                else:
                    label = info.text.split('\n')[0]
                temp[label] = info.text.split('\n')[1]

            paralympic_athletes[athletes_no] = temp
            print(athletes_no)
            athletes_no = athletes_no + 1

        # 오류날때까지 페이지 이동
        # 현재 페이지가 안넘어가는 이슈가 있음 !!
        # // *[ @ id = "entries-table_paginate"]
        # driver.find_elements_by_css_selector('ul.pagination > *')[8].click().perform()
        #element = driver.find_element_by_xpath('// *[ @ id = "entries-table_paginate"]')
        element = driver.find_elements_by_css_selector('ul.pagination > *')[8]
        actions = ActionChains(driver)
        actions.move_to_element(element).click().perform()


    return paralympic_athletes


if __name__ == "__main__":
    print(paralympic_crawler())
