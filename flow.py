import time
from protocol import *
from get_config import get_driver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import matplotlib.image as img 
import matplotlib.pyplot as plt

from datetime import datetime
import os

import requests as req
from io import BytesIO

import sys

import matplotlib.image as img 
import matplotlib.pyplot as plt
import cv2
import numpy as np

from recognize import predict_image

def download_image(logger, url, name, p=True):
	date = datetime.now().strftime("%Y-%m-%d")
	img_dir = 'DCARD/Image/' + date + '/'
	logger.info(img_dir)

	if not os.path.exists(img_dir):
		logger.info('create folder')
		os.makedirs(img_dir)
		
	img_path = img_dir + "{}.jpg".format(name.replace('\t', ''))
	with open(img_path, 'wb') as handle:
		response = req.get(url, headers=chrome_headers, stream=True)
		if not response.ok:
			print(response)
		for block in response.iter_content(1024):
			if not block:
				break
			handle.write(block)

	image = img.imread(img_path)
	image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR) # opencvImage
	# cv2.imshow("OpenCV",image)  
	# cv2.waitKey() 
	return image

def get_pred_info(logger, image, p=True):
	if p:
		try:
			score = predict_image(logger, image)
			if score > 60:
				return 'beautiful', '#ff1aff', score
			else:
				return 'normal', 'black', score
		except:
			return 'Unknown', 'black', 0
	else:
		return "Unknown", "black", 0


def open_web(logger, yesterday, account, pwd, alis):
	try:
		driver = get_driver()
		driver.get(dcard_login_url)

		# 輸入帳號
		accountBox = driver.find_element_by_xpath(accountBox_XPath)		
		accountBox.send_keys(account)  # 清空內容

		# 輸入密碼
		pwdBox = driver.find_element_by_xpath(pwdBox_XPath)
		pwdBox.send_keys(pwd)  # 清空內容

		# 送出按鈕
		driver.find_element_by_xpath(sign_up_btn_XPath).click()  # 送出
		time.sleep(5)

		# 前往抽卡頁面
		while (True):
			try:
				locator = (By.XPATH, draw_page_XPath)
				WebDriverWait(driver, 5, interval_wait).until(EC.presence_of_element_located(locator))
				driver.find_element_by_xpath(draw_page_XPath).click()
				logger.info('前往抽卡頁面')
				break
			except:
				pass
				driver.refresh()

		# 判斷性別
		locator = (By.XPATH, draw_sex_XPath)
		WebDriverWait(driver, total_wait, interval_wait).until(EC.presence_of_element_located(locator))
		sex = driver.find_element_by_xpath(draw_sex_XPath).text

		mail_text = u'<html><body>'
		box_flag = False
		if u'女' in sex:

			locator = (By.XPATH, draw_img_XPath)
			WebDriverWait(driver, total_wait, interval_wait).until(EC.presence_of_element_located(locator))
			img_src = driver.find_element_by_xpath(draw_img_XPath).get_attribute('src')

			locator = (By.XPATH, draw_info_XPath)
			WebDriverWait(driver, total_wait, interval_wait).until(EC.presence_of_element_located(locator))
			info = driver.find_element_by_xpath(draw_info_XPath).text

			info = info.replace(' ', '	-	')
			logger.info(img_src)
			logger.info(info + u" " + sex)
			info = info.replace('＆emsp;', ' ')
			image = download_image(logger, img_src, info)
			face_text, color, score = get_pred_info(logger, image)
			mail_text += '<h2>' + alis + '</h2>'
			try:
				mail_text += '<font size="4" color="' + color + '">' + info + '</font>' + '<br>'
				mail_text += '<font size="5" color="' + color + '">' + u"顏質分數 ==> " + str(score) + '</font>' + '<br>'
				mail_text += '<font size="5" color="' + color + '">' + face_text + '</font>' + '<br>'
				mail_text += '<img src="'
				# 送出邀請
				driver.find_element_by_xpath(invite_XPath).click()
				# 打招呼
				driver.find_element_by_xpath(say_hello_XPath).send_keys(u'Hi~~妳好')
				# 送出
				driver.find_element_by_xpath(send_invite_XPath).click()
				logger.info(u'已送出邀請')
				mail_text += img_src + '">' + u'抽卡 - 狀態 : ' + u'已送出邀請' + '</a></h4>'
			except Exception as e:
				logger.info(u'已重複抽卡')
				mail_text += img_src + '">' + u'抽卡 - 狀態 : ' + u'已重複抽卡' + '</a></h4>'
			# traceback = sys.exc_info()[2]
			# logger.error(sys.exc_info())
			# logger.error(traceback.tb_lineno)
			# logger.error(e)
		else:
			mail_text += '<h4>' + alis + '</h4>'
			mail_text += u'<h4>歐歐~~今天抽到的男孩子呢ㅠㅠ 明日請再接再厲:")</h4>'
			logger.info(u'今日的抽卡是男生')

		# time.sleep(3)
		driver.refresh()
		# 點擊通知
		locator = (By.XPATH, notify_XPath)
		WebDriverWait(driver, total_wait, interval_wait).until(EC.presence_of_element_located(locator))
		driver.find_element_by_xpath(notify_XPath).click()
		time.sleep(2)

		locator = (By.CLASS_NAME, notify_CLASS)
		WebDriverWait(driver, total_wait, interval_wait).until(EC.presence_of_element_located(locator))
		notfy_list = driver.find_elements_by_class_name(notify_CLASS)
		date_list = driver.find_elements_by_class_name(date_CLASS)

		if len(notfy_list) > 0:
			for index in range(0, len(notfy_list)):
				nofify = notfy_list[index].text
				date = date_list[index].text
				if (u'命運之神' in nofify) and (date == yesterday):
					logger.info(date + u"恭喜獲得新卡友")
					logger.info(nofify)
					# 前往新好友頁面
					notfy_list[index].click()
					logger.info(u'前往新好友頁面')
					# ----------------------------------------------------
					# 點擊好友關於
					driver.find_element_by_xpath(about_XPath).click()
					logger.info(u'點擊好友關於')
					# ----------------------------------------------------
					time.sleep(3)
					img_src = driver.find_element_by_class_name(new_friend_img_CLASS).get_attribute('src')
					logger.info(img_src)
					mail_text += u'<h2 align="center">' + date + u'恭喜獲得新卡友</h2><br>'
					mail_text += '<h4><img src="' + img_src + '"></h4>'
					mail_text += u'<h2 align="center">' + nofify + '</h2>'
					box_flag = True
					break
				if index == 4:
					logger.info(u'無新卡友')

		else:
			logger.info(u'無新卡友')

		# 若無新卡友切至收件閘
		if not box_flag:
			logger.info(u'切至收件閘')
			locator = (By.XPATH, received_XPath)
			WebDriverWait(driver, total_wait, interval_wait).until(EC.presence_of_element_located(locator))
			driver.find_element_by_xpath(received_XPath).click()
		# 未讀信件訊息
		# time.sleep(5)

		# 切至未回覆信件閘
		locator = (By.XPATH, un_reply_XPath)
		WebDriverWait(driver, total_wait, interval_wait).until(EC.presence_of_element_located(locator))
		driver.find_element_by_xpath(un_reply_XPath).click()

		# 收集未讀信件條
		msgInfo = driver.find_element_by_xpath(un_reply_XPath)
		imgList = driver.find_elements_by_class_name(img_CLASS)
		nameList = driver.find_elements_by_class_name(name_CLASS)
		msgList = driver.find_elements_by_class_name(msg_CLASS)
		timeList = driver.find_elements_by_class_name(time_CLASS)
		mail_text += '<h3><p>' + msgInfo.text + '</h3>'

		if (len(imgList) == 0):
			logger.info(u'沒有未回覆信件')
			mail_text += '<h4><p>' + u'沒有未回覆信件' + '</h4></p>'
		else:
			for i in range(len(nameList)):
				receive_img = str(imgList[i].get_attribute('src'))
				# logger.info(receive_img)
				mail_text += '<h4><img src="' + receive_img
				mail_text += '" width="70px" height="90px"></a>'
				mail_text += '<font size="3" color="#ff1aff">' + nameList[i].text + '<br>'
				t_text = str(timeList[i].text).split(" ")[-1]
				mail_text += '&emsp;&emsp;&emsp;&emsp;' + '(' + t_text + ')' + '</font>'
				mail_text += '<h4><p>' + msgList[i].text + '</h4></p>'

		mail_text += '</body></html>'

		time.sleep(3)
		driver.close()
		return True, mail_text
	except Exception as e:
		driver.close()
		traceback = sys.exc_info()[2]
		logger.error(sys.exc_info())  #
		logger.error(traceback.tb_lineno)  #
		logger.error(e)
		return False, None
