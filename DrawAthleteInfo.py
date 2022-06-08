import time
from datetime import datetime
from bs4 import BeautifulSoup
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
    #time.sleep(0.2)
    element = driver.find_element(By.XPATH,'/html/body/div/div[2]/table/tbody/tr/td[4]')
    element.click()
    
    data = []

    for y in range(now-10,now+1):
        entries = []
        year = str(y)
        
        #time.sleep(0.3)
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

        try:
            table = driver.find_element(By.XPATH,tablexpath)
            soup = BeautifulSoup(table.get_attribute('innerHTML'), 'html.parser')
            t = soup.get_text(separator='|||').split('\n')
            #print(t)
            for i in range (2,len(t)):
                l = t[i].split('|||')
                date = l[1]
                event = l[3]
                event,hidden_event = standardize_event(event,gender)
                perf = l[6]
                perf = clean_up_perf(perf,event)
                if len(l)==12: #no wind
                    points = l[7]
                    category = l[8]
                elif len(l)==13: #wind
                    points = l[8]
                    category = l[9]
                else:
                    points = 0
                    category = "unknown"

                entry = [firstname+'_'+athletename,[event,hidden_event],perf,points,category,year,date]
                
                try: #compute points
                    entry[3] = regressor.reg(hidden_event,perf)
                except: #event unknown by regressor
                    pass
            
                entries.append(entry)
            entries.reverse()
            print(entries)
        except:
            pass

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
        
        if type(entry[3])==int and entry[3]>0 and 'tria' not in entry[1][1]: 
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
    parser.add_argument('--licence_nb',type=int,default=0,help='Athlete licence')

    args = parser.parse_args()
    
    return(args)


def main():
    
    opt = parse_option()
    if not os.path.isdir("Figures/"+opt.name+"/"):
        os.makedirs("Figures/"+opt.name+"/")
    
    athletename = opt.name
    firstname = opt.firstname
    gender = opt.gender
    by_licence_nb = (opt.licence_nb!=0)
    licence_nb = opt.licence_nb

    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument("headless")
    driver_options.add_argument("disable-gpu")
    driver_options.add_argument("disable-extensions")
    driver_options.add_argument("no-sandbox")
    driver_options.add_argument("disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=driver_options)

    url = "https://bases.athle.fr/asp.net/accueil.aspx?frmbase=resultats"
    driver.get(url)

    data = request(driver,athletename,firstname,gender,by_licence_nb,licence_nb,'')
    #print(data)
    draw_graphics_from_athlete_data(data,opt)


if __name__ == '__main__':
    main()