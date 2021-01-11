import requests
import re
from download_file import DownloadFile
from ftp import Ftp
import datetime
import os
import pymongo
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from html.parser import HTMLParser
import time

# 断点调试
# BeautifulSoup , Scrapy
# 爬虫、反爬虫、反反爬虫
# 封IP-IP代理库
# m3u8格式就是将MP4分割成多个ts视频文件
class Spider():
    PATH = 'D:\\为爱鼓掌\\91\\'
    URL = 'http://www.91porn.com/v.php'
    list_pattern = '<div class="well well-sm videos-text-align">([\w\W]*?)</div>\s*</div>'
    title_href_img_pattern = '<a target=blank href="([\w\W]*?)">\s*<img src="([\w\W]*?)"[\w\W]*title="([\w\W]*?)">'
    see_pattern = '<span class="info">查看:</span>([\w\W]*?)<span'
    collect_pattern = '<span class="info">收藏:</span>([\w\W]*?)<br/>'
    comment_pattern = '<span class="info">留言:</span>([\w\W]*?)<span'
    source_pattern = 'script><source src="([\w\W]*?)" type="application/x-mpegURL"'
    id_pattern = '/(\d+)\.m3u8'
    path_pattern = '([\w\W]*?)\d+.m3u8'
    pagenum_pattern = '<input maxlength="(\d+)"[\w\W]*name="page" class="page_number"'

    def __init__(self):
        Spider.mongo_client = pymongo.MongoClient('127.0.0.1', 27017)
        Spider.mongo_db = Spider.mongo_client['db91']
        Spider.mongo_collection = Spider.mongo_db['video']

    def __get_page_num(self, html):
        pagenum = re.findall(Spider.pagenum_pattern, html)[0]
        return int(pagenum)

    def __get_content(self, page):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
            'Host': 'www.91porn.com',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://www.91porn.com/v.php?next=watch',
            'Cache-Control': 'max-age=0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
        params = {'category': 'top', 'viewtype': 'basic', 'page': page} #本月最热
        #params = {'category': 'tf', 'viewtype': 'basic', 'page': page} #本月收藏
        #params = {'category': 'hot', 'viewtype': 'basic', 'page': page} #当前最热

        response = requests.get(Spider.URL, headers=headers, params=params)

        return response.text

    def __get_content_detail(self, detail_url):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
            'Host': 'www.91porn.com',
            'Referer': 'http://www.91porn.com/v.php?category=top&viewtype=basic',
            'Cache-Control': 'max-age=0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Upgrade-Insecure-Requests': '1'}

        response = requests.get(detail_url, headers=headers)

        return response.text

    def __get_content_detail_other(self, detail_url):

        chrome_options = Options()
        #chrome以无界面模式打开
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("disable-extensions");
        chrome_options.add_argument("--start-maximized");
        chrome_options.add_argument('user-agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"')
        chrome_options.add_argument('Accept-Language: "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7"')
        chrome_options.add_argument('Host: "www.91porn.com"')
        chrome_options.add_argument('Referer: "http://www.91porn.com/v.php?category=top&viewtype=basic"')
        chrome_options.add_argument('Cache-Control: "max-age=0"')
        chrome_options.add_argument('Accept: "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"')
        chrome_options.add_argument('Upgrade-Insecure-Requests: "1"')
        #禁止加载图片
        prefs = {
            'profile.default_content_setting_values': {
                'images': 2
            }
        }
        chrome_options.add_experimental_option('prefs', prefs)
        # chrome_options.add_extension(r'D:\PyWorkSpace\learn\4.10.0_0adblock.crx')
        # 驱动路径
        path = r'D:\PyWorkSpace\learn\chromedriver.exe'



        # selenium + 无头google解决js懒加载video url问题
        browser = webdriver.Chrome(executable_path=path, options=chrome_options)
        # 解决browser.get全部加载完成需要的时间太长问题
        browser.set_page_load_timeout(10)
        browser.set_script_timeout(10)

        try:
            browser.get(detail_url)
        except:
            print("加载页面太慢，停止加载，继续下一步操作")
            browser.execute_script("window.stop()")

        page_source=browser.page_source

        browser.quit()
        p = HTMLParser()
        p.feed(page_source)
        # 处理html中&被转义
        page_source=p.unescape(page_source)
        print(page_source)
        p.close()
        return page_source


    # 提取数据
    def __analysis(self, html):
        info_list = re.findall(Spider.list_pattern, html)

        result = []
        # for rank in range(0, 1):
        for rank in range(0, len(info_list)):
            title_href_img = re.findall(Spider.title_href_img_pattern, info_list[rank])[0]
            see = re.findall(Spider.see_pattern, info_list[rank])[0]
            collect = re.findall(Spider.collect_pattern, info_list[rank])[0]
            comment = re.findall(Spider.comment_pattern, info_list[rank])[0]

            detail_html = self.__get_content_detail_other(title_href_img[0])
            #print(detail_html)
            source_url_list = re.findall(Spider.source_pattern, detail_html)
            if len(source_url_list) > 0:
                source_url = source_url_list[0]
                id = re.findall(Spider.id_pattern, source_url)[0]
                result.append(
                    {'id': id, 'title': title_href_img[2], 'source_url': source_url, 'detail_url': title_href_img[0],
                     'img': title_href_img[1],
                     'see': see, 'collect': collect, 'comment': comment, 'vtime': str(datetime.date.today())})
            else:
                print('达到每日上限！')
                break

        return result

    # 精炼数据
    def __refine(self, items):
        for item in items:
            item['see'] = re.findall('\d+', item['see'])[0]
            item['collect'] = re.findall('\d+', item['collect'])[0]
            item['comment'] = re.findall('\d+', item['comment'])[0]
            item['title'] = re.sub('[\s\\\/:*?"<>|！、，。.,]', '', item['title'])


        return items

    # 过滤掉重复数据
    def __filter(self, videos):
        result = []
        for video in videos:
            find_result = Spider.mongo_collection.find_one({'id': video['id']})
            if find_result == None:
                result.append(video)
            elif video['collect'] > find_result['collect']:
                Spider.mongo_collection.update_one({'id': video['id']}, {
                    '$set': {'see': video['see'], 'collect': video['collect'], 'comment': video['comment']}})

        return result

    def __sort(self, result):
        result = sorted(result, key=self.__sort_seed, reverse=True)
        return result

    # 指定排序依据
    def __sort_seed(self, item):
        return int(item['collect'])

    def show(self, result):
        for rank in range(0, len(result)):
            print('排名' + str(rank + 1) + '  ' + str(result[rank]))

    def m3u8file(self,path_url,file_name):
        result = []
        f = open(file_name)
        line = f.readline()
        while line:
            line = line.strip('\n')
            if not line.startswith("#"):
                result.append({'file_name': line, 'sour_url':path_url+line})
            line = f.readline()

        return result






    def go(self):
        html = self.__get_content(1)
        #print(html)
        page_num = self.__get_page_num(html)
        print('页数=' + str(page_num))
        today = datetime.date.today()

        total_num = 0

        for index in range(0, page_num):
            result_all = []
            html = self.__get_content(index + 1)
            result = self.__analysis(html)
            result_all.extend(result)

            #print(result_all)
            result_all = self.__refine(result_all)
            #print(result_all)
            result_all = self.__sort(result_all)
            self.show(result_all)


            result_all = self.__filter(result_all)
            self.show(result_all)

            print(str(today) + "有 " + str(len(result_all)) + " 部待上传")
            if len(result_all) == 0:
                continue

            dir = Spider.PATH + str(today) + "\\"

            if not os.path.exists(dir):
                os.makedirs(dir)

            ftp = Ftp('192.168.0.1')
            ftp.login('admin', 'zdd2093419')
            remote_file = '/KINGSTON-b/91/' + str(today) + '/'
            try:
                ftp.mkd(remote_file)
            except:
                traceback.print_exc()

            ftp.close()

            for index in range(0, len(result_all)):
                video = result_all[index]
                download_file = DownloadFile(dir, video['title'] + '.m3u8', video['source_url'])
                download_file.download_progress()

                # 根据m3u8文件获取到所有ts的链接
                result = spider.m3u8file(re.findall(Spider.path_pattern,video['source_url'])[0], dir+video['title'] + '.m3u8')
                print(result)

                all_ts_name=''
                # 下载所有ts
                for ts in result:
                    all_ts_name+=dir+ts['file_name']+'|'
                    download_file = DownloadFile(dir, ts['file_name'],  ts['sour_url'])
                    download_file.download_progress()

                # 合并ts
                os.system('ffmpeg -i "concat:'+all_ts_name.strip('|')+'" -acodec copy -vcodec copy -absf aac_adtstoasc '+dir+video['title'] + '.mp4')
                os.system("del "+dir+"*.ts")

                # 下载完一个就上传一个
                ftp = Ftp('192.168.0.1')
                ftp.login('admin', 'zdd2093419')
                try:
                    ftp.upload_file(dir + video['title'] + '.mp4', remote_file + video['title'] + '.mp4')
                    Spider.mongo_collection.insert_one(video)
                    print("============ " + " 已上传 " + str(index + 1) + " 部 ============")
                    total_num += 1
                except:
                    traceback.print_exc()

                ftp.close()


        print("============ " + str(today) + " 总共上传 " + str(total_num) + " 部 ============")


spider = Spider()
spider.go()
