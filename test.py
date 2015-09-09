import os
import shutil
import logging
import datetime
import time

import arrow

from psutil_func import *
from my_logger import online_logging
from ini_conf import MyIni

online_logging(u'logs\\error.log')
logger = logging.getLogger('root')

BASE_PATH = 'SpreadData\ImageFile'
IMG_DISK_LIST = ['E','F']
DATE_FLAG = '2015-06-01'

BEGIN = datetime.time(0, 0, 0, 0)
END = datetime.time(4, 0, 0, 0)

def total_disk_state():
    disk_dict = disk_state_dict()
    total = 0L
    free = 0L
    for i in IMG_DISK_LIST:
        if disk_dict.get(i, None):
            total += disk_dict[i]['total']
            free += disk_dict[i]['free']

    return {'total': total, 'free': free, 'free_percent': float(free)/total}

def remove_files():
    for i in IMG_DISK_LIST:
        path = os.path.join('%s:\\' % i, BASE_PATH, DATE_FLAG.format('YYYYMMDD'))
        print '[%s] remove files %s' % (arrow.now().format('YYYY-MM-DD'), path)
        try:
            if os.path.isdir(path):
                for f in os.listdir(path):
                    rm_file = os.path.join(path, f)
                    shutil.rmtree(rm_file)
                    logger.warning('%s has been removed' % rm_file)
        except Exception as e:
            logger.error(e)

def main_loop():
    ini = MyIni('my_ini.conf')
    sys_ini = ini.get_sys()
    BASE_PATH = sys_ini['base_path']
    IMG_DISK_LIST = sys_ini['img_disk'].split(',')
    DATE_FLAG = arrow.get(sys_ini['date_flag'])

    while 1:
        try:
            t = arrow.now().time()
            if t > BEGIN and t < END:
                disk_dict = total_disk_state()
                if disk_dict['free_percent'] < 0.02:
                    remove_files()
                    DATE_FLAG.replace(days=1)
                    ini.set_sys(DATE_FLAG.format('YYYY-MM-DD'))
            time.sleep(1)
        except KeyboardInterrupt:
            break
    del ini
    print 'quit'


if __name__ == "__main__":
    #print disk_state()
    #print disk_state_dict()
    #print total_disk_state()
    #test()
    #remove_files()
    main_loop()


