from twentyfourcore import *
import sqlite3
import time
import random
import os.path

class db():
    def __init__(self,dbname="dbfile.db"):
        self.conn = sqlite3.connect(dbname)
        self.curs = self.conn.cursor()
        if len(open(dbname,"rb").read())==0:
            self.tblcmd = 'create table questions (qid char(4), qchar char(15), qnature bool(5), qanswer char(40), qtimecost float(4))'
            self.curs.execute(self.tblcmd)
        self.builddb()

    def element(self,i):
        return lambda x: x[i]

    def search(self,ref=5):
        self.curs.execute("select * from questions")

        fall= self.curs.fetchall()
        if ref==5:
            return fall
        else:
            return list(map(self.element(ref),fall))

    def show(self):
        for _ in self.search() :
            print(_)
        # print(self.search())

    def add(self,questions):
        self.curs.execute("select * from questions")
        names=[q[0] for q in self.search() ]
        for question in questions:
            if question[0] not in names:
                self.curs.execute('insert into questions values (?, ?, ?, ? ,?)', question)
        self.conn.commit()

    def update(self,questions):
        self.curs.execute("select * from questions")
        names=[q[0] for q in self.curs.fetchall()]
        for question in questions:
            if question[0] in names:
                self.curs.execute('update questions set qnature=?, qanswer=?, qtimecost=? where qid=?',[question[2],question[3],question[4],question[0]])
        self.conn.commit()

    def rowcount(self):
        print(self.conn.rowcount)

    def close(self):
        self.conn.close()

    def delete(self,qids):
        self.curs.execute('delete from questions where qid = ? ', qids)
        self.conn.commit()

    def clean(self):
        self.curs.execute('delete from questions')
        self.conn.commit()

    def hasanswer(self,s='true'):
        self.curs.execute("select * from questions where qnature = ? ", [s])
        return self.curs.fetchall()

    def answer(self,qid):
            self.curs.execute("select * from questions where qid = ? ", [qid])
            an=self.curs.fetchone()
            if an !=None:
                return an[3]
            else:
                return "这道题目没有答案"

    def answer2(self,qlst):
        qid=lst2str(qlst)
        if qid=="0000":
            return "Bingo!"
        self.curs.execute("select * from questions where qid = ? ", [qid])
        an=self.curs.fetchone()
        if an == None:
            return "参数超过范围"
        elif an[2]=='false':
            return "这道题目没有答案"
        else:
            return an[3]

    def builddb(self):
        if os.path.getsize("dbfile.db")< 10000:
            questions=prob(13)
            self.add(questions)

    def fetch(self,num1,num2):
        self.curs.execute("select * from questions where qtimecost >= ?", [num2])
        return self.curs.fetchall()

    def getQs(self,mode='easy',ref='whole'):
        self.curs.execute("select * from questions where qnature='true'")
        qs = self.curs.fetchall()
        if mode=='easy':
            bottom,top=(0,10)
        elif mode=='normal':
            bottom, top=(10,100)
        elif mode=='hard':
            bottom,top=(100,10000)
        else:
            bottom,top=(0,10000)

        qGen=filter(lambda x: bottom <=x[4]<top,qs)
        if ref=='qonly':
            newlst=[]
            lst=list(map(lambda x: x[1],list(qGen)))
            for _ in lst:
                _= list(map(int, eval(_)))
                newlst.append(_)
            newlst.sort()
            return newlst
        else:
            return list(qGen)


    def getQ(self,mode="easy"):
        Qs=self.getQs(mode)
        r=random.randint(0,len(Qs))
        return Qs[r][1]



def prob(rng=3):
    allref=set()
    questions=[]
    for i1 in range(rng):
        for i2 in range(rng):
            for i3 in range(rng):
                for i4 in range(rng):
                    lst=[i1,i2,i3,i4]
                    lst.sort()
                    allref.add(tuple(lst))
    for oneref in allref:
        tstart=time.time()
        q=[oneref[0]+1,oneref[1]+1,oneref[2]+1,oneref[3]+1]
        qid=lst2str(q)
        answer=f24(q)
        if answer != None:
            qnature="true"
        else:
            qnature="false"
        tgap="{0:.2f}".format((time.time()-tstart)*1000*100)
        question=[qid,str(q),qnature,answer,tgap]
        questions.append(question)
    return questions


def lst2str(lst4):
    if type(lst4)==type([]):
        lst4.sort()
        return "".join(list(map(num2str,lst4)))
    elif type(lst4)==type(""):
        newlst4=eval(lst4)
        return lst2str(newlst4)


def num2str(num):
    if int(num)<10:
        return str(num)
    elif int(num)<33:
        return chr(num-10+65)
    else:
        return "Z"

def str2num(str1):
    if len(str1)==1:
        if "A"<=str1<="Y": return ord(str1)-65+10
        return int(str1)

def str2lst(str4):
    return list(map(str2num,str4))

def ask():
    print("题目(n)/退出(q)/游戏难度(m)/寻找答案(x)?")

def game():
    print("等待初始化游戏数据库...")
    a=db()
    a.builddb()
    print("游戏数据库初始化成功...")
    mode="easy"
    cq=[]
    ask()
    while True:
        cmd=input(">").lower()
        try:
            if eval(cmd)==24:
                print("答对了！")
                ask()
            elif eval(cmd)!=24:
                print("答错了！再试一次(g)/答案(a)")
                erinput=input(">")
                if erinput=="g":
                    print(cq)
                elif erinput=="a":
                    print(a.answer2(cq))
                    ask()
                else:
                    print("输入错误.")
        except:
            if cmd=="quit" or cmd=="q":
                print("退出游戏")
                exit()
            elif cmd=="new" or cmd=="n":
                cq=a.getQ(mode)
                print(cq)
            elif cmd=="setmode" or cmd=="m":
                print("设置游戏难度: 简单(e),正常(e),复杂(h)")
                b=input().lower()
                if b=="easy" or b=="e":
                    mode="easy"
                elif b=="normal" or b=="n":
                    mode="normal"
                elif b=="hard" or b=="h":
                    mode="hard"
                print("游戏难度设置成功!")
                ask()
            elif cmd=="x":
                print("输入题目，用空格分隔数字，例如 3 3 8 8")
                try:
                    b=input(">").lower()
                    if " " in b:
                        spliter=" "
                    elif "," in b:
                        spliter=","
                    cq=list(map(int,b.split(spliter)))
                    print(f"{cq}的一个答案是：{a.answer2(cq)}")
                    ask()
                except:
                    print("输入错误。")
                    ask()
            else:
                print("输入错误。")
                ask()

if __name__ == '__main__':
    a=db()
    b=a.getQs("all","qonly")
    print(b)








    






