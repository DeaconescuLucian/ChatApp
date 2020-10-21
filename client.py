import socket
import threading
from tkinter import simpledialog


from tkinter import *
from network import Network

class ScrollableFrame(Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = Canvas(self,width=850, height=600)
        scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


class Chat:
    master = Tk()
    n = Network()
    listen = True
    name='Unknown'
    def __init__(self):
        self.row=0
        self.master.bind("<Return>", self.trimite)
        thread=threading.Thread(target=self.primeste)
        thread.start()
        self.group = LabelFrame(self.master, padx=5, pady=5,width=300,background='blue')
        self.group.grid(padx=10, pady=10)
        self.label = Label(self.group, text="You:",background='blue',fg='white')
        self.frame = ScrollableFrame(self.group, padx=10, pady=10,background='pink')
        self.frame.grid(sticky=N, columnspan=2)
        self.frame.grid_propagate(False)
        self.label.grid(sticky=S + W)
        self.w = Entry(self.group,width=143)
        self.w.grid(row=1, column=1)
        label1 = Label(self.frame.scrollable_frame,
                      text="                                                                                                                       ")
        label1.grid(row=self.row,column=0, sticky=W)
        row = 1
        s = simpledialog.askstring("Log in", "Enter your name")
        if s:
            self.name=s
        self.n.connect(self.name)
        mainloop()


    def trimite(self,event):
        message=self.w.get().split()
        self.n.send(self.w.get())
        message_length = len(message)
        label=Label(self.frame.scrollable_frame, text="You:")
        label.grid(row=self.row,column=0, sticky=W)
        self.row+=1
        current_length=0
        msg=''
        for i in range(message_length):
            if current_length+len(message[i])<=30:
                msg=msg+message[i]+' '
                current_length=current_length+len(message[i])+1
            if len(message[i])>30:
                msg=message[i][0:30]+' '
                label = Label(self.frame.scrollable_frame, text=msg)
                label.grid(row=self.row,column=0, sticky=W)
                msg=message[i][30:]+' '
                self.row += 1
                current_length = len(msg)
                i-=1
            elif current_length+len(message[i])>30:
                label = Label(self.frame.scrollable_frame, text=msg)
                label.grid(row=self.row,column=0, sticky=W)
                self.row += 1
                current_length=0
                msg=''
                i-=1
            if i==message_length-1 and current_length+len(message[i])<=30:
                label = Label(self.frame.scrollable_frame, text=msg)
                label.grid(row=self.row,column=0, sticky=W)
                self.row += 1
                msg=''
        if msg!='':
            for i in range((len(msg)//30)+1):
                m=msg[i*30:(i+1)*30]
                label = Label(self.frame.scrollable_frame, text=m)
                label.grid(row=self.row,column=0, sticky=W)
                self.row+=1
        self.w.delete(0,len(self.w.get()))



    def primeste(self):
        while self.listen:
            try:
                data = self.n.get()
            except:
                pass
            if data:
                self.listen = False
        if data:
            message = data.split()
            message_length = len(message)
            current_length = 0
            msg = ''
            for i in range(message_length):
                if current_length + len(message[i]) <= 30:
                    msg = msg + message[i] + ' '
                    current_length = current_length + len(message[i]) + 1
                if len(message[i]) > 30:
                    msg = message[i][0:30] + ' '
                    label = Label(self.frame.scrollable_frame, text=msg)
                    label.grid(row=self.row, column=1, padx=105, sticky=W)
                    msg = message[i][30:] + ' '
                    self.row += 1
                    current_length = len(msg)
                    i -= 1
                elif current_length + len(message[i]) > 30:
                    label = Label(self.frame.scrollable_frame, text=msg)
                    label.grid(row=self.row, column=1, padx=105, sticky=W)
                    self.row += 1
                    current_length = 0
                    msg = ''
                    i -= 1
                if i == message_length - 1 and current_length + len(message[i]) <= 30:
                    label = Label(self.frame.scrollable_frame, text=msg)
                    label.grid(row=self.row, column=1, padx=105, sticky=W)
                    self.row += 1
                    msg = ''
            if msg != '':
                for i in range((len(msg) // 30) + 1):
                    m = msg[i * 30:(i + 1) * 30]
                    label = Label(self.frame.scrollable_frame, text=m)
                    label.grid(row=self.row, column=1, padx=105, sticky=W)
                    self.row += 1
            self.listen = True
            self.primeste()




chat = Chat()
