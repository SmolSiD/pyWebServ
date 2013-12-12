__author__ = 'user'
import configparser
config = configparser.ConfigParser()
config['Web-Server'] = {'Port': '80'}
with open('config.ini', 'w') as configfile:
  config.write(configfile)