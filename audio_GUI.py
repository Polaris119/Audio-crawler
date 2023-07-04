from PyQt5.Qt import *
from audio_spider import *
import sys
import time


class WorkerThread(QThread):
    # 自定义信号，传递两个字符串参数
    finish = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(WorkerThread, self).__init__(parent)
        self.text1 = None
        self.text2 = None

    def run(self):
        # 调用audio_spider.py的函数
        filename, url, headers = bv_name(self.text1, self.text2)
        res = send_request(url, headers).text
        video = get_video_data(res)  # 音频地址
        start_time = time.time()  # 下载开始时间
        save_data(filename, video, headers)
        end_time = time.time()  # 下载结束时间

        value1 = video  # 音频地址
        value2 = "下载完成咯！！！用时" + str(round(end_time - start_time, 2)) + '秒'  # 下载用时，保留两位小数
        self.finish.emit(value1, value2)  # 发射信号，传递结果给主线程


class mainwindow(QWidget):

    def __init__(self):
        super(mainwindow, self).__init__()
        self.windowUI()
        self.setWindowTitle("B站音频提取")
        self.resize(1000, 1000)

    def windowUI(self):
        palette = QPalette()
        pix = QPixmap("./file/background.jpg")

        pix = pix.scaled(self.width(), self.height())

        palette.setBrush(QPalette.Background, QBrush(pix))
        self.setPalette(palette)

        label_1 = QLabel(self)
        label_1.move(400, 70)
        label_1.setText("B站音频提取")
        label_1.setFont(QFont('SimHei', 20))

        label_2 = QLabel(self)
        label_2.move(500, 900)
        label_2.setText("数据来源：Bilibili")

        label_3 = QLabel(self)
        label_3.move(800, 900)
        label_3.setText("作者：Polaris")
        # label_3.setFont(QFont('Arial', 0))

        label_4 = QLabel(self)
        label_4.move(200, 200)
        label_4.setText("输入BV号")
        label_4.setFont(QFont('SimSun', 20, 75))

        label_5 = QLabel(self)
        label_5.move(200, 300)
        label_5.setText("输入文件名")
        label_5.setFont(QFont('SimSun', 20, 75))

        label_6 = QLabel(self)
        label_6.move(200, 480)
        label_6.setText("音频地址")
        label_6.setFont(QFont('SimSun', 20, 75))

        label_7 = QLabel(self)
        label_7.move(200, 680)
        label_7.setText("下载用时")
        label_7.setFont(QFont('SimSun', 20, 75))

        self.line_1 = QLineEdit(self)  # BV号
        self.line_1.resize(200, 40)
        self.line_1.move(430, 200)

        self.line_2 = QLineEdit(self)  # 文件名
        self.line_2.resize(200, 40)
        self.line_2.move(430, 300)

        self.text_1 = QTextEdit(self)  # 音频地址
        self.text_1.move(430, 400)

        self.text_2 = QTextEdit(self)  # 下载进度
        self.text_2.move(430, 600)

        self.btn = QPushButton('立即下载', self)
        self.btn.setFont(QFont('SimSun', 10, 75))
        self.btn.resize(150, 80)
        self.btn.move(750, 235)

        # 在 mainwindow 类的构造函数中创建了一个 WorkerThread 对象（在主线程中创建一个子线程对象）
        self.worker_thread = WorkerThread()
        # 绑定按钮事件
        self.btn.clicked.connect(self.start_thread)
        # 将子线程的 finish 信号连接到主线程的 value_change 槽函数上
        self.worker_thread.finish.connect(self.value_change)

    def start_thread(self):
        # 获取文本框内容
        self.worker_thread.text1 = self.line_1.text()
        self.worker_thread.text2 = self.line_2.text()
        # 我们使用 moveToThread 方法将 worker_thread 移动到一个新的线程中(即子线程中)
        # 将主线程中text1、text2的值传递到子线程中
        self.worker_thread.moveToThread(self.worker_thread)
        # 启动子线程
        self.worker_thread.start()

    def value_change(self, value1, value2):
        # 在槽函数中获取子线程传递的结果，并进行处理
        self.text_1.setText(value1)
        self.text_2.setPlainText(value2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = mainwindow()
    a.show()
    sys.exit(app.exec_())
