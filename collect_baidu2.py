from urllib.parse import quote
import threading
import queue
from bs4 import BeautifulSoup
import requests
import config


# 收集百度url的类 创建实例时要传入搜索的关键词
class CollectBaidu(object):
    def __init__(self, search):
        self.search = search

    # 收集百度url的主函数
    def collectBaidu(self):
        raw_search = self.search
        search_word = quote(raw_search)
        q = queue.Queue()
        url = 'http://www.baidu.com/s?wd=' + search_word + '&pn='
        realUrl = []
        for i in range(0, 420, 10):
            q.put(url + str(i))

        thread_count = 5
        threads = []
        for i in range(thread_count):
            threads.append(self.FindUrl(q=q, result=realUrl))
        for t in threads:
            t.start()
        for t in threads:
            t.join()

            return realUrl

    # 提取每个页面所有url的多线程函数 传入包含每个页面的url队列 以及输出结果的列表
    class FindUrl(threading.Thread):
        def __init__(self, q, result):
            threading.Thread.__init__(self)
            self.q = q
            self.result = result

        # 只要队列不空 则取出百度页面url提取页面的搜索url
        def run(self) -> None:
            while not self.q.empty():
                url = self.q.get()
                print('队列剩余' + str(self.q.qsize()) + '个')
                res = requests.get(url=url, headers=config.getHeader(), timeout=1)
                s = BeautifulSoup(res.text, features='html.parser')
                tag3 = s.find_all('h3')
                for h3 in tag3:
                    href = h3.find('a').get('href')
                    try:
                        baidu_link = requests.get(url=href, headers=config.getHeader(), timeout=1)
                        if 'asp?' in baidu_link.url and 'id' in baidu_link.url:
                            print(baidu_link.url + '符合条件')
                            self.result.append(baidu_link.url)
                    except:
                        print('页面' + href + '无法访问')
                        pass


if __name__ == '__main__':
    search_word = 'inurl:asp?id='
    cb = CollectBaidu(search=search_word)
    res = cb.collectBaidu()
