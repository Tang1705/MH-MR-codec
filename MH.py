# 码表
MH_BAI_63 = ['00110101', '000111', '0111', '1000', '1011', '1100', '1110', '1111', '10011', '10100', '00111', '01000',
             '001000', '000011', '110100', '110101', '101010', '101011', '0100111', '0001100', '0001000', '0010111',
             '0000011', '0000100', '0101000', '0101011', '0010011', '0100100', '0011000', '00000010', '00000011',
             '00011010', '00011011', '00010010', '00010011', '00010100', '00010101', '00010110', '00010111', '00101000',
             '00101001', '00101010', '00101011', '00101100', '00101101', '00000100', '00000101', '00001010', '00001011',
             '01010010', '01010011', '01010100', '01010101', '00100100', '00100101', '01011000', '01011001', '01011010',
             '01011011', '01001010', '01001011', '00110010', '00110011', '00110100']
MH_BLACK_63 = ['0000110111', '010', '11', '10', '011', '0011', '0010', '00011', '000101', '000100', '0000100',
               '0000101', '0000111', '00000100', '00000111', '000011000', '0000010111', '0000011000', '0000001000',
               '00001100111', '00001101000', '00001101100', '00000110111', '00000101000', '00000010111', '00000011000',
               '000011001010', '000011001011', '000011001100', '000011001101', '000001101000', '000001101001',
               '000001101010', '000001101011', '000011010010', '000011010011', '000011010100', '000011010101',
               '000011010110', '000011010111', '000001101100', '000001101101', '000011011010', '000011011011',
               '000001010100', '000001010101', '000001010110', '000001010111', '000001100100', '000001100101',
               '000001010010', '000001010011', '000000100100', '000000110111', '000000111000', '000000100111',
               '000000101000', '000001011000', '000001011001', '000000101011', '000000101100', '000001011010',
               '000001100110', '000001100111']
MH_BAI_128 = ['11011', '10010', '010111', '0110111', '00110110', '00110111', '01100100', '01100101', '01101000',
              '01100111', '011001100', '011001101', '011010010', '101010011', '011010100', '011010101', '011010110',
              '011010111', '011011000', '011011001', '011011010', '011011011', '010011000', '010011001', '010011010',
              '011000', '010011011']
MH_BLACK_128 = ['0000001111', '00011001000', '000011001001', '000001011011', '000000110011', '000000110100',
                '000000110101', '0000001101100', '0000001101101', '0000001001010', '0000001001011', '0000001001100',
                '0000001001101', '0000001110010', '0000001110011', '0000001110100', '0000001110101', '0000001110110',
                '0000001110111', '0000001010010', '0000001010011', '0000001010100', '0000001010101', '0000001011010',
                '0000001011011', '0000001100100', '0000001100101']

EOL = "000000000001"


# 第一个为64对应的数，以此类推，最后一个代表eol

# 编码
def MH(inpu):
    temp = '0'  # 通常白游程开始 ，用于记忆所扫描的相同字符
    tempnum = 0  # 记忆当前扫描序列的首字符位置
    code = ''  # 存取编码结果
    if inpu[0] == '1':
        # 若开头为1，则为黑游程开始，需要在前面输出黑游程对应为0的码
        # print(MH_BLACK_63[0], end='')
        code += MH_BLACK_63[0]
        temp = '1'

    for num in range(len(inpu)):

        if inpu[num] == temp:
            # 如果当前字符和之前字符相同，则搜寻下一个字符，直到字符不同
            continue

        if num - tempnum < 64:
            # 相同字符格式小于64个情况下
            if temp == '1':
                # 如果为黑游程
                # print(MH_BLACK_63[num-tempnum], end='')
                code += MH_BLACK_63[num - tempnum]
            else:
                # 如果为白游程
                # print(MH_BAI_63[num-tempnum], end='')
                code += MH_BAI_63[num - tempnum]
        else:
            # 在相同字符大于64情况下，需要加组合基于码
            rank = int((num - tempnum) / 64) - 1
            if temp == '1':
                # print(MH_BLACK_128[rank], end='')
                code += MH_BLACK_128[rank]
                # print(MH_BLACK_63[(num - tempnum) % 64], end='')
                code += MH_BLACK_63[(num - tempnum) % 64]
            else:
                # print(MH_BAI_128[rank], end='')
                code += MH_BAI_128[rank]
                # print(MH_BAI_63[(num - tempnum) % 64], end='')
                code += MH_BAI_63[(num - tempnum) % 64]
        # 更新信息
        temp = inpu[num]
        tempnum = num

    # 输出最后一串
    if num - tempnum + 1 < 64:

        if temp == '1':
            # print(MH_BLACK_63[num-tempnum+1], end='')
            code += MH_BLACK_63[num - tempnum + 1]
        else:
            # print(MH_BAI_63[num-tempnum+1], end='')
            code += MH_BAI_63[num - tempnum + 1]
    else:
        rank = int((num - tempnum + 1) / 64) - 1
        if temp == '1':
            # print(MH_BLACK_128[rank], end='')
            code += MH_BLACK_128[rank]
            # print(MH_BLACK_63[(num - tempnum+1) % 64], end='')
            code += MH_BLACK_63[(num - tempnum + 1) % 64]
        else:
            # print(MH_BAI_128[rank], end='')
            code += MH_BAI_128[rank]
            # print(MH_BAI_63[(num - tempnum+1) % 64], end='')
            code += MH_BAI_63[(num - tempnum + 1) % 64]
    return code


def Search(src, MH):
    # 用于判断数组中是否包含给定的字符串
    if src in MH:
        # return True
        return MH.index(src)
    else:
        return False


def output(number, char, code_trans):
    # 用于输出记录解码结果
    for i in range(number):
        # print(char, end='')
        code_trans += char
    return code_trans


def SearchAll(src, temp):
    # 用于判断在数组中是否有相同的字符出现
    a = 0
    if temp == '1':
        if src in MH_BLACK_63:
            a += 1
        if src in MH_BLACK_128:
            a += 1
    else:
        if src in MH_BAI_63:
            a += 1
        if src in MH_BAI_128:
            a += 1
    if a == 0:
        return True
    else:
        return False


# 解码
def MH_trans(code):
    code_trans = ''  # 记忆解码结果
    temp = '0'  # 记忆当前所扫描的游程类型
    tempnum = 0  # 记忆当前扫描序列的首字符位置
    if code[0:10] == MH_BLACK_63[0]:
        # 即黑游程为开始
        temp = '1'
        tempnum = 10
    for num in range(len(code)):
        if num < tempnum:
            # 即此时为黑游程开始，则前10个字符代表结尾码中黑游程对应的长度为0的码，可以直接忽略
            continue
        if SearchAll(code[tempnum:num], temp):
            continue
        if temp == '1':
            # 判断是否存在组合基于码，如果存在，则先输出组合基于码对应的解码，再继续遍历寻找结尾码并输出。否则直接输出结尾码
            if code[tempnum:num] in MH_BLACK_128:
                youchen_128 = Search(code[tempnum:num], MH_BLACK_128)
                code_trans = output(youchen_128 * 64 + 64, '1', code_trans)
                temp = '1'
                tempnum = num
            else:
                youchen_64 = Search(code[tempnum:num], MH_BLACK_63)
                code_trans = output(youchen_64, '1', code_trans)
                temp = '0'
                tempnum = num
        else:
            # 判断是否存在组合基于码，如果存在，则先输出组合基于码对应的解码，再继续遍历寻找结尾码并输出。否则直接输出结尾码
            if code[tempnum:num] in MH_BAI_128:
                youchen_128 = Search(code[tempnum:num], MH_BAI_128)
                code_trans = output(youchen_128 * 64 + 64, '0', code_trans)
                temp = '0'
                tempnum = num
            else:
                youchen_64 = Search(code[tempnum:num], MH_BAI_63)
                code_trans = output(youchen_64, '0', code_trans)
                temp = '1'
                tempnum = num

    # 用于输出解码最后的结果,由于for循环的限制，无法对最后的字符串进行解码，故再对最后的字串需要解码一次
    num += 1
    if temp == '1':
        # 黑游程，编码中，由于是组合基于码+结尾码，或者直接为结尾码，故最后的码必定为结尾码，只需对结尾码进行生成即可
        youchen_64 = Search(code[tempnum:num], MH_BLACK_63)
        code_trans = output(youchen_64, '1', code_trans)

    else:
        # 白游程，编码中，由于是组合基于码+结尾码，或者直接为结尾码，故最后的码必定为结尾码，只需对结尾码进行生成即可

        youchen_64 = Search(code[tempnum:num], MH_BAI_63)
        # print(youchen_64)
        code_trans = output(youchen_64, '0', code_trans)

    return code_trans


def makejpg(binary):
    strjpg = []
    for i in range(binary.shape[0]):
        strjpg.append('')
        for j in range(binary.shape[0]):
            if binary[i][j] >= 200:
                strjpg[i] += '1'
            else:
                strjpg[i] += '0'

    # strjpg中，分别存取图像中的每一行数据
    code = []
    for i in range(binary.shape[0]):
        code.append(MH(strjpg[i]))

    code_trans = []
    for i in range(binary.shape[0]):
        code_trans.append(MH_trans(code[i]))
        if len(code_trans[i]) != 256:
            print(str(i) + ':' + str(len(code_trans[i])))
    # print(strjpg[228])
    # print(code[228])
    # print(code_trans[99])
    # print(MH(code_trans[99]))
    binary_trans = []
    for i in range(binary.shape[0]):
        temp = []
        # print(i)
        for j in range(len(code_trans[i])):
            # print(j)
            if code_trans[i][j] == '1':
                temp.append(255)
            else:
                temp.append(0)
        binary_trans.append(temp)

    return code, code_trans, binary_trans


def MH_trans_in_MR(inpu, youchen, boolshouwei):
    # 用于在MR解码中的MH解码,此处解码较为特殊，每次只解一种字符，并且需要验证判断是否大于64位。
    # 同时，如果检索到组合基于码，还需要继续检索结尾码，并且该处属于同义词MH解码
    # 因此，要先判断是否存在组合基于码，如果存在，则需要继续搜索剩余的结尾码
    # 第二个返回值代表是否匹配到序列，第三个返回值代表是否需要继续搜索结尾码-
    code_trans = ''
    if youchen == '0':

        if inpu in MH_BAI_128:
            return output(MH_BAI_128.index(inpu) * 64 + 64, youchen, code_trans), True, True, False

        if inpu in MH_BAI_63:
            return output(MH_BAI_63.index(inpu), youchen, code_trans), True, False, False

    if youchen == '1':
        # 当其为黑游程开始时，由于MH编码的特性，在黑游程开始前会加入一串字符MH_BLACK_63[0]表示黑游程开始，但这串字符并无意义，故需要去掉
        # 这里可以考虑，当其搜到到MH_BLACK_63[0]时，需要继续进行一次搜索，但是当只有64个1像素时，此时依然后会搜索到MH_BLACK_63[0]，并且不需要继续搜索，
        # 因此，这里只能通过增加返回值，来表示是最前面的MH_BLACK_63[0]还是最后的MH_BLACK_63[0]默认为TRUE，只有经过128位的查找之后才会变为FALSE
        if inpu in MH_BLACK_128:
            return output(MH_BLACK_128.index(inpu) * 64 + 64, youchen, code_trans), True, True, False

        if inpu in MH_BLACK_63:
            if boolshouwei == True:
                if inpu == MH_BLACK_63[0]:
                    return output(MH_BLACK_63.index(inpu), youchen, code_trans), True, True, False
            return output(MH_BLACK_63.index(inpu), youchen, code_trans), True, False, False

    return 0, False, 0, boolshouwei


# print(makejpg())

if __name__ == "__main__":
    # inpu = input('输入传输的内容:(0代表白游程，1代表黑游程，从白游程开始) ')

    inpu = '11100011100011111'
    code = MH(inpu)
    print(code)
    code_trans = MH_trans(code)
    print(code_trans)