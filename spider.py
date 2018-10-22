from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
brower = webdriver.Chrome()
wait = WebDriverWait(brower,10)

def func_query(frm,to,date):
    '''
    填写出发地、目的地和时间进行查询
    :param frm: 出发地
    :param to: 目的地
    :param date: 时间
    :return:
    '''
    try:
        url = 'https://www.xiamenair.com/zh-cn/'
        brower.get(url)
        loca_from = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#dancheng .start-city')))
        loca_to = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#dancheng .end-city')))
        loca_date = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#dancheng #date01')))
        loca_from.clear()
        loca_to.clear()
        loca_date.clear()
        loca_from.send_keys(frm)
        loca_to.send_keys(to)
        loca_date.send_keys(date)
        # 向下滚动200px
        brower.execute_script("window.scrollBy(0,200)", "")
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#dancheng #open-line')))
        submit.click()
        get_flight()
    except TimeoutException:
        func_query(frm,to,date)
    except Exception as e:
        print("查询时间{0} 地点{1}到{2} 出错".format(date,frm,to))

def get_flight():
    '''
    提取航班信息
    :return:
    '''
    html = brower.page_source
    doc = pq(html,parser='html')
    items = doc('.segment-mess .form-mess').items()
    for item in items:
        info1 = item('.segment-info')
        num = info1.find('.flight-num').text().strip()
        flight = {
            'num':num,
            'type_plane': info1('div:nth-child(2) p').text(),
            'time_from': info1.find('#takeoffTime').text(),
            'from_airport':info1('div:nth-child(3)>p').text(),
            'time_to':info1('div:nth-child(5) .bold').text(),
            'to_airport':info1('div:nth-child(5) p').text(),
            'min_price': info1('div:nth-child(8) .flight-price').text(),
        }
        print(flight)

if __name__ == '__main__':
    func_query('天津','厦门','2018-11-03')

