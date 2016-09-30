from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as etree
from datetime import datetime as dt
from datetime import timedelta

def loaded(browser,URL):
    while(browser.current_url!=URL):
        time.sleep(1)


def login(browser):
    username= '#Your facebook id'
    password='#facebook password'
    loginURL='https://www.facebook.com/login.php?login_attempt=1&lwv=110'
    print 'Logging in.....'
    browser.get(loginURL)
    username_field=browser.find_element_by_id('email')
    password_field=browser.find_element_by_id('pass')
    username_field.send_keys(username)
    password_field.send_keys(password)
    browser.find_element_by_id("loginbutton").click()
    loaded(browser,'https://www.facebook.com/?sk=welcome')

    print "Logged in successfully!"


def get_userIds(browser,pageName):
    pageName=pageName.replace(' ','%20')
    page='https://www.facebook.com/search/top/?q=People%20who%20like%20'+pageName
    browser.get(page)
    loaded(browser,page)
    time.sleep(3)
    id=browser.find_element_by_xpath('//*[@id="xt_uniq_1"]/footer/a')
    browser.get(id.get_attribute('href'))
    users=list()
    userElements=list()
    while len(users)<100:
        del users[:]
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        userElements=browser.find_elements_by_css_selector("*[class^='_3u1 _gli _5und']")
        for element in userElements:
            yes=element.get_attribute('data-bt').split(',')[0]
            users.append(yes[6:])
        users[100:]=[]
    return users

def get_postsncomments(browser,userId,userElement):
    browser.get('https://www.facebook.com/'+userId)
    postURLs=list()
    postElements=browser.find_elements_by_css_selector("*[class^='userContentWrapper _5pcr']")
    for element in postElements:
        postURLs.append(element.find_element_by_class_name('_5pcq').get_attribute('href'))
    for postURL in postURLs:
        browser.get(postURL)
        temp=browser.find_element_by_class_name("timestampContent")
        timeStampElement=temp.find_element_by_xpath("./parent::*")
        timeStamp=timeStampElement.get_attribute('title')
        status=False
        try:
            status=checkTime(timeStamp)
        except:
            pass
        if status:
            postElement=Element('post')
            postElement.set('href',postURL)
            userElement.append(postElement)
            browser.get(postURL)
            try:
                browser.find_element_by_link_text('See Translation').click()
                time.sleep(3)
                post= browser.find_element_by_class_name('_50f4')
                postElement.text=post.text
                postElement.set('date',timeStamp)
            except:
                try:
                    post=browser.find_element_by_class_name('_5wj-')
                    postElement.text=post.text
                except:
                    pass
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                while True:
                    browser.find_element_by_link_text('View previous comments').click()
            except:
                pass
            commentElements=browser.find_elements_by_class_name('UFICommentContent')
            for comment in commentElements:
                commentElement=Element('comment')
                commentBody=comment.find_element_by_class_name("UFICommentBody")
                try:
                    commentElement.text=commentBody.text
                except:
                    commentElement.text=commentBody.text
                postElement.append(commentElement)

def get_likes(browser,user,userElement):
    URL='https://www.facebook.com/profile.php?id='+user+'&sk=likes'
    browser.get(URL)
    time.sleep(2)
    if browser.current_url==URL:
        cls=browser.find_elements_by_css_selector("*[class^='fsl fwb fcb']")
        count=0
        for cls1 in cls:
            count+=1
            likedPages=cls1.find_element_by_xpath('.//a')
            likeElement=Element('like')
            likeElement.set('url',likedPages.get_attribute('href'))
            likeElement.text=likedPages.text
            userElement.append(likeElement)

def get_groups(browser,user,userElement):
    URL='https://www.facebook.com/profile.php?id='+user+'&sk=groups'
    browser.get(URL)
    time.sleep(2)
    if browser.current_url==URL:
        cls=browser.find_elements_by_css_selector("*[class^='mbs fwb']")
        count=0
        for cls1 in cls:
            count+=1
            likedPages=cls1.find_element_by_xpath('.//a')
            likeElement=Element('group')
            likeElement.set('url',likedPages.get_attribute('href'))
            likeElement.text=likedPages.text
            userElement.append(likeElement)

def checkTime(timeStamp):
    current=dt.today()
    leastDate=current-timedelta(days=5)
    time.sleep(2)
    print timeStamp
    datentime=timeStamp.split('at')[0]
    postYear=int(datentime.split(',')[2][-3:])
    po=datentime.split(',')[1]
    postDate=po.split(' ')[2]
    postMonthWord=po.split(' ')[1]
    if postMonthWord=='January':
        postMonth=1
    elif postMonthWord=='February':
        postMonth=2
    elif postMonthWord=='March':
        postMonth=3
    elif postMonthWord=='April':
        postMonth=4
    elif postMonthWord=='May':
        postMonth=5
    elif postMonthWord=='June':
        postMonth=6
    elif postMonthWord=='July':
        postMonth=7
    elif postMonthWord=='August':
        postMonth=8
    elif postMonthWord=='September':
        postMonth=9
    elif postMonthWord=='October':
        postMonth=10
    elif postMonthWord=='November':
        postMonth=11
    elif postMonthWord=='December':
        postMonth=12
    a=str(postMonth)+'/'+postDate+'/'+str(postYear)
    postDated=dt.strptime(a,'%m/%d/%y')
    if postDated>leastDate:
        return True
    else:
        return False

def main():
    #Initializing the browser....
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    browser=webdriver.Chrome('chromedriver.exe',chrome_options=chrome_options)
    print "---------------------------------------------------"

    #Logging in
    login(browser)
    print "---------------------------------------------------"
    print "Getting the users from the given page"
    #Querying for a people who likes a specific page
    pageName='libyanwomen'
    users=get_userIds(browser,pageName)
    #writing the above data to the output file
    root=Element('page')
    tree=ElementTree(root)
    root.set("pageName",pageName)
    print "---------------------------------------------------"
    print "Length of the users is",len(users)
    #getting likes, posts, shares, comments of the users 761263760
    for user in users:
        try:
            userElement=Element('user')
            userElement.set('id',user)
            get_postsncomments(browser,user,userElement)
            get_likes(browser,user,userElement)
            get_groups(browser,user,userElement)
            root.append(userElement)
        except:
            pass
    tree.write(open('output.xml','w'),encoding='utf-8')

if __name__=='__main__':
    main()
