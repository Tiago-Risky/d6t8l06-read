from threading import Thread
from random import randint
import tkinter
import time
import serial

vals = [0] * 8
valPTAT = 0
debug = True

class SerialThread(Thread):
 
    def __init__(self, val):
        Thread.__init__(self)
        self.val = val
        
    def run(self):
        while True:
            print("Attempting to connect")
            try:
                conn = serial.Serial('/dev/ttyUSB0', 9600)
                break
            except serial.SerialException as e:
                print("Falha a ligar: {}".format(e))
                time.sleep(3)
        time.sleep(2)

        print("Listening")

        while True:
            ler = conn.readline().decode()
            ler = ler.strip()
            temp = ler.split(",")
            for i in range(8):
                vals[i] = temp[i]
            valPTAT = temp[8]

            if debug:
                print("Values: {}".format(vals))
                print("PTAT Value: {}".format(valPTAT))



class WindowThread(Thread):
 
    def __init__(self, val):
        Thread.__init__(self)
        self.val = val
        
    def run(self):
        window = tkinter.Tk()
        window.title("D6T-8L-06 value reading")
        window.geometry("490x120")
        Canv = tkinter.Canvas(window, bg="white",height=300, width=1000)
        squareSize = 50
        marginSize = 10
        coord = [0] * 8
        for x in range(8):
            y = x+1
            subCoord = [0] * 4
            subCoord[0] = y*marginSize + x*squareSize
            subCoord[1] = marginSize
            subCoord[2] = y*marginSize + y*squareSize
            subCoord[3] = marginSize+squareSize
            coord[x] = subCoord

        #Previous manually written approach using 10 margin and 50 squaresize...    
        #coord = [[10, 10, 60, 60], [70, 10, 120, 60], [130, 10, 180, 60],[190, 10, 240, 60],
         #       [250, 10, 300, 60], [310, 10, 360, 60], [370, 10, 420, 60], [430, 10, 480, 60]]

        for a in range(8):
            c = coord[a]
            tagRect = "rect"+str(a)
            tagText = "text"+str(a)
            Canv.create_rectangle(c, fill="blue", tags=tagRect)
            Canv.create_text((c[0]+(squareSize/2),marginSize+(squareSize/2)), text=vals[a], tags=tagText)

        def ticktock():
            for x in range(8):
                tagRect = "rect"+str(x)
                tagText = "text"+str(x)
                rectItem = Canv.find_withtag(tagRect)
                txtItem = Canv.find_withtag(tagText)
                if rectItem:
                    rect_id = rectItem[0]
                    Canv.itemconfigure(rect_id, fill="red")
                if txtItem:
                    txt_id = txtItem[0]
                    Canv.itemconfigure(txt_id, text=vals[x])


            window.after(1000, ticktock)

        ticktock()

        Canv.pack()
        window.mainloop()


if __name__ == '__main__':
    thread1 = SerialThread(1)
    thread1.setName('Thread 1')
 
    thread2 = WindowThread(2)
    thread2.setName('Thread 2')
    thread1.start()
    thread2.start()
 
    thread1.join()
    thread2.join()
 
    print('Main Terminating...')