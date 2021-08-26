import socket
import sys
import time
import select
import termios
import os
FORMAT = "utf-8"
DISCONNET_MSG = "!DISCONNECT"
HEADER = 2048
PORT = 5555
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def close():
   send(DISCONNET_MSG)
   client.close()


def send(msg):
   message = msg.encode(FORMAT)
   client.send(message)

def receive():
   msg = client.recv(HEADER).decode(FORMAT)
   if msg == DISCONNET_MSG:
      close()
      sys.exit()
   else:
      return msg

print(receive())
time.sleep(1)
print(receive())
time.sleep(5)
flag=True
count=0

while flag:
   try:
      time.sleep(3)
      os.system('clear')
      question = receive()

      if(question!="The game has ended."):
         count+=1
         print("--------------------------QUIZ SHOW-------------------------\n")
         print("QUESTION-"+str(count),"---->",question)
         buzzer=""
         print("Enter anything to press the buzzer.\nYou have 10 seconds...")
         i, o, e = select.select([sys.stdin], [], [], 10)
         if (i):
            buzzer = sys.stdin.readline().strip()
         else:
            print("\nTimeOut!")
         send(buzzer)
         termios.tcflush(sys.stdin, termios.TCIFLUSH)
         reply = receive()

         if(reply == "You may answer the question now"):
            print(reply,"\nYou have 10 seconds to answer..")
            i, o, e = select.select([sys.stdin], [], [], 10)
            answer=" "
            if(i):
               answer=sys.stdin.readline().strip()
               print("Your entered:",answer)
            else:
               print("TimeOut!\nSorry you said nothing")
            send(answer)
            print(receive())
            termios.tcflush(sys.stdin, termios.TCIFLUSH)

         elif(reply == "No one pressed the buzzer!!!!\nNext question...."):
            print(reply)
            time.sleep(2)
            termios.tcflush(sys.stdin, termios.TCIFLUSH)
         
         else:
            print(reply)
            time.sleep(10)
            termios.tcflush(sys.stdin, termios.TCIFLUSH)
         
         print(receive())

      else:
         flag=False
         print("                            SCORECARD                              \v")
         print("\t-----------------------------------------")
         print(client.recv(4096).decode())
         print("\t-----------------------------------------")
         print(receive())
   
   except:
      print("\n Some error occured")
      client.close()
      quit()