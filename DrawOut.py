# coding=utf-8
import sys
import time
from datetime import datetime
from protocol import *
from get_config import *
import os
import numpy as np
from flow import open_web
from send_mail import send
# 網頁成功開啟後開啟logger
try:
	today, yesterday = getDay()
	loggerName = "DCARD"
	loggerPath = 'DCARD/LOG/log - ' + str(today) + '.txt'
	logger = getLogger(loggerName, loggerPath)

	DCARD_INFO = {}
	login_file = 'DCARD_INFO.txt'
	logger.info(u'檢查登入文件:{}'.format(os.path.exists(login_file)))
	if os.path.exists(login_file):
		logger.info(os.path.abspath(login_file))
		with open(login_file, 'r') as f:
			data = f.readlines()
			for d in data:
				d = d.split(' ')
				DCARD_INFO[d[0]] = d[1].replace('\n', '')

		while (True):
			status, mail_text = open_web(logger, yesterday, 
										DCARD_INFO['NKFUST_ACCOUNT'], 
										DCARD_INFO['NKFUST_PASSWORD'], 
										u'高科狄卡')
			if status != False:
				send(logger,
						DCARD_INFO['SMTP_ACCOUNT'], 
						DCARD_INFO['SMPT_PASSWORD'], 
						u'高科狄卡', 
						mail_text, 
						today)
				break

		while (True):
			status, mail_text = open_web(logger, yesterday, 
										DCARD_INFO['NCKU_ACCOUNT'], 
										DCARD_INFO['NCKU_PASSWORD'], 
										u'成大狄卡')
			if status != False:
				send(logger,
						DCARD_INFO['SMTP_ACCOUNT'], 
						DCARD_INFO['SMPT_PASSWORD'], 
						u'成大狄卡', 
						mail_text, 
						today)
				break

		while (True):
			status, mail_text = open_web(logger, yesterday, 
										DCARD_INFO['NTU_ACCOUNT'], 
										DCARD_INFO['NTU_PASSWORD'], 
										u'台大狄卡')
			if status != False:
				send(logger,
						DCARD_INFO['SMTP_ACCOUNT'], 
						DCARD_INFO['SMPT_PASSWORD'], 
						u'台大狄卡', 
						mail_text, 
						today)
				break

	else:
		logger.info(u'找不到登入文件:{}'.format(login_file))

except Exception as e:
	traceback = sys.exc_info()[2]
	print(sys.exc_info())
	print(traceback.tb_lineno)
	print(e)
finally:
	logger.info(u'logger已關閉')
	handlers = logger.handlers[:]
	for handler in handlers:
		handler.close()
		logger.removeHandler(handler)
