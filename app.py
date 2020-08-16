from flask import Flask,render_template,request #render_emplate使程序可以返回一个网页模板，rquest把用户表单信息封装好了，以待传递
import os       #删除文件，运行文件
import _sqlite3 #sqlite3数据库操作
import jieba    #分词
from matplotlib import pyplot as plt    #绘图功能
from wordcloud import WordCloud         #词云
from PIL import Image                   #图片处理
import numpy as np                      #矩阵运算

#运行前先在pycharm将flaskdebug模式打开
app = Flask(__name__)

@app.route('/')
def home():
    #return render_template('index.html')
    return render_template('index.html')
@app.route('/',methods=['POST'])     #捕捉用户对/目录发起的post提交请求
def index():
    if request.method == 'POST':
        if os.path.exists(r'51job.db'):
            os.remove(r'51job.db')  #在每次搜索前删除上一次搜索创建的文件
            os.remove(r'51job.xls')
            os.remove(r'51jobinput.db')
        result = request.form      #将网页表格中的所有内容形成一个字典
        list = []
        for value in result.values():
            list.append(value)
        print(list)
        sql1 = '''
                create table job50
                (
                id integer primary key autoincrement,
                keyword text,
                cityname text
                )

            '''  # 创建数据表
        conn = _sqlite3.connect("51jobinput.db")
        cursor = conn.cursor()
        cursor.execute(sql1)
        conn.commit()
        conn.close()
        conn1 = _sqlite3.connect("51jobinput.db")
        cur1 = conn1.cursor()
        sql = '''
                insert into job50
                (keyword,cityname)
                values('%s','%s')''' %(list[0],list[1])
        cur1.execute(sql)
        conn1.commit()
        cur1.close()
        conn1.close()
        os.system("python test51job.py")        #运行爬虫程序

    return position()



@app.route('/index')
def homepage():
    #return render_template('index.html')
    return render_template('index.html')

@app.route('/position')
def position():
    datalist = []
    con = _sqlite3.connect("51job.db")
    cur = con.cursor()
    sql = "select * from job50 order by salarylow desc,salaryhigh desc"
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)
    cur.close()
    con.close()
    return render_template('position.html',positions = datalist)    #返回position.html返回至用户浏览页，并将datalist赋值给positions，将positions变量传递至position.html

@app.route('/salary')
def salary():
    list = []
    num = []
    con = _sqlite3.connect("51job.db")
    cur = con.cursor()
    #字符串前加入labelx，帮助进行文本排序
    sql = '''
select count(1),(CASE WHEN salarylow is 0 then 'label1 薪酬待协商'
WHEN salarylow between 1 and 5 then 'label2 5k以下'
WHEN salarylow between 5 and 8 then 'label3 5k-8k'
WHEN salarylow between 8 and 10 then 'label4 8k-10k'
WHEN salarylow between 10 and 13 then 'label5 10k-13k'
WHEN salarylow between 13 and 18 then 'label6 13k-18k'
WHEN salarylow between 18 and 25 then 'label7 18k-25k'
ELSE  'label8 25k以上'
end)
from job50 group by(CASE WHEN salarylow is 0 then 'label1 薪酬待协商'
WHEN salarylow between 1 and 5 then 'label2 5k以下'
WHEN salarylow between 5 and 8 then 'label3 5k-8k'
WHEN salarylow between 8 and 10 then 'label4 8k-10k'
WHEN salarylow between 10 and 13 then 'label5 10k-13k'
WHEN salarylow between 13 and 18 then 'label6 13k-18k'
WHEN salarylow between 18 and 25 then 'label7 18k-25k'
ELSE  'label8 25k以上'
end);

    '''
    data = cur.execute(sql)
    for item in data:
        num.append(item[0])
        str = ''.join(item[1])
        st = str[6:]                #移除orderby排序使用的labelx
        list.append(st)
    print(num,list)
    cur.close()
    con.close()
    return render_template('salary.html',num=num,list=list)


@app.route('/keyword')
def keyword1():
    #清除上次搜索产生的word图片
    if os.path.exists(r'.\static\pic\word.jpg'):
        os.remove(r'.\static\pic\word.jpg')
    # 准备词云的词
    con = _sqlite3.connect('51job.db')
    cur = con.cursor()
    sql = 'select distinct  cwelfare from job50'
    data = cur.execute(sql)
    text = ""
    for item in data:
        text = text + item[0]
    cur.close()
    con.close()
    #分词
    cut = jieba.cut(text)
    string = ''.join(cut)

    img = Image.open(r'.\static\pic\tree.jpg') #打开遮罩图片
    img_array = np.array(img) #将图片转为数组
    #生成词云对象
    wc = WordCloud(
        background_color='white',   #输出图片的颜色
        mask = img_array,   #进行遮罩的图片
        font_path="STXINGKA.TTF"    #字体位置在C:\Windows\Fonts
    )
    wc.generate_from_text(string)


    #绘制图片
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off') #是否显示坐标轴
    #plt.show()     #显示生成的词云图片
    #输出词云图片到文件
    plt.savefig(r'.\static\pic\word.jpg',dpi=2000)

    return render_template('keyword.html')
if __name__ == '__main__':
    app.run()
