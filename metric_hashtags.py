#imports
import math
import random
from collections import Counter
from collections import defaultdict
import csv

KMeans=False
try:
    from sklearn.cluster import KMeans
except ImportError:
    print("pip install sklearn")

plotly = False
try:
    import plotly
    import plotly.graph_objs as go
    from plotly import tools
    import matplotlib.pyplot as plt
except ImportError:
    print("Plotly ist nicht installiert. pip install plotly")

numpy=False
try:
    import numpy
except ImportError:
    print("numpy ist nicht installiert. pip install numpy")

affinegap=False
try:
    import affinegap
except ImportError:
    print("affinegap ist nicht installiert. Berechnung der Distanzen kann nicht ausgeführt werden. pip install affinegap")

psycopg2=False
try:
    import psycopg2
except ImportError:
    print("psycopg2 nicht installiert. Verbindung zur Datenbank nicht möglich. pip install psycopg2")

#Funktionen
def distancematrix(x, matchweight, missmatchweight, gap_ext_weight):
    '''Einagbe: Liste der Hashtags, matchweight, mismatchweight, Kosten für Verlängerung von gaps
       Ausgabe: Ähnlichkeitsmatrix'''
    E = numpy.zeros((len(x),len(x)))
    for i in range(0,len(x)-1):
        for j in range(0,len(x)-1):
            if x[i] == x[j]:
                E[i,j]= 1
            else:
                dist = affinegap.affineGapDistance(x[i], x[j], matchWeight = matchweight, mismatchWeight = missmatchweight, gapWeight =0 , spaceWeight=gap_ext_weight, abbreviation_scale = 0)
                if len(x[i])>len(x[j]):
                    E[i,j]= (-1)*dist/len(x[j])
                else:
                    E[i,j]= (-1)*dist/len(x[i])
    return E

def heatplot(z,x,y):
    """Einagbe: Matrix der Distanzen, Vektoren für x und y"""
    layout = go.Layout(
        title='Ähnlichkeit Hashtags',
        xaxis = dict(nticks=150),
        yaxis = dict(nticks = 100 ))
    trace = go.Heatmap(z=z, x=x, y=y)
    data=[trace]
    figure = go.Figure(data = data,layout = layout)
    plotly.offline.plot(figure, filename='basic-heatmap.html')

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

def main():
    # connect PostgreSQL
    sql = "SELECT * FROM hashtag;"
    raw_dat = get_data_postgres("localhost", "election","postgres","postgres","5432", sql)
    data = []
    #tuple zu Liste
    for i in range(len(raw_dat)):
        data.append(raw_dat[i][0])

    #Auswertung
    E = distancematrix(data, -1, 1, 0.5)

    kmeans = KMeans(n_clusters=25, random_state=0).fit(E)
    clusters = kmeans.labels_

    #Hashtags den Clustern zuordnen
    data_cluster_dict = defaultdict(list)
    for h,c in zip(data,clusters):
        data_cluster_dict[c].append(h)

    #plots
    heatplot(E,data,data)
    cluster_dict={}
    for c,h in zip(clusters,data):
            cluster_dict.update({h:c})

    #Export, da kein Bock.
    with open('dict.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        for key, value in cluster_dict.items():
            writer.writerow([key, value])
    with open('dict_cluster.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        for key, value in data_cluster_dict.items():
            writer.writerow([key, value, len(data_cluster_dict[key])])

if __name__ == "__main__": main()
