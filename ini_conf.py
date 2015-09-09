#-*- encoding: utf-8 -*-
import ConfigParser

class MyIni:
    def __init__(self, confpath = 'my_ini.conf'):
        self.confpath = confpath
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(confpath)

    def get_sys(self):
        conf = {}
        conf['base_path'] = self.cf.get('SYS','base_path')
        conf['img_disk'] = self.cf.get('SYS','img_disk')
        conf['date_flag'] = self.cf.get('SYS','date_flag')
        return conf

    def set_sys(self, date_flag):
        self.cf.set('SYS', 'date_flag', date_flag)
        self.cf.write(open(self.confpath, "w"))

ini = MyIni()
ini.set_sys('2014-01-02')
del ini
        


