from selenium import webdriver
import requests
from tqdm import tqdm
from pandas import json_normalize


def paralympic_crawler():
    # json 형태로 저장된 웹 페이지를 불러온다
    json_url = 'https://olympics.com/tokyo-2020/paralympic-games/en/results/all-sports/zzje001a.json'
    json_data = requests.get(json_url).json()

    # 옵션 생성
    options = webdriver.ChromeOptions()
    # 창 숨기는 옵션 추가
    options.add_argument("headless")
    driver = webdriver.Chrome('/Users/mhcho/chromedriver', options=options)
    # 해당 json에 이름 noc 관련 링크 존재함
    paralympic_athletes = json_data['data']

    for athlete in tqdm(json_data['data']):
        link = athlete['lnk']
        driver.get('https://olympics.com/tokyo-2020/paralympic-games/en/results' + link)

        # 이동한 페이지에 정보를 긁어옴
        # 동작 도중 index error 발생한 경우 그냥 pass 진행 > 해당번호(1번부터시작) 1320, 1912, 2864 에서 오류 발생 csv 직접 수정..?
        try:
            basic_infos = driver.find_elements_by_class_name('col-md-6')
            for basic_info in basic_infos[0].find_elements_by_tag_name('div'):
                if basic_info.text != "":
                    athlete[basic_info.text.split(':')[0]] = basic_info.text.split(':')[1]

            for basic_info in basic_infos[1].find_elements_by_tag_name('div'):
                if (basic_info.text != "") and (":" in basic_info.text):
                    athlete[basic_info.text.split(':')[0]] = basic_info.text.split(':')[1]

        except IndexError:
            print("Index error link : " + link)
            pass

        # 추가 정보
        add_infos = driver.find_elements_by_class_name('form-group')  # 길이만큼 가져와야함
        for info in add_infos:
            if ':' in info.text.split('\n')[0]:
                label = info.text.split('\n')[0].replace(":", "")
            else:
                label = info.text.split('\n')[0]
            athlete[label] = info.text.split('\n')[1]
    driver.close()
    return paralympic_athletes


if __name__ == "__main__":
    df = json_normalize(paralympic_crawler())
    df.to_csv('./data/paralympic_athletes.csv')
