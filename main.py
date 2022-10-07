from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.extensions.android.nativekey import AndroidKey
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json,time,winsound

desired_caps = {
  'platformName': 'Android', # 被测手机是安卓
  'platformVersion': '11', # 手机安卓版本
  'deviceName': 'M2006J10C', # 设备名，安卓手机可以随意填写
  'unicodeKeyboard': True, # 使用自带输入法，输入中文时填True
  'resetKeyboard': True, # 执行完程序恢复原来输入法
  'noReset': True,       # 不要重置App
  'newCommandTimeout': 6000,
  'automationName' : 'UiAutomator2'
  # 'app': r'd:\apk\bili.apk',
}
'''
'appPackage': 'com.jingyao.easybike', # 启动APP Package名称
'appActivity': 'com.hellobike.atlas.business.portal.PortalActivity', # 启动Activity名称
'''

'''
# 连接Appium Server，初始化自动化环境
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
'''

'''
# 设置缺省等待时间
driver.implicitly_wait(5)
'''

# 关闭广告
try:
    ad = driver.find_element(By.ID, "com.jingyao.easybike:id/actionDialogClose")
    ad.click()
except NoSuchElementException as e:
    pass

#确定是否有订单在找乘客,如果有就点进订单
try:
    driver.find_element(By.XPATH, "//*[@text='正在寻找顺路乘客']").click()
    print('有订单,尝试订单查找')
except NoSuchElementException as e:
    #如果没有,进入车主页并进行跨市查找
    print('没有订单,尝试跨市查找')
    raise

#获取所有订单信息
'''
#打印顺路程度
hitch_percents = driver.find_elements(By.ID, 'com.jingyao.easybike:id/tvHitchPercent')
for hitch_percent in hitch_percents:
    print(hitch_percent.text)
'''

#循环查找合适的订单
got_it = 0
while got_it == 0:
    #计算是否有达到条件的订单
    amounts = driver.find_elements(By.ID, 'com.jingyao.easybike:id/tvAmount')
    orders = 1
    for amount in amounts:
        print(amount.text)
        if float(amount.text) > 150:
            print('第',orders,'笔订单达到金额条件,点进去')
            amount.click()
            got_it = 1
            break
        else:
            orders += 1

    #如果找到就开始扫描订单是否合适
    if got_it == 1:
        #检查订单是否合适

        while 1:
            #合适,重复声音报警
            winsound.PlaySound('alert', winsound.SND_ASYNC)
            time.sleep(1)
    else:
        #过段时间刷新订单
        print('没有合适的订单,20秒后刷新')
        time.sleep(20)
        # 获取屏幕分辨率,宽度,高度
        size = driver.get_window_size()
        width = size['width']
        height = size['height']
        # 执行滑屏操作,向下（下拉）滑动
        x1 = width*0.5
        y1 = height*0.4
        y2 = height*0.8
        driver.swipe(x1,y1,x1,y2)
        print("滑动完成")


'''
#点进订单
driver.find_element(AppiumBy.XPATH, "//android.widget.LinearLayout[@resource-id='com.jingyao.easybike:id/dslContainerView']/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup").click()
'''


'''
# 根据id定位搜索输入框，点击
sbox = driver.find_element(By.ID, 'search_src_text')
sbox.send_keys('白月黑羽')
# 输入回车键，确定搜索
driver.press_keycode(AndroidKey.ENTER)
'''


input('**** Press to quit..')
driver.quit()
