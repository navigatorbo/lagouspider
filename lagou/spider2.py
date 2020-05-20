from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from lxml import etree
import re
import time

class LagouSpider(object):
    chrome_driver = r"F:\python\python_environment\chromedriver.exe"

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=self.chrome_driver)
        self.url = 'https://www.lagou.com/jobs/list_python/p-city_0?&cl=false&fromSearch=true&labelWords=&suginput='
        self.positions = []

    def run(self):
        self.driver.get(self.url)
        while True:
            #driver.page_source 可以拿到整个页面的信息，包括ajax加载的数据（网页上不显示）
            source = self.driver.page_source
            # print(source)
            #显示等待，条件：获取下一页的按钮信息
            WebDriverWait(driver=self.driver,timeout=10).until(
                EC.presence_of_element_located((By.XPATH,'//div[@class="pager_container"]/span[last()]'))
            )
            self.prase_list_page(source)
            try:
                next_btn = self.driver.find_element_by_xpath('//div[@class="pager_container"]/span[last()]')
                if "pager_next pager_next_disabled" in  next_btn.get_attribute("class"):
                    break
                else:
                    next_btn.click()
            except:
                print(source)
            time.sleep(2)

    def prase_list_page(self,source):
        html = etree.HTML(source)
        urls = html.xpath('//div[@class="position"]/div/a[@class="position_link"]/@href')
        # print(urls)
        for url in urls:
            self.request_detail_page(url)
            time.sleep(1)

    def request_detail_page(self,url):
        # self.driver.get(url)
        #打开一个新的窗口，并切换窗口
        self.driver.execute_script("window.open('%s')"%url)
        self.driver.switch_to.window(self.driver.window_handles[1])
        #WebDriverWait方法中的xpath方法不能匹配文本信息。
        WebDriverWait(driver=self.driver,timeout=10).until(
            EC.presence_of_element_located((By.XPATH,'//div[@class="job-name"]/h1'))
        )
        source = self.driver.page_source
        self.prase_detail_page(source)
        #关闭当前窗口
        self.driver.close()
        #切换回原来的窗口
        self.driver.switch_to.window(self.driver.window_handles[0])

    def prase_detail_page(self,source):
        html = etree.HTML(source)
        position_name = html.xpath('//div[@class="job-name"]/h1/text()')[0]

        job_request = html.xpath('//dd[@class="job_request"]//span')
        # 工资
        salary = job_request[0].xpath('.//text()')[0].strip()
        # 城市
        city = job_request[1].xpath('.//text()')[0]
        city = re.sub(r'[\s/]', '', city)
        # 年限
        work_years = job_request[2].xpath('.//text()')[0]
        work_years = re.sub(r'[\s/]', '', work_years)
        # 学历
        eduction = job_request[3].xpath('.//text()')[0]
        eduction = re.sub(r'[\s/]', '', eduction)
        #公司名字
        company_name = html.xpath('//h3[@class="fl"]/em/text()')[0].strip()
        #详细信息
        desc = "".join(html.xpath('//dd[@class="job_bt"]//text()')).strip()
        position ={
            'name':position_name,
            'company_name':company_name,
            'salary':salary,
            'city':city,
            'work_years':work_years,
            'eduction':eduction,
            'desc':desc
        }
        print(position)
        self.positions.append(position)


if __name__ == '__main__':
    lagou = LagouSpider()
    lagou.run()
    # print(lagou.positions)