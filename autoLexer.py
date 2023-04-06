import ply.lex as lex


class AutoLexer(object):

    # 创建构造器
    def __init__(self):
        self.lexer = None

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # 启动
    def start(self, filename):
        data = self.readFile(filename)
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)
            self.words.append([tok.value, tok.lineno, self.changeToTokNum(tok)])

    # 读取文件
    def readFile(self, filename):
        with open(file=filename, mode='r', encoding='utf-8') as f:
            return f.read()

    # 将token转换为种别码
    def changeToTokNum(self, t):
        for token in self.tokens:
            if t.type == token:
                for tokenNum in self.tokenNums.keys():
                    if token == tokenNum:
                        return self.tokenNums.get(tokenNum)

    def getWords(self):
        return self.words

    # 记录单词
    words = []

    # 关键字
    keyID = {
        # 数据类型相关
        'char': 'CHAR', 'int': 'INT', 'float': 'FLOAT', 'void': 'VOID', 'const': 'CONST',
        # 函数内关键字
        'break': 'BREAK', 'continue': 'CONTINUE', 'return': 'RETURN',
        'do': 'DO', 'while': 'WHILE', 'if': 'IF', 'else': 'ELSE', 'for': 'FOR',
        'true': 'TRUE', 'false': 'FALSE',
        # 内置函数
        'memset': 'MEMSET', 'sizeof': 'SIZEOF', 'gets': 'GETS', 'printf': 'PRINTF', 'scanf': 'SCANF'
    }

    # token序列
    tokens = [
        # 运算符
        'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'NOT',
        'MULTIPLY', 'DIVIDE', 'PERCENT', 'PLUS', 'MINUS',
        'LESS', 'LESSEQUAL', 'MORE', 'MOREEQUAL', 'DOUBLEEQUAL',
        'NOTEQUAL', 'AND', 'OR', 'EQUAL', 'BINARYAND',
        'PLUSEQUAL', 'MINUSEQUAL', 'MULTIPLYEQUAL', 'DIVIDEEQUAL', 'DOUBLEPLUS',
        'DOUBLEMINUS', 'ANDEQUAL', 'OREQUAL',
        # 界符
        'LBRACES', 'RBRACES', 'SEMICOLON', 'COMMA',
        # 函数token
        'NUMBER', 'ID', 'COMMENT', 'STRING', 'CH', 'error'] + list(keyID.values())

    tokenNums = {
        # 数据类型相关
        'CHAR': 101, 'INT': 102, 'FLOAT': 103, 'VOID': 104, 'CONST': 105,
        # 函数内关键字
        'BREAK': 106, 'CONTINUE': 107, 'RETURN': 108,
        'DO': 109, 'WHILE': 110, 'IF': 111, 'ELSE': 112, 'FOR': 113,
        'TRUE': 114, 'FALSE': 115,
        # 内置函数
        'MEMSET': 116, 'SIZEOF': 117, 'GETS': 118, 'PRINTF': 119, 'SCANF': 120,
        # 运算符
        'LPAREN': 201, 'RPAREN': 202, 'LBRACKET': 203, 'RBRACKET': 204, 'NOT': 205,
        'MULTIPLY': 206, 'DIVIDE': 207, 'PERCENT': 208, 'PLUS': 209, 'MINUS': 210,
        'LESS': 211, 'LESSEQUAL': 212, 'MORE': 213, 'MOREEQUAL': 214, 'DOUBLEEQUAL': 215,
        'NOTEQUAL': 216, 'AND': 217, 'OR': 218, 'EQUAL': 219, 'BINARYAND': 220,
        'PLUSEQUAL': 221, 'MINUSEQUAL': 222, 'MULTIPLYEQUAL': 223, 'DIVIDEEQUAL': 224, 'DOUBLEPLUS': 225,
        'DOUBLEMINUS': 226, 'ANDEQUAL': 227, 'OREQUAL': 228,
        # 界符
        'LBRACES': 301, 'RBRACES': 302, 'SEMICOLON': 303, 'COMMA': 304,
        # 数字标志符等
        'NUMBER': 400, 'ID': 700, 'CH': 500, 'STRING': 600, 'error': 0
    }

    # 规则
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_NOT = r'\!'
    t_MULTIPLY = r'\*'
    t_DIVIDE = r'/'
    t_PERCENT = r'%'
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_LESS = r'<'
    t_LESSEQUAL = r'<='
    t_MORE = r'>'
    t_MOREEQUAL = r'>='
    t_DOUBLEEQUAL = r'=='
    t_NOTEQUAL = r'!='
    t_AND = r'&&'
    t_OR = r'\|\|'
    t_EQUAL = r'='
    t_BINARYAND = r'\&'
    t_PLUSEQUAL = r'\+='
    t_MINUSEQUAL = r'-='
    t_MULTIPLYEQUAL = r'\*='
    t_DIVIDEEQUAL = r'/='
    t_DOUBLEPLUS = r'\+\+'
    t_DOUBLEMINUS = r'--'
    t_ANDEQUAL = r'&='
    t_OREQUAL = r'\|='
    t_LBRACES = r'\{'
    t_RBRACES = r'\}'
    t_SEMICOLON = r';'
    t_COMMA = r'\,'

    # # ID规则
    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.keyID.get(t.value, 'ID')  # Check for keyID words
        return t

    # 数字规则
    def t_NUMBER(self, t):
        # 1:整数，小数，科学计数，2:0开头的数 3：八进制 4:16进制
        r"""
        [+-]?[1-9]\d*(\.\d+)?([eE][+-]?[1-9]\d*)?\b|
        [+-]?0(\.\d+)?([eE][+-]?\d+)?\b|
        0[1-7]+\b|
        0[xX][1-9a-fA-F]+\b
        """
        return t

    # 注释规则
    def t_COMMENT(self, t):
        r'/\*.*?\n*.*?\*/|//.*'
        for ch in t.value:
            if ch == '\n':
                t.lexer.lineno += 1

    # 字符串规则
    def t_STRING(self, t):
        r'\".*\"'
        t.value = t.value[1:len(t.value) - 1]
        return t

    # 字符规则
    def t_CH(self, t):
        r'\'.*\''
        t.value = t.value[1:len(t.value) - 1]
        return t

    # 对于空行的规则
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # 忽略空格
    t_ignore = ' \t'

    # 输出错误的规则
    def t_error(self, t):
        index = 0
        currentCH = t.value[index]
        while currentCH != ' ' and currentCH != '\r' and currentCH != '\n':
            index += 1
            currentCH = t.value[index]
        if currentCH == '\n':
            t.lexer.lineno += 1
        t.value = t.value[0:index]
        # print("----LexToken(ERROR,'" + str(t.value) + "'," + str(t.lineno) + "," + str(t.lexpos) + ")----")
        t.lexer.skip(1+index)
        return t


if __name__ == '__main__':
    # Build the lexer
    lexer = AutoLexer()
    lexer.build()
    lexer.start("词法分析用例1.txt")

