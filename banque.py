import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime, os




def import_csv():
    csv_files = [f"compte/{file}" for file in os.listdir("compte/") if file.endswith('.csv')]
    if not csv_files:
        raise FileNotFoundError("Aucun fichier CSV trouvé dans le répertoire compte/")

    df = pd.DataFrame()
    for file_name in csv_files:
        print(f"Importation du fichier {file_name}")
        temp_df = pd.read_csv(file_name, sep=';', encoding='ISO-8859-1')
        clean_csv(temp_df)
        df = pd.concat([df, temp_df]).drop_duplicates()

    df['Date operation'] = pd.to_datetime(df['Date operation'], format='%d/%m/%Y')
    df = df.sort_values(by='Date operation', ascending=True)
    df = df.reset_index(drop=True)

    return df



def clean_csv(df):
    cols_to_drop = ['Date de comptabilisation', 'Libelle operation', 'Reference', 'Informations complementaires', 'Date de valeur', 'Pointage operation', 'test']
    df.drop(columns=[col for col in cols_to_drop if col in df.columns], inplace=True, errors='ignore')

    for montant in ['Debit', 'Credit']:
        df[montant] = df[montant].str.replace(',', '.').astype(float)

    df['Date operation'] = pd.to_datetime(df['Date operation'], format='%d/%m/%Y')
    df.sort_values(by='Date operation', inplace=True)




def create_file_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)



def depenses_revenus_par_mois(compte):

    compte['Date operation'] = pd.to_datetime(compte['Date operation'])
    compte['Mois'] = compte['Date operation'].dt.month
    compte['Annee'] = compte['Date operation'].dt.year

    depenses_par_mois = compte.groupby(['Annee', 'Mois'])['Debit'].sum().abs()
    revenus_par_mois = compte.groupby(['Annee', 'Mois'])['Credit'].sum().abs()
    depenses_par_mois = depenses_par_mois.reset_index()
    revenus_par_mois = revenus_par_mois.reset_index()
    depenses_par_mois['Date'] = depenses_par_mois['Annee'].astype(str) + "-" + depenses_par_mois['Mois'].astype(str)
    revenus_par_mois['Date'] = revenus_par_mois['Annee'].astype(str) + "-" + revenus_par_mois['Mois'].astype(str)
    finances_par_mois = pd.merge(depenses_par_mois, revenus_par_mois, on='Date', suffixes=('_dep', '_rev'))

    dates = finances_par_mois['Date']
    depenses = finances_par_mois['Debit']
    revenus = finances_par_mois['Credit']

    x = range(len(dates))
    width = 0.35
    plt.figure(figsize=(12, 6))
    plt.bar(x, depenses, width=width, label='Dépenses', color='red')
    plt.bar([p + width for p in x], revenus, width=width, label='Revenus', color='green')
    plt.xlabel('Mois')
    plt.ylabel('Montant')
    plt.title('Comparaison des dépenses et revenus par mois')
    plt.xticks([p + width / 2 for p in x], dates, rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"figures/depenses_revenus_par_mois.png")




def nombre_transations_par_categorie(compte):
    
    operation_counts = compte['Categorie'].value_counts()

    plt.figure(figsize=(20, 15))
    operation_counts.plot(kind='bar')
    plt.title('Répartition des types d\'opérations')
    plt.xlabel('Type d\'opération')
    plt.ylabel('Nombre de transactions')
    plt.xticks(rotation=45)
    plt.savefig(f"figures/nombre_transactions_par_categorie.png")




def montant_depenses_par_categorie(compte):
    
    total_depenses_par_categorie = compte.groupby('Categorie')['Debit'].sum().abs()
    total_depenses_par_categorie = total_depenses_par_categorie[total_depenses_par_categorie > 0]
    total_depenses_par_categorie = total_depenses_par_categorie.sort_values(ascending=False)
    
    plt.figure(figsize=(10, 10))
    plt.xticks(rotation=45)
    plt.bar(total_depenses_par_categorie.index, total_depenses_par_categorie)
    plt.title("Répartition des dépenses par catégorie")
    plt.savefig(f"figures/montant_depenses_par_categorie.png")
    plt.clf()




def evolution_solde(compte, current_balance, show_graph):
    
    tab_balance = [current_balance]
    tab_dates = [datetime.datetime.now().strftime("%d/%m/%Y")]
    
    # On compte à l'envers
    for index, depense in compte.iloc[::-1].iterrows():
        if depense['Debit'] < 0:
            current_balance -= depense['Debit']  # Ajouter le débit car il est négatif
        else:
            current_balance -= depense['Credit']  # Soustraire le crédit
        current_balance = round(current_balance, 2)
        tab_balance.append(current_balance)
        tab_dates.append(datetime.datetime.strftime(depense['Date operation'], "%d/%m/%Y"))

    # Inverser pour bien afficher le temps
    tab_balance.reverse()
    tab_dates.reverse()
    
    _, ax = plt.subplots()
    ax.plot(tab_dates, tab_balance)
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Balance")
    plt.title("Évolution du solde du compte")
    plt.tight_layout()
    if show_graph:
        plt.show()
    else:
        plt.savefig(f"figures/evolution_solde.png", dpi=400)
    plt.clf()




def analyse_data(current_balance, show_graph):

    compte = import_csv()

    create_file_if_not_exists("figures")
    
    # 1. Evolution du solde du compte
    evolution_solde(compte, current_balance, show_graph)

    # 2. Répartition des dépenses par catégorie
    montant_depenses_par_categorie(compte)

    # 3. Répartition des types d'opérations
    nombre_transations_par_categorie(compte)

    # 4. Ratio des dépenses par mois
    depenses_revenus_par_mois(compte)

    print("Analyse terminée ! Graphiques sauvegardés dans le dossier 'figures'")




if __name__ == "__main__":

    solde_courant = 1000
    show_graph = True
    analyse_data(solde_courant, show_graph)