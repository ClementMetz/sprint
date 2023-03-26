from datetime import timedelta
from datetime import datetime
import numpy as np
from math import sqrt


def standardize_event(event,gender): #Second version
    
    event=event.lower()    
    hidden_event = event
    
    identifiers = {"salle":"salle" in event,"distance": "0m" in event or "mile" in event,"poids": "g)" in event,"haies":"haies" in event, "steeple":"steeple" in event,
                   "saut":"longueur" in event or "hauteur" in event or "triple" in event or "perche" in event,"relais":" X " in event,
                  "marche": "marche" in event}
    event_features = 0
    
    if identifiers["relais"]:
        return(event,hidden_event)
    
    if identifiers["poids"]:
        if "2 kg" in event or "2kg" in event:
            event_features = 2
        elif "3 kg" in event or "3kg" in event:
            event_features = 3
        elif "4 kg" in event or "4kg" in event:
            event_features = 4
        elif "5 kg" in event or "5kg" in event:
            event_features = 5
        elif "6 kg" in event or "6kg" in event:
            event_features = 6
        elif "7 kg" in event or "7kg" in event:
            event_features = 7
        elif "7.26 kg" in event or "7.26kg" in event:
            event_features = 7
        elif "0.3 kg" in event or "300 g" in event or "0.3kg" in event or "300g" in event:
            event_features = 0.3
        elif "0.4 kg" in event or "400 g" in event or "0.4kg" in event or "400g" in event:
            event_features = 0.4
        elif "0.5 kg" in event or "500 g" in event or "0.5kg" in event or "500g" in event:
            event_features = 0.5
        elif "0.6 kg" in event or "600 g" in event or "0.6kg" in event or "600g" in event:
            event_features = 0.6
        elif "0.8 kg" in event or "800 g" in event or "0.8kg" in event or "800g" in event:
            event_features = 0.8
        elif "1.25 kg" in event  or "1.25kg" in event:
            event_features = 1.25
        elif "1.5 kg" in event  or "1.5kg" in event:
            event_features = 1.5
        elif "1.75 kg" in event  or "1.75kg" in event:
            event_features = 1.75
    elif identifiers["haies"]:
        if "65" in event:
            event_features = 65
        elif "76" in event:
            event_features = 76
        elif "84" in event:
            event_features = 84
        elif "91" in event:
            event_features = 91
        elif "99" in event:
            event_features = 99
        elif "106" in event:
            event_features = 106
        elif "steeple" in event:
            event_features = 3000
    
    if gender=="G":
        gender="M"
    if gender=="F":
        gender="W"
    
    if identifiers["salle"]:
        if identifiers["haies"]:
            if "60m" in event:
                if gender=="W":
                    if event_features==84:
                        event,hidden_event = "60mHWi","60mHWi"
                    else:
                        event,hidden_event = "60mHWi ("+str(event_features)+")","60mHWi"
                elif gender=="M":
                    if event_features==106:
                        event,hidden_event = "60mHMi","60mHMi"
                    else:
                        event,hidden_event = "60mHMi ("+str(event_features)+")","60mHMi"
            elif "50m" in event:
                if gender=="W":
                    if event_features==84:
                        event,hidden_event = "50mHWi","50mHWi"
                    else:
                        event,hidden_event = "50mHWi ("+str(event_features)+")","50mHWi"
                elif gender=="M":
                    if event_features==106:
                        event,hidden_event = "50mHMi","50mHMi"
                    else:
                        event,hidden_event = "50mHMi ("+str(event_features)+")","50mHMi"
        elif "triathlon" in event and not (identifiers["distance"] or identifiers["haies"] or identifiers["poids"] or identifiers["saut"]):
            event = "tria"+gender+"i"
            if gender=="M":
                hidden_event="heptaMi"
            else:
                hidden_event="pentaWi"
        elif "pentathlon" in event and not (identifiers["distance"] or identifiers["haies"] or identifiers["poids"] or identifiers["saut"]):
            event,hidden_event = "penta"+gender+"i","penta"+"Wi"
        elif "heptathlon" in event and not (identifiers["distance"] or identifiers["haies"] or identifiers["poids"] or identifiers["saut"]):
            event,hidden_event = "hepta"+gender+"i","heptaMi"
        elif identifiers["distance"] and not identifiers["haies"]:
            if event[:3]=="30m":
                event,hidden_event = "30m"+gender+'i',"50m"+gender+'i'
            elif event[:3]=="40m":
                event,hidden_event = "40m"+gender+'i',"50m"+gender+'i'
            elif event[:3]=="50m":
                event,hidden_event = "50m"+gender+'i',"50m"+gender+'i'
            elif event[:3]=="60m":
                event,hidden_event = "60m"+gender+'i',"60m"+gender+'i'
            elif event[:4]=="100m":
                event,hidden_event = "100m"+gender+'i',"100m"+gender
            elif event[:4]=="200m":
                event,hidden_event = "200m"+gender+'i',"200m"+gender+'i'
            elif event[:4]=="300m":
                event,hidden_event = "300m"+gender+'i',"300m"+gender+'i'
            elif event[:4]=="400m":
                event,hidden_event = "400m"+gender+'i',"400m"+gender+'i'
            elif event[:4]=="600m":
                event,hidden_event = "600m"+gender+'i',"600m"+gender+'i'
            elif event[:4]=="800m":
                event,hidden_event = "800m"+gender+'i',"800m"+gender+'i'
            elif event[:6]=="1 000m":
                event,hidden_event = "1000m"+gender+'i',"1000m"+gender+'i'
            elif event[:6]=="1 500m":
                event,hidden_event = "1500m"+gender+'i',"1500m"+gender+'i'
            elif event[:4]=="mile":
                event,hidden_event = "1mile"+gender+'i',"1mile"+gender+'i'
            elif event[:6]=="3 000m":
                event,hidden_event = "3000m"+gender+'i',"3000m"+gender+'i'
            else: #unknown distance
                l = (event.split('/')[0]).split(' ')
                s = ''
                for i in range(len(l)):
                    s+=l[i]
                event,hidden_event=s,s
        elif "longueur" in event:
            event,hidden_event = "long"+gender+'i',"long"+gender+'i'
        elif "hauteur" in event:
            event,hidden_event = "high"+gender+'i',"high"+gender+'i'
        elif "triple" in event:
            event,hidden_event = "triple"+gender+'i',"triple"+gender+'i'
        elif "perche" in event:
            event,hidden_event = "pole"+gender+'i',"pole"+gender+'i'
        elif identifiers["poids"]:
            #print("features",event_features)
            if "poids" in event:
                if gender=="W":
                    if event_features==4:
                        event,hidden_event = "shotWi","shotWi"
                    else:
                        event,hidden_event = "shotWi ("+str(event_features)+"kg)","shotWi"
                elif gender=="M":
                    if event_features==7:
                        event,hidden_event = "shotMi","shotMi"
                    else:
                        event,hidden_event = "shotMi"+"("+str(event_features)+"kg)","shotMi"
            #print(event,hidden_event)
            
        else:
            l = (event.split('/')[0]).split(' ')
            s = ''
            for i in range(len(l)):
                s+=l[i]
            event,hidden_event=s,s
        
    else: #outdoor
        
        if identifiers["haies"]:
            if "400m" in event:
                if gender=="W":
                    if event_features==76:
                        event,hidden_event = "400mHW","400mHW"
                    else:
                        event,hidden_event = "400mHW ("+str(event_features)+")","400mHW"
                elif gender=="M":
                    if event_features==91:
                        event,hidden_event = "400mHM","400mHM"
                    else:
                        event,hidden_event = "400mHM ("+str(event_features)+")","400mHM"
            elif "200m" in event:
                if gender=="W":
                    if event_features==76:
                        event,hidden_event = "200mHW","400mHW"
                    else:
                        event,hidden_event = "200mHW ("+str(event_features)+")","400mHW"
                elif gender=="M":
                    if event_features==91:
                        event,hidden_event = "200mHM","400mHM"
                    else:
                        event,hidden_event = "200mHM ("+str(event_features)+")","400mHM"
            elif "110m" in event:
                if gender=="M":
                    if event_features==106:
                        event,hidden_event = "110mHM","110mHM"
                    else:
                        event,hidden_event = "110mHM ("+str(event_features)+")","110mHM"
            elif "100m" in event:
                if gender=="W":
                    if event_features==84:
                        event,hidden_event = "100mHW","100mHW"
                    else:
                        event,hidden_event = "100mHW ("+str(event_features)+")","100mHW"
            elif "80m" in event:
                if gender=="W":
                    if event_features==84:
                        event,hidden_event = "80mHW","100mHW"
                    else:
                        event,hidden_event = "80mHW ("+str(event_features)+")","100mHW"
                elif gender=="M":
                    if event_features==106:
                        event,hidden_event = "80mHM","100mHM"
                    else:
                        event,hidden_event = "80mHM ("+str(event_features)+")","100mHM"
            elif "60m" in event:
                if gender=="W":
                    if event_features==84:
                        event,hidden_event = "60mHW","60mHWi"
                    else:
                        event,hidden_event = "60mHW ("+str(event_features)+")","60mHWi"
                elif gender=="M":
                    if event_features==106:
                        event,hidden_event = "60mHM","60mHMi"
                    else:
                        event,hidden_event = "60mHM ("+str(event_features)+")","60mHMi"
            elif "50m" in event:
                if gender=="W":
                    if event_features==84:
                        event,hidden_event = "50mHW","50mHWi"
                    else:
                        event,hidden_event = "50mHW ("+str(event_features)+")","50mHWi"
                elif gender=="M":
                    if event_features==106:
                        event,hidden_event = "50mHM","50mHMi"
                    else:
                        event,hidden_event = "50mHM ("+str(event_features)+")","50mHMi"
        
        elif "triathlon" in event and not (identifiers["distance"] or identifiers["haies"] or identifiers["poids"] or identifiers["saut"]):
            event = "tria"+gender
            if gender=="M":
                hidden_event="decaM"
            else:
                hidden_event="heptaW"
        elif "pentathlon" in event and not (identifiers["distance"] or identifiers["haies"] or identifiers["poids"] or identifiers["saut"]):
            event = "penta"+gender
            if gender=="M":
                hidden_event="decaM"
            else:
                hidden_event="heptaW"
        elif "heptathlon" in event and not (identifiers["distance"] or identifiers["haies"] or identifiers["poids"] or identifiers["saut"]):
            event = "hepta"+gender
            if gender=="M":
                hidden_event="decaM"
            else:
                hidden_event="heptaW"
        elif "decathlon" in event and not (identifiers["distance"] or identifiers["haies"] or identifiers["poids"] or identifiers["saut"]):
            event = "deca"+gender
            if gender=="M":
                hidden_event="decaM"
            else:
                hidden_event="heptaW"
        
        elif identifiers["distance"] and not identifiers["haies"] and not identifiers["marche"]:
            if identifiers["steeple"]:
                if "2000" in event or "2 000" in event:
                    event,hidden_event = "2000msc"+gender,"2000msc"+gender
                elif "3000" in event or "3 000" in event:
                    event,hidden_event = "3000msc"+gender,"3000msc"+gender
            elif event[:3]=="30m":
                event,hidden_event = "30m"+gender,"50m"+gender+'i'
            elif event[:3]=="40m":
                event,hidden_event = "40m"+gender,"50m"+gender+'i'
            elif event[:3]=="50m":
                event,hidden_event = "50m"+gender,"50m"+gender+'i'
            elif event[:3]=="60m":
                event,hidden_event = "60m"+gender,"60m"+gender+'i'
            elif event[:4]=="100m":
                event,hidden_event = "100m"+gender,"100m"+gender
            elif event[:4]=="200m":
                event,hidden_event = "200m"+gender,"200m"+gender
            elif event[:4]=="300m":
                event,hidden_event = "300m"+gender,"300m"+gender
            elif event[:4]=="400m":
                event,hidden_event = "400m"+gender,"400m"+gender
            elif event[:4]=="600m":
                event,hidden_event = "600m"+gender,"600m"+gender
            elif event[:4]=="800m":
                event,hidden_event = "800m"+gender,"800m"+gender
            elif event[:6]=="1 000m":
                event,hidden_event = "1000m"+gender,"1000m"+gender
            elif event[:6]=="1 500m":
                event,hidden_event = "1500m"+gender,"1500m"+gender
            elif event[:4]=="mile":
                event,hidden_event = "1mile"+gender,"1mile"+gender
            elif event=="2 000m":
                event,hidden_event = "2000m"+gender,"2000m"+gender
            elif event=="3 000m":
                event,hidden_event = "3000m"+gender,"3000m"+gender
            elif event=="5 000m":
                event,hidden_event = "5000m"+gender,"5000m"+gender
            elif event=="10 000m":
                event,hidden_event = "10000m"+gender,"10000m"+gender
            else: #unknown distance
                l = (event.split('/')[0]).split(' ')
                s = ''
                for i in range(len(l)):
                    s+=l[i]
                event,hidden_event=s,s
        elif identifiers["marche"]:
            if "3 000m" in event:
                event,hidden_event="3000walk"+gender,"3000walk"+gender
            elif "5 000m" in event:
                event,hidden_event="5000walk"+gender,"5000walk"+gender
                    
        elif "longueur" in event:
            event,hidden_event = "long"+gender,"long"+gender
        elif "hauteur" in event:
            event,hidden_event = "high"+gender,"high"+gender
        elif "triple" in event:
            event,hidden_event = "triple"+gender,"triple"+gender
        elif "perche" in event:
            event,hidden_event = "pole"+gender,"pole"+gender
        elif identifiers["poids"]:
            if "poids" in event:
                if gender=="W":
                    if event_features==4:
                        event,hidden_event = "shotW","shotW"
                    else:
                        event,hidden_event = "shotW ("+str(event_features)+"kg)","shotW"
                elif gender=="M":
                    if event_features==7:
                        event,hidden_event = "shotM","shotM"
                    else:
                        event,hidden_event = "shotM"+"("+str(event_features)+"kg)","shotM"
            
            elif "marteau" in event:
                if gender=="W":
                    if event_features==4:
                        event,hidden_event = "hammerW","hammerW"
                    else:
                        event,hidden_event = "hammerW ("+str(event_features)+"kg)","hammerW"
                elif gender=="M":
                    if event_features==7:
                        event,hidden_event = "hammerM","hammerM"
                    else:
                        event,hidden_event = "hammerM"+"("+str(event_features)+"kg)","hammerM"

            elif "disque" in event:
                if gender=="W":
                    if event_features==1:
                        event,hidden_event = "discW","discW"
                    else:
                        event,hidden_event = "discW ("+str(event_features)+"kg)","discW"
                elif gender=="M":
                    if event_features==2:
                        event,hidden_event = "discM","discM"
                    else:
                        event,hidden_event = "discM"+"("+str(event_features)+"kg)","discM"
                        
            elif "javelot" in event:
                if gender=="W":
                    if event_features==0.6:
                        event,hidden_event = "javW","javW"
                    else:
                        event,hidden_event = "javW ("+str(event_features)+"kg)","javW"
                elif gender=="M":
                    if event_features==0.8:
                        event,hidden_event = "javM","javM"
                    else:
                        event,hidden_event = "javM"+"("+str(event_features)+"kg)","javM"
        else:
            l = (event.split('/')[0]).split(' ')
            s = ''
            for i in range(len(l)):
                s+=l[i]
            event,hidden_event=s,s
    
    return(event,hidden_event)
    
            
            
"""
Polynomial interpolation results
{'100mM':(24.53,- 834.9,7101),'200mM':(5.072,- 360.3, 6397),'400mM':(1.021, - 161.3, 6372),
                          '400mHM':(0.5455, - 104.2, 4977),'110mHM':(7.676,- 395.7, 5102),'800mM':(0.1981, - 72.09, 6559.3)
                          ,'1500mM':(0.04066, - 31.31, 6027),'3000mM':(0.008155,- 13.7,5752),'3000mscM':(0.004322,- 8.812, 4492),
                         '5000walkM':(0.0004375,- 2.411, 3323),'highM':(32.69, 743.6,- 704),'poleM':(2.808,241.5,- 284.5),
                         'longM':(1.588,191.1,- 493.3),'tripleM':(0.4479, 91.27, - 516.9),'shotM':(0.037,58.15,- 57.02),
                         'discM':(0.003979, 17.9,- 27.25),'hammerM':(0.002642 ,14.98, - 21.22),'javM':(0.002538, 13.83,- 20.78),
                         '100mW':(10.05, - 439.7, 4820.5),'200mW':(2.219, - 202.8 ,4625),'400mW':(0.3355, - 73.77, 4055),
                         '400mHW':(0.2083,- 54.19,3523),'100mHW':(4.018, - 240, 3591),'800mW':(0.06873,- 34.38,4298),
                         '1500mW':(0.0134,- 14.47,3908),'3000mW':(0.002541 ,- 6.096, 3657),'3000walkW':(0.0008818,- 3.3, 3086),
                         'highW':(52.34, 793.2, - 573.1),'poleW':(3.769, 276.7, - 207.2),'longW':(2.067, 192.9, - 232.7),
                         'tripleW':(0.4004, 90.87, - 234),'shotW':(0.05937, 60.42, - 23.91),'discW':(0.004131, 17.93,- 18.95),
                         'hammerW':(0.002993, 15.74, - 22.75),'javW':(0.004627, 18 ,- 18.1)}
constants = list(self.constants[event])
constants.reverse()
poly = np.polynomial.Polynomial(constants)

            if perf < np.real(max(poly.roots())): #perf worse than 0 pts
                return(0)
            if perf > np.real(min(poly.roots())): #perf worse than 0 pts
                return(0)
return(round(poly.__call__(perf)))

"""



def string_converter_time(s):

    time = []
    x = ''
    for i in range (len(s)):
        if s[i] not in ['0','1','2','3','4','5','6','7','8','9']:

            time.append(x)
            x = ''
        else:
            x+=s[i]

    time.append(x)
    
    if len(time)==2:
        t = "0:"+str(int(time[0])//60)+":"+str(int(time[0])%60)+':'+time[1]
    
    elif len(time)==3:
        t = "0:"+ time[0]+':' +time[1]+':'+time[2]
    
    elif len(time)==4:
        t = time[0]+':' +time[1]+':'+time[2]+':'+time[3]
    
    else:
        raise("ValueError")
    
    init_t = "0:0:0:0"
    init_t = datetime.strptime(init_t,"%H:%M:%S:%f")
    t = datetime.strptime(t,"%H:%M:%S:%f")
    t = t-init_t
    return(t.total_seconds())

def string_converter_dist(s):

    dist=[]
    x=''
    for i in range(len(s)):
        if s[i] not in ['0','1','2','3','4','5','6','7','8','9']:
            dist.append(int(x))
            x=''
        else:
            x+=s[i]
    dist.append(int(x))
    if len(dist)==2:
        return(dist[0]+dist[1]/100)
    else:
        raise("ValueError")
    
def time_converter_string(t):
    t = round(t*100)/100
    h = t//3600
    m = int((t%3600)//60)
    s = str(int(t%60*100)/100)
    if int(s)<10:
        s = '0'+s
    if h>0:
        return(str(h)+"'"+str(m)+"'"+s)
    
    elif m>0:
        return(str(m)+"'"+s)
    else:
        return(s)

def dist_converter_string(d):
    d = round(d*100)/100
    return(str(d))

class athle_regressor(): #IAAF 2017 points calculator
    def __init__(self):
        self.constants = {'100mM':(-17,24.63,0),'200mM':(-35.5,5.08,0),'400mM':(-79,1.021,0),
        '800mM':(-182,0.198,0),'1500mM':(-385,0.04066,0),'3000mM':(-840,0.00815,0),
        '110mHM':(-25.8,7.66,0),'400mHM':(-95.5,0.546,0),'3000mscM':(-1020,0.004316,0),
        '5000walkM':(-2760,0.000436,0),'highM':(11.534,32.29,-5000),'poleM':(39.39,3.042,-5000),
        'longM':(48.41,1.929,-5000),'tripleM':(98.63,0.4611,-5000),'shotM':(687.7,0.042172,-20000),
        'discM':(2232.6,0.004007,-20000),'hammerM':(2669.4,0.0028038,-20000),'javM':(2886.8,0.0023974,-20000),
        '100mW':(-22,9.92,0),'200mW':(-45.5,2.242,0),'400mW':(-110,0.335,0),'800mW':(-250,0.0688,0),
        '1500mW':(-540,0.0134,0),'3000mW':(-1200,0.002539,0),'100mHW':(-30,3.98,0),'400mHW':(-130,0.208567,0),
        '3000walkW':(-1871,0.000881,0),'highW':(10.574,39.34,-5000),'poleW':(34.83,3.953,-5000),
        'longW':(49.24,1.966,-5000),'tripleW':(105.53,0.4282,-5000),'shotW':(657.53,0.0462,-20000),
        'discW':(2227.3,0.0040277,-20000),'hammerW':(2540,0.0030965,-20000),'javW':(2214.9,0.004073,-20000),
        '300mM':(-57.2,1.83,0),'600mM':(-131,0.367,0),'1000mM':(-240,0.1074,0),'1mileM':(-415,0.0351,0)
        ,'2000mM':(-528,0.02181,0),'2milesM':(-904.8,0.00703,0),'5000mM':(-1440,0.002778,0),'10000mM':
        (-3150,0.000524,0),'2000mscM':(-660,0.01023,0),'4x100mM':(-69.5,1.236,0),'4x200mM':(-144,0.29767,0),
        '4x400mM':(-334,0.05026,0),'3000walkM':(-1650,0.001209,0),'decaM':(71170,0.00000097749,-5000),
        '300mW':(-77,0.7,0),'600mW':(-184,0.1192,0),'1000mW':(-330,0.0382,0),'1mileW':(-580,0.01165,0),
        '2000mW':(-750,0.006766,0),'2milesW':(-1296.3,0.002157,0),'5000mW':(-2100,0.000808,0),'10000mW':
        (-4500,0.0001712,0),'3000mscW':(-1510,0.001323,0),'2000mscW':(-880,0.0045,0),'4x100mW':(-98,0.3895,0),'4x200mW':
        (-212,0.0795,0),'4x400mW':(-480,0.01562,0),'5000walkW':(-3140,0.0003246,0),'heptaW':
        (55990,0.000001581,-5000),'pentaWi':(41033,0.0000029445,-5000),'heptaMi':(53175,0.000001752,-5000),
        '50mMi':(-9.2,95.8,0),'60mMi':(-10.7,68.6,0),'200mMi':(-36,5.04,0),'300mMi':(-58,1.803,0),
        '400mMi':(-80.6,0.981,0),'600mMi':(-131,0.39,0),'800mMi':(-184,0.1974,0),'1000mMi':(-240,0.1139,0),
        '1500mMi':(-386,0.042,0),'1mileMi':(-415,0.0369,0),'3000mMi':(-840,0.008322,0),'5000mMi':(-1440,0.0029,0),
        '50mHMi':(-12.35,34.2,0),'60mHMi':(-14.6,23.9,0),'highMi':(11.534,32.29,-5000),'poleMi':(39.39,3.042,-5000),
        'longMi':(48.41,1.929,-5000),'tripleMi':(98.63,0.4611,-5000),'shotMi':(687.7,0.042172,-20000),
        '50mWi':(-12.1,33.03,0),'60mWi':(-14,24.9,0),'200mWi':(-47.5,1.962,0),'300mWi':(-79,0.6595,0),
        '400mWi':(-112,0.3224,0),'600mWi':(-190.35,0.1063,0),'800mWi':(-264,0.0572,0),
        '1000mWi':(-340.4,0.03473,0),'1500mWi':(-540,0.01365,0),'1mileWi':(-585.5,0.01154,0),
        '3000mWi':(-1200,0.00259,0),'5000mWi':(-2100,0.000825,0),'50mHWi':(-15.3,16.2,0),
        '60mHWi':(-18.2,11.16,0),'highWi':(10.574,39.34,-5000),'poleWi':(34.83,3.953,-5000),
        'longWi':(49.24,1.966,-5000),'tripleWi':(105.53,0.4282,-5000),'shotWi':(657.53,0.0462,-20000)}
    
    
    def reg(self,event,perf): #perf given in seconds or meters or 'o' for no perf
        if perf.lower().split(' ')[0] in ['o','','dq','dns','dnf','nm','nc','ab','x','0','*hb*','='] or 'inv' in perf.lower(): #no perf
            return(0)
        resultShift,conversionFactor,pointShift = self.constants[event]
        if event in ['highM','poleM','longM','tripleM','shotM','discM','hammerM','javM','highW','poleW','longW','tripleW','shotW','discW','hammerW','javW','highMi','poleMi','longMi','tripleMi','shotMi','highWi','poleWi','longWi','tripleWi','shotWi']:
            perf = string_converter_dist(perf)
        elif event in ['decaM','heptaW','heptaMi','pentaWi']: #combined events points to hungarian points
            perf = int(perf)
        else:
            perf = string_converter_time(perf)
            if perf > abs(resultShift):
                return(0)
        
        pointz = int(conversionFactor*(perf+resultShift)**2 + pointShift)
        return(pointz)#,perf)
    
    def inv(self,event,points):
        #x = -b+-sqrt(d) / 2a
        resultShift,conversionFactor,pointShift = self.constants[event]
        if points==0:
            return(0)
        
        a = conversionFactor
        b = conversionFactor*2*resultShift
        c = conversionFactor*resultShift**2+pointShift
        d = b**2-4*a*(c-points)
        
        if event in ['highM','poleM','longM','tripleM','shotM','discM','hammerM','javM','highW','poleW','longW','tripleW','shotW','discW','hammerW','javW','highMi','poleMi','longMi','tripleMi','shotMi','highWi','poleWi','longWi','tripleWi','shotWi']:
            
            x = (-b+sqrt(d)) / (2*a)
            return(dist_converter_string(x))
        elif event in ['decaM','heptaW','heptaMi','pentaWi']:
            x = (-b+sqrt(d)) / (2*a)
            return(dist_converter_string(x))
        else:
            x = (-b-sqrt(d)) / (2*a)
            return(time_converter_string(x))


def clean_up_perf(perf,event):
    if perf.lower().split(' ')[0] in ['o','','dq','dns','dnf','nm','nc','ab','x','0','*hb*','='] or 'inv' in perf.lower():
        return('o')
    perf = perf.split("''")
    if len(perf)>=2:
        j=0
        while j<len(perf):
            if perf[j]=='': #'' at the end of the string
                perf = perf[0:j]+["'"]+['00']
                break
            else: #'' in the middle of the string
                if j+1<len(perf):
                    if perf[j+1]!='':
                        perf = perf[0:j+1]+["'"]+perf[j+1:]
                        j+=2
                    else:
                        perf = perf[0:j+1]+perf[j+1:]
                        j+=1

                else:
                    break

            #j+=1
        s = ''
        for j in range(len(perf)):
            s+=perf[j]
        perf=s

    else:
        perf = perf[0]
    if perf[0]=='m':
        perf = '0'+perf
    if perf[-1]=="'": #marker at the end of the string : add hundredths
        perf = perf+'00'

    #print(perf)

    #Handle combined events and spaces
    if event in ["pentaWi","heptaWi","heptaW","pentaW","pentaM","pentaMi","decaM","heptaM","heptaMi","triaW","triaM","triaWi","triaMi"]:
        s = perf.split(' ')
        if len(s)==2: #121 pts -> 121
            if s[1]=="pts": 
                perf = s[0]
            else: #7 000 -> 7000
                perf = s[0]+s[1]
        elif len(s)==3:
            if s[1]=="pts": #121 pts blabla -> 121
                perf = s[0]
            elif s[2] == "pts": #7 000 pts -> 7000
                perf = s[0]+s[1]
            else: #7 000 blabla -> 7000
                perf = s[0]+s[1]
    else:
        perf = perf.split(' ')[0] #8m95 blabla (+1.7) -> 8m95

    return(perf)


#test
