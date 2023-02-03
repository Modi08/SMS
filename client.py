import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
import sys

import socket
import threading

kivy.require('1.9.1')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class MyRoot(BoxLayout):

    ip_text = ObjectProperty(None)
    nickname_text = ObjectProperty(None)
    connect_btn = ObjectProperty(None)
    chat_text = ObjectProperty(None)
    message_text = ObjectProperty(None)
    send_btn = ObjectProperty(None)
    connection_grid = ObjectProperty(None)

    



    def __init__(self):
        super(MyRoot, self).__init__()
    
    def send_msg(self):
        print(self.nickname_text.text)
        client.send(f"{self.nickname_text.text}: {self.message_text.text}".encode('utf8'))
        

    def make_invisible(self, widget):
            widget.visible = False
            widget.size_hint_x = None
            widget.size_hint_y = None
            widget.height = 0
            widget.width = 0
            widget.text = ''
            widget.opacity = 0
    
    def connect_to_server(self):
        if self.nickname_text != "":
            client.connect((self.ip_text.text, 9999))
            message = client.recv(1024).decode('utf8')
            if message == "NICK":
                client.send(self.nickname_text.text.encode('utf8'))
                self.send_btn.disabled = False
                self.message_text.disabled = False
                self.connect_btn.disabled = True
                self.ip_text.disabled = True

                self.make_invisible(self.connection_grid)
                self.make_invisible(self.connect_btn)

                thread = threading.Thread(target=self.receive)
                thread.start()

    def receive(self):
        string = ''
        stop = False
        while not stop:
            try:
                print('hi')
                message = client.recv(1024).decode('utf8')
                string += message + '\n'
                print("hi")
                self.chat_text.text = string
                print("Hi3: ", self.chat_text.text)
            except:
                print("error")
                sys.exit(2)
    



class EkanshChat(App):

    def build(self):
        return MyRoot()

ekanshChat = EkanshChat()
ekanshChat.run()