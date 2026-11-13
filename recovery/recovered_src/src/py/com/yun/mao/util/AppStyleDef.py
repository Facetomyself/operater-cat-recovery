# Recovered module: src.py.com.yun.mao.util.AppStyleDef
# Exact stylesheet constant from the module constants chunk.
from __future__ import annotations


APP_ALL_STYLE_DEF = """
*{
background-color:#3c3f42;
color: #e6e6e6;
}

*:disabled {
\tbackground-color: #3c3f42;
\tcolor: #afafaf;
\tcursor: not-allowed;

}
QListWidget:disabled,QTextEdit:disabled,QLineEdit:disabled,QTabWidget:disabled{
background-color:rgb(40, 40, 40);
}
QTextBrowser:disabled{
background-color:rgb(40, 40, 40);
color: rgb(152, 197, 150);
}

QPushButton:disabled {
\tbackground-color: rgb(80, 80, 80);
\tcolor: #afafaf;
\tcursor: not-allowed;

}

QCheckBox:hover,QRadioButton:hover {
color: white;
}

QPushButton:hover {

font-weight: bold;
background-color:rgb(84, 84, 84);
color: white;
border-radius: 2pt;

}

QPushButton{
font-weight: bold;
background-color:rgb(106, 106, 106);
color: #e6e6e6;
border-radius: 2pt;
}

QTextBrowser,QListWidget,QTextEdit,QLineEdit,QTabWidget{
background-color:rgb(40, 40, 40);
color: rgba(152, 197, 150, 185);
font-size:12pt;
}

QTextBrowser:hover,QTextEdit:hover,QLineEdit:hover{
background-color:rgb(40, 40, 40);
color: rgb(152, 197, 150);
font-size:12pt;
}


QLabel{
color: #ebf905;
}



QRadioButton,QCheckBox {
        border: none;
        border-radius: 9px;
}
QRadioButton::indicator,QCheckBox::indicator{
    background-color: rgb(42, 45, 66);
    border: 0px solid #b1b1b1;
\twidth: 18px;
\theight: 18px;
\tborder-radius: 9px;
}

QRadioButton::indicator:checked,QCheckBox::indicator:checked {
    background-color: #ebf905;
    border-color: #ebf905;
}

QMenuBar { background-color: transparent; }
QMenuBar::item { background-color: transparent; }
QMenuBar::item:selected { background-color:transparent; color: #ffffff;}
QMenu { background-color: transparent; }
QMenu::item { background-color: transparent; }
QMenu::item:selected { background-color: transparent; color: #ffffff; }


"""
