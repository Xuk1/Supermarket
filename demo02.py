fname = "data.txt"                      #存储商品种类，名称和库存的文件
finame = "details.txt"                  #存储商品名，编号，价格，保质期的文件

goodsnm = []                            #按顺序存放details文件中商品名称
code = []                               #按顺序存放对于编号
prices = []                             #按顺序存放对应价格
date = []                               #按顺序存放对于保质期
f = open(finame, "r+")
for line in f:
    tmp_data = eval(line)
    goodsnm.append(tmp_data[0])
    code.append(tmp_data[1])
    prices.append(tmp_data[2])
    date.append(tmp_data[3])
f.close()

#主函数
def main():
    j = 0
    print("0：顾客")
    print("1：管理员")
    choice = eval(input("请选择您是顾客还是管理员："))
    if choice == 0:                     #如果输入choice为0，则使用顾客函数
        customer(fname, finame)
    elif choice == 1:                   #如果输入choice为1，则使用管理员函数
        for i in range(3):              #判断管理员账号是否能够登录，如果能，才执行管理员函数
            f = open("password.txt", "r+")
            name = input("用户名：")
            password = eval(input("密码："))
            for line in f:
                tmp_id = eval(line)
                if tmp_id.__contains__(name) and password == tmp_id[name]:
                    j = 1
                    break
            f.close()
            if j == 1:
                manager(fname, finame)
                break
            elif j == 0:
                print("用户名或密码错误！")

#得到种类名称函数
def getSort(fname):
    sort = []  #存储种类名称
    f = open(fname, "r+")  #打开数据文件
    for line in f:  #获得种类列表
        sort.append(line.split("-")[0])
    f.close()
    return sort

#查询函数
def query(sort, fname, goodsnm, code, prices, date):
    number = [] #存放商品数量
    for sortname in sort:  #打印所有种类
        print(sortname)
    while True:
        k = -1
        judge = [] #存储文件到第几行满足条件
        f = open(fname, "r+")
        tmp_sort = input('\n'"请输入查询的种类(输入数字0退出):")
        input_sort = [] #存放用户输入种类
        if tmp_sort in sort or tmp_sort == '0':
            if (tmp_sort) == '0':
                break
            else:
                input_sort.append(tmp_sort)
            for line in f:
                k += 1
                for i in range(len(input_sort)):
                    if line.split("-")[0] == input_sort[i]:
                        print("要查询的种类下所有商品库存如下：{}".format(line.split("-")[1]), end = '')
                        judge.append(k)
            for j in range(len(judge)):
                for i in range(5*judge[j], 5*(judge[j]+1)):
                    print("商品:{}       编号:{}      价格:{}      保质期:{}".format(goodsnm[i], code[i], prices[i], date[i]))
        else:
            print("输入种类不存在！")
        f.close()

#输入购买清单
def inputBuyList():
    try: #限制输入格式只能为字典类型
        input_buylist = eval(input('\n' "请输入要购买的商品名称和数量（格式为{商品名称: 数量}）："))
        return input_buylist
    except:
        print("输入格式错误！" '\n')

#输出购物清单函数
def buyList(input_buylist, prices, goodsnm, code):
    total = 0 #计算购买商品总价
    output = [] #存放输出语句
    for ky in input_buylist.keys():
        for i in range(len(goodsnm)):
            if ky == goodsnm[i]:
                a = goodsnm.index(ky)
                total += prices[a]*input_buylist[ky]
                output.append(code[a])
                output.append('\t')
                output.append(ky)
                output.append(':')
                output.append(prices[a])
                output.append(' *')
                output.append(input_buylist[ky])
                output.append('\n')
    print("————————购物清单————————")
    for i in range(len(output)):
        print(output[i], end = '')
    print("总计:{}".format(total))

#调整库存函数
def inventory(input_buylist, fname):
    f = open(fname, "r+")
    output_lines = [] #存放输出语句
    for line in f:
        ls = eval(line.split("-")[1])
        for lsname in ls.keys():
            for name in input_buylist.keys():
                if name == lsname:
                    ls[lsname] -= input_buylist[name]
        ls_head = line.split("-")[0]
        output_lines.append(ls_head +'- '+ str(ls) + '\n')
    f.close()
    f =  open(fname,"w")
    f.writelines(output_lines)
    f.close()
    print("库存调整完成！")

#顾客函数
def customer(fname, finame):
    sort = getSort(fname)
    query(sort, fname, goodsnm, code, prices, date)
    input_buylist = inputBuyList()
    buyList(input_buylist, prices, goodsnm, code)
    inventory(input_buylist, fname)

#上架商品函数
def add(fname):
    while True:
        input_good = [] #用于存储上架的商品名
        input_number = [] #用于存储上架的商品数量
        addgoods = {} #用于存储{商品名称: 上架数量}
        output_lines = []
        input_good = []
        input_sort = input("请输入上架商品的种类(输入是数字0退出)：")
        if input_sort == '0':
            break
        else:
            print("请输入上架的商品名称(输入数字0退出):")
            while True:
                tmp_good = input()
                if tmp_good == '0':
                    break
                input_good.append(tmp_good)
            print("请输入上架商品对应的数量(输入数字0退出):")
            while True:
                tmp_number = eval(input())
                if tmp_number == 0:
                    break
                input_number.append(tmp_number)
            for i in range(len(input_good)):
                addgoods[input_good[i]] = input_number[i]
            f = open(fname, "r+")
            i = 0
            for line in f:
                if line == "\n":
                    break
                tmp_dict = eval(line.split("-")[1])
                if input_sort == line.split("-")[0]:
                    for i in range(len(input_good)):
                        tmp_dict[input_good[i]] += input_number[i]
                output_lines.append(line.split("-")[0] +'- '+ str(tmp_dict) + '\n')
                i += 1
            f.close()
            f = open(fname, "w")
            f.writelines(output_lines)
            f.close()
            print("上架已完成！")

#下架商品函数
def reduce(fname):
    input_good = [] #用于存储下架的商品名
    input_number = [] #用于存储下架的商品数量
    while True:
        f = open(fname, "r+")
        sort_find = False
        reducegoods = {} #用于存储{商品名称: 下架数量}
        output_lines = [] #用于存储打印的语句
        input_sort = input("请输入下架商品的种类(输入数字0退出):")
        if input_sort == '0':
            break
        else:
            print("请输入下架的商品名称(输入数字0退出):")
            for line in f:
                tmp_dict = eval(line.split("-")[1])
                if line.split("-")[0] == input_sort:
                    sort_find = True
                    tmp_goods = []
                    tmp_numbers = []
                    while True: #存储商品名称
                        tmp_good = input()
                        if tmp_good == '0':
                            break
                        tmp_goods.append(tmp_good)
                    print("请输入下架商品对应的数量(输入数字0退出):")
                    while True: #存储商品数量
                        tmp_number = eval(input())
                        if tmp_number == 0:
                            break
                        tmp_numbers.append(tmp_number)
                    if len(tmp_goods) != len(tmp_numbers): #比较商品数目和商品数量是否相等
                        print("输入商品数量和商品数目不匹配")
                        continue
                    for i in range(len(tmp_numbers)): 
                        if tmp_dict[tmp_goods[i]] - tmp_numbers[i] >= 0: #当操作后商品数量>0的时候才能继续操作
                            tmp_dict[tmp_goods[i]] -= tmp_numbers[i] 
                        else:
                            print("该商品已没有库存无法减少")
                output_lines.append(line.split("-")[0] +'- '+ str(tmp_dict) + '\n')
            if not sort_find:
                print("无法找到该商品种类")
            f.close()
            f = open(fname, "w")
            f.writelines(output_lines)
            f.close()
    print("下架已完成！")

#显示库存为0的商品，并提醒管理员上架的函数 - 提醒函数
def notice(fname):
    f = open(fname, "r")
    for line in f:
        tmp = eval(line.split("-")[1])
        for ky in tmp.keys():
            if tmp[ky] == 0:
                print("商品:{}需要补货！".format(ky))
    
#管理员函数
def manager(fname, finame):
    notice(fname)
    print("0：上架商品")
    print("1：下架商品")
    while True:
        goon = input("是否继续上/下架商品(输入数字1继续):")
        if goon != '1':
            break
        else:
            choice = eval(input("选择上/下架商品："))
            if choice == 0:
                add(fname)
            elif choice == 1:
                reduce(fname)

main()
input("Press any key to exit...")
