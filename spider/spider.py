from urllib import request
import gzip
import re

#断点调试
#BeautifulSoup , Scrapy
#爬虫、反爬虫、反反爬虫
#封IP-IP代理库
class Spider():
    URL='https://www.douyu.com/g_jiaoyou'
    root_pattern='<div class="DyListCover-content">([\w\W]*?)</a>'
    name_pattern1='<h2([\w\W]*?)</h2>'
    name_pattern2='</svg>([\w\W]*)'

    number_pattern='</svg>([\w\W]*?)</span>'

    def __get_content(self):
        headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
        douyu_url=request.Request(Spider.URL,headers=headers)
        r=request.urlopen(douyu_url)
        html=r.read()
        html=gzip.decompress(html).decode('utf-8')
        return html

    #提取数据
    def __analysis(self,html):
        root_html=re.findall(Spider.root_pattern,html)
        result =[]
        for rank in range(0,len(root_html)):
            name=re.findall(Spider.name_pattern1,root_html[rank])
            name=re.findall(Spider.name_pattern2,name[0])
            number=re.findall(Spider.number_pattern,root_html[rank])
            result.append({'name':name,'number':number})
        return result

    #精炼数据
    def __refine(self,items):
        l=lambda item:{
            'name':item['name'][0].strip(),  #strip()除去空格
            'number':item['number'][0]
        }
        return map(l,items)


    def __sort(self,result):
        result=sorted(result,key=self.__sort_seed,reverse=True)
        return result

    #指定排序依据
    def __sort_seed(self,item):
        r = re.findall('\d*',item['number'])
        number = float(r[0])
        if '万' in item['number']:
            number *= 10000
        return number

    def show(self,result):
        for rank in range(0,len(result)):
            print('排名'+str(rank+1)+'  '+result[rank]['name']+'   '+result[rank]['number'])

    def go(self):
        html=self.__get_content()
        items=self.__analysis(html)
        result=list(self.__refine(items))   #map要转为list才能打印
        result=self.__sort(result)
        self.show(result)

spider=Spider()
spider.go()


