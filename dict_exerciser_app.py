__author__ = "Tolga Erdönmez"
__version__ = "1.0"
from PyQt5.QtWidgets import QWidget,QApplication,QPushButton,QLabel,QLineEdit,QHBoxLayout,QVBoxLayout,QComboBox,QMessageBox,QStyleFactory
from PyQt5 import QtGui
from PyQt5 import QtCore
import sys
import requests
import sqlite3
import os

class app_dict_login(QWidget):

    def __init__(self,lang = 'tr'):
        super().__init__()
        self.current_lang = lang
        self.init_ui()
        self.connectdb()
    def connectdb(self):
        self.connection = sqlite3.connect("userdata.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS userdata (username TEXT,password TEXT,user_practice_words TEXT)")
        self.connection.commit()

    def init_ui(self):
        self.status = False
        # True logged in
        self.usernameInput = QLineEdit()
        self.passwordInput = QLineEdit()
        self.usernameLabel = QLabel()#("Username:")
        self.passwordLabel = QLabel()#("Password:")
        
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.login_output = QLabel("")
        self.log_in = QPushButton()#("Login")
        self.register = QPushButton()#("Register")
        v_box = QVBoxLayout()
        v_box.addWidget(self.usernameLabel)
        v_box.addWidget(self.usernameInput)
        v_box.addWidget(self.passwordLabel)
        v_box.addWidget(self.passwordInput)
        v_box.addWidget(self.login_output)
        v_box.addWidget(self.log_in)
        v_box.addWidget(self.register)
        v_box.addStretch()
        h_box = QHBoxLayout()
        h_box.addStretch()
        h_box.addLayout(v_box)
        h_box.addStretch()
        #adding lang choices
        v_box.addLayout(self.lang_choice_widgets())
        
        #EVENTS
        self.log_in.clicked.connect(self.sys_login)
        self.register.clicked.connect(self.sys_register)
        self.setLayout(h_box)
        self.setGeometry(750,200,500,250)
        
        #setting language
        self.set_lang(self.current_lang)
        
        self.show()
    def lang_choice_widgets(self):
        h_box = QHBoxLayout()
        h_box.addStretch()
        #WIDGETS & WIDGETS
        # GET FLAG IMG FROM 'lang' folder and creates pushbutton(with icon) and puts them into the 'h_box'
        for i,j,g in os.walk('lang'):
            for x in g:
                # i folder name x img name
                lang_button = QPushButton()
                lang_button.setObjectName('lang_{}'.format(x.split('.')[0][1:]))
                lang_button.setIcon(QtGui.QIcon('{}/{}'.format(i,x)))
                #adding custom events to buttons
                lang_button.clicked.connect(lambda: self.set_lang(self.sender().objectName().split('_')[1]))
                h_box.addWidget(lang_button)
                
        h_box.addStretch()
        
        return h_box
    
    def set_lang(self,select):
        #lang_choice = self.sender().objectName()
        #print(lang_choice)
        def turkish():
            self.usernameLabel.setText('Kullanıcı Adı: ')
            self.passwordLabel.setText('Şifre: ')
            self.log_in.setText('Giriş Yap')
            self.register.setText('Üye Ol')
            self.setWindowTitle('Kelime Çalışması & Çeviri | Giriş Yap')
        def english():
            self.usernameLabel.setText('Username: ')
            self.passwordLabel.setText('Password: ')
            self.log_in.setText('Log in')
            self.register.setText('Register')
            self.setWindowTitle('Word Exerciser & Translate | Log In')
        def german():
            self.usernameLabel.setText('Benutzername: ')
            self.passwordLabel.setText('Passwort: ')
            self.log_in.setText('Anmelden')
            self.register.setText('Registrieren')
            self.setWindowTitle('Wörter üben & Übersetzen | Anmelden')
        if select == 'tr':
            turkish()
        elif select == 'en':
            english()
        elif select == 'de':
            german()

        self.current_lang = select
    def sys_login(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()
        self.cursor.execute("SELECT * FROM userdata WHERE username = ? and password = ?",(username,password))
        user_data = self.cursor.fetchall()
        if len(user_data) == 0:
            self.status = False
            self.login_output.setText("There is no user named {}\n".format(username) + "You can create one by clicking 'register' ")
        else:
            self.status = True
            self.login_output.setText("Logged Succesfully")
            self.passwordInput.clear()
            self.close()
            self.dict_app_userpanel = app_word_translate(user_data,self.current_lang)

    def sys_register(self):
        self.cursor.execute('SELECT username FROM userdata')
        current_users = self.cursor.fetchall()
        new_username = self.usernameInput.text()
        new_password = self.passwordInput.text()
        #cheking if there is existing username as same as 'new_username'
        check_if_same = 'nope'
        for i in current_users:
            if i[0] == new_username:
                check_if_same = 'exists'
                break
        if new_username == '':
            msg = ["Lütfen geçerli bir kullanıcı adı giriniz !",'Please enter a valid username !',"Schreib bitte ein valider Benutzername !"]
            if self.current_lang == 'tr':
                self.login_output.setText(msg[0])
            elif self.current_lang == 'en':
                self.login_output.setText(msg[1])
            elif self.current_lang == 'de':
                self.login_output.setText(msg[2])
            
        elif check_if_same == 'exists':
            msg = ["Zaten böyle bir kullanıcı var\nlütfen başka bir kullanıcı adı deneyiniz",
                   'That username already exists\nplease try a new one',"Es gibt selben Benutzername\nVersucht bitte ein ander !"]
            if self.current_lang == 'tr':
                self.login_output.setText(msg[0])
            elif self.current_lang == 'en':
                self.login_output.setText(msg[1])
            elif self.current_lang == 'de':
                self.login_output.setText(msg[2])
        else:
            practice_words = str()
            self.cursor.execute("INSERT INTO userdata Values(?,?,?)",(new_username,new_password,practice_words))
            self.connection.commit()
            msg = ["Başarıyla üye oldunuz !",'Successfully registered !',"Du hast mit Erfolg registriert !"]
            if self.current_lang == 'tr':
                self.login_output.setText(msg[0])
            elif self.current_lang == 'en':
                self.login_output.setText(msg[1])
            elif self.current_lang == 'de':
                self.login_output.setText(msg[2])

class app_word_translate(QWidget):
    def __init__(self,user_data,lang):
        super().__init__()
        self.current_lang = lang
        self.user_data = user_data[0]
        self.setupUI()  
        self.connect_user()
        

    def connect_user(self):
        self.connection = sqlite3.connect('userdata.db')
        self.cursor = self.connection.cursor()
        self.connection.commit()
    def setupUI(self):
        #Widgets
        self.word_input = QLineEdit()
        self.from_label = QLabel()
        self.to_label = QLabel()
        lic_label = QLabel()
        lic_label.setText('<a href="https://tech.yandex.com/dictionary/" style="color: black;">Powered by Yandex.Dictionary</a>')
        lic_label.setOpenExternalLinks(True)
        author_label = QLabel('Ahmet Tolga Erdönmez')
        #user panel
        self.logout_btn = QPushButton()
        self.user_label = QLabel()
        self.go_practice = QPushButton()
        self.show_practice_list = QPushButton()
        self.check_first = 0
        #main panel
        self.translate_btn = QPushButton()
        self.trans_output = QLabel('')
        self.add_word_to_list = QPushButton()
        self.lang_one = QComboBox()
        self.lang_two = QComboBox()
        self.word = QLineEdit('')
        #Layouts
        self.v_box = QVBoxLayout()
        h_box_label = QHBoxLayout()
        lic_h_box = QHBoxLayout()
        author_h_box = QHBoxLayout()
        
        lic_h_box.addStretch()
        lic_h_box.addWidget(lic_label)
        lic_h_box.addStretch()

        author_h_box.addStretch()
        author_h_box.addWidget(author_label)
        author_h_box.addStretch()
        
        h_box_label.addWidget(self.from_label)
        h_box_label.addStretch()
        h_box_label.addWidget(self.to_label)
        h_box_label.addStretch()
        
        self.h_box_combo_box = QHBoxLayout()
        self.h_box_output = QHBoxLayout()
        
        self.h_box_combo_box.addWidget(self.lang_one)
        self.lang_one.addItem('Türkçe')
        self.lang_one.addItem('English')
        self.lang_one.addItem('Deutsch')
        self.lang_one.addItem('Français')
        self.h_box_combo_box.addWidget(self.lang_two)
        self.lang_two.addItem('Türkçe')
        self.lang_two.addItem('English')
        self.lang_two.addItem('Deutsch')
        self.lang_two.addItem('Français')
        self.v_box.addWidget(self.user_label)
        self.v_box.addLayout(h_box_label)
        self.v_box.addLayout(self.h_box_combo_box)
        self.v_box.addWidget(self.word)
        self.v_box.addWidget(self.translate_btn)

        self.v_box.addLayout(self.h_box_output)
        #self.v_box.addStretch()
        self.v_box.addWidget(self.go_practice)
        self.v_box.addWidget(self.show_practice_list)
        self.v_box.addWidget(self.logout_btn)
        self.v_box.addStretch()
        self.v_box.addLayout(self.lang_choice_widgets())
        self.v_box.addStretch()
        self.v_box.addLayout(lic_h_box)
        self.v_box.addLayout(author_h_box)
        #Events
        self.translate_btn.clicked.connect(self.event_get_lang_choice)
        self.setLayout(self.v_box)
        self.setGeometry(750,300,300,350)
        
        self.add_word_to_list.clicked.connect(self.event_add_to_list)
        self.logout_btn.clicked.connect(self.logout_to_main_app)
        self.show_practice_list.clicked.connect(self.event_see_practice_list)
        self.go_practice.clicked.connect(self.event_go_practice)
        #setting language
        self.set_lang(self.current_lang)
        
        self.show()
    def lang_choice_widgets(self):
        h_box = QHBoxLayout()
        h_box.addStretch()
        #WIDGETS & WIDGETS
        # GET FLAG IMG FROM 'lang' folder and creates pushbutton(with icon) and puts them into the 'h_box'
        for i,j,g in os.walk('lang'):
            for x in g:
                # i folder name x img name
                lang_button = QPushButton()
                lang_button.setObjectName('lang_{}'.format(x.split('.')[0][1:]))
                lang_button.setIcon(QtGui.QIcon('{}/{}'.format(i,x)))
                #adding custom events to buttons
                lang_button.clicked.connect(lambda: self.set_lang(self.sender().objectName().split('_')[1]))
                h_box.addWidget(lang_button)
                
        h_box.addStretch()

        return h_box
    def set_lang(self,lang):
        def turkish():
            self.setWindowTitle('Kelime Çalışması & Çeviri')
            self.logout_btn.setText('Çıkış yap')
            self.user_label.setText("Merhaba! {}".format(self.user_data[0].capitalize()))
            self.go_practice.setText('Kelimelerini çalış !')
            self.show_practice_list.setText('Çalışma listeni gör !')
            self.translate_btn.setText('Çevir')
            self.add_word_to_list.setText('Ekle')
            self.add_word_to_list.setToolTip('Çalışma listene ekle !')
            self.from_label.setText('   Neyden')
            self.to_label.setText('Neye')
        def english():
            self.setWindowTitle('Word Practice & Translate')
            self.logout_btn.setText('Log out')
            self.user_label.setText("Hi! {}".format(self.user_data[0].capitalize()))
            self.go_practice.setText('Practice Words !')
            self.show_practice_list.setText('See Your Practice List')
            self.translate_btn.setText('Translate')
            self.add_word_to_list.setText('Add')
            self.add_word_to_list.setToolTip('Add to your practice list !')
            self.from_label.setText('   From')
            self.to_label.setText('To')
        def deutsch():
            self.setWindowTitle('Wort Üben & übersetzen')
            self.logout_btn.setText('Abmelden')
            self.user_label.setText("Hallo! {}".format(self.user_data[0].capitalize()))
            self.go_practice.setText('Üben Wörter !')
            self.show_practice_list.setText('Sieh deine Liste !')
            self.translate_btn.setText('Übersetzt')
            self.add_word_to_list.setText('Hinzufügen')
            self.add_word_to_list.setToolTip('Füg deine Liste hinzu !')
            self.from_label.setText('   Von')
            self.to_label.setText('Zu')
        if lang == 'tr':
            turkish()
        elif lang == 'en':
            english()
        elif lang == 'de':
            deutsch()
        self.current_lang = lang
    def event_get_lang_choice(self):
        langs = ['tr','en','de','fr']
        l1 = str()
        l2 = str()
        if self.lang_one.currentText() == self.lang_two.currentText():
            msg = ["Aynı dilden aynı dile çevirilmiyor !","Can't translate from same language !","Kann nicht zu selben Sprache übersetzen !"]
            if self.current_lang == 'tr':
                msg_box = QMessageBox.warning(self, '!!!', msg[0] , QMessageBox.Ok)
            elif self.current_lang == 'en':
                msg_box = QMessageBox.warning(self, '!!!', msg[1] , QMessageBox.Ok)
            elif self.current_lang == 'de':
                msg_box = QMessageBox.warning(self, '!!!', msg[2] , QMessageBox.Ok)
        else:
            if self.lang_one.currentText() == "Türkçe":
                l1 = 'tr'
                l2 = self.lang_two.currentText()[0:2].lower()
            elif self.lang_two.currentText() == "Türkçe":
                l1 = self.lang_one.currentText()[0:2].lower()
                l2 = 'tr'
            else:
                l1 = self.lang_one.currentText()[0:2].lower()
                l2 = self.lang_two.currentText()[0:2].lower()
            lang = l1 + '-' + l2
            self.get_trans(lang)
    def get_trans(self,lang):
        base_url = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key=dict.1.1.20180424T202020Z.dbeff593adc28b99.4ee8cc89b87584c797a29178d75bef63add3a05a&'
        custom_url = 'lang={}&text={}'.format(lang,self.word.text())
        dict_val = requests.get(base_url + custom_url).json()
        
        try:
            self.trans_output.setText(dict_val['def'][0]['tr'][0]['text'])
            if self.check_first == 0:
                self.h_box_output.addStretch()
                self.h_box_output.addWidget(self.trans_output)
                self.h_box_output.addWidget(self.add_word_to_list)
                self.h_box_output.addStretch()
                self.check_first += 1
        except IndexError:
            msg = ["'{}' diye bir kelime yok ! ","There is no word here such as '{}'","Es gibt keinen Wort heißt '{}' !"]
            if self.current_lang == 'tr':
                msg_box = QMessageBox.warning(self, '!!!', msg[0].format(self.word.text()), QMessageBox.Ok)
            elif self.current_lang == 'en':
                msg_box = QMessageBox.warning(self, '!!!', msg[1].format(self.word.text()), QMessageBox.Ok)
            elif self.current_lang == 'de':
                msg_box = QMessageBox.warning(self, '!!!', msg[2].format(self.word.text()), QMessageBox.Ok)
    def event_add_to_list(self):
        text = self.word.text() + ',' + self.trans_output.text()
        #CHECKING IF EMPTY OR NOT!
        self.cursor.execute('SELECT * FROM userdata WHERE username = ? AND password = ?',(self.user_data[0],self.user_data[1]))
        user_words = self.cursor.fetchall()[0][2]
        if user_words == '':
            self.cursor.execute("UPDATE userdata SET user_practice_words = ? WHERE username = ? and password = ?",(text,self.user_data[0],self.user_data[1]))
            self.connection.commit()
        else:
            add_practice = user_words + ',' + text
            self.cursor.execute("UPDATE userdata SET user_practice_words = ? WHERE username = ? AND password = ?",(add_practice,self.user_data[0],self.user_data[1]))
            self.connection.commit()
    def event_see_practice_list(self):
        try:
            self.see_prac_list = practice_list(self.user_data,self.current_lang)
        except IndexError:
            msg = ["Listen boş ! ","Your List is Empty !","Deine Liste ist leer !"]
            if self.current_lang == 'tr':
                msg_box = QMessageBox.warning(self, '!!!', msg[0], QMessageBox.Ok)
            elif self.current_lang == 'en':
                msg_box = QMessageBox.warning(self, '!!!', msg[1], QMessageBox.Ok)
            elif self.current_lang == 'de':
                msg_box = QMessageBox.warning(self, '!!!', msg[2], QMessageBox.Ok)
            
    def event_go_practice(self):
        try:
            self.go_practice_words = word_list_practice(self.user_data,self.current_lang)
        except IndexError:
            msg = ["Listen boş ! ","Your List is Empty !","Deine Liste ist leer !"]
            if self.current_lang == 'tr':
                msg_box = QMessageBox.warning(self, '!!!', msg[0], QMessageBox.Ok)
            elif self.current_lang == 'en':
                msg_box = QMessageBox.warning(self, '!!!', msg[1], QMessageBox.Ok)
            elif self.current_lang == 'de':
                msg_box = QMessageBox.warning(self, '!!!', msg[2], QMessageBox.Ok)
    def logout_to_main_app(self):
        self.login_screen = app_dict_login(self.current_lang)
        self.close()
    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

                    
class practice_list(QWidget):
    
    def __init__(self,user_data,lang):
        super().__init__()
        self.current_lang = lang
        self.user_data = user_data
        self.connect_user()
        self.setupUi()
    def connect_user(self):
        self.connection = sqlite3.connect('userdata.db')
        self.cursor = self.connection.cursor()
        self.connection.commit()
    def setupUi(self):
        #WIDGETS
        self.cursor.execute('SELECT user_practice_words FROM userdata WHERE username = ? AND password = ?',(self.user_data[0],self.user_data[1]))
        data = self.cursor.fetchall()[0]
        user_practice_words = data[0].split(',')
        self.clear_list = QPushButton()
        #LAYOUTS
        self.v_box = QVBoxLayout()
        v_main_box = QVBoxLayout()
        v_main_box.addWidget(self.clear_list)
        v_main_box.addLayout(self.v_box)
        #getting as tuples
        i = 0
        words = list()
        while len(user_practice_words) > i:
            add = (user_practice_words[i],user_practice_words[i+1])
            words.append(add)
            i += 2
        number = 0
        for i,j in words:
            self.h_label_box = QHBoxLayout()
            self.h_label_box.setObjectName('delhbox|{}'.format(number))
            word_label = QLabel(i)
            word_label.setObjectName('dellabel|{}'.format(number))
            word_delete_btn = QPushButton('X')
            word_delete_btn.setObjectName('delbtn|{}'.format(number))
            word_delete_btn.clicked.connect(self.del_selected_item)
            self.h_label_box.addWidget(word_label)
            self.h_label_box.addStretch()
            self.h_label_box.addWidget(word_delete_btn)
            self.v_box.addLayout(self.h_label_box)
            number += 1
        v_main_box.addStretch()
        #creating list that we use in deleting items
        self.w = dict(enumerate(words))
        #EVENTS
        
        self.setLayout(v_main_box)
        self.clear_list.clicked.connect(self.event_clear_list)
        self.setGeometry(750,200,500,250)

        self.set_lang(self.current_lang)
        self.show()
    def set_lang(self,lang):
        def turkish():
            self.setWindowTitle('Listene Bak !')
            self.clear_list.setText('Listeyi temizle')
        def english():
            self.setWindowTitle('See your List !')
            self.clear_list.setText('Clear List')
        def deutsch():
            self.setWindowTitle('Sieh deine Liste !')
            self.clear_list.setText('Lösch deine Liste !')           
        if lang == 'tr':
            turkish()
        elif lang == 'en':
            english()
        elif lang == 'de':
            deutsch()
    def event_clear_list(self):
        self.clearLayout(self.v_box)
        self.cursor.execute("UPDATE userdata SET user_practice_words = '' WHERE username = ? AND password = ?",(self.user_data[0],self.user_data[1]))
        self.connection.commit()
    def del_selected_item(self):
        self.cursor.execute('SELECT user_practice_words FROM userdata WHERE username = ? AND password = ?',(self.user_data[0],self.user_data[1]))
        data = self.cursor.fetchall()[0]
        user_practice_words = data[0].split(',')
        i = 0
        words = list()
        
##        while len(user_practice_words) > i:
##            add = (user_practice_words[i],user_practice_words[i+1])
##            words.append(add)
##            i += 2
##        w = dict(enumerate(words))
        
        
        btn = self.sender().objectName()
        number = btn.split("|")[1]
        layout = self.findChild(QtCore.QObject, "delhbox|{}".format(number))
        word = layout.itemAt(0).widget().text()
        #pops from dict by index value
        self.w.pop(int(number),None)
        
        new_words1 = list()
        new_words2 = ''
        for i in self.w.items():
            new_words1.append(i[1])
        
        for i,j in new_words1:
            if new_words2 == '':
                new_words2 = str(i) + ',' + str(j) + ','
            else:
                new_words2 = new_words2 + i + ',' + j + ','

        new_words2 = new_words2.strip(',')
        self.cursor.execute('UPDATE userdata SET user_practice_words = ? WHERE username = ? AND password = ?',(new_words2,self.user_data[0],self.user_data[1]))
        self.connection.commit()
        #clears from layout = deletes h_label_box
        self.clearLayout(layout)
            
    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())
class word_list_practice(QWidget):
    
    def __init__(self,user_data,lang):
        super().__init__()
        self.current_lang = lang
        self.user_data = user_data
        self.connect_user()
        self.setupUi()
    def connect_user(self):
        self.connection = sqlite3.connect('userdata.db')
        self.cursor = self.connection.cursor()
        self.connection.commit()
    def setupUi(self):
        #WIDGETS
        self.cursor.execute('SELECT user_practice_words FROM userdata WHERE username = ? AND password = ?',(self.user_data[0],self.user_data[1]))
        data = self.cursor.fetchall()[0]
        user_practice_words = data[0].split(',')
        self.check_words = QPushButton()
        #LAYOUTS
        self.v_box = QVBoxLayout()
        v_main_box = QVBoxLayout()
        v_main_box.addLayout(self.v_box)
        #getting as tuples
        i = 0
        words = list()
        while len(user_practice_words) > i:
            add = (user_practice_words[i],user_practice_words[i+1])
            words.append(add)
            i += 2
        number = 0
        for i,j in words:
            self.h_label_box = QHBoxLayout()
            self.word_from_label = QLabel(i)
            self.word_to_input = QLineEdit()
            self.word_to_input.setObjectName('wordinput|{}'.format(number))
            self.h_label_box.addStretch()
            self.h_label_box.addWidget(self.word_from_label)
            self.h_label_box.addWidget(self.word_to_input)
            self.h_label_box.addStretch()
            
            self.v_box.addLayout(self.h_label_box)
            number += 1
        v_main_box.addStretch()
        v_main_box.addWidget(self.check_words)
        #EVENTS
        self.check_words.clicked.connect(self.event_check_words)
        self.setLayout(v_main_box)
        self.setGeometry(750,200,500,250)

        self.set_lang(self.current_lang)
        self.show()
    def set_lang(self,lang):
        def turkish():
            self.setWindowTitle('Çalış !')
            self.check_words.setText('Kontrol Et')
        def english():
            self.setWindowTitle('Practice !')
            self.check_words.setText('Check')
        def deutsch():
            self.setWindowTitle('Üben !')
            self.check_words.setText('Kontrollieren')            
        if lang == 'tr':
            turkish()
        elif lang == 'en':
            english()
        elif lang == 'de':
            deutsch()
    def event_check_words(self):
        self.cursor.execute('SELECT user_practice_words FROM userdata WHERE username = ? AND password = ?',(self.user_data[0],self.user_data[1]))
        data = self.cursor.fetchall()[0]
        user_practice_words = data[0].split(',')
        #getting as tuples
        i = 0
        word_ans = list()
        del_words = list()
        while len(user_practice_words) > i:
            add = (user_practice_words[i+1])
            del_words.append((user_practice_words[i],user_practice_words[i+1]))
            word_ans.append(add)
            i += 2
        #creates the dict that we use when deleting items ! important
        w = dict(enumerate(del_words))

        #reading answers and checking from QLineEdits
        number = 0
        try:
            while True:
                item = self.findChild(QtCore.QObject, "wordinput|{}".format(number))
                if (item.text() == word_ans[number]):
                    item.setStyleSheet('color: green;')
                    self.del_selected_item(item,w)
                else:
                    text = item.text() + '->' + word_ans[number]
                    item.setText(text)
                    item.setStyleSheet('color: red;')
                number += 1
        except (AttributeError or IndexError):
            pass

    def del_selected_item(self,item,w):
        self.cursor.execute('SELECT user_practice_words FROM userdata WHERE username = ? AND password = ?',(self.user_data[0],self.user_data[1]))
        data = self.cursor.fetchall()[0]
        user_practice_words = data[0].split(',')
        
##        i = 0
##        words = list()
##        while len(user_practice_words) > i:
##            add = (user_practice_words[i],user_practice_words[i+1])
##            words.append(add)
##            i += 2
##        w = dict(enumerate(words))
        
        btn = item.objectName()
        number = btn.split("|")[1]
        #pops from dict by index value
        w.pop(int(number),None)
        
        new_words1 = list()
        new_words2 = ''
        for i in w.items():
            new_words1.append(i[1])
        
        for i,j in new_words1:
            if new_words2 == '':
                new_words2 = str(i) + ',' + str(j) + ','
            else:
                new_words2 = new_words2 + i + ',' + j + ','

        new_words2 = new_words2.strip(',')
        self.cursor.execute('UPDATE userdata SET user_practice_words = ? WHERE username = ? AND password = ?',(new_words2,self.user_data[0],self.user_data[1]))
        self.connection.commit()
    
    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

        
app = QApplication(sys.argv)
app.setStyle(QStyleFactory.create("fusion"))
app_dict = app_dict_login()
sys.exit(app.exec_())
