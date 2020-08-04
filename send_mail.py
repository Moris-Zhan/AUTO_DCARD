from email.mime.text import MIMEText
# from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
# from smtplib import SMTP
import smtplib
import sys

def send(logger, sender, passwd, alis, text, today):
	try:
		logger.info(u'發送email')  # 建立mail (發送圖片)
		receivers = ['afly.bsky@yahoo.com.tw']
		emails = [elem.strip().split(',') for elem in receivers]
		msg = MIMEMultipart()
		msg['Subject'] = alis + str(today)
		msg['From'] = sender
		msg['To'] = ','.join(receivers)

		msg.preamble = 'Multipart massage.\n'
		part = MIMEText(text, 'html', 'utf-8')
		msg.attach(part)

		smtp = smtplib.SMTP("smtp.gmail.com:587")
		smtp.ehlo()
		smtp.starttls()
		smtp.login(sender, passwd)

		smtp.sendmail(msg['From'], emails, msg.as_string())
		logger.info('Send mails to ' + msg['To'])
		logger.info(u'寄信成功')
	except smtplib.SMTPException as e:
		logger.error(e)
		logger.error(u'寄信失敗')

	except Exception as e:
		traceback = sys.exc_info()[2]
		logger.error(sys.exc_info())
		logger.error(traceback.tb_lineno)
		logger.error(e)
	finally:
		smtp.quit()

