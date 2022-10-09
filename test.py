from this import d
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def main():
    st.set_page_config(layout="wide")
    st.title('Cleaning')

if __name__ == '__main__':
    main()

#Load prediction data
    @st.cache
    def load_Dataframe(link):
        df= pd.read_csv(link)  #Currently on my local machine
        return df
    
    def get_dom(dt):
        return dt.day

    def get_month(dt):
        return dt.month

    def get_year(dt):
        return dt.year
    
    def apply_dwhy(df):
        df["date_mutation"] = pd.to_datetime(df["date_mutation"])
        df["Day"] = df["date_mutation"].apply(get_dom)
        df["Month"] = df["date_mutation"].apply(get_month)
        df["Year"] = df["date_mutation"].apply(get_year)
        return df

    
    def highlight_NbNaN(df2):
        #pourcentage = 0.7 * len(df)
        return ['background-color: green']*len(df2) if df2["Nb_NaN"]/len(df)<0.7 else ['background-color: red']*len(df2)
    
    def highlight(df2):
    #pourcentage = 0.7 * len(df)
        return ['background-color: green']*len(df2) if df2["% de valeurs nulls"]=='moins de 70%' else ['background-color: red']*len(df2)


    df= load_Dataframe("full_2019.csv")


    st.dataframe(df.head())



    st.title("on supprimes les valeurs ayant trop de valeurs nulls")
    df_isnull = pd.DataFrame(df.isnull().sum())
    df_isnull.rename(columns = {0 : "Nb_NaN"}, inplace=True)
    
    col1,col2 = st.columns(2)
    
    col1.dataframe(df_isnull.style.apply(highlight_NbNaN, axis=1))
    
    dict = {'vert': "plus de 70%", 'rouge': 'moins de 70%'}
    dict.items()
    df_legend = pd.DataFrame(dict.items())
    df_legend.rename(columns= {0 : "couleurs"}, inplace=True)
    df_legend.index= df_legend["couleurs"]
    df_legend.drop(columns="couleurs", inplace=True)
    df_legend.rename(columns= {1 : "% de valeurs nulls"}, inplace=True)
    #df_legend

    df_legend = df_legend.style.apply(highlight, axis=1)
    col2.dataframe(df_legend)

    @st.cache
    def Delete_Col(df2):
        L = [ df2.index[i] for i in range(len(df2)) if df2.iloc[i,0]/len(df) >= 0.7]
        return L

    df_clean_1 = df.copy()
    df_clean_1 = df_clean_1.drop(Delete_Col(df_isnull),axis=1)

    st.markdown("***")
    col1, col2 = st.columns(2)

    col1.dataframe(df_clean_1.head())
    col2.dataframe(df_clean_1.isnull().sum())

    st.title("On supprimer les valeurs foncières NaN")

    df_clean_1.drop(df_clean_1[df_clean_1["valeur_fonciere"].isnull()].index, axis=0, inplace=True)
    df_clean_1.drop(df_clean_1[df_clean_1["longitude"].isnull()].index, axis=0, inplace=True)
    df_clean_1.drop(df_clean_1[df_clean_1["type_local"].isnull()].index, axis=0, inplace=True)
    #df_clean_1.drop(df_clean_1[df_clean_1["lot1_numero"].isnull()].index, axis=0, inplace=True)
    df_clean_1.drop(df_clean_1[df_clean_1["surface_reelle_bati"].isnull()].index, axis=0, inplace=True)
    df_clean_1.drop(df_clean_1[df_clean_1["nombre_lots"] > 1].index, axis=0, inplace=True)
    

    df_clean_1.drop(["adresse_nom_voie","adresse_code_voie","adresse_numero","code_postal","code_type_local"], axis=1, inplace=True)
    df_clean_1["code_commune"] = df_clean_1["code_commune"].astype(str)
    df_clean_1["code_departement"] = df_clean_1["code_departement"].astype(str)
    df_clean_1["lot1_numero"] = df_clean_1["lot1_numero"].astype(str)


    st.write(len(df_clean_1))
    st.dataframe(df_clean_1.isnull().sum())

    df_clean_1.reset_index(drop=True,inplace=True)
    df_clean_1["nombre_pieces_principales"] = df_clean_1["nombre_pieces_principales"].astype(str)



    st.dataframe(df_clean_1.head(100))

    df_dep = pd.read_csv("departements-france.csv")
    df_clean_1["code_region"] = df_clean_1["code_departement"].copy()
    for i in df_dep["code_region"].unique():
        df_clean_1["code_region"].replace(df_dep["code_departement"][df_dep["code_region"]==i].unique(), i, inplace=True)
    st.title("We add code Region Thanks to the code departement")
    st.title("Dataframe code département")
    st.dataframe(df_dep)

    st.title("Dataframe with the new column Region")
    st.dataframe(df_clean_1)

    st.write(df_clean_1.describe())


    df_clean_1 = apply_dwhy(df_clean_1)

    st.title("Dataframe with Day, Month, Year")
    st.dataframe(df_clean_1)



    st.title("we do the same with all the dataframe 2016 2017 2018 2020")





    








