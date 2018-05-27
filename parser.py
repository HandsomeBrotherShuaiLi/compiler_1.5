import lexer
from  definition import *
from util import Production, Symbol
class PRODUCTION(object):
    def __init__(self,left,right,select=None):
        self.left=left
        self.right=right
        self.select=set()
    def str_production(self):
        return self.left+'->'+str(self.right)+'Select:'+str(self.select)
class SYMBOL(object):
    def __init__(self,symbol,first_set=None,follow_set=None,sym_type='N'):
        self.symbol=symbol
        self.first_set=first_set
        self.follow_set=follow_set
        self.sym_type=sym_type
        self.is_nullable=False
        self.attr=dict()
        self.father=None
        self.children=[]
        self.lex_value=None
        self.parsing_table={}
    def is_terminal(self):
        return self.sym_type=='T'


class ENTRY(object):
    def __init__(self,type,length,name):
        self.type=type
        self.length=length
        self.name=name


class grammar(object):
    def __init__(self,grammar_path=None,c_file_path=None):
        # testbanch***********************************************
        self.terminal_set = set(terminal_set)
        #*********************************************************
        self.non_terminal_set=set()
        self.symbol_dictionary=dict()
        self.production_list=[]
        self.parsing_table={}
        self.symbol_table={}
        self.symbol_stack=[]

        self.grammar_file=open(grammar_path,'r')

        self.last_stack_top_symbol=None

    def pretreatment(self):
        # blocks = self.grammar_file.read().split('\n\n')
        # for i in blocks:
        #     tm=i.split('\n')
        #     self.non_terminal_set.update([tm[0]])
        #     print(i)
        #
        #     for x in tm[1:-1]:
        #         x = x.strip(' ').strip('|').strip(':').split( )
        #         tmp=[]
        #         for w in x:
        #             if w[0]=='\'' and w[-1]=='\'':
        #                 self.terminal_set.update([w[1:-1]])
        #                 tmp.append(w[1:-1])
        #             elif w in reserved_words.values()or w in reserved_words.keys() or w=='id':
        #                 self.terminal_set.update([w])
        #                 tmp.append(w)
        #             else:
        #                 self.non_terminal_set.update([w])
        #                 tmp.append(w)
        #         p=PRODUCTION(tm[0],tmp)
        #         self.production_list.append(p)
        #         print(p.str_production())









        for line in self.grammar_file:
            left_and_right=line.split('::=')
            left=left_and_right[0].strip().strip('\t')
            self.non_terminal_set.update([left])
            right=left_and_right[1].strip().strip('\t').strip('\n')
            if right=='':
                p = PRODUCTION(left, ['null'])
            else:
                p = PRODUCTION(left, right.split( ))
            self.production_list.append(p)
        # print(self.non_terminal_set)



        for i in self.terminal_set:
            symb=SYMBOL(i,sym_type='T')
            self.symbol_dictionary[i]=symb
        for i in self.non_terminal_set:
            symb=SYMBOL(i,sym_type='N')
            self.symbol_dictionary[i]=symb
        flag=1
        while flag:
            flag=0
            for i in self.production_list:
                print(i)
                if self.symbol_dictionary[i.left].is_nullable==False:
                    if i.right[0]=='null':
                        self.symbol_dictionary[i.left].is_nullable=True
                        flag=1
                        continue
                    else:

                        tmp=self.symbol_dictionary[i.right[0]].is_nullable
                        for x in i.right[1:]:
                            tmp=tmp and self.symbol_dictionary[x].is_nullable
                        if tmp:
                            flag=1
                            self.symbol_dictionary[i.left].is_nullable=True
    #计算first集
    def make_first_set(self):
        for s in self.terminal_set:
            self.symbol_dictionary[s].first_set=set([s])
        for s in self.non_terminal_set:
            sym=self.symbol_dictionary[s]
            if sym.is_nullable:
                self.symbol_dictionary[s].first_set=set(['null'])
            else:
                self.symbol_dictionary[s].first_set=set()
        while 1:
            flag=True
            for p in self.production_list:
                if p.right[0]=='null':
                    self.symbol_dictionary[p.left].first_set.update(['null'])
                    continue
                previous=set(self.symbol_dictionary[p.left].first_set)
                for s in p.right:
                    self.symbol_dictionary[p.left].first_set.update(self.symbol_dictionary[s].first_set)
                    if self.symbol_dictionary[s].is_nullable:
                        continue
                    else:
                        break

                if previous!=self.symbol_dictionary[p.left].first_set:
                    flag = False

            if flag:
                break
    #计算follow集
    def make_follow_set(self):
        for s in self.non_terminal_set:
            self.symbol_dictionary[s].follow_set=set()
        self.symbol_dictionary['S'].follow_set.update(['#'])
        while 1:
            flag=True
            for p in self.production_list:
                if self.symbol_dictionary[p.left].is_terminal():
                    continue
                for s in p.right:
                    if s=='null':
                        continue
                    if self.symbol_dictionary[s].is_terminal():
                        continue
                    current_symbol=self.symbol_dictionary[s]
                    previous=set(current_symbol.follow_set)
                    next_is_nullable=True
                    for w in p.right[p.right.index(s)+1:]:
                        next_symbol=self.symbol_dictionary[w]
                        self.symbol_dictionary[s].follow_set.update(next_symbol.first_set)

                        if next_symbol.is_nullable:
                            continue
                        else:
                            next_is_nullable=False
                            break
                    if next_is_nullable:
                        self.symbol_dictionary[s].follow_set.update(self.symbol_dictionary[p.left].follow_set)
                    if self.symbol_dictionary[s].follow_set!=previous:
                        flag=False
            if flag:
                break
        #mark!!!!!!!!!!!!!!!!!!*******
        for x in self.non_terminal_set:
            if str('null') in self.symbol_dictionary[x].follow_set:
                self.symbol_dictionary[x].follow_set.remove('null')
    #做分析表
    def make_parse_table(self):
        while 1:
            flag=True
            for p in self.production_list:
                sym_left=self.symbol_dictionary[p.left]
                previous=set(p.select)
                if p.right[0]=='null':
                    p.select.update(sym_left.follow_set)
                    continue
                sym_right=self.symbol_dictionary[p.right[0]]
                p.select.update(sym_right.first_set)
                if sym_right.is_nullable:
                    p.select.update(sym_right.first_set.union(sym_left.follow_set))
                if previous!=p.select:
                    flag=False
            if flag:
                break
        for n in self.non_terminal_set:
            self.parsing_table[n]={}
            for p in self.production_list:
                if n==p.left:
                    for symbol in p.select:
                        self.parsing_table[n][symbol]=p
            for symbol in self.symbol_dictionary[n].follow_set:
                if symbol in self.terminal_set:
                    try:
                        p=self.parsing_table[n][symbol]
                    except KeyError:
                        self.parsing_table[n][symbol]='SYNC'
            for symbol in self.symbol_dictionary[n].first_set:
                if symbol in self.terminal_set:
                    try:
                        p=self.parsing_table[n][symbol]
                    except KeyError:
                        self.parsing_table[n][symbol]='SYNC'
    def do_grammar(self):
        self.symbol_stack.append('#')
        self.symbol_stack.append('<s>')
        productions=open('productions.txt','w')
        stack=open('stack.txt','w')
        i=0
        tokenlength=len(self.tokens)
        while(len(self.symbol_stack)>0):
            stack_top_symbol=self.symbol_stack[-1]
            current_token=str()
            if i>=tokenlength:
                current_token='#'

            if self.tokens[i]['type'] == 'OPERATOR' or self.tokens[i]['type'] == 'SEPERATOR':
                current_token = self.tokens[i]['data']
            if stack_top_symbol == 'null':
                self.last_stack_top_symbol = self.symbol_stack.pop()
                continue
            if stack_top_symbol == '#':
                break
            if stack_top_symbol not in self.terminal_set:
                try:
                    p = self.parsing_table[stack_top_symbol][current_token]
                except KeyError:
                    print('第'+self.tokens[i]['linenumber']+'行'+'第'+self.tokens[i]['column']+'列不匹配出错')

                    i+=1
                    continue
                if p=='SYNC':
                    print('第' + self.tokens[i]['linenumber'] + '行' + '第' + self.tokens[i]['column'] + '列重复覆盖出错')
                    self.last_stack_top_symbol=self.symbol_stack.pop()
                    stack.write(str(self.symbol_stack)+'\n')
                    productions.write(str(p)+'\n')
                    continue
                stack.write(str(self.symbol_stack)+'\n')
                productions.write(str(p)+'\n')
                self.last_stack_top_symbol=self.symbol_stack.pop()
                self.symbol_stack.extend(reversed(p.right))
            else:
                self.symbol_stack.pop()
                i+=1
        productions.close()
        stack.close()
    def main(self):
        self.pretreatment()
        self.make_first_set()
        self.make_follow_set()
        self.make_parse_table()
        self.do_grammar()
        print(self.non_terminal_set)
        print(self.terminal_set)

TERMINAL_SET = set()

NON_TERMINAL_SET = set()

SYMBOL_DICT = {}

PRODUCTION_LIST = []

PARSING_TABLE = {}

SYMBOL_STACK = []

SYMBOL_TABLE = {}

LAST_STACK_TOP_SYMBOL = None

def symbol_for_str(string):
    return SYMBOL_DICT[string]


def is_terminal(string):
    return string in TERMINAL_SET


def syntax_error(msg, line=None, row=None):
    if line is None:
        line = lexer.current_line + 1
    if row is None:
        row = lexer.current_row + 1
    print(str(line) + ':' + str(row) + ' Syntax error: ' + msg)


def prepare_symbols_and_productions():
    f = open('grammer.txt', 'r')
    lines = f.readlines()
    terminal = False
    production = False
    for l in lines:
        if l.strip() == '*terminals':
            terminal = True
            production = False
            continue
        if l.strip() == '*productions':
            terminal = False
            production = True
            continue
        if l.strip() == '*end':
            break
        if terminal:
            TERMINAL_SET.update([l.strip()])
        if production:
            left = l.split('::=')[0].strip()
            NON_TERMINAL_SET.update([left])

            try:
                right = l.split('::=')[1].strip()
                if right == '':
                    raise IndexError
                p = Production(left, right.split(' '))
            except IndexError:
                p = Production(left, ['null'])

            PRODUCTION_LIST.append(p)

    for s in TERMINAL_SET:
        sym = Symbol(s, sym_type='T')
        SYMBOL_DICT[s] = sym

    for s in NON_TERMINAL_SET:
        sym = Symbol(s, sym_type='N')
        SYMBOL_DICT[s] = sym


def get_nullable():

    changes = True
    while changes:
        changes = False
        for p in PRODUCTION_LIST:
            if not symbol_for_str(p.left).is_nullable:
                if p.right[0] == 'null':
                    symbol_for_str(p.left).is_nullable = True
                    changes = True
                    continue
                else:
                    right_is_nullable = symbol_for_str(p.right[0]).is_nullable

                    for r in p.right[1:]:
                        right_is_nullable = right_is_nullable & symbol_for_str(
                            r).is_nullable

                    if right_is_nullable:
                        changes = True
                        symbol_for_str(p.left).is_nullable = True


def get_first():

    for s in TERMINAL_SET:
        # For each terminal, initialize First with itself.
        sym = SYMBOL_DICT[s]
        sym.first_set = set([s])

    for s in NON_TERMINAL_SET:
        sym = SYMBOL_DICT[s]
        if sym.is_nullable:
            sym.first_set = set(['null'])
        else:
            sym.first_set = set()

    while True:
        first_set_is_stable = True
        for p in PRODUCTION_LIST:
            sym_left = symbol_for_str(p.left)
            if p.right[0] == 'null':
                sym_left.first_set.update(set(['null']))
                continue
            previous_first_set = set(sym_left.first_set)

            for s in p.right:

                sym_right = symbol_for_str(s)
                sym_left.first_set.update(sym_right.first_set)

                if sym_right.is_nullable:
                    continue
                else:
                    break

            if previous_first_set != sym_left.first_set:
                first_set_is_stable = False

        if first_set_is_stable:
            break


def get_follow():

    for s in NON_TERMINAL_SET:
        sym = symbol_for_str(s)
        sym.follow_set = set()

    symbol_for_str('<s>').follow_set.update(set(['#']))

    while True:
        follow_set_is_stable = True
        for p in PRODUCTION_LIST:
            sym_left = symbol_for_str(p.left)
            if sym_left.is_terminal():
                continue
            for s in p.right:
                if s == 'null':
                    continue
                if symbol_for_str(s).is_terminal():
                    continue
                current_symbol = symbol_for_str(s)
                previous_follow_set = set(current_symbol.follow_set)
                next_is_nullable = True
                for s2 in p.right[p.right.index(s) + 1:]:
                    # For X -> sYt, Follow(Y) = Follow(Y) U First(t)
                    next_symbol = symbol_for_str(s2)
                    current_symbol.follow_set.update(next_symbol.first_set)
                    if next_symbol.is_nullable:
                        continue
                    else:
                        next_is_nullable = False
                        break
                if next_is_nullable:

                    current_symbol.follow_set.update(sym_left.follow_set)

                if current_symbol.follow_set != previous_follow_set:
                    follow_set_is_stable = False

        if follow_set_is_stable:
            break


def get_select():

    while True:
        select_set_is_stable = True
        for p in PRODUCTION_LIST:
            sym_left = symbol_for_str(p.left)
            previous_select = set(p.select)
            if p.right[0] == 'null':

                p.select.update(sym_left.follow_set)
                continue
            sym_right = symbol_for_str(p.right[0])

            p.select.update(sym_right.first_set)

            if sym_right.is_nullable:
                p.select.update(sym_right.first_set.union(sym_left.follow_set))
            if previous_select != p.select:
                select_set_is_stable = False
        if select_set_is_stable:
            break


def get_parsing_table():

    global PARSING_TABLE
    for non_terminal in NON_TERMINAL_SET:
        PARSING_TABLE[non_terminal] = {}
        for p in PRODUCTION_LIST:
            if non_terminal == p.left:
                for symbol in p.select:
                    PARSING_TABLE[non_terminal][symbol] = p

        for symbol in symbol_for_str(non_terminal).follow_set:
            if is_terminal(symbol):
                try:
                    p = PARSING_TABLE[non_terminal][symbol]
                except KeyError:
                    PARSING_TABLE[non_terminal][symbol] = 'SYNC'

        for symbol in symbol_for_str(non_terminal).first_set:
            if is_terminal(symbol):
                try:
                    p = PARSING_TABLE[non_terminal][symbol]
                except KeyError:
                    PARSING_TABLE[non_terminal][symbol] = 'SYNC'



def prettyprint_parsing_table():
    for non_terminal in PARSING_TABLE.keys():
        symbol_to_production_list = []
        for symbol in PARSING_TABLE[non_terminal]:
            p = PARSING_TABLE[non_terminal][symbol]
            symbol_to_production = str(symbol) + ':' + str(p)
            symbol_to_production_list.append(symbol_to_production)

        print(non_terminal)
        print(symbol_to_production_list)

def print_symbol_table():
    for t in SYMBOL_TABLE:
        print(t)

def next_token():
    r = lexer.scanner()
    while r is None:
        r = lexer.scanner()
    return r


def prepare_grammar():
    prepare_symbols_and_productions()
    get_nullable()
    get_first()
    get_follow()
    get_select()
    get_parsing_table()


def do_parsing():
    SYMBOL_STACK.append('#')
    SYMBOL_STACK.append('<s>')

    token_tuple = next_token()
    productions = open('productions.txt', 'w')
    stack = open('stack.txt', 'w')
    while len(SYMBOL_STACK) > 0:
        stack_top_symbol = SYMBOL_STACK[-1]
        current_token = token_tuple[0]
        if current_token == 'OP' or current_token == 'SEP':
            current_token = token_tuple[1]

        if current_token == 'SCANEOF':
            current_token = '#'

        if stack_top_symbol == 'null':
            LAST_STACK_TOP_SYMBOL = SYMBOL_STACK.pop()
            continue

        if stack_top_symbol == '#':
            break

        if not is_terminal(stack_top_symbol):
            try:
                p = PARSING_TABLE[stack_top_symbol][current_token]
            except KeyError:

                syntax_error('unmatched')
                token_tuple = next_token()
                continue

            if p == 'SYNC':

                syntax_error("sync symbol, recovering")
                LAST_STACK_TOP_SYMBOL = SYMBOL_STACK.pop()
                stack.write(str(SYMBOL_STACK) + '\n')
                productions.write(str(p) + '\n')
                continue

            stack.write(str(SYMBOL_STACK) + '\n')
            productions.write(str(p) + '\n')
            LAST_STACK_TOP_SYMBOL = SYMBOL_STACK.pop()
            SYMBOL_STACK.extend(reversed(p.right))

        else:
            SYMBOL_STACK.pop()
            token_tuple = next_token()

    productions.close()
    stack.close()


# def main():
#     prepare_grammar()
#     lexer.read_source_file('1.c')
#     do_parsing()
#     print_symbol_table()

