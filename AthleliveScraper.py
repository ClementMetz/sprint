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
import csv

""" #Exemple
competition_url = 'https://athle.live/challenge/6286492bfcef3bf59ac57943'
competition_status = 'live' #'live' ou 'resultats'
ping = 1.5
nb_days=2
"""

def parse_option():
    parser = argparse.ArgumentParser(description='Scrap athle.live for competition info')
    parser.add_argument('--competition_url', metavar='url', type=str,
                    help='Url of the competition')
    parser.add_argument('--competition_status', metavar='status', type=str, default='resultats', choices=['live','resultats']
                    ,help='Status of the competition on athle.live')
    parser.add_argument('--ping',type=float,default=1,help='Your internet ping')
    parser.add_argument('--nb_days',type=int,default=1,help='Number of competition days')
    parser.add_argument('--projection',action='store_true',help='Perform projection according to start-lists')

    args = parser.parse_args()
    args.clubpoints = dict()

    return(args)



def filter_linebreaks(t):
    s = t.split('\n')
    ev = s[0].split(' ')
    return(ev[:len(ev)-1],ev[-1],"\n---------------------- Evaluation of " + s[0] +" -----------------------")
            
def filter_athlete(t):
    s = t.split('\n')
    if len(s)==2: #has category
        return(s[1])
    else:
        return(s[0])


def scrap_event(n,day,opt,driver):
    regressor = athle_regressor()
    competition_base = []
    if opt.competition_status=='resultats':
        pannel_nb = 5
    elif opt.competition_status=='live':
        pannel_nb = 6
    else:
        print("Unknown status")
    
    time.sleep(opt.ping)
    if opt.nb_days==1: #/html/body/div/div[2]/main/div/div[2]/div/div[7]/div[1]/div/div/div
        try:
            element = driver.find_element(By.XPATH,"/html/body/div/div[2]/main/div/div[2]/div/div["+str(pannel_nb)+"]/div["+str(n)+"]/div/div/div/span")
        except:
            try:
                element = driver.find_element(By.XPATH,"/html/body/div/div[2]/main/div/div[2]/div/div["+str(pannel_nb+1)+"]/div["+str(n)+"]/div/div/div/span")
            except:
                return(0)
    # /html/body/div/div[2]/main/div/div[2]/div/div[7]/div[1]/div/div/div
    else:
        try:
            element = driver.find_element(By.XPATH,
                "/html/body/div/div[2]/main/div/div[2]/div/div["+str(pannel_nb)+"]/div/div/div["+str(day)+"]/div["+str(n+1)+"]/div/div/div/span")
        except:
            try:
                element = driver.find_element(By.XPATH,
                    "/html/body/div/div[2]/main/div/div[2]/div/div["+str(pannel_nb+1)+"]/div/div/div["+str(day)+"]/div["+str(n+1)+"]/div/div/div/span")
            except:
                return(0)

    event = element.text
    #print(event)
    event,category,eventstyle = filter_linebreaks(event)
    #category = event.split(' ')[-1]
    gender = category[-1]
    if gender in ['G','H']:
        gender = 'M'
    elif gender=='F':
        gender = 'W'
    
    print(eventstyle)
    element.click() 
    time.sleep(opt.ping)
    
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

    for k,race in enumerate(races):
        
        try: #Check event status
            eventStatusPannelxpath = "/html/body/div/div[2]/main/div/div[2]/div/div[3]/div/div[1]/div["+str(k+1)+"]/div/div/div[3]/header/div/div/div"
            eventStatus = driver.find_element(By.XPATH,eventStatusPannelxpath).text
            if not ("Résultats" in eventStatus or opt.projection):
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

                competition_base.append({'club':'','gender':gender,'name':'','event':event,'cat':category,'perf':'','nbpoints':0})

                try:
                    athletexpath = athletePannelxpath+"/div[1]/span"       
                    athletename = filter_athlete(driver.find_element(By.XPATH,athletexpath).text)
                    competition_base[-1]['name'] = athletename
                except:
                    pass

                try:
                    clubxpath = athletePannelxpath+"/div/div[2]"
                    clubname = driver.find_element(By.XPATH,clubxpath).text.lower()
                    competition_base[-1]['club'] = clubname

                except: #no number exception
                    try:
                        clubxpath = athletePannelxpath+"/div/div"
                        clubname = driver.find_element(By.XPATH,clubxpath).text.lower()
                        competition_base[-1]['club'] = clubname
                    except: #club not found exception
                        print("Club not found")
                        pass
                    pass

                try:
                    pointsxpath = athletePannelxpath+"/div[3]/div/span/span[1]/span"
                    nbpoints = driver.find_element(By.XPATH,pointsxpath).text
                    int(nbpoints) #assert nb points is an int and not bolt machin SB truc
                    competition_base[-1]['nbpoints'] = nbpoints
                except:
                    pass
                
                try:
                    perfxpath = athletePannelxpath+"/div[2]/span"
                    perf = driver.find_element(By.XPATH,perfxpath).text
                    competition_base[-1]['perf'] = perf
                except:
                    pass

                try:
                    if clubname in opt.clubpoints.keys(): #Add points to club total
                        opt.clubpoints[clubname]+=int(nbpoints)
                    else:
                        opt.clubpoints[clubname]=int(nbpoints)
                except:
                    pass
                
                i+=1
                                    
            except: #end of pannel exception
                break
        print("Number of athletes found in group "+str(k+1)+" : " +str(i-1))

    return(opt.clubpoints,competition_base)


def main():
    competition_base = []
    opt = parse_option()
    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument("headless")
    driver_options.add_argument("disable-gpu")
    driver_options.add_argument("disable-extensions")
    driver_options.add_argument("no-sandbox")
    driver_options.add_argument("disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=driver_options)
    driver.get(opt.competition_url)
    accept_cookies = driver.find_element(By.XPATH,"/html/body/div/div[3]/div/div/div[3]/button") 
    accept_cookies.send_keys(Keys.ENTER)#accept cookies
    time.sleep(opt.ping)
    day=1
    i=1
    count_event=1

    while day<=opt.nb_days:
        try:
            assert(day<=opt.nb_days)
            opt.clubpoints,event_base = scrap_event(i,day,opt,driver)
            competition_base+=event_base
            print("Number of evaluated events : "+str(count_event))
            i+=1
            count_event+=1
            driver.back()
            print(opt.clubpoints)
        except:
            day+=1
            i=1
    with open('competition.csv', 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter='|')
        filewriter.writerow(list(opt.clubpoints.keys()))
        filewriter.writerow(list(opt.clubpoints.values()))
        filewriter.writerow(['Club','Name','Gender','Event','Category','Perf','NbPoints'])
        for x in competition_base:
            row = [x['club'],x['name'],x['gender'],x['event'],x['cat'],x['perf'],x['nbpoints']]
            filewriter.writerow(row)

    driver.close()


if __name__ == '__main__':
    main()
