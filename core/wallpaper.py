import datetime
import io
import json
import os

import requests
from PIL import Image
from win32.lib import win32con
import win32.win32api as win32api
import win32.win32gui as win32gui

__author__ = 'sunshine'


class Wallpaper:
    def __init__(self, img_url, save_path, platform='win32'):
        self.img_suffix = ['jpeg', 'jpg', 'bmp']
        if img_url.split('.')[-1].lower() in self.img_suffix:
            self.image_url = img_url
            self.date = None
        else:
            self.image_url, self.date = self.parse_bing_wallpaper(img_url)
        self.save_path = save_path
        self.platform = platform

    def convert_img2bmp(self, wallpaper_path=None):
        """
        将图片转换成bmp格式
        :param wallpaper_path: 壁纸地址，如果没有的话则去下载
        :return:
        """
        if wallpaper_path is None:
            wallpaper_path = self.download_image()
        bmp_image = Image.open(wallpaper_path)
        bmp_path = wallpaper_path.replace("jpg", "bmp")
        bmp_path = bmp_path.split(os.sep)
        bmp_path.insert(-1, "bmp")
        bmp_dir = os.sep.join(bmp_path[:-1])
        if not os.path.exists(bmp_dir):
            os.makedirs(bmp_dir)
        bmp_path = os.sep.join(bmp_path)
        bmp_image.save(bmp_path, "BMP")
        return bmp_path

    def download_image(self, img_url=None):
        """
        下载壁纸
        :param img_url: 图片的url地址，如果不存在，则使用原本保存的地址，否则直接使用传入的地址
        :return:
        """
        if img_url:
            self.image_url = img_url
        resp = requests.get(self.image_url)
        pil_image = Image.open(io.BytesIO(resp.content))
        wallpaper_path = os.path.join(self.save_path, self.generator_wallpaper_name(day=self.date))
        pil_image.save(wallpaper_path)
        return wallpaper_path

    def set_win32_wallpaper(self, image_path=None):
        """
        :param image_path: 图片本地地址
        设置windows系统壁纸
        :return:
        """
        bmp_path = self.convert_img2bmp(image_path)
        k = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
        win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "2")  # 2拉伸适应桌面,0桌面居中
        win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
        win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, bmp_path, 1 + 2)

    @staticmethod
    def parse_bing_wallpaper(bing_url):
        """
        解析必应壁纸的图片路径
        :param bing_url:
        :return:
        """
        resp = requests.get(bing_url, json=True)
        content = json.loads(resp.text)
        url = content['images'][0]['url']
        date = content['images'][0]['enddate']
        date = date[:4]+'-'+date[4:6]+'-'+date[6:8]
        return url, date

    @staticmethod
    def generator_wallpaper_name(name="BingWallpaper", day=None):
        """
        生成壁纸名称
        :param name
        :param day
        :return:
        """
        if day is None:
            day = datetime.datetime.now().strftime("%Y-%m-%d")
        elif isinstance(day, datetime.datetime):
            day = day.strftime("%Y-%m-%d")
        return name + "-" + day + ".jpg"


if __name__ == '__main__':
    save = "E:\BingWallpapers"
    # wallpaper.set_win32_wallpaper()
    # 获取bing壁纸当天的壁纸数据
    bing = "http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&nc=1451872017333&pid=hp"
    # wallpaper = Wallpaper("http://s.cn.bing.net/az/hprichbg/rb/TutankhamunMask_ZH-CN11157835683_1920x1080.jpg", save)
    wallpaper = Wallpaper(bing, save)
    wallpaper.set_win32_wallpaper()
