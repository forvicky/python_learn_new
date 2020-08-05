import requests
import json
import os
from download_file import DownloadFile
import re



#https://m.weishi100.com/m/course/courses?courseId=1109428&pageNum=1&pageSize=10
#https://m.weishi100.com/m/course/download?purchaseId=312163061560135680&courseId=3845246


class Spider():
    path="D:\\weishi\\"
    courListUrl="https://m.weishi100.com/m/course/courses"
    courDetailUrl="https://m.weishi100.com/m/course/download"


    def __getCourseList(self):
        headers = {
            'Host': 'm.weishi100.com',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; Pixel 2 Build/OPM1.171019.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.98 Mobile Safari/537.36; weishi-student',
            'Referer': 'https://m.weishi100.com/mweb/androidApp/series/?id=1109428&isLowVersion=1&isNewLive=1&purchaseId=312163061560135680',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.8',
            'Cookie': 'GID=e813f1f51fd245cac223f33b07332202; weishiroute=36b2dff54efda9dfd537ccd41fffb6e4; _weishi_uid_=8680325; acw_tc=2f624a5715966147915222860e63194c78e0c4f9b6e2ee879429e16bf7c8d3; _const_weishi_id_="b51b9ad5-a521-4e7f-9f0e-a3a88e8c348e::63DB15433F4E7FA6AAE2D708B9F81153"; Hm_lvt_4fe36727dba7aabcdd581120c42af358=1596606456; Hm_lpvt_4fe36727dba7aabcdd581120c42af358=1596616436',

        }
        params = {'courseId': 1109428, 'pageNum': 1, 'pageSize': 40}

        response = requests.get(Spider.courListUrl, headers=headers, params=params)

        return response.text

    def __getCourseDetail(self,courseId):
        headers = {
            'Host': 'm.weishi100.com',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.1.0; Pixel 2 Build/OPM1.171019.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.98 Mobile Safari/537.36; weishi-student',
            'Referer': 'https://m.weishi100.com/mweb/androidApp/series/?id=1109428&isLowVersion=1&isNewLive=1&purchaseId=312163061560135680',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.8',
            'Cookie': 'GID=e813f1f51fd245cac223f33b07332202; weishiroute=36b2dff54efda9dfd537ccd41fffb6e4; _weishi_uid_=8680325; acw_tc=2f624a5715966147915222860e63194c78e0c4f9b6e2ee879429e16bf7c8d3; _const_weishi_id_="b51b9ad5-a521-4e7f-9f0e-a3a88e8c348e::63DB15433F4E7FA6AAE2D708B9F81153"; Hm_lvt_4fe36727dba7aabcdd581120c42af358=1596606456; Hm_lpvt_4fe36727dba7aabcdd581120c42af358=1596616436',

        }
        params = {'purchaseId': 312163061560135680, 'courseId': courseId}

        response = requests.get(Spider.courDetailUrl, headers=headers, params=params)

        return response.text

    def go(self):
        responseStr=self.__getCourseList()
        print(responseStr)

        responseModel=json.loads(responseStr)
        courses=responseModel["data"]["courses"]

        for course in courses:
            responseStr=self.__getCourseDetail(course["id"])
            print(responseStr)
            responseModel = json.loads(responseStr)
            playbackVideos = responseModel["data"]["downloadInfo"]["playbackVideos"]
            for playbackVideo in playbackVideos:
                if playbackVideo["cdn"]=="ms":
                    course["downloadUrl"]=playbackVideo["url"]
                    break

        i=0

        for course in courses:
            print(course["id"])
            course['name'] = re.sub('[\s\\\/:*?"<>|~]', '', course['name'])

            print(course["name"])
            print(course["downloadUrl"])
            print("========================================")

            i=i+1

            if not os.path.exists(Spider.path):
                os.makedirs(Spider.path)

            download_file = DownloadFile(Spider.path, str(i)+"."+course['name'] + '.mp4', course['downloadUrl'])
            download_file.download_progress()






spider = Spider()
spider.go()