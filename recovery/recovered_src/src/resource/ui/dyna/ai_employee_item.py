# Recovered module: src.resource.ui.dyna.ai_employee_item
#
# The original Qt Designer .ui file is not shipped in the distribution.
# Widget names and types are recovered from the dialog widget map and the
# Nuitka constants chunk. The layout is a behaviour-level reconstruction.
from __future__ import annotations

from PyQt5 import QtCore, QtWidgets


FORM_TITLE = 'Form'

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
    'btn_em_import_sensitive': 'QPushButton',
    'btn_em_save': 'QPushButton',
    'btn_em_test': 'QPushButton',
    'btn_show_model_info': 'QPushButton',
    'btn_em_sexy_init': 'QPushButton',
    'btn_em_news_init': 'QPushButton',
    'textEdit_em_test_input': 'QTextEdit',
    'textEdit_em_role_display': 'QTextEdit',
    'textEdit_em_pre_text_display': 'QTextEdit',
    'textEdit_em_sensitive_word_display': 'QTextEdit',
    'textEdit_em_test_output': 'QTextEdit',
    'comboBox_em_select_model': 'QComboBox',
    'lineEdit_em_word_min': 'QLineEdit',
    'lineEdit_em_word_max': 'QLineEdit',
    'lineEdit_em_retry_count': 'QLineEdit',
    'lineEdit_em_name': 'QLineEdit',
    'label_em_role': 'QLabel',
    'label_em_pre_text': 'QLabel',
    'label_em_sensitive': 'QLabel',
    'label_em_model': 'QLabel',
    'label_em_name': 'QLabel',
    'label_2': 'QLabel',
    'label_3': 'QLabel',
    'label_5': 'QLabel',
    'label': 'QLabel',
    'label_4': 'QLabel',
}


_SIZE_CONSTRAINTS = {
}


SETUP_ORDER = (
    'btn_em_sexy_init',
    'btn_em_news_init',
    'textEdit_em_role_display',
    'textEdit_em_pre_text_display',
    'btn_em_import_sensitive',
    'textEdit_em_sensitive_word_display',
    'lineEdit_em_word_min',
    'lineEdit_em_word_max',
    'lineEdit_em_retry_count',
    'comboBox_em_select_model',
    'btn_show_model_info',
    'textEdit_em_test_input',
    'btn_em_test',
    'textEdit_em_test_output',
    'lineEdit_em_name',
    'btn_em_save',
    'label_em_role',
    'label_em_pre_text',
    'label_em_sensitive',
    'label_em_model',
    'label_em_name',
    'label_2',
    'label_3',
    'label_5',
    'label',
    'label_4',
)


class Ui_Form:
    def setupUi(self, Form):
        Form.setObjectName('Form')
        Form.resize(851, 728)
        Form.setStyleSheet('*{\nbackground-color:#3c3f42;\ncolor: #e6e6e6;\n}\n\n*:disabled {\n    background-color: #3c3f42;\n    color: #afafaf;\n    cursor: not-allowed;\n\n}\nQListWidget:disabled,QTextEdit:disabled,QLineEdit:disabled,QTabWidget:disabled{\nbackground-color:rgb(40, 40, 40);\n}\nQTextBrowser:disabled{\nbackground-color:rgb(40, 40, 40);\ncolor: rgb(152, 197, 150);\n}\n\nQPushButton:disabled {\n    background-color: rgb(80, 80, 80);\n    color: #afafaf;\n    cursor: not-allowed;\n\n}\n\nQCheckBox:hover,QRadioButton:hover {\ncolor: white;\n}\n\nQPushButton:hover {\n\nfont-weight: bold;\nbackground-color:rgb(84, 84, 84);\ncolor: white;\nborder-radius: 2pt;\n\n}\n\nQPushButton{\nfont-weight: bold;\nbackground-color:rgb(106, 106, 106);\ncolor: #e6e6e6;\nborder-radius: 2pt;\n}\n\nQTextBrowser,QListWidget,QTextEdit,QTabWidget{\nbackground-color:rgb(40, 40, 40);\ncolor: rgba(152, 197, 150, 185);\nfont-size:10pt;\n}\n\nQTextBrowser:hover,QTextEdit:hover{\nbackground-color:rgb(40, 40, 40);\ncolor: rgb(152, 197, 150);\nfont-size:10pt;\n}\n\nQLineEdit{\nbackground-color:rgb(40, 40, 40);\ncolor: rgba(152, 197, 150, 185);\nfont-size:12pt;\n}\n\nQLineEdit:hover{\nbackground-color:rgb(40, 40, 40);\ncolor: rgb(152, 197, 150);\nfont-size:12pt;\n}\n\n\nQLabel{\ncolor: #ebf905;\n}\n\n\n\nQRadioButton,QCheckBox {\n        border: none;\n        border-radius: 9px;\n}\nQRadioButton::indicator,QCheckBox::indicator{\n    background-color: rgb(42, 45, 66);\n    border: 0px solid #b1b1b1;\n    width: 18px;\n    height: 18px;\n    border-radius: 9px;\n}\n\nQRadioButton::indicator:checked,QCheckBox::indicator:checked {\n    background-color: #ebf905;\n    border-color: #ebf905;\n}\n\nQMenuBar { background-color: transparent; }\nQMenuBar::item { background-color: transparent; }\nQMenuBar::item:selected { background-color:transparent; color: #ffffff;}\nQMenu { background-color: transparent; }\nQMenu::item { background-color: transparent; }\nQMenu::item:selected { background-color: transparent; color: #ffffff; }\n\n')

        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName('horizontalLayout')
        Form.setLayout(self.horizontalLayout)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName('verticalLayout')
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName('horizontalLayout_8')
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.label_2 = _make_widget('label_2', Form)
        self.horizontalLayout_8.addWidget(self.label_2)
        self.btn_em_sexy_init = _make_widget('btn_em_sexy_init', Form)
        self.horizontalLayout_8.addWidget(self.btn_em_sexy_init)
        self.btn_em_news_init = _make_widget('btn_em_news_init', Form)
        self.horizontalLayout_8.addWidget(self.btn_em_news_init)
        self.textEdit_em_role_display = _make_widget('textEdit_em_role_display', Form)
        self.verticalLayout.addWidget(self.textEdit_em_role_display)
        self.label_3 = _make_widget('label_3', Form)
        self.verticalLayout.addWidget(self.label_3)
        self.textEdit_em_pre_text_display = _make_widget('textEdit_em_pre_text_display', Form)
        self.verticalLayout.addWidget(self.textEdit_em_pre_text_display)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName('horizontalLayout_6')
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.label_5 = _make_widget('label_5', Form)
        self.horizontalLayout_6.addWidget(self.label_5)
        self.btn_em_import_sensitive = _make_widget('btn_em_import_sensitive', Form)
        self.horizontalLayout_6.addWidget(self.btn_em_import_sensitive)
        self.textEdit_em_sensitive_word_display = _make_widget('textEdit_em_sensitive_word_display', Form)
        self.verticalLayout.addWidget(self.textEdit_em_sensitive_word_display)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName('horizontalLayout_2')
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label = _make_widget('label', Form)
        self.horizontalLayout_2.addWidget(self.label)
        self.lineEdit_em_word_min = _make_widget('lineEdit_em_word_min', Form)
        self.horizontalLayout_2.addWidget(self.lineEdit_em_word_min)
        self.lineEdit_em_word_max = _make_widget('lineEdit_em_word_max', Form)
        self.horizontalLayout_2.addWidget(self.lineEdit_em_word_max)
        self.lineEdit_em_retry_count = _make_widget('lineEdit_em_retry_count', Form)
        self.horizontalLayout_2.addWidget(self.lineEdit_em_retry_count)
        self.label_4 = _make_widget('label_4', Form)
        self.horizontalLayout_2.addWidget(self.label_4)
        self.comboBox_em_select_model = _make_widget('comboBox_em_select_model', Form)
        self.horizontalLayout_2.addWidget(self.comboBox_em_select_model)
        self.btn_show_model_info = _make_widget('btn_show_model_info', Form)
        self.horizontalLayout_2.addWidget(self.btn_show_model_info)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName('horizontalLayout_5')
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName('verticalLayout_3')
        self.horizontalLayout_5.addLayout(self.verticalLayout_3)
        self.textEdit_em_test_input = _make_widget('textEdit_em_test_input', Form)
        self.verticalLayout_3.addWidget(self.textEdit_em_test_input)
        self.btn_em_test = _make_widget('btn_em_test', Form)
        self.verticalLayout_3.addWidget(self.btn_em_test)
        self.textEdit_em_test_output = _make_widget('textEdit_em_test_output', Form)
        self.verticalLayout_3.addWidget(self.textEdit_em_test_output)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName('verticalLayout_2')
        self.horizontalLayout_5.addLayout(self.verticalLayout_2)
        self.lineEdit_em_name = _make_widget('lineEdit_em_name', Form)
        self.verticalLayout_2.addWidget(self.lineEdit_em_name)
        self.btn_em_save = _make_widget('btn_em_save', Form)
        self.verticalLayout_2.addWidget(self.btn_em_save)
        self.label_em_role = QtWidgets.QLabel(Form)
        self.label_em_role.setObjectName('label_em_role')
        self.label_em_role.setVisible(False)
        self.label_em_pre_text = QtWidgets.QLabel(Form)
        self.label_em_pre_text.setObjectName('label_em_pre_text')
        self.label_em_pre_text.setVisible(False)
        self.label_em_sensitive = QtWidgets.QLabel(Form)
        self.label_em_sensitive.setObjectName('label_em_sensitive')
        self.label_em_sensitive.setVisible(False)
        self.label_em_model = QtWidgets.QLabel(Form)
        self.label_em_model.setObjectName('label_em_model')
        self.label_em_model.setVisible(False)
        self.label_em_name = QtWidgets.QLabel(Form)
        self.label_em_name.setObjectName('label_em_name')
        self.label_em_name.setVisible(False)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate('Form', FORM_TITLE))
        self.label_2.setText(_translate('Form', 'AI员工角色描述设定'))
        self.btn_em_sexy_init.setText(_translate('Form', '初始化为色情AI员工'))
        self.btn_em_news_init.setText(_translate('Form', '初始化为中文新闻记者'))
        self.textEdit_em_role_display.setPlaceholderText(_translate('Form', 'AI员工角色描述设定'))
        self.label_3.setText(_translate('Form', '前置文案，就是描述AI员工如何生成文案，这里设置一些简单约束规则'))
        self.textEdit_em_pre_text_display.setPlaceholderText(_translate('Form', '前置文案，就是描述AI员工如何生成文案，这里设置一些简单约束规则'))
        self.label_5.setText(_translate('Form', 'AI敏感词，必须要设置，使用竖线分割，比可以在默认基础上添加敏感词（敏感词用于防止AI系统风控）'))
        self.btn_em_import_sensitive.setText(_translate('Form', '导入默认敏感词'))
        self.textEdit_em_sensitive_word_display.setPlaceholderText(_translate('Form', 'AI敏感词，必须要设置，使用竖线分割，比可以在默认基础上添加敏感词（敏感词用于防止AI系统风控）'))
        self.label.setText(_translate('Form', '目标文本长度(最小值和最大值之间的随机长度)'))
        self.lineEdit_em_word_min.setPlaceholderText(_translate('Form', '最小值'))
        self.lineEdit_em_word_max.setPlaceholderText(_translate('Form', '最大值'))
        self.lineEdit_em_retry_count.setPlaceholderText(_translate('Form', '重试次数'))
        self.label_4.setText(_translate('Form', '模型选择'))
        self.btn_show_model_info.setText(_translate('Form', '查看模型计费'))
        self.textEdit_em_test_input.setPlaceholderText(_translate('Form', '在这里输入色情文案，可以去色情频道里面复制色情文本，然后粘贴到这里。'))
        self.btn_em_test.setText(_translate('Form', '点击测试文本同义转换效果⬇️'))
        self.lineEdit_em_name.setPlaceholderText(_translate('Form', '给这个AI员工取一个名字'))
        self.btn_em_save.setText(_translate('Form', '保存'))

