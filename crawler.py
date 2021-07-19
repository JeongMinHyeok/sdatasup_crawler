import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

def crawler(data_name):
    # Chromedriver Option setting (headless)
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    
    # execute driver & connect page
    driver = webdriver.Chrome('./chromedriver', options=options)
    driver.get('http://data.seoul.go.kr/')
    
    # input data name in search box & click searchbutton
    searchbox = driver.find_element_by_css_selector("#searchKeyword") 
    searchbox.send_keys(data_name)
    searchbutton = driver.find_element_by_css_selector("#datasetVO > div > div.search-wrap > button")
    searchbutton.click()

    # select accuracy option in dropdown box & resorted
    select = Select(driver.find_element_by_id('sortColByCheck'))
    select.select_by_value('R')
    searchbutton = driver.find_element_by_css_selector("#btSortColBy > span")
    searchbutton.click()
    
    # select the first dataset
    searchbutton = driver.find_element_by_css_selector("#datasetVO > div.wrap-a > div > section > div.list-statistics > dl > dt > a > strong")
    searchbutton.click()

    # xpath of open date, edit date, institution info, team info
    open_xpath = '//*[@id="frm"]/div[3]/div[2]/table/tbody/tr[1]/td[1]/span'
    edit_xpath = '//*[@id="frm"]/div[3]/div[2]/table/tbody/tr[1]/td[2]/span'
    ins_xpath = '//*[@id="frm"]/div[3]/div[2]/table/tbody/tr[4]/td[1]'
    team_xpath = '//*[@id="frm"]/div[3]/div[2]/table/tbody/tr[4]/td[2]'
    
    # load text
    open_date = driver.find_element_by_xpath(open_xpath).text.replace('.','-')
    edit_date = driver.find_element_by_xpath(edit_xpath).text.replace('.','-')
    institution = driver.find_element_by_xpath(ins_xpath).text
    team = driver.find_element_by_xpath(team_xpath).text
    link = driver.current_url
    print('공개일자 : {}, 최신수정일자 : {}, 제공기관 : {}, 제공부서 : {}'.format(open_date, edit_date, institution, team))
    
    driver.close()
    
    # return to list
    return [open_date, edit_date, institution, team, link]