
import datetime as dt
from datetime import datetime
import logging
from selenium import webdriver
from protocol import CHROMEDRIVER_PATH, WINDOW_SIZE
import os
from selenium.webdriver.chrome.options import Options

def getDay():
	now = datetime.now()
	today = str(now.strftime("%Y-%m-%d"))

	now -= dt.timedelta(days=1)
	yesterday = "{}月{}日".format(now.month, now.day)
	return today, yesterday

def getLogger(loggerName, loggerPath):
	# 設置logger
	logger = logging.getLogger(loggerName)  # 不加名稱設置root logger
	logger.setLevel(logging.DEBUG)
	formatter = logging.Formatter(
		'%(asctime)s - %(name)s - %(levelname)s: - %(message)s',
		datefmt='%Y-%m-%d %H:%M:%S')
	logging.Filter(loggerName)

	# 使用FileHandler輸出到文件
	directory = os.path.dirname(loggerPath)
	if not os.path.exists(directory):
		os.makedirs(directory)
	fh = logging.FileHandler(loggerPath)

	fh.setLevel(logging.DEBUG)
	fh.setFormatter(formatter)

	# 使用StreamHandler輸出到屏幕
	ch = logging.StreamHandler()
	ch.setLevel(logging.DEBUG)
	ch.setFormatter(formatter)
	# 添加兩個Handler
	logger.addHandler(ch)
	logger.addHandler(fh)
	# Handler只啟動一次
	# 設置logger
	logger.info(u'logger已啟動')
	return logger

def get_driver():
	chrome_options = Options()  
	chrome_options.add_argument("--headless")  
	chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

	driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
						   chrome_options=chrome_options) 
	# driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH)
	return driver