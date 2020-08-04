# coding=utf-8

# web driver
# If you are using Chrome version 84, please download ChromeDriver 84.0.4147.30

# 記錄所有locator物件

chrome_headers = {
			'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}

dcard_login_url = "https://www.dcard.tw/signup"

WINDOW_SIZE = "1920,1080"
CHROMEDRIVER_PATH = ".\chromedriver.exe"

dlib_path = 'DCARD/model/shape_predictor_68_face_landmarks.dat'
recogn_model_path = 'DCARD/model/faceRank.h5'
recogn_model_weight_path = 'DCARD/model/faceRank_weights.h5'

accountBox_XPath = '//*[@id="__next"]/main/div/div/div/div[2]/div[1]/div[2]/div[3]/form/div[1]/label/div[2]/input'
pwdBox_XPath = '//*[@id="__next"]/main/div/div/div/div[2]/div[1]/div[2]/div[3]/form/div[2]/label/div[2]/input'
sign_up_btn_XPath = '//*[@id="__next"]/main/div/div/div/div[2]/div[1]/div[2]/div[3]/form/button'

draw_page_XPath = '//*[@id="__next"]/div[1]/div/div[2]/a[2]'
draw_sex_XPath = '//*[@id="__next"]/main/div/div/div[2]/div[1]/div[3]/div[1]/div/div/span'
draw_img_XPath = '//*[@id="__next"]/main/div/div/div[2]/div[1]/div[2]/div/picture/img'
draw_info_XPath = '//*[@id="__next"]/main/div/div/div[2]/div[1]/div[4]/div[1]/div/div/span'

invite_XPath = '//*[@id="__next"]/main/div/div/div[2]/div[1]/button'
say_hello_XPath = '/html/body/div[2]/div/div[2]/div/div/form/label/div'
send_invite_XPath = '/html/body/div[2]/div/div[2]/div/div/footer/div[2]/div[2]/button'

notify_XPath = '//*[@id="__next"]/div[1]/div/div[2]/div[1]/a'
notify_CLASS = 'sc-1ewqdax-4'
date_CLASS = 'sc-1ewqdax-5'

about_XPath = '//*[@id="__next"]/div[2]/div/div[2]/div/div[1]/div/div[1]/a[2]'
new_friend_img_CLASS = 'sc-1b8g6pv-1 xRZAa roplxp-8 dhNHZn'

received_XPath = '//*[@id="__next"]/div[1]/div/div[2]/a[3]/span'
un_reply_XPath = '//*[@id="__next"]/div[2]/div/div[1]/div/div[1]/div[2]'
img_CLASS = 'sc-44j7wu-2'
name_CLASS = 'sc-44j7wu-5'
msg_CLASS = 'sc-44j7wu-6'
time_CLASS = 'sc-44j7wu-4'

interval_wait = 0.5
total_wait = 10