import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import argparse
from auxiliary import athle_regressor,standardize_event

"""
competition_url = 'https://athle.live/challenge/6286492bfcef3bf59ac57943'
competition_status = 'live' #'live' ou 'resultats'
ping = 1.5
nb_days=2
"""

parser = argparse.ArgumentParser(description='Scrap athle.live')
parser.add_argument('--competition_url', metavar='url', type=str,
                    help='Url of the competition')
parser.add_argument('--competition_status', metavar='status', type=str, default='resultats', choices=['live','resultats']
                    ,help='Status of the competition on athle.live')
parser.add_argument('--ping',type=float,default=1,help='Your internet ping')
parser.add_argument('--nb_days',type=int,default=1,help='Number of competition days')
parser.add_argument('--projection',action='store_true',help='Perform projection according to start-lists')

args = parser.parse_args()

competition_url,competition_status,ping,nb_days = args.competition_url,args.competition_status,args.ping,args.nb_days



def filter_linebreaks(t):
    s = t.split('\n')
    return(s[1],"\n---------------------- Evaluation"+" of " + s[1] +" -----------------------")
            
def filter_athlete(t):
    s = t.split('\n')
    if len(s)==2: #has category
        return(s[1])
    else:
        return(s[0])


def scrap_event(n,status,day,nb_days,projection=False):
    if status=='resultats':
        pannel_nb = 5
    elif status=='live':
        pannel_nb = 6
    else:
        print("Unknown status")
    
    time.sleep(ping)
    if nb_days==1:
        element = driver.find_element(By.XPATH,"/html/body/div/div[2]/main/div/div[2]/div/div["+str(pannel_nb)+"]/div["+str(n)+"]")

    else:
        element = driver.find_element(By.XPATH,
            "/html/body/div/div[2]/main/div/div[2]/div/div["+str(pannel_nb)+"]/div/div/div["+str(day)+"]/div["+str(n+1)+"]")
    event = element.text
    event,eventstyle = filter_linebreaks(event)
    category = event.split(' ')[-1]
    gender = category[-1]
    print(eventstyle)
    element.click() 
    time.sleep(ping)
    
    

    racePannelxpath = "/html/body/div/div[2]/main/div/div[2]/div/div[3]/div/div[1]"
    racePannel = driver.find_element(By.XPATH,racePannelxpath)
    
    races = []
    i=1
    while True:
        try:
            race = driver.find_element(By.XPATH,racePannelxpath+"/div["+str(i)+"]")
            racexpath = racePannelxpath+"/div["+str(i)+"]/div/div/div[5]"
            races.append(racexpath)
            i+=1
        except:
            break

    for k in range(len(races)):
        race = races[k]
        
        try: #Check event status
            eventStatusPannelxpath = "/html/body/div/div[2]/main/div/div[2]/div/div[3]/div/div[1]/div["+str(k+1)+"]/div/div/div[3]/header/div/div/div"
            eventStatus = driver.find_element(By.XPATH,eventStatusPannelxpath).text
            if not ("Résultats" in eventStatus or projection):
                print("Start-list detected, uncounted")
                continue
                    
        except:
            #print("Not a start-list")
            pass
        
        i=1
        
        while True: #iterate on athletes
            try:
                athletePannel = driver.find_element(By.XPATH,race+"/div["+str(i)+"]")
                athletePannelxpath = race+"/div["+str(i)+"]/div/div/div"
                
                try:
                    athletexpath = athletePannelxpath+"/div[1]/span"       
                    athletename = filter_athlete(driver.find_element(By.XPATH,athletexpath).text)
                    
                    try:
                        clubxpath = athletePannelxpath+"/div/div[2]"
                        clubname = driver.find_element(By.XPATH,clubxpath).text.lower()
                    except: #no number exception
                        try:
                            clubxpath = athletePannelxpath+"/div/div"
                            clubname = driver.find_element(By.XPATH,clubxpath).text.lower()
                        except: #club not found exception
                            print("Club not found")
                            pass
                        pass
                    
                    perfxpath = athletePannelxpath+"/div[2]/span"
                    perf = driver.find_element(By.XPATH,perfxpath).text
                
                    pointsxpath = athletePannelxpath+"/div[3]/div/span/span[1]/span"
                    nbpoints = driver.find_element(By.XPATH,pointsxpath).text
                    
                    try:
                        stand_event = standardize_event(event,gender)
                        computed_points = regressor.reg(stand_event,perf)
                        if computed_points!=int(nbpoints):
                            print("Computed points do not match with website : " + "computed points = "+str(computed_points)+
                                 " and website points = "+nbpoints)
                    except:
                        pass
                    
                    competition_base.append({'club':clubname,'gender':gender,'name':athletename,'event':event,'cat':category,'perf':perf,'nbpoints':nbpoints})
                    
                    
                    if clubname in clubpoints.keys():
                        clubpoints[clubname]+=int(nbpoints)
                    else:
                        clubpoints[clubname]=int(nbpoints)
                    i+=1
                
                except: #athlete or perf not found exception
                    print("Athlete or perf not found")
                    i+=1
                    pass
                
            except: #end of pannel exception
                break
        print("Number of athletes found in group "+str(k+1)+" : " +str(i-1))

    return(clubpoints)




driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get(competition_url)

accept_cookies = driver.find_element(By.XPATH,"/html/body/div/div[3]/div/div/div[3]/button") 

accept_cookies.send_keys(Keys.ENTER)#accept cookies
time.sleep(ping)

competition_base = []
clubpoints = dict()

day=1
i=1
count_event=1
regressor = athle_regressor()

while day<=nb_days:
    try:
        assert(day<=nb_days)
        #print(i,day)
        scrap_event(i,competition_status,day,nb_days)
        print("Number of evaluated events : "+str(count_event))
        i+=1
        count_event+=1
        driver.get(competition_url)
        print(clubpoints)
    except:
        day+=1
        i=1

#print(competition_base) #club, name, gender, event, category, points
print(clubpoints)

def condition(x):
    return(x['club']=='fc laon' and x['gender']=='M')

#print(list(x for x in competition_base if (condition(x))))
#{'club':clubname,'gender':gender,'name':athletename,'event':event,'cat':category,'perf':perf,'nbpoints':nbpoints}
import csv

with open('competition.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter='|')
    filewriter.writerow(['Club','Name','Gender','Event','Category','Perf','NbPoints'])
    for x in competition_base:
        row = [x['club'],x['name'],x['gender'],x['event'],x['cat'],x['perf'],x['nbpoints']]
        filewriter.writerow(row)
    





driver.close()

