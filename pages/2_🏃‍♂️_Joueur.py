import streamlit as st
import pandas as pd
import seaborn as sns
from matplotlib.cm import get_cmap
import matplotlib.pyplot as plt
import cmasher as cmr
from matplotlib.colors import LinearSegmentedColormap
from mplsoccer import Pitch, VerticalPitch, Sbopen, FontManager
import numpy as np
import openpyxl

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title('Partie Joueur du site!')

def get_heatmap(player):

    player_df = df.loc[df.Player==player,['Team','Numero','X','Y']]
    pitch = Pitch(line_color='#cfcfcf',pitch_type="wyscout", line_zorder=2, pitch_color='#122c3d')

    if (player_df.Team.values[0] == 'DRANCY U17Nat'):
        fig, ax = pitch.draw()
        kde = pitch.kdeplot(player_df.X, player_df.Y, ax=ax,
                            # fill using 100 levels so it looks smooth
                            fill=True, levels=100,
                            # shade the lowest area so it looks smooth
                            # so even if there are no events it gets some color
                            shade_lowest=True,
                            cut=10,  # extended the cut so it reaches the bottom edge
                            cmap=cmr.emerald)
        ax.set_title(f'Heatmap de {player} | Poste n°{player_df.Numero.values[1]} | {player_df.Team.values[1]}')
        plt.gca().invert_xaxis()
        plt.gca().invert_yaxis()
        plt.show()
    
    else : 
        fig, ax = pitch.draw()
        kde = pitch.kdeplot(player_df.X, player_df.Y, ax=ax,
                            # fill using 100 levels so it looks smooth
                            fill=True, levels=100,
                            # shade the lowest area so it looks smooth
                            # so even if there are no events it gets some color
                            shade_lowest=True,
                            cut=10,  # extended the cut so it reaches the bottom edge
                            cmap=cmr.emerald)
        ax.set_title(f'Heatmap de {player} | Poste n°{player_df.Numero.values[1]} | {player_df.Team.values[1]}')

def get_def(player):
    player_pressure_mask = ((df.Event=='Pressing') | (df.Event=='Récupération') | (df.Event=='Tacle') | (df.Event=='Dégagement') | (df.Event=='Interception') | (df.Event.str.contains('Duel')) | (df.Event.str.contains('Contré')) ) & (df.Player==player)
    pressure_df = df[player_pressure_mask]
    return pressure_df

def def_map(player):
    pressure_df = get_def(player)

    pitch = Pitch(pitch_type="wyscout",pitch_color='#22312b',line_zorder=2)
    fig,ax = pitch.draw()

    if (pressure_df.Team == 'DRANCY U17Nat').any():
        plt.gca().invert_xaxis()
        plt.gca().invert_yaxis()

        pitch.kdeplot(
            pressure_df.X, pressure_df.Y, ax=ax,
            fill=True, levels=100,
            shade_lowest=True,
            cut=10,  # extended the cut so it reaches the bottom edge
            cmap=cmr.emerald
        )

        ax.set_title(f'Actions défensives de {player} | Poste n° {pressure_df.Numero.values[1]} | {pressure_df.Team.values[1]}')

        plt.show()
    else:
        pitch.kdeplot(
            pressure_df.X, pressure_df.Y, ax=ax,
            fill=True, levels=100,
            shade_lowest=True,
            cut=10,  # extended the cut so it reaches the bottom edge
            cmap=cmr.emerald
        )

        ax.set_title(f'Action défensives de {player} | Poste n° {pressure_df.Numero.values[1]} | {pressure_df.Team.values[1]}')

        plt.show()

def get_dribbles(player):
    dribble_df = df[(df.Event.str.contains('Dribble') | df.Event.str.contains('Conduite')) & (df.Player==player)]
    return dribble_df

def dribbles_arrows(player):
    dribble_df = get_dribbles(player).replace('-',np.nan).dropna(subset=['X2'])
    dribble_df = dribble_df.apply(pd.to_numeric, errors='ignore', downcast='float')
    incompleted_dribble_mask = (dribble_df.Event.str.contains('Manqué'))
    completed_dribble = dribble_df[~incompleted_dribble_mask]
    incompleted_dribble = dribble_df[incompleted_dribble_mask]
    
    pitch = Pitch(pitch_type="wyscout",pitch_color='#22312b',line_zorder=2)
    fig, ax = pitch.draw()
    try: 
        if (dribble_df.Team=='DRANCY U17Nat').any():
            plt.gca().invert_xaxis()
            plt.gca().invert_yaxis()
            pitch.arrows( 
                xstart=completed_dribble.X, ystart= completed_dribble.Y, xend=completed_dribble.X2, yend=completed_dribble.Y2,
                width=2, ax=ax,headwidth=10,headlength=10,color='#3533CD',label='Dribbles Réussis'
            )

            pitch.arrows( 
                xstart=incompleted_dribble.X, ystart= incompleted_dribble.Y, xend=incompleted_dribble.X2, yend=incompleted_dribble.Y2,
                width=2, ax=ax,headwidth=10,headlength=10,color='#990000',label='Dribbles Manqués'
            )

            ax.set_title(f'Dribbles de {player} | Poste n° {dribble_df.Numero.values[1]} | {dribble_df.Team.values[1]}')

            ax.legend(loc='upper left')
            plt.show()
        else:
            pitch.arrows( 
                xstart=completed_dribble.X, ystart= completed_dribble.Y, xend=completed_dribble.X2, yend=completed_dribble.Y2,
                width=2, ax=ax,headwidth=10,headlength=10,color='#3533CD',label='Dribbles Réussis'
            )

            pitch.arrows( 
                xstart=incompleted_dribble.X, ystart= incompleted_dribble.Y, xend=incompleted_dribble.X2, yend=incompleted_dribble.Y2,
                width=2, ax=ax,headwidth=10,headlength=10,color='#990000',label='Dribbles Manqués'
            )

            ax.set_title(f'Dribbles de {player} | Poste n° {dribble_df.Numero.values[1]} | {dribble_df.Team.values[1]}')

            ax.legend(loc='upper left')
            plt.show()
    except:
        st.write(f'{player} n\'a pas dribblé!')
    
def get_pass(player):
    pass_df = df_pass.loc[df_pass.Player==player]
    return pass_df

def pass_arrows(player):
    pass_df = get_pass(player)
    incompleted_pass_mask = pass_df.Event.str.contains('Manquée')
    completed_pass = pass_df[~incompleted_pass_mask]
    key_pass = pass_df[pass_df.Event.str.contains('Clé')]
    dec_pass = pass_df[pass_df.Event.str.contains('Décisive')]
    sm_pass = pass_df[pass_df.Event.str.contains('Intelligente')]
    incompleted_pass = pass_df[incompleted_pass_mask]
    
    pitch = Pitch(pitch_type="wyscout",pitch_color='#22312b',line_zorder=2)
    fig, ax = pitch.draw()

    if (pass_df.Team=='DRANCY U17Nat').any():
        plt.gca().invert_xaxis()
        plt.gca().invert_yaxis()

        pitch.arrows( 
            xstart=completed_pass.X, ystart= completed_pass.Y, xend=completed_pass.X2, yend=completed_pass.Y2,
            width=2, ax=ax,headwidth=10,headlength=10,color='#3533CD',label='Passes Réussies'
        )
        pitch.arrows( 
            xstart=key_pass.X, ystart= key_pass.Y, xend=key_pass.X2, yend=key_pass.Y2,
            width=2, ax=ax,headwidth=10,headlength=10,color='#E9E622',label='Passes Clés'
        )

        pitch.arrows( 
            xstart=dec_pass.X, ystart= dec_pass.Y, xend=dec_pass.X2, yend=dec_pass.Y2,
            width=2, ax=ax,headwidth=10,headlength=10,color='#36DD14',label='Passes Décisives'
        )
        
                
        pitch.arrows( 
            xstart=incompleted_pass.X, ystart= incompleted_pass.Y, xend=incompleted_pass.X2, yend=incompleted_pass.Y2,
            width=2, ax=ax,headwidth=10,headlength=10,color='#990000',label='Passes Manquées'
        )

        pitch.arrows( 
            xstart=sm_pass.X, ystart= sm_pass.Y, xend=sm_pass.X2, yend=sm_pass.Y2,
            width=2, ax=ax,headwidth=10,headlength=10,color='#23E3CF',label='Passes Intelligentes'
        )

        ax.set_title(f'Passes de {player} | Poste n° {pass_df.Numero.values[1]} | {pass_df.Team.values[1]}')
        ax.legend(loc='upper left')
        plt.show()

    
    else:

        pitch.arrows( 
            xstart=completed_pass.X, ystart= completed_pass.Y, xend=completed_pass.X2, yend=completed_pass.Y2,
            width=2, ax=ax,headwidth=10,headlength=10,color='#3533CD',label='Passes Réussies'
        )
        pitch.arrows( 
            xstart=key_pass.X, ystart= key_pass.Y, xend=key_pass.X2, yend=key_pass.Y2,
            width=2, ax=ax,headwidth=10,headlength=10,color='#E9E622',label='Passes Clés'
        )

        pitch.arrows( 
            xstart=dec_pass.X, ystart= dec_pass.Y, xend=dec_pass.X2, yend=dec_pass.Y2,
            width=2, ax=ax,headwidth=10,headlength=10,color='#36DD14',label='Passes Décisives'
        )
        
                
        pitch.arrows( 
            xstart=incompleted_pass.X, ystart= incompleted_pass.Y, xend=incompleted_pass.X2, yend=incompleted_pass.Y2,
            width=2, ax=ax,headwidth=10,headlength=10,color='#990000',label='Passes Manquées'
        )

        ax.set_title(f'Passes de {player} | Poste n° {pass_df.Numero.values[1]} | {pass_df.Team.values[1]}')
        ax.legend(loc='upper left')
        plt.show()

def get_shot(player):
    team_shot_mask = ( (df.Event.str.contains('But')) | (df.Event.str.contains('Tir')) & (~df.Event.str.contains('Contré')) ) & (df.Player==player)
    shot_df = df[team_shot_mask]
    team_goals = shot_df[(shot_df.Event=='But') | (shot_df.Event=='But CF')]
    team__not_goals = shot_df[shot_df.Event=='Tir']
    team_offtarget = shot_df[shot_df.Event.str.contains('Cadre')]
    
    pitch = Pitch(pitch_type="wyscout",pitch_color='#22312b',line_zorder=2)

    fig,ax = pitch.draw()

    pitch.scatter(x=team_goals.X,y=team_goals.Y,edgecolor='black',ax=ax,marker='football')

    pitch.scatter(x=team__not_goals.X,y=team__not_goals.Y,edgecolor='black',ax=ax,color='blue')
    pitch.scatter(x=team_offtarget.X,y=team_offtarget.Y,edgecolor='black',ax=ax,color='red')

    plt.show()

df = pd.read_excel('data/jad_reims.xlsx',sheet_name='main')
df_pass =pd.read_excel('data/jad_reims.xlsx',sheet_name='pass')

st.sidebar.header('Filtrez Ici:')

plot_sel = st.sidebar.selectbox("Selectionnez un graphique",
                                options=['Heatmap','Actions défensives','Dribbles','Passes','Tirs'])

player = st.sidebar.selectbox(
    "Séléctionnez un Joueur:",
    options=df["Player"].unique()
)

df_selection = df.query("Player == @player")

header = st.container()

with header:
    st.title('Partie Joueur du site!')
    st.text('Ici vous pourrez observer le travail effectué par chacun des joueurs!\n🔎 Les cartes se lisent dans le sens de la lecture ➡')

if plot_sel == 'Heatmap':
    st.markdown('### 🥵 Heatmap')
    st.pyplot(get_heatmap(player))

if plot_sel == 'Actions défensives':
    st.markdown('### 🤼‍♂️ Actions défensives')
    st.write(f'{df[df.Event=="Récupération"][["Event","Player"]].value_counts().index[0][1]} est le joueur qui a récupéré le plus de ballons avec {df[df.Event=="Récupération"][["Event","Player"]].value_counts()[0]} récupérations')
    st.pyplot(def_map(player))

if plot_sel == 'Dribbles':
    st.markdown('### 🕺 Dribbles')
    st.write(f'{df[(df.Event.str.contains("Dribble") | df.Event.str.contains("Conduite") ) & ~(df.Event.str.contains("Manqué"))][["Event","Player"]].value_counts().index[0][1]} est le joueur qui a le plus porté le ballon {df[(df.Event.str.contains("Dribble") | df.Event.str.contains("Conduite") ) & ~(df.Event.str.contains("Manqué"))][["Event","Player"]].value_counts()[0]} dribbles & conduites de balle')
    st.pyplot(dribbles_arrows(player))


if plot_sel == 'Passes':
    st.markdown('### 🎯 Passes')
    st.pyplot(pass_arrows(player))

if plot_sel == 'Tirs':
    st.markdown('### ⚽ Tirs')
    st.write('Bleu : Cadré | Rouge : Pas Cadré')
    st.pyplot(get_shot(player))


st.sidebar.markdown('''---
Visualisation des datas collectées\nmanuellement (par @IzmoScouting\n([Twitter]('https://twitter.com/IzmoScouting') & [Instagram]('https://www.instagram.com/izmoscouting/'))) \ndu match entre Drancy\net le Stade de Reims''')