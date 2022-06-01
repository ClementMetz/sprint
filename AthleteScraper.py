import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from auxiliary import athle_regressor,clean_up_perf,standardize_event
import numpy as np
import xlrd
import xlsxwriter
import argparse


def parse_option():
    parser = argparse.ArgumentParser(description='Optimize interclubs placement')
    parser.add_argument('--workdir', type=str,default='ISPTableur_run.xlsm',help='Workbook directory')
    args = parser.parse_args()
    return(args)


def initialize(athletes_table):
    print(athletes_table)
    ath_table = []
    for i in range(1,len(athletes_table.col(0)[1:])+1):
        ath = {}
        licence = athletes_table.cell_value(i,2)
        if licence == '':
            ath['licence'] = ''
        else:
            ath['licence'] = str(int(athletes_table.cell_value(i,2)))
        ath['name'] = athletes_table.cell_value(i,0) 
        ath['firstname'] = athletes_table.cell_value(i,1)
        ath['gender'] = athletes_table.cell_value(i,3)
        print(ath) #ath = [nom,prenom,licence,gender]
        ath_table.append(ath)
    return(ath_table)

def request(driver,athletename,firstname,gender,by_licence_nb=False,licence_nb=0,clubname=''):
    print('*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*.*')
    now = datetime.now().year
    regressor = athle_regressor()
    element = driver.find_element(By.XPATH,'/html/body/div/div[2]/table/tbody/tr/td[4]')
    element.click()
    last_SBs = {}

    for y in range(now-10,now+1):
        current_SBs = {}
        year = str(y)
        
        select = Select(driver.find_element(By.XPATH,'/html/body/div/div[2]/div[5]/div/form/table/tbody/tr/td/table/tbody/tr[1]/td[2]/select'))
        select.select_by_visible_text(year)
        
        if by_licence_nb: #to avoid namesakes
            element = driver.find_element(By.XPATH,'/html/body/div/div[2]/div[5]/div/form/table/tbody/tr/td/table/tbody/tr[6]/td[2]/input')
            element.send_keys(licence_nb)

        element = driver.find_element(By.XPATH,'/html/body/div/div[2]/div[5]/div/form/table/tbody/tr/td/table/tbody/tr[3]/td[2]/input')
        element.send_keys(athletename)
        #time.sleep(0.2)
        element = driver.find_element(By.XPATH,'/html/body/div/div[2]/div[5]/div/form/table/tbody/tr/td/table/tbody/tr[4]/td[2]/input')
        element.send_keys(firstname)
        #time.sleep(0.2)
        element = driver.find_element(By.XPATH,'/html/body/div/div[2]/div[5]/div/form/div[1]/input')
        element.click()
        #time.sleep(0.5)
        tablexpath = '/html/body/div/div[2]/table[2]/tbody'
        i=3

        while True: #/html/body/div/div[2]/table[2]/tbody/tr[3]/td[5]
            try:
                datexpath = tablexpath+'/tr['+str(i)+']/td[1]'
                date = driver.find_element(By.XPATH,datexpath).text
                
                namexpath = tablexpath+'/tr['+str(i)+']/td[3]'
                name = driver.find_element(By.XPATH,namexpath).text
                
                eventxpath = tablexpath+'/tr['+str(i)+']/td[5]'
                event = driver.find_element(By.XPATH,eventxpath).text
                event,hidden_event = standardize_event(event,gender)
                l = len(hidden_event)
                if event[l-1] == 'i': #indoor events are outdoor events
                    event = event[:l-1]
                
                perfxpath = tablexpath+'/tr['+str(i)+']/td[11]'
                perf = driver.find_element(By.XPATH,perfxpath).text
                perf = clean_up_perf(perf,event)
                #print(event,hidden_event,perf)

                if event in ['100mM','200mM','400mM','800mM','1500mM','3000mM','3000scM','110mHM','400mHM','5000walkM','longM','highM','tripleM','poleM',
                'shotM','javM','hammerM','discM','100mW','200mW','400mW','800mW','1500mW','3000mW','100mHW','400mHW','3000walkW','longW','highW','tripleW','poleW','shotW','javW','hammerW','discW']:
                    new = regressor.reg(hidden_event,perf)
                    if new>0 and (event not in current_SBs.keys() or new > regressor.reg(hidden_event,current_SBs[event])):
                        current_SBs[event] = perf



                i+=1
    
            except:
                break
        
        for key in current_SBs.keys():
            #print(key)
            last_SBs[key] = current_SBs[key]
        
        driver.back()

    return(last_SBs)


def make_csv(dico,gender,file):
    
    if gender=='W':
        list_events = ['100mW','200mW','400mW','800mW','1500mW','3000mW','100mHW','400mHW','3000walkW','longW','highW','tripleW','poleW','shotW',
                'javW','hammerW','discW']
    else:
        list_events = ['100mM','200mM','400mM','800mM','1500mM','3000mM','3000scM','110mHM','400mHM','5000walkM','longM','highM','tripleM','poleM',
                'shotM','javM','hammerM','discM']
    for i in range(len(list_events)):
        x = list_events[i]
        if x in dico.keys():
            file.write(dico[x])
        else:
            file.write('o')
        if i<len(list_events)-1:
            file.write('|')
        else:
            file.write('\n')



def main():
    opt = parse_option()
    table = xlrd.open_workbook(opt.workdir)
    athletes2scrape = table.sheet_by_name("AthleteScraper")
    ath_table = initialize(athletes2scrape)
    time.sleep(0.1)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    url = "https://bases.athle.fr/asp.net/accueil.aspx?frmbase=resultats"
    driver.get(url)

    f = open('last_sbs.txt','w')
    for ath in ath_table:
        last_SBs = request(driver,ath['name'],ath['firstname'],ath['gender'],True,ath['licence'],'')
        print(ath['firstname'],ath['name'])
        print(last_SBs)
        make_csv(last_SBs,ath['gender'],f)
    f.close()


if __name__ == '__main__':
    main()




