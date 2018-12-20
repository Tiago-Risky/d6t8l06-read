from threading import Thread
import tkinter
import time
import serial

## Change this to your USB serial port
serialPort = 'COM3'

vals = [0] * 8
valPTAT = 0
debug = True
kill = False

class SerialThread(Thread):
    def run(self):
        conn = None
        
        global kill
        while not kill:
            print("Attempting to connect")
            try:
                global serialPort
                conn = serial.Serial(serialPort, 9600)
                break
            except serial.SerialException as e:
                print("Fail to connect: {}".format(e))
                time.sleep(3)
        time.sleep(2)
        print("Listening")

        while not kill and conn!=None:
            global valPTAT
            ler = conn.readline().decode()
            ler = ler.strip()
            temp = ler.split(",")
            for i in range(8):
                vals[i] = temp[i]

            valPTAT = temp[8]

            if debug:
                print("Values: {}".format(vals))
                print("PTAT Value: {}".format(valPTAT))
        
        if conn != None:
            conn.close()
            print("Connection closed")



class WindowThread(Thread):
    def run(self):
        global kill
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

        for x in range(8):
            c = coord[x]
            tagRect = "rect"+str(x)
            tagText = "text"+str(x)
            Canv.create_rectangle(c, fill="blue", tags=tagRect)
            Canv.create_text((c[0]+(squareSize/2),marginSize+(squareSize/2)), text=vals[x], tags=tagText)

        Canv.create_text((marginSize+(squareSize/2),(marginSize*3)+squareSize), text=valPTAT, tags="textPTAT")

        def ticktock():
            if not kill:
                for x in range(8):
                    tagRect = "rect"+str(x)
                    tagText = "text"+str(x)
                    rectItem = Canv.find_withtag(tagRect)
                    txtItem = Canv.find_withtag(tagText)
                    if rectItem:
                        rect_id = rectItem[0]
                        valInt = int(vals[x])
                        if 10 > valInt:
                            Canv.itemconfigure(rect_id, fill="light cyan")
                        elif 20 > valInt >= 10:
                            Canv.itemconfigure(rect_id, fill="gold")
                        elif 25 > valInt >= 20:
                            Canv.itemconfigure(rect_id, fill="orange")
                        elif 30 > valInt >= 25:
                            Canv.itemconfigure(rect_id, fill="dark orange")
                        else:
                            Canv.itemconfigure(rect_id, fill="red")
                    
                    if txtItem:
                        txt_id = txtItem[0]
                        Canv.itemconfigure(txt_id, text=vals[x])
                txtItem = Canv.find_withtag("textPTAT")
                if txtItem:
                    txt_id = txtItem[0]
                    Canv.itemconfigure(txt_id, text=valPTAT)

                window.after(1000, ticktock)
            else:
                window.destroy()
                window.quit()
                print("Window Closed")

        def closeWindow():
            global kill
            kill = True
            
        ticktock()

        Canv.pack()
        window.protocol("WM_DELETE_WINDOW", closeWindow)
        window.mainloop()


if __name__ == '__main__':
    thread1 = SerialThread()
    thread1.setName('Thread 1')
 
    thread2 = WindowThread()
    thread2.setName('Thread 2')

    thread1.start()
    thread2.start()

    #Locking mainthread while thread1 and 2 are still alive
    #This means the program won't terminate until a thread
    #crashes/closes or until we catch the KeyboardInterrupt
    #that will signal both threads to kill themselves correctly
    try:
        while(thread1.is_alive and thread2.is_alive and not kill):
            time.sleep(1)
    except KeyboardInterrupt:
            kill = True
            print("Stopping every task")
