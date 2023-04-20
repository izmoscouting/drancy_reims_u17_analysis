def get_teams_name(df):
    team1,team2 = df.Team.unique()
    return team1,team2

def get_pass(df_pass,team):
    pass_df = df_pass.loc[df_pass.Team==team]
    print(pass_df)
    return pass_df

def pass_arrows(team):
    pass_df = get_pass(team)
    incompleted_pass_mask = pass_df.Event.str.contains('Manquée')
    completed_pass = pass_df[~incompleted_pass_mask]
    incompleted_pass = pass_df[incompleted_pass_mask]
    
    pitch = Pitch(pitch_type="wyscout")
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

    pitch = Pitch(pitch_type="wyscout",pitch_color='grass')
    fig, ax = pitch.draw()
    pitch.arrows(
        xstart=pass_between.X, ystart=pass_between.Y, xend=pass_between.X2,
        yend=pass_between.Y2, width=2, headwidth=10, headlength=30, color='#990000', ax=ax
    )

    pitch.scatter(
        x=pass_between.X, y=pass_between.Y, s=250, color='red',edgecolor='black',linewidth=1,alpha=1,ax=ax
    )

    for index, row in avg_loc.iterrows():
        maillot_num = df1[df1.Player==index].Numero.values[0]
        pitch.annotate(maillot_num, xy=(row.X,row.Y), c='white',va='center',ha='center',
                       size=8,weight='bold',ax=ax)
    plt.show()