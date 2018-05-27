#coding:utf-8
from __future__ import print_function
from sematic import *
from modules.function import *
CurrentLable=0
CurrentTemp=0
CurrentFunction=0
CurrentStep=0
CurrentOffset=0
CurrentProduction=None
CurrentFunctionSymbol=None
ProductionGroup=[]
DotedProductionGroup=[]
TerminalSymbolGroup=[]
LeftGroup=[]
StateIndexTable={}
TerminalIndexTable={}
NonterminalIndexTable={}
ACTION=[]
GOTO=[]
StartProduction=None
DFA=DFA()
Reduce={}
Shift={}
FIRST={}
FOLLOW={}
OpStack = []
StateStack = []
Table=None
SymbolTable=[]
FunctionTable=[]
SemanticStack=[]
Tokens=[]
Regs={'$'+str(x):'' for x in range(7,26)}
TempValueStatus={}
Mips=[]
StackOffset=8000
DataSegment=10010000
path=''

def MiPS(c_path_file):
    prepare_grammar()
    lexer.read_source_file(c_path_file)
    do_parsing()
    # prettyprint_parsing_table()
    print("SYMBOL TABLE")
    print("------------")
    print_symbol_table()
    print('\n')
    print("CODE")
    print("------------")
    print_code_result()
    variables={}
    i=1
    print('\n')
    print("MIPS_CODE")
    print("------------")
    # print("#寄存器说明")
    # print("#变量  寄存器")
    for t in SYMBOL_TABLE:
        variables[t.name]=str('$'+str(i))

        # print('# '+t.name+'     '+variables[t.name])
        i+=1
    # print('\n')
    print('sll $0,$0,0')
    mark_1=i
    print('addi &'+str(mark_1)+",$0,1")
    i+=1


    labels={}
    count=1
    for r in CODE_RESULT:
        tmp = r.strip(' ').split()
        if 'GOTO' in r:
            labels[int(tmp[-1])]=str('loop'+str(count)+':')
            count+=1


    for r in CODE_RESULT:
        tmp=r.strip(' ').split( )
        # print(tmp)
        if CODE_RESULT.index(r) in labels.keys():
            print(labels[CODE_RESULT.index(r)])

        if ':=' in tmp:
            print('lw '+variables[tmp[0]]+','+tmp[-1])
        if 'IF' in tmp:
            print('addi $'+str(i)+',$0,'+str(tmp[1]))
            i+=1
            print('subi $'+str(i)+',$'+str(i-1)+',$'+str(mark_1))
            print('bgez $'+str(i)+','+labels[int(tmp[-1])][0:-1])
        if 'IF' not in tmp and 'GOTO' in tmp:
            print('j '+labels[int(tmp[-1])][0:-1])
        if '+'==tmp[0]:
            if tmp[1] not in variables.keys() and tmp[2] not in variables.keys():
                print('addi $' + str(i-1) + ',$0,' + str(tmp[1]))
                print('addi '+variables[tmp[-1]]+',$'+str(i-1)+','+str(tmp[2]))
            elif tmp[1] in variables.keys() and tmp[2] not in variables.keys():
                print('addi '+variables[tmp[-1]]+','+variables[tmp[1]]+','+str(tmp[2]))
            elif tmp[1] not in variables.keys() and tmp[2] in variables.keys():
                print('addi '+variables[tmp[-1]]+','+variables[tmp[2]]+','+str(tmp[1]))
            else:
                print('add '+variables[tmp[-1]]+','+variables[tmp[1]]+','+variables[tmp[2]])
        if tmp[0]=='-':
            if tmp[1] not in variables.keys() and tmp[2] not in variables.keys():
                print('addi $' + str(i-1) + ',$0,' + str(tmp[1]))
                print('subi '+variables[tmp[-1]]+',$'+str(i-1)+','+str(tmp[2]))
            elif tmp[1] in variables.keys() and tmp[2] not in variables.keys():
                print('subi '+variables[tmp[-1]]+','+variables[tmp[1]]+','+str(tmp[2]))
            elif tmp[1] not in variables.keys() and tmp[2] in variables.keys():
                print('lw $'+str(i-1)+','+tmp[1])
                print('sub '+variables[tmp[-1]]+',$'+str(i-1)+','+variables[tmp[2]])
            else:
                print('sub '+variables[tmp[-1]]+','+variables[tmp[1]]+','+variables[tmp[2]])
        if tmp[0]=='*':
            if tmp[1] not in variables.keys() and tmp[2] not in variables.keys():
                print('addi $' + str(i-1) + ',$0,' + str(tmp[1]))
                print('lw $'+str(i)+','+str(tmp[2]))
                print('mul '+variables[tmp[-1]]+',$'+str(i-1)+',$'+str(i))
            elif tmp[1] in variables.keys() and tmp[2] not in variables.keys():
                print('lw $'+str(i-1)+','+tmp[2])
                print('mul '+variables[tmp[-1]]+','+variables[tmp[1]]+','+str(i-1))
            elif tmp[1] not in variables.keys() and tmp[2] in variables.keys():
                print('lw $'+str(i-1)+','+tmp[1])
                print('mul '+variables[tmp[-1]]+',$'+str(i-1)+','+variables[tmp[2]])
            else:
                print('mul '+variables[tmp[-1]]+','+variables[tmp[1]]+','+variables[tmp[2]])
        if tmp[0]=='/':
            if tmp[1] not in variables.keys() and tmp[2] not in variables.keys():
                print('addi $' + str(i-1) + ',$0,' + str(tmp[1]))
                print('lw $'+str(i)+','+str(tmp[2]))
                print('div $'+str(i-1)+',$'+str(i))
                print('mfl0 '+variables[tmp[-1]])
            elif tmp[1] in variables.keys() and tmp[2] not in variables.keys():
                print('lw $'+str(i-1)+','+tmp[2])
                print('div '+variables[tmp[1]]+','+str(i-1))
                print('mfl0 ' + variables[tmp[-1]])
            elif tmp[1] not in variables.keys() and tmp[2] in variables.keys():
                print('lw $'+str(i-1)+','+tmp[1])
                print('div $'+str(i-1)+','+variables[tmp[2]])
                print('mfl0 ' + variables[tmp[-1]])
            else:
                print('div '+variables[tmp[1]]+','+variables[tmp[2]])
                print('mfl0 ' + variables[tmp[-1]])
        if tmp[0]=='&':
            if tmp[1] not in variables.keys() and tmp[2] not in variables.keys():
                print('addi $' + str(i-1) + ',$0,' + str(tmp[1]))
                print('lw $'+str(i)+','+str(tmp[2]))
                print('and '+variables[tmp[-1]]+',$'+str(i-1)+',$'+str(i))
            elif tmp[1] in variables.keys() and tmp[2] not in variables.keys():
                print('lw $'+str(i-1)+','+tmp[2])
                print('and '+variables[tmp[-1]]+','+variables[tmp[1]]+','+str(i-1))
            elif tmp[1] not in variables.keys() and tmp[2] in variables.keys():
                print('lw $'+str(i-1)+','+tmp[1])
                print('and '+variables[tmp[-1]]+',$'+str(i-1)+','+variables[tmp[2]])
            else:
                print('and '+variables[tmp[-1]]+','+variables[tmp[1]]+','+variables[tmp[2]])
            if tmp[0]=='%':
                if tmp[1] not in variables.keys() and tmp[2] not in variables.keys():
                    print('addi $' + str(i - 1) + ',$0,' + str(tmp[1]))
                    print('lw $' + str(i) + ',' + str(tmp[2]))
                    print('div $' + str(i - 1) + ',$' + str(i))
                    print('mfhi ' + variables[tmp[-1]])
                elif tmp[1] in variables.keys() and tmp[2] not in variables.keys():
                    print('lw $' + str(i - 1) + ',' + tmp[2])
                    print('div ' + variables[tmp[1]] + ',' + str(i - 1))
                    print('mfhi ' + variables[tmp[-1]])
                elif tmp[1] not in variables.keys() and tmp[2] in variables.keys():
                    print('lw $' + str(i - 1) + ',' + tmp[1])
                    print('div $' + str(i - 1) + ',' + variables[tmp[2]])
                    print('mfhi ' + variables[tmp[-1]])
                else:
                    print('div ' + variables[tmp[1]] + ',' + variables[tmp[2]])
                    print('mfhi ' + variables[tmp[-1]])
            if tmp[0]=='>':
                if tmp[1] not in variables.keys() and tmp[2] not in variables.keys():
                    print('addi $' + str(i - 1) + ',$0,' + str(tmp[1]))
                    print('lw $' + str(i) + ',' + str(tmp[2]))
                    print('sub $' + str(i - 1) + ',$' + str(i-1)+',$'+str(i))
                    count+=1
                    print('bgz $' + str(i-1)+',loop'+str(count))
                    print('lw '+variables[tmp[-1]]+',0')
                    print('loop'+str(count))
                    print('lw '+variables[tmp[-1]]+',1')

                elif tmp[1] in variables.keys() and tmp[2] not in variables.keys():
                    print('lw $' + str(i - 1) + ',' + tmp[2])
                    print('sub $' + str(i - 1)+','+variables[tmp[1]] + ',' + str(i - 1))
                    count += 1
                    print('bgz $' + str(i - 1) + ',loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',0')
                    print('loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',1')
                elif tmp[1] not in variables.keys() and tmp[2] in variables.keys():
                    print('lw $' + str(i - 1) + ',' + tmp[1])
                    print('sub $' + str(i - 1) + ',$' + str(i-1)+','+ variables[tmp[2]])
                    count += 1
                    print('bgz $' + str(i - 1) + ',loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',0')
                    print('loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',1')
                else:
                    print('sub ' + str(i-1) + ',' + variables[tmp[1]]+','+variables[tmp[2]])
                    count += 1
                    print('bgz $' + str(i - 1) + ',loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',0')
                    print('loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',1')
            if tmp[0]=='>=':
                if tmp[1] not in variables.keys() and tmp[2] not in variables.keys():
                    print('addi $' + str(i - 1) + ',$0,' + str(tmp[1]))
                    print('lw $' + str(i) + ',' + str(tmp[2]))
                    print('sub $' + str(i - 1) + ',$' + str(i-1)+',$'+str(i))
                    count+=1
                    print('bgez $' + str(i-1)+',loop'+str(count))
                    print('lw '+variables[tmp[-1]]+',0')
                    print('loop'+str(count))
                    print('lw '+variables[tmp[-1]]+',1')

                elif tmp[1] in variables.keys() and tmp[2] not in variables.keys():
                    print('lw $' + str(i - 1) + ',' + tmp[2])
                    print('sub $' + str(i - 1)+','+variables[tmp[1]] + ',' + str(i - 1))
                    count += 1
                    print('bgez $' + str(i - 1) + ',loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',0')
                    print('loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',1')
                elif tmp[1] not in variables.keys() and tmp[2] in variables.keys():
                    print('lw $' + str(i - 1) + ',' + tmp[1])
                    print('sub $' + str(i - 1) + ',$' + str(i-1)+','+ variables[tmp[2]])
                    count += 1
                    print('bgez $' + str(i - 1) + ',loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',0')
                    print('loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',1')
                else:
                    print('sub ' + str(i-1) + ',' + variables[tmp[1]]+','+variables[tmp[2]])
                    count += 1
                    print('bgez $' + str(i - 1) + ',loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',0')
                    print('loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',1')
            if tmp[0]=='==':
                if tmp[1] not in variables.keys() and tmp[2] not in variables.keys():
                    print('addi $' + str(i - 1) + ',$0,' + str(tmp[1]))
                    print('lw $' + str(i) + ',' + str(tmp[2]))
                    print('sub $' + str(i - 1) + ',$' + str(i-1)+',$'+str(i))
                    count+=1
                    print('beq $' + str(i-1)+',loop'+str(count))
                    print('lw '+variables[tmp[-1]]+',0')
                    print('loop'+str(count))
                    print('lw '+variables[tmp[-1]]+',1')

                elif tmp[1] in variables.keys() and tmp[2] not in variables.keys():
                    print('lw $' + str(i - 1) + ',' + tmp[2])
                    print('sub $' + str(i - 1)+','+variables[tmp[1]] + ',' + str(i - 1))
                    count += 1
                    print('beq $' + str(i - 1) + ',loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',0')
                    print('loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',1')
                elif tmp[1] not in variables.keys() and tmp[2] in variables.keys():
                    print('lw $' + str(i - 1) + ',' + tmp[1])
                    print('sub $' + str(i - 1) + ',$' + str(i-1)+','+ variables[tmp[2]])
                    count += 1
                    print('beq $' + str(i - 1) + ',loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',0')
                    print('loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',1')
                else:
                    print('sub ' + str(i-1) + ',' + variables[tmp[1]]+','+variables[tmp[2]])
                    count += 1
                    print('beq $' + str(i - 1) + ',loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',0')
                    print('loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',1')
            if tmp[0]=='<':
                if tmp[1] not in variables.keys() and tmp[2] not in variables.keys():
                    print('addi $' + str(i - 1) + ',$0,' + str(tmp[1]))
                    print('lw $' + str(i) + ',' + str(tmp[2]))
                    print('sub $' + str(i - 1) + ',$' + str(i-1)+',$'+str(i))
                    count+=1
                    print('bltz $' + str(i-1)+',loop'+str(count))
                    print('lw '+variables[tmp[-1]]+',0')
                    print('loop'+str(count))
                    print('lw '+variables[tmp[-1]]+',1')

                elif tmp[1] in variables.keys() and tmp[2] not in variables.keys():
                    print('lw $' + str(i - 1) + ',' + tmp[2])
                    print('sub $' + str(i - 1)+','+variables[tmp[1]] + ',' + str(i - 1))
                    count += 1
                    print('bltz $' + str(i - 1) + ',loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',0')
                    print('loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',1')
                elif tmp[1] not in variables.keys() and tmp[2] in variables.keys():
                    print('lw $' + str(i - 1) + ',' + tmp[1])
                    print('sub $' + str(i - 1) + ',$' + str(i-1)+','+ variables[tmp[2]])
                    count += 1
                    print('bltz $' + str(i - 1) + ',loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',0')
                    print('loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',1')
                else:
                    print('sub ' + str(i-1) + ',' + variables[tmp[1]]+','+variables[tmp[2]])
                    count += 1
                    print('bltz $' + str(i - 1) + ',loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',0')
                    print('loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',1')
            if tmp[0]=='<=':
                if tmp[1] not in variables.keys() and tmp[2] not in variables.keys():
                    print('addi $' + str(i - 1) + ',$0,' + str(tmp[1]))
                    print('lw $' + str(i) + ',' + str(tmp[2]))
                    print('sub $' + str(i - 1) + ',$' + str(i-1)+',$'+str(i))
                    count+=1
                    print('blez $' + str(i-1)+',loop'+str(count))
                    print('lw '+variables[tmp[-1]]+',0')
                    print('loop'+str(count))
                    print('lw '+variables[tmp[-1]]+',1')

                elif tmp[1] in variables.keys() and tmp[2] not in variables.keys():
                    print('lw $' + str(i - 1) + ',' + tmp[2])
                    print('sub $' + str(i - 1)+','+variables[tmp[1]] + ',' + str(i - 1))
                    count += 1
                    print('blez $' + str(i - 1) + ',loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',0')
                    print('loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',1')
                elif tmp[1] not in variables.keys() and tmp[2] in variables.keys():
                    print('lw $' + str(i - 1) + ',' + tmp[1])
                    print('sub $' + str(i - 1) + ',$' + str(i-1)+','+ variables[tmp[2]])
                    count += 1
                    print('blez $' + str(i - 1) + ',loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',0')
                    print('loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',1')
                else:
                    print('sub ' + str(i-1) + ',' + variables[tmp[1]]+','+variables[tmp[2]])
                    count += 1
                    print('blez $' + str(i - 1) + ',loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',0')
                    print('loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',1')
            if tmp[0]=='!=':
                if tmp[1] not in variables.keys() and tmp[2] not in variables.keys():
                    print('addi $' + str(i - 1) + ',$0,' + str(tmp[1]))
                    print('lw $' + str(i) + ',' + str(tmp[2]))
                    print('sub $' + str(i - 1) + ',$' + str(i-1)+',$'+str(i))
                    count+=1
                    print('bgz $' + str(i-1)+',loop'+str(count))
                    print('lw '+variables[tmp[-1]]+',0')
                    print('loop'+str(count))
                    print('lw '+variables[tmp[-1]]+',1')

                elif tmp[1] in variables.keys() and tmp[2] not in variables.keys():
                    print('lw $' + str(i - 1) + ',' + tmp[2])
                    print('sub $' + str(i - 1)+','+variables[tmp[1]] + ',' + str(i - 1))
                    count += 1
                    print('bne $' + str(i - 1) + ',loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',0')
                    print('loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',1')
                elif tmp[1] not in variables.keys() and tmp[2] in variables.keys():
                    print('lw $' + str(i - 1) + ',' + tmp[1])
                    print('sub $' + str(i - 1) + ',$' + str(i-1)+','+ variables[tmp[2]])
                    count += 1
                    print('bne $' + str(i - 1) + ',loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',0')
                    print('loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',1')
                else:
                    print('sub ' + str(i-1) + ',' + variables[tmp[1]]+','+variables[tmp[2]])
                    count += 1
                    print('bne $' + str(i - 1) + ',loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',0')
                    print('loop' + str(count))
                    print('lw ' + variables[tmp[-1]] + ',1')

if __name__=='__main__':
    MIPS('S:\pycharm\compiler_1.5\modules\\test.c')



