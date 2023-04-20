import streamlit as st
import pandas as pd
import seaborn as sns
from matplotlib.cm import get_cmap
import matplotlib.pyplot as plt
import cmasher as cmr
from matplotlib.colors import LinearSegmentedColormap
from mplsoccer import Pitch, VerticalPitch, FontManager


def get_teams_name(df):
    team1,team2 = df.Team.unique()
    return team1,team2

def get_pass(team):
    pass_df = df_pass.loc[df_pass.Team==team]
    print(pass_df)
    return pass_df

def pass_arrows(team):
    pass_df = get_pass(team)
    incompleted_pass_mask = pass_df.Event.str.contains('Manquée')
    completed_pass = pass_df[~incompleted_pass_mask]
    incompleted_pass = pass_df[incompleted_pass_mask]
    
    pitch = Pitch(pitch_type="wyscout",pitch_color='#22312b',line_zorder=2)
    fig, ax = pitch.draw()

    pitch.arrows( 
        xstart=completed_pass.X, ystart= completed_pass.Y, xend=completed_pass.X2, yend=completed_pass.Y2,
        width=2, ax=ax,headwidth=10,headlength=10,color='#3533CD',label='Passes Réussies'
    )

    pitch.arrows( 
        xstart=incompleted_pass.X, ystart= incompleted_pass.Y, xend=incompleted_pass.X2, yend=incompleted_pass.Y2,
        width=2, ax=ax,headwidth=10,headlength=10,color='#990000',label='Passes Manquées'
    )

    ax.set_title(f'Passes de {team}')

    ax.legend(loc='upper left')
    plt.show()

def pass_network(team):
    pass_df=get_pass(team)
    incompleted_pass_mask = pass_df.Event.str.contains('Manquée')
    completed_pass = pass_df[~incompleted_pass_mask]
    incompleted_pass = pass_df[incompleted_pass_mask]
    avg_loc = completed_pass.groupby('Player').agg({"X":['mean'],"Y":['mean']})
    avg_loc.columns = ['X','Y']

    pass_between = completed_pass.groupby(['Player','Passe Pour'],as_index=False).Team.count()
    pass_between.columns = ['Passeur','Receveur','Passe Entre']
    pass_between=pass_between.merge(avg_loc, left_on='Passeur',right_index=True)
    pass_between=pass_between.merge(avg_loc, left_on='Receveur',right_index=True,suffixes=['','2'])

    pitch = Pitch(pitch_type="wyscout",pitch_color='#22312b',line_zorder=2)
    fig, ax = pitch.draw()
    pitch.arrows(
        xstart=pass_between.X, ystart=pass_between.Y, xend=pass_between.X2,
        yend=pass_between.Y2, width=2, headwidth=10, headlength=30, color='#990000', ax=ax
    )

    pitch.scatter(
        x=pass_between.X, y=pass_between.Y, s=250, color='red',edgecolor='black',linewidth=1,alpha=1,ax=ax
    )

    for index, row in avg_loc.iterrows():
        maillot_num = df[df.Player==index].Numero.values[0]
        pitch.annotate(maillot_num, xy=(row.X,row.Y), c='white',va='center',ha='center',
                       size=8,weight='bold',ax=ax)
    plt.show()

def get_pressure(team):
    team_pressure_mask = (df.Event=='Pressing') & (df.Team==team)
    pressure_df = df[team_pressure_mask]
    return pressure_df

def pressure_map(team):
    pressure_df = get_pressure(team)

    pitch = Pitch(pitch_type="wyscout",pitch_color='#22312b',line_zorder=2)
    fig,ax = pitch.draw()

    if team == 'DRANCY U17Nat':
        plt.gca().invert_xaxis()
        plt.gca().invert_yaxis()

        pitch.kdeplot(
            pressure_df.X, pressure_df.Y, ax=ax,
            fill=True, levels=100,
            shade_lowest=True,
            cut=10,  # extended the cut so it reaches the bottom edge
            cmap=cmr.emerald
        )

        ax.set_title(f'Pressing de {team}')

        plt.show()
    else:
        pitch.kdeplot(
            pressure_df.X, pressure_df.Y, ax=ax,
            fill=True, levels=100,
            shade_lowest=True,
            cut=10,  # extended the cut so it reaches the bottom edge
            cmap=cmr.emerald
        )

        ax.set_title(f'Pressing de {team}')

        plt.show()

def pass_flow(team):
    pass_df = get_pass(team)
    
    pitch = Pitch(pitch_type="wyscout",pitch_color='#22312b',line_zorder=2)
    fig,ax = pitch.draw()
    bins = (6,3)
    
    if team == 'DRANCY U17Nat':
        plt.gca().invert_xaxis()
        plt.gca().invert_yaxis()
        bins_heatmap = pitch.bin_statistic(pass_df.X,pass_df.Y,statistic='count',bins=bins)
        pitch.heatmap(bins_heatmap,ax=ax,cmap='Reds')
        pitch.flow(xstart=pass_df.X,ystart=pass_df.Y,xend=pass_df.X2,yend=pass_df.X2,
                   ax=ax,color='black',arrow_type='same',arrow_length=5,bins=bins)
        
        ax.set_title(f'Tendances de Passes de {team}')
        plt.show()     

    else:
        bins_heatmap = pitch.bin_statistic(pass_df.X,pass_df.Y,statistic='count',bins=bins)
        pitch.heatmap(bins_heatmap,ax=ax,cmap='Reds')
        pitch.flow(xstart=pass_df.X,ystart=pass_df.Y,xend=pass_df.X2,yend=pass_df.X2,
                   ax=ax,color='black',arrow_type='same',arrow_length=5,bins=bins)
        
        ax.set_title(f'Tendances de Passes de {team}')
        plt.show() 

def get_shot(team):
    team_shot_mask = ( (df.Event.str.contains('But')) | (df.Event.str.contains('Tir')) & (~df.Event.str.contains('Contré')) ) & (df.Team==team)
    shot_df = df[team_shot_mask]
    team_goals = shot_df[(shot_df.Event=='But') | (shot_df.Event=='But CF')]
    team__not_goals = shot_df[shot_df.Event!='But']
    
    pitch = Pitch(pitch_type="wyscout",pitch_color='#22312b',line_zorder=2)

    fig,ax = pitch.draw()

    pitch.scatter(x=team_goals.X,y=team_goals.Y,edgecolor='black',ax=ax,marker='football')

    pitch.scatter(x=team__not_goals.X,y=team__not_goals.Y,edgecolor='black',ax=ax,color='blue')

    plt.show()

header = st.container()

dataset = st.container()

with header:
    st.title('Partie Équipe du site web!')
    st.write('Ici vous aurez des beaux graphiques pour vivre \nle match comme si vous y étiez!')

df = pd.read_excel('data/jad_reims.xlsx',sheet_name='main')
df_pass =pd.read_excel('data/jad_reims.xlsx',sheet_name='pass')

with dataset:
    st.header('JAD - SDR U17N')
    st.text('La version brute des données, attention les yeux.. ça pique!')
    st.write(df.head(10))


st.sidebar.header('Filtrez Ici:')

plot_sel = st.sidebar.selectbox("Selectionnez un graphique",
                                options=['Réseau de Passes','Direction des Passes','Carte de Tir','Carte de Pression','Tendance de Passes'])

team = st.sidebar.selectbox(
    "Séléctionnez une équipe:",
    options=df["Team"].unique()
)

df_selection = df.query("Team == @team")

if plot_sel == 'Réseau de Passes':
    st.markdown('### ⚽Réseau de Passes')
    col1,col2 = st.columns(2)
    col1.write(f'Le joueur avec le plus de passes est {df_pass["Player"].value_counts().index[0]} (N°{df_pass["Numero"].value_counts().index[0]}) avec {df_pass["Player"].value_counts()[0]} passes')
    col2.write(f'Le joueur qui a reçu le plus de passes est {df_pass["Passe Pour"].value_counts().index[0]} (N°{df_pass[df_pass.Player==df_pass["Passe Pour"].value_counts().index[0]].reset_index()["Numero"][0]}) avec {df_pass["Passe Pour"].value_counts()[0]} passes reçues')
    st.pyplot(pass_network(team))
    st.write('Voici le top 5 des joueurs ayant reçu le plus de ballons')
    st.write(df_pass[["Player","Numero"]].value_counts()[:5])


if plot_sel == 'Direction des Passes':
    st.markdown('### 🔀Direction des Passes')
    if team == 'DRANCY U17Nat':
        st.text('Passeurs Décisifs:\nLeny JACOB (1)\nAdnane KHARROUBI (1)\nTidiane DUMENIL (1)')
        st.pyplot(pass_arrows(team))
        st.text('On peut voir qu\'ils ont pratiqué un jeu direct ce dimanche')
    elif team == 'REIMS U17Nat':
        st.pyplot(pass_arrows(team))
        st.text('Largement plus patients que leurs adversaires, sûrement un peu trop!')

if plot_sel == 'Carte de Pression':
    st.markdown('### 🏃‍♂️ Carte de Pression')
    st.write('Lire de la gauche vers la droite')
    st.pyplot(pressure_map(team))


if plot_sel == 'Tendance de Passes':
    st.markdown('### 📈 Tendance de Passes')
    st.write('Lire de la gauche vers la droite')
    st.pyplot(pass_flow(team))


if plot_sel == 'Carte de Tir':
    st.markdown('### 🥅 Carte de Tir')
    st.text('Buteurs\nRayan ABO EL NAY | DRANCY (2) \nAlseny DIAWARA | Drancy (1) \nNoam FAUBERT | REIMS (1)')
    st.pyplot(get_shot(team))


st.sidebar.markdown('''---
Visualisation des datas collectées\nmanuellement (par @IzmoScouting\n([Twitter]('https://twitter.com/IzmoScouting') & [Instagram]('https://www.instagram.com/izmoscouting/'))) \ndu match entre Drancy\net le Stade de Reims''')