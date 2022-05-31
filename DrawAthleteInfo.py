import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from auxiliary import athle_regressor,standardize_event
from auxiliary import string_converter_dist,string_converter_time,clean_up_perf
from matplotlib import pyplot as plt
from numpy import polyfit,polyval,arange
import argparse
import os



def request(driver,athletename,firstname,gender,by_licence_nb=False,licence_nb=0,clubname=''):
    regressor = athle_regressor()
    now = datetime.now().year
    time.sleep(0.2)
    element = driver.find_element(By.XPATH,'/html/body/div/div[2]/table/tbody/tr/td[4]')
    element.click()
    
    data = []

    for y in range(now-10,now+1):
        entries = []
        year = str(y)
        
        time.sleep(0.3)
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

        tablexpath = '/html/body/div/div[2]/table[2]/tbody'
        i=3

        while True:
            try:
                entry=[]
                datexpath = tablexpath+'/tr['+str(i)+']/td[1]'
                date = driver.find_element(By.XPATH,datexpath).text
                
                namexpath = tablexpath+'/tr['+str(i)+']/td[3]'
                name = driver.find_element(By.XPATH,namexpath).text
                entry.append(name)
                
                eventxpath = tablexpath+'/tr['+str(i)+']/td[5]'
                event = driver.find_element(By.XPATH,eventxpath).text
                #print(event)
                event,hidden_event = standardize_event(event,gender)
                entry.append([event,hidden_event])
                #print(event,hidden_event)
                
                perfxpath = tablexpath+'/tr['+str(i)+']/td[11]'
                perf = driver.find_element(By.XPATH,perfxpath).text
                #print(perf)
                perf = clean_up_perf(perf,event)
                #print(perf)
                entry.append(perf)
                
                pointsxpath = tablexpath+'/tr['+str(i)+']/td[13]'
                points = driver.find_element(By.XPATH,pointsxpath).text
                entry.append(points)
                #print(points)
                categoryxpath = tablexpath+'/tr['+str(i)+']/td[15]'
                category = driver.find_element(By.XPATH,categoryxpath).text
                entry.append(category)
                #print(category)
                entry.append(year)
                entry.append(date)
                
                try: #compute points
                    #print(event,hidden_event,perf)
                    entry[3] = regressor.reg(hidden_event,perf)
                    #print('cc')
                except: #event unknown by regressor
                    pass
                
                #print(entry)
                entries.append(entry)
                i+=1
    
            except:
                break
        
        entries.reverse()
        data+=entries
        
        driver.back()

    print(str(len(data))+' entries found.')
    return(data)


def date_to_float(date):
    j,m = tuple(date.split('/'))
    return((int(j)+(int(m)-1)*30)/360)


def draw_graphics_from_athlete_data(data,opt):
    data_by_event = {}
    for entry in data:
        #entry[2] = clean_up_perf(entry[2],entry[1][1])
       
        #if 'tria' in entry[1][0] or 'penta' in entry[1][0] or 'hepta' in entry[1][0] or 'deca' in entry[1][0]: #handle combine events
            #entry[3] = entry[2]
        
        #Get rid of unknown and poorly scored events, take care of triathlon for kids
        cond = (entry[3]!=' ' and ((int(entry[3])>50 and 'tria' not in entry[1]) or
                    ('tria' in entry[1] and not ("CA" in entry[4] or "JU" in entry[4] or "ES" in entry[4] or "SE" in entry[4] or "VE" in entry[4]))))
        if cond : 
            #print(entry)
            if entry[1][0] not in data_by_event.keys():
                data_by_event[entry[1][0]] = [[entry[2],int(entry[3]),int(entry[5])+date_to_float(entry[6])]]
            else:
                data_by_event[entry[1][0]].append([entry[2],int(entry[3]),int(entry[5])+date_to_float(entry[6])])
    
    for event in data_by_event.keys():
        year_list = []
        perf_list = []
        label_list = []
        for x in data_by_event[event]:
            perf_list.append(x[1])
            year_list.append(x[2])
            label_list.append(x[0])
        
        p = polyfit(year_list,perf_list,2)
        
        fig, ax = plt.subplots()
        ax.set_title(event)
        ax.scatter(year_list, perf_list)
        ax.plot(arange(min(year_list)-0.6,max(year_list)+0.6,0.02),[polyval(p,x) for x in arange(min(year_list)-0.6,max(year_list)+0.6,0.02)],'r')

        for i, txt in enumerate(label_list):
            ax.annotate(txt, (year_list[i], perf_list[i]))
    
        plt.savefig("Figures/"+opt.name+"/"+event+".png")
        
def parse_option():
    parser = argparse.ArgumentParser(description='Scrap bases FFA for athlete info')
    parser.add_argument('--firstname', type=str,help='Athlete firstname')
    parser.add_argument('--name',type=str,help='Athlete name')
    parser.add_argument('--gender',type=str,choices=['W','M'],help='Athlete gender')
    parser.add_argument('--by_licence_nb',default=False,help='Search by licence nb')
    parser.add_argument('--licence_nb',type=int,help='Athlete licence')

    args = parser.parse_args()
    
    return(args)


def main():
    
    opt = parse_option()
    if not os.path.isdir("Figures/"+opt.name+"/"):
        os.makedirs("Figures/"+opt.name+"/")
    
    athletename = opt.name
    firstname = opt.firstname
    gender = opt.gender
    by_licence_nb = opt.by_licence_nb
    licence_nb = opt.licence_nb

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    url = "https://bases.athle.fr/asp.net/accueil.aspx?frmbase=resultats"
    driver.get(url)

    data = request(driver,athletename,firstname,gender,by_licence_nb,licence_nb,'')
    #print(data)
    draw_graphics_from_athlete_data(data,opt)


if __name__ == '__main__':
    main()