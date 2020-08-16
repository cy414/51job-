#-*- coding = utf-8 -*-
#@Time : 2020/7/26 10:17
#@Author : simintan
#@File : test51job.py
#@Software : PyCharm


from bs4 import BeautifulSoup   #网页解析获取数据
import urllib.request,urllib.error,urllib.parse  #指定url，获取网络数据
import re   #正则表达式-进行文字匹配的
import sys  #删除文件操作
import xlwt #进行excel操作
import _sqlite3 #进行SQLlite数据库操作

#正则匹配规则，以此匹配关键数据，getData函数使用

#findPositionname = re.compile(r'<a href="(.*)">')
findJobname = re.compile(r'"job_name":(.*?),')
findCompanyname = re.compile(r'"company_name":(.*?),')
#findWorkarea = re.compile(r'"workarea_text":(.*?),')
findUpadatetime =re.compile(r'"updatedate":(.*?),')
findCompanytype = re.compile(r'"companytype_text":(.*?),')
findBriefrequests = re.compile(r'"attribute_text":\[(.*?)]')
findJobwelfare = re.compile(r'"jobwelf":(.*?),')
findProvidesalary = re.compile(r'"providesalary_text":(.*?),')
findCompanysize = re.compile(r'"companysize_text":(.*?),')
findDetailmessage = re.compile(r'"job_href":(.*?),')



#<span class="t2"><a href="https://jobs.51job.com/all/co5597496.html" target="_blank" title="中国通信服务股份有限公司">中国通信服务股份有限公司</a></span>
#<a href="https://jobs.51job.com/changsha/120747290.html?s=01&amp;t=0" onmousedown="" target="_blank" title="网络信息安全工程师（中通服项目管理咨询有限公司）">
#                    网络信息安全工程师（中通服项目管理咨询有限公司）                </a>



#得到指定一个URL的网页内容
def askURL(url):
    #ctrl+shift+j 合并为一行
    head = {                                            #头部信息：模拟浏览器头部信息，向51job服务器发送消息
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36"
        "Accept-Language: zh-CN,zh;q=0.9"
        "Accept-Encoding: gzip, deflate, br"
    }                                                   #用户代理：告诉51job我们是什么类型的机器/浏览器，本质上是告诉浏览器我们能接受什么类型的文件

    request = urllib.request.Request(url,headers=head)  #封装出一个request对象
    html = ""
    try:
        response = urllib.request.urlopen(request)      #接受回来的response对象，含有整个网页的信息
        html = response.read().decode("gbk")            #解码整个网页的信息：从51job网页F12查看源码，得知该网站编码为gbk，故以gbk解码
    except urllib.error.URLError as e:                  #可返回未读取到的原因
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)

    return html
def getData(url,city):
    html = askURL(url)
    soup = BeautifulSoup(html, "html.parser")            #使用html解析器解析html对象，形成soup树形结构对象
    #item = soup.findAll(name="script", type="text/javascript")
    #print(soup)
    #item = soup.find_all(lambda tag: tag.name == 'script' and tag.get('type') == ['text/javascript'] and 'id' not in tag.attrs)
    item = soup.find_all(lambda tag: tag.name == 'script' and 'src' not in tag.attrs and 'type' in tag.attrs)   #筛选出便签含有script开头，含有type属性但不含有src属性的内容

    # kk = re.compile(r'<div class="el">(.*?)</div>',re.S)
    # soup = str(soup)
    # item = re.findall(kk,soup)
    #print(item)
    for data in item:
        alldata = []
        partdata = []
        detailmessagelist = []
        it = str(data)
        str1 = city
        cstr = '"' + str(str1) + '"'                                                #得到用户选择的城市，作为数据库表中的第一列
        jobname = re.findall(findJobname,it)
        newjobname = [new.replace('\\', '') for new in jobname]                     #得到匹配、整理后的职位名称
        #print(jobname)
        companyname = re.findall(findCompanyname,it)                                #得到匹配、整理后的公司名称
        #print(companyname)
        # print(workarea)
        updatetime = re.findall(findUpadatetime, it)                                #得到匹配、整理后的招聘信息更新时间
        #print(updatetime)
        companytype = re.findall(findCompanytype, it)                               #得到匹配、整理后的公司类型
        #print(companytype)
        briefrequests = re.findall(findBriefrequests, it)
        newbriefrequests = [new.replace('","', ',') for new in briefrequests]
        newnewbriefrequests = [new.replace('\\', '') for new in newbriefrequests]    #得到匹配、整理后的招聘要求
        #print(briefrequests)
        jobwelfare = re.findall(findJobwelfare, it)
        newjobwelfare = [new.replace(' ', ',') for new in jobwelfare]                #得到匹配、整理后的岗位福利
        #print(jobwelfare)
        providesalary = re.findall(findProvidesalary, it)
        newprovidesalary=[new.replace('\\','')  for new in providesalary]
        newnewprovidesalary = [new.replace('"', '') for new in newprovidesalary]     #得到匹配、整理后的薪水
        #print(newprovidesalary)
        #print(providesalary)
        companysize = re.findall(findCompanysize, it)                                #得到匹配、整理后的公司大小
        #print(companysize)
        detailmessage = re.findall(findDetailmessage, it)
        newdetailmessage = [new.replace('\\', '') for new in detailmessage]          #得到匹配、整理后的岗位详情链接

        for i in range(len(newjobname)):                                             #数字长度即为该页含有的职位信息条数
            partdata.append(cstr)
            partdata.append(newjobname[i])
            partdata.append(newnewbriefrequests[i])
            partdata.append(companyname[i])
            partdata.append(companytype[i])
            partdata.append(companysize[i])
            partdata.append(newjobwelfare[i])
            #print(newprovidesalary[i])
            # 将页面展示的薪资统一单位与X-X千/月
            list = re.split('[-/]', newnewprovidesalary[i])
                #print(len(list))
            #print(newnewprovidesalary[i])
            print("list是%s"%list)
                # s = a.decode('utf-8')  # 举个栗子是字符串s，为了匹配下文的unicode形式，所以需要解码
            if len(list) == 3:
                    part1 = re.split(r'[\u4e00-\u9fa5]',list[1])                       # 这里是精髓，[\u4e00-\u9fa5]是匹配所有中文的正则，因为是unicode形式，所以也要转为ur
                    part2 = re.findall(r'[\u4e00-\u9fa5]', list[1])
                    if (((''.join(part2)) == '元') & ((''.join(list[1])) == '天')):
                        a = (float(''.join(part1[0])) * 30) / 1000
                        b = (float(''.join(part1)) * 30) / 1000
                    elif (((''.join(part2)) == '万') & ((''.join(list[2])) != '年')):
                        a = float(''.join(list[0])) * 10
                        b = float(''.join(part1)) * 10
                    elif (((''.join(part2)) != '万') & ((''.join(list[2])) == '年')):
                        a = float(''.join(list[0])) / 12
                        b = float(''.join(part1)) / 12
                        a = round(a, 2)
                        b = round(b, 2)
                    elif (((''.join(part2)) == '万') & ((''.join(list[2])) == '年')):
                        a = (float(''.join(list[0])) * 10) / 12
                        b = (float(''.join(part1)) * 10) / 12
                        a = round(a, 2)
                        b = round(b, 2)
                    elif (((''.join(part2)) == '元') & ((''.join(list[2])) == '天')):
                        a = (float(''.join(list[0])) * 30) / 1000
                        b = (float(''.join(part1)) * 30) / 1000
                    else:
                        a = float(''.join(list[0]))
                        b = float(''.join(part1))
                    reunion = '"' + str(a) + '-' + str(b) + '千' + '/' + '月' + '"'
                    partdata.append(reunion)
                    compareInt = re.findall('[0-9.]+', reunion)
                    partdata.append('"' + compareInt[0] + '"')
                    partdata.append('"' + compareInt[1] + '"')
            elif len(list) == 2:
                    part1 = re.split(r'[\u4e00-\u9fa5]', list[0])  #
                    part2 = re.findall(r'[\u4e00-\u9fa5]', list[0])
                    print("part1是%s，part2是%s"%(part1,part2))
                    if (((''.join(part2)) == '元') & ((''.join(list[1])) == '天')):
                        a = (float(''.join(part1[0])) * 30) / 1000
                        b = (float(''.join(part1)) * 30) / 1000
                    elif (((''.join(part2) == '万以下') or (''.join(part2)) == '万以上')) & (''.join(list[1]) == '年'):
                        a = (float(''.join(part1)) * 10) / 12
                        b = (float(''.join(part1)) * 10) / 12
                    elif (((''.join(part2)) == '万以上') & ((''.join(list[1])) == '月')):
                        a = float(''.join(part1)) * 10
                        b = float(''.join(part1)) * 10
                    elif (''.join(part2)) == '千以下':
                        a = float(''.join(part1))
                        b = float(''.join(part1))
                    elif (((''.join(part2)) == '万') & ((''.join(list[1])) != '年')):
                        a = float(''.join(list[0])) * 10
                        b = float(''.join(part1)) * 10
                    elif (((''.join(part2)) != '万') & ((''.join(list[1])) == '年')):
                        a = float(''.join(list[0])) / 12
                        b = float(''.join(part1)) / 12
                        a = round(a, 2)
                        b = round(b, 2)
                    elif (((''.join(part2)) == '万') & ((''.join(list[1])) == '年')):
                        a = (float(''.join(list[0])) * 10) / 12
                        b = (float(''.join(part1)) * 10) / 12
                        a = round(a, 2)
                        b = round(b, 2)
                    elif (((''.join(part2)) == '元') & ((''.join(list[1])) == '天')):
                        a = (float(''.join(list[0])) * 30) / 1000
                        b = (float(''.join(part1)) * 30) / 1000
                    elif (((''.join(part2)) == '元') & ((''.join(list[1])) == '小时')):
                        a = (float(''.join(part1)) * 30 * 8 ) / 1000
                        b = (float(''.join(part1)) * 30 * 8) / 1000
                    else:
                        a = float(''.join(list[0]))
                        b = float(''.join(part1))
                    reunion = '"' + str(a) + '-' + str(b) + '千' + '/' + '月' + '"'
                    partdata.append(reunion)
                    compareInt = re.findall('[0-9.]+',reunion)
                    partdata.append('"' + compareInt[0] + '"')
                    partdata.append('"' + compareInt[1] + '"')
            else :
                partdata.append(newprovidesalary[i])
                compareInt = re.findall('[0-9.]+',''.join(newprovidesalary[i]))
                partdata.append("0")
                partdata.append("0")
            #print(part1, part2)
            # print((''.join(part2)),''.join(list[2]))
            # print((''.join(list[2])))
            #print(i,newnewprovidesalary)
            #partdata.append(newprovidesalary[i])
            partdata.append(newdetailmessage[i])
            partdata.append(updatetime[i])
            alldata.append(partdata)                #将一条职位的详情信息汇总至alldata数组，清空partdata等待下一次赋值
            partdata = []
        #len(alldata)
        #print(alldata)
        return alldata
        #print(alldata)
        #print(len(alldata))
        #companyName = re.findall(findCompanyname, it)

        #print(companyName)
        #alldata.append(companyName)
        #print(companyName)
        #print(alldata)



#提供五个可供搜索职位的城市,根据规律将城市转换为对于的URL参数
def getCitycode(city):
    if city == "长沙":
        url = "https://search.51job.com/list/190200,000000,0000,00,9,99,"
    elif city == "北京":
        url = "https://search.51job.com/list/010000,000000,0000,00,9,99,"
    elif city == "上海":
        url = "https://search.51job.com/list/020000,000000,0000,00,9,99,"
    elif city == "成都":
        url = "https://search.51job.com/list/090200,000000,0000,00,9,99,"
    elif city == "深圳":
        url = "https://search.51job.com/list/040000,000000,0000,00,9,99,"
    else:
        print("请重新输入")
        sys.exit(0)
    return url



#得到整个搜索结果的总页数
def getCount(baseurl):
    html = askURL(baseurl)
    # print(html)
    soup = BeautifulSoup(html, "html.parser")
    item = soup.find_all(lambda tag: tag.name == 'script' and 'src' not in tag.attrs and 'type' in tag.attrs)
    # item = soup.find_all(lambda tag: tag.name == 'li' and ('class') in tag.attrs)
    # print(item)
    findPage = re.compile(r'"total_page":(.*?),')
    it = str(item)
    page = re.findall(findPage, it)[0]
    count = eval(page)
    intcount = int(count)
    return intcount


#将数据存入excel表
def saveData2excel(datalist,savepath):
    print("save...")
    workbook = xlwt.Workbook(encoding="utf-8",style_compression=0)  # 创建workbook对象
    worksheet = workbook.add_sheet('51job数据',cell_overwrite_ok=True)  # 创建工作表
    col = ["城市名称", "岗位名称", "招聘条件", "公司名称", "公司类型", "公司规模", "公司福利", "薪酬", "薪酬下限", "薪酬上限", "岗位详情链接", "岗位更新日期"]
    for i in range(12):
        worksheet.write(0,i,col[i]) #列名
    for i in range (len(datalist)): #插入数据的行数
        print("第%d条" %(i+1))
        data = datalist[i]
        for j in range(12):         #插入数据的列数
            worksheet.write(i+1,j,data[j])
    workbook.save(savepath)

#初始化数据库

def init_db(dbpath): #col = ["城市名称","岗位名称","招聘条件","公司名称","公司类型","公司规模","公司福利","薪酬","岗位详情链接","岗位更新日期"]
    # 创建数据库的sql语句
    sql = '''                  
         create table job50
        (
        id integer primary key autoincrement,
        cityname text,
        position text,
        hirecon text,
        cname text,
        ctype text,
        csize text,
        cwelfare text,
        salary text,
        salarylow numeric,
        salaryhigh numeric,
        detaillink text,
        updatetime text
        )

    '''    #创建数据表
    conn = _sqlite3.connect(dbpath)     #创建数据库连接
    cursor = conn.cursor()              #创建游标
    cursor.execute(sql)                 #执行sql语句
    conn.commit()                       #提交结果
    cursor.close()                      #关闭游标
    conn.close()                        #关闭数据库连接



#将数据存至sqllite数据库
def saveData2DB(datalist,dbpath):
    print("...")
    init_db(dbpath)         #初始化数据库
    conn = _sqlite3.connect(dbpath)
    cur = conn.cursor()
    for data in datalist:           #将datalist数据插入数据库中
        sql = '''
                insert into job50
                (cityname,position,hirecon,cname,ctype,csize,cwelfare,salary,salarylow,salaryhigh,detaillink,updatetime)
                values(%s)''' % ",".join(data)
        #print(type(data[4]))
        #print(sql)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()


#得到用户在网页输入的信息
def getInputdata():
    datalist = []
    con = _sqlite3.connect("51jobinput.db")     #连接jobinputdb数据库，取到用户输入信息，供getData函数调用
    cur = con.cursor()
    sql = "select * from job50"
    data = cur.execute(sql)
    print(data)
    for item in data:
        datalist.append(item)
    for item in datalist:
        keyword = item[1]
        city = item[2]
    # keyword = datalist[1]
    cur.close()
    con.close()
    return city,keyword



def main():
    #若须单独执行test51job.py，可将下面四行的注释取消掉，并注释第五行city,keyword = getInputdata()
    # print("请输入想查询的城市")
    # city = input()
    # print("请输入想查询的职位名")
    # keyword = input()
    city,keyword = getInputdata()
    name = urllib.parse.quote(keyword)
    parturl = re.sub('%', "%25", name)
    #newkeyword = parse.quote(name) 这样也可以，51job网站就是对中文字符进行转换再对%进行转换 大转换为%E5%A4%A7再转换为%25E5%25A4%25A7
    baseurl = getCitycode(city) + parturl + ",2,1.html?"    #得到访问的内容，即搜索结果的第一页（首页）
    datalist = []
    for i in range(getCount(baseurl)):                      #得到搜索结果的总页数
         url = (getCitycode(city) + parturl + ",2,%d.html?"%(i+1))  #得到剩余的所有页数
         for data in getData(url,city):
            datalist.append(data)
    #print(datalist)
    savepath = ".\\51job.xls"
    saveData2excel(datalist,savepath)                       #将结果保存至51jon.xls，excel文件
    dbpath = "51job.db"
    saveData2DB(datalist, dbpath)                           #将结果保存至51job.db数据库
    # #print(url)
    # # html = askURL(url)
    # #print(html)
    # getData(url)





if __name__ == "__main__":  #当程序执行时
    #调用函数
    main()
    print("爬取完毕")