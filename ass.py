import sys

OPTAB={'ADD':'18', 'ADDF':'58', 'ADDR':'90', 'AND':'40', 'CLEAR':'B4', 'COMP':'28',
         'COMPF':'88', 'COMPR':'A0', 'DIV':'24', 'DIVF':'64', 'DIVR':'9C', 'FIX':'C4',
         'FLOAT':'C0', 'HIO':'F4', 'J':'3C', 'JEQ':'30', 'JGT':'34', 'JLT':'38', 'JSUB':'48',
         'LDA':'00', 'LDB':'68', 'LDCH':'50', 'LDF':'70', 'LDL':'08', 'LDS':'6C', 'LDT':'74',
         'LDX':'04', 'LPS':'E0', 'UML':'20', 'MULF':'60', 'MULR':'98', 'NORM':'C8',
         'OR':'44', 'RD':'D8', 'RMO':'AC', 'RSUB':'4C', 'SHIFTL':'A4', 'SHIFTR':'A8',
         'SIO':'F0', 'SSK':'EC', 'STA':'0C', 'STB':'78', 'STCH':'54', 'STF':'80', 'STI':'D4',
         'STL':'14', 'STS':'7C', 'STSW':'E8', 'STT':'84', 'STX':'10', 'SUB':'1C', 'SUBF':'5C',
         'SUBR':'94', 'SVC':'B0', 'TD':'E0', 'TIO':'F8', 'TIX':'2C', 'TIXR':'B8', 'WD':'DC'}
directive_command = ['BYTE', 'WORD', 'RESB', 'RESW']
SYMTAB = {'':0}
ERROR = []
def devide(line):
    line=str(line)
    labels=[]
    for i in range(3):
        label = line[:line.find('\t')]
        labels.append(label)
        if line.find('\t') == -1:
            line = ""
        else:
            line=line[line.find('\t')+1:]
    return labels
def dir_cmd(line):
    if line[2] == directive_command[0]: 
        if line[3].startswith('X'):
            return 1
        else:
            raw_B = line[3]
            raw_B = raw_B[raw_B.find("'")+1:]
            return len(raw_B[:raw_B.find("'")]);
    elif line[2] == directive_command[1]:
        return 3
    elif line[2] == directive_command[2]:
        return int(line[3])
    elif line[2] == directive_command[3]:
        return int(line[3])*3
argvs = sys.argv
if len(argvs) == 1:
    file_name = input('Please enter filename.')
    asm = open(file_name)
else:
    try:
        asm = open(argvs[1],'r')
    except:
        exit()
#分割成3欄
lines = []
for line in asm:
    labels = devide(line)
    lines.append(labels)
#設定LOCCTR
if  lines[0][1] == 'START':
    LOCCTR = int(lines[0][2],16)
    START = LOCCTR
else:
    LOCCTR = 0
name = lines[0][0]
lines[0].insert(0,hex(LOCCTR)[2:])

for i in range(1,len(lines)-1):
    #填入位置
    lines[i].insert(0,hex(LOCCTR)[2:].upper())
    #將標記符號置入符號表
    if lines[i][1] != "":
       if lines[i][1] in SYMTAB:
           ERROR.append("Duplicate symbol on line "+i)
       else:
           SYMTAB[lines[i][1]] = LOCCTR
    #計算下個位置
    if lines[i][2] in directive_command:
        LOCCTR += dir_cmd(lines[i])
    else:
        LOCCTR += 3
if lines[len(lines)-1][1] == "END":
    lines[len(lines)-1].insert(0,"")
#建立目的碼
for i in range(0,len(lines)):
    OBJCODE = "" 
    if lines[i][2] in OPTAB:
        if ',X' in lines[i][3]:
            position = SYMTAB[lines[i][3][:lines[i][3].find(',X')]] + int('8000',16)
        else:
            position = SYMTAB[lines[i][3]]
        OBJCODE = OPTAB[lines[i][2]] + hex(position)[2:].zfill(4)
    elif lines[i][2] == "BYTE":
        raw_B = lines[i][3]
        if 'C' in raw_B:
            raw_B = raw_B[raw_B.find("'")+1:]
            raw_B = raw_B[:raw_B.find("'")]
            for c in raw_B:
                OBJCODE += hex(ord(c))[2:]
        else:
            raw_B = raw_B[raw_B.find("'")+1:]
            raw_B = raw_B[:raw_B.find("'")]
            OBJCODE = raw_B
    elif lines[i][2] == "WORD":
        OBJCODE = hex(int(lines[i][3]))[2:].zfill(6)
    lines[i].append(OBJCODE.upper())

#.lst
for line in lines:
    for i in range(5):
        label = line[i]
        if label == "":
             if i == 3:
                print("", end="\t\t")
             else:
                print("", end="\t")
        else:
            if i == 3 and len(line[3]) < 8:
                print(label, end="\t\t")
            else:
                print(label, end="\t")
    print('')
#.obj
HEADER = "H" + name
for i in range(6-len(name)):
    HEADER += " "
HEADER += hex(START)[2:].zfill(6) + hex(LOCCTR - START)[2:].zfill(6)
HEADER = HEADER.upper()
TEXT = []
text_start = 0
text_length = 0
text = ""
i = 1
while i < len(lines):
    if len(text) == 0:
        text_start = lines[i][0]
    if lines[i][4] == "" and len(text) > 0:
        text = "T"+text_start.zfill(6)+str(hex(int(len(text)/2))[2:]).zfill(2)+text
        TEXT.append(text.upper())
        text = "" 
    else:
        if len(text+lines[i][4]) <= 60:
            text += lines[i][4]
        else:
            text = "T"+text_start.zfill(6)+str(hex(int(len(text)/2))[2:]).zfill(2)+text
            TEXT.append(text.upper())    
            text_start = lines[i][0]
            text = lines[i][4]
        if len(text) == 60:
            text = "T"+text_start.zfill(6)+str(hex(int(len(text)/2))[2:]).zfill(2)+text
            TEXT.append(text.upper())
            text = ""
    i += 1
if text != "":
    text = "T"+text_start.zfill(6)+str(hex(int(len(text)/2))[2:]).zfill(2)+text
    TEXT.append(text.upper())
if lines[len(lines)-1][3] == "":
    END = "E"+hex(START)[2:].zfill(6)
else:
    END = "E"+hex(SYMTAB[lines[len(lines)-1][3]])[2:].zfill(6)
asm.close()
if len(argvs) == 1:
    file_name = file_name[:file_name.find('.asm')]
else:
    file_name = argvs[1][:argvs[1].find('.asm')]
with open(file_name+".lst","w") as lst:
        for line in lines:
            for i in range(5):
                label = line[i]
                if label == "":
                     if i == 3:
                         lst.write("\t")
                     else:
                         lst.write("\t")
                else:
                    if i == 3 and len(line[3]) < 8:
                        lst.write(label+"\t\t")
                    else:
                        lst.write(label+"\t")
            lst.write("\n")
with open(file_name+".obj","w") as obj:
    obj.write(HEADER+"\n")
    for text in TEXT:
        obj.write(text+"\n")
    obj.write(END+"\n")
