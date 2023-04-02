import re


class Lexer:
    line = ""
    lines = None
    index = 0
    row = 0

    # 单词表
    words = []

    # 关键字
    key_token = {
        # 数据类型
        'char': 101, 'int': 102, 'float': 103, 'void': 104,  'const': 105,
        # 函数内关键字
        'break': 106, 'continue': 107, 'return': 108,
        'do': 109, 'while': 110, 'if': 111, 'else': 112, 'for': 113,
        'true': 114, 'false': 115,
        # 内置函数
        'memset': 116, 'sizeof': 117, 'gets': 118, 'printf': 119, 'scanf': 120
    }

    # 界符
    boundary_token = {
        '{': 301, '}': 302, ';': 303, ',': 304
    }

    # 运算符
    operation_token = {  # 删除了'.'操作符
        '(': 201, ')': 202, '[': 203, ']': 204, '!': 205,
        '*': 206, '/': 207, '%': 208, '+': 209, '-': 210,
        '<': 211, '<=': 212, '>': 213, '>=': 214, '==': 215,
        '!=': 216, '&&': 217, '||': 218, '=': 219, '&': 220,
        '+=': 221, '-=': 222, '*=': 223, '/=': 224, '++': 225,
        '--': 226, '&=': 227, '|=': 228

    }

    def start(self, filename):
        self.readLineFromFile(filename)
        self.line = self.lines[self.row]
        self.recognizeFirstCh()
        print('**********编译完成**********')

    def addWord(self, word, row, token):
        self.words.append([word, row, token])

    def getWords(self):
        return self.words

    # 从文件读取所有行的字符串
    def readLineFromFile(self, filename):
        with open(file=filename, mode="r", encoding="utf-8") as file:
            self.lines = file.readlines()
        self.ifNoEmptyLine()

    # 规范文件格式，检查行尾最后一个字符是否是换行符
    def ifNoEmptyLine(self):
        lastLine = self.lines[len(self.lines) - 1]
        if lastLine[len(lastLine) - 1] != '\n':
            # 不改原文件
            self.lines[len(self.lines) - 1] = lastLine + '\n'
            # 改写原文件
            # with open(file="1.txt", mode="a", encoding="utf-8") as file:
            #     file.write('\n')
            # self.readLineFromFile()

    def readNextLine(self):
        self.row += 1
        if self.row == len(self.lines):  # 判断是否读到最后一行
            return False
        else:
            self.line = self.lines[self.row]
            self.index = 0
            return True

    def recognizeFirstCh(self):
        while self.row < len(self.lines):
            ch = self.line[self.index]
            if ch == ' ' or ch == '\t':  # 忽略空白符
                self.index += 1
                continue
            elif ch.isdigit() or ch == '-':  # 首字符为数字或负号进入数值识别
                if not self.rec_dig():  # 识别到非负号的负号直接进入运算符识别
                    self.rec_other()
            elif ch.isalpha() or ch == "_":  # 首字符是字母或下划线进入标志符/关键字识别
                self.rec_id()
            elif ch == '/':  # 首字母为斜杠进入注释或除号识别
                self.rec_comment()
            elif ch == '\'':  # 首字符为单引号进入字符识别
                self.rec_ch()
            elif ch == '\"':  # 首字符为双引号进入字符串识别
                self.rec_str()
            elif ch == '\n':
                if self.readNextLine():
                    continue
            else:  # 其他字符进入运算符或界符识别
                self.rec_other()

    # 识别空白界符运算符
    def rec_blankBoundaryOperation(self, ch):
        flag = False
        # 判断空白
        if ch == ' ' or ch == '\t' or ch == '\n':
            flag = True
        else:
            # 判断界符
            for key in self.boundary_token:
                if ch == key:
                    flag = True
                    break
            if not flag:
                # 判断运算符
                for key in self.operation_token:
                    if ch == key:
                        flag = True
                        break
        return flag

    # 识别数字
    def rec_dig(self):
        token = 0  # 记录token值
        startIndex = self.index  # 记录初始下标
        state = 0
        # 状态转换阶段
        # 12:科学计数 13:小数 14:整数 15:八进制  16:十六进制 17:出错
        while state < 12 and self.index < len(self.line):
            ch = self.line[self.index]

            if state == 0:
                if ch == '-':
                    state = 1
                elif ch.isdigit() and ch != '0':
                    state = 2
                elif ch == '0':
                    state = 3
                # 0状态在首字符判断是已经确定是数字或负号,不需要再判断其他状况
            elif state == 1:
                if ch.isdigit() and ch != '0':
                    state = 1
                # 当识别到的‘-’不是负号时退出该方法
                elif self.rec_blankBoundaryOperation(ch):   # 单独的'-'识别为减号
                    self.index -= 1
                    return False
                elif ch == '-':   # 识别'--'
                    self.index -= 2
                    return False
                elif ch == '=':   # 识别'-='
                    self.index -= 2
                    return False
                else:
                    state = 11
            elif state == 2:
                if ch.isdigit():
                    state = 2
                elif ch == '.':
                    state = 6
                elif ch == 'e' or ch == 'E':
                    state = 8
                elif self.rec_blankBoundaryOperation(ch):
                    state = 14
                else:
                    state = 11
            elif state == 3:
                if ch == 'x' or ch == 'X':
                    state = 4
                elif ch.isdigit() and ch != '8' and ch != '9' and ch != '0':
                    state = 5
                elif ch == '.':
                    state = 6
                elif self.rec_blankBoundaryOperation(ch):   # 3状态识别到下一个字符为空白时说明读到了0
                    state = 14
                else:
                    state = 11
            elif state == 4:
                if ch.isdigit() or re.search('[a-fA-F]', ch) is not None:
                    state = 4
                elif self.rec_blankBoundaryOperation(ch):
                    state = 16
                else:
                    state = 11
            elif state == 5:
                if ch.isdigit() and ch != '8' and ch != '9':
                    state = 5
                elif self.rec_blankBoundaryOperation(ch):
                    state = 15
                else:
                    state = 11
            elif state == 6:
                if ch.isdigit():
                    state = 7
                else:
                    state = 11
            elif state == 7:
                if ch.isdigit():
                    state = 7
                elif ch == 'e' or ch == 'E':
                    state = 8
                elif self.rec_blankBoundaryOperation(ch):
                    state = 13
                else:
                    state = 11
            elif state == 8:
                if ch == '+' or ch == '-':
                    state = 9
                elif ch.isdigit():
                    state = 10
                else:
                    state = 11
            elif state == 9:
                if ch.isdigit():
                    state = 10
                else:
                    state = 11
            elif state == 10:
                if ch.isdigit():
                    state = 10
                elif self.rec_blankBoundaryOperation(ch):
                    state = 12
                else:
                    state = 11
            elif state == 11:
                if self.rec_blankBoundaryOperation(ch):
                    state = 17
                else:
                    state = 11
            # 继续判断下一字符
            self.index += 1
        # 识别结果
        if state == 17 or state == 11:  # 出错
            token = 0   # 表示错误
            print("当前行: " + str(self.row+1) + "\terror: " + self.line[startIndex:self.index-1])
            self.addWord(self.line[startIndex:self.index-1], str(self.row+1), str(token))
        else:
            token = 400
            print("当前行: " + str(self.row+1) + "\t数值: " + self.line[startIndex:self.index-1] + "\t" + str(token))
            self.addWord(self.line[startIndex:self.index-1], str(self.row+1), str(token))

        # 回退空白符
        self.index -= 1
        return True

    # 识别关键字或标志符
    def rec_id(self):
        token = 0   # 记录token值
        startIndex = self.index  # 记录初始下标
        state = 0
        # 状态转换阶段
        # 2:关键字 3:标志符
        while state < 2 and self.index < len(self.line):
            ch = self.line[self.index]

            if state == 0:
                if ch.isalpha() or ch == "_":
                    state = 1
            elif state == 1:
                if self.rec_blankBoundaryOperation(ch):  # 在读入空白等结束符时再进行判断，避免重复循环判断
                    flag = 0  # 1:关键字 0:标志符
                    for key in self.key_token:
                        if self.line[startIndex:self.index] == key:
                            token = self.key_token[key]
                            flag = 1
                            state = 2
                    if flag == 0:  # 标志符判断
                        state = 3
                else:
                    state = 1
            # 继续判断下一字符
            self.index += 1
        # 识别结果
        if state == 2:  # 关键字
            print("当前行: " + str(self.row+1) + "\t关键字: " + self.line[startIndex:self.index-1] + "\t" + str(token))
            self.addWord(self.line[startIndex:self.index-1], str(self.row+1), str(token))
        else:  # 标志符
            token = 700
            print("当前行: " + str(self.row+1) + "\t标志符: " + self.line[startIndex:self.index-1] + "\t" + str(token))
            self.addWord(self.line[startIndex:self.index-1], str(self.row+1), str(token))
        self.index -= 1

    # 识别注释或除号
    def rec_comment(self):
        state = 0
        # 状态转换阶段
        # 4:多行注释 5:单行注释 6:除号
        while state < 4 and self.index < len(self.line):
            ch = self.line[self.index]

            if state == 0:
                if ch == '/':
                    state = 1
            elif state == 1:
                if ch == '*':
                    state = 2
                elif ch == '/':
                    state = 5
                else:
                    state = 6
                    break
            elif state == 2:
                if ch == '*':
                    state = 3
                else:
                    state = 2
            elif state == 3:
                if ch == '/':
                    state = 4
                else:
                    state = 2
            self.index += 1
            # 读到行尾时读下一行字符串，防越界
            if self.index == len(self.line):
                if not self.readNextLine():
                    return

        # 多行注释直接忽略，不做任何操作

        # 单行注释忽略此行//后的所有内容
        if state == 5:
            if self.readNextLine():
                return
        elif state == 6:  # 不能else，否则多行注释状态会进入此处
            token = 207
            print("当前行: " + str(self.row+1) + "\t界符或运算符: " + self.line[self.index-1] + "\t" + str(token))
            self.addWord(self.line[self.index-1], str(self.row+1), str(token))

    # 识别字符
    def rec_ch(self):
        startIndex = self.index  # 记录初始下标
        state = 0
        # 状态转换阶段
        # 2:完整字符
        while state < 2 and self.index < len(self.line):
            ch = self.line[self.index]
            if state == 0:
                if ch == '\'':
                    state = 1
            elif state == 1:
                if ch == '\'':
                    state = 2
                else:
                    state = 1
            self.index += 1

        if state == 2 and self.index - startIndex - 2 == 1:  # 还有单字符检查
            token = 500
            print("当前行: " + str(self.row+1) + "\t字符: " + self.line[startIndex+1:self.index-1] + "\t" + str(
                token))  # 去掉两边单引号
            self.addWord(self.line[startIndex+1:self.index-1], str(self.row+1), str(token))
        else:
            token = 0
            self.addWord(self.line[startIndex:self.index-1], str(self.row+1), str(token))
            print("当前行: " + str(self.row + 1) + "\terror: " + self.line[startIndex:self.index-1])
            self.index -= 1

    # 识别字符串
    def rec_str(self):
        startIndex = self.index  # 记录初始下标
        state = 0
        # 状态转换阶段
        # 2:完整字符
        while state < 2 and self.index < len(self.line):
            ch = self.line[self.index]

            if state == 0:
                if ch == '\"':
                    state = 1
            elif state == 1:
                if ch == '\"':
                    state = 2
                else:
                    state = 1
            self.index += 1

        if state == 2:
            token = 500
            print("当前行: " + str(self.row+1) + "\t字符串: " + self.line[startIndex+1:self.index-1] + "\t" + str(
                token))  # 去掉两边双引号
            self.addWord(self.line[startIndex+1:self.index-1], str(self.row+1), str(token))
        else:
            token = 0
            self.addWord(self.line[startIndex:self.index-1], str(self.row+1), str(token))
            print("当前行: " + str(self.row + 1) + "\terror: " + self.line[startIndex:self.index-1])
            self.index -= 1

    # 识别运算符、界符
    def rec_other(self):
        startIndex = self.index
        numCh = 1  # 2:双字符 1:单字符 0:错误
        token = 0

        # 双字符判断
        ch = self.line[startIndex:startIndex + 2]
        for key in self.operation_token:
            if ch == key:
                token = self.operation_token[key]
                numCh = 2
                break
        # 单字符判断
        if numCh == 1:
            ch = self.line[self.index]
            for key in self.boundary_token:
                if ch == key:
                    token = self.boundary_token[key]
                    numCh = 1
                    break
            else:
                for key in self.operation_token:
                    if ch == key:
                        token = self.operation_token[key]
                        numCh = 1
                        break
                else:  # 单字符判断也找不到时说明出错
                    numCh = 0
                    ch = self.line[self.index]
                    while not self.rec_blankBoundaryOperation(ch):
                        self.index += 1
                        ch = self.line[self.index]

        if numCh == 0:
            token = 0
            self.addWord(self.line[startIndex:self.index-1], str(self.row+1), str(token))
            print("当前行: " + str(self.row+1) + "\terror: " + self.line[startIndex:self.index])
        elif numCh == 1:
            self.index = startIndex + 1
            print("当前行: " + str(self.row+1) + "\t界符或运算符: " + ch + "\t" + str(token))
            self.addWord(ch, str(self.row+1), str(token))
        elif numCh == 2:
            self.index = startIndex + 2
            print("当前行: " + str(self.row+1) + "\t界符或运算符: " + ch + "\t" + str(token))
            self.addWord(ch, str(self.row+1), str(token))


if __name__ == '__main__':
    lexer = Lexer()
    lexer.start('词法分析用例1.txt')
    pass
