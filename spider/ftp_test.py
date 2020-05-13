from ftp import Ftp
import traceback
import datetime


ftp = Ftp('192.168.0.1')
ftp.login('admin', 'zdd2093419')

today = datetime.date.today()

remote_file = '/sda/91/' + str(today) + '/'
try:
    ftp.mkd(remote_file)
except:
    traceback.print_exc()

ftp.close()