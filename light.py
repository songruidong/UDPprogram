import socket
import time,threading
import random
import turtle
class Light(object):
    temperature=None#温度
    humidity=None#湿度
    illumination=None#环境照度显示
    workstate=False
    workaddress=None
    name=None
    mysocket=None
    def __init__(self,name,workaddress):
        self.name=name
        self.workaddress=workaddress
        self.flag=False
        self.mysocket= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.mysocket.connect(('127.0.0.1', 8888))

    def flush(self):
        print("begin")
        n=0
        while(True):
            self.temperature=random.randint(0,50)
            self.humidity=random.randint(0,20)
            self.illumination=random.randint(100,200)
            n+=1
            print(n)
            self.mysocket.sendto((self.temperature, self.humidity, self.illumination).__str__().encode('utf-8'),('127.0.0.1', 8888))
            time.sleep(5)
        pass
    def openorclose(self):
        while True:
            # d=self.mysocket.recv(1024)
            d, addr = self.mysocket.recvfrom(1024)
            print('Received from %s:%s.' % addr)
            if d:
                choice=d.decode('utf-8') 
                if (choice=="我准备控制你了"):
                    self.mysocket.sendto("同意".encode('utf-8'),addr)
                    print("同意")
                    time.sleep(1)
                if(choice=="关灯"):
                    self.mysocket.sendto("收到".encode('utf-8'),addr)
                    self.workstate=False
                    self.flag=True
                    print("收到")
                    time.sleep(1)
                if(choice=="开灯"):
                    self.mysocket.sendto("收到".encode('utf-8'),addr)
                    self.workstate=True
                    self.flag = True
                    print("收到")
                    time.sleep(1)
    def view(self):
        turtle.setup(400,400,200,200)
        turtle.hideturtle()
        turtle.speed(0)
        turtle.color(self.name, self.name)
        while(True):
            # print(self.workstate,self.flag)
            if(self.flag==True):
                self.flag=False
                turtle.clear()
            if (self.workstate == True):
                turtle.pensize(1)
                turtle.begin_fill()
                turtle.circle(50)
                turtle.end_fill()
            else:
                turtle.pensize(1)
                turtle.circle(50)

            # turtle.done()
            # turtle.begin_fill()
            # turtle.circle(39)
            # turtle.circle(39)
            # turtle.end_fill()
            # time.sleep(5)

    def run(self):    
        t1=threading.Thread(target=self.flush,name=self.name+"flush")
        t1.start()
        t2=threading.Thread(target=self.openorclose,name=self.name+"openorclose")
        t2.start()
        t3 = threading.Thread(target=self.view, name=self.name + "view")
        t3.start()
        time.sleep(20)
if __name__ == "__main__":
    a=Light("red","testt")
    g = Light("green", "testt")
    g.run()
    a.run()