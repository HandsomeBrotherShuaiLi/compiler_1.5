#coding:utf-8
reserved_words = {'if' : 'IF','then' : 'THEN','else' : 'ELSE', 'while' : 'WHILE', 'break':'BREAK', 'continue':'CONTINUE', 'for':'FOR', 'double':'DOUBLE','do':'DO',
    'string':'STRING','int':'INT','float':'FLOAT', 'long':'LONG', 'short':'SHORT', 'bool':'BOOL', 'switch':'SWITCH', 'case':'CASE', 'return':'RETURN', 'void':'VOID',
    'unsigned':'UNSIGNED', 'enum':'ENUM','register':'REGISTER', 'typedef':'TYPEDEF', 'char':'CHAR','extern':'EXTERN', 'union':'UNION','function':'FUNCTION',
    'const':'CONST', 'signed':'SIGNED', 'default':'DEFAULT','goto':'GOTO', 'sizeof':'SIZEOF','volatile':'VOLATILE','static':'STATIC','auto':'AUTO','struct':'STRUCT'
    ,'number':'NUMBER'
}#保留字
type=[
    'seperator', 'operator', 'id', 'string', 'char', 'int', 'float'
]#类别
regexs=[
    '\{|\}|\[|\]|\(|\)|,|;|\.|\?|\:'#分界符
    ,'\+|-|\*|%|/|>|<|=|==|!=|'#操作符
    ,'[a-zA-Z_][a-zA-Z_0-9]*'#标识符
    ,'\".+?\"'#字符串
    ,'\'.{1}\''#字符
    ,'\d+'#整数
    ,'-?\d+\.\d+?'#浮点数
]
terminal_set=['ID','VOID','INT','CHAR','FLOAT','LONG','DOUBLE','SHORT','STRING_LITERAL','(',')','[',']',
              ',',';','{','}','=',':','>','<','>=','<=','!=','==','+=','-=','*=','/=','%=','+',
              '-','*','/','%','&','~','++','--','!','#','int','float','double','short','long','while','if','else']
terminal_set_2=['+','*','(',')','i']



KEYWORD_LIST = ['if', 'else', 'while', 'break', 'continue', 'for', 'double', 'int', 'float', 'long', 'short',
                'switch', 'case', 'return', 'void','bool']

SEPARATOR_LIST = ['{', '}', '[', ']', '(', ')', '~', ',', ';', '.', '?', ':']

OPERATOR_LIST = ['+', '++', '-', '--', '+=', '-=', '*', '*=', '%', '%=', '->', '|', '||', '|=',
                 '/', '/=', '>', '<', '>=', '<=', '=', '==', '!=', '!',"&"]

CATEGORY_DICT = {
    "double": 265,
    "int": 266,
    "break": 268,
    "else": 269,
    "switch": 271,
    "case": 272,
    "char": 276,
    "return": 278,
    "float":  281,
    "continue": 284,
    "for": 285,
    "void": 287,
    "do": 292,
    "if": 293,
    "while": 294,
    "static": 295,
    "{": 299,
    "}": 300,
    "[": 301,
    "]": 302,
    "(": 303,
    ")": 304,
    "~": 305,
    ",": 306,
    ";": 307,
    "?": 310,
    ":": 311,
    "<": 314,
    "<=": 315,
    ">": 316,
    ">=": 317,
    "=": 318,
    "==": 319,
    "|": 320,
    "||": 321,
    "|=": 322,
    "^": 323,
    "^=": 324,
    "&": 325,
    "&&": 326,
    "&=": 327,
    "%": 328,
    "%=": 329,
    "+": 330,
    "++": 331,
    "+=": 332,
    "-": 333,
    "--": 334,
    "-=": 335,
    "->": 336,
    "/": 337,
    "/=": 338,
    "*": 339,
    "*=": 340,
    "!": 341,
    "!=": 342,
    "ID": 256,
    'INT10': 346,
    'FLOAT': 347,
    'STRING': 351,
}