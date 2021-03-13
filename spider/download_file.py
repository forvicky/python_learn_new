import requests
import time


class DownloadFile():
    def __init__(self, file_path, file_name, file_url):
        self.file_path = file_path
        self.file_name = file_name
        self.file_url = file_url

    def download_small(self):
        start = time.time()
        r = requests.get(self.file_url)
        with open(self.file_path + self.file_name, 'wb') as file:
            file.write(r.content)

        end = time.time()
        print('\n' + "%s下载完成！用时%.2f秒" % (self.file_name, end - start))

    def download_big(self):
        start = time.time()
        r = requests.get(self.file_url, stream=True)
        with open(self.file_path + self.file_name, "wb") as file:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)

        end = time.time()
        print('\n' + "%s下载完成！用时%.2f秒" % (self.file_name, end - start))

    def download_progress(self):
        start = time.time()
        size = 0
        response = requests.get(self.file_url, stream=True)
        chunk_size = 1024
        result = response.headers.get('content-length')
        if result != None:
            content_size = int(result)
            if response.status_code == 200:
                print('[文件大小]:%0.2f MB' % (content_size / chunk_size / 1024))
                with open(self.file_path + self.file_name, "wb") as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        size += len(data)
                        print('\r' + '[下载进度]:%s%.2f%%' % (
                            '>' * int(size * 50 / content_size), float(size / content_size * 100)), end='')
            end = time.time()
            print('\n' + "%s下载完成！用时%.2f秒" % (self.file_name, end - start))
