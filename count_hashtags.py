from collections import defaultdict

psycopg2=False
try:
    import psycopg2
except ImportError:
    print("psycopg2 nicht installiert. Verbindung zur Datenbank nicht möglich. pip install psycopg2")

plotly = False
try:
    import plotly
    import plotly.graph_objs as go
    from plotly import tools
    import matplotlib.pyplot as plt
except ImportError:
    print("Plotly ist nicht installiert. Ausgabe von Grafiken nicht moeglich. \n pip install plotly")

#Funktionen
def get_data_postgres(h,db,u,pa,po,sql):
    conn = None
    try:
        print("Connect to Database")
        conn = psycopg2.connect(host=h, database=db, user=u, password=pa, port=po)
        cur = conn.cursor()
        cur.execute(sql)
        raw_dat = cur.fetchall()
        cur.close
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    return raw_dat

def set_values(datelist):
    xls = []
    ydt = {}
    for date in datelist:
        if date not in xls:
            xls.append(date)
            ydt.update({date:1})
        else:
            ydt[date]+=1
    yls = []
    for date in xls:
        yls.append(ydt[date])
    return xls,yls

def main():
    #Daten beziehen und vorbereiten
    #Auf das Datum reduziert, da sonst zu viele Datenpunkte
    sql="SELECT tweet.time::timestamp::date, contains.label FROM tweet INNER JOIN contains ON tweet.id = contains.id;"
    hashtags_by_date_ls = get_data_postgres("localhost", "election","postgres","postgres","5432", sql)

    hashtags_by_date_dict = defaultdict(list)
    for d,h in hashtags_by_date_ls:
        hashtags_by_date_dict[d].append(h)

    date_by_hashtags_dict = defaultdict(list)
    for d,h in hashtags_by_date_ls:
        date_by_hashtags_dict[h].append(d)

    #Traces vorbereiten
    traces=[]
    for i in date_by_hashtags_dict.keys():
        x,y = set_values(date_by_hashtags_dict[i])
        trace = go.Bar( x = x, y = y, name = i)

        traces.append(trace)

    #Plotten
    data=traces
    fig = go.Figure(data=data)
    plotly.offline.plot(data)

if __name__ == '__main__':
    main()
