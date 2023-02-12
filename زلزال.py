import sys
import obspy
from obspy import read
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox

class SeismicAnalysis(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # مكونات الواجهة الرسومية
        self.label_file_path = QLabel('مسار الملف الزلزالي:', self)
        self.label_file_path.move(10, 10)

        self.text_file_path = QLineEdit(self)
        self.text_file_path.move(150, 10)
        self.text_file_path.resize(300, 20)

        self.label_stations = QLabel('المحطات الزلزالية:', self)
        self.label_stations.move(10, 40)

        self.combo_stations = QComboBox(self)
        self.combo_stations.move(150, 40)
        self.combo_stations.resize(100, 20)

        self.label_min_freq = QLabel('الحد الأدنى للتردد:', self)
        self.label_min_freq.move(10, 70)

        self.text_min_freq = QLineEdit(self)
        self.text_min_freq.move(150, 70)
        self.text_min_freq.resize(100, 20)

        self.label_max_freq = QLabel('الحد الأعلى للتردد:', self)
        self.label_max_freq.move(10, 100)

        self.text_max_freq = QLineEdit(self)
        self.text_max_freq.move(150, 100)
        self.text_max_freq.resize(100, 20)

        self.button_load = QPushButton('تحميل الملف', self)
        self.button_load.move(460, 10)

        self.button_process = QPushButton('معالجة البيانات', self)
        self.button_process.move(460, 40)

        self.label_amplitude = QLabel('شدة الزلزال:', self)
        self.label_amplitude.move(10, 130)

        self.text_amplitude = QTextEdit(self)
        self.text_amplitude.move(150, 130)
        self.text_amplitude.resize(300, 100)

        # تحديد المحطات الزلزالية المتاحة
        self.stations = ['ABC', 'DEF', 'GHI']

        for station in self.stations:
            self.combo_stations.addItem(station)

        # الإشارات المستخدمة في تحليل الزلزال
        self.st = None

        # توصيل الأحداث بالدوال المناسبة
        self.button_load.clicked.connect(self.load_file)
        self.button_process.clicked.connect(self.process_data)

        # إعداد النافذة
        self.setGeometry(100, 100, 600, 250)
        self.setWindowTitle('تحليل الزلازل')
        self.show()

    # دالة لتحميل الملف الزلزالي
    def load_file(self):
        file_path = self.text_file_path.text()
        self.st = read
        self.combo_stations.currentText()
        
        # دالة لتحليل البيانات الزلزالية
    def process_data(self):
        if self.st is not None:
            # تحديد المحطة الزلزالية المحددة
            station = self.combo_stations.currentText()

            # تحديد المحطات الزلزالية المستخدمة
            st = self.st.select(station=station)

            # تحويل بيانات الزلزال إلى وحدات شدة الزلزال
            st = st.detrend("linear")
            st = st.taper(max_percentage=0.05, type="hann")

            # تحديد الحدود الزمنية
            t_start = st[0].stats.starttime
            t_end = st[0].stats.endtime
            duration = t_end - t_start

            # تصفية الإشارة الزلزالية
            min_freq = float(self.text_min_freq.text())
            max_freq = float(self.text_max_freq.text())
            st = st.filter("bandpass", freqmin=min_freq, freqmax=max_freq)

            # حساب شدة الزلزال باستخدام وظيفة Amplitude الخاصة بتكنتر
            max_gap = duration / 10
            amp = obspy.signal.amplitude.max_p2p(st[0].data, max_gap=max_gap)

            # طباعة شدة الزلزال
            self.text_amplitude.setText(str(amp))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SeismicAnalysis()
    sys.exit(app.exec_())
