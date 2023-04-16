import pandas as pd
import matplotlib.pyplot as plt

#POBIRANJE PODATKOV=========================================================================================
def scrape_table_data(url, table_index, column_names=None, selected_columns=None):
    """
    Pobira podatke iz HTML tabel na spletni strani.

    Argumenti:
    url (str): URL spletne strani, iz katere pobiramo podatke.
    table_index (int): Indeks tabele na spletni strani od 0 do n.
    column_names (list): Seznam imen stolpcev, ki jih bomo uporabili.
    selected_columns (list): Seznam strolpcev, ki jih bomo uporabili (če ne želimo vseh stolpcev).

    Vrne:
    Slovar slovarjev ki ima pobrane podatke z ključi ki predstavljajo št. vrstice in vrednostmi ki
    predstavljajo podatke v določeni vrstici
    """

    # Uporabi pandas da prevede HTML tabelo v DataFrame
    tables = pd.read_html(url, header=0)
    table = tables[table_index]

    # Preimenuje stolpce v podana imena
    if column_names is not None:
        name_map = {table.columns[i]: col_name for i, col_name in enumerate(column_names)}
        table = table.rename(columns=name_map)

    # Izbere željene stolpce
    if selected_columns is not None:
        table = table.iloc[:, selected_columns]

    # Prevede DataFrame v slovar slovarjev
    data_dict = {}
    for i in range(len(table)):
        row_dict = {}
        for j, col_name in enumerate(column_names):
            row_dict[col_name] = table.iloc[i, j]
        data_dict[i] = row_dict

    return data_dict

#KLUBI==========================================================================================================
def bar_chart_klubi():
    url = 'https://en.wikipedia.org/wiki/UEFA_Champions_League'
    table_index = 4
    selected_columnss = [0, 1, 2]
    column = ['Club', 'Title(s)', 'Runners-up']
    data_klubi = scrape_table_data(url, table_index, column, selected_columnss)

    klubi = [data_klubi[i]['Club'] for i in data_klubi]
    titles = [data_klubi[i]['Title(s)'] for i in data_klubi]
    total = [data_klubi[i]['Title(s)'] + data_klubi[i]['Runners-up'] for i in data_klubi]

    plt.rcParams['toolbar'] = 'None'
    fig1,ax = (plt.subplots(num = 'UEFA Clubs',figsize =(16, 10)))

    p1 = ax.barh(klubi, total)
    ax.barh(klubi, titles)

    # Odstrane okvire
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)
 
    # Odstrane x,y črtice
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')

    # Mreža
    ax.grid(color ='grey',
            linestyle ='-.', linewidth = 0.5,
            alpha = 0.2)

    # Zamenjamo vrednosti
    ax.invert_yaxis()

    #Notacija ob stolpcih
    for i in p1.patches:
        plt.text(i.get_width()+0.2, i.get_y() + 0.7,
                    str(round((i.get_width()), 2)),
                    fontsize = 10, fontweight ='bold',
                    color ='#A9A9A9')

    # Naslov
    ax.set_title('Nastopi v Evropskem pokalu in UEFA Ligi prvakov po klubih',
             loc ='center', )

    #Legenda
    plt.legend(['Število finalnih tekem', 'Število zmag'],loc = "lower right", frameon = True, fontsize = 15)
    plt.show()
    
#DRŽAVE==========================================================================================================
def bar_chart_drzave():
    url = 'https://en.wikipedia.org/wiki/UEFA_Champions_League'
    table_indexx = 5
    columnn = ['Nation' ,'Titles', 'Total']
    selected_columns=[0, 1,3]
    data_drzave = scrape_table_data(url, table_indexx, columnn ,selected_columns)

    drzave = [data_drzave[i]['Nation'] for i in data_drzave] #države
    Y = [data_drzave[i]['Total'] for i in data_drzave] 
    Z = [data_drzave[i]['Titles'] for i in data_drzave]

    fig2,ax =(plt.subplots(num = 'UEFA by Nations',figsize = (16, 9)))

    ax.barh(drzave, Y)
    ax.barh(drzave, Z)

    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)
 
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')

    ax.grid(color ='grey',
            linestyle ='-.', linewidth = 0.5,
            alpha = 0.2)

    ax.invert_yaxis()

    for i in ax.patches:
        plt.text(i.get_width()+0.2, i.get_y()+0.5,
                    str(round((i.get_width()), 2)),
                    fontsize = 10, fontweight ='bold',
                    color ='#A9A9A9')

    ax.set_title('Nastopi v finalu po državah',
                 loc ='center', )

    plt.legend(['Število finalnih tekem', 'Število zmag'],loc = "lower right", frameon = True, fontsize = 15)
    plt.show()

#IGRALCI===============================================================================================================
def graf_igralci():
    url = 'https://en.wikipedia.org/wiki/UEFA_Champions_League'
    table_indexxx = 8
    columnnn = ['Player', 'Goals', 'Apps']
    selected_columnsss=[1,2,3]
    data_igralci = scrape_table_data(url, table_indexxx, columnnn ,selected_columnsss)

    igralci = [data_igralci[i]['Player'] for i in data_igralci]
    goals = [data_igralci[i]['Goals'] for i in data_igralci]
    apps = [data_igralci[i]['Apps'] for i in data_igralci]

    fig3,ax = plt.subplots(num = 'UEFA Players',figsize = (15, 9))
    ax.scatter(goals, apps)

    for s in ['top', 'right']:
        ax.spines[s].set_visible(False)
    
    ax.grid(color ='grey',
            linestyle ='-.', linewidth = 0.5,
            alpha = 0.2)

    plt.xlabel('Število golov')
    plt.ylabel('Število nastopov')

    ax.set_title('Rezultati igralcev v UEFA Ligi prvakov',
                 loc ='center', )
    
    #Pokaže ime igralca ob točki
    for i, txt in enumerate(igralci):
        ax.annotate(txt, (goals[i], apps[i]), xytext=(0,10), textcoords='offset points')
    
    plt.show()
    
#FINALNE TEKME=================================================================================================
url2 = "https://en.wikipedia.org/wiki/List_of_European_Cup_and_UEFA_Champions_League_finals"
dat = scrape_table_data(url2,2, ['Season','Winners','Score', 'Runners-up'],[0,2 ,3, 5])
leta = [dat[i]['Season'] for i in dat]
leta.pop(0)
leta = leta[:68]

#================================================================================================
while True:
    print("Kaj vas zanima?")
    print("1. Stolpični diagram zmagovalcev po klubih")
    print("2. Stolpični diagram zmagovalcev po državah")
    print("3. Graf število golov igralca v Ligi prvakov")
    print("4. Rezultat finala")
    print("5. Zaustavitev programa")
    odg = input("Prosim vpišite število vaše izbire: ")
    if odg == "1":
        print("\n")
        bar_chart_klubi()
    elif odg == "2":
        print("\n")
        bar_chart_drzave()
    elif odg == "3":
        print("\n")
        graf_igralci()
    elif odg == "4":
        print("\n")
        print("Leta vseh finalnih tekem:\n", leta,"\n")
        leto = input("Iz seznama prekopirite letnico finala npr. 2005-06: ")
        if leto not in leta:
            print("\n")
            print("Prosim vpišite leto v veljavni obliki!")
            print("\n")
        else:    
            print("\n")
            index = leta.index(leto)+1
            if dat[index]['Winners'][-1] == 'a':
                print('Leta' ,leto, 'je' ,dat[index]['Winners'], 'premagala' ,dat[index]['Runners-up'], 'z rezultatom' ,dat[index]['Score'] + '.')
            else:
                print('Leta' ,leto, 'je' ,dat[index]['Winners'], 'premagal' ,dat[index]['Runners-up'], 'z rezultatom' ,dat[index]['Score'] + '.')
            print("\n")
    elif odg == "5":
        break
    else:
        print("\n")
        print("Vpišite število 1, 2, 3, 4, 5 ali 6!")
        print("\n")