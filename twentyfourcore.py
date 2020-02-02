
from itertools import permutations
import time
import random
import shelve
import os.path

def f(fp1,op,fp2):
    if op==0: return fp1+fp2
    if op==1: return fp1-fp2
    if op==2: return fp2-fp1
    if op==3: return fp1*fp2
    if op==4 and fp2!=0:
        return fp1/fp2
    if op==5 and fp1!=0:
        return fp2/fp1
    return 10000

def showf(fp1,op,fp2):
    if op == 0: return "(" + str(fp1) + "+" + str(fp2) + ")"
    if op == 1: return "(" + str(fp1) + "-" + str(fp2) + ")"
    if op == 2: return "(" + str(fp2) + "-" + str(fp1) + ")"
    if op == 3: return "(" + str(fp1) + "*" + str(fp2) + ")"
    if op == 4: return "(" + str(fp1) + "/" + str(fp2) + ")"
    if op == 5: return "(" + str(fp2) + "/" + str(fp1) + ")"


def fx1(fp1,op1,fp2,op2,fp3,op3,fp4):
    return f(f(f(fp1,op1,fp2),op2,fp3),op3,fp4)
def fx2(fp1,op1,fp2,op2,fp3,op3,fp4):
    return f(f(fp1,op1,fp2),op2,f(fp3,op3,fp4))


def showfx1(fp1,op1,fp2,op2,fp3,op3,fp4):
    return showf(showf(showf(fp1,op1,fp2),op2,fp3),op3,fp4)
def showfx2(fp1,op1,fp2,op2,fp3,op3,fp4):
    return showf(showf(fp1,op1,fp2),op2,showf(fp3,op3,fp4))

def fchoosed(fps):
    (fp1, fp2, fp3, fp4)=fps
    for op1 in range(6):
        for op2 in range(6):
            for op3 in range(6):
                r1 = f(fp1, op1, fp2)
                r2 = f(r1, op2, fp3)
                r3 = f(r2, op3, fp4)
                r4= f(fp3,op3,fp4)
                r5 = f(r1,op2,r4)
                if eql(r3):
                    return showfx1(fp1,op1,fp2,op2,fp3,op3,fp4) + "=24"
                    break
                elif eql(r5):
                    return showfx2(fp1, op1, fp2, op2, fp3, op3, fp4) + "=24"
                    break

def eql(x):
    if abs(x-24)<0.0001:
        return True
    return False

def choose(lst):
    perms=permutations(range(len(lst)))
    b=set()
    for perm in perms:
        a = []
        for i in range(len(lst)):
            a.append(lst[perm[i]])
        b.add(tuple(a))
    return b


def f24(dataInput:list):
    dct=choose(dataInput)
    results= (fchoosed(one) for one in dct)
    for result in results:
        if result != None:
            return result
            break

def prob(rng=13):
    allref=set()
    okref=set()
    notref=set()
    for i1 in range(rng):
        for i2 in range(rng):
            for i3 in range(rng):
                for i4 in range(rng):
                    lst=[i1,i2,i3,i4]
                    lst.sort()
                    allref.add(tuple(lst))
    for oneref in allref:
        tstart=time.time()
        question=[oneref[0]+1,oneref[1]+1,oneref[2]+1,oneref[3]+1]
        answer=f24(question)
        tgap=(time.time()-tstart)*1000*100

        if answer != None:
            notref.add(tuple(question.append(tgap)))
        else:
            okref.add(tuple(question.append(tgap)))

    return (allref, okref, notref)

def loadin(k,v):
    dbase = shelve.open("mydb")
    dbase[k]=v
    dbase.close

def loadout(k):
    dbase = shelve.open("mydb")
    if k in dbase.keys():
        return dbase[k]
    else:
        return False

def saveFavor(v):
    if loadout("favor")==False:
        st=set()
        st.add(v)
        loadin("favor",st)
    else:
        st=loadout("favor")
        st.add(v)
        loadin("favor",st)

def delFavor(v):
    if loadout("favor"):
        st=loadout("favor")
        st.discard(v)
        loadin("favor",st)

def showFavor():
    if loadout("favor"):
        return "\n".join(list(map(lambda x: str(x),list(loadout("favor")))))
    else:
        return "收藏夹是空的。"
def myFavor():
    if loadout("favor"):
        return list(map(list,loadout("favor")))
    else:
        return []

def cleanDB(mode=1):
    dbase = shelve.open("mydb")
    for key in dbase:
        if mode==1:
            if key != "12" and ("q" in key)==False:
                del(dbase[key])
        elif mode==2:
            if key !="12":
                del(dbase[key])
        elif mode==3:
            del(dbase[key])


def getQuestion(rng:int):
    dbase = shelve.open("mydb")
    # print(len(dbase))
    questions=dbase[str(rng)]
    return(random.choice(list(questions[1])))

# runToFile()

def getQ(point1:int,point2:int):
    while True:
        question=getQuestion(12)
        tstart = time.time()
        f24(question)
        tcost=(time.time()-tstart)*1000*10
        # print(question,tcost)
        if point1<=tcost<point2:
            return question
            break
if __name__ == '__main__':
    x=(4, 6, 8, 13)
    delFavor(x)
    pass








