import sys
import io
import initialize
import oper
from PyQt6.QtWidgets import QPushButton, QMessageBox, QApplication, QVBoxLayout, QTableWidget, QTableWidgetItem, QWidget, QHBoxLayout, QLineEdit, QDialog, QLabel, QFileDialog
from PyQt6.QtCore import QByteArray
from PyQt6.QtGui import QIcon, QPixmap, QImage

class Check_StudentWindow(QDialog):
    def __init__(self, db, cursor):
        super().__init__()
        self.db = db
        self.cursor = cursor
        self.ID, self.name, self.age, self.major, self.photo = '', '', 1, '', ''
        self.setWindowTitle('输入需要查询的学生学号')
        self.resize(320, 200)
        self.init_ui()

    def init_ui(self):

        # 创建 QLineEdit 对象
        self.input_box1 = QLineEdit(self)
        self.input_box1.setPlaceholderText("在此输入学号...")

        # 创建确认按钮
        self.closeButton = QPushButton('确认', self)
        self.closeButton.clicked.connect(self.get_text)

        # 设置布局
        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout1.addWidget(self.input_box1)
        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.closeButton)
        layout.addLayout(layout1)
        layout.addLayout(bottomLayout)
        self.setLayout(layout)

    def get_text(self):
        self.acceptflag = False
        if (len(self.input_box1.text()) != 0):
            self.ID = self.input_box1.text()
            info = oper.select_student_baseinfo(self.db, self.cursor, self.ID)
            if info == None:
                widget = QWidget()
                QMessageBox.information(widget, '信息', '学生不存在') #触发的事件时弹出会话框
            else:
                self.acceptflag = True
                self.name = info[1]
                self.age = info[2]
                self.major = info[3]
                self.photo = info[4]

        if self.acceptflag:
            self.accept()

    def get_entered_ID(self):
        return self.ID
    
    def get_entered_Name(self):
        return self.name
    
    def get_entered_Age(self):
        return self.age
    
    def get_entered_Major(self):
        return self.major
        
    def get_entered_Photo(self):
        return self.photo

class ResultWindow(QWidget):
    def __init__(self, db, cursor, id, name, age, major, photo):
        super().__init__()
        self.db = db
        self.cursor = cursor
        self.id = id
        self.name = name
        self.age = age
        self.major = major
        self.photo = photo
        self.setWindowTitle('学生详细信息')
        self.resize(600, 750)
        self.init_ui()
    
    def init_ui(self):
        scoreinfo = oper.select_student_score(self.db, self.cursor, self.id)
        punishinfo = oper.select_student_prizes(self.db, self.cursor, self.id)
        prizeinfo = oper.select_student_punish(self.db, self.cursor, self.id)
        if (len(scoreinfo)!=0):
            total_points_info = oper.get_total_points(self.db, self.cursor, self.id)
            total_points = total_points_info[0]
        else:
            total_points = 0

        # 创建 QLabel 对象
        self.label1 = QLabel(f"学号：{self.id}")
        self.label2 = QLabel(f"姓名：{self.name}")
        self.label3 = QLabel(f"年龄：{self.age}")
        self.label4 = QLabel(f"专业：{self.major}")
        self.label5 = QLabel(f"当前已获总学分：{total_points}")   
        try:
            image = QImage.fromData(QByteArray(self.photo))
            pixmap = QPixmap(image)
            self.label6 = QLabel(self)
            self.label6.setPixmap(pixmap)
        except Exception as e:
            print(f"ERROR:{e}")
            return

        # 创建表格
        self.table1 = QTableWidget(len(scoreinfo), 2)
        self.table1.setHorizontalHeaderLabels(['课程号','成绩'])
        # 填充表格数据
        for i in range(len(scoreinfo)):
            for j in range(2):
                    item = QTableWidgetItem(str(scoreinfo[i][j+1]))
                    self.table1.setItem(i, j, item)
        # 创建表格
        self.table2 = QTableWidget(len(prizeinfo), 2)
        self.table2.setHorizontalHeaderLabels(['奖项','等级'])
        # 填充表格数据
        for i in range(len(prizeinfo)):
            for j in range(2):
                    item = QTableWidgetItem(str(prizeinfo[i][j]))
                    self.table2.setItem(i, j, item)

        # 创建表格
        self.table3 = QTableWidget(len(punishinfo), 1)
        self.table3.setHorizontalHeaderLabels(['惩罚'])
        # 填充表格数据
        for i in range(len(punishinfo)):
            for j in range(1):
                    item = QTableWidgetItem(str(punishinfo[i][j]))
                    self.table3.setItem(i, j, item)

        # 创建关闭按钮
        self.closeButton = QPushButton('Close', self)
        self.closeButton.clicked.connect(self.close)

        # 设置布局
        layout = QVBoxLayout()
        layout_base = QHBoxLayout()
        layout_base1 = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout1.addWidget(self.label1)
        layout1.addWidget(self.label2)
        layout2 = QHBoxLayout()
        layout2.addWidget(self.label3)
        layout2.addWidget(self.label4)
        layout3 = QHBoxLayout()
        layout3.addWidget(self.label5)
        layout_base1.addLayout(layout1)
        layout_base1.addLayout(layout2)
        layout_base1.addLayout(layout3)
        layout_base.addLayout(layout_base1)
        layout_base.addWidget(self.label6)
        layout.addLayout(layout_base)
        layout.addWidget(self.table1)
        layout.addWidget(self.table2)
        layout.addWidget(self.table3)
        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.closeButton)
        layout.addLayout(bottomLayout)
        self.setLayout(layout)

class delete_scoreWindow(QDialog):
    def __init__(self, db, cursor):
        super().__init__()
        self.db = db
        self.cursor = cursor
        self.sID = ''
        self.cID = ''
        self.setWindowTitle('输入要删除的学生学号和课程号')
        self.resize(320, 200)
        self.init_ui()
    
    def init_ui(self):
        # 创建 QLabel 对象
        self.label1 = QLabel("学生学号：")
        self.label2 = QLabel("课程号：")

        # 创建 QLineEdit 对象
        self.input_box1 = QLineEdit(self)
        self.input_box1.setPlaceholderText("在此输入学号...")
        self.input_box2 = QLineEdit(self)
        self.input_box2.setPlaceholderText("在此输入课程号...")

        # 创建确认按钮
        self.closeButton = QPushButton('确认', self)
        self.closeButton.clicked.connect(self.get_text)

        # 设置布局
        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout1.addWidget(self.label1)
        layout1.addWidget(self.input_box1)
        layout2 = QHBoxLayout()
        layout2.addWidget(self.label2)
        layout2.addWidget(self.input_box2)
        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.closeButton)
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(bottomLayout)
        self.setLayout(layout)

    def get_text(self):
        acceptflag = 0
        if (len(self.input_box1.text()) != 0):
            acceptflag += 1
            self.sID = self.input_box1.text()
            
        if (len(self.input_box2.text()) != 0):
            acceptflag += 1
            self.cID = self.input_box2.text()

        if acceptflag == 2:
            self.accept()
        else:
            widget = QWidget()
            QMessageBox.information(widget, '信息', '缺少信息') #触发的事件时弹出会话框    

    def get_entered_sID(self):
        return self.sID
    
    def get_entered_cID(self):
        return self.cID
    
class add_timescoreWindow(QDialog):
    def __init__(self, db, cursor, kind):
        super().__init__()
        self.db = db
        self.cursor = cursor
        self.kind = kind
        self.ID = ''
        self.name = ''
        self.timescore = ''
        if self.kind == 0:
            self.setWindowTitle('输入获奖学生的学号和奖项信息')
        if kind == 1:
            self.setWindowTitle('输入受惩学生的学号和惩罚信息')
        if kind == 2:
            self.setWindowTitle('输入学生的学号和课程号')
        self.resize(320, 200)
        self.init_ui()
    
    def init_ui(self):
        # 创建 QLabel 对象
        self.label1 = QLabel("学生学号：")
        if self.kind == 0:
            self.label2 = QLabel("奖项名称：")
        if self.kind == 1:
            self.label2 = QLabel("惩罚名称：")
        if self.kind == 2:
            self.label2 = QLabel("课程号：")
        if self.kind == 2:
            self.label3 = QLabel("成绩：") 
        else:
            self.label3 = QLabel("时间：") 

        # 创建 QLineEdit 对象
        self.input_box1 = QLineEdit(self)
        self.input_box1.setPlaceholderText("在此输入学号...")
        self.input_box2 = QLineEdit(self)
        if self.kind == 2:
            self.input_box2.setPlaceholderText("在此输入课程号...")
        else:
            self.input_box2.setPlaceholderText("在此输入名称...")
        self.input_box3 = QLineEdit(self)
        if self.kind == 2:
            self.input_box3.setPlaceholderText("在此输入成绩...")
        else:
            self.input_box3.setPlaceholderText("在此输入时间...")

        # 创建确认按钮
        self.closeButton = QPushButton('确认', self)
        self.closeButton.clicked.connect(self.get_text)

        # 设置布局
        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout1.addWidget(self.label1)
        layout1.addWidget(self.input_box1)
        layout2 = QHBoxLayout()
        layout2.addWidget(self.label2)
        layout2.addWidget(self.input_box2)
        layout3 = QHBoxLayout()
        layout3.addWidget(self.label3)
        layout3.addWidget(self.input_box3)
        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.closeButton)
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        layout.addLayout(bottomLayout)
        self.setLayout(layout)

    def get_text(self):
        acceptflag = 0
        if (len(self.input_box1.text()) != 0):
            acceptflag += 1
            self.ID = self.input_box1.text()
            info = oper.select_student_baseinfo(self.db, self.cursor, self.ID)
            if (info == None):
                widget = QWidget()
                QMessageBox.information(widget, '信息', '学生不存在') #触发的事件时弹出会话框
                return
            
        if (len(self.input_box2.text()) != 0):
            acceptflag += 1
            self.name = self.input_box2.text()

        if acceptflag == 2:
            if self.kind == 0:
                info = oper.select_prize_name(self.db, self.cursor, self.name)
                if (info == None):
                    widget = QWidget()
                    QMessageBox.information(widget, '信息', '奖项不存在') #触发的事件时弹出会话框
                    return
                info = oper.select_student_prize_one(self.db, self.cursor, self.ID, self.name)
            if self.kind == 1:
                info = oper.select_punish_name(self.db, self.cursor, self.name)
                if (info == None):
                    widget = QWidget()
                    QMessageBox.information(widget, '信息', '惩罚不存在') #触发的事件时弹出会话框
                    return
                info = oper.select_student_punish_one(self.db, self.cursor, self.ID, self.name)
            if self.kind == 2:
                info = oper.select_class_ID(self.db, self.cursor, self.name)
                if (info == None):
                    widget = QWidget()
                    QMessageBox.information(widget, '信息', '课程不存在') #触发的事件时弹出会话框
                    return
                info = oper.select_student_class_score(self.db, self.cursor, self.ID, self.name)
            if (info != None):
                widget = QWidget()
                QMessageBox.information(widget, '信息', '已存在') #触发的事件时弹出会话框
                return

        if (len(self.input_box3.text()) != 0):
            acceptflag += 1
            self.timescore = self.input_box3.text()

        if acceptflag == 3:
            self.accept()
        else:
            widget = QWidget()
            QMessageBox.information(widget, '信息', '缺少信息') #触发的事件时弹出会话框    

    def get_entered_ID(self):
        return self.ID
    
    def get_entered_Name(self):
        return self.name
    
    def get_entered_timescore(self):
        return self.timescore

class New_PrizeWindow(QDialog):
    def __init__(self, db, cursor):
        super().__init__()
        self.db = db
        self.cursor = cursor
        self.grade = ''
        self.name = ''
        self.setWindowTitle('输入新奖项信息')
        self.resize(320, 200)
        self.init_ui()
    
    def init_ui(self):
        # 创建 QLabel 对象
        self.label1 = QLabel("奖项：")
        self.label2 = QLabel("等级：")

        # 创建 QLineEdit 对象
        self.input_box1 = QLineEdit(self)
        self.input_box1.setPlaceholderText("在此输入新的奖项...")
        self.input_box2 = QLineEdit(self)
        self.input_box2.setPlaceholderText("在此输入新的等级...")

        # 创建确认按钮
        self.closeButton = QPushButton('确认', self)
        self.closeButton.clicked.connect(self.get_text)

        # 设置布局
        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout1.addWidget(self.label1)
        layout1.addWidget(self.input_box1)
        layout2 = QHBoxLayout()
        layout2.addWidget(self.label2)
        layout2.addWidget(self.input_box2)
        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.closeButton)
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(bottomLayout)
        self.setLayout(layout)

    def get_text(self):
        acceptflag = 0
        if (len(self.input_box1.text()) != 0):
            acceptflag += 1
            self.name = self.input_box1.text()
            info = oper.select_prize_name(self.db, self.cursor, self.name)
            if (info != None):
                widget = QWidget()
                QMessageBox.information(widget, '信息', '该奖项已存在') #触发的事件时弹出会话框
                return
            
        if (len(self.input_box2.text()) != 0):
            acceptflag += 1
            self.grade = self.input_box2.text()

        if acceptflag == 2:
            self.accept()
        else:
            widget = QWidget()
            QMessageBox.information(widget, '信息', '缺少信息') #触发的事件时弹出会话框

    def get_entered_Name(self):
        return self.name
    
    def get_entered_Grade(self):
        return self.grade
    
class New_PunishWindow(QDialog):
    def __init__(self, db, cursor):
        super().__init__()
        self.db = db
        self.cursor = cursor
        self.name = ''
        self.setWindowTitle('输入新课惩罚信息')
        self.resize(320, 200)
        self.init_ui()
    
    def init_ui(self):
        # 创建 QLabel 对象
        self.label1 = QLabel("惩罚：")

        # 创建 QLineEdit 对象
        self.input_box1 = QLineEdit(self)
        self.input_box1.setPlaceholderText("在此输入新的惩罚...")

        # 创建确认按钮
        self.closeButton = QPushButton('确认', self)
        self.closeButton.clicked.connect(self.get_text)

        # 设置布局
        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout1.addWidget(self.label1)
        layout1.addWidget(self.input_box1)
        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.closeButton)
        layout.addLayout(layout1)
        layout.addLayout(bottomLayout)
        self.setLayout(layout)

    def get_text(self):
        acceptflag = 0
        if (len(self.input_box1.text()) != 0):
            acceptflag += 1
            self.name = self.input_box1.text()
            info = oper.select_class_ID(self.db, self.cursor, self.name)
            if (info != None):
                widget = QWidget()
                QMessageBox.information(widget, '信息', '该惩罚已存在') #触发的事件时弹出会话框
                return
            
        if acceptflag == 1:
            self.accept()
        else:
            widget = QWidget()
            QMessageBox.information(widget, '信息', '缺少信息') #触发的事件时弹出会话框

    def get_entered_Name(self):
        return self.name

class New_StudentWindow(QDialog):
    def __init__(self, db, cursor):
        super().__init__()
        self.db = db
        self.cursor = cursor
        self.ID = ''
        self.name = ''
        self.age = 0
        self.major = ''
        self.photo = ''
        self.setWindowTitle('输入新学生信息')
        self.resize(320, 200)
        self.init_ui()
    
    def init_ui(self):
        # 创建 QLabel 对象
        self.label1 = QLabel("学号：")
        self.label2 = QLabel("姓名：")
        self.label3 = QLabel("年龄：")
        self.label4 = QLabel("专业：")

        # 创建 QLineEdit 对象
        self.input_box1 = QLineEdit(self)
        self.input_box1.setPlaceholderText("在此输入新的学号...")
        self.input_box2 = QLineEdit(self)
        self.input_box2.setPlaceholderText("在此输入新的姓名...")
        self.input_box3 = QLineEdit(self)
        self.input_box3.setPlaceholderText("在此输入新的年龄...")
        self.input_box4 = QLineEdit(self)
        self.input_box4.setPlaceholderText("在此输入新的专业...")

        # 创建上传照片按钮
        self.chooseButton = QPushButton('选择要上传的照片', self)
        self.chooseButton.clicked.connect(self.choosePhoto)

        # 创建确认按钮
        self.closeButton = QPushButton('确认', self)
        self.closeButton.clicked.connect(self.get_text)

        # 设置布局
        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout1.addWidget(self.label1)
        layout1.addWidget(self.input_box1)
        layout2 = QHBoxLayout()
        layout2.addWidget(self.label2)
        layout2.addWidget(self.input_box2)
        layout3 = QHBoxLayout()
        layout3.addWidget(self.label3)
        layout3.addWidget(self.input_box3)
        layout4 = QHBoxLayout()
        layout4.addWidget(self.label4)
        layout4.addWidget(self.input_box4)
        layout5 = QHBoxLayout()
        layout5.addWidget(self.chooseButton)
        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.closeButton)
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        layout.addLayout(layout4)
        layout.addLayout(layout5)
        layout.addLayout(bottomLayout)
        self.setLayout(layout)

    def get_text(self):
        self.acceptflag = 0
        if (len(self.input_box1.text()) != 0):
            self.acceptflag += 1
            self.ID = self.input_box1.text()
            info = oper.select_student_baseinfo(self.db, self.cursor, self.ID)
            if (info != None):
                widget = QWidget()
                QMessageBox.information(widget, '信息', '该学号已存在') #触发的事件时弹出会话框
                return
            
        if (len(self.input_box2.text()) != 0):
            self.acceptflag += 1
            self.name = self.input_box2.text()
        if (len(self.input_box3.text()) != 0):
            try:
                self.age = int(self.input_box3.text())
                assert(self.age > 14 and self.age < 32)
                self.acceptflag += 1
            except Exception as e:
                print(f"ERROR:{e}")
                widget = QWidget()
                QMessageBox.information(widget, '信息', '年龄不合法') #触发的事件时弹出会话框
                return
            
        if (len(self.input_box4.text()) != 0):
            self.acceptflag += 1
            self.major = self.input_box4.text()

        if self.acceptflag == 4:
            self.accept()
        else:
            widget = QWidget()
            QMessageBox.information(widget, '信息', '缺少信息') #触发的事件时弹出会话框

    def choosePhoto(self):
        photo_path, _ = QFileDialog.getOpenFileName(self, "Select Photo", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if photo_path:
            # 读取图片并保存为二进制
            picture = open(photo_path, 'rb')
            pictureByte = picture.read()
            picture.close()
            self.photo = pictureByte

    def get_entered_ID(self):
        return self.ID
    
    def get_entered_Name(self):
        return self.name
    
    def get_entered_Age(self):
        return self.age
    
    def get_entered_Major(self):
        return self.major
        
    def get_entered_Photo(self):
        return self.photo

class Change_StudentWindow(QDialog):
    def __init__(self, db, cursor, oldinfo):
        super().__init__()
        self.ID = oldinfo[0]
        self.name = oldinfo[1]
        self.age = oldinfo[2]
        self.major = oldinfo[3]
        self.photo = oldinfo[4]
        self.acceptflag = False
        self.setWindowTitle(f'请输入要修改的内容，不需要修改则留空')
        self.resize(320, 200)
        self.init_ui()
    
    def init_ui(self):
        # 创建 QLabel 对象
        self.label1 = QLabel(f"从{self.ID}修改为：")
        self.label2 = QLabel(f"从{self.name}修改为：")
        self.label3 = QLabel(f"从{self.age}修改为：")
        self.label4 = QLabel(f"从{self.major}修改为：")

        # 创建 QLineEdit 对象
        self.input_box1 = QLineEdit(self)
        self.input_box1.setPlaceholderText("在此输入新的学号...")
        self.input_box2 = QLineEdit(self)
        self.input_box2.setPlaceholderText("在此输入新的姓名...")
        self.input_box3 = QLineEdit(self)
        self.input_box3.setPlaceholderText("在此输入新的年龄...")
        self.input_box4 = QLineEdit(self)
        self.input_box4.setPlaceholderText("在此输入新的专业...")

        # 创建上传照片按钮
        self.chooseButton = QPushButton('选择要上传的照片', self)
        self.chooseButton.clicked.connect(self.choosePhoto)

        # 创建确认按钮
        self.closeButton = QPushButton('确认', self)
        self.closeButton.clicked.connect(self.get_text)

        # 设置布局
        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout1.addWidget(self.label1)
        layout1.addWidget(self.input_box1)
        layout2 = QHBoxLayout()
        layout2.addWidget(self.label2)
        layout2.addWidget(self.input_box2)
        layout3 = QHBoxLayout()
        layout3.addWidget(self.label3)
        layout3.addWidget(self.input_box3)
        layout4 = QHBoxLayout()
        layout4.addWidget(self.label4)
        layout4.addWidget(self.input_box4)
        layout5 = QHBoxLayout()
        layout5.addWidget(self.chooseButton)
        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.closeButton)
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        layout.addLayout(layout4)
        layout.addLayout(layout5)
        layout.addLayout(bottomLayout)
        self.setLayout(layout)

    def get_text(self):
        
        if (len(self.input_box1.text()) != 0):
            self.acceptflag = True
            self.ID = self.input_box1.text()
        if (len(self.input_box2.text()) != 0):
            self.acceptflag = True
            self.name = self.input_box2.text()
        if (len(self.input_box3.text()) != 0):
            try:
                self.age = int(self.input_box3.text())
                assert(self.age > 14 and self.age < 32)
                self.acceptflag = True
            except Exception as e:
                print(f"ERROR:{e}")
                widget = QWidget()
                QMessageBox.information(widget, '信息', '年龄不合法') #触发的事件时弹出会话框
        if (len(self.input_box4.text()) != 0):
            self.acceptflag = True
            self.major = self.input_box4.text()

        if self.acceptflag:
            self.accept()

    def choosePhoto(self):
        photo_path, _ = QFileDialog.getOpenFileName(self, "Select Photo", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if photo_path:
            # 读取图片并保存为二进制
            picture = open(photo_path, 'rb')
            pictureByte = picture.read()
            picture.close()
            self.photo = pictureByte
            self.acceptflag = True

    def get_entered_ID(self):
        return self.ID
    
    def get_entered_Name(self):
        return self.name
    
    def get_entered_Age(self):
        return self.age
    
    def get_entered_Major(self):
        return self.major
        
    def get_entered_Photo(self):
        return self.photo

class New_ClassWindow(QDialog):
    def __init__(self, db, cursor):
        super().__init__()
        self.db = db
        self.cursor = cursor
        self.ID = ''
        self.name = ''
        self.point = 0
        self.setWindowTitle('输入新课程信息')
        self.resize(320, 200)
        self.init_ui()
    
    def init_ui(self):
        # 创建 QLabel 对象
        self.label1 = QLabel("课程号：")
        self.label2 = QLabel("课程名：")
        self.label3 = QLabel("学分：")

        # 创建 QLineEdit 对象
        self.input_box1 = QLineEdit(self)
        self.input_box1.setPlaceholderText("在此输入新的课程号...")
        self.input_box2 = QLineEdit(self)
        self.input_box2.setPlaceholderText("在此输入新的课程名...")
        self.input_box3 = QLineEdit(self)
        self.input_box3.setPlaceholderText("在此输入新的学分...")

        # 创建确认按钮
        self.closeButton = QPushButton('确认', self)
        self.closeButton.clicked.connect(self.get_text)

        # 设置布局
        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout1.addWidget(self.label1)
        layout1.addWidget(self.input_box1)
        layout2 = QHBoxLayout()
        layout2.addWidget(self.label2)
        layout2.addWidget(self.input_box2)
        layout3 = QHBoxLayout()
        layout3.addWidget(self.label3)
        layout3.addWidget(self.input_box3)
        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.closeButton)
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        layout.addLayout(bottomLayout)
        self.setLayout(layout)

    def get_text(self):
        acceptflag = 0
        if (len(self.input_box1.text()) != 0):
            acceptflag += 1
            self.ID = self.input_box1.text()
            info = oper.select_class_ID(self.db, self.cursor, self.ID)
            if (info != None):
                widget = QWidget()
                QMessageBox.information(widget, '信息', '该课程号已存在') #触发的事件时弹出会话框
                return
            
        if (len(self.input_box2.text()) != 0):
            acceptflag += 1
            self.name = self.input_box2.text()
        if (len(self.input_box3.text()) != 0):
            try:
                self.point = int(self.input_box3.text())
                assert(self.point > 0 and self.point < 7)
                acceptflag += 1
            except Exception as e:
                print(f"ERROR:{e}")
                widget = QWidget()
                QMessageBox.information(widget, '信息', '学分不合法') #触发的事件时弹出会话框
                return

        if acceptflag == 3:
            self.accept()
        else:
            widget = QWidget()
            QMessageBox.information(widget, '信息', '缺少信息') #触发的事件时弹出会话框


    def get_entered_ID(self):
        return self.ID
    
    def get_entered_Name(self):
        return self.name
    
    def get_entered_Point(self):
        return self.point

class Change_ClassWindow(QDialog):
    def __init__(self, db, cursor, oldinfo):
        super().__init__()
        self.ID = oldinfo[0]
        self.name = oldinfo[1]
        self.point = oldinfo[2]
        self.setWindowTitle(f'请输入要修改的内容，不需要修改则留空')
        self.resize(320, 200)
        self.init_ui()
    
    def init_ui(self):
        # 创建 QLabel 对象
        self.label1 = QLabel(f"从{self.ID}修改为：")
        self.label2 = QLabel(f"从{self.name}修改为：")
        self.label3 = QLabel(f"从{self.point}修改为：")

        # 创建 QLineEdit 对象
        self.input_box1 = QLineEdit(self)
        self.input_box1.setPlaceholderText("在此输入新的课程号...")
        self.input_box2 = QLineEdit(self)
        self.input_box2.setPlaceholderText("在此输入新的课程名...")
        self.input_box3 = QLineEdit(self)
        self.input_box3.setPlaceholderText("在此输入新的学分...")

        # 创建确认按钮
        self.closeButton = QPushButton('确认', self)
        self.closeButton.clicked.connect(self.get_text)

        # 设置布局
        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout1.addWidget(self.label1)
        layout1.addWidget(self.input_box1)
        layout2 = QHBoxLayout()
        layout2.addWidget(self.label2)
        layout2.addWidget(self.input_box2)
        layout3 = QHBoxLayout()
        layout3.addWidget(self.label3)
        layout3.addWidget(self.input_box3)
        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.closeButton)
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        layout.addLayout(bottomLayout)
        self.setLayout(layout)

    def get_text(self):
        acceptflag = False
        if (len(self.input_box1.text()) != 0):
            acceptflag = True
            self.ID = self.input_box1.text()
        if (len(self.input_box2.text()) != 0):
            acceptflag = True
            self.name = self.input_box2.text()
        if (len(self.input_box3.text()) != 0):
            try:
                self.point = int(self.input_box3.text())
                assert(self.point > 0 and self.point < 7)
                acceptflag = True
            except Exception as e:
                print(f"ERROR:{e}")
                widget = QWidget()
                QMessageBox.information(widget, '信息', '学分不合法') #触发的事件时弹出会话框
        if acceptflag:
            self.accept()

    def get_entered_ID(self):
        return self.ID
    
    def get_entered_Name(self):
        return self.name
    
    def get_entered_Point(self):
        return self.point

class Entertext(QDialog):
    def __init__(self, action, content):
        super().__init__()
        self.text = ''
        self.setWindowTitle(f'请输入要{action}的{content}')
        self.resize(320, 200)
        self.init_ui()
    
    def init_ui(self):
        # 创建 QLineEdit 对象
        self.input_box = QLineEdit(self)
        self.input_box.setPlaceholderText("在此输入...")

        # 创建确认按钮
        self.closeButton = QPushButton('确认', self)
        self.closeButton.clicked.connect(self.get_text)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.input_box)
        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.closeButton)
        layout.addLayout(bottomLayout)
        self.setLayout(layout)

    def get_text(self):
        self.text = self.input_box.text()
        self.accept()

    def get_entered_text(self):
        return self.text
        

class select_allTable(QWidget):
    def __init__(self, db, cursor, kind, name = ''):
        super().__init__()
        self.db = db
        self.cursor = cursor
        self.kind = kind
        self.name = name
        tablename = ['学生名单','课程','学生名单','奖项','惩罚']
        self.setWindowTitle(tablename[kind])
        self.resize(600, 750)
        self.init_ui()
    
    def init_ui(self):
        if (self.kind == 0):
            info = oper.select_students_all(self.db, self.cursor)
        if (self.kind == 1):
            info = oper.select_classes_all(self.db, self.cursor)
        if (self.kind == 2):
            info = oper.select_students_name(self.db, self.cursor, self.name)
        if (self.kind == 3):
            info = oper.select_prize_all(self.db, self.cursor)
        if (self.kind == 4):
            info = oper.select_punish_all(self.db, self.cursor)
        #print(info)
        # 创建表格
        try:
            if (self.kind == 0 or self.kind == 2):
                leninfo = 4
                self.table = QTableWidget(len(info), leninfo)
                self.table.setHorizontalHeaderLabels(['学号','姓名','年龄','专业'])
            if (self.kind == 1):
                leninfo = 3
                self.table = QTableWidget(len(info), leninfo)
                self.table.setHorizontalHeaderLabels(['课程号','课程名','学分'])
            if (self.kind == 3):
                leninfo = 2
                self.table = QTableWidget(len(info), leninfo)
                self.table.setHorizontalHeaderLabels(['奖项','等级'])
            if (self.kind == 4):
                leninfo = 1
                self.table = QTableWidget(len(info), leninfo)
                self.table.setHorizontalHeaderLabels(['惩罚'])

        except Exception as e:
            print(f"ERROR:{e}")
            return
        
        # 填充表格数据
        for i in range(len(info)):
            for j in range(leninfo):
                    item = QTableWidgetItem(str(info[i][j]))
                    self.table.setItem(i, j, item)

        # 创建关闭按钮
        self.closeButton = QPushButton('Close', self)
        self.closeButton.clicked.connect(self.close)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.closeButton)
        layout.addLayout(bottomLayout)
        self.setLayout(layout)



class Main_Window(QWidget):
    def __init__(self, db, cursor):
        super().__init__()
        self.db = db
        self.cursor = cursor
        self.setWindowTitle('学籍管理系统')
        self.resize(600, 750)
        self.btn1 = QPushButton('查看学生名单', self)
        self.btn2 = QPushButton('查看全部课程', self)
        self.btn3 = QPushButton('按姓名查询', self)
        self.btn4 = QPushButton('学号查询具体信息', self)
        self.btn5 = QPushButton('新增学生', self)
        self.btn6 = QPushButton('新增课程', self)
        self.btn7 = QPushButton('新增奖项', self)
        self.btn8 = QPushButton('新增惩罚', self)
        self.btn9 = QPushButton('修改课程信息', self)
        self.btn10 = QPushButton('修改学生信息', self)
        self.btn11 = QPushButton('删除学生', self)
        self.btn12 = QPushButton('删除课程', self)
        self.btn13 = QPushButton('删除奖项', self)
        self.btn14 = QPushButton('删除惩罚', self)
        self.btn15 = QPushButton('查看全部奖项', self)
        self.btn16 = QPushButton('查看全部惩罚', self)
        self.btn17 = QPushButton('为学生添加惩罚', self)
        self.btn18 = QPushButton('为学生添加奖项', self)
        self.btn19 = QPushButton('新增成绩', self)
        self.btn20 = QPushButton('删除成绩', self)
        self.btn21 = QPushButton('重置数据库', self)
        self.init_ui()

    def init_ui(self):
        self.btn1.resize(110,55)
        self.btn1.move(50, 50)   #按钮的位置
        self.btn1.clicked.connect(self.check_all_students) #使用connect绑定事件，点击按钮时触发

        self.btn2.resize(110,55)
        self.btn2.move(250, 50)   #按钮的位置
        self.btn2.clicked.connect(self.check_all_classes) #使用connect绑定事件，点击按钮时触发

        self.btn3.resize(110,55)
        self.btn3.move(450, 50)   #按钮的位置
        self.btn3.clicked.connect(self.check_student_name) #使用connect绑定事件，点击按钮时触发

        self.btn4.resize(110,55)
        self.btn4.move(50, 150)   #按钮的位置
        self.btn4.clicked.connect(self.check_student_info) #使用connect绑定事件，点击按钮时触发

        self.btn5.resize(110,55)
        self.btn5.move(250, 150)   #按钮的位置
        self.btn5.clicked.connect(self.add_student) #使用connect绑定事件，点击按钮时触发

        self.btn6.resize(110,55)
        self.btn6.move(450, 150)   #按钮的位置
        self.btn6.clicked.connect(self.add_class) #使用connect绑定事件，点击按钮时触发

        self.btn7.resize(110,55)
        self.btn7.move(50, 250)   #按钮的位置
        self.btn7.clicked.connect(self.add_prize) #使用connect绑定事件，点击按钮时触发

        self.btn8.resize(110,55)
        self.btn8.move(250, 250)   #按钮的位置
        self.btn8.clicked.connect(self.add_punish) #使用connect绑定事件，点击按钮时触发

        self.btn9.resize(110,55)
        self.btn9.move(450, 250)   #按钮的位置
        self.btn9.clicked.connect(self.change_class) #使用connect绑定事件，点击按钮时触发

        self.btn10.resize(110,55)
        self.btn10.move(50, 350)   #按钮的位置
        self.btn10.clicked.connect(self.change_student) #使用connect绑定事件，点击按钮时触发

        self.btn11.resize(110,55)
        self.btn11.move(250, 350)   #按钮的位置
        self.btn11.clicked.connect(self.delete_student) #使用connect绑定事件，点击按钮时触发

        self.btn12.resize(110,55)
        self.btn12.move(450, 350)   #按钮的位置
        self.btn12.clicked.connect(self.delete_class) #使用connect绑定事件，点击按钮时触发

        self.btn13.resize(110,55)
        self.btn13.move(50, 450)   #按钮的位置
        self.btn13.clicked.connect(self.delete_prize) #使用connect绑定事件，点击按钮时触发

        self.btn14.resize(110,55)
        self.btn14.move(250, 450)   #按钮的位置
        self.btn14.clicked.connect(self.delete_punish) #使用connect绑定事件，点击按钮时触发

        self.btn15.resize(110,55)
        self.btn15.move(450, 450)   #按钮的位置
        self.btn15.clicked.connect(self.check_all_prizes) #使用connect绑定事件，点击按钮时触发

        self.btn16.resize(110,55)
        self.btn16.move(50, 550)   #按钮的位置
        self.btn16.clicked.connect(self.check_all_punishments) #使用connect绑定事件，点击按钮时触发

        self.btn17.resize(110,55)
        self.btn17.move(250, 550)   #按钮的位置
        self.btn17.clicked.connect(self.add_punish_for_student) #使用connect绑定事件，点击按钮时触发

        self.btn18.resize(110,55)
        self.btn18.move(450, 550)   #按钮的位置
        self.btn18.clicked.connect(self.add_prize_for_student) #使用connect绑定事件，点击按钮时触发

        self.btn19.resize(110,55)
        self.btn19.move(50, 650)   #按钮的位置
        self.btn19.clicked.connect(self.add_score) #使用connect绑定事件，点击按钮时触发

        self.btn20.resize(110,55)
        self.btn20.move(250, 650)   #按钮的位置
        self.btn20.clicked.connect(self.delete_score) #使用connect绑定事件，点击按钮时触发

        self.btn21.resize(110,55)
        self.btn21.move(450, 650)   #按钮的位置
        self.btn21.clicked.connect(self.reset_db) #使用connect绑定事件，点击按钮时触发

    def check_all_students(self):
        self.tableWindow = select_allTable(self.db, self.cursor, 0, '')
        self.tableWindow.show()
    
    def check_all_classes(self):
        self.tableWindow = select_allTable(self.db, self.cursor, 1, '')
        self.tableWindow.show()

    def check_student_name(self):
        getname = Entertext('查询','姓名')
        if getname.exec():
            # 如果用户点击确认按钮，则获取输入的文本
            name = getname.get_entered_text()
            self.tableWindow = select_allTable(self.db, self.cursor, 2, name)
            self.tableWindow.show()
    
    def check_student_info(self):
        self.newWindow = Check_StudentWindow(self.db, self.cursor)
        if self.newWindow.exec():
            newID = self.newWindow.get_entered_ID()
            newName = self.newWindow.get_entered_Name()
            newAge = self.newWindow.get_entered_Age()
            newMajor = self.newWindow.get_entered_Major()
            newPhoto = self.newWindow.get_entered_Photo()
            self.resultWindow = ResultWindow(self.db, self.cursor, newID, newName, newAge, newMajor, newPhoto)
            self.resultWindow.show()

    def add_student(self):
        self.newWindow = New_StudentWindow(self.db, self.cursor)
        if self.newWindow.exec():
            newID = self.newWindow.get_entered_ID()
            newName = self.newWindow.get_entered_Name()
            newAge = self.newWindow.get_entered_Age()
            newMajor = self.newWindow.get_entered_Major()
            newPhoto = self.newWindow.get_entered_Photo()
            oper.add_student(self.db, self.cursor, newID, newName, newAge, newMajor, newPhoto)
            widget = QWidget()
            QMessageBox.information(widget, '信息', '添加成功') #触发的事件时弹出会话框
    
    def add_class(self):
        self.newWindow = New_ClassWindow(self.db, self.cursor)
        if self.newWindow.exec():
            newID = self.newWindow.get_entered_ID()
            newName = self.newWindow.get_entered_Name()
            newPoint = self.newWindow.get_entered_Point()
            oper.add_class(self.db, self.cursor, newID, newName, newPoint)
            widget = QWidget()
            QMessageBox.information(widget, '信息', '添加成功') #触发的事件时弹出会话框

    def add_prize(self):
        self.newWindow = New_PrizeWindow(self.db, self.cursor)
        if self.newWindow.exec():
            newName = self.newWindow.get_entered_Name()
            newGrade = self.newWindow.get_entered_Grade()
            oper.add_prize(self.db, self.cursor, newName, newGrade)
            widget = QWidget()
            QMessageBox.information(widget, '信息', '添加成功') #触发的事件时弹出会话框

    def add_punish(self):
        self.newWindow = New_PunishWindow(self.db, self.cursor)
        if self.newWindow.exec():
            newName = self.newWindow.get_entered_Name()
            punishments.add_punishment(self.db, self.cursor, newName)
            widget = QWidget()
            QMessageBox.information(widget, '信息', '添加成功') #触发的事件时弹出会话框

    def change_class(self):
        getID = Entertext('修改','课程号')
        if getID.exec():
            # 如果用户点击确认按钮，则获取输入的文本
            oldID = getID.get_entered_text()
            oldinfo = oper.select_class_ID(self.db, self.cursor, oldID)
            if oldinfo == None:
                widget = QWidget()
                QMessageBox.information(widget, '信息', '课程不存在')
            else:
                self.changeWindow = Change_ClassWindow(self.db, self.cursor, oldinfo)
                if self.changeWindow.exec():
                    newID = self.changeWindow.get_entered_ID()
                    newName = self.changeWindow.get_entered_Name()
                    newPoint = self.changeWindow.get_entered_Point()
                    oper.change_class(self.db, self.cursor, oldID, 1, newName)
                    oper.change_class(self.db, self.cursor, oldID, 2, newPoint)
                    oper.changeid_class(self.db, self.cursor, oldID, newID)
                    widget = QWidget()
                    QMessageBox.information(widget, '信息', '修改成功') #触发的事件时弹出会话框

    def change_student(self):
        getID = Entertext('修改','学生的学号')
        if getID.exec():
            # 如果用户点击确认按钮，则获取输入的文本
            oldID = getID.get_entered_text()
            oldinfo = oper.select_student_baseinfo(self.db, self.cursor, oldID)
            if oldinfo == None:
                widget = QWidget()
                QMessageBox.information(widget, '信息', '学生不存在')
            else:
                self.changeWindow = Change_StudentWindow(self.db, self.cursor, oldinfo)
                if self.changeWindow.exec():
                    newID = self.changeWindow.get_entered_ID()
                    newName = self.changeWindow.get_entered_Name()
                    newAge = self.changeWindow.get_entered_Age()
                    newMajor = self.changeWindow.get_entered_Major()
                    newPhoto = self.changeWindow.get_entered_Photo()
                    oper.change_student(self.db, self.cursor, oldID, 1, newName)
                    oper.change_student(self.db, self.cursor, oldID, 2, newAge)
                    oper.change_student(self.db, self.cursor, oldID, 3, newMajor)
                    oper.change_student(self.db, self.cursor, oldID, 4, newPhoto)
                    oper.changeid_student(self.db, self.cursor, oldID, newID)
                    widget = QWidget()
                    QMessageBox.information(widget, '信息', '修改成功') #触发的事件时弹出会话框

    def delete_student(self):
        getID = Entertext('删除','学生的学号')
        if getID.exec():
            oldID = getID.get_entered_text()
            oldinfo = oper.select_student_baseinfo(self.db, self.cursor, oldID)
            if oldinfo == None:
                widget = QWidget()
                QMessageBox.information(widget, '信息', '学生不存在')
            else:
                oper.delete_student(self.db, self.cursor, oldID)
                widget = QWidget()
                QMessageBox.information(widget, '信息', '删除成功') #触发的事件时弹出会话框

    def delete_class(self):
        getID = Entertext('删除','课程号')
        if getID.exec():
            oldID = getID.get_entered_text()
            oldinfo = oper.select_class_ID(self.db, self.cursor, oldID)
            if oldinfo == None:
                widget = QWidget()
                QMessageBox.information(widget, '信息', '课程不存在')
            else:
                oper.delete_class(self.db, self.cursor, oldID)
                widget = QWidget()
                QMessageBox.information(widget, '信息', '删除成功') #触发的事件时弹出会话框

    def delete_prize(self):
        getID = Entertext('删除','奖项')
        if getID.exec():
            oldID = getID.get_entered_text()
            oldinfo = oper.select_prize_name(self.db, self.cursor, oldID)
            if oldinfo == None:
                widget = QWidget()
                QMessageBox.information(widget, '信息', '奖项不存在')
            else:
                oper.delete_prize(self.db, self.cursor, oldID)
                widget = QWidget()
                QMessageBox.information(widget, '信息', '删除成功') #触发的事件时弹出会话框

    def delete_punish(self):
        getID = Entertext('删除','惩罚')
        if getID.exec():
            oldID = getID.get_entered_text()
            oldinfo = oper.select_punish_name(self.db, self.cursor, oldID)
            if oldinfo == None:
                widget = QWidget()
                QMessageBox.information(widget, '信息', '惩罚不存在')
            else:
                oper.delete_punishment(self.db, self.cursor, oldID)
                widget = QWidget()
                QMessageBox.information(widget, '信息', '删除成功') #触发的事件时弹出会话框

    def check_all_prizes(self):
        self.tableWindow = select_allTable(self.db, self.cursor, 3, '')
        self.tableWindow.show()
    
    def check_all_punishments(self):
        self.tableWindow = select_allTable(self.db, self.cursor, 4, '')
        self.tableWindow.show()

    def add_punish_for_student(self):
        self.newWindow = add_timescoreWindow(self.db, self.cursor, 1)
        if self.newWindow.exec():
            newID = self.newWindow.get_entered_ID()
            newName = self.newWindow.get_entered_Name()
            newTime = self.newWindow.get_entered_timescore()
            oper.add_punishtime(self.db, self.cursor, newID, newName, newTime)
            widget = QWidget()
            QMessageBox.information(widget, '信息', '添加成功') #触发的事件时弹出会话框

    def add_prize_for_student(self):
        self.newWindow = add_timescoreWindow(self.db, self.cursor, 0)
        if self.newWindow.exec():
            newID = self.newWindow.get_entered_ID()
            newName = self.newWindow.get_entered_Name()
            newTime = self.newWindow.get_entered_timescore()
            oper.add_punishtime(self.db, self.cursor, newID, newName, newTime)
            widget = QWidget()
            QMessageBox.information(widget, '信息', '添加成功') #触发的事件时弹出会话框

    def add_score(self):
        self.newWindow = add_timescoreWindow(self.db, self.cursor, 2)
        if self.newWindow.exec():
            newID = self.newWindow.get_entered_ID()
            newName = self.newWindow.get_entered_Name()
            newScore = self.newWindow.get_entered_timescore()
            oper.add_score(self.db, self.cursor, newID, newName, newScore)
            widget = QWidget()
            QMessageBox.information(widget, '信息', '添加成功') #触发的事件时弹出会话框

    def delete_score(self):
        self.newWindow = delete_scoreWindow(self.db, self.cursor)
        if self.newWindow.exec():
            newsID = self.newWindow.get_entered_sID()
            newcID = self.newWindow.get_entered_cID()
            oldinfo = oper.select_student_class_score(self.db, self.cursor, newsID, newcID)
            if oldinfo == None:
                widget = QWidget()
                QMessageBox.information(widget, '信息', '成绩不存在')
            else:
                oper.delete_score(self.db, self.cursor, newsID, newcID)
                widget = QWidget()
                QMessageBox.information(widget, '信息', '删除成功') #触发的事件时弹出会话框

    def reset_db(self):
        initialize.init(self.db, self.cursor)
        widget = QWidget()
        QMessageBox.information(widget, '信息', '成功重置数据库') #触发的事件时弹出会话框



