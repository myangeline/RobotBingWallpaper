import io
import requests
from PIL import Image
from win32.lib import win32con
import win32.win32api as win32api
import win32.win32gui as win32gui
__author__ = 'sunshine'


def setWallpaperFromBMP(imagepath):
    k = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "2")  # 2拉伸适应桌面,0桌面居中
    win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, imagepath, 1 + 2)


def convent2BMP(picFile):
    bmpImage = Image.open(picFile)
    newPath = r"C:\Users\sunshine\Desktop\images\demo_wallpaper.bmp"
    bmpImage.save(newPath, "BMP")
    return newPath

if __name__ == '__main__':
    # img_path = convent2BMP(r"C:\Users\sunshine\Desktop\images\demo.jpg")
    # setWallpaperFromBMP(img_path)
    resp = requests.get("http://s.cn.bing.net/az/hprichbg/rb/RedLakeBolivia_ZH-CN12956356143_1920x1080.jpg")
    # print(resp.content)
    pil_image = Image.open(io.BytesIO(resp.content))
    newPath = r"C:\Users\sunshine\Desktop\images\BingWallpaper.bmp"
    pil_image.save(newPath, "BMP")
    pass

