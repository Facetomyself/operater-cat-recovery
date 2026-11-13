# Recovered module: src.resource.ui.dyna.auto_flow_item
#
# The original Qt Designer .ui file is not shipped in the distribution.
# Widget names and types are recovered from the dialog widget map and the
# Nuitka constants chunk. The layout is a behaviour-level reconstruction.
from __future__ import annotations

from PyQt5 import QtCore, QtWidgets


FORM_TITLE = '编辑自动流'

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
    'btn_flow_hui_yuan_link_jc': 'QPushButton',
    'btn_flow_you_ke_link_jc': 'QPushButton',
    'btn_show_duration_dialog': 'QPushButton',
    'auto_res_btn_jiao_chen': 'QPushButton',
    'btn_auto_flow_res_op_jiao_chen': 'QPushButton',
    'btn_auto_flow_action_jiao_chen': 'QPushButton',
    'auto_flow_topic_jiao_chen': 'QPushButton',
    'btn_auto_select_ai_em': 'QPushButton',
    'btn_flow_water_pic_jiao_chen': 'QPushButton',
    'btn_flow_water_select_pic': 'QPushButton',
    'btn_auto_grid_jiao_chen': 'QPushButton',
    'auto_cover_jiao_chen': 'QPushButton',
    'btn_save_flow_item': 'QPushButton',
    'btn_flow_add_ad': 'QPushButton',
    'comboBox_flow_number_dan_wei': 'QComboBox',
    'comboBox_flow_number_random_dan_wei': 'QComboBox',
    'comboBox_flow_select_mode': 'QComboBox',
    'comboBox_auto_flow_select_auto_flow_mode': 'QComboBox',
    'cb_flow_water_mode': 'QComboBox',
    'listWidget_flow_private_ad_list': 'QListWidget',
    'cb_flow_origin_source_text': 'QCheckBox',
    'cb_flow_ad_enable': 'QCheckBox',
    'cb_flow_hui_yuan_link': 'QCheckBox',
    'lineEdit_flow_hui_yuan_tip_text': 'QLineEdit',
    'cb_flow_hui_yuan_customer_link': 'QCheckBox',
    'lineEdit_flow_hui_yuan_tip_text_link': 'QLineEdit',
    'cb_flow_you_ke_link': 'QCheckBox',
    'lineEdit_flow_you_ke_tip_text': 'QLineEdit',
    'lineEdit_flow_you_ke_tip_text_link': 'QLineEdit',
    'radioButton_auto_flow_10': 'QRadioButton',
    'radioButton_auto_flow_20': 'QRadioButton',
    'radioButton_auto_flow_30': 'QRadioButton',
    'radioButton_auto_flow_customer': 'QRadioButton',
    'checkBox_flow_video_photo': 'QCheckBox',
    'checkBox_pb_auto_flow_video': 'QCheckBox',
    'checkBox_auto_ai_enable': 'QCheckBox',
    'horizontalGroupBox_ai_auto': 'QGroupBox',
    'label_auto_ai_name': 'QLabel',
    'label_flow_water_pic_path': 'QLabel',
    'lineEdit_auto_flow_customer': 'QLineEdit',
    'yulan_qu': 'QGroupBox',
    'yulan_qu_wrapper': 'QGroupBox',
    'checkBox_chai_zu': 'QCheckBox',
    'checkBox_flow_photo': 'QCheckBox',
    'checkBox_flow_video': 'QCheckBox',
    'checkBox_flow_file': 'QCheckBox',
    'lineEdit_flow_random_want_count': 'QLineEdit',
    'cb_flow_dele_source_text': 'QCheckBox',
    'cb_flow_dele_link': 'QCheckBox',
    'cb_flow_fliter_button': 'QCheckBox',
    'lineEdit_flow_increase_start_id': 'QLineEdit',
    'lineEdit_flow_increase_want_count': 'QLineEdit',
    'lineEdit_auto_duration_min': 'QLineEdit',
    'lineEdit_auto_duration_max': 'QLineEdit',
    'lineEdit_auto_mb_min': 'QLineEdit',
    'lineEdit_auto_mb_max': 'QLineEdit',
    'checkBox_flow_text': 'QCheckBox',
    'lineEdit_auto_flow_min_duration': 'QLineEdit',
    'lineEdit_auto_flow_max_duration': 'QLineEdit',
    'lineEdit_auto_flow_sleep_min': 'QLineEdit',
    'lineEdit_auto_flow_sleep_max': 'QLineEdit',
    'radioButton_auto_flow_action_auto': 'QRadioButton',
    'radioButton_auto_flow_action_download': 'QRadioButton',
    'checkBox_pb_auto_flow_picture': 'QCheckBox',
    'auto_flow_pic_blur_radius': 'QLineEdit',
    'cb_flow_hui_yuan_link_bq': 'QCheckBox',
    'cb_flow_you_ke_link_bq': 'QCheckBox',
    'checkBox_auto_add_duration_info_bq': 'QCheckBox',
    'lineEdit_priority': 'QLineEdit',
    'radioButton_ai_auto_skip_source': 'QRadioButton',
    'radioButton_ai_auto_use_source': 'QRadioButton',
    'line_edit_auto_flow_water_pic_ratio': 'QLineEdit',
    'lineEdit_auto_grid_number': 'QLineEdit',
    'cb_flow_ad_is_bottom_up': 'QCheckBox',
    'cb_flow_ad_delete': 'QCheckBox',
    'present_container': 'QGroupBox',
    'duration_container': 'QGroupBox',
    'text_water_wrapper': 'QGroupBox',
    'pic_water_wrapper': 'QGroupBox',
    'random_com': 'QGroupBox',
    'increase_com': 'QGroupBox',
    'loop_com': 'QGroupBox',
    'text_model': 'QLineEdit',
    'number_model': 'QLineEdit',
    'lineEdit_flow_source': 'QLineEdit',
    'textEdit_flow_dest_list': 'QTextEdit',
    'textEdit_flow_auto_flow_dest_list': 'QTextEdit',
    'lineEdit_flow_fliter_words_contain': 'QLineEdit',
    'lineEdit_flow_fliter_words_exclude': 'QLineEdit',
    'lineEdit_flow_loop_start_id': 'QLineEdit',
    'lineEdit_flow_loop_end_id': 'QLineEdit',
    'checkBox_discard_no_text_resource': 'QCheckBox',
    'textEdit_flow_tail_text': 'QTextEdit',
    'cb_flow_pic_water': 'QCheckBox',
    'cb_flow_video_water': 'QCheckBox',
    'cb_flow_video_minute': 'QComboBox',
    'lineEdit_cb_water_text': 'QLineEdit',
    'textEdit_flow_replace_rule': 'QTextEdit',
    'checkBox_auto_add_duration_info': 'QCheckBox',
    'cb_auto_flow_spoiler': 'QCheckBox',
    'cb_auto_flow_pic_blur': 'QCheckBox',
    'cb_auto_random_cover': 'QCheckBox',
    'lineEdit_flow_item_name': 'QLineEdit',
    'verticalGroupBox_4': 'QGroupBox',
    'label': 'QLabel',
    'pushButton_auto_step1': 'QPushButton',
    'label_2': 'QLabel',
    'pushButton_auto_step2': 'QPushButton',
    'label_4': 'QLabel',
    'ziyuanleiixing': 'QGroupBox',
    'groupBox': 'QGroupBox',
    'label_21': 'QLabel',
    'label_13': 'QLabel',
    'zhuanfa': 'QWidget',
    'label_14': 'QLabel',
    'moshi_xuanze': 'QGroupBox',
    'label_3': 'QLabel',
    'label_7': 'QLabel',
    'label_6': 'QLabel',
    'label_8': 'QLabel',
    'label_5': 'QLabel',
    'jichu_filter': 'QWidget',
    'label_41': 'QLabel',
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
    'weiba_qu': 'QGroupBox',
    'verticalGroupBox1': 'QWidget',
    'ai_employee_qu': 'QGroupBox',
    'label_131': 'QLabel',
    'huiyuan_quyu': 'QWidget',
    'youkke_quyu': 'QWidget',
    'horizontalGroupBox_4': 'QGroupBox',
    'horizontalGroupBox_auto': 'QGroupBox',
    'line': 'QFrame',
}


_SIZE_CONSTRAINTS = {
    'ai_employee_qu': {'setMinimumSize': [0, 25]},
    'btn_save_flow_item': {'setMaximumSize': [16777215, 30]},
    'horizontalGroupBox_4': {'setMaximumSize': [16777215, 70]},
    'horizontalGroupBox_auto': {'setMinimumSize': [30, 0]},
    'huiyuan_quyu': {'setMinimumSize': [30, 0]},
    'increase_com': {'setMaximumSize': [16777215, 40]},
    'lineEdit_flow_item_name': {'setMinimumSize': [0, 0], 'setMaximumSize': [16777215, 30]},
    'lineEdit_priority': {'setMaximumSize': [60, 30]},
    'loop_com': {'setMaximumSize': [16777215, 50]},
    'pic_water_wrapper': {'setMaximumSize': [30, 16777215]},
    'random_com': {'setMaximumSize': [16777215, 40]},
    'verticalGroupBox1': {'setMaximumSize': [16777215, 60]},
    'verticalGroupBox_4': {'setMaximumSize': [16777215, 60], 'setMinimumSize': [30, 0]},
    'verticalGroupBox_yulan_op': {'setMaximumSize': [30, 16777215]},
    'weiba_qu': {'setMaximumSize': [16777215, 60]},
    'youkke_quyu': {'setMinimumSize': [30, 0]},
    'zhuanfa': {'setMinimumSize': [0, 0]},
    'ziyuanleiixing': {'setMinimumSize': [30, 0]},
}


SETUP_ORDER = (
    'lineEdit_flow_source',
    'auto_flow_topic_jiao_chen',
    'textEdit_flow_dest_list',
    'textEdit_flow_auto_flow_dest_list',
    'checkBox_flow_video_photo',
    'checkBox_flow_photo',
    'checkBox_flow_video',
    'checkBox_flow_file',
    'checkBox_flow_text',
    'auto_res_btn_jiao_chen',
    'yulan_qu_wrapper',
    'checkBox_pb_auto_flow_picture',
    'checkBox_pb_auto_flow_video',
    'yulan_qu',
    'comboBox_auto_flow_select_auto_flow_mode',
    'present_container',
    'radioButton_auto_flow_10',
    'radioButton_auto_flow_20',
    'radioButton_auto_flow_30',
    'radioButton_auto_flow_customer',
    'lineEdit_auto_flow_customer',
    'duration_container',
    'lineEdit_auto_flow_min_duration',
    'lineEdit_auto_flow_max_duration',
    'radioButton_auto_flow_action_download',
    'radioButton_auto_flow_action_auto',
    'lineEdit_auto_flow_sleep_min',
    'lineEdit_auto_flow_sleep_max',
    'btn_auto_flow_action_jiao_chen',
    'comboBox_flow_select_mode',
    'random_com',
    'lineEdit_flow_random_want_count',
    'comboBox_flow_number_random_dan_wei',
    'increase_com',
    'lineEdit_flow_increase_start_id',
    'lineEdit_flow_increase_want_count',
    'comboBox_flow_number_dan_wei',
    'loop_com',
    'lineEdit_flow_loop_start_id',
    'lineEdit_flow_loop_end_id',
    'lineEdit_auto_duration_min',
    'lineEdit_auto_duration_max',
    'lineEdit_auto_mb_min',
    'lineEdit_auto_mb_max',
    'cb_flow_dele_source_text',
    'checkBox_discard_no_text_resource',
    'cb_flow_fliter_button',
    'cb_flow_dele_link',
    'cb_flow_origin_source_text',
    'checkBox_chai_zu',
    'lineEdit_flow_fliter_words_contain',
    'lineEdit_flow_fliter_words_exclude',
    'cb_auto_flow_pic_blur',
    'cb_auto_flow_spoiler',
    'btn_auto_flow_res_op_jiao_chen',
    'auto_flow_pic_blur_radius',
    'btn_auto_grid_jiao_chen',
    'lineEdit_auto_grid_number',
    'cb_auto_random_cover',
    'auto_cover_jiao_chen',
    'cb_flow_pic_water',
    'cb_flow_video_water',
    'cb_flow_video_minute',
    'cb_flow_water_mode',
    'text_water_wrapper',
    'lineEdit_cb_water_text',
    'pic_water_wrapper',
    'btn_flow_water_pic_jiao_chen',
    'btn_flow_water_select_pic',
    'line_edit_auto_flow_water_pic_ratio',
    'label_flow_water_pic_path',
    'textEdit_flow_tail_text',
    'textEdit_flow_replace_rule',
    'checkBox_auto_ai_enable',
    'label_auto_ai_name',
    'btn_auto_select_ai_em',
    'horizontalGroupBox_ai_auto',
    'radioButton_ai_auto_use_source',
    'radioButton_ai_auto_skip_source',
    'cb_flow_hui_yuan_link',
    'cb_flow_hui_yuan_customer_link',
    'cb_flow_hui_yuan_link_bq',
    'btn_flow_hui_yuan_link_jc',
    'lineEdit_flow_hui_yuan_tip_text',
    'lineEdit_flow_hui_yuan_tip_text_link',
    'cb_flow_you_ke_link',
    'cb_flow_you_ke_link_bq',
    'btn_flow_you_ke_link_jc',
    'lineEdit_flow_you_ke_tip_text',
    'lineEdit_flow_you_ke_tip_text_link',
    'checkBox_auto_add_duration_info',
    'checkBox_auto_add_duration_info_bq',
    'btn_show_duration_dialog',
    'cb_flow_ad_enable',
    'cb_flow_ad_is_bottom_up',
    'cb_flow_ad_delete',
    'btn_flow_add_ad',
    'listWidget_flow_private_ad_list',
    'lineEdit_priority',
    'lineEdit_flow_item_name',
    'btn_save_flow_item',
    'text_model',
    'number_model',
    'verticalGroupBox_4',
    'label',
    'pushButton_auto_step1',
    'label_2',
    'pushButton_auto_step2',
    'label_4',
    'ziyuanleiixing',
    'groupBox',
    'label_21',
    'label_13',
    'zhuanfa',
    'label_14',
    'moshi_xuanze',
    'label_3',
    'label_7',
    'label_6',
    'label_8',
    'label_5',
    'jichu_filter',
    'label_41',
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
    'weiba_qu',
    'verticalGroupBox1',
    'ai_employee_qu',
    'label_131',
    'huiyuan_quyu',
    'youkke_quyu',
    'horizontalGroupBox_4',
    'horizontalGroupBox_auto',
    'line',
)


class Ui_Form:
    def setupUi(self, Form):
        Form.setObjectName('Form')
        Form.resize(889, 1199)
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
        self.lineEdit_flow_source = _make_widget('lineEdit_flow_source', Form)
        self.horizontalLayout_10.addWidget(self.lineEdit_flow_source)
        self.auto_flow_topic_jiao_chen = _make_widget('auto_flow_topic_jiao_chen', Form)
        self.horizontalLayout_10.addWidget(self.auto_flow_topic_jiao_chen)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName('verticalLayout_9')
        self.verticalLayout_4.addLayout(self.verticalLayout_9)
        self.pushButton_auto_step1 = _make_widget('pushButton_auto_step1', Form)
        self.verticalLayout_9.addWidget(self.pushButton_auto_step1)
        self.label_2 = _make_widget('label_2', Form)
        self.verticalLayout_9.addWidget(self.label_2)
        self.textEdit_flow_dest_list = _make_widget('textEdit_flow_dest_list', Form)
        self.verticalLayout_9.addWidget(self.textEdit_flow_dest_list)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName('verticalLayout')
        self.verticalLayout_4.addLayout(self.verticalLayout)
        self.pushButton_auto_step2 = _make_widget('pushButton_auto_step2', Form)
        self.verticalLayout.addWidget(self.pushButton_auto_step2)
        self.label_4 = _make_widget('label_4', Form)
        self.verticalLayout.addWidget(self.label_4)
        self.textEdit_flow_auto_flow_dest_list = _make_widget('textEdit_flow_auto_flow_dest_list', Form)
        self.verticalLayout.addWidget(self.textEdit_flow_auto_flow_dest_list)
        self.ziyuanleiixing = _make_widget('ziyuanleiixing', Form)
        self.zuobian.addWidget(self.ziyuanleiixing)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName('horizontalLayout_8')
        self.ziyuanleiixing.setLayout(self.horizontalLayout_8)
        self.checkBox_flow_video_photo = _make_widget('checkBox_flow_video_photo', Form)
        self.horizontalLayout_8.addWidget(self.checkBox_flow_video_photo)
        self.checkBox_flow_photo = _make_widget('checkBox_flow_photo', Form)
        self.horizontalLayout_8.addWidget(self.checkBox_flow_photo)
        self.checkBox_flow_video = _make_widget('checkBox_flow_video', Form)
        self.horizontalLayout_8.addWidget(self.checkBox_flow_video)
        self.checkBox_flow_file = _make_widget('checkBox_flow_file', Form)
        self.horizontalLayout_8.addWidget(self.checkBox_flow_file)
        self.checkBox_flow_text = _make_widget('checkBox_flow_text', Form)
        self.horizontalLayout_8.addWidget(self.checkBox_flow_text)
        self.auto_res_btn_jiao_chen = _make_widget('auto_res_btn_jiao_chen', Form)
        self.horizontalLayout_8.addWidget(self.auto_res_btn_jiao_chen)
        self.groupBox = _make_widget('groupBox', Form)
        self.zuobian.addWidget(self.groupBox)
        self.verticalLayout1 = QtWidgets.QVBoxLayout()
        self.verticalLayout1.setObjectName('verticalLayout1')
        self.groupBox.setLayout(self.verticalLayout1)
        self.yulan_qu_wrapper = QtWidgets.QVBoxLayout()
        self.yulan_qu_wrapper.setObjectName('yulan_qu_wrapper')
        self.verticalLayout1.addLayout(self.yulan_qu_wrapper)
        self.type_wraper = QtWidgets.QHBoxLayout()
        self.type_wraper.setObjectName('type_wraper')
        self.yulan_qu_wrapper.addLayout(self.type_wraper)
        self.checkBox_pb_auto_flow_picture = _make_widget('checkBox_pb_auto_flow_picture', Form)
        self.type_wraper.addWidget(self.checkBox_pb_auto_flow_picture)
        self.checkBox_pb_auto_flow_video = _make_widget('checkBox_pb_auto_flow_video', Form)
        self.type_wraper.addWidget(self.checkBox_pb_auto_flow_video)
        self.yulan_qu = _make_widget('yulan_qu', Form)
        self.yulan_qu_wrapper.addWidget(self.yulan_qu)
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName('verticalLayout_11')
        self.yulan_qu.setLayout(self.verticalLayout_11)
        self.comboBox_auto_flow_select_auto_flow_mode = _make_widget('comboBox_auto_flow_select_auto_flow_mode', Form)
        self.verticalLayout_11.addWidget(self.comboBox_auto_flow_select_auto_flow_mode)
        self.present_container = _make_widget('present_container', Form)
        self.verticalLayout_11.addWidget(self.present_container)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName('horizontalLayout_6')
        self.present_container.setLayout(self.horizontalLayout_6)
        self.radioButton_auto_flow_10 = _make_widget('radioButton_auto_flow_10', Form)
        self.horizontalLayout_6.addWidget(self.radioButton_auto_flow_10)
        self.radioButton_auto_flow_20 = _make_widget('radioButton_auto_flow_20', Form)
        self.horizontalLayout_6.addWidget(self.radioButton_auto_flow_20)
        self.radioButton_auto_flow_30 = _make_widget('radioButton_auto_flow_30', Form)
        self.horizontalLayout_6.addWidget(self.radioButton_auto_flow_30)
        self.radioButton_auto_flow_customer = _make_widget('radioButton_auto_flow_customer', Form)
        self.horizontalLayout_6.addWidget(self.radioButton_auto_flow_customer)
        self.lineEdit_auto_flow_customer = _make_widget('lineEdit_auto_flow_customer', Form)
        self.horizontalLayout_6.addWidget(self.lineEdit_auto_flow_customer)
        self.duration_container = _make_widget('duration_container', Form)
        self.verticalLayout_11.addWidget(self.duration_container)
        self.horizontalLayout_61 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_61.setObjectName('horizontalLayout_61')
        self.duration_container.setLayout(self.horizontalLayout_61)
        self.label_21 = _make_widget('label_21', Form)
        self.horizontalLayout_61.addWidget(self.label_21)
        self.lineEdit_auto_flow_min_duration = _make_widget('lineEdit_auto_flow_min_duration', Form)
        self.horizontalLayout_61.addWidget(self.lineEdit_auto_flow_min_duration)
        self.label_13 = _make_widget('label_13', Form)
        self.horizontalLayout_61.addWidget(self.label_13)
        self.lineEdit_auto_flow_max_duration = _make_widget('lineEdit_auto_flow_max_duration', Form)
        self.horizontalLayout_61.addWidget(self.lineEdit_auto_flow_max_duration)
        self.zhuanfa = _make_widget('zhuanfa', Form)
        self.zuobian.addWidget(self.zhuanfa)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName('horizontalLayout_7')
        self.zhuanfa.setLayout(self.horizontalLayout_7)
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_23.setObjectName('horizontalLayout_23')
        self.horizontalLayout_7.addLayout(self.horizontalLayout_23)
        self.lineEdit_auto_flow_sleep_min = _make_widget('lineEdit_auto_flow_sleep_min', Form)
        self.horizontalLayout_23.addWidget(self.lineEdit_auto_flow_sleep_min)
        self.label_14 = _make_widget('label_14', Form)
        self.horizontalLayout_23.addWidget(self.label_14)
        self.lineEdit_auto_flow_sleep_max = _make_widget('lineEdit_auto_flow_sleep_max', Form)
        self.horizontalLayout_23.addWidget(self.lineEdit_auto_flow_sleep_max)
        self.radioButton_auto_flow_action_download = _make_widget('radioButton_auto_flow_action_download', Form)
        self.horizontalLayout_7.addWidget(self.radioButton_auto_flow_action_download)
        self.radioButton_auto_flow_action_auto = _make_widget('radioButton_auto_flow_action_auto', Form)
        self.horizontalLayout_7.addWidget(self.radioButton_auto_flow_action_auto)
        self.btn_auto_flow_action_jiao_chen = _make_widget('btn_auto_flow_action_jiao_chen', Form)
        self.horizontalLayout_7.addWidget(self.btn_auto_flow_action_jiao_chen)
        self.moshi_xuanze = _make_widget('moshi_xuanze', Form)
        self.zuobian.addWidget(self.moshi_xuanze)
        self.verticalLayout2 = QtWidgets.QVBoxLayout()
        self.verticalLayout2.setObjectName('verticalLayout2')
        self.moshi_xuanze.setLayout(self.verticalLayout2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName('verticalLayout_3')
        self.verticalLayout2.addLayout(self.verticalLayout_3)
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
        self.lineEdit_flow_random_want_count = _make_widget('lineEdit_flow_random_want_count', Form)
        self.horizontalLayout_20.addWidget(self.lineEdit_flow_random_want_count)
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setObjectName('horizontalLayout_21')
        self.horizontalLayout_11.addLayout(self.horizontalLayout_21)
        self.comboBox_flow_number_random_dan_wei = _make_widget('comboBox_flow_number_random_dan_wei', Form)
        self.horizontalLayout_21.addWidget(self.comboBox_flow_number_random_dan_wei)
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
        self.lineEdit_flow_increase_start_id = _make_widget('lineEdit_flow_increase_start_id', Form)
        self.horizontalLayout_13.addWidget(self.lineEdit_flow_increase_start_id)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName('horizontalLayout_12')
        self.horizontalLayout_2.addLayout(self.horizontalLayout_12)
        self.label_6 = _make_widget('label_6', Form)
        self.horizontalLayout_12.addWidget(self.label_6)
        self.lineEdit_flow_increase_want_count = _make_widget('lineEdit_flow_increase_want_count', Form)
        self.horizontalLayout_12.addWidget(self.lineEdit_flow_increase_want_count)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName('horizontalLayout_9')
        self.horizontalLayout_2.addLayout(self.horizontalLayout_9)
        self.comboBox_flow_number_dan_wei = _make_widget('comboBox_flow_number_dan_wei', Form)
        self.horizontalLayout_9.addWidget(self.comboBox_flow_number_dan_wei)
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
        self.lineEdit_flow_loop_start_id = _make_widget('lineEdit_flow_loop_start_id', Form)
        self.horizontalLayout_15.addWidget(self.lineEdit_flow_loop_start_id)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName('horizontalLayout_14')
        self.horizontalLayout_4.addLayout(self.horizontalLayout_14)
        self.label_5 = _make_widget('label_5', Form)
        self.horizontalLayout_14.addWidget(self.label_5)
        self.lineEdit_flow_loop_end_id = _make_widget('lineEdit_flow_loop_end_id', Form)
        self.horizontalLayout_14.addWidget(self.lineEdit_flow_loop_end_id)
        self.comboBox_flow_select_mode = _make_widget('comboBox_flow_select_mode', Form)
        self.verticalLayout2.addWidget(self.comboBox_flow_select_mode)
        self.jichu_filter = _make_widget('jichu_filter', Form)
        self.zuobian.addWidget(self.jichu_filter)
        self.verticalLayout_111 = QtWidgets.QVBoxLayout()
        self.verticalLayout_111.setObjectName('verticalLayout_111')
        self.jichu_filter.setLayout(self.verticalLayout_111)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName('horizontalLayout_5')
        self.verticalLayout_111.addLayout(self.horizontalLayout_5)
        self.label_41 = _make_widget('label_41', Form)
        self.horizontalLayout_5.addWidget(self.label_41)
        self.lineEdit_auto_duration_min = _make_widget('lineEdit_auto_duration_min', Form)
        self.horizontalLayout_5.addWidget(self.lineEdit_auto_duration_min)
        self.label_10 = _make_widget('label_10', Form)
        self.horizontalLayout_5.addWidget(self.label_10)
        self.lineEdit_auto_duration_max = _make_widget('lineEdit_auto_duration_max', Form)
        self.horizontalLayout_5.addWidget(self.lineEdit_auto_duration_max)
        self.horizontalLayout_62 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_62.setObjectName('horizontalLayout_62')
        self.verticalLayout_111.addLayout(self.horizontalLayout_62)
        self.label_9 = _make_widget('label_9', Form)
        self.horizontalLayout_62.addWidget(self.label_9)
        self.lineEdit_auto_mb_min = _make_widget('lineEdit_auto_mb_min', Form)
        self.horizontalLayout_62.addWidget(self.lineEdit_auto_mb_min)
        self.label_11 = _make_widget('label_11', Form)
        self.horizontalLayout_62.addWidget(self.label_11)
        self.lineEdit_auto_mb_max = _make_widget('lineEdit_auto_mb_max', Form)
        self.horizontalLayout_62.addWidget(self.lineEdit_auto_mb_max)
        self.ziyuanguolu = _make_widget('ziyuanguolu', Form)
        self.zuobian.addWidget(self.ziyuanguolu)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName('verticalLayout_5')
        self.ziyuanguolu.setLayout(self.verticalLayout_5)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName('horizontalLayout_3')
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.cb_flow_dele_source_text = _make_widget('cb_flow_dele_source_text', Form)
        self.horizontalLayout_3.addWidget(self.cb_flow_dele_source_text)
        self.checkBox_discard_no_text_resource = _make_widget('checkBox_discard_no_text_resource', Form)
        self.horizontalLayout_3.addWidget(self.checkBox_discard_no_text_resource)
        self.cb_flow_fliter_button = _make_widget('cb_flow_fliter_button', Form)
        self.horizontalLayout_3.addWidget(self.cb_flow_fliter_button)
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_22.setObjectName('horizontalLayout_22')
        self.verticalLayout_5.addLayout(self.horizontalLayout_22)
        self.cb_flow_dele_link = _make_widget('cb_flow_dele_link', Form)
        self.horizontalLayout_22.addWidget(self.cb_flow_dele_link)
        self.cb_flow_origin_source_text = _make_widget('cb_flow_origin_source_text', Form)
        self.horizontalLayout_22.addWidget(self.cb_flow_origin_source_text)
        self.checkBox_chai_zu = _make_widget('checkBox_chai_zu', Form)
        self.horizontalLayout_22.addWidget(self.checkBox_chai_zu)
        self.baohanci = QtWidgets.QHBoxLayout()
        self.baohanci.setObjectName('baohanci')
        self.verticalLayout_5.addLayout(self.baohanci)
        self.label_15 = _make_widget('label_15', Form)
        self.baohanci.addWidget(self.label_15)
        self.lineEdit_flow_fliter_words_contain = _make_widget('lineEdit_flow_fliter_words_contain', Form)
        self.baohanci.addWidget(self.lineEdit_flow_fliter_words_contain)
        self.paichuci = QtWidgets.QHBoxLayout()
        self.paichuci.setObjectName('paichuci')
        self.verticalLayout_5.addLayout(self.paichuci)
        self.label_151 = _make_widget('label_151', Form)
        self.paichuci.addWidget(self.label_151)
        self.lineEdit_flow_fliter_words_exclude = _make_widget('lineEdit_flow_fliter_words_exclude', Form)
        self.paichuci.addWidget(self.lineEdit_flow_fliter_words_exclude)
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
        self.cb_flow_ad_enable = _make_widget('cb_flow_ad_enable', Form)
        self.horizontalLayout_16.addWidget(self.cb_flow_ad_enable)
        self.cb_flow_ad_is_bottom_up = _make_widget('cb_flow_ad_is_bottom_up', Form)
        self.horizontalLayout_16.addWidget(self.cb_flow_ad_is_bottom_up)
        self.cb_flow_ad_delete = _make_widget('cb_flow_ad_delete', Form)
        self.horizontalLayout_16.addWidget(self.cb_flow_ad_delete)
        self.btn_flow_add_ad = _make_widget('btn_flow_add_ad', Form)
        self.horizontalLayout_16.addWidget(self.btn_flow_add_ad)
        self.listWidget_flow_private_ad_list = _make_widget('listWidget_flow_private_ad_list', Form)
        self.verticalLayout_7.addWidget(self.listWidget_flow_private_ad_list)
        self.anniu_qu = QtWidgets.QVBoxLayout()
        self.anniu_qu.setObjectName('anniu_qu')
        self.youbian.addLayout(self.anniu_qu)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName('horizontalLayout_17')
        self.anniu_qu.addLayout(self.horizontalLayout_17)
        self.lineEdit_priority = _make_widget('lineEdit_priority', Form)
        self.horizontalLayout_17.addWidget(self.lineEdit_priority)
        self.lineEdit_flow_item_name = _make_widget('lineEdit_flow_item_name', Form)
        self.horizontalLayout_17.addWidget(self.lineEdit_flow_item_name)
        self.btn_save_flow_item = _make_widget('btn_save_flow_item', Form)
        self.anniu_qu.addWidget(self.btn_save_flow_item)
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
        self.cb_auto_flow_pic_blur = _make_widget('cb_auto_flow_pic_blur', Form)
        self.horizontalLayout_18.addWidget(self.cb_auto_flow_pic_blur)
        self.cb_auto_flow_spoiler = _make_widget('cb_auto_flow_spoiler', Form)
        self.horizontalLayout_18.addWidget(self.cb_auto_flow_spoiler)
        self.btn_auto_flow_res_op_jiao_chen = _make_widget('btn_auto_flow_res_op_jiao_chen', Form)
        self.horizontalLayout_18.addWidget(self.btn_auto_flow_res_op_jiao_chen)
        self.auto_flow_pic_blur_radius = _make_widget('auto_flow_pic_blur_radius', Form)
        self.verticalLayout_12.addWidget(self.auto_flow_pic_blur_radius)
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setObjectName('verticalLayout_13')
        self.horizontalLayout_25.addLayout(self.verticalLayout_13)
        self.horizontalLayout_26 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_26.setObjectName('horizontalLayout_26')
        self.verticalLayout_13.addLayout(self.horizontalLayout_26)
        self.label_17 = _make_widget('label_17', Form)
        self.horizontalLayout_26.addWidget(self.label_17)
        self.btn_auto_grid_jiao_chen = _make_widget('btn_auto_grid_jiao_chen', Form)
        self.horizontalLayout_26.addWidget(self.btn_auto_grid_jiao_chen)
        self.lineEdit_auto_grid_number = _make_widget('lineEdit_auto_grid_number', Form)
        self.verticalLayout_13.addWidget(self.lineEdit_auto_grid_number)
        self.verticalLayout_14 = QtWidgets.QVBoxLayout()
        self.verticalLayout_14.setObjectName('verticalLayout_14')
        self.horizontalLayout_25.addLayout(self.verticalLayout_14)
        self.horizontalLayout_27 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_27.setObjectName('horizontalLayout_27')
        self.verticalLayout_14.addLayout(self.horizontalLayout_27)
        self.auto_cover_jiao_chen = _make_widget('auto_cover_jiao_chen', Form)
        self.horizontalLayout_27.addWidget(self.auto_cover_jiao_chen)
        self.cb_auto_random_cover = _make_widget('cb_auto_random_cover', Form)
        self.verticalLayout_14.addWidget(self.cb_auto_random_cover)
        self.verticalGroupBox = _make_widget('verticalGroupBox', Form)
        self.youbian.addWidget(self.verticalGroupBox)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName('verticalLayout_10')
        self.verticalGroupBox.setLayout(self.verticalLayout_10)
        self.horizontalLayout_181 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_181.setObjectName('horizontalLayout_181')
        self.verticalLayout_10.addLayout(self.horizontalLayout_181)
        self.cb_flow_pic_water = _make_widget('cb_flow_pic_water', Form)
        self.horizontalLayout_181.addWidget(self.cb_flow_pic_water)
        self.cb_flow_video_water = _make_widget('cb_flow_video_water', Form)
        self.horizontalLayout_181.addWidget(self.cb_flow_video_water)
        self.cb_flow_video_minute = _make_widget('cb_flow_video_minute', Form)
        self.horizontalLayout_181.addWidget(self.cb_flow_video_minute)
        self.cb_flow_water_mode = _make_widget('cb_flow_water_mode', Form)
        self.horizontalLayout_181.addWidget(self.cb_flow_water_mode)
        self.label_12 = _make_widget('label_12', Form)
        self.verticalLayout_10.addWidget(self.label_12)
        self.text_water_wrapper = _make_widget('text_water_wrapper', Form)
        self.verticalLayout_10.addWidget(self.text_water_wrapper)
        self.text_water_wrapper_xx = QtWidgets.QVBoxLayout()
        self.text_water_wrapper_xx.setObjectName('text_water_wrapper_xx')
        self.text_water_wrapper.setLayout(self.text_water_wrapper_xx)
        self.lineEdit_cb_water_text = _make_widget('lineEdit_cb_water_text', Form)
        self.text_water_wrapper_xx.addWidget(self.lineEdit_cb_water_text)
        self.pic_water_wrapper = _make_widget('pic_water_wrapper', Form)
        self.verticalLayout_10.addWidget(self.pic_water_wrapper)
        self.pic_water_wrapper_xx = QtWidgets.QHBoxLayout()
        self.pic_water_wrapper_xx.setObjectName('pic_water_wrapper_xx')
        self.pic_water_wrapper.setLayout(self.pic_water_wrapper_xx)
        self.btn_flow_water_pic_jiao_chen = _make_widget('btn_flow_water_pic_jiao_chen', Form)
        self.pic_water_wrapper_xx.addWidget(self.btn_flow_water_pic_jiao_chen)
        self.btn_flow_water_select_pic = _make_widget('btn_flow_water_select_pic', Form)
        self.pic_water_wrapper_xx.addWidget(self.btn_flow_water_select_pic)
        self.line_edit_auto_flow_water_pic_ratio = _make_widget('line_edit_auto_flow_water_pic_ratio', Form)
        self.pic_water_wrapper_xx.addWidget(self.line_edit_auto_flow_water_pic_ratio)
        self.label_flow_water_pic_path = _make_widget('label_flow_water_pic_path', Form)
        self.pic_water_wrapper_xx.addWidget(self.label_flow_water_pic_path)
        self.weiba_qu = _make_widget('weiba_qu', Form)
        self.youbian.addWidget(self.weiba_qu)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName('verticalLayout_2')
        self.weiba_qu.setLayout(self.verticalLayout_2)
        self.textEdit_flow_tail_text = _make_widget('textEdit_flow_tail_text', Form)
        self.verticalLayout_2.addWidget(self.textEdit_flow_tail_text)
        self.verticalGroupBox1 = _make_widget('verticalGroupBox1', Form)
        self.youbian.addWidget(self.verticalGroupBox1)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName('verticalLayout_8')
        self.verticalGroupBox1.setLayout(self.verticalLayout_8)
        self.textEdit_flow_replace_rule = _make_widget('textEdit_flow_replace_rule', Form)
        self.verticalLayout_8.addWidget(self.textEdit_flow_replace_rule)
        self.ai_employee_qu = _make_widget('ai_employee_qu', Form)
        self.youbian.addWidget(self.ai_employee_qu)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName('verticalLayout_6')
        self.ai_employee_qu.setLayout(self.verticalLayout_6)
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setObjectName('horizontalLayout_19')
        self.verticalLayout_6.addLayout(self.horizontalLayout_19)
        self.checkBox_auto_ai_enable = _make_widget('checkBox_auto_ai_enable', Form)
        self.horizontalLayout_19.addWidget(self.checkBox_auto_ai_enable)
        self.label_auto_ai_name = _make_widget('label_auto_ai_name', Form)
        self.horizontalLayout_19.addWidget(self.label_auto_ai_name)
        self.btn_auto_select_ai_em = _make_widget('btn_auto_select_ai_em', Form)
        self.horizontalLayout_19.addWidget(self.btn_auto_select_ai_em)
        self.horizontalGroupBox_ai_auto = _make_widget('horizontalGroupBox_ai_auto', Form)
        self.verticalLayout_6.addWidget(self.horizontalGroupBox_ai_auto)
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_24.setObjectName('horizontalLayout_24')
        self.horizontalGroupBox_ai_auto.setLayout(self.horizontalLayout_24)
        self.label_131 = _make_widget('label_131', Form)
        self.horizontalLayout_24.addWidget(self.label_131)
        self.radioButton_ai_auto_use_source = _make_widget('radioButton_ai_auto_use_source', Form)
        self.horizontalLayout_24.addWidget(self.radioButton_ai_auto_use_source)
        self.radioButton_ai_auto_skip_source = _make_widget('radioButton_ai_auto_skip_source', Form)
        self.horizontalLayout_24.addWidget(self.radioButton_ai_auto_skip_source)
        self.huiyuan_quyu = _make_widget('huiyuan_quyu', Form)
        self.youbian.addWidget(self.huiyuan_quyu)
        self.verticalLayout_31 = QtWidgets.QVBoxLayout()
        self.verticalLayout_31.setObjectName('verticalLayout_31')
        self.huiyuan_quyu.setLayout(self.verticalLayout_31)
        self.horizontalLayout_41 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_41.setObjectName('horizontalLayout_41')
        self.verticalLayout_31.addLayout(self.horizontalLayout_41)
        self.cb_flow_hui_yuan_link = _make_widget('cb_flow_hui_yuan_link', Form)
        self.horizontalLayout_41.addWidget(self.cb_flow_hui_yuan_link)
        self.cb_flow_hui_yuan_customer_link = _make_widget('cb_flow_hui_yuan_customer_link', Form)
        self.horizontalLayout_41.addWidget(self.cb_flow_hui_yuan_customer_link)
        self.cb_flow_hui_yuan_link_bq = _make_widget('cb_flow_hui_yuan_link_bq', Form)
        self.horizontalLayout_41.addWidget(self.cb_flow_hui_yuan_link_bq)
        self.btn_flow_hui_yuan_link_jc = _make_widget('btn_flow_hui_yuan_link_jc', Form)
        self.horizontalLayout_41.addWidget(self.btn_flow_hui_yuan_link_jc)
        self.lineEdit_flow_hui_yuan_tip_text = _make_widget('lineEdit_flow_hui_yuan_tip_text', Form)
        self.verticalLayout_31.addWidget(self.lineEdit_flow_hui_yuan_tip_text)
        self.lineEdit_flow_hui_yuan_tip_text_link = _make_widget('lineEdit_flow_hui_yuan_tip_text_link', Form)
        self.verticalLayout_31.addWidget(self.lineEdit_flow_hui_yuan_tip_text_link)
        self.youkke_quyu = _make_widget('youkke_quyu', Form)
        self.youbian.addWidget(self.youkke_quyu)
        self.verticalLayout_61 = QtWidgets.QVBoxLayout()
        self.verticalLayout_61.setObjectName('verticalLayout_61')
        self.youkke_quyu.setLayout(self.verticalLayout_61)
        self.horizontalLayout_51 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_51.setObjectName('horizontalLayout_51')
        self.verticalLayout_61.addLayout(self.horizontalLayout_51)
        self.cb_flow_you_ke_link = _make_widget('cb_flow_you_ke_link', Form)
        self.horizontalLayout_51.addWidget(self.cb_flow_you_ke_link)
        self.cb_flow_you_ke_link_bq = _make_widget('cb_flow_you_ke_link_bq', Form)
        self.horizontalLayout_51.addWidget(self.cb_flow_you_ke_link_bq)
        self.btn_flow_you_ke_link_jc = _make_widget('btn_flow_you_ke_link_jc', Form)
        self.horizontalLayout_51.addWidget(self.btn_flow_you_ke_link_jc)
        self.lineEdit_flow_you_ke_tip_text = _make_widget('lineEdit_flow_you_ke_tip_text', Form)
        self.verticalLayout_61.addWidget(self.lineEdit_flow_you_ke_tip_text)
        self.lineEdit_flow_you_ke_tip_text_link = _make_widget('lineEdit_flow_you_ke_tip_text_link', Form)
        self.verticalLayout_61.addWidget(self.lineEdit_flow_you_ke_tip_text_link)
        self.horizontalGroupBox_auto = _make_widget('horizontalGroupBox_auto', Form)
        self.youbian.addWidget(self.horizontalGroupBox_auto)
        self.horizontalLayout_71 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_71.setObjectName('horizontalLayout_71')
        self.horizontalGroupBox_auto.setLayout(self.horizontalLayout_71)
        self.checkBox_auto_add_duration_info = _make_widget('checkBox_auto_add_duration_info', Form)
        self.horizontalLayout_71.addWidget(self.checkBox_auto_add_duration_info)
        self.checkBox_auto_add_duration_info_bq = _make_widget('checkBox_auto_add_duration_info_bq', Form)
        self.horizontalLayout_71.addWidget(self.checkBox_auto_add_duration_info_bq)
        self.btn_show_duration_dialog = _make_widget('btn_show_duration_dialog', Form)
        self.horizontalLayout_71.addWidget(self.btn_show_duration_dialog)
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
        self.lineEdit_flow_source.setPlaceholderText(_translate('Form', '公有链接或私有ID(支持话题)'))
        self.auto_flow_topic_jiao_chen.setText(_translate('Form', '教程'))
        self.pushButton_auto_step1.setText(_translate('Form', '第一步、搬运到私密会员频道'))
        self.label_2.setText(_translate('Form', '会员目标频道/群组(支持多个，一行一个，支持话题)'))
        self.textEdit_flow_dest_list.setPlaceholderText(_translate('Form', '公有链接或私有ID（支持多个，一行一个，支持话题）'))
        self.pushButton_auto_step2.setText(_translate('Form', '第二步、自动生成预览资源，并发布到公开预览频道'))
        self.label_4.setText(_translate('Form', '公开预览频道/群组(支持多个，一行一个，支持话题)'))
        self.textEdit_flow_auto_flow_dest_list.setPlaceholderText(_translate('Form', '公有链接或私有ID（支持多个，一行一个，支持话题）'))
        self.ziyuanleiixing.setTitle(_translate('Form', '资源类型'))
        self.checkBox_flow_video_photo.setText(_translate('Form', '仅包含视频的消息组'))
        self.checkBox_flow_photo.setText(_translate('Form', '图片'))
        self.checkBox_flow_video.setText(_translate('Form', '视频'))
        self.checkBox_flow_file.setText(_translate('Form', '文件'))
        self.checkBox_flow_text.setText(_translate('Form', '纯文本'))
        self.auto_res_btn_jiao_chen.setText(_translate('Form', '教程'))
        self.groupBox.setTitle(_translate('Form', '预览频道发布资源类型'))
        self.checkBox_pb_auto_flow_picture.setText(_translate('Form', '图片'))
        self.checkBox_pb_auto_flow_video.setText(_translate('Form', '视频'))
        self.yulan_qu.setTitle(_translate('Form', '预览视频规则'))
        self.comboBox_auto_flow_select_auto_flow_mode.setItemText(0, _translate('Form', '按比例模式'))
        self.comboBox_auto_flow_select_auto_flow_mode.setItemText(1, _translate('Form', '自定义时长模式'))
        self.radioButton_auto_flow_10.setText(_translate('Form', '10%'))
        self.radioButton_auto_flow_20.setText(_translate('Form', '20%'))
        self.radioButton_auto_flow_30.setText(_translate('Form', '30%'))
        self.radioButton_auto_flow_customer.setText(_translate('Form', '自定义'))
        self.lineEdit_auto_flow_customer.setPlaceholderText(_translate('Form', '自定义比例1~99'))
        self.label_21.setText(_translate('Form', '自定义时长(单位秒钟)：'))
        self.lineEdit_auto_flow_min_duration.setPlaceholderText(_translate('Form', '最小值'))
        self.label_13.setText(_translate('Form', '~'))
        self.lineEdit_auto_flow_max_duration.setPlaceholderText(_translate('Form', '最大值'))
        self.zhuanfa.setTitle(_translate('Form', '搬运方式'))
        self.radioButton_auto_flow_action_download.setText(_translate('Form', '强制下载方式'))
        self.radioButton_auto_flow_action_auto.setText(_translate('Form', '自动方式'))
        self.lineEdit_auto_flow_sleep_min.setPlaceholderText(_translate('Form', '间隔最小值'))
        self.label_14.setText(_translate('Form', '~'))
        self.lineEdit_auto_flow_sleep_max.setPlaceholderText(_translate('Form', '间隔最大值'))
        self.btn_auto_flow_action_jiao_chen.setText(_translate('Form', '教程'))
        self.moshi_xuanze.setTitle(_translate('Form', '模式选择'))
        self.comboBox_flow_select_mode.setItemText(0, _translate('Form', '顺序模式'))
        self.comboBox_flow_select_mode.setItemText(1, _translate('Form', '随机模式'))
        self.comboBox_flow_select_mode.setItemText(2, _translate('Form', '循环模式'))
        self.random_com.setTitle(_translate('Form', '随机模式参数'))
        self.label_3.setText(_translate('Form', '期望数量'))
        self.lineEdit_flow_random_want_count.setPlaceholderText(_translate('Form', '填写整数'))
        self.comboBox_flow_number_random_dan_wei.setItemText(0, _translate('Form', '按组计算'))
        self.comboBox_flow_number_random_dan_wei.setItemText(1, _translate('Form', '按个计算'))
        self.increase_com.setTitle(_translate('Form', '顺序模式参数（包括开始ID）'))
        self.label_7.setText(_translate('Form', '开始ID'))
        self.lineEdit_flow_increase_start_id.setPlaceholderText(_translate('Form', '填写整数'))
        self.label_6.setText(_translate('Form', '期望数量'))
        self.lineEdit_flow_increase_want_count.setPlaceholderText(_translate('Form', '填写整数'))
        self.comboBox_flow_number_dan_wei.setCurrentText(_translate('Form', '按组计算'))
        self.comboBox_flow_number_dan_wei.setItemText(0, _translate('Form', '按组计算'))
        self.comboBox_flow_number_dan_wei.setItemText(1, _translate('Form', '按个计算'))
        self.loop_com.setTitle(_translate('Form', '循环模式参数（包括开始ID，不包括结束ID）'))
        self.label_8.setText(_translate('Form', '开始ID'))
        self.lineEdit_flow_loop_start_id.setPlaceholderText(_translate('Form', '填写整数'))
        self.label_5.setText(_translate('Form', '结束ID'))
        self.lineEdit_flow_loop_end_id.setPlaceholderText(_translate('Form', '填写整数'))
        self.jichu_filter.setTitle(_translate('Form', '基础条件(如果是视频资源，则需要同时满足时长和大小)'))
        self.label_41.setText(_translate('Form', '时长过滤(单位分钟)：'))
        self.lineEdit_auto_duration_min.setPlaceholderText(_translate('Form', '最小值'))
        self.label_10.setText(_translate('Form', '~'))
        self.lineEdit_auto_duration_max.setPlaceholderText(_translate('Form', '最大值'))
        self.label_9.setText(_translate('Form', '大小过滤(单位 MB )：'))
        self.lineEdit_auto_mb_min.setPlaceholderText(_translate('Form', '最小值'))
        self.label_11.setText(_translate('Form', '~'))
        self.lineEdit_auto_mb_max.setPlaceholderText(_translate('Form', '最大值'))
        self.ziyuanguolu.setTitle(_translate('Form', '资源过滤条件'))
        self.cb_flow_dele_source_text.setText(_translate('Form', '丢弃资源自带的文本'))
        self.checkBox_discard_no_text_resource.setText(_translate('Form', '丢弃无文本的资源'))
        self.cb_flow_fliter_button.setText(_translate('Form', '丢弃带按钮的资源'))
        self.cb_flow_dele_link.setText(_translate('Form', '删除源文本中的外链'))
        self.cb_flow_origin_source_text.setText(_translate('Form', '原样文本搬运'))
        self.checkBox_chai_zu.setText(_translate('Form', '根据大小时长拆组'))
        self.label_15.setText(_translate('Form', '包含关键词的资源'))
        self.lineEdit_flow_fliter_words_contain.setPlaceholderText(_translate('Form', '填写关键词，多个词使用竖线"|"分割'))
        self.label_151.setText(_translate('Form', '排除关键词的资源'))
        self.lineEdit_flow_fliter_words_exclude.setPlaceholderText(_translate('Form', '填写关键词，多个词使用竖线"|"分割'))
        self.verticalGroupBox_yulan_op.setTitle(_translate('Form', '预览频道资源处理（可选）'))
        self.cb_auto_flow_pic_blur.setText(_translate('Form', '图片模糊'))
        self.cb_auto_flow_spoiler.setText(_translate('Form', '防剧透'))
        self.btn_auto_flow_res_op_jiao_chen.setText(_translate('Form', '教程'))
        self.auto_flow_pic_blur_radius.setPlaceholderText(_translate('Form', '1~20数字越大越模糊'))
        self.label_17.setText(_translate('Form', '消息组宫格补齐'))
        self.btn_auto_grid_jiao_chen.setText(_translate('Form', '教程'))
        self.lineEdit_auto_grid_number.setPlaceholderText(_translate('Form', '填写0~10的整数'))
        self.cb_auto_random_cover.setText(_translate('Form', '随机封面'))
        self.auto_cover_jiao_chen.setText(_translate('Form', '教程'))
        self.verticalGroupBox.setTitle(_translate('Form', '水印（可选，仅仅对发布到预览频道的资源生效）'))
        self.label_12.setText(_translate('Form', '图片水印或者视频动态水印'))
        self.cb_flow_pic_water.setText(_translate('Form', '图片水印'))
        self.cb_flow_video_water.setText(_translate('Form', '视频水印'))
        self.cb_flow_video_minute.setItemText(0, _translate('Form', '1分钟内视频'))
        self.cb_flow_video_minute.setItemText(1, _translate('Form', '3分钟内视频'))
        self.cb_flow_video_minute.setItemText(2, _translate('Form', '5分钟内视频'))
        self.cb_flow_video_minute.setItemText(3, _translate('Form', '10分钟内视频'))
        self.cb_flow_video_minute.setItemText(4, _translate('Form', '30分钟内视频'))
        self.cb_flow_video_minute.setItemText(5, _translate('Form', '60分钟内视频'))
        self.cb_flow_video_minute.setItemText(6, _translate('Form', '90分钟内视频'))
        self.cb_flow_video_minute.setItemText(7, _translate('Form', '120分钟内视频'))
        self.cb_flow_video_minute.setItemText(8, _translate('Form', '150分钟内视频'))
        self.cb_flow_water_mode.setItemText(0, _translate('Form', '图片水印'))
        self.cb_flow_water_mode.setItemText(1, _translate('Form', '文字水印'))
        self.lineEdit_cb_water_text.setPlaceholderText(_translate('Form', '水印文字，支持中文，英文'))
        self.btn_flow_water_pic_jiao_chen.setText(_translate('Form', '教程'))
        self.btn_flow_water_select_pic.setText(_translate('Form', '选择图片'))
        self.line_edit_auto_flow_water_pic_ratio.setPlaceholderText(_translate('Form', '30'))
        self.label_flow_water_pic_path.setText(_translate('Form', '图片路径：'))
        self.weiba_qu.setTitle(_translate('Form', '尾巴（可选，仅仅对发布到预览频道的资源生效）'))
        self.textEdit_flow_tail_text.setPlaceholderText(_translate('Form', '尾巴文案，支持html格式和电报会员表情'))
        self.verticalGroupBox1.setTitle(_translate('Form', '替换规则（可选，咨询客服如何编辑）'))
        self.textEdit_flow_replace_rule.setPlaceholderText(_translate('Form', '源词->目标词（中间使用英文输入法的->分割）'))
        self.ai_employee_qu.setTitle(_translate('Form', 'AI员工（可选，AI文案同义转换）'))
        self.checkBox_auto_ai_enable.setText(_translate('Form', '启用AI文案'))
        self.label_auto_ai_name.setText(_translate('Form', '当前选择：xxx'))
        self.btn_auto_select_ai_em.setText(_translate('Form', '选择AI员工'))
        self.label_131.setText(_translate('Form', 'AI拒绝生成文案时候：'))
        self.radioButton_ai_auto_use_source.setText(_translate('Form', '使用源文案'))
        self.radioButton_ai_auto_skip_source.setText(_translate('Form', '跳过此资源'))
        self.huiyuan_quyu.setTitle(_translate('Form', '会员超级链接配置（可选，仅仅对发布到预览频道的资源生效）'))
        self.cb_flow_hui_yuan_link.setText(_translate('Form', '启用会员超级链接'))
        self.cb_flow_hui_yuan_customer_link.setText(_translate('Form', '自定义会员超级链接'))
        self.cb_flow_hui_yuan_link_bq.setText(_translate('Form', 'BQ字体'))
        self.btn_flow_hui_yuan_link_jc.setText(_translate('Form', '教程'))
        self.lineEdit_flow_hui_yuan_tip_text.setPlaceholderText(_translate('Form', '请配置会员提示文案'))
        self.lineEdit_flow_hui_yuan_tip_text_link.setPlaceholderText(_translate('Form', '请配置会员的超级链接（可选）'))
        self.youkke_quyu.setTitle(_translate('Form', '游客超级链接配置（可选，仅仅对发布到预览频道的资源生效）'))
        self.cb_flow_you_ke_link.setText(_translate('Form', '启用游客超级链接'))
        self.cb_flow_you_ke_link_bq.setText(_translate('Form', 'BQ字体'))
        self.btn_flow_you_ke_link_jc.setText(_translate('Form', '教程'))
        self.lineEdit_flow_you_ke_tip_text.setPlaceholderText(_translate('Form', '请配置游客提示文案'))
        self.lineEdit_flow_you_ke_tip_text_link.setPlaceholderText(_translate('Form', '请配置游客的超级链接'))
        self.checkBox_auto_add_duration_info.setText(_translate('Form', '添加原视频时长信息'))
        self.checkBox_auto_add_duration_info_bq.setText(_translate('Form', 'BQ字体'))
        self.btn_show_duration_dialog.setText(_translate('Form', '教程'))
        self.horizontalGroupBox_4.setTitle(_translate('Form', '私有广告（可选，仅仅对发布到预览频道的资源生效）'))
        self.cb_flow_ad_enable.setText(_translate('Form', '启用广告'))
        self.cb_flow_ad_is_bottom_up.setText(_translate('Form', '置底广告'))
        self.cb_flow_ad_delete.setText(_translate('Form', '删除历史广告'))
        self.btn_flow_add_ad.setText(_translate('Form', '添加广告'))
        self.lineEdit_priority.setPlaceholderText(_translate('Form', '优先级'))
        self.lineEdit_flow_item_name.setPlaceholderText(_translate('Form', '请输入自动流的名字'))
        self.btn_save_flow_item.setText(_translate('Form', '保存'))

