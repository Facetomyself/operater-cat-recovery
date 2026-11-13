# Recovered module: src.resource.ui.dyna.ban_yun_flow_comment_item
#
# The original Qt Designer .ui file is not shipped in the distribution.
# Widget names and types are recovered from the dialog widget map and the
# Nuitka constants chunk. The layout is a behaviour-level reconstruction.
from __future__ import annotations

from PyQt5 import QtCore, QtWidgets


FORM_TITLE = '编辑搬运流'

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
    'btn_save_yun_yin_item': 'QPushButton',
    'btn_add_ad': 'QPushButton',
    'btn_config_comment_rule': 'QPushButton',
    'ban_yun_res_btn_jiao_chen': 'QPushButton',
    'btn_ban_yun_res_op_jiao_chen': 'QPushButton',
    'ban_yun_topic_jiao_chen': 'QPushButton',
    'btn_banyun_select_ai_em': 'QPushButton',
    'btn_banyun_water_pic_jiao_chen': 'QPushButton',
    'btn_banyun_water_select_pic': 'QPushButton',
    'btn_ban_yun_grid_jiao_chen': 'QPushButton',
    'ban_yun_cover_jiao_chen': 'QPushButton',
    'comboBox_number_dan_wei': 'QComboBox',
    'comboBox_number_random_dan_wei': 'QComboBox',
    'comboBox_select_mode': 'QComboBox',
    'cb_banyun_water_mode': 'QComboBox',
    'listWidget_private_ad_list': 'QListWidget',
    'checkBox_chai_zu': 'QCheckBox',
    'checkBox_origin_source_text': 'QCheckBox',
    'checkBox_ad_enable': 'QCheckBox',
    'checkBox_copy_comment': 'QCheckBox',
    'checkBox_video_photo': 'QCheckBox',
    'checkBox_banyun_ai_enable': 'QCheckBox',
    'horizontalGroupBox_ai_banyun': 'QGroupBox',
    'label_banyun_ai_name': 'QLabel',
    'checkBox_photo': 'QCheckBox',
    'checkBox_video': 'QCheckBox',
    'checkBox_file': 'QCheckBox',
    'checkBox_text': 'QCheckBox',
    'checkBox_dele_source_text': 'QCheckBox',
    'checkBox_dele_link': 'QCheckBox',
    'checkBox_fliter_button': 'QCheckBox',
    'checkBox_discard_no_text_resource': 'QCheckBox',
    'checkBox_pic_water': 'QCheckBox',
    'checkBox_video_water': 'QCheckBox',
    'checkBox_ad_is_bottom_up': 'QCheckBox',
    'checkBox_ad_delete': 'QCheckBox',
    'lineEdit_random_want_count': 'QLineEdit',
    'lineEdit_increase_start_id': 'QLineEdit',
    'lineEdit_increase_want_count': 'QLineEdit',
    'lineEdit_auto_sleep_min': 'QLineEdit',
    'lineEdit_auto_sleep_max': 'QLineEdit',
    'lineEdit_ban_yun_duration_min': 'QLineEdit',
    'lineEdit_ban_yun_duration_max': 'QLineEdit',
    'lineEdit_ban_yun_mb_min': 'QLineEdit',
    'lineEdit_ban_yun_mb_max': 'QLineEdit',
    'lineEdit_priority': 'QLineEdit',
    'lineEdit_source': 'QLineEdit',
    'lineEdit_fliter_words_contain': 'QLineEdit',
    'lineEdit_fliter_words_exclude': 'QLineEdit',
    'lineEdit_loop_start_id': 'QLineEdit',
    'lineEdit_loop_end_id': 'QLineEdit',
    'lineEdit_water_text': 'QLineEdit',
    'lineEdit_yun_yin_name': 'QLineEdit',
    'lineEdit_ban_yun_grid_number': 'QLineEdit',
    'line_edit_by_com_water_pic_ratio': 'QLineEdit',
    'radioButton_action_auto': 'QRadioButton',
    'radioButton_action_download': 'QRadioButton',
    'radioButton_ai_banyun_skip_source': 'QRadioButton',
    'radioButton_ai_banyun_use_source': 'QRadioButton',
    'label_banyun_water_pic_path': 'QLabel',
    'text_water_wrapper': 'QGroupBox',
    'pic_water_wrapper': 'QGroupBox',
    'text_model': 'QLineEdit',
    'number_model': 'QLineEdit',
    'textEdit_dest_list': 'QTextEdit',
    'textEdit_tail_text': 'QTextEdit',
    'textEdit_replace_rule': 'QTextEdit',
    'comboBox_video_minute': 'QComboBox',
    'ban_yun_pic_blur_radius': 'QLineEdit',
    'cb_ban_yun_spoiler': 'QCheckBox',
    'cb_ban_yun_pic_blur': 'QCheckBox',
    'cb_ban_yun_random_cover': 'QCheckBox',
    'random_com': 'QGroupBox',
    'increase_com': 'QGroupBox',
    'loop_com': 'QGroupBox',
    'jichu': 'QGroupBox',
    'label': 'QLabel',
    'label_2': 'QLabel',
    'ziyuanleiixing': 'QGroupBox',
    'moshi_xuanze': 'QGroupBox',
    'label_3': 'QLabel',
    'label_7': 'QLabel',
    'label_6': 'QLabel',
    'label_8': 'QLabel',
    'label_5': 'QLabel',
    'zhuanfa': 'QWidget',
    'label_14': 'QLabel',
    'jichu_filter': 'QWidget',
    'label_4': 'QLabel',
    'label_10': 'QLabel',
    'label_9': 'QLabel',
    'label_11': 'QLabel',
    'ziyuanguolu': 'QWidget',
    'label_15': 'QLabel',
    'label_151': 'QLabel',
    'verticalGroupBox_yulan_op': 'QWidget',
    'label_17': 'QLabel',
    'verticalGroupBox': 'QWidget',
    'label_12': 'QLabel',
    'verticalGroupBox1': 'QWidget',
    'weiba_qu': 'QGroupBox',
    'ai_employee_qu': 'QGroupBox',
    'label_13': 'QLabel',
    'pinlunqu': 'QWidget',
    'horizontalGroupBox_4': 'QGroupBox',
    'line': 'QFrame',
}


_SIZE_CONSTRAINTS = {
    'ai_employee_qu': {'setMinimumSize': [0, 25]},
    'btn_save_yun_yin_item': {'setMaximumSize': [16777215, 40]},
    'horizontalGroupBox_4': {'setMaximumSize': [16777215, 80]},
    'increase_com': {'setMaximumSize': [16777215, 40]},
    'jichu': {'setMaximumSize': [16777215, 70], 'setMinimumSize': [30, 0]},
    'lineEdit_priority': {'setMaximumSize': [60, 40]},
    'lineEdit_yun_yin_name': {'setMinimumSize': [0, 0], 'setMaximumSize': [16777215, 40]},
    'loop_com': {'setMaximumSize': [16777215, 50]},
    'pic_water_wrapper': {'setMaximumSize': [30, 16777215]},
    'pinlunqu': {'setMinimumSize': [0, 25]},
    'random_com': {'setMaximumSize': [16777215, 40]},
    'verticalGroupBox1': {'setMaximumSize': [16777215, 70]},
    'verticalGroupBox_yulan_op': {'setMaximumSize': [30, 16777215]},
    'weiba_qu': {'setMaximumSize': [16777215, 70]},
}


SETUP_ORDER = (
    'lineEdit_source',
    'ban_yun_topic_jiao_chen',
    'textEdit_dest_list',
    'checkBox_video_photo',
    'checkBox_photo',
    'checkBox_video',
    'checkBox_file',
    'checkBox_text',
    'ban_yun_res_btn_jiao_chen',
    'comboBox_select_mode',
    'random_com',
    'lineEdit_random_want_count',
    'comboBox_number_random_dan_wei',
    'increase_com',
    'lineEdit_increase_start_id',
    'lineEdit_increase_want_count',
    'comboBox_number_dan_wei',
    'loop_com',
    'lineEdit_loop_start_id',
    'lineEdit_loop_end_id',
    'radioButton_action_download',
    'radioButton_action_auto',
    'lineEdit_auto_sleep_min',
    'lineEdit_auto_sleep_max',
    'lineEdit_ban_yun_duration_min',
    'lineEdit_ban_yun_duration_max',
    'lineEdit_ban_yun_mb_min',
    'lineEdit_ban_yun_mb_max',
    'checkBox_dele_source_text',
    'checkBox_discard_no_text_resource',
    'checkBox_fliter_button',
    'checkBox_dele_link',
    'checkBox_origin_source_text',
    'checkBox_chai_zu',
    'lineEdit_fliter_words_contain',
    'lineEdit_fliter_words_exclude',
    'cb_ban_yun_pic_blur',
    'cb_ban_yun_spoiler',
    'btn_ban_yun_res_op_jiao_chen',
    'ban_yun_pic_blur_radius',
    'btn_ban_yun_grid_jiao_chen',
    'lineEdit_ban_yun_grid_number',
    'cb_ban_yun_random_cover',
    'ban_yun_cover_jiao_chen',
    'checkBox_pic_water',
    'checkBox_video_water',
    'comboBox_video_minute',
    'cb_banyun_water_mode',
    'text_water_wrapper',
    'lineEdit_water_text',
    'pic_water_wrapper',
    'btn_banyun_water_pic_jiao_chen',
    'btn_banyun_water_select_pic',
    'line_edit_by_com_water_pic_ratio',
    'label_banyun_water_pic_path',
    'textEdit_replace_rule',
    'textEdit_tail_text',
    'checkBox_banyun_ai_enable',
    'label_banyun_ai_name',
    'btn_banyun_select_ai_em',
    'horizontalGroupBox_ai_banyun',
    'radioButton_ai_banyun_use_source',
    'radioButton_ai_banyun_skip_source',
    'checkBox_copy_comment',
    'btn_config_comment_rule',
    'checkBox_ad_enable',
    'checkBox_ad_is_bottom_up',
    'checkBox_ad_delete',
    'btn_add_ad',
    'listWidget_private_ad_list',
    'lineEdit_priority',
    'lineEdit_yun_yin_name',
    'btn_save_yun_yin_item',
    'text_model',
    'number_model',
    'jichu',
    'label',
    'label_2',
    'ziyuanleiixing',
    'moshi_xuanze',
    'label_3',
    'label_7',
    'label_6',
    'label_8',
    'label_5',
    'zhuanfa',
    'label_14',
    'jichu_filter',
    'label_4',
    'label_10',
    'label_9',
    'label_11',
    'ziyuanguolu',
    'label_15',
    'label_151',
    'verticalGroupBox_yulan_op',
    'label_17',
    'verticalGroupBox',
    'label_12',
    'verticalGroupBox1',
    'weiba_qu',
    'ai_employee_qu',
    'label_13',
    'pinlunqu',
    'horizontalGroupBox_4',
    'line',
)


class Ui_Form:
    def setupUi(self, Form):
        Form.setObjectName('Form')
        Form.resize(860, 817)
        Form.setStyleSheet('*{\nbackground-color:#3c3f42;\ncolor: #e6e6e6;\n}\n\n*:disabled {\n    background-color: #3c3f42;\n    color: #afafaf;\n    cursor: not-allowed;\n\n}\nQListWidget:disabled,QTextEdit:disabled,QLineEdit:disabled,QTabWidget:disabled{\nbackground-color:rgb(40, 40, 40);\n}\nQTextBrowser:disabled{\nbackground-color:rgb(40, 40, 40);\ncolor: rgb(152, 197, 150);\n}\n\nQPushButton:disabled {\n    background-color: rgb(80, 80, 80);\n    color: #afafaf;\n    cursor: not-allowed;\n\n}\n\nQCheckBox:hover,QRadioButton:hover {\ncolor: white;\n}\n\nQPushButton:hover {\n\nfont-weight: bold;\nbackground-color:rgb(84, 84, 84);\ncolor: white;\nborder-radius: 2pt;\n\n}\n\nQPushButton{\nfont-weight: bold;\nbackground-color:rgb(106, 106, 106);\ncolor: #e6e6e6;\nborder-radius: 2pt;\n}\n\nQTextBrowser,QListWidget,QTextEdit,QTabWidget{\nbackground-color:rgb(40, 40, 40);\ncolor: rgba(152, 197, 150, 185);\nfont-size:10pt;\n}\n\nQTextBrowser:hover,QTextEdit:hover{\nbackground-color:rgb(40, 40, 40);\ncolor: rgb(152, 197, 150);\nfont-size:10pt;\n}\n\nQLineEdit{\nbackground-color:rgb(40, 40, 40);\ncolor: rgba(152, 197, 150, 185);\nfont-size:12pt;\n}\n\nQLineEdit:hover{\nbackground-color:rgb(40, 40, 40);\ncolor: rgb(152, 197, 150);\nfont-size:12pt;\n}\n\n\nQLabel{\ncolor: #ebf905;\n}\n\n\n\nQRadioButton,QCheckBox {\n        border: none;\n        border-radius: 9px;\n}\nQRadioButton::indicator,QCheckBox::indicator{\n    background-color: rgb(42, 45, 66);\n    border: 0px solid #b1b1b1;\n    width: 18px;\n    height: 18px;\n    border-radius: 9px;\n}\n\nQRadioButton::indicator:checked,QCheckBox::indicator:checked {\n    background-color: #ebf905;\n    border-color: #ebf905;\n}\n\nQMenuBar { background-color: transparent; }\nQMenuBar::item { background-color: transparent; }\nQMenuBar::item:selected { background-color:transparent; color: #ffffff;}\nQMenu { background-color: transparent; }\nQMenu::item { background-color: transparent; }\nQMenu::item:selected { background-color: transparent; color: #ffffff; }\nQToolTip {\n                background-color: #3c3f42;\n                color: #e0e0e0;\n                border: 1px solid #666;\n                border-radius: 4px;\n                padding: 6px;\n                font-size: 13px;\n            }\n\n')

        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName('horizontalLayout')
        Form.setLayout(self.horizontalLayout)
        self.zuobian = QtWidgets.QVBoxLayout()
        self.zuobian.setObjectName('zuobian')
        self.horizontalLayout.addLayout(self.zuobian)
        self.jichu = _make_widget('jichu', Form)
        self.zuobian.addWidget(self.jichu)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName('verticalLayout_4')
        self.jichu.setLayout(self.verticalLayout_4)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName('horizontalLayout_10')
        self.verticalLayout_4.addLayout(self.horizontalLayout_10)
        self.label = _make_widget('label', Form)
        self.horizontalLayout_10.addWidget(self.label)
        self.lineEdit_source = _make_widget('lineEdit_source', Form)
        self.horizontalLayout_10.addWidget(self.lineEdit_source)
        self.ban_yun_topic_jiao_chen = _make_widget('ban_yun_topic_jiao_chen', Form)
        self.horizontalLayout_10.addWidget(self.ban_yun_topic_jiao_chen)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName('verticalLayout_9')
        self.verticalLayout_4.addLayout(self.verticalLayout_9)
        self.label_2 = _make_widget('label_2', Form)
        self.verticalLayout_9.addWidget(self.label_2)
        self.textEdit_dest_list = _make_widget('textEdit_dest_list', Form)
        self.verticalLayout_9.addWidget(self.textEdit_dest_list)
        self.ziyuanleiixing = _make_widget('ziyuanleiixing', Form)
        self.zuobian.addWidget(self.ziyuanleiixing)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName('horizontalLayout_8')
        self.ziyuanleiixing.setLayout(self.horizontalLayout_8)
        self.checkBox_video_photo = _make_widget('checkBox_video_photo', Form)
        self.horizontalLayout_8.addWidget(self.checkBox_video_photo)
        self.checkBox_photo = _make_widget('checkBox_photo', Form)
        self.horizontalLayout_8.addWidget(self.checkBox_photo)
        self.checkBox_video = _make_widget('checkBox_video', Form)
        self.horizontalLayout_8.addWidget(self.checkBox_video)
        self.checkBox_file = _make_widget('checkBox_file', Form)
        self.horizontalLayout_8.addWidget(self.checkBox_file)
        self.checkBox_text = _make_widget('checkBox_text', Form)
        self.horizontalLayout_8.addWidget(self.checkBox_text)
        self.ban_yun_res_btn_jiao_chen = _make_widget('ban_yun_res_btn_jiao_chen', Form)
        self.horizontalLayout_8.addWidget(self.ban_yun_res_btn_jiao_chen)
        self.moshi_xuanze = _make_widget('moshi_xuanze', Form)
        self.zuobian.addWidget(self.moshi_xuanze)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName('verticalLayout')
        self.moshi_xuanze.setLayout(self.verticalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName('verticalLayout_3')
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.random_com = _make_widget('random_com', Form)
        self.verticalLayout_3.addWidget(self.random_com)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName('horizontalLayout_11')
        self.random_com.setLayout(self.horizontalLayout_11)
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_20.setObjectName('horizontalLayout_20')
        self.horizontalLayout_11.addLayout(self.horizontalLayout_20)
        self.label_3 = _make_widget('label_3', Form)
        self.horizontalLayout_20.addWidget(self.label_3)
        self.lineEdit_random_want_count = _make_widget('lineEdit_random_want_count', Form)
        self.horizontalLayout_20.addWidget(self.lineEdit_random_want_count)
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setObjectName('horizontalLayout_21')
        self.horizontalLayout_11.addLayout(self.horizontalLayout_21)
        self.comboBox_number_random_dan_wei = _make_widget('comboBox_number_random_dan_wei', Form)
        self.horizontalLayout_21.addWidget(self.comboBox_number_random_dan_wei)
        self.increase_com = _make_widget('increase_com', Form)
        self.verticalLayout_3.addWidget(self.increase_com)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName('horizontalLayout_2')
        self.increase_com.setLayout(self.horizontalLayout_2)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName('horizontalLayout_13')
        self.horizontalLayout_2.addLayout(self.horizontalLayout_13)
        self.label_7 = _make_widget('label_7', Form)
        self.horizontalLayout_13.addWidget(self.label_7)
        self.lineEdit_increase_start_id = _make_widget('lineEdit_increase_start_id', Form)
        self.horizontalLayout_13.addWidget(self.lineEdit_increase_start_id)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName('horizontalLayout_12')
        self.horizontalLayout_2.addLayout(self.horizontalLayout_12)
        self.label_6 = _make_widget('label_6', Form)
        self.horizontalLayout_12.addWidget(self.label_6)
        self.lineEdit_increase_want_count = _make_widget('lineEdit_increase_want_count', Form)
        self.horizontalLayout_12.addWidget(self.lineEdit_increase_want_count)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName('horizontalLayout_9')
        self.horizontalLayout_2.addLayout(self.horizontalLayout_9)
        self.comboBox_number_dan_wei = _make_widget('comboBox_number_dan_wei', Form)
        self.horizontalLayout_9.addWidget(self.comboBox_number_dan_wei)
        self.loop_com = _make_widget('loop_com', Form)
        self.verticalLayout_3.addWidget(self.loop_com)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName('horizontalLayout_4')
        self.loop_com.setLayout(self.horizontalLayout_4)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName('horizontalLayout_15')
        self.horizontalLayout_4.addLayout(self.horizontalLayout_15)
        self.label_8 = _make_widget('label_8', Form)
        self.horizontalLayout_15.addWidget(self.label_8)
        self.lineEdit_loop_start_id = _make_widget('lineEdit_loop_start_id', Form)
        self.horizontalLayout_15.addWidget(self.lineEdit_loop_start_id)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName('horizontalLayout_14')
        self.horizontalLayout_4.addLayout(self.horizontalLayout_14)
        self.label_5 = _make_widget('label_5', Form)
        self.horizontalLayout_14.addWidget(self.label_5)
        self.lineEdit_loop_end_id = _make_widget('lineEdit_loop_end_id', Form)
        self.horizontalLayout_14.addWidget(self.lineEdit_loop_end_id)
        self.comboBox_select_mode = _make_widget('comboBox_select_mode', Form)
        self.verticalLayout.addWidget(self.comboBox_select_mode)
        self.zhuanfa = _make_widget('zhuanfa', Form)
        self.zuobian.addWidget(self.zhuanfa)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName('horizontalLayout_7')
        self.zhuanfa.setLayout(self.horizontalLayout_7)
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_23.setObjectName('horizontalLayout_23')
        self.horizontalLayout_7.addLayout(self.horizontalLayout_23)
        self.lineEdit_auto_sleep_min = _make_widget('lineEdit_auto_sleep_min', Form)
        self.horizontalLayout_23.addWidget(self.lineEdit_auto_sleep_min)
        self.label_14 = _make_widget('label_14', Form)
        self.horizontalLayout_23.addWidget(self.label_14)
        self.lineEdit_auto_sleep_max = _make_widget('lineEdit_auto_sleep_max', Form)
        self.horizontalLayout_23.addWidget(self.lineEdit_auto_sleep_max)
        self.radioButton_action_download = _make_widget('radioButton_action_download', Form)
        self.horizontalLayout_7.addWidget(self.radioButton_action_download)
        self.radioButton_action_auto = _make_widget('radioButton_action_auto', Form)
        self.horizontalLayout_7.addWidget(self.radioButton_action_auto)
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
        self.lineEdit_ban_yun_duration_min = _make_widget('lineEdit_ban_yun_duration_min', Form)
        self.horizontalLayout_5.addWidget(self.lineEdit_ban_yun_duration_min)
        self.label_10 = _make_widget('label_10', Form)
        self.horizontalLayout_5.addWidget(self.label_10)
        self.lineEdit_ban_yun_duration_max = _make_widget('lineEdit_ban_yun_duration_max', Form)
        self.horizontalLayout_5.addWidget(self.lineEdit_ban_yun_duration_max)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName('horizontalLayout_6')
        self.verticalLayout_11.addLayout(self.horizontalLayout_6)
        self.label_9 = _make_widget('label_9', Form)
        self.horizontalLayout_6.addWidget(self.label_9)
        self.lineEdit_ban_yun_mb_min = _make_widget('lineEdit_ban_yun_mb_min', Form)
        self.horizontalLayout_6.addWidget(self.lineEdit_ban_yun_mb_min)
        self.label_11 = _make_widget('label_11', Form)
        self.horizontalLayout_6.addWidget(self.label_11)
        self.lineEdit_ban_yun_mb_max = _make_widget('lineEdit_ban_yun_mb_max', Form)
        self.horizontalLayout_6.addWidget(self.lineEdit_ban_yun_mb_max)
        self.ziyuanguolu = _make_widget('ziyuanguolu', Form)
        self.zuobian.addWidget(self.ziyuanguolu)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName('verticalLayout_5')
        self.ziyuanguolu.setLayout(self.verticalLayout_5)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName('horizontalLayout_3')
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.checkBox_dele_source_text = _make_widget('checkBox_dele_source_text', Form)
        self.horizontalLayout_3.addWidget(self.checkBox_dele_source_text)
        self.checkBox_discard_no_text_resource = _make_widget('checkBox_discard_no_text_resource', Form)
        self.horizontalLayout_3.addWidget(self.checkBox_discard_no_text_resource)
        self.checkBox_fliter_button = _make_widget('checkBox_fliter_button', Form)
        self.horizontalLayout_3.addWidget(self.checkBox_fliter_button)
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_22.setObjectName('horizontalLayout_22')
        self.verticalLayout_5.addLayout(self.horizontalLayout_22)
        self.checkBox_dele_link = _make_widget('checkBox_dele_link', Form)
        self.horizontalLayout_22.addWidget(self.checkBox_dele_link)
        self.checkBox_origin_source_text = _make_widget('checkBox_origin_source_text', Form)
        self.horizontalLayout_22.addWidget(self.checkBox_origin_source_text)
        self.checkBox_chai_zu = _make_widget('checkBox_chai_zu', Form)
        self.horizontalLayout_22.addWidget(self.checkBox_chai_zu)
        self.baohanci = QtWidgets.QHBoxLayout()
        self.baohanci.setObjectName('baohanci')
        self.verticalLayout_5.addLayout(self.baohanci)
        self.label_15 = _make_widget('label_15', Form)
        self.baohanci.addWidget(self.label_15)
        self.lineEdit_fliter_words_contain = _make_widget('lineEdit_fliter_words_contain', Form)
        self.baohanci.addWidget(self.lineEdit_fliter_words_contain)
        self.paichuci = QtWidgets.QHBoxLayout()
        self.paichuci.setObjectName('paichuci')
        self.verticalLayout_5.addLayout(self.paichuci)
        self.label_151 = _make_widget('label_151', Form)
        self.paichuci.addWidget(self.label_151)
        self.lineEdit_fliter_words_exclude = _make_widget('lineEdit_fliter_words_exclude', Form)
        self.paichuci.addWidget(self.lineEdit_fliter_words_exclude)
        self.youbian = QtWidgets.QVBoxLayout()
        self.youbian.setObjectName('youbian')
        self.horizontalLayout.addLayout(self.youbian)
        self.guanggao_qu = QtWidgets.QHBoxLayout()
        self.guanggao_qu.setObjectName('guanggao_qu')
        self.youbian.addLayout(self.guanggao_qu)
        self.horizontalGroupBox_4 = _make_widget('horizontalGroupBox_4', Form)
        self.guanggao_qu.addWidget(self.horizontalGroupBox_4)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName('verticalLayout_7')
        self.horizontalGroupBox_4.setLayout(self.verticalLayout_7)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName('horizontalLayout_16')
        self.verticalLayout_7.addLayout(self.horizontalLayout_16)
        self.checkBox_ad_enable = _make_widget('checkBox_ad_enable', Form)
        self.horizontalLayout_16.addWidget(self.checkBox_ad_enable)
        self.checkBox_ad_is_bottom_up = _make_widget('checkBox_ad_is_bottom_up', Form)
        self.horizontalLayout_16.addWidget(self.checkBox_ad_is_bottom_up)
        self.checkBox_ad_delete = _make_widget('checkBox_ad_delete', Form)
        self.horizontalLayout_16.addWidget(self.checkBox_ad_delete)
        self.btn_add_ad = _make_widget('btn_add_ad', Form)
        self.horizontalLayout_16.addWidget(self.btn_add_ad)
        self.listWidget_private_ad_list = _make_widget('listWidget_private_ad_list', Form)
        self.verticalLayout_7.addWidget(self.listWidget_private_ad_list)
        self.anniu_qu = QtWidgets.QVBoxLayout()
        self.anniu_qu.setObjectName('anniu_qu')
        self.youbian.addLayout(self.anniu_qu)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName('horizontalLayout_17')
        self.anniu_qu.addLayout(self.horizontalLayout_17)
        self.lineEdit_priority = _make_widget('lineEdit_priority', Form)
        self.horizontalLayout_17.addWidget(self.lineEdit_priority)
        self.lineEdit_yun_yin_name = _make_widget('lineEdit_yun_yin_name', Form)
        self.horizontalLayout_17.addWidget(self.lineEdit_yun_yin_name)
        self.btn_save_yun_yin_item = _make_widget('btn_save_yun_yin_item', Form)
        self.anniu_qu.addWidget(self.btn_save_yun_yin_item)
        self.verticalGroupBox_yulan_op = _make_widget('verticalGroupBox_yulan_op', Form)
        self.youbian.addWidget(self.verticalGroupBox_yulan_op)
        self.horizontalLayout_25 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_25.setObjectName('horizontalLayout_25')
        self.verticalGroupBox_yulan_op.setLayout(self.horizontalLayout_25)
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setObjectName('verticalLayout_12')
        self.horizontalLayout_25.addLayout(self.verticalLayout_12)
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName('horizontalLayout_18')
        self.verticalLayout_12.addLayout(self.horizontalLayout_18)
        self.cb_ban_yun_pic_blur = _make_widget('cb_ban_yun_pic_blur', Form)
        self.horizontalLayout_18.addWidget(self.cb_ban_yun_pic_blur)
        self.cb_ban_yun_spoiler = _make_widget('cb_ban_yun_spoiler', Form)
        self.horizontalLayout_18.addWidget(self.cb_ban_yun_spoiler)
        self.btn_ban_yun_res_op_jiao_chen = _make_widget('btn_ban_yun_res_op_jiao_chen', Form)
        self.horizontalLayout_18.addWidget(self.btn_ban_yun_res_op_jiao_chen)
        self.ban_yun_pic_blur_radius = _make_widget('ban_yun_pic_blur_radius', Form)
        self.verticalLayout_12.addWidget(self.ban_yun_pic_blur_radius)
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setObjectName('verticalLayout_13')
        self.horizontalLayout_25.addLayout(self.verticalLayout_13)
        self.horizontalLayout_26 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_26.setObjectName('horizontalLayout_26')
        self.verticalLayout_13.addLayout(self.horizontalLayout_26)
        self.label_17 = _make_widget('label_17', Form)
        self.horizontalLayout_26.addWidget(self.label_17)
        self.btn_ban_yun_grid_jiao_chen = _make_widget('btn_ban_yun_grid_jiao_chen', Form)
        self.horizontalLayout_26.addWidget(self.btn_ban_yun_grid_jiao_chen)
        self.lineEdit_ban_yun_grid_number = _make_widget('lineEdit_ban_yun_grid_number', Form)
        self.verticalLayout_13.addWidget(self.lineEdit_ban_yun_grid_number)
        self.verticalLayout_14 = QtWidgets.QVBoxLayout()
        self.verticalLayout_14.setObjectName('verticalLayout_14')
        self.horizontalLayout_25.addLayout(self.verticalLayout_14)
        self.horizontalLayout_27 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_27.setObjectName('horizontalLayout_27')
        self.verticalLayout_14.addLayout(self.horizontalLayout_27)
        self.ban_yun_cover_jiao_chen = _make_widget('ban_yun_cover_jiao_chen', Form)
        self.horizontalLayout_27.addWidget(self.ban_yun_cover_jiao_chen)
        self.cb_ban_yun_random_cover = _make_widget('cb_ban_yun_random_cover', Form)
        self.verticalLayout_14.addWidget(self.cb_ban_yun_random_cover)
        self.verticalGroupBox = _make_widget('verticalGroupBox', Form)
        self.youbian.addWidget(self.verticalGroupBox)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName('verticalLayout_10')
        self.verticalGroupBox.setLayout(self.verticalLayout_10)
        self.horizontalLayout_181 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_181.setObjectName('horizontalLayout_181')
        self.verticalLayout_10.addLayout(self.horizontalLayout_181)
        self.checkBox_pic_water = _make_widget('checkBox_pic_water', Form)
        self.horizontalLayout_181.addWidget(self.checkBox_pic_water)
        self.checkBox_video_water = _make_widget('checkBox_video_water', Form)
        self.horizontalLayout_181.addWidget(self.checkBox_video_water)
        self.comboBox_video_minute = _make_widget('comboBox_video_minute', Form)
        self.horizontalLayout_181.addWidget(self.comboBox_video_minute)
        self.cb_banyun_water_mode = _make_widget('cb_banyun_water_mode', Form)
        self.horizontalLayout_181.addWidget(self.cb_banyun_water_mode)
        self.label_12 = _make_widget('label_12', Form)
        self.verticalLayout_10.addWidget(self.label_12)
        self.text_water_wrapper = _make_widget('text_water_wrapper', Form)
        self.verticalLayout_10.addWidget(self.text_water_wrapper)
        self.text_water_wrapper_xx = QtWidgets.QVBoxLayout()
        self.text_water_wrapper_xx.setObjectName('text_water_wrapper_xx')
        self.text_water_wrapper.setLayout(self.text_water_wrapper_xx)
        self.lineEdit_water_text = _make_widget('lineEdit_water_text', Form)
        self.text_water_wrapper_xx.addWidget(self.lineEdit_water_text)
        self.pic_water_wrapper = _make_widget('pic_water_wrapper', Form)
        self.verticalLayout_10.addWidget(self.pic_water_wrapper)
        self.pic_water_wrapper_xx = QtWidgets.QHBoxLayout()
        self.pic_water_wrapper_xx.setObjectName('pic_water_wrapper_xx')
        self.pic_water_wrapper.setLayout(self.pic_water_wrapper_xx)
        self.btn_banyun_water_pic_jiao_chen = _make_widget('btn_banyun_water_pic_jiao_chen', Form)
        self.pic_water_wrapper_xx.addWidget(self.btn_banyun_water_pic_jiao_chen)
        self.btn_banyun_water_select_pic = _make_widget('btn_banyun_water_select_pic', Form)
        self.pic_water_wrapper_xx.addWidget(self.btn_banyun_water_select_pic)
        self.line_edit_by_com_water_pic_ratio = _make_widget('line_edit_by_com_water_pic_ratio', Form)
        self.pic_water_wrapper_xx.addWidget(self.line_edit_by_com_water_pic_ratio)
        self.label_banyun_water_pic_path = _make_widget('label_banyun_water_pic_path', Form)
        self.pic_water_wrapper_xx.addWidget(self.label_banyun_water_pic_path)
        self.verticalGroupBox1 = _make_widget('verticalGroupBox1', Form)
        self.youbian.addWidget(self.verticalGroupBox1)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName('verticalLayout_8')
        self.verticalGroupBox1.setLayout(self.verticalLayout_8)
        self.textEdit_replace_rule = _make_widget('textEdit_replace_rule', Form)
        self.verticalLayout_8.addWidget(self.textEdit_replace_rule)
        self.weiba_qu = _make_widget('weiba_qu', Form)
        self.youbian.addWidget(self.weiba_qu)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName('verticalLayout_2')
        self.weiba_qu.setLayout(self.verticalLayout_2)
        self.textEdit_tail_text = _make_widget('textEdit_tail_text', Form)
        self.verticalLayout_2.addWidget(self.textEdit_tail_text)
        self.ai_employee_qu = _make_widget('ai_employee_qu', Form)
        self.youbian.addWidget(self.ai_employee_qu)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName('verticalLayout_6')
        self.ai_employee_qu.setLayout(self.verticalLayout_6)
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setObjectName('horizontalLayout_19')
        self.verticalLayout_6.addLayout(self.horizontalLayout_19)
        self.checkBox_banyun_ai_enable = _make_widget('checkBox_banyun_ai_enable', Form)
        self.horizontalLayout_19.addWidget(self.checkBox_banyun_ai_enable)
        self.label_banyun_ai_name = _make_widget('label_banyun_ai_name', Form)
        self.horizontalLayout_19.addWidget(self.label_banyun_ai_name)
        self.btn_banyun_select_ai_em = _make_widget('btn_banyun_select_ai_em', Form)
        self.horizontalLayout_19.addWidget(self.btn_banyun_select_ai_em)
        self.horizontalGroupBox_ai_banyun = _make_widget('horizontalGroupBox_ai_banyun', Form)
        self.verticalLayout_6.addWidget(self.horizontalGroupBox_ai_banyun)
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_24.setObjectName('horizontalLayout_24')
        self.horizontalGroupBox_ai_banyun.setLayout(self.horizontalLayout_24)
        self.label_13 = _make_widget('label_13', Form)
        self.horizontalLayout_24.addWidget(self.label_13)
        self.radioButton_ai_banyun_use_source = _make_widget('radioButton_ai_banyun_use_source', Form)
        self.horizontalLayout_24.addWidget(self.radioButton_ai_banyun_use_source)
        self.radioButton_ai_banyun_skip_source = _make_widget('radioButton_ai_banyun_skip_source', Form)
        self.horizontalLayout_24.addWidget(self.radioButton_ai_banyun_skip_source)
        self.pinlunqu = _make_widget('pinlunqu', Form)
        self.youbian.addWidget(self.pinlunqu)
        self.replies = QtWidgets.QHBoxLayout()
        self.replies.setObjectName('replies')
        self.pinlunqu.setLayout(self.replies)
        self.checkBox_copy_comment = _make_widget('checkBox_copy_comment', Form)
        self.replies.addWidget(self.checkBox_copy_comment)
        self.btn_config_comment_rule = _make_widget('btn_config_comment_rule', Form)
        self.replies.addWidget(self.btn_config_comment_rule)
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
        self.jichu.setTitle(_translate('Form', '基础'))
        self.label.setText(_translate('Form', '来源频道/群组'))
        self.lineEdit_source.setPlaceholderText(_translate('Form', '公有链接或私有ID(支持话题)'))
        self.ban_yun_topic_jiao_chen.setText(_translate('Form', '教程'))
        self.label_2.setText(_translate('Form', '目标频道/群组(支持多个，一行一个，支持话题)'))
        self.textEdit_dest_list.setPlaceholderText(_translate('Form', '公有链接或私有ID（支持多个，一行一个，支持话题）'))
        self.ziyuanleiixing.setTitle(_translate('Form', '资源类型'))
        self.checkBox_video_photo.setText(_translate('Form', '仅包含视频的消息组'))
        self.checkBox_photo.setText(_translate('Form', '图片'))
        self.checkBox_video.setText(_translate('Form', '视频'))
        self.checkBox_file.setText(_translate('Form', '文件'))
        self.checkBox_text.setText(_translate('Form', '纯文本'))
        self.ban_yun_res_btn_jiao_chen.setText(_translate('Form', '教程'))
        self.moshi_xuanze.setTitle(_translate('Form', '模式选择'))
        self.comboBox_select_mode.setItemText(0, _translate('Form', '顺序模式'))
        self.comboBox_select_mode.setItemText(1, _translate('Form', '随机模式'))
        self.comboBox_select_mode.setItemText(2, _translate('Form', '循环模式'))
        self.random_com.setTitle(_translate('Form', '随机模式参数'))
        self.label_3.setText(_translate('Form', '期望数量'))
        self.lineEdit_random_want_count.setPlaceholderText(_translate('Form', '填写整数'))
        self.comboBox_number_random_dan_wei.setItemText(0, _translate('Form', '按组计算'))
        self.comboBox_number_random_dan_wei.setItemText(1, _translate('Form', '按个计算'))
        self.increase_com.setTitle(_translate('Form', '顺序模式参数（包括开始ID）'))
        self.label_7.setText(_translate('Form', '开始ID'))
        self.lineEdit_increase_start_id.setPlaceholderText(_translate('Form', '填写整数'))
        self.label_6.setText(_translate('Form', '期望数量'))
        self.lineEdit_increase_want_count.setPlaceholderText(_translate('Form', '填写整数'))
        self.comboBox_number_dan_wei.setCurrentText(_translate('Form', '按组计算'))
        self.comboBox_number_dan_wei.setItemText(0, _translate('Form', '按组计算'))
        self.comboBox_number_dan_wei.setItemText(1, _translate('Form', '按个计算'))
        self.loop_com.setTitle(_translate('Form', '循环模式参数（包括开始ID，不包括结束ID）'))
        self.label_8.setText(_translate('Form', '开始ID'))
        self.lineEdit_loop_start_id.setPlaceholderText(_translate('Form', '填写整数'))
        self.label_5.setText(_translate('Form', '结束ID'))
        self.lineEdit_loop_end_id.setPlaceholderText(_translate('Form', '填写整数'))
        self.zhuanfa.setTitle(_translate('Form', '搬运方式'))
        self.radioButton_action_download.setText(_translate('Form', '强制下载方式'))
        self.radioButton_action_auto.setText(_translate('Form', '自动方式'))
        self.lineEdit_auto_sleep_min.setPlaceholderText(_translate('Form', '间隔最小值'))
        self.label_14.setText(_translate('Form', '~'))
        self.lineEdit_auto_sleep_max.setPlaceholderText(_translate('Form', '间隔最大值'))
        self.jichu_filter.setTitle(_translate('Form', '基础条件(如果是视频资源，则需要同时满足时长和大小)'))
        self.label_4.setText(_translate('Form', '时长过滤(单位分钟)：'))
        self.lineEdit_ban_yun_duration_min.setPlaceholderText(_translate('Form', '最小值'))
        self.label_10.setText(_translate('Form', '~'))
        self.lineEdit_ban_yun_duration_max.setPlaceholderText(_translate('Form', '最大值'))
        self.label_9.setText(_translate('Form', '大小过滤(单位 MB )：'))
        self.lineEdit_ban_yun_mb_min.setPlaceholderText(_translate('Form', '最小值'))
        self.label_11.setText(_translate('Form', '~'))
        self.lineEdit_ban_yun_mb_max.setPlaceholderText(_translate('Form', '最大值'))
        self.ziyuanguolu.setTitle(_translate('Form', '资源过滤条件'))
        self.checkBox_dele_source_text.setText(_translate('Form', '丢弃资源自带的文本'))
        self.checkBox_discard_no_text_resource.setText(_translate('Form', '丢弃无文本的资源'))
        self.checkBox_fliter_button.setText(_translate('Form', '丢弃带按钮的资源'))
        self.checkBox_dele_link.setText(_translate('Form', '删除源文本中的外链'))
        self.checkBox_origin_source_text.setText(_translate('Form', '原样文本搬运'))
        self.checkBox_chai_zu.setText(_translate('Form', '根据大小时长拆组'))
        self.label_15.setText(_translate('Form', '包含关键词的资源'))
        self.lineEdit_fliter_words_contain.setPlaceholderText(_translate('Form', '填写关键词，多个词使用竖线"|"分割'))
        self.label_151.setText(_translate('Form', '排除关键词的资源'))
        self.lineEdit_fliter_words_exclude.setPlaceholderText(_translate('Form', '填写关键词，多个词使用竖线"|"分割'))
        self.verticalGroupBox_yulan_op.setTitle(_translate('Form', '资源处理（可选）'))
        self.cb_ban_yun_pic_blur.setText(_translate('Form', '图片模糊'))
        self.cb_ban_yun_spoiler.setText(_translate('Form', '防剧透'))
        self.btn_ban_yun_res_op_jiao_chen.setText(_translate('Form', '教程'))
        self.ban_yun_pic_blur_radius.setPlaceholderText(_translate('Form', '1~20数字越大越模糊'))
        self.label_17.setText(_translate('Form', '消息组宫格补齐'))
        self.btn_ban_yun_grid_jiao_chen.setText(_translate('Form', '教程'))
        self.lineEdit_ban_yun_grid_number.setPlaceholderText(_translate('Form', '填写0~10的整数'))
        self.cb_ban_yun_random_cover.setText(_translate('Form', '随机封面'))
        self.ban_yun_cover_jiao_chen.setText(_translate('Form', '教程'))
        self.verticalGroupBox.setTitle(_translate('Form', '水印（可选）'))
        self.label_12.setText(_translate('Form', '图片水印或者视频动态水印'))
        self.checkBox_pic_water.setText(_translate('Form', '图片水印'))
        self.checkBox_video_water.setText(_translate('Form', '视频水印'))
        self.comboBox_video_minute.setItemText(0, _translate('Form', '1分钟内视频'))
        self.comboBox_video_minute.setItemText(1, _translate('Form', '3分钟内视频'))
        self.comboBox_video_minute.setItemText(2, _translate('Form', '5分钟内视频'))
        self.comboBox_video_minute.setItemText(3, _translate('Form', '10分钟内视频'))
        self.comboBox_video_minute.setItemText(4, _translate('Form', '30分钟内视频'))
        self.comboBox_video_minute.setItemText(5, _translate('Form', '60分钟内视频'))
        self.comboBox_video_minute.setItemText(6, _translate('Form', '90分钟内视频'))
        self.comboBox_video_minute.setItemText(7, _translate('Form', '120分钟内视频'))
        self.comboBox_video_minute.setItemText(8, _translate('Form', '150分钟内视频'))
        self.cb_banyun_water_mode.setItemText(0, _translate('Form', '图片水印'))
        self.cb_banyun_water_mode.setItemText(1, _translate('Form', '文字水印'))
        self.lineEdit_water_text.setPlaceholderText(_translate('Form', '水印文字，支持中文，英文'))
        self.btn_banyun_water_pic_jiao_chen.setText(_translate('Form', '教程'))
        self.btn_banyun_water_select_pic.setText(_translate('Form', '选择图片'))
        self.line_edit_by_com_water_pic_ratio.setPlaceholderText(_translate('Form', '30'))
        self.label_banyun_water_pic_path.setText(_translate('Form', '图片路径：'))
        self.verticalGroupBox1.setTitle(_translate('Form', '替换规则（可选，详情可以查看pdf文档）'))
        self.textEdit_replace_rule.setPlaceholderText(_translate('Form', '源词语->目标词语，详情可以查看pdf文档'))
        self.weiba_qu.setTitle(_translate('Form', '尾巴（可选，支持html格式和电报会员表情）'))
        self.textEdit_tail_text.setPlaceholderText(_translate('Form', '支持html格式和电报会员表情，详情可以查看pdf文档'))
        self.ai_employee_qu.setTitle(_translate('Form', 'AI员工（可选，AI文案同义转换）'))
        self.checkBox_banyun_ai_enable.setText(_translate('Form', '启用AI文案'))
        self.label_banyun_ai_name.setText(_translate('Form', '当前选择：xxx'))
        self.btn_banyun_select_ai_em.setText(_translate('Form', '选择AI员工'))
        self.label_13.setText(_translate('Form', 'AI拒绝生成文案时候：'))
        self.radioButton_ai_banyun_use_source.setText(_translate('Form', '使用源文案'))
        self.radioButton_ai_banyun_skip_source.setText(_translate('Form', '跳过此资源'))
        self.pinlunqu.setTitle(_translate('Form', '评论区（可选）'))
        self.checkBox_copy_comment.setText(_translate('Form', '一比一复刻评论区'))
        self.btn_config_comment_rule.setText(_translate('Form', '配置评论区搬运规则'))
        self.horizontalGroupBox_4.setTitle(_translate('Form', '私有广告（可选）'))
        self.checkBox_ad_enable.setText(_translate('Form', '启用广告'))
        self.checkBox_ad_is_bottom_up.setText(_translate('Form', '置底广告'))
        self.checkBox_ad_delete.setText(_translate('Form', '删除历史广告'))
        self.btn_add_ad.setText(_translate('Form', '添加广告'))
        self.lineEdit_priority.setPlaceholderText(_translate('Form', '优先级'))
        self.lineEdit_yun_yin_name.setPlaceholderText(_translate('Form', '输入搬运流的名字'))
        self.btn_save_yun_yin_item.setText(_translate('Form', '保存'))

