import ply.lex as lex


class AutoLexer(object):

    # 记录单词
    words = []

    # 关键字
    keyID = {
        # 数据类型
        'char': 'CHAR', 'int': 'INT', 'float': 'FLOAT', 'void': 'VOID', 'const': 'CONST',
        # 函数内关键字
        'break': 'BREAK', 'continue': 'CONTINUE', 'return': 'RETURN',
        'do': 'DO', 'while': 'WHILE', 'if': 'IF', 'else': 'ELSE', 'for': 'FOR',
        'true': 'TRUE', 'false': 'FALSE',
        # 内置函数
        'memset': 'MEMSET', 'sizeof': 'SIZEOF', 'gets': 'GETS', 'printf': 'PRINTF', 'scanf': 'SCANF'
    }

    # token序列
    tokens = ['LPAREN', 'RPAREN', 'DIVIDE', 'TIMES', 'MINUS', 'PLUS', 'NUMBER', 'FENHAO',
              'DENGHAO', 'XIAOYU', 'DAYU', 'ZUODAKUOHAO', 'YOUDAKUOHAO', 'ID', 'COMMENT', 'STRING', 'CH'] \
             + list(keyID.values())

    tokenNums = {}

    # 创建构造器
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
            self.words.append([tok.value, tok.lineno, tok.type])

    # 读取文件
    def readFile(self, filename):
        with open(file=filename, mode='r', encoding='utf-8') as f:
            return f.read()

    # 将token转换为种别码
    def changeToTokNum(self, t):
        for token in self.tokens:
            if t == token:
                for tokenNum in self.tokenNums.keys():
                    if token == tokenNum:
                        return self.tokenNums.get(tokenNum)

    # 规则
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_FENHAO = r';'
    t_DENGHAO = r'='
    t_XIAOYU = r'<'
    t_DAYU = r'>'
    t_ZUODAKUOHAO = r'\{'
    t_YOUDAKUOHAO = r'\}'

    # # ID规则
    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.keyID.get(t.value, 'ID')  # Check for keyID words
        return t

    # 识别数字
    def t_NUMBER(self, t):
        # 1:整数，小数，科学计数，2:0开头的数 3：八进制 4:16进制
        r"""
        [+-]?[1-9]\d*(\.\d+)?([eE][+-]?[1-9]\d*)?\b|
        [+-]?0(\.[1-9]\d*[eE][+-]?[1-9]\d*|\.[1-9]\d*)?\b|
        0[0-7]+\b|
        0[xX][0-9a-fA-F]+\b
        """
        return t

    # 忽略注释
    def t_COMMENT(self, t):
        r'/\*.*?\n*.*?\*/|//.*'
        return t

    # 识别字符串
    def t_STRING(self, t):
        r'\".*\"'
        t.value = t.value[1:len(t.value) - 1]
        return t

    # 识别字符
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
        print("----LexToken(ERROR,'" + str(t.value[0]) + "'," + str(t.lineno) + "," + str(t.lexpos) + ")----")
        # self.errorWord += t.value
        t.lexer.skip(1)


if __name__ == '__main__':
    # Build the lexer
    lexer = AutoLexer()
    lexer.build()
    lexer.start("词法分析用例1.txt")

