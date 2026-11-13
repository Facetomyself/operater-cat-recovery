# Recovered module: src.resource.ui.dyna.down_load_flow_item
#
# The original Qt Designer .ui file is not shipped in the distribution.
# Widget names and types are recovered from the dialog widget map and the
# Nuitka constants chunk. The layout is a behaviour-level reconstruction.
from __future__ import annotations

from PyQt5 import QtCore, QtWidgets


FORM_TITLE = '编辑下载流'

WATER_MODE_PIC = '图片水印'
WATER_MODE_TEXT = '文字水印'
YULAN_MODE_PRESENT_TEXT = '按比例模式'
YULAN_MODE_DURATION_TEXT = '自定义时长模式'
MESSAGE_NUMBER_DAN_WEI_GROUP_TEXT = '按组计算'
MESSAGE_NUMBER_DAN_WEI_SINGLE_TEXT = '按个计算'
MODE_RANDOM_TEXT = '随机模式'
MODE_INCREASE_TEXT = '顺序模式'
MODE_LOOP_TEXT = '循环模式'


def _pretty(name: str) -> str:
    for prefix in (
        'horizontalGroupBox_', 'checkBox_', 'radioButton_', 'comboBox_',
        'lineEdit_', 'textEdit_', 'listWidget_', 'groupBox_', 'label_',
        'btn_', 'dl_', 'cb_',
    ):
        if name.startswith(prefix):
            name = name[len(prefix):]
            break
    return name.replace('_', ' ').strip() or 'field'


def _configure_combo(name: str, combo) -> None:
    lower = name.lower()
    if 'water_mode' in lower:
        combo.addItems([WATER_MODE_PIC, WATER_MODE_TEXT])
    elif 'select_yulan_mode' in lower or 'select_auto_flow_mode' in lower:
        combo.addItems([YULAN_MODE_PRESENT_TEXT, YULAN_MODE_DURATION_TEXT])
    elif 'video_minute' in lower:
        for text, value in (
            ('不限制', 0), ('15分钟', 15), ('30分钟', 30), ('60分钟', 60),
        ):
            combo.addItem(text, value)
        combo.setCurrentIndex(3)
    elif 'number_dan_wei' in lower or 'number_random_dan_wei' in lower:
        combo.addItems([MESSAGE_NUMBER_DAN_WEI_GROUP_TEXT, MESSAGE_NUMBER_DAN_WEI_SINGLE_TEXT])
    elif 'select_mode' in lower:
        combo.addItems([MODE_RANDOM_TEXT, MODE_INCREASE_TEXT, MODE_LOOP_TEXT])


def _make_widget(name: str, parent):
    kind = _TYPE_MAP.get(name, 'QWidget')
    if kind == 'QTextEdit':
        widget = QtWidgets.QTextEdit(parent)
        widget.setMinimumHeight(64)
    elif kind == 'QTextBrowser':
        widget = QtWidgets.QTextBrowser(parent)
    elif kind == 'QComboBox':
        widget = QtWidgets.QComboBox(parent)
        _configure_combo(name, widget)
    elif kind == 'QCheckBox':
        widget = QtWidgets.QCheckBox(_pretty(name), parent)
    elif kind == 'QRadioButton':
        widget = QtWidgets.QRadioButton(_pretty(name), parent)
    elif kind == 'QListWidget':
        widget = QtWidgets.QListWidget(parent)
        widget.setMinimumHeight(80)
    elif kind == 'QLineEdit':
        widget = QtWidgets.QLineEdit(parent)
        widget.setPlaceholderText(_pretty(name))
    elif kind == 'QPushButton':
        widget = QtWidgets.QPushButton(_pretty(name), parent)
    elif kind == 'QLabel':
        widget = QtWidgets.QLabel(_pretty(name), parent)
        widget.setWordWrap(True)
    elif kind == 'QGroupBox':
        widget = QtWidgets.QGroupBox(_pretty(name), parent)
    elif kind == 'QTabWidget':
        widget = QtWidgets.QTabWidget(parent)
    elif kind == 'QScrollArea':
        widget = QtWidgets.QScrollArea(parent)
        widget.setWidgetResizable(True)
    elif kind == 'QAction':
        widget = QtWidgets.QAction(_pretty(name), parent)
    elif kind == 'QMenu':
        widget = QtWidgets.QMenu(_pretty(name), parent)
    elif kind == 'QMenuBar':
        widget = QtWidgets.QMenuBar(parent)
    elif kind == 'QStatusBar':
        widget = QtWidgets.QStatusBar(parent)
    else:
        widget = QtWidgets.QWidget(parent)
    widget.setObjectName(name)
    for method, size in _SIZE_CONSTRAINTS.get(name, {}).items():
        getattr(widget, method)(QtCore.QSize(*size))
    return widget


_TYPE_MAP = {
    'btn_save_dl_item': 'QPushButton',
    'btn_dl_water_pic_jiao_chen': 'QPushButton',
    'btn_dl_water_select_pic': 'QPushButton',
    'down_load_res_btn_jiao_chen': 'QPushButton',
    'down_load_topic_jiao_chen': 'QPushButton',
    'label_dl_water_pic_path': 'QLabel',
    'dl_lineEdit_source': 'QLineEdit',
    'dl_lineEdit_random_want_count': 'QLineEdit',
    'dl_lineEdit_increase_start_id': 'QLineEdit',
    'dl_lineEdit_increase_want_count': 'QLineEdit',
    'dl_lineEdit_loop_start_id': 'QLineEdit',
    'dl_lineEdit_loop_end_id': 'QLineEdit',
    'dl_lineEdit_fliter_words_contain': 'QLineEdit',
    'dl_lineEdit_fliter_words_exclude': 'QLineEdit',
    'dl_lineEdit_water_text': 'QLineEdit',
    'lineEdit_dl_name': 'QLineEdit',
    'dl_checkBox_video_photo': 'QCheckBox',
    'dl_checkBox_photo': 'QCheckBox',
    'dl_checkBox_video': 'QCheckBox',
    'dl_checkBox_file': 'QCheckBox',
    'dl_checkBox_pic_water': 'QCheckBox',
    'dl_checkBox_video_water': 'QCheckBox',
    'dl_comboBox_select_mode': 'QComboBox',
    'dl_comboBox_number_dan_wei': 'QComboBox',
    'dl_comboBox_number_random_dan_wei': 'QComboBox',
    'dl_comboBox_video_minute': 'QComboBox',
    'cb_dl_water_mode': 'QComboBox',
    'lineEdit_down_load_duration_min': 'QLineEdit',
    'lineEdit_down_load_duration_max': 'QLineEdit',
    'lineEdit_down_load_mb_min': 'QLineEdit',
    'lineEdit_down_load_mb_max': 'QLineEdit',
    'lineEdit_priority': 'QLineEdit',
    'line_edit_dl_water_pic_ratio': 'QLineEdit',
    'text_model': 'QLineEdit',
    'number_model': 'QLineEdit',
    'text_water_wrapper': 'QGroupBox',
    'pic_water_wrapper': 'QGroupBox',
    'dl_random_com': 'QGroupBox',
    'dl_increase_com': 'QGroupBox',
    'dl_loop_com': 'QGroupBox',
    'verticalGroupBox_4': 'QGroupBox',
    'label': 'QLabel',
    'ziyuanleiixing': 'QGroupBox',
    'moshi_xuanze': 'QGroupBox',
    'label_3': 'QLabel',
    'label_7': 'QLabel',
    'label_6': 'QLabel',
    'label_8': 'QLabel',
    'label_5': 'QLabel',
    'jichu_filter': 'QWidget',
    'label_4': 'QLabel',
    'label_10': 'QLabel',
    'label_9': 'QLabel',
    'label_11': 'QLabel',
    'ziyuanguolu': 'QWidget',
    'label_15': 'QLabel',
    'label_151': 'QLabel',
    'verticalGroupBox': 'QWidget',
    'label_12': 'QLabel',
    'line': 'QFrame',
}


_SIZE_CONSTRAINTS = {
    'btn_save_dl_item': {'setMaximumSize': [16777215, 40]},
    'dl_increase_com': {'setMaximumSize': [16777215, 40]},
    'dl_loop_com': {'setMaximumSize': [16777215, 50]},
    'dl_random_com': {'setMaximumSize': [16777215, 40]},
    'lineEdit_dl_name': {'setMinimumSize': [0, 0], 'setMaximumSize': [16777215, 40]},
    'lineEdit_priority': {'setMaximumSize': [60, 40]},
    'pic_water_wrapper': {'setMaximumSize': [30, 16777215]},
    'verticalGroupBox_4': {'setMaximumSize': [16777215, 16777215], 'setMinimumSize': [30, 0]},
    'ziyuanleiixing': {'setMinimumSize': [30, 0]},
}


SETUP_ORDER = (
    'dl_lineEdit_source',
    'down_load_topic_jiao_chen',
    'dl_checkBox_video_photo',
    'dl_checkBox_photo',
    'dl_checkBox_video',
    'dl_checkBox_file',
    'down_load_res_btn_jiao_chen',
    'dl_comboBox_select_mode',
    'dl_random_com',
    'dl_lineEdit_random_want_count',
    'dl_comboBox_number_random_dan_wei',
    'dl_increase_com',
    'dl_lineEdit_increase_start_id',
    'dl_lineEdit_increase_want_count',
    'dl_comboBox_number_dan_wei',
    'dl_loop_com',
    'dl_lineEdit_loop_start_id',
    'dl_lineEdit_loop_end_id',
    'lineEdit_down_load_duration_min',
    'lineEdit_down_load_duration_max',
    'lineEdit_down_load_mb_min',
    'lineEdit_down_load_mb_max',
    'dl_lineEdit_fliter_words_contain',
    'dl_lineEdit_fliter_words_exclude',
    'dl_checkBox_pic_water',
    'dl_checkBox_video_water',
    'dl_comboBox_video_minute',
    'cb_dl_water_mode',
    'text_water_wrapper',
    'dl_lineEdit_water_text',
    'pic_water_wrapper',
    'btn_dl_water_pic_jiao_chen',
    'btn_dl_water_select_pic',
    'line_edit_dl_water_pic_ratio',
    'label_dl_water_pic_path',
    'lineEdit_priority',
    'lineEdit_dl_name',
    'btn_save_dl_item',
    'text_model',
    'number_model',
    'verticalGroupBox_4',
    'label',
    'ziyuanleiixing',
    'moshi_xuanze',
    'label_3',
    'label_7',
    'label_6',
    'label_8',
    'label_5',
    'jichu_filter',
    'label_4',
    'label_10',
    'label_9',
    'label_11',
    'ziyuanguolu',
    'label_15',
    'label_151',
    'verticalGroupBox',
    'label_12',
    'line',
)


class Ui_Form:
    def setupUi(self, Form):
        Form.setObjectName('Form')
        Form.resize(822, 606)
        Form.setStyleSheet('*{\nbackground-color:#3c3f42;\ncolor: #e6e6e6;\n}\n\n*:disabled {\n    background-color: #3c3f42;\n    color: #afafaf;\n    cursor: not-allowed;\n\n}\nQListWidget:disabled,QTextEdit:disabled,QLineEdit:disabled,QTabWidget:disabled{\nbackground-color:rgb(40, 40, 40);\n}\nQTextBrowser:disabled{\nbackground-color:rgb(40, 40, 40);\ncolor: rgb(152, 197, 150);\n}\n\nQPushButton:disabled {\n    background-color: rgb(80, 80, 80);\n    color: #afafaf;\n    cursor: not-allowed;\n\n}\n\nQCheckBox:hover,QRadioButton:hover {\ncolor: white;\n}\n\nQPushButton:hover {\n\nfont-weight: bold;\nbackground-color:rgb(84, 84, 84);\ncolor: white;\nborder-radius: 2pt;\n\n}\n\nQPushButton{\nfont-weight: bold;\nbackground-color:rgb(106, 106, 106);\ncolor: #e6e6e6;\nborder-radius: 2pt;\n}\n\nQTextBrowser,QListWidget,QTextEdit,QTabWidget{\nbackground-color:rgb(40, 40, 40);\ncolor: rgba(152, 197, 150, 185);\nfont-size:10pt;\n}\n\nQTextBrowser:hover,QTextEdit:hover{\nbackground-color:rgb(40, 40, 40);\ncolor: rgb(152, 197, 150);\nfont-size:10pt;\n}\n\nQLineEdit{\nbackground-color:rgb(40, 40, 40);\ncolor: rgba(152, 197, 150, 185);\nfont-size:12pt;\n}\n\nQLineEdit:hover{\nbackground-color:rgb(40, 40, 40);\ncolor: rgb(152, 197, 150);\nfont-size:12pt;\n}\n\n\nQLabel{\ncolor: #ebf905;\n}\n\n\n\nQRadioButton,QCheckBox {\n        border: none;\n        border-radius: 9px;\n}\nQRadioButton::indicator,QCheckBox::indicator{\n    background-color: rgb(42, 45, 66);\n    border: 0px solid #b1b1b1;\n    width: 18px;\n    height: 18px;\n    border-radius: 9px;\n}\n\nQRadioButton::indicator:checked,QCheckBox::indicator:checked {\n    background-color: #ebf905;\n    border-color: #ebf905;\n}\n\nQMenuBar { background-color: transparent; }\nQMenuBar::item { background-color: transparent; }\nQMenuBar::item:selected { background-color:transparent; color: #ffffff;}\nQMenu { background-color: transparent; }\nQMenu::item { background-color: transparent; }\nQMenu::item:selected { background-color: transparent; color: #ffffff; }\nQToolTip {\n                background-color: #3c3f42;\n                color: #e0e0e0;\n                border: 1px solid #666;\n                border-radius: 4px;\n                padding: 6px;\n                font-size: 13px;\n            }\n\n')

        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName('horizontalLayout')
        Form.setLayout(self.horizontalLayout)
        self.zuobian = QtWidgets.QVBoxLayout()
        self.zuobian.setObjectName('zuobian')
        self.horizontalLayout.addLayout(self.zuobian)
        self.verticalGroupBox_4 = _make_widget('verticalGroupBox_4', Form)
        self.zuobian.addWidget(self.verticalGroupBox_4)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName('verticalLayout_4')
        self.verticalGroupBox_4.setLayout(self.verticalLayout_4)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName('horizontalLayout_10')
        self.verticalLayout_4.addLayout(self.horizontalLayout_10)
        self.label = _make_widget('label', Form)
        self.horizontalLayout_10.addWidget(self.label)
        self.dl_lineEdit_source = _make_widget('dl_lineEdit_source', Form)
        self.horizontalLayout_10.addWidget(self.dl_lineEdit_source)
        self.down_load_topic_jiao_chen = _make_widget('down_load_topic_jiao_chen', Form)
        self.horizontalLayout_10.addWidget(self.down_load_topic_jiao_chen)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName('verticalLayout_9')
        self.verticalLayout_4.addLayout(self.verticalLayout_9)
        self.ziyuanleiixing = _make_widget('ziyuanleiixing', Form)
        self.zuobian.addWidget(self.ziyuanleiixing)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName('horizontalLayout_8')
        self.ziyuanleiixing.setLayout(self.horizontalLayout_8)
        self.dl_checkBox_video_photo = _make_widget('dl_checkBox_video_photo', Form)
        self.horizontalLayout_8.addWidget(self.dl_checkBox_video_photo)
        self.dl_checkBox_photo = _make_widget('dl_checkBox_photo', Form)
        self.horizontalLayout_8.addWidget(self.dl_checkBox_photo)
        self.dl_checkBox_video = _make_widget('dl_checkBox_video', Form)
        self.horizontalLayout_8.addWidget(self.dl_checkBox_video)
        self.dl_checkBox_file = _make_widget('dl_checkBox_file', Form)
        self.horizontalLayout_8.addWidget(self.dl_checkBox_file)
        self.down_load_res_btn_jiao_chen = _make_widget('down_load_res_btn_jiao_chen', Form)
        self.horizontalLayout_8.addWidget(self.down_load_res_btn_jiao_chen)
        self.moshi_xuanze = _make_widget('moshi_xuanze', Form)
        self.zuobian.addWidget(self.moshi_xuanze)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName('verticalLayout')
        self.moshi_xuanze.setLayout(self.verticalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName('verticalLayout_3')
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.dl_random_com = _make_widget('dl_random_com', Form)
        self.verticalLayout_3.addWidget(self.dl_random_com)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName('horizontalLayout_11')
        self.dl_random_com.setLayout(self.horizontalLayout_11)
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_20.setObjectName('horizontalLayout_20')
        self.horizontalLayout_11.addLayout(self.horizontalLayout_20)
        self.label_3 = _make_widget('label_3', Form)
        self.horizontalLayout_20.addWidget(self.label_3)
        self.dl_lineEdit_random_want_count = _make_widget('dl_lineEdit_random_want_count', Form)
        self.horizontalLayout_20.addWidget(self.dl_lineEdit_random_want_count)
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setObjectName('horizontalLayout_21')
        self.horizontalLayout_11.addLayout(self.horizontalLayout_21)
        self.dl_comboBox_number_random_dan_wei = _make_widget('dl_comboBox_number_random_dan_wei', Form)
        self.horizontalLayout_21.addWidget(self.dl_comboBox_number_random_dan_wei)
        self.dl_increase_com = _make_widget('dl_increase_com', Form)
        self.verticalLayout_3.addWidget(self.dl_increase_com)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName('horizontalLayout_2')
        self.dl_increase_com.setLayout(self.horizontalLayout_2)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName('horizontalLayout_13')
        self.horizontalLayout_2.addLayout(self.horizontalLayout_13)
        self.label_7 = _make_widget('label_7', Form)
        self.horizontalLayout_13.addWidget(self.label_7)
        self.dl_lineEdit_increase_start_id = _make_widget('dl_lineEdit_increase_start_id', Form)
        self.horizontalLayout_13.addWidget(self.dl_lineEdit_increase_start_id)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName('horizontalLayout_12')
        self.horizontalLayout_2.addLayout(self.horizontalLayout_12)
        self.label_6 = _make_widget('label_6', Form)
        self.horizontalLayout_12.addWidget(self.label_6)
        self.dl_lineEdit_increase_want_count = _make_widget('dl_lineEdit_increase_want_count', Form)
        self.horizontalLayout_12.addWidget(self.dl_lineEdit_increase_want_count)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName('horizontalLayout_9')
        self.horizontalLayout_2.addLayout(self.horizontalLayout_9)
        self.dl_comboBox_number_dan_wei = _make_widget('dl_comboBox_number_dan_wei', Form)
        self.horizontalLayout_9.addWidget(self.dl_comboBox_number_dan_wei)
        self.dl_loop_com = _make_widget('dl_loop_com', Form)
        self.verticalLayout_3.addWidget(self.dl_loop_com)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName('horizontalLayout_4')
        self.dl_loop_com.setLayout(self.horizontalLayout_4)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName('horizontalLayout_15')
        self.horizontalLayout_4.addLayout(self.horizontalLayout_15)
        self.label_8 = _make_widget('label_8', Form)
        self.horizontalLayout_15.addWidget(self.label_8)
        self.dl_lineEdit_loop_start_id = _make_widget('dl_lineEdit_loop_start_id', Form)
        self.horizontalLayout_15.addWidget(self.dl_lineEdit_loop_start_id)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName('horizontalLayout_14')
        self.horizontalLayout_4.addLayout(self.horizontalLayout_14)
        self.label_5 = _make_widget('label_5', Form)
        self.horizontalLayout_14.addWidget(self.label_5)
        self.dl_lineEdit_loop_end_id = _make_widget('dl_lineEdit_loop_end_id', Form)
        self.horizontalLayout_14.addWidget(self.dl_lineEdit_loop_end_id)
        self.dl_comboBox_select_mode = _make_widget('dl_comboBox_select_mode', Form)
        self.verticalLayout.addWidget(self.dl_comboBox_select_mode)
        self.jichu_filter = _make_widget('jichu_filter', Form)
        self.zuobian.addWidget(self.jichu_filter)
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName('verticalLayout_11')
        self.jichu_filter.setLayout(self.verticalLayout_11)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName('horizontalLayout_5')
        self.verticalLayout_11.addLayout(self.horizontalLayout_5)
        self.label_4 = _make_widget('label_4', Form)
        self.horizontalLayout_5.addWidget(self.label_4)
        self.lineEdit_down_load_duration_min = _make_widget('lineEdit_down_load_duration_min', Form)
        self.horizontalLayout_5.addWidget(self.lineEdit_down_load_duration_min)
        self.label_10 = _make_widget('label_10', Form)
        self.horizontalLayout_5.addWidget(self.label_10)
        self.lineEdit_down_load_duration_max = _make_widget('lineEdit_down_load_duration_max', Form)
        self.horizontalLayout_5.addWidget(self.lineEdit_down_load_duration_max)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName('horizontalLayout_6')
        self.verticalLayout_11.addLayout(self.horizontalLayout_6)
        self.label_9 = _make_widget('label_9', Form)
        self.horizontalLayout_6.addWidget(self.label_9)
        self.lineEdit_down_load_mb_min = _make_widget('lineEdit_down_load_mb_min', Form)
        self.horizontalLayout_6.addWidget(self.lineEdit_down_load_mb_min)
        self.label_11 = _make_widget('label_11', Form)
        self.horizontalLayout_6.addWidget(self.label_11)
        self.lineEdit_down_load_mb_max = _make_widget('lineEdit_down_load_mb_max', Form)
        self.horizontalLayout_6.addWidget(self.lineEdit_down_load_mb_max)
        self.ziyuanguolu = _make_widget('ziyuanguolu', Form)
        self.zuobian.addWidget(self.ziyuanguolu)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName('verticalLayout_5')
        self.ziyuanguolu.setLayout(self.verticalLayout_5)
        self.baohanci = QtWidgets.QHBoxLayout()
        self.baohanci.setObjectName('baohanci')
        self.verticalLayout_5.addLayout(self.baohanci)
        self.label_15 = _make_widget('label_15', Form)
        self.baohanci.addWidget(self.label_15)
        self.dl_lineEdit_fliter_words_contain = _make_widget('dl_lineEdit_fliter_words_contain', Form)
        self.baohanci.addWidget(self.dl_lineEdit_fliter_words_contain)
        self.paichuci = QtWidgets.QHBoxLayout()
        self.paichuci.setObjectName('paichuci')
        self.verticalLayout_5.addLayout(self.paichuci)
        self.label_151 = _make_widget('label_151', Form)
        self.paichuci.addWidget(self.label_151)
        self.dl_lineEdit_fliter_words_exclude = _make_widget('dl_lineEdit_fliter_words_exclude', Form)
        self.paichuci.addWidget(self.dl_lineEdit_fliter_words_exclude)
        self.youbian = QtWidgets.QVBoxLayout()
        self.youbian.setObjectName('youbian')
        self.horizontalLayout.addLayout(self.youbian)
        self.anniu_qu = QtWidgets.QVBoxLayout()
        self.anniu_qu.setObjectName('anniu_qu')
        self.youbian.addLayout(self.anniu_qu)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName('horizontalLayout_3')
        self.anniu_qu.addLayout(self.horizontalLayout_3)
        self.lineEdit_priority = _make_widget('lineEdit_priority', Form)
        self.horizontalLayout_3.addWidget(self.lineEdit_priority)
        self.lineEdit_dl_name = _make_widget('lineEdit_dl_name', Form)
        self.horizontalLayout_3.addWidget(self.lineEdit_dl_name)
        self.btn_save_dl_item = _make_widget('btn_save_dl_item', Form)
        self.anniu_qu.addWidget(self.btn_save_dl_item)
        self.verticalGroupBox = _make_widget('verticalGroupBox', Form)
        self.youbian.addWidget(self.verticalGroupBox)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName('verticalLayout_10')
        self.verticalGroupBox.setLayout(self.verticalLayout_10)
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName('horizontalLayout_18')
        self.verticalLayout_10.addLayout(self.horizontalLayout_18)
        self.dl_checkBox_pic_water = _make_widget('dl_checkBox_pic_water', Form)
        self.horizontalLayout_18.addWidget(self.dl_checkBox_pic_water)
        self.dl_checkBox_video_water = _make_widget('dl_checkBox_video_water', Form)
        self.horizontalLayout_18.addWidget(self.dl_checkBox_video_water)
        self.dl_comboBox_video_minute = _make_widget('dl_comboBox_video_minute', Form)
        self.horizontalLayout_18.addWidget(self.dl_comboBox_video_minute)
        self.cb_dl_water_mode = _make_widget('cb_dl_water_mode', Form)
        self.horizontalLayout_18.addWidget(self.cb_dl_water_mode)
        self.label_12 = _make_widget('label_12', Form)
        self.verticalLayout_10.addWidget(self.label_12)
        self.text_water_wrapper = _make_widget('text_water_wrapper', Form)
        self.verticalLayout_10.addWidget(self.text_water_wrapper)
        self.text_water_wrapper_xx = QtWidgets.QVBoxLayout()
        self.text_water_wrapper_xx.setObjectName('text_water_wrapper_xx')
        self.text_water_wrapper.setLayout(self.text_water_wrapper_xx)
        self.dl_lineEdit_water_text = _make_widget('dl_lineEdit_water_text', Form)
        self.text_water_wrapper_xx.addWidget(self.dl_lineEdit_water_text)
        self.pic_water_wrapper = _make_widget('pic_water_wrapper', Form)
        self.verticalLayout_10.addWidget(self.pic_water_wrapper)
        self.pic_water_wrapper_xx = QtWidgets.QHBoxLayout()
        self.pic_water_wrapper_xx.setObjectName('pic_water_wrapper_xx')
        self.pic_water_wrapper.setLayout(self.pic_water_wrapper_xx)
        self.btn_dl_water_pic_jiao_chen = _make_widget('btn_dl_water_pic_jiao_chen', Form)
        self.pic_water_wrapper_xx.addWidget(self.btn_dl_water_pic_jiao_chen)
        self.btn_dl_water_select_pic = _make_widget('btn_dl_water_select_pic', Form)
        self.pic_water_wrapper_xx.addWidget(self.btn_dl_water_select_pic)
        self.line_edit_dl_water_pic_ratio = _make_widget('line_edit_dl_water_pic_ratio', Form)
        self.pic_water_wrapper_xx.addWidget(self.line_edit_dl_water_pic_ratio)
        self.label_dl_water_pic_path = _make_widget('label_dl_water_pic_path', Form)
        self.pic_water_wrapper_xx.addWidget(self.label_dl_water_pic_path)
        self.line = _make_widget('line', Form)
        self.horizontalLayout.addWidget(self.line)
        self.number_model = _make_widget('number_model', Form)
        self.horizontalLayout.addWidget(self.number_model)
        self.text_model = _make_widget('text_model', Form)
        self.horizontalLayout.addWidget(self.text_model)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate('Form', FORM_TITLE))
        self.verticalGroupBox_4.setTitle(_translate('Form', '基础'))
        self.label.setText(_translate('Form', '来源频道/群组'))
        self.dl_lineEdit_source.setPlaceholderText(_translate('Form', '公有链接或私有ID(支持话题)'))
        self.down_load_topic_jiao_chen.setText(_translate('Form', '教程'))
        self.ziyuanleiixing.setTitle(_translate('Form', '资源类型'))
        self.dl_checkBox_video_photo.setText(_translate('Form', '仅包含视频的消息组'))
        self.dl_checkBox_photo.setText(_translate('Form', '图片'))
        self.dl_checkBox_video.setText(_translate('Form', '视频'))
        self.dl_checkBox_file.setText(_translate('Form', '文件'))
        self.down_load_res_btn_jiao_chen.setText(_translate('Form', '教程'))
        self.moshi_xuanze.setTitle(_translate('Form', '模式选择'))
        self.dl_comboBox_select_mode.setItemText(0, _translate('Form', '顺序模式'))
        self.dl_comboBox_select_mode.setItemText(1, _translate('Form', '随机模式'))
        self.dl_comboBox_select_mode.setItemText(2, _translate('Form', '循环模式'))
        self.dl_random_com.setTitle(_translate('Form', '随机模式参数'))
        self.label_3.setText(_translate('Form', '期望数量'))
        self.dl_lineEdit_random_want_count.setPlaceholderText(_translate('Form', '填写整数'))
        self.dl_comboBox_number_random_dan_wei.setItemText(0, _translate('Form', '按组计算'))
        self.dl_comboBox_number_random_dan_wei.setItemText(1, _translate('Form', '按个计算'))
        self.dl_increase_com.setTitle(_translate('Form', '顺序模式参数（包括开始ID）'))
        self.label_7.setText(_translate('Form', '开始ID'))
        self.dl_lineEdit_increase_start_id.setPlaceholderText(_translate('Form', '填写整数'))
        self.label_6.setText(_translate('Form', '期望数量'))
        self.dl_lineEdit_increase_want_count.setPlaceholderText(_translate('Form', '填写整数'))
        self.dl_comboBox_number_dan_wei.setCurrentText(_translate('Form', '按组计算'))
        self.dl_comboBox_number_dan_wei.setItemText(0, _translate('Form', '按组计算'))
        self.dl_comboBox_number_dan_wei.setItemText(1, _translate('Form', '按个计算'))
        self.dl_loop_com.setTitle(_translate('Form', '循环模式参数（包括开始ID，不包括结束ID）'))
        self.label_8.setText(_translate('Form', '开始ID'))
        self.dl_lineEdit_loop_start_id.setPlaceholderText(_translate('Form', '填写整数'))
        self.label_5.setText(_translate('Form', '结束ID'))
        self.dl_lineEdit_loop_end_id.setPlaceholderText(_translate('Form', '填写整数'))
        self.jichu_filter.setTitle(_translate('Form', '基础条件(如果是视频资源，则需要同时满足时长和大小)'))
        self.label_4.setText(_translate('Form', '时长过滤(单位分钟)：'))
        self.lineEdit_down_load_duration_min.setPlaceholderText(_translate('Form', '最小值'))
        self.label_10.setText(_translate('Form', '~'))
        self.lineEdit_down_load_duration_max.setPlaceholderText(_translate('Form', '最大值'))
        self.label_9.setText(_translate('Form', '大小过滤(单位 MB )：'))
        self.lineEdit_down_load_mb_min.setPlaceholderText(_translate('Form', '最小值'))
        self.label_11.setText(_translate('Form', '~'))
        self.lineEdit_down_load_mb_max.setPlaceholderText(_translate('Form', '最大值'))
        self.ziyuanguolu.setTitle(_translate('Form', '资源过滤条件'))
        self.label_15.setText(_translate('Form', '包含关键词的资源'))
        self.dl_lineEdit_fliter_words_contain.setPlaceholderText(_translate('Form', '填写关键词，多个词使用竖线"|"分割'))
        self.label_151.setText(_translate('Form', '排除关键词的资源'))
        self.dl_lineEdit_fliter_words_exclude.setPlaceholderText(_translate('Form', '填写关键词，多个词使用竖线"|"分割'))
        self.verticalGroupBox.setTitle(_translate('Form', '水印（可选）'))
        self.label_12.setText(_translate('Form', '图片水印或者视频动态水印'))
        self.dl_checkBox_pic_water.setText(_translate('Form', '图片水印'))
        self.dl_checkBox_video_water.setText(_translate('Form', '视频水印'))
        self.dl_comboBox_video_minute.setItemText(0, _translate('Form', '1分钟内视频'))
        self.dl_comboBox_video_minute.setItemText(1, _translate('Form', '3分钟内视频'))
        self.dl_comboBox_video_minute.setItemText(2, _translate('Form', '5分钟内视频'))
        self.dl_comboBox_video_minute.setItemText(3, _translate('Form', '10分钟内视频'))
        self.dl_comboBox_video_minute.setItemText(4, _translate('Form', '30分钟内视频'))
        self.dl_comboBox_video_minute.setItemText(5, _translate('Form', '60分钟内视频'))
        self.dl_comboBox_video_minute.setItemText(6, _translate('Form', '90分钟内视频'))
        self.dl_comboBox_video_minute.setItemText(7, _translate('Form', '120分钟内视频'))
        self.dl_comboBox_video_minute.setItemText(8, _translate('Form', '150分钟内视频'))
        self.cb_dl_water_mode.setItemText(0, _translate('Form', '图片水印'))
        self.cb_dl_water_mode.setItemText(1, _translate('Form', '文字水印'))
        self.dl_lineEdit_water_text.setPlaceholderText(_translate('Form', '水印文字，支持中文，英文'))
        self.btn_dl_water_pic_jiao_chen.setText(_translate('Form', '教程'))
        self.btn_dl_water_select_pic.setText(_translate('Form', '选择图片'))
        self.line_edit_dl_water_pic_ratio.setPlaceholderText(_translate('Form', '30'))
        self.label_dl_water_pic_path.setText(_translate('Form', '图片路径：'))
        self.lineEdit_priority.setPlaceholderText(_translate('Form', '优先级'))
        self.lineEdit_dl_name.setPlaceholderText(_translate('Form', '输入名字'))
        self.btn_save_dl_item.setText(_translate('Form', '保存'))

