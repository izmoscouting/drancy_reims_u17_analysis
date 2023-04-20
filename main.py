import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl
from st_pages import Page, show_pages, add_page_title



show_pages(
    [
        Page("main.py ", "Menu Principal", "⚽"),
        Page("pages/1_🦾_Equipe.py", "Equipe", "🦾"),
        Page("pages/2_🏃‍♂️_Joueur.py", "Joueurs", "🏃‍♂️")
    ]
)


st.set_page_config(layout='wide',
                   initial_sidebar_state='expanded',
                   page_title='U17NAT: JA Drancy - SD Reims',
                   page_icon='📊')


with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: black;'>U17NAT - J23: JA Drancy - SD Reims</h1>", unsafe_allow_html=True)
score_equipe1 = 3
score_equipe2 = 1

equipe1_logo = 'data/JAD.png'
equipe2_logo = 'data/SDR.png'

st.markdown('### 💻Score')
col1, col2,col3,col4 = st.columns(4)
col1.metric('JA Drancy',score_equipe1)
col2.image(equipe1_logo,width=100)
col3.metric("SD Reims", score_equipe2)
col4.image(equipe2_logo,width=80)

passes = pd.read_excel('data/jad_reims.xlsx',sheet_name='pass')
possession = passes.groupby('Team')['Team'].count()

st.markdown('### 🍩Possession du Ballon')

fig, ax = plt.subplots(figsize=(4, 4))
ax.pie(possession, labels=['Drancy','Reims'], colors=['#073AE8','#E83707'], autopct='%1.1f%%', pctdistance=0.85, explode=(0.01, 0.01))
my_circle = plt.Circle((0,0), 0.7, color='white')
ax.add_artist(my_circle)

# Appliquer des styles supplémentaires
ax.axis('equal')

# Afficher le graphique dans Streamlit
c1,c2 = st.columns((7,3))
with c1:
    st.pyplot(fig)

st.sidebar.success('Selectionnez une page')
st.sidebar.markdown('''---
Visualisation des datas collectées\nmanuellement (par @IzmoScouting\n([Twitter]('https://twitter.com/IzmoScouting') & [Instagram]('https://www.instagram.com/izmoscouting/'))) \ndu match entre Drancy\net le Stade de Reims''')