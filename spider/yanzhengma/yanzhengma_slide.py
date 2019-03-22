from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time

EMAIL = ''
PASSWORD = ''
class Crackgeet():
    def __init__(self):
        self.url = 'https://id.163yun.com/login'
        self.brower = webdriver.Chrome()
        self.wait = WebDriverWait(self.brower,10)
        self.email = EMAIL
        self.password = PASSWORD
    def get_geetest_button(self):
        '''
        获取初始验证位置
        :return:按钮对象
        '''
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'geetest_radar_tip')))
        return button
    def get_position(self):
        '''
        获取验证码位置
        :return: 验证码位置元组
        '''
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'geetest_canvas_img')))
        time.sleep(2)
        location = img.location
        size = img.size
        top,bottom,left,right = location['y'],location['y']+size['height'],\
                                location['x'],location['x']+size['width']
        return (top,bottom,left,right)
    def get_geetest_image(self):
        '''
        获取验证码图片
        :param name:图片对象
        :return:
        '''
        top,bottom,left,right = self.get_position()
        print('验证码位置',top,bottom,left,right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left,bottom,left,right))
        return captcha
    def get_slider(self):
        '''
        获取滑块
        :return:滑块对象
        '''
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'geetest_slider_button')))
        return slider
    def is_pixel_equal(self,image1,image2,x,y):
        '''
        判断两个像素是否相同
        :param image1: 图片1
        :param image2: 图片2
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同
        '''
        #取两个图片的像素点
        pixel1 = image1.load()[x,y]
        pixel2 = image2.load()[x,y]
        threshold = 60
        if abs(pixel1[0]-pixel2[0]) < threshold and abs(pixel1[0]-pixel2[0]) < threshold and \
            abs(pixel1[0]-pixel2[0]) < threshold:
            return True
        else:
            return False

    def get_gap(self,image1,image2):
        '''
        获取缺口偏移量
        :param image1:不带缺口图片
        :param image2:带缺口图片
        :return:缺口的横坐标位置
        '''
        left = 60
        for i in range(left,image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1,image2,i,j):
                    left = i
                    return left
        return left

    def get_track(self,distance):
        '''
        根据偏移量获取移动轨迹
        :param distance:
        :return:移动轨迹
        '''
        #移动轨迹
        track = []
        #当前位移
        current = 0
        #减速阈值
        mid = distance * 4 / 5
        #计算间隔
        t = 0.2
        #初速度
        v = 0

        while current < distance:
            if current < mid:
                #加速度为+2
                a = 2
            else:
                #减速度为-3
                b = -3
            #初速度
            v0 = v
            #当前速度
            v = v0 + a * t
            #移动距离
            move = v0 * t + 1/2 * a * t * t
            #当前位移
            current += move
            track.append(round(move))
        return track

    def move_to_gap(self,slider,tracks):
        '''
        拖动滑块到缺口处
        :param slider:滑块
        :param tracks: 轨迹
        :return:
        '''
        ActionChains(self.brower).click_and_hold(slider).perform()
        for x in tracks:
            ActionChains(self.brower).move_by_offset(xoffset=x,yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.brower).release().perform()
    def run(self):
        button = self.get_geetest_button()
        button.click()
        img1 = self.get_geetest_image()
        slider = self.get_slider()
        slider.click()
        img2 = self.get_geetest_image()
        gap = self.get_gap(img1,img2)
        tracks = self.get_track(gap)
        self.move_to_gap(slider,tracks)

if __name__ == '__main__':
    spider = Crackgeet()
    spider.run()
