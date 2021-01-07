#!/usr/bin/python
#coding:utf-8
from bs4 import BeautifulSoup
import requests
import re
import time 
from optparse import OptionParser 
from fake_useragent import UserAgent

class Domain:
    def __init__(self,domain,page,filename):
        self.domain=domain
        self.page=page
        self.filename=filename

    def GetHeaders(self):
        ua = UserAgent()
        header ={
            "Connection":"keep-alive",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"%s"%ua.random,
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding":"gzip,deflate",
            "Accept-Language":"zh-CN,zh;q=0.9"
            }
        return header

    def GetDomainFromsogou(self):
        print("#######################################################Sogou##########################\n")
        result=[]
        file=open(self.filename,"w+")
        ua = UserAgent()
        for j in range(1,int(self.page)+1):
            p=(j-1)*10
            url="https://www.sogou.com/web?query=site%%3A%s&from=index-no\
            login&s_from=index&sut=6694&sst0=1609987344627&lkt=15%%2C1609987337934%%2C1609987344355&\
            sugsuv=1609987334545270&sugtime=1609987344627&page=%s&ie=utf8&p=40040100&dp=1&w=01019900&dr=1" %(self.domain,p)
            print("获取site:%s第%s页的内容.................."%(self.domain,j))
            
            #s=requests.Session()
            data=requests.get(url=url,headers=self.GetHeaders())
            #print(data.text)
            soup=BeautifulSoup(data.text,'lxml')
            #print(soup)
            #tag=soup.find_all('div',attrs={'id':'content_left'})
            tag=soup.find_all('div',attrs={'class':'fb'})
            #print(tag)
            for i in tag:
                if i.cite.string:
                    sogoudomain=i.cite.string.split()[2]
                else:
                    continue
                if sogoudomain:
                    sogoudomain=sogoudomain.split('/')[0]
                else:
                    continue
                print(sogoudomain)
                result.append(sogoudomain)
                file.write(sogoudomain+"\n")
            time.sleep(5)
        #print(result)
        return result
        file.close()

    def GetDomainFromBaidu(self):
        print("#######################################################Baidu##########################\n")
        result=[]
        file=open(self.filename,"w+")
        
        for j in range(1,int(self.page)+1):
            p=(j-1)*10
            url="https://www.baidu.com/s?wd=site%%3A%s&pn=%s&oq=site%%3A%s\
            &ie=utf-8&fenlei=256&rsv_idx=1&rsv_pq=ee5b2a33000815e7&\
            rsv_t=685afsrI5MwzKqY7Q54co3Z4umvdAM0BApUIv7IX%%2B761hYc1O8%%2FyMog2fXk&rsv_page=1" %(self.domain,p,self.domain)
            print("获取site:%s第%s页的内容.................................."%(self.domain,j))  
            data=requests.get(url=url,headers=self.GetHeaders())
            soup=BeautifulSoup(data.text,'lxml')
            tag=soup.find_all('a',attrs={'class':'c-showurl c-color-gray'})
            for i in tag:
                getdomain=str(i.string).split('/')[0]
                if self.domain in  getdomain:
                    if getdomain not in result:
                        print(getdomain)
                        result.append(getdomain)
                        file.write(getdomain+'\n')
                else:
                    continue
            time.sleep(3)
        #print(result)
        file.close()
        return result

    def GetDomainFromBing(self):
        print("#######################################################Bing##########################\n")
        result=[]
        file=open(self.filename,"w+")
        ua = UserAgent()
        for j in range(1,int(self.page)+1):
            p=(j-1)*10
            print("获取site:%s第%s页的内容.................................."%(self.domain,j))
            url="https://cn.bing.com/search?q=site%%3a%s&qs=n&\
            sp=-1&pq=site%%3a%s&sc=1-14&sk=&cvid=F13445D401B348\
            2FBAF018C1403CDFC4&first=%s&FORM=PORE" %(self.domain,self.domain,p)
            #print(url)
            data=requests.get(url=url,headers=self.GetHeaders())
            #print(data.text)
            soup=BeautifulSoup(data.text,'lxml')
            #print(soup)
            #tag=soup.find_all('div',attrs={'id':'content_left'})
            tag=soup.findAll('h2')
            #print(tag)
            for i in tag:
                if i.a and ('?' not in i.a.string):
                    print(i.a.get('href').split('/')[2])
                    if self.domain in str(i.a.get('href').split('/')[2]):
                        if str(i.a.get('href').split('/')[2]) not in result:
                            result.append(str(i.a.get('href').split('/')[2]))
                            file.write(str(i.a.get('href').split('/')[2])+"\n")
                else:
                    continue

            time.sleep(3)
        #print(result)
        file.close()
        return result

    def GetDomainFrom360(self):
        print("#######################################################360##########################\n")
        result=[]
        file=open(self.filename,"w+")
        ua = UserAgent()
        for j in range(1,int(self.page)+1):
            p=(j-1)*10
            url="https://www.so.com/s?q=site%%3A%s&pn=%s&psid=001266ee55b3cd61dbc2c072b5e8820a&src=srp_paging&fr=none" %(self.domain,p)
            print("获取site:%s第%s页的内容.................."%(self.domain,j))
            
            #s=requests.Session()
            data=requests.get(url=url,headers=self.GetHeaders())
            #print(data.text)
            soup=BeautifulSoup(data.text,'lxml')
            #print(soup)
            #tag=soup.find_all('div',attrs={'id':'content_left'})
            tag=soup.find_all('p',attrs={'class':'g-linkinfo'})
            #print(tag)
            for i in tag:
                #print(i)
                #print(i.cite.string)
                if '/' in i.cite.string:
                    getdomain=i.cite.string.split('/')[0]
                    print(getdomain)
                elif '>' in i.cite.string:
                    getdomain=i.cite.string.split('>')[0]
                    print(getdomain)
                else:
                    getdomain=i.cite.string
                if self.domain in getdomain:
                    print(getdomain)
                    if getdomain not in result:
                        result.append(getdomain)
                        file.write(getdomain+'\n')
                else:
                    continue
            time.sleep(3)
        #print(result)
        return result
        file.close()
def GetOptions():
    optParser = OptionParser()
    optParser.add_option('-d','--domain',action = 'store',type = "string" ,dest = 'domain',help='Domain')
    optParser.add_option('-p','--page',action = 'store',type = "string" ,dest = 'page',help='page')
    optParser.add_option('-f','--filename',action = 'store',type = "string" ,dest = 'filename',help='filename')
    
    (options, args) = optParser.parse_args() 
    return (options,args)

if __name__=="__main__":
    domainresult=[]
    baiduresult=[]
    bingresult=[]
    result360=[]
    sogouresult=[]

    (options,args)=GetOptions()
    file=open(str(options.filename),"w+")
    classdomain=Domain(str(options.domain),str(options.page),str(options.filename))

    try:
        baiduresult=classdomain.GetDomainFromBaidu()
        bingresult=classdomain.GetDomainFromBing()
        result360=classdomain.GetDomainFrom360()
        sogouresult=classdomain.GetDomainFromsogou()
        domainresult.extend(baiduresult)
        domainresult.extend(bingresult)
        domainresult.extend(result360)
        domainresult.extend(sogouresult)
    except Exception as e:
        print(e)
    domainresult=list(set(domainresult))
    #domainresult=list(set(domainresult)).sort()
    print(domainresult)
    
    for k in domainresult:
        file.write(k+"\n")
    file.close()