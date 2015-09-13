import os
import shutil
import logging
import datetime
import time

import arrow

from psutil_func import *
from my_logger import online_logging
from ini_conf import MyIni

online_logging(u'logs/error.log')
logger = logging.getLogger('root')


class ImgCleaner(object):
    def __init__(self):
        my_ini = MyIni('my_ini.conf')
        sys_ini = my_ini.get_sys()

        self.base_path = sys_ini['base_path']
        self.disk_list = sys_ini['img_disk'].split(',')
        self.date_flag = arrow.get(sys_ini['date_flag'])

        self.begin = datetime.time(0, 0, 0, 0)
        self.end = datetime.time(4, 0, 0, 0)

    def __del__(self):
        del my_ini
        print 'quit'
    
    def total_disk_state():
        disk_dict = disk_state_dict()
        total = 0L
        free = 0L
        for i in self.disk_list:
            if disk_dict.get(i, None):
                total += disk_dict[i]['total']
                free += disk_dict[i]['free']

        return {'total': total, 'free': free, 'free_percent': float(free)/total}

    def remove_files():
        for i in self.disk_list:
            rm_file = os.path.join('%s:\\' % i, self.base_path,
                                   self.date_flag.format('YYYYMMDD'))
            try:
                if os.path.isdir(rm_file):
                    shutil.rmtree(rm_file)
                    print '%s has been removed' % rm_file
                    logger.warning('%s has been removed' % rm_file)
            except Exception as e:
                logger.error(e)

    def main_loop():
        while 1:
            try:
                t = arrow.now().time()
                if t > BEGIN and t < END:
                    disk_dict = self.total_disk_state()
                    if disk_dict['free_percent'] < 0.03:
                        remove_files()
                        self.date_flag.replace(days=1)
                        my_ini.set_sys(DATE_FLAG.format('YYYY-MM-DD'))
                time.sleep(1)
            except KeyboardInterrupt:
                break



if __name__ == "__main__":
    #print disk_state()
    #print disk_state_dict()
    #print total_disk_state()
    #test()
    #remove_files()
    main_loop()


