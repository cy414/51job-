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
直接运行51jobflask项目，打开debug模式，app.py中对test51job.py进行了调用
![image]https://github.com/tansimin-crypto/51job-/blob/master/static/pic/search.jpg
个人主页再由上一步来解析。

## 代码解释

app.pyyu51job.py有非常详细的注释，在此我就不详细讲解。



## 效果图
