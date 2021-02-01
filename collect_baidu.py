import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
import config


# 1.找到百度的搜索页面url规律
# 2.将搜索xxx得到结果的url全部放入queue中
# 3.多线程跑queue中的url 把每个页面的所有url提取出来
# 4.对url检验是否符合xxx的约束
# 5.所有符合要求的url存入txt中等待下步扫描

# https://www.baidu.com/s?wd=inurl%3Aasp%3Fid%3D
def get_real_url(urls):
    real_urls = []
    page = 0
    for url in urls:
        print('***************************正在访问第' + str(page) + '页**************************************')
        page += 1
        response = requests.get(url=url, headers=config.getHeader(),timeout=1)
        soup = BeautifulSoup(response.text, features='html.parser')
        tag3 = soup.find_all('h3')
        i = 0
        for h3 in tag3:
            href = h3.find('a').get('href')
            print('正在解析第' + str(i) + '个链接')
            i += 1
            try:
                baidu_link = requests.get(url=href, headers=config.getHeader(), timeout=1)
                if 'asp?' in baidu_link.url and 'id' in baidu_link.url:
                    print(baidu_link.url + '符合条件')
                    real_urls.append(baidu_link.url)
            except:
                print('页面' + href + '无法访问')
                pass
    return real_urls


if __name__ == '__main__':
    search_word_raw = 'inurl:asp?id='
    search_word = quote(search_word_raw)
    urls = []
    url = 'http://www.baidu.com/s?wd=' + search_word + '&pn='
    for i in range(0, 410, 10):
        urls.append(url + str(i))
    print('请求的页面url为' + urls[0])
    real_urls = get_real_url(urls)
    print(real_urls)

    # 第二种解析方法
    # tag3 = soup.find_all('h3')
    # print(type(tag3))
    # for h3 in tag3:
    #     href = h3.find('a').get('href')
    #     print(href)
