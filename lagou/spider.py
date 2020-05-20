import time
from lxml import etree
import requests
import re
# 爬虫程序返回没有结果，爬取网页仍可以访问，说明爬虫程序被检测到了，最简单的方法：检测传递的参数（可能是cookie过期）
# ip地址被封的话，爬虫程序和网页都不能显示，

#此处需要设置Cookie，User-Agent，Referer，Accept（可以不设置），不然报操作频繁错误
urls = 'https://www.lagou.com/jobs/list_python/p-city_0?&cl=false&fromSearch=true&labelWords=&suginput='
url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
           'Referer':'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
           'Accept':'application/json, text/javascript, */*; q=0.01'
           }
data = {
    'first': 'false',
    'pn':'1',
    'kd': 'python'
}
#使用Session方法获取搜索页的cookie
s=requests.Session()
s.get(urls,headers=headers,timeout=3)
cookie = s.cookies

def get_list_page():
    # response = requests.post(url=url,headers=headers,data=data,cookies=cookie,timeout= 3)
    # #json方法，如果返回的是json数据，那么这个方法可以直接load成字典
    # print(response.json())
    for x in range(10):
        data['pn']=x
        response = requests.post(url=url, headers=headers, data=data, cookies=cookie, timeout=3)
        # print(response.json())
        # time.sleep(1)
        result = response.json()
        positions = result['content']['positionResult']['result']
        for position in positions:
            positionID = position['positionId']
            position_url = 'https://www.lagou.com/jobs/%s.html' % positionID
            print(position_url)
            prase_list_page(position_url)
            time.sleep(5)
            # break
        break

def prase_list_page(url):
    response = requests.get(url,headers=headers)
    text = response.text
    html = etree.HTML(text)

    position_name = html.xpath('//div[@class="job-name"]/h1/text()')[0]
    print(position_name)
    job_request = html.xpath('//dd[@class="job_request"]//span')
    #工资
    salary = job_request[0].xpath('.//text()')[0].strip()
    #城市
    city = job_request[1].xpath('.//text()')[0]
    city = re.sub(r'[\s/]','',city)
    #年限
    work_years = job_request[2].xpath('.//text()')[0]
    work_years = re.sub(r'[\s/]','',work_years)
    #学历
    eduction = job_request[3].xpath('.//text()')[0]
    eduction = re.sub(r'[\s/]','',eduction)
    # 公司名字
    company_name = html.xpath('//h3[@class="fl"]/em/text()')[0].strip()
    desc = "".join(html.xpath('//dd[@class="job_bt"]//text()')).strip()



if __name__ == '__main__':
    get_list_page()