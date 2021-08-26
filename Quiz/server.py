import socket
import sys
import time
import select
import random
FORMAT = "utf-8"
DISCONNET_MSG = "!DISCONNECT"
HEADER = 1024
PORT = 5555
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
no =3
clients = []

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
score=[0,0,0]
server.bind((ADDR))
server.listen(3)
def broadcast(message):
   for client in clients:
      try:
         client.send(message.encode(FORMAT))
      except:
         close(client)

def receive(conn):
   msg = conn.recv(HEADER).decode(FORMAT)
   return msg

def close(conn):
   conn.close()
   clients.remove(conn)

def shutdown(client_list):
   for client in client_list:
      client.shutdown(1) 

def answers(con1,con2,con3,ques,num):
   player=con1
   con1.send(str.encode("You may answer the question now"))
   con2.send(str.encode("Player 2 has pressed the buzzer.."))
   con3.send(str.encode("Player 2 has pressed the buzzer.."))
   time.sleep(10)
   answer = receive(player)
   print(answer)
   if (Q[ques] == answer):
      score[num] += 1
      player.send(str.encode("You gave the right answer"))
   else:
      score[num] -= 0.5
      player.send(str.encode("You gave the wrong answer"))
   sendallScore(clients)
   time.sleep(3)


print(f"Server bound to: {SERVER} : {PORT}")
i=0
for x in range(no):
   i+=1
   conn,addr = server.accept()
   print(f"Connected to Player 1 at [{addr}]")
   conn.send(("You are Player" +str(i)+" \nWaiting for other players").encode(FORMAT))
   clients.append(conn)

conn1 = clients[0]
conn2 = clients[1]
conn3 = clients[2]
time.sleep(0.1)
broadcast("The game will begin soon...")
time.sleep(8)

Q={}
for i in range(50):
    Q["2+"+str(i)+"=??"]=str(2+i)


def sendallScore(connlist):
    global score
    for i, conn in enumerate(connlist):
        time.sleep(0.1)
        conn.send(str.encode("\nPlayer "+str(i+1)+", your score is: "+str(score[i])+"\n"))
        time.sleep(0.1)

def sendallscores(connlist):
    global score
    for i in range(3):
        connlist[i].send(str.encode("\t|\tPLAYER-1     -->       "+ str(score[0]) + "\t|\n\t|\tPLAYER-2     -->       "+ str(score[1])+"\t|\n\t|\tPLAYER-3     -->       "+ str(score[2])+"\t|"))


for ques in Q.keys():
   if(score[0]<5 and score[1]<5 and score[2]<5):
      try:
         broadcast(ques)
         time.sleep(1)
         print("Sending:", ques)
         read_sockets, _, _ = select.select(clients, [], [],10)
         time.sleep(10)
         read_sockets_all, _, _ = select.select(clients, [], [],3)
         print(read_sockets)
         print(read_sockets_all)
         for conn in read_sockets_all:
            conn.recv(1024)

         if(read_sockets==[]):
            print(f"No one pressed the buzzer!!!!\nNext question....")
            broadcast("No one pressed the buzzer!!!!\nNext question....")
            time.sleep(2)
            sendallScore(clients)
            time.sleep(3)

         elif(read_sockets[-1]==clients[0]):
            answers(conn1,conn2,conn3,ques,0)

         elif(read_sockets[-1]==clients[1]):
            answers(conn2,conn1,conn3,ques,1)
            player=conn2

         elif(read_sockets[-1]==clients[2]):
            answers(conn3,conn1,conn2,ques,2)

      except socket.error as e:
         print(e)
         break
   else:
      broadcast("The game has ended.")
      time.sleep(0.1)
      sendallscores(clients)
      time.sleep(1)
      if(score[0] == max(score)):
         winner="Player1"
      elif(score[1] == max(score)):
         winner="Player2"
      else:
         winner="Player3"
      time.sleep(0.1)
      broadcast("\n"+ winner + " wins")
      shutdown(clients)
      server.close()
      quit()

broadcast("The game has ended.")
time.sleep(0.1)
sendallscores(clients)
time.sleep(1)
if(score[0] == max(score)):
    winner="Player1"
elif(score[1] == max(score)):
   winner="Player2"
else:
   winner="Player3"
broadcast("Out of questions\n"+ winner + " wins")
time.sleep(0.1)
shutdown(clients)
server.close()
quit()