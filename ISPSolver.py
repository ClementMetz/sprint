from auxiliary import athle_regressor
from datetime import timedelta
from datetime import datetime
import scipy.optimize as op
import numpy as np
import xlrd
import xlsxwriter
import warnings
import os
import random
import argparse

def parse_option():
    parser = argparse.ArgumentParser(description='Optimize interclubs placement')
    parser.add_argument('--workdir', type=str,default='ISPInput.xlsx',help='Workbook directory')
    args = parser.parse_args()
    return(args)



def initialize(perf,conflicts): #problem initialization
    athletes = perf.col(0)[1:]
    ath = []
    for i in range(1,len(athletes)+1):
        ath.append(perf.cell_value(i,0))
    #print(ath)

    events = perf.row(0)[1:]
    ev = []
    for i in range(1,len(events)+1):
        ev.append(perf.cell_value(0,i))
    #print(ev)

    conf = conflicts.col(0)[1:]
    nb_confs = len(conf)
    
    
    n = perf.nrows -1
    k = perf.ncols -1
    
    perfos = []
    for i in range(n):
        perfos.append([])
        for j in range(k):
            perfos[i].append("")


    for i in range(n):
        for j in range(k):
            perfos[i][j] = perf.cell_value(i+1,j+1)

    #perfos = np.random.random((n,k)).flatten() * 700
    #print(perfos)

    #Conversion with hungarian table
    hungarian_perfos = np.zeros((n,k))
    regressor = athle_regressor()
    for i in range(n):
        for j in range(k):
            hungarian_perfos[i,j] = regressor.reg(ev[j],perfos[i][j])

    #print(hungarian_perfos)

    conftable = []

    for i in range(nb_confs):
        conftable.append([])
        for j in range(k):
            conftable[i].append(conflicts.cell_value(i+1,j))

        
    conftable = np.matrix(conftable,dtype=str)
    
    
    return(ev,ath,k,n,nb_confs,perfos,hungarian_perfos,conftable)
    

def output(ev,ath,workbook,sheetname,k,n,sol,perfos,hung,solution_feasible): #output management
    format = workbook.add_format({'bold':True})
    format2 = workbook.add_format({'color': 'red','bold':True})
    center = workbook.add_format({'align':'center'})

    x = sol.x
    #opt = int(-sol.fun)
    opt = np.dot(hung.flatten(),x)

    x = x.reshape((n,k))
    success = sol.success and solution_feasible
    
    worksheet = workbook.add_worksheet("Affectation"+sheetname)
    worksheet.add_table(7, 0, n+7, k+5)
    worksheet.print_row_col_headers()
    worksheet.set_column(0,k+1,16)
    worksheet.add_table(0, 0, 5, k,{'style': 'Table Style Medium 3'})
    for i in range(1,k+1):
        worksheet.write_string(7,i,ev[i-1]) #event names
    worksheet.write_string(7,k+1,"Athlete")
    worksheet.write_string(7,k+2,"Event 1")
    worksheet.write_string(7,k+3,"Perf 1")
    worksheet.write_string(7,k+4,"Event 2")
    worksheet.write_string(7,k+5,"Perf 2")

    for j in range(1,n+1):
        worksheet.write_string(j+7,0,ath[j-1]) #athlete names
        worksheet.write_string(j+7,k+1,ath[j-1])
    
    worksheet.write_string(1,0,"Athlete 1")
    worksheet.write_string(2,0,"Perf 1")
    worksheet.write_string(3,0,"Athlete 2")
    worksheet.write_string(4,0,"Perf 2")
    worksheet.write_string(5,0,"Total")
    
    for i in range(n):
        for j in range(k):
            worksheet.write_rich_string(i+8,j+1,perfos[i][j]," → ",format2,str(int(hung[i,j])),center) #one hot encoding

    worksheet.write_number(0,0,opt,format) #total perf
    worksheet.write_number(7,0,opt,format) #total perf
    worksheet.write_string(n+9,1,"Optimization successful : "+ str(success),format)
    
    for r in range(k): #participants per event
        num=0
        tot = 0
        worksheet.write_string(0,r+1,ev[r])
        for a in range(n):
            if x[a,r]==1:
                num+=1
                worksheet.write_string(num,r+1,ath[a])
                num+=1
                tot += hung[a,r]
                worksheet.write_number(num,r+1,hung[a,r])
        worksheet.write_number(5,r+1,tot)
    
    for a in range(n): #participants per event
        num=0
        for r in range(k):
            if x[a,r]==1:
                num+=1
                worksheet.write_string(a+8,k+1+num,ev[r])
                num+=1
                worksheet.write_number(a+8,k+1+num,hung[a,r])
    """
    chart1 = workbook.add_chart({'type': 'column', 'subtype': 'stacked'})
    chart1.add_series({
    'categories': ["Affectation"+sheetname, 0, 1, 0, k],
    'values':     ["Affectation"+sheetname, 2, 1, 2, k],
    'name': "Athlete 1",
    'data_labels': {'value': True}})
    chart1.add_series({
    'categories': ["Affectation"+sheetname, 0, 1, 0, k],
    'values':     ["Affectation"+sheetname, 4, 1, 4, k],
    'name': "Athlete 2",
    'data_labels': {'value': True}})
    chart1.set_size({'width': 1000, 'height': 576})
    chart1.set_legend({'none': True})
    worksheet.insert_chart('C10', chart1)

    chart2 = workbook.add_chart({'type': 'column'})
    chart2.add_series({
    'categories': ["Affectation"+sheetname, 8, k+1, n+7, k+1],
    'values':     ["Affectation"+sheetname, 8, k+3, n+7, k+3],
    'name': "Event 1",
    'fill':   {'color': '#62BF6C'},
    'overlap':    -25,
    'data_labels': {'value': True}})
    chart2.add_series({
    'categories': ["Affectation"+sheetname, 8, k+1, n+7, k+1],
    'values':     ["Affectation"+sheetname, 8, k+5, n+7, k+5],
    'name': "Event 2",
    'fill':   {'color': '#FCF235'},
    'data_labels': {'value': True}})
    chart2.set_size({'width': 1440, 'height': 576})
    chart2.set_legend({'none': True})
    worksheet.insert_chart('G18', chart2)

    chart3 = workbook.add_chart({'type': 'pie'})
    chart3.add_series({
    'categories': ["Affectation"+sheetname, 0, 1, 0, k],
    'values':     ["Affectation"+sheetname, 5, 1, 5, k],
    'data_labels': {'value': True,'category':True},
    'label_position': 'none'})
    chart3.set_size({'width': 750, 'height': 750})
    chart3.set_legend({'none': True})
    worksheet.insert_chart('E15', chart3)
    """
    
    
    worksheet = workbook.add_worksheet("HungarianTable"+sheetname)
    worksheet.add_table(0, 0, n, k)
    worksheet.print_row_col_headers()
    worksheet.set_column(0,k,16)
    worksheet.write_number(0,0,opt,format) #total perf
    for i in range(1,k+1):
        worksheet.write_string(0,i,ev[i-1]) #event names

    for j in range(1,n+1):
        worksheet.write_string(j,0,ath[j-1]) #athlete names
    
    for i in range(n):
        for j in range(k):
            worksheet.write_number(i+1,j+1,hung[i,j]) #hungarian scores
    
    worksheet.conditional_format(1, 1, n, k, {'type': '2_color_scale','min_color': '#62BF6C',
                                        'max_color': '#FCF235'})
    
    
        

    
    
    

def optim(perf,conflicts,ev,ath,k,n,nb_confs,hungarian_perfos,conftable):

    
    #Affectation computation
    
    criterion = - hungarian_perfos

    #add random perturbations to force convergence to a vertex of the simplex

    for i in range(n):
        for j in range(k):
            if criterion[i,j]!=0:
                criterion[i,j]+=random.random()/100
    
    criterion = criterion.flatten()

    Aub = np.zeros((n+k+nb_confs*n,n*k))

    for i in range(n): #lignes athlètes
        for r in range(k):
            Aub[i,i*k+r] = 1

    for j in range(0,k): #lignes épreuves
        for s in range(n):
            Aub[n+j,s*k+j] = 1

    for c in range(0,nb_confs): #lignes conflits
        for s in range(n):
            Aub[n+k+nb_confs*s+c,s*k:(s+1)*k] = conftable[c,:]




    bub = np.ones(n+k+nb_confs*n)
    bub[:n+k] = 2

    l = 0
    u = 1

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sol = op.linprog(criterion,Aub,bub,bounds = (l,u),options = {'disp':True}) #,method = 'simplex'
    
    x = sol.x
    x[x<=0.5]=0
    x[x>0.5] = 1
    
    if np.all(np.less_equal(np.dot(Aub,x),bub)):
        solution_feasible = True
    else:
        print("Constraint violated")
        solution_feasible = False
    
    sol.x = x
    return(sol,solution_feasible)
    


def main():
    opt = parse_option()
    table = xlrd.open_workbook(opt.workdir)
    perfM = table.sheet_by_name("PerfM")
    perfW = table.sheet_by_name("PerfW")
    conflictsM = table.sheet_by_name("EventConflictsM")
    conflictsW = table.sheet_by_name("EventConflictsW")
    print("----------Men's problem initialization-------------")
    ev,ath,k,n,nb_confs,perfos,hung,conf = initialize(perfM,conflictsM)
    print("----------Men's problem resolution-------------")
    sol,solution_feasible = optim(perfM,conflictsM,ev,ath,k,n,nb_confs,hung,conf)
    print("----------Men's solution found-------------")
    workbook = xlsxwriter.Workbook('ISPSolution.xlsx')
    output(ev,ath,workbook,"M",k,n,sol,perfos,hung,solution_feasible)
    print("----------Women's problem initialization-------------")
    ev,ath,k,n,nb_confs,perfos,hung,conf = initialize(perfW,conflictsW)
    print("----------Women's problem resolution-------------")
    sol,solution_feasible = optim(perfW,conflictsW,ev,ath,k,n,nb_confs,hung,conf)
    print("----------Women's solution found-------------")
    output(ev,ath,workbook,"W",k,n,sol,perfos,hung,solution_feasible)
    workbook.close()

if __name__ == '__main__':
    main()
