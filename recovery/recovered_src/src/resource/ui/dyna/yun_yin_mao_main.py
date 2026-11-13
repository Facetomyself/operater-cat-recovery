# Recovered module: src.resource.ui.dyna.yun_yin_mao_main
#
# The original main-window .ui file is not shipped in the distribution.
# This reconstruction follows the recovered Qt constructor graph:
# 161 widgets, 56 layout edges and the four top-level tabs.
from __future__ import annotations

from PyQt5 import QtCore, QtWidgets


WIDGET_NAMES = (
    'lb_display_txt',
    'main_expri_permission',
    'label_env_show',
    'btn_kefu_link',
    'cb_enable_proxy',
    'btn_proxy_setting',
    'label_version_grade',
    'tabWidget_important',
    'btn_clear_log',
    'btn_copy_log',
    'btn_open_log_folder',
    'btn_open_down_load_folder',
    'lineEdit_text_biao_shi',
    'btn_close_left',
    'btn_close_right',
    'btn_expand_log',
    'text_brow_log',
    'action_copy_code',
    'action_dev',
    'action_reset',
    'api_fun',
    'label_22',
    'label_23',
    'lineEdit_api_app_id',
    'label_24',
    'lineEdit_api_app_hash',
    'btn_save_app_config',
    'label_25',
    'btn_go_to_link',
    'line_2',
    'line_3',
    'centralwidget',
    'gen_session',
    'groupBox_5',
    'label_30',
    'label_38',
    'label_18',
    'lineEdit_input_phone',
    'btn_send_yan_zhen_ma',
    'lineEdit_yan_zhen_ma',
    'lineEdit_two_pass_word',
    'btn_login_gen_session',
    'label_5',
    'listWidget_account_list',
    'btn_refresh_account',
    'btn_net_test',
    'menu',
    'menu_operation',
    'menubar',
    'scrollAreaWidgetContents',
    'label_monitor_text',
    'tab',
    'zuobian_widget',
    'label_6',
    'btn_auto_add_down_load',
    'btn_auto_add_item',
    'btn_auto_add_yulan',
    'btn_auto_add_flow',
    'btn_auto_add_yun_preview',
    'btn_auto_add_yun_auto',
    'btn_auto_add_unkown1',
    'btn_auto_add_unkown2',
    'checkBox_auto_selected_all',
    'btn_copy_format_text',
    'main_btn_items_jiao_chen',
    'listWidget_auto_list',
    'youbian_widget',
    'youbian_top_one',
    'verticalGroupBox',
    'checkBox_g_pic_water',
    'checkBox_g_video_water',
    'comboBox_g_video_minute',
    'cb_g_water_mode',
    'label_12',
    'text_water_wrapper',
    'lineEdit_g_water_text',
    'pic_water_wrapper',
    'btn_g_water_pic_jiao_chen',
    'btn_g_water_select_pic',
    'line_edit_g_water_pic_ratio',
    'label_g_water_pic_path',
    'guanggao',
    'checkBox_enable_global_ad',
    'checkBox_global_ad_is_bottom_up',
    'checkBox_global_ad_delete',
    'btn_add_g_ad',
    'listWidget_g_ad_list',
    'zhanghao',
    'btn_auto_select_session',
    'label_4',
    'label_current_session',
    'checkBox_check_post_permission',
    'label',
    'lineEdit_down_load_rate',
    'lineEdit_up_load_rate',
    'checkBox_auto_changed_rate',
    'btn_show_how',
    'jichu_option',
    'checkBox_delete_temp_files',
    'btn_changed_folder',
    'label_folder_text',
    'comboBox_wrapper',
    'comboBox_dingshi_monitor',
    'main_ban_yun_monitor_jiao_chen',
    'youbian_top_two',
    'dingshi_container',
    'dingshi',
    'checkBox0',
    'checkBox1',
    'checkBox2',
    'checkBox3',
    'checkBox4',
    'checkBox5',
    'checkBox6',
    'checkBox7',
    'checkBox8',
    'checkBox9',
    'checkBox10',
    'checkBox11',
    'checkBox12',
    'checkBox13',
    'checkBox14',
    'checkBox15',
    'checkBox16',
    'checkBox17',
    'checkBox18',
    'checkBox19',
    'checkBox20',
    'checkBox21',
    'checkBox22',
    'checkBox23',
    'ban_yun_cao_zuo_qu',
    'btn_auto_yun_yin_start',
    'btn_auto_yun_yin_run_one_and_start',
    'btn_auto_yun_yin_run_one',
    'btn_auto_yun_yin_stop',
    'monitor_container',
    'label_monitor_tip',
    'scrollArea',
    'btn_start_monitor',
    'btn_stop_monitor',
    'btn_open_close_big_show',
    'tools',
    'verticalGroupBox_3',
    'tools_btn_gen_html',
    'tools_box_ad_jiao_chen',
    'label_2',
    'lineEdit_tools_post_link',
    'horizontalGroupBox',
    'label_ad_config_tip',
    'tools_btn_edit_ad',
    'tools_btn_post_ad',
    'lineEdit_ad_post_source',
    'verticalGroupBox_2',
    'cb_cover_expri',
    'cb_cover_item_yun',
    'btn_qian_yi_jiao_chen',
    'label_3',
    'label_7',
    'lineEdit_old_u_code',
    'lineEdit_new_u_code',
    'tools_move_permission',
)


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
    if 'g_video_minute' in lower:
        combo.addItems([''] * 9)
    elif 'water_mode' in lower:
        combo.addItems(['图片水印', '文字水印'])
    elif 'dingshi_monitor' in lower:
        combo.addItems([''] * 2)
    elif 'video_minute' in lower:
        for text, value in (
            ('不限制', 0), ('15分钟', 15), ('30分钟', 30), ('60分钟', 60),
        ):
            combo.addItem(text, value)
        combo.setCurrentIndex(3)


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
    elif kind == 'QFrame':
        widget = QtWidgets.QFrame(parent)
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
    'lb_display_txt': 'QLabel',
    'main_expri_permission': 'QPushButton',
    'label_env_show': 'QLabel',
    'btn_kefu_link': 'QPushButton',
    'cb_enable_proxy': 'QCheckBox',
    'btn_proxy_setting': 'QPushButton',
    'label_version_grade': 'QLabel',
    'tabWidget_important': 'QTabWidget',
    'btn_clear_log': 'QPushButton',
    'btn_copy_log': 'QPushButton',
    'btn_open_log_folder': 'QPushButton',
    'btn_open_down_load_folder': 'QPushButton',
    'lineEdit_text_biao_shi': 'QLineEdit',
    'btn_close_left': 'QPushButton',
    'btn_close_right': 'QPushButton',
    'btn_expand_log': 'QPushButton',
    'text_brow_log': 'QTextBrowser',
    'action_copy_code': 'QAction',
    'action_dev': 'QAction',
    'action_reset': 'QAction',
    'api_fun': 'QWidget',
    'label_22': 'QLabel',
    'label_23': 'QLabel',
    'lineEdit_api_app_id': 'QLineEdit',
    'label_24': 'QLabel',
    'lineEdit_api_app_hash': 'QLineEdit',
    'btn_save_app_config': 'QPushButton',
    'label_25': 'QLabel',
    'btn_go_to_link': 'QWidget',
    'line_2': 'QFrame',
    'line_3': 'QFrame',
    'centralwidget': 'QWidget',
    'gen_session': 'QWidget',
    'groupBox_5': 'QGroupBox',
    'label_30': 'QLabel',
    'label_38': 'QLabel',
    'label_18': 'QLabel',
    'lineEdit_input_phone': 'QLineEdit',
    'btn_send_yan_zhen_ma': 'QPushButton',
    'lineEdit_yan_zhen_ma': 'QLineEdit',
    'lineEdit_two_pass_word': 'QLineEdit',
    'btn_login_gen_session': 'QPushButton',
    'label_5': 'QLabel',
    'listWidget_account_list': 'QListWidget',
    'btn_refresh_account': 'QPushButton',
    'btn_net_test': 'QPushButton',
    'menu': 'QMenu',
    'menu_operation': 'QMenu',
    'menubar': 'QMenuBar',
    'scrollAreaWidgetContents': 'QWidget',
    'label_monitor_text': 'QLabel',
    'tab': 'QWidget',
    'zuobian_widget': 'QWidget',
    'label_6': 'QLabel',
    'btn_auto_add_down_load': 'QPushButton',
    'btn_auto_add_item': 'QPushButton',
    'btn_auto_add_yulan': 'QPushButton',
    'btn_auto_add_flow': 'QPushButton',
    'btn_auto_add_yun_preview': 'QPushButton',
    'btn_auto_add_yun_auto': 'QPushButton',
    'btn_auto_add_unkown1': 'QPushButton',
    'btn_auto_add_unkown2': 'QPushButton',
    'checkBox_auto_selected_all': 'QCheckBox',
    'btn_copy_format_text': 'QPushButton',
    'main_btn_items_jiao_chen': 'QPushButton',
    'listWidget_auto_list': 'QListWidget',
    'youbian_widget': 'QWidget',
    'youbian_top_one': 'QFrame',
    'verticalGroupBox': 'QGroupBox',
    'checkBox_g_pic_water': 'QCheckBox',
    'checkBox_g_video_water': 'QCheckBox',
    'comboBox_g_video_minute': 'QComboBox',
    'cb_g_water_mode': 'QComboBox',
    'label_12': 'QLabel',
    'text_water_wrapper': 'QGroupBox',
    'lineEdit_g_water_text': 'QLineEdit',
    'pic_water_wrapper': 'QGroupBox',
    'btn_g_water_pic_jiao_chen': 'QPushButton',
    'btn_g_water_select_pic': 'QPushButton',
    'line_edit_g_water_pic_ratio': 'QLineEdit',
    'label_g_water_pic_path': 'QLabel',
    'guanggao': 'QGroupBox',
    'checkBox_enable_global_ad': 'QCheckBox',
    'checkBox_global_ad_is_bottom_up': 'QCheckBox',
    'checkBox_global_ad_delete': 'QCheckBox',
    'btn_add_g_ad': 'QPushButton',
    'listWidget_g_ad_list': 'QListWidget',
    'zhanghao': 'QGroupBox',
    'btn_auto_select_session': 'QPushButton',
    'label_4': 'QLabel',
    'label_current_session': 'QLabel',
    'checkBox_check_post_permission': 'QCheckBox',
    'label': 'QLabel',
    'lineEdit_down_load_rate': 'QLineEdit',
    'lineEdit_up_load_rate': 'QLineEdit',
    'checkBox_auto_changed_rate': 'QCheckBox',
    'btn_show_how': 'QPushButton',
    'jichu_option': 'QGroupBox',
    'checkBox_delete_temp_files': 'QCheckBox',
    'btn_changed_folder': 'QPushButton',
    'label_folder_text': 'QLabel',
    'comboBox_wrapper': 'QFrame',
    'comboBox_dingshi_monitor': 'QComboBox',
    'main_ban_yun_monitor_jiao_chen': 'QPushButton',
    'youbian_top_two': 'QFrame',
    'dingshi_container': 'QGroupBox',
    'dingshi': 'QGroupBox',
    'checkBox0': 'QCheckBox',
    'checkBox1': 'QCheckBox',
    'checkBox2': 'QCheckBox',
    'checkBox3': 'QCheckBox',
    'checkBox4': 'QCheckBox',
    'checkBox5': 'QCheckBox',
    'checkBox6': 'QCheckBox',
    'checkBox7': 'QCheckBox',
    'checkBox8': 'QCheckBox',
    'checkBox9': 'QCheckBox',
    'checkBox10': 'QCheckBox',
    'checkBox11': 'QCheckBox',
    'checkBox12': 'QCheckBox',
    'checkBox13': 'QCheckBox',
    'checkBox14': 'QCheckBox',
    'checkBox15': 'QCheckBox',
    'checkBox16': 'QCheckBox',
    'checkBox17': 'QCheckBox',
    'checkBox18': 'QCheckBox',
    'checkBox19': 'QCheckBox',
    'checkBox20': 'QCheckBox',
    'checkBox21': 'QCheckBox',
    'checkBox22': 'QCheckBox',
    'checkBox23': 'QCheckBox',
    'ban_yun_cao_zuo_qu': 'QWidget',
    'btn_auto_yun_yin_start': 'QPushButton',
    'btn_auto_yun_yin_run_one_and_start': 'QPushButton',
    'btn_auto_yun_yin_run_one': 'QPushButton',
    'btn_auto_yun_yin_stop': 'QPushButton',
    'monitor_container': 'QGroupBox',
    'label_monitor_tip': 'QLabel',
    'scrollArea': 'QScrollArea',
    'btn_start_monitor': 'QPushButton',
    'btn_stop_monitor': 'QPushButton',
    'btn_open_close_big_show': 'QPushButton',
    'tools': 'QWidget',
    'verticalGroupBox_3': 'QGroupBox',
    'tools_btn_gen_html': 'QPushButton',
    'tools_box_ad_jiao_chen': 'QPushButton',
    'label_2': 'QLabel',
    'lineEdit_tools_post_link': 'QLineEdit',
    'horizontalGroupBox': 'QGroupBox',
    'label_ad_config_tip': 'QLabel',
    'tools_btn_edit_ad': 'QPushButton',
    'tools_btn_post_ad': 'QPushButton',
    'lineEdit_ad_post_source': 'QLineEdit',
    'verticalGroupBox_2': 'QGroupBox',
    'cb_cover_expri': 'QCheckBox',
    'cb_cover_item_yun': 'QCheckBox',
    'btn_qian_yi_jiao_chen': 'QPushButton',
    'label_3': 'QLabel',
    'label_7': 'QLabel',
    'lineEdit_old_u_code': 'QLineEdit',
    'lineEdit_new_u_code': 'QLineEdit',
    'tools_move_permission': 'QPushButton',
}


_SIZE_CONSTRAINTS = {
    'api_fun': {'setMaximumSize': [150, 50], 'setMinimumSize': [0, 0]},
    'ban_yun_cao_zuo_qu': {'setMinimumSize': [0, 20], 'setMaximumSize': [16777215, 40]},
    'centralwidget': {'setMaximumSize': [260, 50], 'setMinimumSize': [0, 50]},
    'comboBox_wrapper': {'setMaximumSize': [16777215, 30]},
    'gen_session': {'setMaximumSize': [16777215, 50]},
    'groupBox_5': {'setMaximumSize': [16777215, 40], 'setMinimumSize': [180, 35]},
    'guanggao': {'setMaximumSize': [16777215, 70]},
    'horizontalGroupBox': {'setMinimumSize': [200, 40], 'setMaximumSize': [600, 16777215]},
    'monitor_container': {'setMinimumSize': [0, 20], 'setMaximumSize': [16777215, 40]},
    'pic_water_wrapper': {'setMaximumSize': [30, 16777215]},
    'verticalGroupBox_2': {'setMinimumSize': [0, 40], 'setMaximumSize': [200, 16777215]},
    'verticalGroupBox_3': {'setMinimumSize': [30, 0], 'setMaximumSize': [400, 16777215]},
    'zhanghao': {'setMaximumSize': [16777215, 16777215]},
    'zuobian_widget': {'setMaximumSize': [16777215, 16777215]},
}


class Ui_MainWindow:
    def setupUi(self, MainWindow):
        MainWindow.setObjectName('MainWindow')
        MainWindow.resize(984, 970)
        MainWindow.setStyleSheet('*{\nbackground-color:#3c3f42;\ncolor: #e6e6e6;\n}\n\n*:disabled {\n    background-color: #3c3f42;\n    color: #afafaf;\n    cursor: not-allowed;\n\n}\nQListWidget:disabled,QTextEdit:disabled,QLineEdit:disabled,QTabWidget:disabled{\nbackground-color:rgb(40, 40, 40);\n}\nQTextBrowser:disabled{\nbackground-color:rgb(40, 40, 40);\ncolor: rgb(152, 197, 150);\n}\n\nQPushButton:disabled {\n    background-color: rgb(80, 80, 80);\n    color: #afafaf;\n    cursor: not-allowed;\n\n}\n\nQCheckBox:hover,QRadioButton:hover {\ncolor: white;\n}\n\nQPushButton:hover {\n\nfont-weight: bold;\nbackground-color:rgb(84, 84, 84);\ncolor: white;\nborder-radius: 2pt;\n\n}\n\nQPushButton{\nfont-weight: bold;\nbackground-color:rgb(106, 106, 106);\ncolor: #e6e6e6;\nborder-radius: 2pt;\n}\n\nQTextBrowser,QListWidget,QTextEdit,QLineEdit,QTabWidget{\nbackground-color:rgb(40, 40, 40);\ncolor: rgba(152, 197, 150, 185);\nfont-size:12pt;\n}\n\nQTextBrowser:hover,QTextEdit:hover,QLineEdit:hover{\nbackground-color:rgb(40, 40, 40);\ncolor: rgb(152, 197, 150);\nfont-size:12pt;\n}\n\n\nQLabel{\ncolor: #ebf905;\n}\n\n\n\nQRadioButton,QCheckBox {\n        border: none;\n        border-radius: 9px;\n}\nQRadioButton::indicator,QCheckBox::indicator{\n    background-color: rgb(42, 45, 66);\n    border: 0px solid #b1b1b1;\n    width: 18px;\n    height: 18px;\n    border-radius: 9px;\n}\n\nQRadioButton::indicator:checked,QCheckBox::indicator:checked {\n    background-color: #ebf905;\n    border-color: #ebf905;\n}\n\nQMenuBar { background-color: transparent; }\nQMenuBar::item { background-color: transparent; }\nQMenuBar::item:selected { background-color:transparent; color: #ffffff;}\nQMenu { background-color: transparent; }\nQMenu::item { background-color: transparent; }\nQMenu::item:selected { background-color: transparent; color: #ffffff; }\nQToolTip {\n                background-color: #3c3f42;\n                color: #e0e0e0;\n                border: 1px solid #666;\n                border-radius: 4px;\n                padding: 6px;\n                font-size: 13px;\n            }\n\n')

        self.centralwidget = _make_widget('centralwidget', MainWindow)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName('verticalLayout_2')
        self.centralwidget.setLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName('verticalLayout')
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_top = QtWidgets.QVBoxLayout()
        self.verticalLayout_top.setObjectName('verticalLayout_top')
        self.verticalLayout.addLayout(self.verticalLayout_top)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName('horizontalLayout_7')
        self.verticalLayout_top.addLayout(self.horizontalLayout_7)
        self.lb_display_txt = _make_widget('lb_display_txt', self.centralwidget)
        self.horizontalLayout_7.addWidget(self.lb_display_txt)
        self.main_expri_permission = _make_widget('main_expri_permission', self.centralwidget)
        self.horizontalLayout_7.addWidget(self.main_expri_permission)
        self.label_env_show = _make_widget('label_env_show', self.centralwidget)
        self.horizontalLayout_7.addWidget(self.label_env_show)
        self.btn_kefu_link = _make_widget('btn_kefu_link', self.centralwidget)
        self.horizontalLayout_7.addWidget(self.btn_kefu_link)
        self.cb_enable_proxy = _make_widget('cb_enable_proxy', self.centralwidget)
        self.horizontalLayout_7.addWidget(self.cb_enable_proxy)
        self.btn_proxy_setting = _make_widget('btn_proxy_setting', self.centralwidget)
        self.horizontalLayout_7.addWidget(self.btn_proxy_setting)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName('horizontalLayout_12')
        self.verticalLayout_top.addLayout(self.horizontalLayout_12)
        self.label_version_grade = _make_widget('label_version_grade', self.centralwidget)
        self.horizontalLayout_12.addWidget(self.label_version_grade)
        self.verticalLayout_mid = QtWidgets.QVBoxLayout()
        self.verticalLayout_mid.setObjectName('verticalLayout_mid')
        self.verticalLayout.addLayout(self.verticalLayout_mid)
        self.tabWidget_important = _make_widget('tabWidget_important', self.centralwidget)
        self.tabWidget_important.setMinimumSize(966, 0)
        self.tabWidget_important.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget_important.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget_important.setElideMode(QtCore.Qt.ElideMiddle)
        self.gen_session = _make_widget('gen_session', self.tabWidget_important)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.gen_session)
        self.verticalLayout_4.setObjectName('verticalLayout_4')
        self.gen_session.setLayout(self.verticalLayout_4)
        self.horizontalLayout_52 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_52.setObjectName('horizontalLayout_52')
        self.verticalLayout_4.addLayout(self.horizontalLayout_52)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName('verticalLayout_9')
        self.horizontalLayout_52.addLayout(self.verticalLayout_9)
        self.groupBox_5 = _make_widget('groupBox_5', self.gen_session)
        self.verticalLayout_69 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_69.setObjectName('verticalLayout_69')
        self.groupBox_5.setLayout(self.verticalLayout_69)
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName('verticalLayout_11')
        self.verticalLayout_69.addLayout(self.verticalLayout_11)
        self.label_30 = _make_widget('label_30', self.groupBox_5)
        self.verticalLayout_11.addWidget(self.label_30)
        self.label_38 = _make_widget('label_38', self.groupBox_5)
        self.verticalLayout_11.addWidget(self.label_38)
        self.label_18 = _make_widget('label_18', self.groupBox_5)
        self.verticalLayout_11.addWidget(self.label_18)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName('verticalLayout_8')
        self.verticalLayout_69.addLayout(self.verticalLayout_8)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName('horizontalLayout_5')
        self.verticalLayout_8.addLayout(self.horizontalLayout_5)
        self.lineEdit_input_phone = _make_widget('lineEdit_input_phone', self.groupBox_5)
        self.horizontalLayout_5.addWidget(self.lineEdit_input_phone)
        self.btn_send_yan_zhen_ma = _make_widget('btn_send_yan_zhen_ma', self.groupBox_5)
        self.horizontalLayout_5.addWidget(self.btn_send_yan_zhen_ma)
        self.horizontalLayout_59 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_59.setObjectName('horizontalLayout_59')
        self.verticalLayout_8.addLayout(self.horizontalLayout_59)
        self.lineEdit_yan_zhen_ma = _make_widget('lineEdit_yan_zhen_ma', self.groupBox_5)
        self.horizontalLayout_59.addWidget(self.lineEdit_yan_zhen_ma)
        self.lineEdit_two_pass_word = _make_widget('lineEdit_two_pass_word', self.groupBox_5)
        self.horizontalLayout_59.addWidget(self.lineEdit_two_pass_word)
        self.horizontalLayout_60 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_60.setObjectName('horizontalLayout_60')
        self.verticalLayout_8.addLayout(self.horizontalLayout_60)
        self.btn_login_gen_session = _make_widget('btn_login_gen_session', self.groupBox_5)
        self.horizontalLayout_60.addWidget(self.btn_login_gen_session)
        self.verticalLayout_9.addWidget(self.groupBox_5)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName('verticalLayout_7')
        self.horizontalLayout_52.addLayout(self.verticalLayout_7)
        self.label_5 = _make_widget('label_5', self.gen_session)
        self.verticalLayout_7.addWidget(self.label_5)
        self.listWidget_account_list = _make_widget('listWidget_account_list', self.gen_session)
        self.verticalLayout_7.addWidget(self.listWidget_account_list)
        self.btn_refresh_account = _make_widget('btn_refresh_account', self.gen_session)
        self.verticalLayout_7.addWidget(self.btn_refresh_account)
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setObjectName('verticalLayout_13')
        self.horizontalLayout_52.addLayout(self.verticalLayout_13)
        self.verticalLayout_16 = QtWidgets.QVBoxLayout()
        self.verticalLayout_16.setObjectName('verticalLayout_16')
        self.verticalLayout_13.addLayout(self.verticalLayout_16)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName('horizontalLayout_3')
        self.verticalLayout_13.addLayout(self.horizontalLayout_3)
        self.btn_net_test = _make_widget('btn_net_test', self.gen_session)
        self.horizontalLayout_3.addWidget(self.btn_net_test)
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setObjectName('verticalLayout_12')
        self.verticalLayout_13.addLayout(self.verticalLayout_12)
        self.tabWidget_important.addTab(self.gen_session, '')
        self.tab = _make_widget('tab', self.tabWidget_important)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.tab.setLayout(self.horizontalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName('verticalLayout_3')
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName('horizontalLayout_2')
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.zuobian_widget = _make_widget('zuobian_widget', self.tab)
        self._6 = QtWidgets.QVBoxLayout(self.zuobian_widget)
        self._6.setObjectName('_6')
        self.zuobian_widget.setLayout(self._6)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName('horizontalLayout_13')
        self._6.addLayout(self.horizontalLayout_13)
        self.label_6 = _make_widget('label_6', self.zuobian_widget)
        self.horizontalLayout_13.addWidget(self.label_6)
        self.zuobian_dibu = QtWidgets.QVBoxLayout()
        self.zuobian_dibu.setObjectName('zuobian_dibu')
        self._6.addLayout(self.zuobian_dibu)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName('horizontalLayout_6')
        self.zuobian_dibu.addLayout(self.horizontalLayout_6)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName('verticalLayout_6')
        self.horizontalLayout_6.addLayout(self.verticalLayout_6)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName('horizontalLayout_16')
        self.verticalLayout_6.addLayout(self.horizontalLayout_16)
        self.btn_auto_add_down_load = _make_widget('btn_auto_add_down_load', self.zuobian_widget)
        self.horizontalLayout_16.addWidget(self.btn_auto_add_down_load)
        self.btn_auto_add_item = _make_widget('btn_auto_add_item', self.zuobian_widget)
        self.horizontalLayout_16.addWidget(self.btn_auto_add_item)
        self.btn_auto_add_yulan = _make_widget('btn_auto_add_yulan', self.zuobian_widget)
        self.horizontalLayout_16.addWidget(self.btn_auto_add_yulan)
        self.btn_auto_add_flow = _make_widget('btn_auto_add_flow', self.zuobian_widget)
        self.horizontalLayout_16.addWidget(self.btn_auto_add_flow)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName('horizontalLayout_15')
        self.verticalLayout_6.addLayout(self.horizontalLayout_15)
        self.btn_auto_add_yun_preview = _make_widget('btn_auto_add_yun_preview', self.zuobian_widget)
        self.horizontalLayout_15.addWidget(self.btn_auto_add_yun_preview)
        self.btn_auto_add_yun_auto = _make_widget('btn_auto_add_yun_auto', self.zuobian_widget)
        self.horizontalLayout_15.addWidget(self.btn_auto_add_yun_auto)
        self.btn_auto_add_unkown1 = _make_widget('btn_auto_add_unkown1', self.zuobian_widget)
        self.horizontalLayout_15.addWidget(self.btn_auto_add_unkown1)
        self.btn_auto_add_unkown2 = _make_widget('btn_auto_add_unkown2', self.zuobian_widget)
        self.horizontalLayout_15.addWidget(self.btn_auto_add_unkown2)
        self.checkBox_auto_selected_all = _make_widget('checkBox_auto_selected_all', self.zuobian_widget)
        self.horizontalLayout_6.addWidget(self.checkBox_auto_selected_all)
        self.btn_copy_format_text = _make_widget('btn_copy_format_text', self.zuobian_widget)
        self.horizontalLayout_6.addWidget(self.btn_copy_format_text)
        self.main_btn_items_jiao_chen = _make_widget('main_btn_items_jiao_chen', self.zuobian_widget)
        self.horizontalLayout_6.addWidget(self.main_btn_items_jiao_chen)
        self.listWidget_auto_list = _make_widget('listWidget_auto_list', self.zuobian_widget)
        self._6.addWidget(self.listWidget_auto_list)
        self.horizontalLayout_2.addWidget(self.zuobian_widget)
        self.youbian_widget = _make_widget('youbian_widget', self.tab)
        self.youbian = QtWidgets.QVBoxLayout(self.youbian_widget)
        self.youbian.setObjectName('youbian')
        self.youbian_widget.setLayout(self.youbian)
        self.youbian_top_one = _make_widget('youbian_top_one', self.youbian_widget)
        self._4 = QtWidgets.QVBoxLayout(self.youbian_top_one)
        self._4.setObjectName('_4')
        self.youbian_top_one.setLayout(self._4)
        self.verticalGroupBox = _make_widget('verticalGroupBox', self.youbian_top_one)
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.verticalGroupBox)
        self.verticalLayout_15.setObjectName('verticalLayout_15')
        self.verticalGroupBox.setLayout(self.verticalLayout_15)
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName('horizontalLayout_18')
        self.verticalLayout_15.addLayout(self.horizontalLayout_18)
        self.checkBox_g_pic_water = _make_widget('checkBox_g_pic_water', self.verticalGroupBox)
        self.horizontalLayout_18.addWidget(self.checkBox_g_pic_water)
        self.checkBox_g_video_water = _make_widget('checkBox_g_video_water', self.verticalGroupBox)
        self.horizontalLayout_18.addWidget(self.checkBox_g_video_water)
        self.comboBox_g_video_minute = _make_widget('comboBox_g_video_minute', self.verticalGroupBox)
        self.horizontalLayout_18.addWidget(self.comboBox_g_video_minute)
        self.cb_g_water_mode = _make_widget('cb_g_water_mode', self.verticalGroupBox)
        self.horizontalLayout_18.addWidget(self.cb_g_water_mode)
        self.label_12 = _make_widget('label_12', self.verticalGroupBox)
        self.verticalLayout_15.addWidget(self.label_12)
        self.text_water_wrapper = _make_widget('text_water_wrapper', self.verticalGroupBox)
        self.text_water_wrapper_xx = QtWidgets.QVBoxLayout(self.text_water_wrapper)
        self.text_water_wrapper_xx.setObjectName('text_water_wrapper_xx')
        self.text_water_wrapper.setLayout(self.text_water_wrapper_xx)
        self.lineEdit_g_water_text = _make_widget('lineEdit_g_water_text', self.text_water_wrapper)
        self.text_water_wrapper_xx.addWidget(self.lineEdit_g_water_text)
        self.verticalLayout_15.addWidget(self.text_water_wrapper)
        self.pic_water_wrapper = _make_widget('pic_water_wrapper', self.verticalGroupBox)
        self.pic_water_wrapper_xx = QtWidgets.QHBoxLayout(self.pic_water_wrapper)
        self.pic_water_wrapper_xx.setObjectName('pic_water_wrapper_xx')
        self.pic_water_wrapper.setLayout(self.pic_water_wrapper_xx)
        self.btn_g_water_pic_jiao_chen = _make_widget('btn_g_water_pic_jiao_chen', self.pic_water_wrapper)
        self.pic_water_wrapper_xx.addWidget(self.btn_g_water_pic_jiao_chen)
        self.btn_g_water_select_pic = _make_widget('btn_g_water_select_pic', self.pic_water_wrapper)
        self.pic_water_wrapper_xx.addWidget(self.btn_g_water_select_pic)
        self.line_edit_g_water_pic_ratio = _make_widget('line_edit_g_water_pic_ratio', self.pic_water_wrapper)
        self.pic_water_wrapper_xx.addWidget(self.line_edit_g_water_pic_ratio)
        self.label_g_water_pic_path = _make_widget('label_g_water_pic_path', self.pic_water_wrapper)
        self.pic_water_wrapper_xx.addWidget(self.label_g_water_pic_path)
        self.verticalLayout_15.addWidget(self.pic_water_wrapper)
        self._4.addWidget(self.verticalGroupBox)
        self.guanggao = _make_widget('guanggao', self.youbian_top_one)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.guanggao)
        self.verticalLayout_5.setObjectName('verticalLayout_5')
        self.guanggao.setLayout(self.verticalLayout_5)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName('horizontalLayout_10')
        self.verticalLayout_5.addLayout(self.horizontalLayout_10)
        self.checkBox_enable_global_ad = _make_widget('checkBox_enable_global_ad', self.guanggao)
        self.horizontalLayout_10.addWidget(self.checkBox_enable_global_ad)
        self.checkBox_global_ad_is_bottom_up = _make_widget('checkBox_global_ad_is_bottom_up', self.guanggao)
        self.horizontalLayout_10.addWidget(self.checkBox_global_ad_is_bottom_up)
        self.checkBox_global_ad_delete = _make_widget('checkBox_global_ad_delete', self.guanggao)
        self.horizontalLayout_10.addWidget(self.checkBox_global_ad_delete)
        self.btn_add_g_ad = _make_widget('btn_add_g_ad', self.guanggao)
        self.horizontalLayout_10.addWidget(self.btn_add_g_ad)
        self.listWidget_g_ad_list = _make_widget('listWidget_g_ad_list', self.guanggao)
        self.verticalLayout_5.addWidget(self.listWidget_g_ad_list)
        self._4.addWidget(self.guanggao)
        self.zhanghao = _make_widget('zhanghao', self.youbian_top_one)
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.zhanghao)
        self.verticalLayout_14.setObjectName('verticalLayout_14')
        self.zhanghao.setLayout(self.verticalLayout_14)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName('horizontalLayout_4')
        self.verticalLayout_14.addLayout(self.horizontalLayout_4)
        self.btn_auto_select_session = _make_widget('btn_auto_select_session', self.zhanghao)
        self.horizontalLayout_4.addWidget(self.btn_auto_select_session)
        self.label_4 = _make_widget('label_4', self.zhanghao)
        self.horizontalLayout_4.addWidget(self.label_4)
        self.label_current_session = _make_widget('label_current_session', self.zhanghao)
        self.horizontalLayout_4.addWidget(self.label_current_session)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName('horizontalLayout_9')
        self.verticalLayout_14.addLayout(self.horizontalLayout_9)
        self.checkBox_check_post_permission = _make_widget('checkBox_check_post_permission', self.zhanghao)
        self.horizontalLayout_9.addWidget(self.checkBox_check_post_permission)
        self.label = _make_widget('label', self.zhanghao)
        self.horizontalLayout_9.addWidget(self.label)
        self.lineEdit_down_load_rate = _make_widget('lineEdit_down_load_rate', self.zhanghao)
        self.horizontalLayout_9.addWidget(self.lineEdit_down_load_rate)
        self.lineEdit_up_load_rate = _make_widget('lineEdit_up_load_rate', self.zhanghao)
        self.horizontalLayout_9.addWidget(self.lineEdit_up_load_rate)
        self.checkBox_auto_changed_rate = _make_widget('checkBox_auto_changed_rate', self.zhanghao)
        self.horizontalLayout_9.addWidget(self.checkBox_auto_changed_rate)
        self.btn_show_how = _make_widget('btn_show_how', self.zhanghao)
        self.horizontalLayout_9.addWidget(self.btn_show_how)
        self._4.addWidget(self.zhanghao)
        self.jichu_option = _make_widget('jichu_option', self.youbian_top_one)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.jichu_option)
        self.horizontalLayout_11.setObjectName('horizontalLayout_11')
        self.jichu_option.setLayout(self.horizontalLayout_11)
        self.checkBox_delete_temp_files = _make_widget('checkBox_delete_temp_files', self.jichu_option)
        self.horizontalLayout_11.addWidget(self.checkBox_delete_temp_files)
        self.btn_changed_folder = _make_widget('btn_changed_folder', self.jichu_option)
        self.horizontalLayout_11.addWidget(self.btn_changed_folder)
        self.label_folder_text = _make_widget('label_folder_text', self.jichu_option)
        self.horizontalLayout_11.addWidget(self.label_folder_text)
        self._4.addWidget(self.jichu_option)
        self.youbian.addWidget(self.youbian_top_one)
        self.comboBox_wrapper = _make_widget('comboBox_wrapper', self.youbian_widget)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.comboBox_wrapper)
        self.horizontalLayout_8.setObjectName('horizontalLayout_8')
        self.comboBox_wrapper.setLayout(self.horizontalLayout_8)
        self.comboBox_dingshi_monitor = _make_widget('comboBox_dingshi_monitor', self.comboBox_wrapper)
        self.horizontalLayout_8.addWidget(self.comboBox_dingshi_monitor)
        self.main_ban_yun_monitor_jiao_chen = _make_widget('main_ban_yun_monitor_jiao_chen', self.comboBox_wrapper)
        self.horizontalLayout_8.addWidget(self.main_ban_yun_monitor_jiao_chen)
        self.youbian.addWidget(self.comboBox_wrapper)
        self.youbian_top_two = _make_widget('youbian_top_two', self.youbian_widget)
        self._5 = QtWidgets.QVBoxLayout(self.youbian_top_two)
        self._5.setObjectName('_5')
        self.youbian_top_two.setLayout(self._5)
        self.dingshi_container = _make_widget('dingshi_container', self.youbian_top_two)
        self._3 = QtWidgets.QVBoxLayout(self.dingshi_container)
        self._3.setObjectName('_3')
        self.dingshi_container.setLayout(self._3)
        self.dingshi = _make_widget('dingshi', self.dingshi_container)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.dingshi)
        self.verticalLayout_10.setObjectName('verticalLayout_10')
        self.dingshi.setLayout(self.verticalLayout_10)
        self.time_one = QtWidgets.QHBoxLayout()
        self.time_one.setObjectName('time_one')
        self.verticalLayout_10.addLayout(self.time_one)
        self.checkBox0 = _make_widget('checkBox0', self.dingshi)
        self.time_one.addWidget(self.checkBox0)
        self.checkBox1 = _make_widget('checkBox1', self.dingshi)
        self.time_one.addWidget(self.checkBox1)
        self.checkBox2 = _make_widget('checkBox2', self.dingshi)
        self.time_one.addWidget(self.checkBox2)
        self.checkBox3 = _make_widget('checkBox3', self.dingshi)
        self.time_one.addWidget(self.checkBox3)
        self.checkBox4 = _make_widget('checkBox4', self.dingshi)
        self.time_one.addWidget(self.checkBox4)
        self.checkBox5 = _make_widget('checkBox5', self.dingshi)
        self.time_one.addWidget(self.checkBox5)
        self.checkBox6 = _make_widget('checkBox6', self.dingshi)
        self.time_one.addWidget(self.checkBox6)
        self.checkBox7 = _make_widget('checkBox7', self.dingshi)
        self.time_one.addWidget(self.checkBox7)
        self.time_two = QtWidgets.QHBoxLayout()
        self.time_two.setObjectName('time_two')
        self.verticalLayout_10.addLayout(self.time_two)
        self.checkBox8 = _make_widget('checkBox8', self.dingshi)
        self.time_two.addWidget(self.checkBox8)
        self.checkBox9 = _make_widget('checkBox9', self.dingshi)
        self.time_two.addWidget(self.checkBox9)
        self.checkBox10 = _make_widget('checkBox10', self.dingshi)
        self.time_two.addWidget(self.checkBox10)
        self.checkBox11 = _make_widget('checkBox11', self.dingshi)
        self.time_two.addWidget(self.checkBox11)
        self.checkBox12 = _make_widget('checkBox12', self.dingshi)
        self.time_two.addWidget(self.checkBox12)
        self.checkBox13 = _make_widget('checkBox13', self.dingshi)
        self.time_two.addWidget(self.checkBox13)
        self.checkBox14 = _make_widget('checkBox14', self.dingshi)
        self.time_two.addWidget(self.checkBox14)
        self.checkBox15 = _make_widget('checkBox15', self.dingshi)
        self.time_two.addWidget(self.checkBox15)
        self.time_three = QtWidgets.QHBoxLayout()
        self.time_three.setObjectName('time_three')
        self.verticalLayout_10.addLayout(self.time_three)
        self.checkBox16 = _make_widget('checkBox16', self.dingshi)
        self.time_three.addWidget(self.checkBox16)
        self.checkBox17 = _make_widget('checkBox17', self.dingshi)
        self.time_three.addWidget(self.checkBox17)
        self.checkBox18 = _make_widget('checkBox18', self.dingshi)
        self.time_three.addWidget(self.checkBox18)
        self.checkBox19 = _make_widget('checkBox19', self.dingshi)
        self.time_three.addWidget(self.checkBox19)
        self.checkBox20 = _make_widget('checkBox20', self.dingshi)
        self.time_three.addWidget(self.checkBox20)
        self.checkBox21 = _make_widget('checkBox21', self.dingshi)
        self.time_three.addWidget(self.checkBox21)
        self.checkBox22 = _make_widget('checkBox22', self.dingshi)
        self.time_three.addWidget(self.checkBox22)
        self.checkBox23 = _make_widget('checkBox23', self.dingshi)
        self.time_three.addWidget(self.checkBox23)
        self._3.addWidget(self.dingshi)
        self.ban_yun_cao_zuo_qu = _make_widget('ban_yun_cao_zuo_qu', self.dingshi_container)
        self.ban_yun_cao_zuo = QtWidgets.QHBoxLayout(self.ban_yun_cao_zuo_qu)
        self.ban_yun_cao_zuo.setObjectName('ban_yun_cao_zuo')
        self.ban_yun_cao_zuo_qu.setLayout(self.ban_yun_cao_zuo)
        self.btn_auto_yun_yin_start = _make_widget('btn_auto_yun_yin_start', self.ban_yun_cao_zuo_qu)
        self.ban_yun_cao_zuo.addWidget(self.btn_auto_yun_yin_start)
        self.btn_auto_yun_yin_run_one_and_start = _make_widget('btn_auto_yun_yin_run_one_and_start', self.ban_yun_cao_zuo_qu)
        self.ban_yun_cao_zuo.addWidget(self.btn_auto_yun_yin_run_one_and_start)
        self.btn_auto_yun_yin_run_one = _make_widget('btn_auto_yun_yin_run_one', self.ban_yun_cao_zuo_qu)
        self.ban_yun_cao_zuo.addWidget(self.btn_auto_yun_yin_run_one)
        self.btn_auto_yun_yin_stop = _make_widget('btn_auto_yun_yin_stop', self.ban_yun_cao_zuo_qu)
        self.ban_yun_cao_zuo.addWidget(self.btn_auto_yun_yin_stop)
        self._3.addWidget(self.ban_yun_cao_zuo_qu)
        self._5.addWidget(self.dingshi_container)
        self.monitor_container = _make_widget('monitor_container', self.youbian_top_two)
        self._2 = QtWidgets.QVBoxLayout(self.monitor_container)
        self._2.setObjectName('_2')
        self.monitor_container.setLayout(self._2)
        self.monitor_show = QtWidgets.QVBoxLayout()
        self.monitor_show.setObjectName('monitor_show')
        self._2.addLayout(self.monitor_show)
        self.label_monitor_tip = _make_widget('label_monitor_tip', self.monitor_container)
        self.monitor_show.addWidget(self.label_monitor_tip)
        self.scrollArea = _make_widget('scrollArea', self.monitor_container)
        self.scrollAreaWidgetContents = _make_widget('scrollAreaWidgetContents', self.scrollArea)
        self.scrollAreaLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollAreaLayout.setObjectName('scrollAreaLayout')
        self.scrollAreaWidgetContents.setLayout(self.scrollAreaLayout)
        self.label_monitor_text = _make_widget('label_monitor_text', self.scrollAreaWidgetContents)
        self.scrollAreaLayout.addWidget(self.label_monitor_text)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.monitor_show.addWidget(self.scrollArea)
        self.monitor_op = QtWidgets.QHBoxLayout()
        self.monitor_op.setObjectName('monitor_op')
        self._2.addLayout(self.monitor_op)
        self.btn_start_monitor = _make_widget('btn_start_monitor', self.monitor_container)
        self.monitor_op.addWidget(self.btn_start_monitor)
        self.btn_stop_monitor = _make_widget('btn_stop_monitor', self.monitor_container)
        self.monitor_op.addWidget(self.btn_stop_monitor)
        self.btn_open_close_big_show = _make_widget('btn_open_close_big_show', self.monitor_container)
        self.monitor_op.addWidget(self.btn_open_close_big_show)
        self._5.addWidget(self.monitor_container)
        self.youbian.addWidget(self.youbian_top_two)
        self.horizontalLayout_2.addWidget(self.youbian_widget)
        self.tabWidget_important.addTab(self.tab, '')
        self.tools = _make_widget('tools', self.tabWidget_important)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout(self.tools)
        self.horizontalLayout_17.setObjectName('horizontalLayout_17')
        self.tools.setLayout(self.horizontalLayout_17)
        self.verticalLayout_17 = QtWidgets.QVBoxLayout()
        self.verticalLayout_17.setObjectName('verticalLayout_17')
        self.horizontalLayout_17.addLayout(self.verticalLayout_17)
        self.horizontalLayout_181 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_181.setObjectName('horizontalLayout_181')
        self.verticalLayout_17.addLayout(self.horizontalLayout_181)
        self.verticalLayout_19 = QtWidgets.QVBoxLayout()
        self.verticalLayout_19.setObjectName('verticalLayout_19')
        self.horizontalLayout_181.addLayout(self.verticalLayout_19)
        self.verticalGroupBox_3 = _make_widget('verticalGroupBox_3', self.tools)
        self.verticalLayout_20 = QtWidgets.QVBoxLayout(self.verticalGroupBox_3)
        self.verticalLayout_20.setObjectName('verticalLayout_20')
        self.verticalGroupBox_3.setLayout(self.verticalLayout_20)
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setObjectName('horizontalLayout_21')
        self.verticalLayout_20.addLayout(self.horizontalLayout_21)
        self.tools_btn_gen_html = _make_widget('tools_btn_gen_html', self.verticalGroupBox_3)
        self.horizontalLayout_21.addWidget(self.tools_btn_gen_html)
        self.tools_box_ad_jiao_chen = _make_widget('tools_box_ad_jiao_chen', self.verticalGroupBox_3)
        self.horizontalLayout_21.addWidget(self.tools_box_ad_jiao_chen)
        self.label_2 = _make_widget('label_2', self.verticalGroupBox_3)
        self.verticalLayout_20.addWidget(self.label_2)
        self.lineEdit_tools_post_link = _make_widget('lineEdit_tools_post_link', self.verticalGroupBox_3)
        self.verticalLayout_20.addWidget(self.lineEdit_tools_post_link)
        self.verticalLayout_19.addWidget(self.verticalGroupBox_3)
        self.horizontalGroupBox = _make_widget('horizontalGroupBox', self.tools)
        self.verticalLayout_24 = QtWidgets.QVBoxLayout(self.horizontalGroupBox)
        self.verticalLayout_24.setObjectName('verticalLayout_24')
        self.horizontalGroupBox.setLayout(self.verticalLayout_24)
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_20.setObjectName('horizontalLayout_20')
        self.verticalLayout_24.addLayout(self.horizontalLayout_20)
        self.label_ad_config_tip = _make_widget('label_ad_config_tip', self.horizontalGroupBox)
        self.horizontalLayout_20.addWidget(self.label_ad_config_tip)
        self.tools_btn_edit_ad = _make_widget('tools_btn_edit_ad', self.horizontalGroupBox)
        self.horizontalLayout_20.addWidget(self.tools_btn_edit_ad)
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_22.setObjectName('horizontalLayout_22')
        self.verticalLayout_24.addLayout(self.horizontalLayout_22)
        self.tools_btn_post_ad = _make_widget('tools_btn_post_ad', self.horizontalGroupBox)
        self.horizontalLayout_22.addWidget(self.tools_btn_post_ad)
        self.lineEdit_ad_post_source = _make_widget('lineEdit_ad_post_source', self.horizontalGroupBox)
        self.verticalLayout_24.addWidget(self.lineEdit_ad_post_source)
        self.verticalLayout_19.addWidget(self.horizontalGroupBox)
        self.verticalLayout_25 = QtWidgets.QVBoxLayout()
        self.verticalLayout_25.setObjectName('verticalLayout_25')
        self.horizontalLayout_181.addLayout(self.verticalLayout_25)
        self.verticalGroupBox_2 = _make_widget('verticalGroupBox_2', self.tools)
        self.verticalLayout_18 = QtWidgets.QVBoxLayout(self.verticalGroupBox_2)
        self.verticalLayout_18.setObjectName('verticalLayout_18')
        self.verticalGroupBox_2.setLayout(self.verticalLayout_18)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName('horizontalLayout_14')
        self.verticalLayout_18.addLayout(self.horizontalLayout_14)
        self.cb_cover_expri = _make_widget('cb_cover_expri', self.verticalGroupBox_2)
        self.horizontalLayout_14.addWidget(self.cb_cover_expri)
        self.cb_cover_item_yun = _make_widget('cb_cover_item_yun', self.verticalGroupBox_2)
        self.horizontalLayout_14.addWidget(self.cb_cover_item_yun)
        self.btn_qian_yi_jiao_chen = _make_widget('btn_qian_yi_jiao_chen', self.verticalGroupBox_2)
        self.horizontalLayout_14.addWidget(self.btn_qian_yi_jiao_chen)
        self.label_3 = _make_widget('label_3', self.verticalGroupBox_2)
        self.verticalLayout_18.addWidget(self.label_3)
        self.label_7 = _make_widget('label_7', self.verticalGroupBox_2)
        self.verticalLayout_18.addWidget(self.label_7)
        self.lineEdit_old_u_code = _make_widget('lineEdit_old_u_code', self.verticalGroupBox_2)
        self.verticalLayout_18.addWidget(self.lineEdit_old_u_code)
        self.lineEdit_new_u_code = _make_widget('lineEdit_new_u_code', self.verticalGroupBox_2)
        self.verticalLayout_18.addWidget(self.lineEdit_new_u_code)
        self.tools_move_permission = _make_widget('tools_move_permission', self.verticalGroupBox_2)
        self.verticalLayout_18.addWidget(self.tools_move_permission)
        self.verticalLayout_25.addWidget(self.verticalGroupBox_2)
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setObjectName('horizontalLayout_19')
        self.verticalLayout_17.addLayout(self.horizontalLayout_19)
        self.verticalLayout_22 = QtWidgets.QVBoxLayout()
        self.verticalLayout_22.setObjectName('verticalLayout_22')
        self.horizontalLayout_19.addLayout(self.verticalLayout_22)
        self.verticalLayout_21 = QtWidgets.QVBoxLayout()
        self.verticalLayout_21.setObjectName('verticalLayout_21')
        self.horizontalLayout_19.addLayout(self.verticalLayout_21)
        self.tabWidget_important.addTab(self.tools, '')
        self.api_fun = _make_widget('api_fun', self.tabWidget_important)
        self.horizontalLayout_33 = QtWidgets.QHBoxLayout(self.api_fun)
        self.horizontalLayout_33.setObjectName('horizontalLayout_33')
        self.api_fun.setLayout(self.horizontalLayout_33)
        self.horizontalLayout_34 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_34.setObjectName('horizontalLayout_34')
        self.horizontalLayout_33.addLayout(self.horizontalLayout_34)
        self.verticalLayout_34 = QtWidgets.QVBoxLayout()
        self.verticalLayout_34.setObjectName('verticalLayout_34')
        self.horizontalLayout_34.addLayout(self.verticalLayout_34)
        self.horizontalLayout_30 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_30.setObjectName('horizontalLayout_30')
        self.verticalLayout_34.addLayout(self.horizontalLayout_30)
        self.label_22 = _make_widget('label_22', self.api_fun)
        self.horizontalLayout_30.addWidget(self.label_22)
        self.horizontalLayout_35 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_35.setObjectName('horizontalLayout_35')
        self.verticalLayout_34.addLayout(self.horizontalLayout_35)
        self.label_23 = _make_widget('label_23', self.api_fun)
        self.horizontalLayout_35.addWidget(self.label_23)
        self.lineEdit_api_app_id = _make_widget('lineEdit_api_app_id', self.api_fun)
        self.horizontalLayout_35.addWidget(self.lineEdit_api_app_id)
        self.horizontalLayout_36 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_36.setObjectName('horizontalLayout_36')
        self.verticalLayout_34.addLayout(self.horizontalLayout_36)
        self.label_24 = _make_widget('label_24', self.api_fun)
        self.horizontalLayout_36.addWidget(self.label_24)
        self.lineEdit_api_app_hash = _make_widget('lineEdit_api_app_hash', self.api_fun)
        self.horizontalLayout_36.addWidget(self.lineEdit_api_app_hash)
        self.horizontalLayout_37 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_37.setObjectName('horizontalLayout_37')
        self.verticalLayout_34.addLayout(self.horizontalLayout_37)
        self.btn_save_app_config = _make_widget('btn_save_app_config', self.api_fun)
        self.horizontalLayout_37.addWidget(self.btn_save_app_config)
        self.horizontalLayout_38 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_38.setObjectName('horizontalLayout_38')
        self.verticalLayout_34.addLayout(self.horizontalLayout_38)
        self.label_25 = _make_widget('label_25', self.api_fun)
        self.horizontalLayout_38.addWidget(self.label_25)
        self.btn_go_to_link = _make_widget('btn_go_to_link', self.api_fun)
        self.horizontalLayout_38.addWidget(self.btn_go_to_link)
        self.horizontalLayout_39 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_39.setObjectName('horizontalLayout_39')
        self.horizontalLayout_34.addLayout(self.horizontalLayout_39)
        self.line_2 = _make_widget('line_2', self.api_fun)
        self.horizontalLayout_34.addWidget(self.line_2)
        self.line_3 = _make_widget('line_3', self.api_fun)
        self.horizontalLayout_34.addWidget(self.line_3)
        self.tabWidget_important.addTab(self.api_fun, '')
        self.verticalLayout_mid.addWidget(self.tabWidget_important)
        self.verticalLayout_bottom = QtWidgets.QVBoxLayout()
        self.verticalLayout_bottom.setObjectName('verticalLayout_bottom')
        self.verticalLayout.addLayout(self.verticalLayout_bottom)
        self.verticalLayout_37 = QtWidgets.QVBoxLayout()
        self.verticalLayout_37.setObjectName('verticalLayout_37')
        self.verticalLayout_bottom.addLayout(self.verticalLayout_37)
        self.horizontalLayout_56 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_56.setObjectName('horizontalLayout_56')
        self.verticalLayout_37.addLayout(self.horizontalLayout_56)
        self.btn_clear_log = _make_widget('btn_clear_log', self.centralwidget)
        self.horizontalLayout_56.addWidget(self.btn_clear_log)
        self.btn_copy_log = _make_widget('btn_copy_log', self.centralwidget)
        self.horizontalLayout_56.addWidget(self.btn_copy_log)
        self.btn_open_log_folder = _make_widget('btn_open_log_folder', self.centralwidget)
        self.horizontalLayout_56.addWidget(self.btn_open_log_folder)
        self.btn_open_down_load_folder = _make_widget('btn_open_down_load_folder', self.centralwidget)
        self.horizontalLayout_56.addWidget(self.btn_open_down_load_folder)
        self.lineEdit_text_biao_shi = _make_widget('lineEdit_text_biao_shi', self.centralwidget)
        self.horizontalLayout_56.addWidget(self.lineEdit_text_biao_shi)
        self.btn_close_left = _make_widget('btn_close_left', self.centralwidget)
        self.horizontalLayout_56.addWidget(self.btn_close_left)
        self.btn_close_right = _make_widget('btn_close_right', self.centralwidget)
        self.horizontalLayout_56.addWidget(self.btn_close_right)
        self.btn_expand_log = _make_widget('btn_expand_log', self.centralwidget)
        self.horizontalLayout_56.addWidget(self.btn_expand_log)
        self.text_brow_log = _make_widget('text_brow_log', self.centralwidget)
        self.verticalLayout_37.addWidget(self.text_brow_log)
        self.menu_operation = _make_widget('menu_operation', self.centralwidget)
        self.verticalLayout_2.addWidget(self.menu_operation)

        self.menubar = _make_widget('menubar', MainWindow)
        self.menu = _make_widget('menu', self.menubar)
        self.menu_operation = self.menu
        self.action_reset = _make_widget('action_reset', MainWindow)
        self.action_dev = _make_widget('action_dev', MainWindow)
        self.action_copy_code = _make_widget('action_copy_code', MainWindow)
        self.menu.addAction(self.action_reset)
        self.menu.addAction(self.action_dev)
        self.menu.addSeparator()
        self.menu.addAction(self.action_copy_code)
        self.menubar.addAction(self.menu.menuAction())

        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setMenuBar(self.menubar)
        self.tabWidget_important.setCurrentIndex(1)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate('MainWindow', '运营猫'))
        self.lb_display_txt.setText(_translate('MainWindow', '加载中...'))
        self.main_expri_permission.setText(_translate('MainWindow', '激活体验'))
        self.label_env_show.setText(_translate('MainWindow', '开发环境'))
        self.btn_kefu_link.setText(_translate('MainWindow', '官方频道'))
        self.cb_enable_proxy.setText(_translate('MainWindow', '是否启用代理'))
        self.btn_proxy_setting.setText(_translate('MainWindow', '代理设置'))
        self.label_30.setText(_translate('MainWindow', '注意：只能添加已经存在的电报账号'))
        self.label_38.setText(_translate('MainWindow', '输入手机号，带上国际标识，比如大陆：+8613812345678'))
        self.label_18.setText(_translate('MainWindow', '两步验证码是可选的，没有就不输入'))
        self.lineEdit_input_phone.setPlaceholderText(_translate('MainWindow', '请输入手机号码'))
        self.btn_send_yan_zhen_ma.setText(_translate('MainWindow', '获取验证码'))
        self.lineEdit_yan_zhen_ma.setPlaceholderText(_translate('MainWindow', '验证码'))
        self.lineEdit_two_pass_word.setPlaceholderText(_translate('MainWindow', '两步验证码'))
        self.btn_login_gen_session.setText(_translate('MainWindow', '添加账号'))
        self.label_5.setText(_translate('MainWindow', '账号列表'))
        self.btn_refresh_account.setText(_translate('MainWindow', '刷新账号列表'))
        self.btn_net_test.setText(_translate('MainWindow', '网络连通性测试'))
        self.label_6.setText(_translate('MainWindow', '序号 选择状态 优先级     条目'))
        self.checkBox_auto_selected_all.setText(_translate('MainWindow', '全部选择'))
        self.btn_auto_add_down_load.setText(_translate('MainWindow', '+下载流'))
        self.btn_auto_add_item.setText(_translate('MainWindow', '+搬运流'))
        self.btn_auto_add_yulan.setText(_translate('MainWindow', '+预览流'))
        self.btn_auto_add_flow.setText(_translate('MainWindow', '+自动流'))
        self.btn_auto_add_yun_preview.setText(_translate('MainWindow', '+云预览'))
        self.btn_auto_add_yun_auto.setText(_translate('MainWindow', '+云自动'))
        self.btn_auto_add_unkown1.setText(_translate('MainWindow', '+未来1'))
        self.btn_auto_add_unkown2.setText(_translate('MainWindow', '+未来2'))
        self.btn_copy_format_text.setText(_translate('MainWindow', '快捷复制'))
        self.main_btn_items_jiao_chen.setText(_translate('MainWindow', '必看教程'))
        self.verticalGroupBox.setTitle(_translate('MainWindow', '全局水印设置（可选，优先使用条目的私有水印，如果私有水印未设置，就会使用这里配置的全局水印）'))
        self.label_12.setText(_translate('MainWindow', '图片水印或者视频动态水印'))
        self.checkBox_g_pic_water.setText(_translate('MainWindow', '图片水印'))
        self.checkBox_g_video_water.setText(_translate('MainWindow', '视频水印'))
        self.comboBox_g_video_minute.setItemText(0, _translate('MainWindow', '1分钟内视频'))
        self.comboBox_g_video_minute.setItemText(1, _translate('MainWindow', '3分钟内视频'))
        self.comboBox_g_video_minute.setItemText(2, _translate('MainWindow', '5分钟内视频'))
        self.comboBox_g_video_minute.setItemText(3, _translate('MainWindow', '10分钟内视频'))
        self.comboBox_g_video_minute.setItemText(4, _translate('MainWindow', '30分钟内视频'))
        self.comboBox_g_video_minute.setItemText(5, _translate('MainWindow', '60分钟内视频'))
        self.comboBox_g_video_minute.setItemText(6, _translate('MainWindow', '90分钟内视频'))
        self.comboBox_g_video_minute.setItemText(7, _translate('MainWindow', '120分钟内视频'))
        self.comboBox_g_video_minute.setItemText(8, _translate('MainWindow', '150分钟内视频'))
        self.cb_g_water_mode.setItemText(0, _translate('MainWindow', '图片水印'))
        self.cb_g_water_mode.setItemText(1, _translate('MainWindow', '文字水印'))
        self.lineEdit_g_water_text.setPlaceholderText(_translate('MainWindow', '水印文字，支持中文，英文'))
        self.btn_g_water_pic_jiao_chen.setText(_translate('MainWindow', '教程'))
        self.btn_g_water_select_pic.setText(_translate('MainWindow', '选择图片'))
        self.line_edit_g_water_pic_ratio.setPlaceholderText(_translate('MainWindow', '30'))
        self.label_g_water_pic_path.setText(_translate('MainWindow', '图片路径：'))
        self.guanggao.setTitle(_translate('MainWindow', '全局广告设置（可选，启用全局广告，会对所有条目都发布全局广告，并且不影响条目的私有广告）'))
        self.checkBox_enable_global_ad.setText(_translate('MainWindow', '启用全局广告'))
        self.checkBox_global_ad_is_bottom_up.setText(_translate('MainWindow', '置底广告'))
        self.checkBox_global_ad_delete.setText(_translate('MainWindow', '删除历史广告'))
        self.btn_add_g_ad.setText(_translate('MainWindow', '添加广告'))
        self.zhanghao.setTitle(_translate('MainWindow', '任务账号设置'))
        self.btn_auto_select_session.setText(_translate('MainWindow', '选择账号'))
        self.label_4.setText(_translate('MainWindow', '当前账号：'))
        self.label_current_session.setText(_translate('MainWindow', '无'))
        self.checkBox_check_post_permission.setText(_translate('MainWindow', '是否检测发消息权限'))
        self.label.setText(_translate('MainWindow', '速率配置：'))
        self.lineEdit_down_load_rate.setPlaceholderText(_translate('MainWindow', '下载每秒请求数'))
        self.lineEdit_up_load_rate.setPlaceholderText(_translate('MainWindow', '上传每秒请求数'))
        self.checkBox_auto_changed_rate.setText(_translate('MainWindow', '智能调速'))
        self.btn_show_how.setText(_translate('MainWindow', '点击查看如何修改'))
        self.checkBox_delete_temp_files.setText(_translate('MainWindow', '删除搬运后的本地资源'))
        self.btn_changed_folder.setText(_translate('MainWindow', '修改搬运目录'))
        self.label_folder_text.setText(_translate('MainWindow', '当前目录：'))
        self.comboBox_dingshi_monitor.setItemText(0, _translate('MainWindow', '定时模式'))
        self.comboBox_dingshi_monitor.setItemText(1, _translate('MainWindow', '监控模式'))
        self.main_ban_yun_monitor_jiao_chen.setText(_translate('MainWindow', '必看教程'))
        self.dingshi.setTitle(_translate('MainWindow', '定时设置'))
        self.checkBox0.setText(_translate('MainWindow', '0点'))
        self.checkBox1.setText(_translate('MainWindow', '1点'))
        self.checkBox2.setText(_translate('MainWindow', '2点'))
        self.checkBox3.setText(_translate('MainWindow', '3点'))
        self.checkBox4.setText(_translate('MainWindow', '4点'))
        self.checkBox5.setText(_translate('MainWindow', '5点'))
        self.checkBox6.setText(_translate('MainWindow', '6点'))
        self.checkBox7.setText(_translate('MainWindow', '7点'))
        self.checkBox8.setText(_translate('MainWindow', '8点'))
        self.checkBox9.setText(_translate('MainWindow', '9点'))
        self.checkBox10.setText(_translate('MainWindow', '10点'))
        self.checkBox11.setText(_translate('MainWindow', '11点'))
        self.checkBox12.setText(_translate('MainWindow', '12点'))
        self.checkBox13.setText(_translate('MainWindow', '13点'))
        self.checkBox14.setText(_translate('MainWindow', '14点'))
        self.checkBox15.setText(_translate('MainWindow', '15点'))
        self.checkBox16.setText(_translate('MainWindow', '16点'))
        self.checkBox17.setText(_translate('MainWindow', '17点'))
        self.checkBox18.setText(_translate('MainWindow', '18点'))
        self.checkBox19.setText(_translate('MainWindow', '19点'))
        self.checkBox20.setText(_translate('MainWindow', '20点'))
        self.checkBox21.setText(_translate('MainWindow', '21点'))
        self.checkBox22.setText(_translate('MainWindow', '22点'))
        self.checkBox23.setText(_translate('MainWindow', '23点'))
        self.btn_auto_yun_yin_start.setText(_translate('MainWindow', '启动定时任务'))
        self.btn_auto_yun_yin_run_one_and_start.setText(_translate('MainWindow', '执行一次并启动定时'))
        self.btn_auto_yun_yin_run_one.setText(_translate('MainWindow', '手动执行一次'))
        self.btn_auto_yun_yin_stop.setText(_translate('MainWindow', '停止任务'))
        self.label_monitor_tip.setText(_translate('MainWindow', '监控大屏'))
        self.btn_start_monitor.setText(_translate('MainWindow', '开启监控'))
        self.btn_stop_monitor.setText(_translate('MainWindow', '停止监控'))
        self.btn_open_close_big_show.setText(_translate('MainWindow', '展开监控大屏'))
        self.verticalGroupBox_3.setTitle(_translate('MainWindow', 'html格式生成工具（可用于生成带会员表情的文案）'))
        self.label_2.setText(_translate('MainWindow', '通过这个小工具，你可以生成支持电报会员表情的html格式的文本，然后可以把它配置到尾巴或者广告的文本中使用'))
        self.lineEdit_tools_post_link.setPlaceholderText(_translate('MainWindow', '这里输入帖子链接，即可生成帖子的html格式的文本'))
        self.tools_btn_gen_html.setText(_translate('MainWindow', '一键生成html文本格式'))
        self.tools_box_ad_jiao_chen.setText(_translate('MainWindow', '教程'))
        self.horizontalGroupBox.setTitle(_translate('MainWindow', '广告文案效果测试工具（可用于测试会员表情效果）'))
        self.lineEdit_ad_post_source.setPlaceholderText(_translate('MainWindow', '这里输入电报频道或者群组（私有的使用频道或者群组ID）'))
        self.label_ad_config_tip.setText(_translate('MainWindow', '当前未配置测试广告'))
        self.tools_btn_edit_ad.setText(_translate('MainWindow', '配置广告和媒体资源'))
        self.tools_btn_post_ad.setText(_translate('MainWindow', '发布广告查看效果'))
        self.verticalGroupBox_2.setTitle(_translate('MainWindow', '会员自助迁移工具'))
        self.label_3.setText(_translate('MainWindow', '请你妥善保管好你的唯一机器码，免得被人盗走会员权限'))
        self.label_7.setText(_translate('MainWindow', '获取完整机器码路径：软件左上角->菜单->复制机器码'))
        self.lineEdit_old_u_code.setPlaceholderText(_translate('MainWindow', '旧机器码'))
        self.lineEdit_new_u_code.setPlaceholderText(_translate('MainWindow', '新机器码'))
        self.cb_cover_expri.setText(_translate('MainWindow', '强制覆盖目标的体验会员'))
        self.cb_cover_item_yun.setText(_translate('MainWindow', '强制迁移数据'))
        self.btn_qian_yi_jiao_chen.setText(_translate('MainWindow', '教程'))
        self.tools_move_permission.setText(_translate('MainWindow', '迁移会员权限'))
        self.label_22.setText(_translate('MainWindow', '修改软件开发者信息，如果长期使用，推荐修改一下'))
        self.label_23.setText(_translate('MainWindow', 'API_ID:'))
        self.lineEdit_api_app_id.setPlaceholderText(_translate('MainWindow', '请输入你自己的app id'))
        self.label_24.setText(_translate('MainWindow', 'API_HASH:'))
        self.lineEdit_api_app_hash.setPlaceholderText(_translate('MainWindow', '请输入你自己的app hash'))
        self.btn_save_app_config.setText(_translate('MainWindow', '确认修改'))
        self.label_25.setText(_translate('MainWindow', '注：用自己TG号注册API，注册地址：https://my.telegram.org'))
        self.btn_go_to_link.setText(_translate('MainWindow', '点击去注册你的API'))
        self.btn_clear_log.setText(_translate('MainWindow', '清空日志'))
        self.btn_copy_log.setText(_translate('MainWindow', '复制日志'))
        self.btn_open_log_folder.setText(_translate('MainWindow', '打开日志目录'))
        self.btn_open_down_load_folder.setText(_translate('MainWindow', '打开下载目录'))
        self.lineEdit_text_biao_shi.setPlaceholderText(_translate('MainWindow', '功能标识，方便你快速备注当前多开软件功能'))
        self.btn_close_left.setText(_translate('MainWindow', '关闭左侧'))
        self.btn_close_right.setText(_translate('MainWindow', '关闭右侧'))
        self.btn_expand_log.setText(_translate('MainWindow', '打开全屏日志'))
        self.text_brow_log.setPlaceholderText(_translate('MainWindow', '日志仪表'))
        self.menu.setTitle(_translate('MainWindow', '菜单'))
        self.action_reset.setText(_translate('MainWindow', '重置运营猫'))
        self.action_dev.setText(_translate('MainWindow', '开发者中心'))
        self.action_copy_code.setText(_translate('MainWindow', '复制机器码'))
        self.label_version_grade.setText(_translate('MainWindow', '版本'))
        self.tabWidget_important.setTabText(self.tabWidget_important.indexOf(self.gen_session), _translate('MainWindow', '账号功能'))
        self.tabWidget_important.setTabText(self.tabWidget_important.indexOf(self.tab), _translate('MainWindow', '自动运营'))
        self.tabWidget_important.setTabText(self.tabWidget_important.indexOf(self.tools), _translate('MainWindow', '工具箱'))
        self.tabWidget_important.setTabText(self.tabWidget_important.indexOf(self.api_fun), _translate('MainWindow', 'API功能'))

