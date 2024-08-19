import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
import io
import warnings
warnings.filterwarnings('ignore')
from datetime import datetime, timedelta

# if 'last_change_time' not in st.session_state:
#     st.session_state.last_change_time = datetime.min
# if 'last_league' not in st.session_state:
#     st.session_state.last_league = ''
# if 'last_name' not in st.session_state:
#     st.session_state.last_name = ''
# # if 'last_season' not in st.session_state:
# #     st.session_state.last_season = ''


# if 'position_group1' not in st.session_state:
#     st.session_state.position_group1 = 'CBs'
# if 'league1' not in st.session_state:
#     st.session_state.league1 = 'NWSL'
# if 'name1' not in st.session_state:
#     st.session_state.name1 = 'Abby Erceg'
# if 'season1' not in st.session_state:
#     st.session_state.season1 = '2024'





file_name = 'InternationalMensData.parquet'
df = pd.read_parquet(file_name)
df = df.drop_duplicates(subset = ['Player', 'Team', 'Competition', 'Season', 'Position Group'])
print('reading file')
st.set_page_config( 
    page_title="Racing Recruitment",
    page_icon=":checkered_flag:",
    layout="centered",
    initial_sidebar_state="expanded"   
    
)
df.fillna(0, inplace=True)

regular_font_path = '/Users/malekshafei/Downloads/Montserrat/static/Montserrat-Regular.ttf'
bold_font_path = '/Users/malekshafei/Downloads/Montserrat/static/Montserrat-Bold.ttf'

custom_css = f"""
<style>
@font-face {{
    font-family: 'Montserrat';
    src: url('file://{regular_font_path}') format('truetype');
    font-weight: normal;
}}
@font-face {{
    font-family: 'Montserrat';
    src: url('file://{bold_font_path}') format('truetype');
    font-weight: bold;
}}
html, body, [class*="css"] {{
    font-family: 'Montserrat', sans-serif;
    background-color: #C00C0D;
    color: #ffffff;
}}
.sidebar .sidebar-content {{
    background-color: #C00C0D;
}}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)
pos_list = ['CBs', 'WBs', 'CMs', 'AMs', 'Ws', 'STs']

#st.title(f"Racing Recruitment")

#st.dataframe(df)

sorted_competitions = sorted(df['Competition'].unique())


mode = st.selectbox("Select Mode", options=['Player Overview', 'Multi Player Dot Graph'])

if mode == 'Player Overview':


    # file_name = 'InternationalWomensData.xlsx'
    # df = pd.read_excel(file_name)
    df = df[df['Detailed Position'] != 'GK']

    
    #df['Position Group'] = df['pos_group']




    position_group1 = st.selectbox("Select Position Group", options=pos_list)
    df = df[df['Position Group'] == position_group1]


    # for pos in pos_list:
    #     new_data = pd.read_excel(file_name, sheet_name=pos)
    #     new_data['Position Group'] = pos
    #     #df = pd.concat([df,new_data], ignore_index = True)

    radar = True
    compare = "No"
    # league1 = st.selectbox("Select League", options=['NWSL', 'Mexico', 'Brazil','England', 'Spain', 'Germany', 'Sweden', 'France', 'Colombia', 'Portugal', 'Japan','Australia', 'Italy', 'Norway', 'Denmark', 'Belgium', 'Switzerland','Russia','Ukraine', 'Scotland', 'Iceland', 'USL', 'MLS Next Pro', 'USL League One' ])
    # name1 = st.selectbox("Select Player", options=df[(df['Position Group'] == position_group1) & (df['Competition'] == league1)]['Player'].unique())
    # season1 = st.selectbox("Select Season", options=sorted(df[(df['Competition'] == league1) & (df['Position Group'] == position_group1) & (df['Player'] == name1)]['Season'].unique(), reverse=True))
    col1, col2, col3 = st.columns(3)
    

    with col1:
        league1 = st.selectbox(
            'Select League',
            sorted_competitions
        )

    # Place the second selectbox in the second column
    with col2:
        #player_options = df[df['Competition'] == st.session_state.league1]['Player'].unique()
        name1 = st.selectbox(
            'Select Player',
            df[(df['Position Group'] == position_group1) & (df['Competition'] == league1)]['Player'].unique(),
            #player_options
            
        )

    # Place the third selectbox in the third column
    with col3:
        #season_options = sorted(df[(df['Competition'] == st.session_state.league1) & (df['Player'] == st.session_state.name1)]['Season'].unique(), reverse=True)
        season1 = st.selectbox(
            'Select Season',
            sorted(df[(df['Competition'] == league1) & (df['Position Group'] == position_group1) & (df['Player'] == name1)]['Season'].unique(), reverse=True),
            #season_options
        )

    col1, col2 = st.columns(2)
    with col1:

        if position_group1 == 'CMs': mode1 = st.selectbox("Select Radar Type", options=["Basic", 'Defending', 'Buildup & Chance Creation', 'Box Threat'])

        elif position_group1 == 'CBs': mode1 = st.selectbox("Select Radar Type", options=["Basic", 'In Possession', 'Defending'])
        elif position_group1 in ['AMs', 'Ws', 'STs']: mode1 = st.selectbox("Select Radar Type", options=["Basic", 'Threat Creation', 'Shooting', 'Out of Possession'])

        else: mode1 = st.selectbox("Select Radar Type", options=["Basic", 'Attacking', 'Defending'])

    
    if mode1 == 'Match by Match Overview': radar = False

 
    

    if radar == True:
        with col2:
            compare = st.selectbox("Compare with another player?", options=["No", 'Yes'])


        if compare == 'Yes':
            col1, col2, col3 = st.columns(3)
            with col1: league2 = st.selectbox("Select other League", options=sorted_competitions)
            with col2: name2 = st.selectbox("Select other Player", options=df[(df['Position Group'] == position_group1) & (df['Competition'] == league2)]['Player'].unique())
            with col3: season2 = st.selectbox("Select other season", options=sorted(df[(df['Competition'] == league2) & (df['Position Group'] == position_group1) & (df['Player'] == name2)]['Season'].unique(), reverse=True))

        ws_leagues = ['Albania', 'Algeria', 'Andorra', 'Argentina2','Argentina3', 'Armenia', 'Austria2', 
                      'Azerbaijan', 'Belgium2', 'Bolivia','Bosnia','Brazil3', 'Bulgaria', 'Canada', 'Chile', 'Croatia',
                       'Costa Rica', 'Cyprus', 'Dominican Republic', 'Ecuador', 'El Salvador',
                        'England5', 'Estonia', 'Finland', 'France3', 'Georgia', 'Germany4', 'Ghana', 'Guatemala',
                         'Honduras', 'Hungary', 'Hungary2', 'Iceland', 'Italy3', 'Jamaica', 'Japan2', 'Korea2', 
                         'Kosovo', 'Latvia', 'Lithuania', 'Mexico2', 'Moldova', 'Montegro', 'Morocco',
                         'Nicaragua', 'Macedonia', 'Norway2', 'Panama', 'Paraguay', 'Peru', 'Portugal2',
                         'Portugal3', 'Ireland', 'Romania', 'Scotland2', 'Serbia', 'Serbia2', 'Slovakia', 'Slovenia',
                         'Spain3', 'Sweden2', 'Switzerland2', 'Tunisia', 'Turkey2', 'Ukraine', 'Ukraine2', 
                         'USA2', 'USA3', 'USA4', 'Uruguay', 'Uzbekistan', 'Venezuela'
                         ]

    # st.session_state['position_group1'] = position_group1
    # st.session_state['league1'] = league1
    # st.session_state['name1'] = name1
    # st.session_state['season1'] = season1
    # st.session_state['mode1'] = mode1
    # st.session_state['compare'] = compare
    # if compare == 'Yes':
    #     st.session_state['league2'] = league2
    #     st.session_state['name2'] = name2
    #     st.session_state['season2'] = season2

    # if st.button('Run Code'):
    #     # Retrieve selections from session state
    #     position_group1 = st.session_state['position_group1']
    #     league1 = st.session_state['league1']
    #     name1 = st.session_state['name1']
    #     season1 = st.session_state['season1']
    #     mode1 = st.session_state['mode1']
    #     compare = st.session_state['compare']
    #     if compare == 'Yes':
    #         league2 = st.session_state['league2']
    #         name2 = st.session_state['name2']
    #         season2 = st.session_state['season2']
    
        
        # Radar Chart Code
        unavail_metrics = ""
        if position_group1 == 'CBs' and mode1 == 'Basic':
                
            Heading = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Heading']
            Carrying = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'SPt']
            BallRetention = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Ball Retention']
            ProgressivePassing = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Progressive Passing']
            DefAccuracy = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Tackle Accuracy']
            DefEngage = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Defensive Output']
            DefHigh = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Defending High']


            data1 = [Carrying, Heading, BallRetention, ProgressivePassing, DefAccuracy, DefEngage, DefHigh]
            #if league1 in ws_leagues: data1 = [0, Heading,  BallRetention, ProgressivePassing, DefAccuracy, DefEngage, 0]
            metrics = ['SPt', 'Heading','Ball Retention', 'Progressive Passing', 'Tackle Accuracy', 'Defensive Output', 'Defending High']
            metric_names = ['Set Piece\nThreat', 'Heading', 'Ball Retention', 'Progressive\nPassing', 'Tackle\nAccuracy', 'Defensive Output', 'Defending\nHigh']
            unavail_metrics = "Set Piece and Defending High"
            if compare == 'Yes':
                Heading2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'Heading']
                Carrying2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'SPt']
                BallRetention2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'Ball Retention']
                ProgressivePassing2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'Progressive Passing']
                DefAccuracy2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'Tackle Accuracy']
                DefEngage2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'Defensive Output']
                DefHigh2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'Defending High']


                data2 = [Carrying2, Heading2, BallRetention2, ProgressivePassing2, DefAccuracy2, DefEngage2, DefHigh2]
                #if league2 in ws_leagues: data2 = [0, Heading2, BallRetention2, ProgressivePassing2, DefAccuracy2, DefEngage2, 0]



        if position_group1 == 'CBs' and mode1 == 'Defending':
                
            TacklePct = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctTackle %']
            Tackles = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctTackles Won']
            Interceptions = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctInterceptions']
            Blocks = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctAerial Wins']
            Headers = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctAerial %']
            AerialPct = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctPct of Defensive Actions Att Third']
            DefThirdTacklePct = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Rank Tackle Outcome']


            data1 = [TacklePct, Tackles, Interceptions, Blocks, Headers, AerialPct, DefThirdTacklePct]
            #if league1 in ws_leagues: data1 = [TacklePct, Tackles, Interceptions, Blocks, Headers, 0, 0]
            metrics = ['pctTackle %', 'pctTackles Won', 'pctInterceptions', 'pctAerial Wins','pctAerial %', '% of Def Actions in Att. 1/3', 'Tackle Outcome']
            metric_names = ['Tackle %', 'Tackles', 'Interceptions', 'Headers\nWon','Aerial %', '% of Def. Actions in Att. 1/3', 'Tackle Outcome']
            unavail_metrics = "Tackle Outcome and Def. 1/3"

            if compare == 'Yes':
                TacklePct2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctTackle %']
                Tackles2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctTackles Won']
                Interceptions2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctInterceptions']
                Blocks2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctAerial Wins']
                Headers2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctAerial %']
                AerialPct2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctPct of Defensive Actions Att Third']
                DefThirdTacklePct2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'Rank Tackle Outcome']


                data2 = [TacklePct2, Tackles2, Interceptions2, Blocks2, Headers2, AerialPct2, DefThirdTacklePct2]
                #if league2 in ws_leagues: data2 = [TacklePct2, Tackles2, Interceptions2, Blocks2, Headers2, 0, 0]


        if position_group1 == 'CBs' and mode1 == 'In Possession':
                
            TacklePct = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctProgressive Passes']
            Tackles = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctLong Passes Completed']
            Interceptions = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctLong Pass %']
            Blocks = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctProgressive Carries']
            Headers = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], f"pct% of Passes Forward"]
            AerialPct = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctPasses into Final Third']
            DefThirdTacklePct = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctShort Pass %']


            data1 = [TacklePct, Tackles, Interceptions, Blocks, Headers, AerialPct, DefThirdTacklePct]
            metrics = ['pctProgressive Passes', 'pctLong Passes Completed', 'pctLong Pass %', 'pctProgressive Carries', f"pct% of Passes Forward", 'pctPasses into Final Third', 'pctShort Pass %']
            metric_names = ['Progressive\nPasses', 'Long Passes', 'Long Pass %', 'Progressive\nCarries',f'% of Passes\nForward', 'Passes into Final Third', 'Short Passing %']

            if compare == 'Yes':
                TacklePct2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctProgressive Passes']
                Tackles2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctLong Passes Completed']
                Interceptions2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctLong Pass %']
                Blocks2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctProgressive Carries']
                Headers2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], f"pct% of Passes Forward"]
                AerialPct2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctPasses into Final Third']
                DefThirdTacklePct2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctShort Pass %']


                data2 = [TacklePct2, Tackles2, Interceptions2, Blocks2, Headers2, AerialPct2, DefThirdTacklePct2]




        if position_group1 == 'WBs' and mode1 == 'Basic':
                
            Creating = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Chance Creation']) 
            Carrying = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Carrying'])
            Technical = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Ball Retention'])
            ReceivingForward = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Receiving Forward'])
            DefAccuracy = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Tackle Accuracy'])
            DefEngage = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Defensive Output'])
            DefendingHigh = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Defending High']
            Heading = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Heading'])
            #data1 = [Creating, Carrying, Technical, BoxThreat, DefAccuracy, DefEngage, DefendingHigh, Heading]
            
            data1 = [ReceivingForward, Technical, Creating, DefAccuracy, DefEngage, DefendingHigh,Heading]
            #if league1 in ws_leagues: data1 = [ReceivingForward, Technical, Creating, DefAccuracy, DefEngage, 0,Heading]
            metrics = ['Receiving', 'Ball Retention', 'Chance Creation', 'Tackle Accuracy', 'Defenisve Output', 'Defending High', 'Heading']
            metric_names = ['Receiving', 'Ball Retention', 'Chance Creation', 'Tackle\nAccuracy', 'Defenisve\nOutput', 'Defending High', 'Heading']
            unavail_metrics = "Defending High"

            if compare == 'Yes':
                Creating2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Chance Creation']) 
                Carrying2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Carrying'])
                Technical2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Ball Retention'])
                ReceivingForward2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Receiving Forward'])
                DefAccuracy2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Tackle Accuracy'])
                DefEngage2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Defensive Output'])
                DefendingHigh2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Defending High']
                Heading2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Heading'])
                #data1 = [Creating, Carrying, Technical, BoxThreat, DefAccuracy, DefEngage, DefendingHigh, Heading]
                
                data2 = [ReceivingForward2, Technical2, Creating2, DefAccuracy2, DefEngage2, DefendingHigh2,Heading2]
                #if league2 in ws_leagues: data2 = [ReceivingForward2, Technical2, Creating2, DefAccuracy2, DefEngage2, 0,Heading2]

        if position_group1 == 'WBs' and mode1 == 'Defending':
                
            TacklesWon = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctTackles Won']) 
            TacklePct = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctTackle %'])
            DefThirdTackles = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctInterceptions'])
            DefThirdTacklePct = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctPct of Defensive Actions Att Third'])
            Intercepts = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pct% of Team Tackles'])
            Pressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Rank Tackle Outcome'])
            AttThirdPressures = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctAerial Wins']
            
            data1 = [TacklesWon, TacklePct, DefThirdTackles, DefThirdTacklePct, Intercepts, Pressures,AttThirdPressures]
            #if league1 in ws_leagues: data1 = [TacklesWon, TacklePct, DefThirdTackles, 0, 0, 0,AttThirdPressures]
            metrics = ['Tackles Won', 'Tackle %', 'Def. Third Tackles Won', 'Def. Third Tackle %', 'Interceptions', 'Pressures','Att. Third Pressures']
            metric_names = ['Tackles Won', 'Tackle %', 'Interceptions', '% of Def Actions\nin Att. 1/3', '% of Team Tackles', 'Tackle Outcome','Headers Won']
            unavail_metrics = "Def. 1/3, % of Team Tackles, & Tackle Outcome"

            if compare == 'Yes':
                TacklesWon2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctTackles Won']) 
                TacklePct2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctTackle %'])
                DefThirdTackles2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctInterceptions'])
                DefThirdTacklePct2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctPct of Defensive Actions Att Third'])
                Intercepts2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pct% of Team Tackles'])
                Pressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Rank Tackle Outcome'])
                AttThirdPressures2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctAerial Wins']
                
                data2 = [TacklesWon2, TacklePct2, DefThirdTackles2, DefThirdTacklePct2, Intercepts2, Pressures2,AttThirdPressures2]
                #if league2 in ws_leagues: data2 = [TacklesWon2, TacklePct2, DefThirdTackles2, 0, 0, 0,AttThirdPressures2]

        if position_group1 == 'WBs' and mode1 == 'Attacking':
                
            KeyPasses = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctKey Passes']) 
            Crosses = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctCrosses Completed into Box'])
            PassesIntoBox = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctPasses into Box'])
            xA = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctxA'])
            Assists = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctAssists'])
            FinalThirdTouches = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctFinal Third Receptions'])
            TakeOns = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctTake Ons']
            
            data1 = [KeyPasses, Crosses, PassesIntoBox, xA, Assists, FinalThirdTouches,TakeOns]
            #if league1 in ws_leagues: data1 = [KeyPasses, Crosses, PassesIntoBox, xA, Assists, 0,TakeOns]
            metrics = ['pctKey Passes', 'pctCrosses Completed into Box', 'pctPasses into Box', 'pctxA', 'pctAssists', 'pctFinal Third Receptions', 'pctTake Ons']
            metric_names = ['Key Passes', 'Completed Crosses', 'Passes into Box', 'xA', 'Assists', 'Final Third Touches', 'Take Ons Completed']
            unavail_metrics = "Final Third Touches"

            if compare == 'Yes':
                KeyPasses2 = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctKey Passes']) 
                Crosses2 = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctCrosses Completed into Box'])
                PassesIntoBox2 = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctPasses into Box'])
                xA2 = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctxA'])
                Assists2 = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctAssists'])
                FinalThirdTouches2 = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctFinal Third Receptions'])
                TakeOns2 = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctTake Ons']
                
                data2 = [KeyPasses2, Crosses2, PassesIntoBox2, xA2, Assists2, FinalThirdTouches2,TakeOns2]
                #if league2 in ws_leagues: data2 = [KeyPasses, Crosses, PassesIntoBox, xA, Assists, 0,TakeOns]

        


        #streamlit run streamlit.py



        if position_group1 == 'CMs' and mode1 == 'Basic':
                
            Creating = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Chance Creation']) 
            Carrying = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Carrying'])
            Technical = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Ball Retention'])
            BoxThreat = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Receiving Forward'])
            DefAccuracy = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Tackle Accuracy'])
            DefEngage = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Defensive Output'])

            DefendingHigh = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Defending High']
            Heading = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Heading'])

            data1 = [BoxThreat, Creating, Technical, DefAccuracy, DefEngage, DefendingHigh, Heading]
            #if league1 in ws_leagues: data1 = [BoxThreat, Creating, Technical, DefAccuracy, DefEngage, 0, Heading]
            metrics = ['Receiving', 'Chance Creation', 'Ball Retention', 'Tackle Accuracy', 'Defensive Output', 'Pressing','Heading']
            metric_names = ['Receiving', 'Chance Creation', 'Ball Retention', 'Tackle\nAccuracy', 'Defensive Output', 'Defending High','Heading']
            unavail_metrics = "Defending High"

            if compare == 'Yes':
                Creating2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Chance Creation']) 
                Carrying2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Carrying'])
                Technical2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Ball Retention'])
                BoxThreat2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Receiving Forward'])
                DefAccuracy2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Tackle Accuracy'])
                DefEngage2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Defensive Output'])

                DefendingHigh2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Defending High']
                Heading2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Heading'])

                data2 = [BoxThreat2, Creating2, Technical2, DefAccuracy2, DefEngage2, DefendingHigh2, Heading2]
                #if league2 in ws_leagues: data2 = [BoxThreat2, Creating2, Technical2, DefAccuracy2, DefEngage2, 0, Heading2]

        if position_group1 == 'CMs' and mode1 == 'Defending':
                
            TacklesWon = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctTackles Won']) 
            TacklePct = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctTackle %'])
            Interceptions = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctInterceptions'])
            Pressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctPct of Defensive Actions Att Third'])
            CounterPressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pct% of Team Tackles'])
            AttThirdPressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Rank Tackle Outcome'])
            AerialWins = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctAerial Wins'])

            data1 = [TacklesWon, TacklePct, Interceptions, Pressures, CounterPressures, AttThirdPressures,AerialWins]
            #if league1 in ws_leagues: data1 = [TacklesWon, TacklePct, Interceptions, 0, 0, 0 ,AerialWins]
            metrics = ['Tackles Won', 'Tackle %', 'Interceptions', 'Pressures','Counterpressures','Att. Third Pressures', 'Headers Won']
            metric_names = ['Tackles Won', 'Tackle %', 'Interceptions', '% of Def Actions\nin Att. 1/3','% of Team Tackles','Tackle Outcome', 'Headers Won']
            unavail_metrics = "Def. 1/3, % of Team Tackles, & Tackle Outcome"

            if compare == 'Yes':
                TacklesWon2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctTackles Won']) 
                TacklePct2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctTackle %'])
                Interceptions2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctInterceptions'])
                Pressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctPct of Defensive Actions Att Third'])
                CounterPressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pct% of Team Tackles'])
                AttThirdPressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Rank Tackle Outcome'])
                AerialWins2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctAerial Wins'])

                data2 = [TacklesWon2, TacklePct2, Interceptions2, Pressures2, CounterPressures2, AttThirdPressures2,AerialWins2]
                #if league2 in ws_leagues: data2 = [TacklesWon2, TacklePct2, Interceptions2, 0, 0, 0,AerialWins2]

        if position_group1 == 'CMs' and mode1 == 'Buildup & Chance Creation':
                
            TacklesWon = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctProgressive Passes']) 
            TacklePct = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctPasses into Final Third'])
            Interceptions = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctKey Passes'])
            Pressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctPasses into Box'])
            CounterPressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctShort Pass %'])
            AttThirdPressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctProgressive Carries'])
            AerialWins = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctTake Ons'])

            data1 = [TacklesWon, TacklePct, Interceptions, Pressures, CounterPressures, AerialWins, AttThirdPressures]
            metrics = ['Progressive Passes', 'Passes into Final Third', 'Key Passes', 'Passes into Box','Short Pass %', '1v1 Dribbles Completed', 'Progressive Carries']
            metric_names = ['Progressive Passes', 'Passes into Final Third', 'Key Passes', 'Passes into Box','Short Pass %', '1v1 Dribbles Completed', 'Progressive Carries']

            if compare == 'Yes':
                TacklesWon2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctProgressive Passes']) 
                TacklePct2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctPasses into Final Third'])
                Interceptions2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctKey Passes'])
                Pressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctPasses into Box'])
                CounterPressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctShort Pass %'])
                AttThirdPressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctProgressive Carries'])
                AerialWins2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctTake Ons'])

                data2 = [TacklesWon2, TacklePct2, Interceptions2, Pressures2, CounterPressures2,AerialWins2, AttThirdPressures2]



        if position_group1 == 'CMs' and mode1 == 'Box Threat':
                
            TacklesWon = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctFinal Third Receptions']) 
            TacklePct = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctBox Receptions'])
            Interceptions = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctGoals'])
            Pressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctShots'])
            CounterPressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctxG'])
            AttThirdPressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctxG/Shot'])
            AerialWins = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctpAdj Received Passes in Six Yard Box'])

            data1 = [TacklesWon, TacklePct, Interceptions, Pressures, CounterPressures, AttThirdPressures,AerialWins]
            #if league1 in ws_leagues: data1 = [0, TacklePct, Interceptions, Pressures, CounterPressures, AttThirdPressures,0]
            metrics = ['Final Third Touches', 'Box Touches', 'Goals', 'Shots', 'xG', 'xG/Shot', 'Big Chances']
            metric_names = ['Final Third\nTouches', 'Box Touches', 'Goals', 'Shots', 'xG', 'xG/Shot', 'Touches in\n6-yd Box']
            unavail_metrics = "Final Third and 6-yd Box Touches"

            if compare == 'Yes':

                TacklesWon2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctFinal Third Receptions']) 
                TacklePct2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctBox Receptions'])
                Interceptions2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctGoals'])
                Pressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctShots'])
                CounterPressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctxG'])
                AttThirdPressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctxG/Shot'])
                AerialWins2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctpAdj Received Passes in Six Yard Box'])

                data2 = [TacklesWon2, TacklePct2, Interceptions2, Pressures2, CounterPressures2, AttThirdPressures2,AerialWins2]
                #if league2 in ws_leagues: data2 = [0, TacklePct2, Interceptions2, Pressures2, CounterPressures2, AttThirdPressures2,0]


                    
        if (position_group1 == 'Ws' or position_group1 == 'AMs') and mode1 == "Basic":
            #Goal_Contributions = df.loc[df.index[(df['Name'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'FW_Goal_Contribution']
            Creating = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Chance Creation'])
            Poaching = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Poaching'])
            Finishing = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Finishing'])
            Technical = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Ball Retention'])
            Dribbling = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Dribbling'])
            DefOutput = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Defensive Output'])
            Progression = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Progression'])
            Heading = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Heading'])

            data1 = [Creating, Dribbling, Poaching, Finishing, Heading, DefOutput, Progression]
            metrics = ['Chance Creation', 'Dribbling Threat', 'Poaching', 'Finishing', 'Heading','Defensive Output','Progression']
            metric_names = ['Chance\nCreation', 'Dribbling Threat', 'Poaching', 'Finishing', 'Heading', 'Defensive Output', 'Progression']

            if compare == 'Yes':

                Creating2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Chance Creation'])
                Poaching2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Poaching'])
                Finishing2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Finishing'])
                Technical2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Ball Retention'])
                Dribbling2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Dribbling'])
                DefOutput2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Defensive Output'])
                Progression2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Progression'])
                Heading2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Heading'])

                data2 = [Creating2, Dribbling2, Poaching2, Finishing2, Heading2, DefOutput2, Progression2]



        if (position_group1 == 'Ws' or position_group1 == 'AMs' or position_group1 == 'STs') and mode1 == "Threat Creation":
            TacklesWon = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctKey Passes']) 
            TacklePct = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctPasses into Box'])
            Interceptions = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctShort Pass %'])
            Pressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctAssists'])
            CounterPressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctCrosses Completed into Box'])
            AttThirdPressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctTake Ons'])
            AerialWins = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctProgressive Carries'])

            data1 = [TacklesWon, TacklePct, Interceptions, Pressures, CounterPressures, AttThirdPressures,AerialWins]
            metrics = ['Key Passes', 'Passes into Box','Short Pass %', 'Assists', 'Big Chances Created', '1v1 Dribbles', 'Progressive Carries']
            metric_names = ['Key Passes', 'Passes into Box','Short Pass %', 'Assists', 'Completed\nCrosses', '1v1 Dribbles', 'Progressive Carries']

            if compare == 'Yes':
                TacklesWon2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctKey Passes']) 
                TacklePct2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctPasses into Box'])
                Interceptions2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctShort Pass %'])
                Pressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctAssists'])
                CounterPressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctCrosses Completed into Box'])
                AttThirdPressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctTake Ons'])
                AerialWins2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctProgressive Carries'])

                data2 = [TacklesWon2, TacklePct2, Interceptions2, Pressures2, CounterPressures2, AttThirdPressures2,AerialWins2]

        if (position_group1 == 'Ws' or position_group1 == 'AMs' or position_group1 == 'STs') and mode1 == "Shooting":
            TacklesWon = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctBox Receptions']) 
            TacklePct = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctGoals'])
            Interceptions = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctShots'])
            Pressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctxG'])
            CounterPressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctxG/Shot'])
            AttThirdPressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctpAdj Received Passes in Six Yard Box'])
            AerialWins = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctpAdj Received Through Passes'])

            data1 = [TacklesWon, TacklePct, Interceptions, Pressures, CounterPressures, AttThirdPressures,AerialWins]
            #if league1 in ws_leagues: data1 = [TacklesWon, TacklePct, Interceptions, Pressures, CounterPressures, 0,0]
            metrics = ['Touches in Box', 'Goals', 'Shots', 'xG', 'xG/Shot', 'Big Chances', 'Big Chance Conversion']
            metric_names = ['Touches in Box', 'Goals', 'Shots', 'xG', 'xG/Shot', 'Touches in 6-yd Box', 'Through Balls\nReceived']
            unavail_metrics = "6-yd Box Touches and Through Ball"

            if compare == 'Yes':
                TacklesWon2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctBox Receptions']) 
                TacklePct2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctGoals'])
                Interceptions2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctShots'])
                Pressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctxG'])
                CounterPressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctxG/Shot'])
                AttThirdPressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctpAdj Received Passes in Six Yard Box'])
                AerialWins2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctpAdj Received Through Passes'])

                
                data2 = [TacklesWon2, TacklePct2, Interceptions2, Pressures2, CounterPressures2, AttThirdPressures2,AerialWins2]
                #if league2 in ws_leagues: data2 = [TacklesWon2, TacklePct2, Interceptions2, Pressures2, CounterPressures2, 0,0]


        if (position_group1 == 'Ws' or position_group1 == 'AMs' or position_group1 == 'STs') and mode1 == "Out of Possession":
            TacklesWon = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctTackles Won']) 
            TacklePct = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctTackle %'])
            Interceptions = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctInterceptions'])
            Pressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctAerial Wins'])
            CounterPressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'pctAerial %'])
            AttThirdPressures = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'pctAtt Box Headers Won'])
            AerialWins = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Rank Disruption'])

            data1 = [TacklesWon, TacklePct, Interceptions, Pressures, CounterPressures, AttThirdPressures,AerialWins]
            if league1 in ws_leagues: data1 = [TacklesWon, TacklePct, Interceptions, Pressures, CounterPressures, 0,0]
            metrics = ['Tackles Won', 'Tackle %', 'Interceptions', 'Pressures','Counterpressures','Att. Third Pressures', 'Att. Third Counterpressures']
            metric_names = ['Tackles Won', 'Tackle %', 'Interceptions', 'Headers Won','Aerial %','Att. Box Headers Won', 'Disruption Score']
            unavail_metrics = "Att. Box Headers and Disruption"

            if compare == 'Yes':
                TacklesWon2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctTackles Won']) 
                TacklePct2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctTackle %'])
                Interceptions2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctInterceptions'])
                Pressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctAerial Wins'])
                CounterPressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'pctAerial %'])
                AttThirdPressures2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'pctAtt Box Headers Won'])
                AerialWins2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Rank Disruption'])


                data2 = [TacklesWon2, TacklePct2, Interceptions2, Pressures2, CounterPressures2, AttThirdPressures2,AerialWins2]
                #if league2 in ws_leagues: data2 = [TacklesWon2, TacklePct2, Interceptions2, Pressures2, CounterPressures2, 0,0]



        if position_group1 == 'STs' and mode1 == "Basic":
            #Goal_Contributions = df.loc[df.index[(df['Name'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'FW_Goal_Contribution']
            Creating = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Chance Creation'])
            Poaching = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Poaching'])
            Finishing = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Finishing'])
            Technical = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Ball Retention'])
            Dribbling = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Dribbling'])
            DefOutput = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'SPt'])
            Heading = (df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0],'Heading'])

            data1 = [Creating, Dribbling, Poaching, Finishing, Heading, DefOutput, Technical]
            metrics = ['Chance Creation', 'Dribbling Threat', 'Poaching', 'Finishing', 'Heading','Defensive Output','Ball Retention']
            metric_names = ['Chance\nCreation', 'Dribbling Threat', 'Poaching', 'Finishing', 'Heading', 'SPt', 'Ball\nRetention']

            if compare == 'Yes':
                Creating2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Chance Creation'])
                Poaching2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Poaching'])
                Finishing2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Finishing'])
                Technical2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Ball Retention'])
                Dribbling2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Dribbling'])
                DefOutput2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'SPt'])
                Heading2 = (df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0],'Heading'])

                data2 = [Creating2, Dribbling2, Poaching2, Finishing2, Heading2, DefOutput2, Technical2]
                        

        angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
        data1 += data1[:1]  # Repeat the first value to close the polygon
        angles += angles[:1]  # Repeat the first angle to close the polygon

        if compare == 'Yes':
            data2 += data2[:1]

        fig, ax = plt.subplots(figsize=(16, 9), subplot_kw=dict(polar=True, facecolor='#C00C0D'))
        fig.patch.set_facecolor('#C00C0D')
        fig.set_facecolor('#C00C0D')

        ax.set_facecolor('#C00C0D')


        ax.spines['polar'].set_visible(False)

        ax.plot(angles, [100] * len(angles), color='white', linewidth=2.25, linestyle='-')
        ax.plot(angles, [75] * len(angles), color='white', linewidth=0.7, linestyle='-')
        ax.plot(angles, [50] * len(angles), color='white', linewidth=0.7, linestyle='-')
        ax.plot(angles, [25] * len(angles), color='white', linewidth=0.7, linestyle='-')

        if compare == 'No':
            ax.plot(angles, data1, color='green', linewidth=0.4, linestyle='-', marker='o', markersize=3)
            ax.fill(angles, data1, color='green', alpha=0.95)

        if compare == 'Yes':
            ax.plot(angles, data1, color='blue', linewidth=2.5, linestyle='-', marker='o', markersize=3)
            ax.fill(angles, data1, color='blue', alpha=0.7)

            ax.plot(angles, data2, color='yellow', linewidth=2.5, linestyle='-', marker='o', markersize=3)
            ax.fill(angles, data2, color='yellow', alpha=0.55)



        ax.set_xticks(angles[:-1])
        metrics = ["" for i in range(len(metrics))]
        ax.set_xticklabels(metrics)

        ax.set_yticks([])
        ax.set_ylim(0, 100)

        ax.plot(0, 0, 'ko', markersize=4, color='#C00C0D')
        #fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        #fig.subplots_adjust(left=0.25, right=0.75, top=0.75, bottom=0.25)
        fig.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.15)



        #ax.set_xticklabels(metrics, color='white', size=12)


        #plt.savefig(save_path + file_name + '.png')
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0,facecolor=fig.get_facecolor())
        #fig.savefig("PIctestjuly3", format='png', bbox_inches='tight', pad_inches=0)

        buf.seek(0)

        # # Open the image using PIL
        # image = Image.open(buf)

        # # Create a new canvas with desired dimensions and background color
        # final_canvas = Image.new('RGB', (1600, 900), (64, 1, 121))

        image = Image.open(buf).convert("RGBA")

        # Create a new canvas with desired dimensions and background color
        final_canvas = Image.new('RGBA', (1600, 900), (192, 12, 13, 255))


        resize_factor = 1.07
        new_size = (int(image.size[0] * resize_factor), int(image.size[1] * resize_factor))
        image = image.resize(new_size)
        image = image.rotate(13, expand=True)
        #image = image.rotate(13)


        # Calculate the position to paste, centering the image
        x = (final_canvas.width - image.width) // 2
        y = (final_canvas.height - image.height) // 2

        # Paste the matplotlib generated image onto the canvas
        final_canvas.paste(image, (x, y+65), image)

        final_canvas = final_canvas.convert("RGB")

        # plt.figure(figsize=(16, 9))  # Adjust figure size as needed
        # plt.imshow(final_canvas)
        # plt.axis('off')  # Turns off axes.


        fig_canvas, ax_canvas = plt.subplots(figsize=(16, 9))
        ax_canvas.imshow(final_canvas)

        ax_canvas.axis('off')
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        plt.tight_layout(pad=0)
        plt.margins(0, 0)

        x_list = [1150,820,770,450,515,800,1090]
        y_list = [460,190,190,460,770,885,770]
        orient_list = ['left', 'left', 'right', 'right', 'right','center', 'left']

        for i in range(7):
            plt.text(x_list[i], y_list[i], metric_names[i], ha = orient_list[i], fontsize=30, color = 'white')#,fontname='Avenir')



        club = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Team']
        mins = int(df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Minutes'])
        detailed_pos = df.loc[df.index[(df['Player'] == name1) & (df['Competition'] == league1) & (df['Season'] == season1)][0], 'Detailed Position']

        #print(unavail_metrics)
        

        if compare == 'No':
            plt.text(800,70,f"{name1}",ha = 'center', fontsize=45, color = 'white', fontweight = 'bold')
            plt.text(800,120,f"{club} - {season1} {league1} - {mins} Minutes - {detailed_pos}",ha = 'center', fontsize=30, color = 'white')#, fontname='Avenir')
            plt.text(30,880,f"Data compared to {league1} {position_group1}",ha = 'left', fontsize=16, color = 'white')#, fontname='Avenir')
            if league1 in ws_leagues and len(unavail_metrics) > 0: plt.text(1570,880,f"{unavail_metrics}\ndata unavailable for {league1}",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir') 
            # if league1 in ws_leagues and mode1 == 'Basic' and position_group1 in ['CBs','WBs']: plt.text(1570,880,f"Defending High data unavailable for {league1}",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir')
            # if league1 in ws_leagues and mode1 == 'Basic' and position_group1 == 'CMs': plt.text(1570,880,f"Pressing data unavailable for {league1}",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir')

        if compare == 'Yes':
            club2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'Team']
            mins2 = int(df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'Minutes'])
            detailed_pos2 = df.loc[df.index[(df['Player'] == name2) & (df['Competition'] == league2) & (df['Season'] == season2)][0], 'Detailed Position']

            plt.text(40,65,f"{name1}",ha = 'left', fontsize=35, color = 'blue', fontweight = 'bold')
            #plt.text(40,110,f"{club} - {season1} {league1}",ha = 'left', fontsize=30, color = 'green', fontname='Avenir')
            #plt.text(40,150,f"{mins} Minutes - {detailed_pos}",ha = 'left', fontsize=30, color = 'green', fontname='Avenir')
            plt.text(40,110,f"{club}",ha = 'left', fontsize=30, color = 'blue')#, fontname='Avenir')
            plt.text(40,150,f"{season1} {league1}",ha = 'left', fontsize=30, color = 'blue')#, fontname='Avenir')
            plt.text(40,190,f"{mins} Mins - {detailed_pos}",ha = 'left', fontsize=30, color = 'blue')#, fontname='Avenir')
        
            plt.text(1560,65,f"{name2}",ha = 'right', fontsize=35, color = 'yellow', fontweight = 'bold')
            #plt.text(1560,110,f"{club2} - {season2} {league2}",ha = 'right', fontsize=30, color = 'red', fontname='Avenir')
            #plt.text(1560,150,f"{mins2} Minutes - {detailed_pos2}",ha = 'right', fontsize=30, color = 'red', fontname='Avenir')
            plt.text(1560,110,f"{club2}",ha = 'right', fontsize=30, color = 'yellow')#, fontname='Avenir')
            plt.text(1560,150,f"{season2} {league2}",ha = 'right', fontsize=30, color = 'yellow')#, fontname='Avenir')
            plt.text(1560,190,f"{mins2} Mins - {detailed_pos2}",ha = 'right', fontsize=30, color = 'yellow')#, fontname='Avenir')
            plt.text(30,880,f"Data compared to {position_group1} in player's league",ha = 'left', fontsize=15, color = 'white')#, fontname='Avenir')

            if league1 in ws_leagues and league2 in ws_leagues: plt.text(1570,880,f"{unavail_metrics}\ndata unavailable",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir') 
            if league1 in ws_leagues and league2 not in ws_leagues: plt.text(1570,880,f"{unavail_metrics}\ndata unavailable for {league1}",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir') 
            if league1 not in ws_leagues and league2 in ws_leagues: plt.text(1570,880,f"{unavail_metrics}\ndata unavailable for {league2}",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir') 



            # if league1 in ws_leagues and league2 in ws_leagues and mode1 == 'Basic' and position_group1 in ['CBs','WBs']: plt.text(1570,880,f"Defending High data unavailable",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir')
            # elif league1 in ws_leagues and mode1 == 'Basic' and position_group1 in ['CBs','WBs']: plt.text(1570,880,f"Defending High data unavailable for {league1}",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir')
            # elif league2 in ws_leagues and mode1 == 'Basic' and position_group1 in ['CBs','WBs']: plt.text(1570,880,f"Defending High data unavailable for {league2}",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir')
            
            # if league1 in ws_leagues and league2 in ws_leagues and mode1 == 'Basic' and position_group1 == 'CMs': plt.text(1570,880,f"Pressing data unavailable",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir')
            # elif league1 in ws_leagues and mode1 == 'Basic' and position_group1 == 'CMs': plt.text(1570,880,f"Pressing data unavailable for {league1}",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir')

            # elif league2 in ws_leagues and mode1 == 'Basic' and position_group1 == 'CMs': plt.text(1570,880,f"Pressing data unavailable for {league2}",ha = 'right', fontsize=16, color = 'white')#, fontname='Avenir')
            
        #streamlit run streamlit.py


        # plt.subplots_adjust(left=0, right=1, top=1, bottom=0) 
        # plt.margins(0,0) 

        # plt.tight_layout(pad=0)
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
        #fig.savefig("PIctestjuly3", format='png', bbox_inches='tight', pad_inches=0)

        buf.seek(0)


        # plt.savefig("PIctestjuly3.png")

        #st.pyplot(plt)

            
        st.image(buf, use_column_width=True)


    



if  mode == 'Multi Player Dot Graph':
    pos_list = ['CBs', 'WBs', 'CMs', 'AMs', 'Ws', 'STs']
    #df['Position Group'] = df['pos_group']




    position_group1 = st.selectbox("Select Position Group", options=pos_list)
    df = df[df['Position Group'] == position_group1]
    # st.session_state['league2'] = ''
    # st.session_state['name2'] = ''
    # st.session_state['season2'] = ''

    # st.session_state['league3'] = ''
    # st.session_state['name3'] = ''
    # st.session_state['season3'] = ''
    # league1 = 'NA'
    # player1 = 'NA'
    # season1 = 'NA'

    # league2 = 'NA'
    # player2 = 'NA'
    # season2 = 'NA'

    # league3 = 'NA'
    # player3 = 'NA'
    # season3 = 'NA'

    # league4 = 'NA'
    # player4 = 'NA'
    # season4 = 'NA'

    # league5 = 'NA'
    # player5 = 'NA'
    # season5 = 'NA'

    if 'league2' not in st.session_state:
        st.session_state.league2 = ''
    if 'name2' not in st.session_state:
        st.session_state.name2 = ''
    if 'season2' not in st.session_state:
        st.session_state.season2 = ''

    
    

    # league1 = st.selectbox("Select League", options=['NWSL', 'Mexico', 'Brazil','England', 'Spain', 'Germany', 'Sweden', 'France', 'Colombia', 'Portugal', 'Japan','Australia', 'Italy', 'Norway', 'Denmark', 'Belgium', 'Switzerland','Russia','Ukraine', 'Scotland', 'Iceland', 'USL', 'MLS Next Pro', 'USL League One' ])
    # name1 = st.selectbox("Select Player", options=df[(df['Position Group'] == position_group1) & (df['Competition'] == league1)]['Player'].unique())
    # season1 = st.selectbox("Select Season", options=sorted(df[(df['Competition'] == league1) & (df['Position Group'] == position_group1) & (df['Player'] == name1)]['Season'].unique(), reverse=True))

    col1, col2, col3 = st.columns(3)
    with col1:
        league1 = st.selectbox(
            'Select League #1',
            sorted_competitions
        )

    # Place the second selectbox in the second column
    with col2:
        name1 = st.selectbox(
            'Select Player #1',
            df[(df['Position Group'] == position_group1) & (df['Competition'] == league1)]['Player'].unique()
        )

    # Place the third selectbox in the third column
    with col3:
        season1 = st.selectbox(
            'Select Season #1',
            sorted(df[(df['Competition'] == league1) & (df['Position Group'] == position_group1) & (df['Player'] == name1)]['Season'].unique(), reverse=True)
        )


    col1, col2, col3 = st.columns(3)
    with col1:
        league2 = st.selectbox(
            'Select League #2',
            sorted_competitions
        )

    # Place the second selectbox in the second column
    with col2:
        name2 = st.selectbox(
            'Select Player #2',
            df[(df['Position Group'] == position_group1) & (df['Competition'] == league2)]['Player'].unique()
        )

    # Place the third selectbox in the third column
    with col3:
        season2 = st.selectbox(
            'Select Season #2',
            sorted(df[(df['Competition'] == league2) & (df['Position Group'] == position_group1) & (df['Player'] == name2)]['Season'].unique(), reverse=True)
        )

    col1, col2, col3 = st.columns(3)
    with col1:
        league3 = st.selectbox(
            'Select League #3',
            sorted_competitions
        )

    # Place the second selectbox in the second column
    with col2:
        name3 = st.selectbox(
            'Select Player #3',
            df[(df['Position Group'] == position_group1) & (df['Competition'] == league3)]['Player'].unique()
        )

    # Place the third selectbox in the third column
    with col3:
        season3 = st.selectbox(
            'Select Season #3',
            sorted(df[(df['Competition'] == league3) & (df['Position Group'] == position_group1) & (df['Player'] == name3)]['Season'].unique(), reverse=True)
        )
    
    
    col1, col2, col3 = st.columns(3)
    with col1:
        league4 = st.selectbox(
            'Select League #4',
            sorted_competitions
        )

    # Place the second selectbox in the second column
    with col2:
        name4 = st.selectbox(
            'Select Player #4',
            df[(df['Position Group'] == position_group1) & (df['Competition'] == league4)]['Player'].unique()
        )

    # Place the third selectbox in the third column
    with col3:
        season4 = st.selectbox(
            'Select Season #4',
            sorted(df[(df['Competition'] == league4) & (df['Position Group'] == position_group1) & (df['Player'] == name4)]['Season'].unique(), reverse=True)
        )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        league5 = st.selectbox(
            'Select League #5',
            sorted_competitions
        )

    # Place the second selectbox in the second column
    with col2:
        name5 = st.selectbox(
            'Select Player #5',
            df[(df['Position Group'] == position_group1) & (df['Competition'] == league5)]['Player'].unique()
        )

    # Place the third selectbox in the third column
    with col3:
        season5 = st.selectbox(
            'Select Season #5',
            sorted(df[(df['Competition'] == league5) & (df['Position Group'] == position_group1) & (df['Player'] == name5)]['Season'].unique(), reverse=True)
        )

    # data = {
    #     'Player': ['Turner', 'Silva', 'Jheniffer', 'Tanaka', 'Ludmila'],
    #     'League': ['NWSL', 'Portugal', 'NWSL', 'Greece', 'NWSL'],
    #     'Season': ['2024', '2023/24', '2023/24', '2023/24', '2023/24'],
    #     'Poaching': [70, 90, 80, 50, 85],
    #     'Finishing': [60, 75, 85, 70, 90],
    #     'Defensive Output 1': [50, 55, 40, 65, 70],
    #     'Chance Creation': [45, 60, 80, 85, 70],
    #     'Defensive Output 2': [5, 50, 45, 70, 80]
    # }


    # df = pd.DataFrame(data)




    df = df[((df['Competition'] == league1) & (df['Player'] == name1) & (df['Season'] == season1)) | 
            ((df['Competition'] == league2) & (df['Player'] == name2) & (df['Season'] == season2)) | 
            ((df['Competition'] == league3) & (df['Player'] == name3) & (df['Season'] == season3)) | 
            ((df['Competition'] == league4) & (df['Player'] == name4) & (df['Season'] == season4)) |
            ((df['Competition'] == league5) & (df['Player'] == name5) & (df['Season'] == season5))]

    df['unique_label'] = df.apply(lambda row: f"{row['Player']}\n{row['Competition']} - {row['Season']}", axis=1)

                
    #print(df)
    # Plotting

    if position_group1 == 'CBs': metrics = ['Ball Retention', 'Progressive Passing', 'Heading', 'Defensive Output', 'Tackle Accuracy']
    if position_group1 == 'WBs': metrics = ['Ball Retention', 'Chance Creation', 'Receiving Forward', 'Defensive Output', 'Tackle Accuracy']
    if position_group1 == 'CMs': metrics = ['Heading','Chance Creation', 'Receiving Forward','Pressing','Defensive Output', 'Tackle Accuracy']
    if position_group1 in ['Ws', 'AMs']: metrics = ['Defensive Output', 'Finishing', 'Poaching', 'Dribbling', 'Chance Creation']
    if position_group1 == 'STs': metrics = ['Chance Creation', 'Heading','Defensive Output', 'Finishing', 'Poaching']


    #metrics = metrics[::-1]

    #players = [player1, player2, player3, player4, player5 ]
    #players = df['Player']
    players = df['unique_label']
    colors = ['purple', 'red', 'green', 'orange', 'black']
    #fig, ax = plt.subplots(figsize=(10, 6))
    fig, ax = plt.subplots(figsize=(16, 9))
    fig.patch.set_facecolor('#C00C0D')
    fig.set_facecolor('#C00C0D')

    ax.set_facecolor('#C00C0D')
    #fig, ax = plt.subplots(figsize=(16, 9))


    # Plot lines for each metric
    for i in range(len(metrics)):
        y = len(metrics) - i
        metric = metrics[i]

        ax.plot([0, 100], [y, y], color='white', linewidth=0.8)



        for x in np.arange(0, 101, 10):
            #ax.axvline(x, ymin=y - 0.05, ymax=y + 0.05, color='black', linewidth=0.5)
            ax.vlines(x, ymin=y-0.1, ymax=y+0.1, color='white', linewidth=0.6, zorder= 1)

        for j in range(len(players)):
            row = df.iloc[j]
            unique_label = row['unique_label']
            player = row['Player']
            league = row['Competition']
            season = row['Season']

            #x = df.loc[j, metric]
            x = row[metric]
            print(player, season, metric, x)
            #ax.scatter(x, i+1, s = 950, color=colors[j], label=player if i == 0 else "", zorder = 3)
            ax.scatter(x, i + 1, s=950, color=colors[j], label=unique_label if i == 0 else "", zorder=3)





    # Customizing the plot

    ax.set_xticks(np.arange(0, 101, 10))
    ax.set_xticklabels(np.arange(0, 101, 10), size = 22, color = 'white')#,fontname='Avenir',
    ax.set_xlabel(f'Rankings vs {position_group1} in their League', size = 20,  color = 'white')#,fontname='Avenir',
    ax.set_title('Player Comparison\n ', size = 30, color = 'white')#fontname='Avenir'

    # for label in ax.get_yticklabels():
    #     label.set_x(-0.05)  # Adjust the value as needed to create more space

    #ax.yaxis.set_tick_params(pad=60)

    for label in ax.get_yticklabels():
        label.set_bbox(dict(facecolor='#C00C0D', edgecolor='None', alpha=0.65, pad=5))

    ax.set_yticks(np.arange(1, len(metrics) + 1))
    ax.set_yticklabels(metrics, size = 23, ha='right', color = 'white')#, fontname='Avenir')




    # Adding legend
    # handles, labels = ax.get_legend_handles_labels()
    # by_label = dict(zip(labels, handles))
    # ax.legend(by_label.values(), by_label.keys(), loc='upper center', bbox_to_anchor=(0.5, -0.15), fontsize='large', ncol=5)
    handles, labels = ax.get_legend_handles_labels()
    #legend_labels = [f'{label}\n{df.loc[df["Player"] == label, "Competition"].iloc[0]} - {df.loc[df["Player"] == label, "Season"].iloc[0]}\n{int(df.loc[df["Player"] == label, "Minutes"].iloc[0])} Minutes' for label in labels]
    legend_labels = [f'{label}\n{int(df.loc[df["unique_label"] == label, "Minutes"].iloc[0])} Minutes' for label in labels]

    by_label = dict(zip(labels, handles))
    legend = ax.legend(by_label.values(), legend_labels, facecolor = '#C00C0D', loc='upper center', bbox_to_anchor=(0.5, -0.2), fontsize=16, ncol=len(players))
     
    for text in legend.get_texts():
        text.set_color('white')
    # from matplotlib import font_manager as fm

    # for text in legend.get_texts():
    #     text.set_color('white')
    #     lines = text.get_text().split('\n')
    #     text.set_text('')  # Clear the current text

    # # Create Text objects with different font sizes
    #     for i, line in enumerate(lines):
    #         if i == 0:
    #             font_properties = fm.FontProperties(size=20)  # Larger font for the first line
    #         else:
    #             font_properties = fm.FontProperties(size=16)  # Normal font for other lines
    #         text_line = plt.Text(0, 0, line, fontproperties=font_properties)
    #         text_line.set_fontproperties(font_properties)

    #         # Append each line with appropriate font size to the text
    #         text._text += text_line.get_text() + '\n'




        
    

    #plt.subplots_adjust(left=0.3, right=0.95, top=0.9, bottom=0.1)
    #plt.axis('off')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.2)
    #fig.savefig("PIctestjuly3", format='png', bbox_inches='tight', pad_inches=0)

    buf.seek(0)


    # plt.savefig("PIctestjuly3.png")

    #st.pyplot(plt)

        
    st.image(buf, use_column_width=True)
    radar = True
    position_group1 = 'NA'
   


if position_group1 == 'CBs' and mode1 == 'Basic':
    st.write("Metric Definitions:")
    st.write("Progressive Passing: How often and how accurate the player is at making progressive, long, and final third entry passes")
    st.write("Ball Retention: A measure of how good they are at keeping the ball and not turning it over (passing and dribbling accuracies)")
    st.write("Carrying: Threat added from ball carries")
    st.write("Heading: How often the player wins aerial duels and how accurate they are in them")
    st.write("Defending High: How often the player makes defensive actions in the attacking half [Only available for leagues with StatsBomb data]")
    st.write("Defensive Output: How often the player makes tackles, interceptions, blocks")
    st.write("Tackle Accuracy: Ratio of tackles won per attacker faced")

if position_group1 == 'WBs' and mode1 == 'Basic':
    st.write("Metric Definitions:")
    st.write("Chance Creation: Assists, xA, Key Passes, Passes & Crosses Completed into Box")
    st.write("Ball Retention: A measure of how good they are at keeping the ball and not turning it over (passing and dribbling accuracies)")
    st.write("Receiving: How often the player receives the ball in advanced positions")
    st.write("Heading: How often the player wins aerial duels and how accurate they are in them")
    st.write("Defending High: How often the player makes defensive actions in the attacking half [Only available for leagues with StatsBomb data]")
    st.write("Defensive Output: How often the player makes tackles, interceptions, blocks")
    st.write("Tackle Accuracy: Ratio of tackles won per attacker faced")

if position_group1 == 'CMs' and mode1 == 'Basic':
    st.write("Metric Definitions:")
    st.write("Ball Retention: A measure of how good they are at keeping the ball and not turning it over (passing and dribbling accuracies)")
    st.write("Chance Creation: Assists, xA, Key Passes, Passes & Crosses Completed into Box")
    st.write("Receiving: How often the player receives the ball in advanced positions")
    st.write("Heading: How often the player wins aerial duels and how accurate they are in them")
    st.write("Pressing: How often the player makes pressure & counterpressure actions, with an emphasis on attacking third pressures [Only available for leagues with StatsBomb data]")
    st.write("Defensive Output: How often the player makes tackles, interceptions, blocks")
    st.write("Tackle Accuracy: Ratio of tackles won per attacker faced")

if (position_group1 == 'AMs' or position_group1 == 'Ws') and mode1 == 'Basic':
    st.write("Metric Definitions:")
    st.write("Finishing: Goal Conversion %, xG Over/Underperformance")
    st.write("Poaching: How often the player gets into goalscoring positons (xG, xG/Shot, Touches in Box)")
    st.write("Dribbling Threat: 1v1 Dribbles, Progressive Carries")
    st.write("Chance Creation: Assists, xA, Key Passes, Passes & Crosses Completed into Box")
    st.write("Progression: Player's involvement in moving the ball forward in the buildup via final third and box entry passes, dribbles")
    st.write("Defensive Output: How often the player makes pressures, counterpressures, tackles, interceptions")
    st.write("Heading: How often the player wins aerial duels and how accurate they are in them")

if position_group1 == 'STs' and mode1 == 'Basic':
    st.write("Metric Definitions:")
    st.write("Finishing: Goal Conversion %, xG Over/Underperformance")
    st.write("Poaching: How often the player gets into goalscoring positons (xG, xG/Shot, Touches in Box)")
    st.write("Dribbling Threat: 1v1 Dribbles, Progressive Carries")
    st.write("Chance Creation: Assists, xA, Key Passes, Passes & Crosses Completed into Box")
    st.write("Ball Retention: A measure of how good they are at keeping the ball and not turning it over (passing and dribbling accuracies)")
    st.write("Defensive Output: How often the player makes pressures, counterpressures, tackles, interceptions")
    st.write("Heading: How often the player wins aerial duels and how accurate they are in them")
     

#streamlit run streamlit.py