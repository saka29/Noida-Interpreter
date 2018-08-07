'''Noida Interpreter
By Saka.
Bad, messy, and terrible because I'm not that good
at Python. But it has a debug option!

Because Python does not have multiline inputs, run from command line
and put the name of the file to be run for example:

interpreter.py hello.txt

See https://esolangs.org/wiki/Noida'''
import sys
file = open(sys.argv[1])
code = file.read()
code = code.splitlines()
varlist = {}
done = False
debug = False

def doMath(ins):
    a = getVal(ins.split()[1])
    o = ins.split()[2]
    b = getVal(ins.split()[3])
    if o=='+':
        return a+b
    elif o=='-':
        return a-b
    elif o=='*':
        return a*b
    elif o=='/':
        return a/b
    else:
        return 'err:Unknown Operation'

def joinStr(ins):
    strs = map(getVal,ins.split()[1:])
    return ''.join(strs)

def getVal(val):
    if val[0]=='.':
        return int(val[1:])
    elif val[0]=='[' and val[-1]==']':
        return val[1:-1].replace('\:',':')
    elif val[0]=='$':
        return varlist[val[1:]]
    elif val.split()[0]=='math':
        return doMath(val)
    elif val.split()[0]=='join':
        return joinStr(val)
    else:
        return 'err:Unknown DataType'

def cond(ins):
    ins = ins.split()
    if ins[0]=='same':
        return getVal(ins[1])==getVal(ins[2])
    elif ins[0]=='greater':
        return getVal(ins[1])>getVal(ins[2])
    else:
        return 'err:Unknown Condition'
                                            
point = 0
while done == False:
    l = code[point].lstrip().split(' : ')
    ins = l[0]
    if debug:
        print('Instruction: ',code[point])
        print('Line: ',str(point))
        print(varlist)
    if ins == 'new':
        varlist[l[1]] = 0
        point += 1
    elif ins == 'set':
        varlist[l[1][1:]] = getVal(l[2])
        point += 1
    elif ins == 'print':
        print(getVal(l[1]))
        point += 1
    elif ins == 'input':
        i = input('>>')
        if l[1]=='int':
            i = int(i)
        varlist[l[2][1:]]=i
        point += 1
    elif ins == 'if':
        if cond(l[1]):
            point += 2
        else:
            cBrack = 0
            oBrack = 0
            point += 1
            oBrack += 1
            while cBrack != oBrack:
                point += 1
                if code[point].lstrip() == '{':
                    oBrack += 1
                elif code[point].lstrip() == '}':
                    cBrack += 1
    elif ins == 'repeat':
        cBrack = 1
        oBrack = 0
        while cBrack != oBrack:
            point -= 1
            if code[point].lstrip() == '{':
                oBrack += 1
            elif code[point].lstrip() == '}':
                cBrack += 1
    elif ins == '{':
        point += 1
    elif ins == '}':
        point += 1
    elif ins[0] == '#':
        point += 1
    elif ins == 'done':
        done = True
    if point > len(code)-1:
        done = True
