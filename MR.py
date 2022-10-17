from MH import MH, MH_trans, SearchAll, MH_trans_in_MR


# 上面两个函数分别是指 MH编码 和 MH解码

def bianma(a0, a1, a2, b1, b2, inpu2, code):
    # 通过各个元素的位置，输出编码以及a0的位置
    if a1 > b2:
        # print('0001', end=' ')
        code += '0001'
        return b2, code
    else:
        a1b1 = a1 - b1
        if a1b1 == 0:
            # print('1', end=' ')
            code += '1'
            return a1, code
        elif a1b1 == 1:
            # print('011', end=' ')
            code += '011'
            return a1, code
        elif a1b1 == 2:
            # print('000011', end=' ')
            code += '000011'
            return a1, code
        elif a1b1 == 3:
            # print('0000011', end=' ')
            code += '0000011'
            return a1, code
        elif a1b1 == -1:
            # print('010', end=' ')
            code += '010'
            return a1, code
        elif a1b1 == -2:
            # print('000010', end=' ')
            code += '000010'
            return a1, code
        elif a1b1 == -3:
            # print('0000010', end=' ')
            code += '0000010'
            return a1, code
        else:
            # 此时对应a1b1之间的距离大于3
            # print('001' + MH(inpu2[a0:a1]) + MH(inpu2[a1:a2]), end=' ')

            # 此时，如果以白游程开始，并且判定为水平模时，由于a0为-1位置，则获取不到该元素，a0实际代表白游程。故这里修改为当a0为-1是，前一段编码为0+0到a1位置的元素进行编码
            if a0 == -1:
                code += '001' + MH('0' + inpu2[:a1]) + MH(inpu2[a1:a2])
            else:
                code += '001' + MH(inpu2[a0:a1]) + MH(inpu2[a1:a2])
            return a2, code


def search(inpu, a1):
    # 在inpu序列中，找与a1的下一个迁移像素a2，a2与a1颜色相反
    # 迁移元素必须是由黑变白或者由白变黑的第一个元素
    if a1 == -1:
        # 即对应第一个为白元素的情况下,才会执行这句
        a1 = 0

    if a1 == len(inpu):
        return len(inpu)

    a2 = len(inpu)

    temp = inpu[a1]
    # print('search开始' + ',a1:' + str(a1)  + ',temp:' + temp)
    for i in range(a1, len(inpu)):
        if inpu[i] != temp:
            # print('i:'+str(i)+',a1:' + str(a1) + ', inpu[i]:' + inpu[i]+',temp:'+temp)
            a2 = i
            break

    return a2


def searchcankao(inpu1, inpu2, a1):
    # inpu1代表参考行
    # inpu2代表编码行
    if a1 == len(inpu2):
        return len(inpu2)
    a2 = len(inpu1)
    temp = inpu2[a1]

    for i in range(a1 + 1, len(inpu1)):
        # 由于迁移元素表示由黑变白或由白变黑的第一个元素，因此不能单纯的从a1开始只找与a1不同的元素
        # 这里可以考虑从a1-1出发遍历，如果某元素与a1对应的元素不同，且与其上一个元素也不同，则可以认定为迁移元素
        # 即先看上一个元素和当前元素颜色是否不同，若不同再看a1对应的颜色和当前元素颜色是否不同
        if inpu1[i - 1] != inpu1[i]:
            if temp != inpu1[i]:
                a2 = i
                break
    return a2


# 通常扫描行第一个元素为白游程，若为黑游程则让a0为第一个元素之前

# inpu1 代表参考行
# inpu2 代表编码行
def MR(inpu1, inpu2):
    a0 = -1  # a0是假想的白元素，将a0置于第一个元素之前
    code = ''
    if inpu2[0] == '1':
        # 即第一个为黑游程的情况下
        a1 = 0
        a2 = search(inpu2, a1)
        i = 0
        for i in range(len(inpu1)):
            if inpu1[i] == '1':
                break
        b1 = i
        # 防止参考行均为0情况下，找不到b1的位置
        b2 = search(inpu1, b1)
        print('a0:' + str(a0) + ',a1:' + str(a1) + ',a2:' + str(a2) + ',b1:' + str(b1) + ',b2:' + str(b2))
        a0, code = bianma(a0, a1, a2, b1, b2, inpu2, code)
    else:
        # 即对应第一个为白元素的情况下
        a1 = search(inpu2, a0)
        a2 = search(inpu2, a1)
        i = 0
        for i in range(len(inpu1)):
            if inpu1[i] == '1':
                break
        b1 = i
        # 防止参考行均为0情况下，找不到b1的位置
        b2 = search(inpu1, b1)
        # print('a0:' + str(a0) + ',a1:' + str(a1) + ',a2:' + str(a2) + ',b1:' + str(b1) + ',b2:' + str(b2))
        a0, code = bianma(a0, a1, a2, b1, b2, inpu2, code)
    while 1:

        if a0 == len(inpu2):
            # 结束编码行编码
            break
        # 更新过程
        a1 = search(inpu2, a0)
        a2 = search(inpu2, a1)
        b1 = searchcankao(inpu1, inpu2, a0)
        # print('b1b2开始')
        b2 = search(inpu1, b1)
        # print('a0:' + str(a0) + ',a1:' + str(a1) + ',a2:' + str(a2) + ',b1:' + str(b1) + ',b2:' + str(b2))
        a0, code = bianma(a0, a1, a2, b1, b2, inpu2, code)
    return code
    # code 代表编码行的编码


def output(num, youchen):
    # num代表输出的数量，youchen代表当前输出是0还是1
    code_trans = ''
    for i in range(num):
        code_trans += youchen
    return code_trans


def searchcode(inpu1, src, a0, b1, b2, code_trans, youchen):
    # inpu1代表参考行，src代表当前选取的子序列，
    # 返回值：
    # code_trans代表复原的码，第二个代表游程是否改变，第三个代表是否搜索完毕
    # 通过搜索码字，确定a1、a2的位置
    if src == '1':
        # 对应a1等于b1的情况，
        code_trans += output(b1 - a0, youchen)
        return code_trans, True, True
    elif src == '011':
        code_trans += output(b1 + 1 - a0, youchen)
        return code_trans, True, True
    elif src == '000011':
        code_trans += output(b1 + 2 - a0, youchen)

        return code_trans, True, True
    elif src == '0000011':
        code_trans += output(b1 + 3 - a0, youchen)
        return code_trans, True, True
    elif src == '010':
        code_trans += output(b1 - 1 - a0, youchen)
        return code_trans, True, True
    elif src == '000010':
        code_trans += output(b1 - 2 - a0, youchen)
        return code_trans, True, True
    elif src == '0000010':
        code_trans += output(b1 - 3 - a0, youchen)
        return code_trans, True, True
    elif src == '0001':
        code_trans += output(b2 - a0, youchen)
        # 这是游程不发生转变
        return code_trans, False, True
    else:
        return code_trans, False, False
    # 对于水平模的情况，直接在父函数中判别


def bianmaa1b1(a1, b1):
    # 初步判断
    code = ''
    a1b1 = a1 - b1
    if a1b1 == 0:
        # print('1', end=' ')
        code += '1'
        return code
    elif a1b1 == -1:
        # print('010', end=' ')
        code += '010'
        return code
    elif a1b1 == -2:
        # print('000010', end=' ')
        code += '000010'
        return code
    elif a1b1 == -3:
        # print('0000010', end=' ')
        code += '0000010'
        return code
    else:
        # 此时对应a1b1之间的距离大于3
        # print('001' + MH(inpu2[a0:a1]) + MH(inpu2[a1:a2]), end=' ')
        code += '001'
        return code


def youchen_change(youchen):
    # 该youchen函数
    if youchen == '0':
        return '1'
    else:
        return '0'


def searchyouchen(inpu, a0, youchen):
    # 得到inpu下一个迁移像素的位置，该迁移像素与youchen的颜色相反
    b1 = len(inpu)
    for i in range(a0 + 1, len(inpu)):
        if inpu[i - 1] != inpu[i]:
            if inpu[i] != youchen:
                b1 = i
                break
    return b1


# 解码


def MR_trans(inpu1, code):
    # 通过搜索码字，确定a1、a2的位置，结合a0的位置，从而确定0,1的个数
    # 解码中，需要记录当前a0的位置(即以及解码好了的的字符的长度），b1、b2的位置由ao的位置获得
    # 首先要判断，该行是由白游程开始还是黑游程开始，具体的判断方法是:通过读取前面的码字，判断编码的模式，从而得到a1和b1的相对位置关系，而由参考行可以得到b1的位置，从而测定得到a1的位置
    #   若a1的位置为0，代表由黑游程开始，若a1位置不为0，代表由白游程开始。
    #   反向考虑，当且仅当a1位置为0时，为黑游程开始，基于此，可以简化运算，即得到b1的位置后，假定a1的位置为0，那么对于其相对位置关系可以得到的模式以及对应的码字，再判断改行码字前面与其是否匹配，
    #   若匹配，则为黑游程开始，若不匹配，则必定为白游程开始。
    #   在该假设的前提下，a1<=b1，则可以将其判断的模式范围缩小
    youchen = '0'
    tempnum = 0  # 记忆当前判断码字的初始位置
    code_trans = ''
    a0 = -1
    i = 0
    for i in range(len(inpu1)):
        if inpu1[i] == '1':
            break
    b1 = i
    b2 = search(inpu1, b1)
    # a1 = 0
    # a1b1 = bianmaa1b1(a1, b1)
    # if code[0:len(a1b1)] == a1b1:
    #     # 即此时对应为开始为黑游程的情况
    #     youchen = '1'
    #     print('qwe')

    i = 1
    while a0 < len(inpu1):

        # print(src)
        src = code[tempnum:i]
        # print('src:'+src+',a0:'+str(a0)+',a0:'+str(a0)+',b1:'+str(b1)+',b2:'+str(b2)+',code_trans:'+str(code_trans) + ',youchen:'+str(youchen))
        code_trans, boolyouchen, boolsuccess = searchcode(inpu1, src, a0, b1, b2, code_trans, youchen)
        if boolsuccess == False:
            if src == '001':
                # 此时代表为水平模,需要进行两次MH编码
                # 由于这里MH编码不是简单的MH解码，需要是固定白或者黑游程确定
                # 第一次搜索
                j = i + 2
                # print(i)
                while 1:
                    srcmh = code[i: j]
                    # print(str(srcmh)+','+youchen)
                    boolshouwei = True
                    out, bool1, bool2, boolshouwei = MH_trans_in_MR(srcmh, youchen, boolshouwei)
                    # 第二个返回值代表是否匹配到序列，第三个返回值代表是否需要继续搜索结尾码
                    if not bool1:
                        j += 1
                        continue
                    else:
                        # 此时代表成功搜索到字符
                        code_trans += out
                        if bool2:
                            # 此时代表需要继续搜索结尾码
                            i = j
                            j = i + 2
                            continue
                        else:
                            break

                # 第二次搜索
                i = j
                j = i + 2
                while 1:
                    srcmh = code[i: j]
                    # print(srcmh+','+youchen_change(youchen))
                    boolshouwei = True
                    out, bool1, bool2, boolshouwei = MH_trans_in_MR(srcmh, youchen_change(youchen), boolshouwei)
                    # 第二个返回值代表是否匹配到序列，第三个返回值代表是否需要继续搜索结尾码
                    if not bool1:
                        j += 1
                        continue
                    else:
                        # 此时代表成功搜索到字符
                        code_trans += out
                        if bool2:
                            # 此时代表需要继续搜索结尾码
                            i = j
                            j = i + 2
                            continue
                        else:
                            break

                tempnum = j
                i = tempnum + 1
                a0 = len(code_trans) - 1
                b1 = searchyouchen(inpu1, a0, youchen)
                b2 = search(inpu1, b1)
                continue
            else:
                # 此时对应当前码字未搜索到需要的码
                i = i + 1
                a0 = len(code_trans) - 1
                continue
        else:
            # 此时对应搜索编码成功的情况
            if boolyouchen == True:
                # 此时游程发生改变
                youchen = youchen_change(youchen)
            a0 = len(code_trans) - 1
            b1 = searchyouchen(inpu1, a0, youchen)
            b2 = search(inpu1, b1)
            tempnum = i
            i = i + 1
            # print(a0)

    return code_trans[1:]


def makejpgMR(binary):
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
    code.append(MH(strjpg[0]))  # 第一行进行MH编码
    for i in range(1, binary.shape[0]):
        code.append(MR(strjpg[i - 1], strjpg[i]))  # 以i-1行为参考编i行

    code_trans = []
    code_trans.append(MH_trans(code[0]))  # 第一行进行MH解码
    for i in range(1, binary.shape[0]):
        code_trans.append(MR_trans(code_trans[i - 1], code[i]))  # 以前一行解出来的码为参考行，对下一行进行解码
        if code_trans[i] != strjpg[i]:
            print(str(i) + ':' + str(len(code_trans[i])))
            print(strjpg[i - 1])
            print(strjpg[i])
            print(code[i])
            print(code_trans[i])
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


if __name__ == "__main__":
    # inpu1 = '001011101001010000'  # 参考行
    # inpu2 = '000101101011010000'  # 编码行

    inpu1 = '11100011100011111'
    inpu2 = '10000111110000001'
    code = MR(inpu1, inpu2)
    print(code)
    