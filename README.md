# 51job-spider
使用Python爬虫（基于岗位关键字+城市静态爬取）、Flask框架、Echarts、Wordcloud等技术实现


## 使用方法

### 直接运行爬虫代码test51job.py
爬虫程序的getInputdata()函数获取用户在网页端输入的岗位关键字与选择的城市（共五个城市可供选择），在main函数中屏蔽调用getInputdata()，放开手动输入，即可单独运行爬虫程序，如下：
```
def main():
    #若须单独执行test51job.py，可将下面四行的注释取消掉，并注释第五行city,keyword = getInputdata()
    print("请输入想查询的城市")
    city = input()
    print("请输入想查询的职位名")
    keyword = input()
    #city,keyword = getInputdata()
```
### 爬虫代码+flask框架，实现爬取数据的可视化效果
打开DEBUG模式，运行51jobflask项目（app.py中对test51job.py进行了调用），打开http://127.0.0.1:5000/ ，在主页输入关键字，选择城市：
![image](https://github.com/tansimin-crypto/51job-/blob/master/static/pic/search.jpg)
输入后点击Get Started按钮，当数据爬取完毕后，自动跳转职位详情页面，其中点击招聘条件列即可跳转至51job的详情描述页：
![image](https://github.com/tansimin-crypto/51job-/blob/master/static/pic/positions.jpg)
薪资统计是按月薪大小对所有信息进行降序排列，效果如下，点击导航栏即可跳转：
![image](https://github.com/tansimin-crypto/51job-/blob/master/static/pic/salary.png)
关键词汇总了所有公司的福利简述，并提取其中的关键字形成词云，效果如下，点击导航栏即可跳转：
![image](https://github.com/tansimin-crypto/51job-/blob/master/static/pic/companysalary.jpg)

## 代码解释

app.py与51job.py有非常详细的注释，就不详细讲解了。





