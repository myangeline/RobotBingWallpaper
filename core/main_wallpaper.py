import datetime
import os

from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDesktopWidget, QApplication, QPushButton, QVBoxLayout, QLabel, \
    QWidget, QGroupBox, QGridLayout

from core.wallpaper import Wallpaper

__author__ = 'sunshine'


class MainWallpaper(QWidget):
    def __init__(self):
        super().__init__()
        self.prefix = r'../wallpapers/'
        self.bing = 'http://cn.bing.com/HPImageArchive.aspx?format=js&idx={0}&n=1&nc=1451872017333&pid=hp'
        self.save_path = os.path.dirname(__file__)
        self.save_path = os.path.join(self.save_path[:-4], 'wallpapers')
        self.files = self.get_image_list(self.save_path)
        # 标识是否为预览，预览的情况下退出后需要询问是否保存，如果保存则保留了预览的图片，否则，换回原来的桌面，
        # 所以在设置为预览后需要保存原来的桌面背景，那么问题来了，我怎么知道他原来的桌面是什么呢...
        self.is_preview = False
        # 生成今日图片的名称
        name = Wallpaper.generator_wallpaper_name()
        # 检测今日图片是否存在，不存在的话，则去下载到本地
        if not self.check_wallpaper_exists(name):
            self.current_image_name = self.download_wallpaper()
        else:
            self.current_image_name = self.files[len(self.files) - 1]

        self.image = QLabel()
        self.image.setScaledContents(True)
        self.set_image()

        vbox = QVBoxLayout()
        vbox.addWidget(self.image)

        self.ctrl_group_box = QGroupBox("控制")
        ctrl_group_box_layout = QGridLayout()

        self.btn_prev = QPushButton('上一张')
        self.btn_next = QPushButton('下一张')
        self.btn_preview = QPushButton('预览')
        self.btn_set = QPushButton('设为壁纸')
        self.btn_prev.clicked.connect(self.get_prev)
        self.btn_next.clicked.connect(self.get_next)
        self.btn_set.clicked.connect(self.set_wallpaper)
        # todo 预览功能暂时没有做
        self.btn_preview.clicked.connect(self.set_preview)

        ctrl_group_box_layout.addWidget(self.btn_prev, 0, 0)
        ctrl_group_box_layout.addWidget(self.btn_next, 0, 1)
        ctrl_group_box_layout.addWidget(self.btn_preview, 1, 0)
        ctrl_group_box_layout.addWidget(self.btn_set, 1, 1)
        self.ctrl_group_box.setLayout(ctrl_group_box_layout)
        vbox.addWidget(self.ctrl_group_box)

        self.setLayout(vbox)
        self.init_window()

    def init_window(self):
        """
        初始化窗口信息
        :return:
        """
        self.setFixedSize(800, 500)
        self.setWindowTitle("RobotBingWallpaper")
        self.set_center()

    def set_image(self):
        """
        设置图片
        :return:
        """
        image = QImage(self.prefix + self.current_image_name)
        self.image.setPixmap(QPixmap.fromImage(image))

    def set_center(self):
        """
        设置窗口居中
        :return:
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def get_prev(self):
        """
        上一张
        :return:
        """
        self.btn_next.setEnabled(True)

        now = datetime.datetime.now()
        day = self.parse_current_wallpaper_name()
        current_day = datetime.datetime.strptime(day, '%Y-%m-%d')
        prev_day = current_day - datetime.timedelta(days=1)
        delta_day = (now - prev_day).days
        prev_name = Wallpaper.generator_wallpaper_name(day=prev_day)
        if not self.check_wallpaper_exists(prev_name):
            self.btn_prev.setEnabled(False)
            image_name = self.download_wallpaper(delta_day)
            if image_name:
                self.current_image_name = image_name
                self.btn_prev.setEnabled(True)
            else:
                self.btn_prev.setText("没有更多了")
        else:
            self.current_image_name = prev_name
        self.set_image()

    def get_next(self):
        """
        下一张
        :return:
        """
        self.btn_prev.setEnabled(True)
        self.btn_prev.setText('上一张')
        now = datetime.datetime.now()
        day = self.parse_current_wallpaper_name()
        current_day = datetime.datetime.strptime(day, '%Y-%m-%d')
        next_day = current_day + datetime.timedelta(days=1)
        delta_day = (now - next_day).days
        if delta_day >= 0:
            if delta_day == 0:
                self.btn_next.setEnabled(False)
            next_name = Wallpaper.generator_wallpaper_name(day=next_day)
            if not self.check_wallpaper_exists(next_name):
                self.current_image_name = self.download_wallpaper(delta_day)
            else:
                self.current_image_name = next_name
            self.set_image()

    def set_wallpaper(self):
        """
        设置壁纸
        :return:
        """
        if not hasattr(self, 'wp'):
            self.wp = Wallpaper(self.current_image_name, self.save_path)
        self.wp.set_win32_wallpaper(os.path.join(self.save_path, self.current_image_name))

    def set_preview(self):
        print('preview...')
        pass

    def get_image_list(self, folder=None):
        """
        获取文件夹下的图片文件列表
        :param folder:
        :return:
        """
        if folder is None:
            folder = self.save_path
        files = os.listdir(folder)
        files = [f for f in files if f.endswith('.jpg')]
        files = sorted(files)
        return files

    def check_wallpaper_exists(self, name):
        """
        检测文件夹下对应的名称的图片是否存在
        :param name:
        :return:
        """
        return name in self.files

    def parse_current_wallpaper_name(self):
        """
        解析当前显示壁纸的名称，获取其中的日期
        :return:
        """
        image_name = self.current_image_name
        return image_name[len('BingWallpaper') + 1: len(image_name) - len('.jpg')]

    def download_wallpaper(self, delta_day=0):
        """
        下载壁纸
        :param delta_day: 距离当前的日期的天数
        :return:
        """
        try:
            self.wp = Wallpaper(self.bing.format(delta_day), self.save_path)
            download_path = self.wp.download_image().replace('\\', '/')
            image_name = download_path.split('/')[-1]
            self.files.append(image_name)
            return image_name
        except Exception as e:
            print(e)
            return None


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mw = MainWallpaper()
    mw.show()
    sys.exit(app.exec_())
