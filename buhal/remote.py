#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os, configparser, MySQLdb
from datetime import datetime, date

config = configparser.RawConfigParser()
config.read(os.path.abspath(os.curdir) + '/djangobuhalteria/config.cfg')
#config.read('/home/earth/PycharmProjects/djangobuhalteria/djangobuhalteria/config.cfg')

MySQLUser = config.get('MySQL', 'User')
MySQLPass = config.get('MySQL', 'Pass')
MySQLDatabase = config.get('MySQL', 'Database')
MySQLHost = config.get('MySQL', 'Host')

def check_host(host):
    response = os.system("ping -c 1 -W 1 " + host)
    if response == 0:
        return True
    else:
        return False

def cr_table_prefix(come_date):
    cmon = come_date.month
    if cmon < 10:
        return "{}0{}".format(come_date.year, cmon)
    else:
        return "{}{}".format(come_date.year, cmon)
    
def check_table(table_name):
    cnx   = MySQLdb.connect(user=MySQLUser, passwd=MySQLPass, db=MySQLDatabase, host=MySQLHost, charset="cp1251", use_unicode = True)
    cursor = cnx.cursor()
    cursor.execute("SHOW TABLES LIKE '{}'".format(table_name))
    if cursor.fetchone():
        cursor.close()
        cnx.close()  
        return True
    else:
        cursor.close()
        cnx.close()          
        return False    
    
def delta_mount(range_data = '202101', delta = -1):
    try:
        year = int(range_data[:4])
        mount = int(range_data[4:])
        all_mount = year*12 + mount + delta
        year = round(all_mount/12-0.5)
        mount = all_mount - year*12
        if mount < 10:
            return "{}0{}".format(year, mount)
        else:
            return "{}{}".format(year, mount)
    except:
        return False

def nav_mounth_scroll(range_data = 0):
    table_prefix_scroll = []
    now_date = datetime.today()
    if range_data == '0':
        range_data = cr_table_prefix(now_date)
        range_data = delta_mount(range_data, -1)
    table_prefix_scroll.append(range_data)
    table_prefix_scroll.append(True)
    table_prefix_scroll.append(datetime.strptime(range_data, "%Y%m"))
    range_d = delta_mount(range_data, -1)
    if check_table("log_session_8_{}".format(range_d)):
        table_prefix_scroll.append(range_d)
        table_prefix_scroll.append(True)
    else:
        table_prefix_scroll.append(range_d)
        table_prefix_scroll.append(False)
    range_d = delta_mount(range_data, 1)
    if check_table("log_session_8_{}".format(range_d)):
        table_prefix_scroll.append(range_d)
        table_prefix_scroll.append(True)
    else:
        table_prefix_scroll.append(range_d)
        table_prefix_scroll.append(False)
    return table_prefix_scroll   

def my_mount(mount):
    try:
        if mount < 10:
            return ("0{}".format(mount))
        else:
            return ("{}".format(mount))
    except:
        return False

def bill_groups():
    cnx   = MySQLdb.connect(user=MySQLUser, passwd=MySQLPass, db=MySQLDatabase, host=MySQLHost, charset="cp1251", use_unicode = True)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM contract_group CG WHERE CG.`enable` = 1")
    my_result = cursor
    cursor.close()
    cnx.close()
    return my_result

def TTK_summ(range_data = '201909'):
    #range_data = range_data.decode()
    cnx   = MySQLdb.connect(user=MySQLUser, passwd=MySQLPass, db=MySQLDatabase, host=MySQLHost, charset="cp1251", use_unicode = True)
    cursor = cnx.cursor()
    mySQL = """SELECT sum(LS.oper_session_cost)
                FROM log_session_8_{} LS, contract_tariff CT
                WHERE LS.sid <> 2
                    AND LS.cid = CT.cid
                    AND (CT.tpid=88 OR CT.tpid=95) /* Код тарифа  TTK-95,88 Ростелеком-137*/""".format(range_data)
    cursor.execute(mySQL)
    for i in cursor:
        summ = i
    cursor.close()
    cnx.close()    
    return round(summ[0],2)

def RTK_summ(range_data = '201909'):
    cnx   = MySQLdb.connect(user=MySQLUser, passwd=MySQLPass, db=MySQLDatabase, host=MySQLHost, charset="cp1251", use_unicode = True)
    cursor = cnx.cursor()
    mySQL = """SELECT sum(LS.oper_session_cost)
            FROM log_session_8_{} LS, contract_tariff CT
            WHERE LS.sid <> 2
                AND LS.cid = CT.cid
                AND CT.tpid=145 /* Код тарифа  TTK-95,88 Ростелеком-137 Ростелеком-145*/""".format(range_data) 
    cursor.execute(mySQL)
    for i in cursor:
        summ = i
    cursor.close()
    cnx.close()    
    return round(summ[0],2)
    
def TTK_all(range_data):
    YEAR = int(range_data[:4])
    MOUNHT = range_data[4:]
    my_table = []
    cnx   = MySQLdb.connect(user=MySQLUser, passwd=MySQLPass, db=MySQLDatabase, host=MySQLHost, charset="cp1251", use_unicode = True)
    cursor = cnx.cursor()
    forsed_scripts_query = """ SELECT
            concat_ws('',NAIMENOVANIE.`val`, FIO.`val`) as NAIMENOVANIE,    /*Наименование*/
            c.title as Contract_N,                                             /*Номер договора*/
            DateOfContract.`val` as Date_zakluch,                             /*Дата заключения договора*/
            INN.`val` as INN,                                                /*ИНН*/
            KPP.`val` as KPP,                                                /*КПП*/
            bl.`format_number` as Doc_N,                                    /*Номер счета-фактуры*/
            bl.`create_dt` Date_SF,                                         /*Дата СФ*/
            round(sum(LogS.`session_cost`)/1.2,2) as summ,                    /*Сумма по счету без НДС*/ /*round(bl.`summ`/1.18,2)*/
            LogS.`zone` as Usluga,                                            /*Тип услуги 2-МГ 4-МН*/
            round(sum(LogS.`session_cost`)/1.2,2) as Dohod_non_NDS,        /*Начисленный доход без НДС*/
            round(sum(LogS.`session_cost`),2) as Dohod,                        /*Начисленный доход с НДС*/
            round(sum(LogS.`oper_session_cost`),2) as Usl_Summ_non_NDS,        /*Условная стоимость без НДС*/
            round(sum(LogS.`oper_session_cost`)*1.2,2) as Usl_Summ,        /*Условная стоимость с НДС*/
            round(sum(LogS.`session_cost`)/1.2 - sum(LogS.`oper_session_cost`),2) as Voznag_non_NDS,    /*Вознаграждение без НДС*/
            round(sum(LogS.`session_cost`) - sum(LogS.`oper_session_cost`)*1.2,2) as Voznag             /*Вознаграждение с НДС*/
        FROM `log_session_8_{0}{1}` /* МЕСЯЦ и ГОД */ LogS, `bill_invoice_data_14` bl
             LEFT JOIN `contract_parameter_type_1` NAIMENOVANIE ON (NAIMENOVANIE.`cid` = bl.`cid` AND NAIMENOVANIE.`pid` = 10)
             LEFT JOIN `contract_parameter_type_1` FIO ON (FIO.`cid` = bl.`cid` AND FIO.`pid` = 33)
             LEFT JOIN `contract_parameter_type_6` DateOfContract ON (DateOfContract.`cid` = bl.`cid` AND DateOfContract.`pid` = 8)
             LEFT JOIN  `contract_parameter_type_1` INN ON (bl.`cid` = INN.`cid` AND INN.`pid` = 25 )
             LEFT JOIN  `contract_parameter_type_1` KPP ON (bl.`cid` = KPP.`cid` AND KPP.`pid` = 32 )
             LEFT JOIN  `contract` c  ON bl.`cid` = c.`id`
        WHERE   
            bl.`yy`={0} /* ГОД */
            AND bl.`mm`={2} /* МЕСЯЦ - 1 */
            AND bl.`type` = 11
            AND bl.`cid` = LogS.`cid`
            AND (LogS.`zone` = 4 OR LogS.`zone` = 2) 
            AND LogS.`session_cost` > 0
        GROUP BY LogS.`cid`, LogS.`zone`
        ORDER BY bl.`format_number`
        limit 500 """.format(YEAR, my_mount(int(MOUNHT)), my_mount(int(MOUNHT) - 1))
    cursor.execute(forsed_scripts_query)
    for row in cursor:
        k = []
        for i in range(0, len(row)):
            if row[i]:
                if isinstance(row[i], date):
                    k.append(row[i].strftime("%d-%m-%Y")) #strftime("%A, %d. %B %Y %I:%M%p")
                else:
                    k.append(row[i])
            else:
                k.append("")                            
        my_table.append(k)
    cursor.close()
    cnx.close()
    return my_table

def SQL_to_CSV(mySQLQuery = "SELECT * FROM contract limit 10", numeric = False):
    cnx = MySQLdb.connect(user=MySQLUser, passwd=MySQLPass, db=MySQLDatabase, host=MySQLHost, charset="cp1251", use_unicode = True) #charset="cp1251",
    cursor = cnx.cursor()
    cursor.execute(mySQLQuery)
    my_result = []
    my_row = []
    num = 0
    for row in cursor:
        num += 1
        if numeric:
            my_row.append(num)
        for i in row:
            my_row.append(i)
        my_result.append(my_row)
        my_row = []
    cursor.close()
    cnx.close()
    return my_result