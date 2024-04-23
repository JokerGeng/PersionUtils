from selenium.webdriver.common.by import By  # 没有selenium库的(请在所用的环境下pip install selenium)
from selenium import webdriver  #selenium库
import time  # 用于延时


def radio1_check(driver:webdriver.Edge,ans:list):
    # radio1有7题
    if len(ans)!=7:
        print('需要7个题的答案选项')
        return
    count=0
    #题目数
    topics = driver.find_elements(By.CSS_SELECTOR,'div.ui-controlgroup.column1')
    for topic in topics:
        #选项数
        selects=topic.find_elements(By.CLASS_NAME,'ui-radio')
        select=selects[ans[count]-1]
        select.click()
        count=count+1
        time.sleep(0.5)

def radio5_check(driver:webdriver.Edge,ans:list):
        # radio1有22题
    if len(ans)!=22:
        print('需要22个题的答案选项')
        return
    count=0
    topics = driver.find_elements(By.CSS_SELECTOR,'div.ui-controlgroup.column5')
    for topic in topics:
        selects=topic.find_elements(By.CLASS_NAME,'ui-radio')
        select=selects[ans[count]-1]
        select.click()
        count=count+1
        time.sleep(0.5)

def test(driver:webdriver.Edge):
    elements=driver.find_elements()
    len(elements)


def answer_num(num:int,radio1_ans:list,radio5_ans:list):
    for count in range(num):
        driver = webdriver.Edge()
        driver.get('https://www.wjx.cn/vm/h4ghRys.aspx')
        sumbit=driver.find_element(By.ID,'ctlNext')
        radio1_check(driver,radio1_ans)
        radio5_check(driver,radio5_ans)
        sumbit.click()
        time.sleep(2)

if __name__ == "__main__":
    #前7题答案
    radio1_ans=[1,2,2,2,1,1,1]
    #后22题答案
    radio5_ans=[1,2,2,2,1,1,1,1,2,2,2,1,1,1,1,2,2,2,1,1,1,2]
    #上面答案需要的份数
    num=10
    answer_num(num,radio1_ans,radio5_ans)#里面填写的数是表示要提交多少次问卷