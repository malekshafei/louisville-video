import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsbombpy import sb
import plotly.express as px
import plotly.graph_objects as go

creds = {"user": "rdell@racingloufc.com", "passwd": "8CStqFOa"}


from PIL import Image, ImageOps
import io
import warnings
warnings.filterwarnings('ignore')
from datetime import datetime, timedelta

from matplotlib import rcParams

    
from matplotlib.font_manager import fontManager, FontProperties
# font_path = '/Users/malekshafei/Downloads/Sen/static/Sen-Regular.ttf'
# fontManager.addfont(font_path)
# sen_font = FontProperties(fname=font_path).get_name()
# rcParams['font.family'] = sen_font
rcParams['text.color'] = 'white' 



# file_name = 'InternationalWomensData.parquet'
# df = pd.read_parquet(file_name)
st.set_page_config( 
    page_title="Racing Recruitment",
    page_icon=":checkered_flag:",
    layout="centered",
    initial_sidebar_state="expanded"   
    
)
import os
regular_font_path = '/Users/malekshafei/Downloads/Montserrat/static/Montserrat-Regular.ttf'
bold_font_path = '/Users/malekshafei/Downloads/Montserrat/static/Montserrat-Bold.ttf'
if os.path.isfile(regular_font_path):
    fontManager.addfont(regular_font_path)
else:
    print(f"Font file not found: {regular_font_path}")

if os.path.isfile(bold_font_path):
    fontManager.addfont(bold_font_path)
else:
    print(f"Font file not found: {bold_font_path}")

custom_css = f"""
<style>
video {{
    width: 100%;
    height: auto;
}}
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
    background-color: #400179;
    color: #ffffff;
}}
.sidebar .sidebar-content {{
    background-color: #400179;
}}
img[data-testid="stLogo"] {{
            height: 3rem;
}}

</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.logo("https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Louisville_City_FC_2020_logo_primary.svg/160px-Louisville_City_FC_2020_logo_primary.svg.png")

selected_team = 'Louisville City'
league = 'USL'
matches = [
    '3/16 @ El Paso',
    '3/23 vs Pittsburgh',
    '3/30 vs Birmingham',
    '4/6 vs Indy',
    '4/9 @ Charleston',
    '4/20 @ Loudoun',
    '4/27 vs Hartford',
    '5/11 vs Orange County',
    '5/18 @ Las Vegas', 
    '5/25 @ Rhode Island',
    '5/29 vs Detroit',
    '6/1 @ Miami',
    '6/8 vs North Carolina',
    '6/15 @ Tampa Bay',
    '6/19 @ Pittsburgh',
    '6/22 vs Rhode Island',
    '6/29 @ Birmingham',
    '7/6 @ Oakland',
    '7/19 vs Colorado',
    '7/27 vs Monterey',
    '8/3 @ New Mexico',
    '8/10 vs Sacramento',
    '8/17 vs Charleston',
    '8/24 @ Hartford',
    '8/31 @ North Carolina',
    '9/6 vs Loudoun'
           ]

match_ids = [3930232, 3930247, 3930255, 3930266, 3930274, 3930288, 3930307,
            3930327, 3930340, 3930351, 3930354, 3930357, 3930369, 3930382,
            3930392, 3930399, 3930412, 3930424, 3930444, 3930456, 3930475,
            3930487, 3930499, 3930506, 3930524, 3930527]



def custom_progress_bar(value, label):
    if value > 75:
        color = "#4CAF50"  # Green
    elif value >= 50: 
        color = 'yellow'
    elif value > 25: 
        color = 'orange'
    else:
        color = "#FF4B4B"  # Red

    # Custom HTML and CSS for progress bar
    progress_html = f"""
    <div style="margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between;">
            <span>{label}</span>
            <span>{value}%</span>
        </div>
        <div style="background-color: #f1f1f1; border-radius: 25px;">
            <div style="width: {value}%; background-color: {color}; height: 15px; border-radius: 25px;"></div>
        </div>
    </div>
    """
    st.markdown(progress_html, unsafe_allow_html=True)

import streamlit.components.v1 as components


player_list = ['Arturo Ordoñez', 'Sean Totsch', 'Kyle Adams', 'Wesley Charpie']


with st.sidebar:
    #team = st.selectbox('Select Team', ['Louisville City'])
    individual = st.radio('Team or Player Analyis?', ['Team', 'Player'])
    if individual == 'Player': 
        player_selection = st.selectbox('Choose Player', player_list)
    full = 'Full Season'
    full = st.radio('Full Season or Select Matches?', ['Full Season', 'Select Matches'])
    if full == 'Select Matches':

        container = st.container()
        #date_selection = st.multiselect("Select Matches", options = list(reversed(matches)))
        all = st.checkbox("Select all")
        if all:
            selected_options = container.multiselect("Select Matches",
            list(reversed(matches)),list(reversed(matches)))
        else:
            selected_options =  container.multiselect("Select Matches",
        list(reversed(matches)))

    selected_ids = []   
    if full == 'Full Season':
        selected_ids = match_ids
    else:
        selected_indices = [list(reversed(matches)).index(option) for option in selected_options]
        selected_indices = [len(matches) - 1 - index for index in selected_indices]

        for ind in selected_indices:
            selected_ids.append(match_ids[ind])
        if selected_ids == []:
            st.error("Please select at least one match")

    league_data = pd.read_parquet(f"{league}TeamMatchLevelVideo.parquet")
    full_team_data = league_data[league_data['Team'] == selected_team]
    
    team_data = league_data[(league_data['match_id'].isin(selected_ids)) & (league_data['Team'] == selected_team)]

    league_data = league_data[league_data['Team'] != selected_team]
    league_data = pd.concat([league_data, team_data], ignore_index=True)
    league_data['Matches'] = 1

    orig_cols = ['Avg. Defensive Distance',
                'Att. Third Pressures',
                'Def Half Entries Allowed',
                'PPDA',
                'Shots after Pressure Regains',
                'Att. Half Regains',
                '% of Goal Kicks Short',
                'Passes per Sequence',
                'Avg. Buildup Speed',
                'Avg. Distance Reached',
                '% -> Att. Half',
                '% -> Att. Third']
    
    neg_cols = ['PPDA', 'Def Half Entries Allowed'] 
    
    aggs = {col: 'mean' for col in orig_cols}
    aggs['Matches'] = 'size'

    if len(selected_ids) > 5:

        team_rankings = league_data.groupby('Team').agg(aggs).reset_index()
        for col in orig_cols:
            team_rankings[col] = round(team_rankings[col],2)
    
    else:
        team_data['Matches'] = 1
        team_avg = team_data.groupby('Team').agg(aggs).reset_index()
        for col in orig_cols:
            team_avg[col] = round(team_avg[col],2)

        team_rankings = league_data[league_data['Team'] != selected_team]
        team_rankings = pd.concat([team_rankings, team_avg], ignore_index=True)



    
    for col in orig_cols:
        if col not in ['match_id', 'Opponent', 'Match Date', 'Team', 'Venue']:
            if col in neg_cols:
                team_rankings[f"pct{col}"] = 100 - round(team_rankings[col].rank(pct=True) * 100,2)

            else:
                team_rankings[f"pct{col}"] = round(team_rankings[col].rank(pct=True) * 100,2)
        
    
    team_rankings['Pressing'] = ((0.2 * team_rankings['pctPPDA']) + (0.25 * team_rankings['pctAvg. Defensive Distance']) + (0.2 * team_rankings['pctAtt. Third Pressures']) + (0.25 * team_rankings['pctAtt. Half Regains']) + (0.1 * team_rankings['pctShots after Pressure Regains']))
    #team_rankings['Pressing'] = round(team_rankings['Pressing'].rank(pct=True) * 100,2)
    team_rankings['Pressing Rating'] = round(team_rankings['Pressing'],1)

               
    team_rankings['Goal Kick Buildouts'] = ((0.3 * team_rankings['pctAvg. Distance Reached']) + (0.15 * team_rankings['pctAvg. Buildup Speed']) + (0.4 * team_rankings['pct% -> Att. Half']) + (0.15 * team_rankings['pctPasses per Sequence']))
    #team_rankings['pctShort GK Buildups'] = round(team_rankings['Short GK Buildups'].rank(pct=True) * 100,2)
    team_rankings['Goal Kick Buildout Rating'] = round(team_rankings['Goal Kick Buildouts'],1)





    
    
    










    print(selected_ids)
    if individual == 'Team' and len(selected_ids) > 0:
        pct1 = team_rankings[team_rankings['Team'] == selected_team]['Pressing Rating'].values[0]
        
        pct2 = team_rankings[team_rankings['Team'] == selected_team]['Goal Kick Buildout Rating'].values[0]
        pct3 = 74
        pct4 = 44 
        pct5 = 99
        custom_progress_bar(int(round(pct1,0)), "Pressing")
        custom_progress_bar(int(round(pct2,0)), "Goal Kick Buildouts")
        custom_progress_bar(int(pct3), "Verticality")
        custom_progress_bar(int(pct4), "Changing Point of Attack")
        custom_progress_bar(int(pct5), "Crossing")

    if individual == 'Player':
        pct1 = 24
        pct2 = 26
        pct3 = 74
        pct4 = 99
        
        custom_progress_bar(int(pct1), "Tackling")
        custom_progress_bar(int(pct2), "Heading")
        custom_progress_bar(int(pct3), "Progressive Passing")
        custom_progress_bar(int(pct4), "Changing Point of Attack")

if individual == 'Team' and len(selected_ids) > 0:    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(['Pressing', 'Goal Kick Buildouts', 'Verticality','Changing Point of Attack', 'Crossing'])

    ## Pressing
    with tab1:
        pct1 = team_rankings[team_rankings['Team'] == selected_team]['pctAtt. Third Pressures'].values[0]
        pct2 = team_rankings[team_rankings['Team'] == selected_team]['pctAtt. Half Regains'].values[0]
        pct3 = team_rankings[team_rankings['Team'] == selected_team]['pctShots after Pressure Regains'].values[0]
        pct4 = team_rankings[team_rankings['Team'] == selected_team]['pctPPDA'].values[0]
        pct5 = team_rankings[team_rankings['Team'] == selected_team]['pctAvg. Defensive Distance'].values[0]
        pct6 = team_rankings[team_rankings['Team'] == selected_team]['pctDef Half Entries Allowed'].values[0]
        
       
        col1, col2, col3 = st.columns(3)
        with col1: custom_progress_bar(int(pct1), f"Att. Third Pressures   ({int(round(team_rankings[team_rankings['Team'] == selected_team]['Att. Third Pressures'].values[0],1))})")
        with col2: custom_progress_bar(int(pct2), f"Att. Half Regains   ({int(round(team_rankings[team_rankings['Team'] == selected_team]['Att. Half Regains'].values[0],1))})")
        with col3: custom_progress_bar(int(pct3), f"Shots from Pressing   ({round(team_rankings[team_rankings['Team'] == selected_team]['Shots after Pressure Regains'].values[0],1)})")

        with col1: custom_progress_bar(int(pct4), f"PPDA   ({round(team_rankings[team_rankings['Team'] == selected_team]['PPDA'].values[0],1)})")
        with col2: custom_progress_bar(int(pct5), f"Avg. Def. Distance   ({int(round(team_rankings[team_rankings['Team'] == selected_team]['Avg. Defensive Distance'].values[0],1))}m)")
        with col3: custom_progress_bar(int(pct6), f"Own Half Entries Conc.   ({int(round(team_rankings[team_rankings['Team'] == selected_team]['Def Half Entries Allowed'].values[0],1))})")

       

        st.write("")
      
        selected_metrics = ['Avg. Defensive Distance', 'PPDA']
        #df = pd.DataFrame(data) 
        df = full_team_data.sort_values(by='match_id')

        #metrics = orig_cols#[col for col in df.columns if col != 'Match']
        metrics = ['Avg. Defensive Distance',
                'Att. Third Pressures', 
                'Def Half Entries Allowed',
                'PPDA',
                'Shots after Pressure Regains',
                'Att. Half Regains']
        print(metrics)
        if 'selected_metrics_t1' not in st.session_state:
            #st.session_state.selected_metrics = metrics[:2]  # Default to first two metrics
            st.session_state.selected_metrics_t1 = ['Avg. Defensive Distance', 'PPDA']
        

        # Create a Streamlit app
        #st.title("Metric Visualization")

        # Function to update the chart based on selected metrics
        def update_chart(selected_metrics):
            fig = go.Figure()
            colors = ['white', 'purple']

            # Add traces for selected metrics
            for i, metric in enumerate(selected_metrics):
                fig.add_trace(go.Scatter(
                    x=df['Match'], y=df[metric],
                    mode='lines+markers',
                    name=metric,
                    yaxis='y' if i == 0 else 'y2',
                    line = dict(color=colors[i]),
                    showlegend=False
                ))
            title_colors = {
                selected_metrics[0]: 'white',
                selected_metrics[1] if len(selected_metrics) > 1 else None: 'purple'
            }
            
            if len(selected_metrics) == 2:
                #title = f"<b style='color:{title_colors[selected_metrics[0]]}'>{selected_metrics[0]}</b> vs <b style='color:{title_colors[selected_metrics[1]]}'>{selected_metrics[1]}</b>"
                title = f"<b style='color:{title_colors[selected_metrics[0]]}'>{selected_metrics[0]}</b> <b style='color: white'>vs</b> <b style='color:{title_colors[selected_metrics[1]]}'>{selected_metrics[1]}</b>"
            else:
                title = f"<b style='color:{title_colors[selected_metrics[0]]}'>{selected_metrics[0]}</b>"
           
           
             
            layout = {
                'title': {
                    'text': title,
                    'x': 0.5,  # Center the title horizontally
                    'xanchor': 'center',  # Anchor the title to the center horizontally
                    'yanchor': 'top',  # Anchor the title to the top vertically
                    'font': {
                        'size': 18,  # Adjust font size if needed
                        'color': 'black'  # Adjust color if needed
                    },
                    'pad': {
                        'b': 20  # Adjust this value to reduce/increase space below the title
                    }
                },
                'xaxis': {
                    'title': "Match",
                    'tickangle': -40
                    },
                'yaxis': {'title': selected_metrics[0], 'side': "left"},
                'legend': {
                    'orientation': "h",
                    'yanchor': "bottom",
                    'y': 1.02,
                    'xanchor': "center",
                    'x': 0.5,
                #   'itemclick': "toggleoff",
                #    'itemdoubleclick': "toggle"
                }
            }

            # Add second y-axis if two metrics are selected
            if len(selected_metrics) == 2:
                layout['yaxis2'] = {'title': selected_metrics[1], 'side': "right", 'overlaying': "y"}
            
            if selected_metrics[0] in neg_cols:
                layout['yaxis']['autorange'] = 'reversed'
            if len(selected_metrics) == 2 and selected_metrics[1] in neg_cols:
                layout['yaxis2']['autorange'] = 'reversed'

            fig.update_layout(layout)

            print(st.session_state.selected_metrics_t1)

            return fig

        # Create columns for metrics selection
        cols = st.columns(len(metrics))

        for i, metric in enumerate(metrics):
            with cols[i]:
                if st.checkbox(metric, value=(metric in st.session_state.selected_metrics_t1)):
                    if metric not in st.session_state.selected_metrics_t1:
                        st.session_state.selected_metrics_t1.append(metric)
                else:
                    if metric in st.session_state.selected_metrics_t1:
                        st.session_state.selected_metrics_t1.remove(metric)

        # Enforce the restriction of selecting only 1 or 2 metrics
        if len(st.session_state.selected_metrics_t1) < 1 or len(st.session_state.selected_metrics_t1) > 2:
            st.error("Please select exactly 1 or 2 metrics.")
        else:
            # Create and display the plot
            fig = update_chart(st.session_state.selected_metrics_t1)
            st.plotly_chart(fig)








        col1, col2 = st.columns(2)
        with col1:
            if len(selected_ids) <= 5:
                team_rankings2 = league_data.groupby('Team').agg(aggs).reset_index()
                for col in orig_cols:
                    team_rankings2[col] = round(team_rankings2[col],1)
                for col in orig_cols:
                    if col not in ['match_id', 'Opponent', 'Match Date', 'Team', 'Venue']:
                        if col in neg_cols:
                            team_rankings2[f"pct{col}"] = 100 - round(team_rankings2[col].rank(pct=True) * 100,2)

                        else:
                            team_rankings2[f"pct{col}"] = round(team_rankings2[col].rank(pct=True) * 100,2)

                
                                
                
                team_rankings2['Pressing'] = ((0.2 * team_rankings2['pctPPDA']) + (0.25 * team_rankings2['pctAvg. Defensive Distance']) + (0.2 * team_rankings2['pctAtt. Third Pressures']) + (0.25 * team_rankings2['pctAtt. Half Regains']) + (0.1 * team_rankings2['pctShots after Pressure Regains']))
                #team_rankings['Pressing'] = round(team_rankings['Pressing'].rank(pct=True) * 100,2)
                team_rankings2['Pressing Rating'] = round(team_rankings2['Pressing'],1)
                team_rankings2 = team_rankings2[team_rankings2['Team'] != selected_team]
                team_rankings = team_rankings[team_rankings['Team'] == selected_team]
                
                team_rankings = pd.concat([team_rankings, team_rankings2], ignore_index=True)

                #print(team_rankings[team_rankings['Team'] == selected_team]['Pressing Rating'].values[0])

                
                            


            for col in orig_cols:
                team_rankings[col] = round(team_rankings[col],2)
                shortened_pressing_data = team_rankings.sort_values(by = 'Pressing Rating', ascending=False)
                shortened_pressing_data = shortened_pressing_data[['Team','Matches', 'Pressing Rating','Avg. Defensive Distance', 'Att. Third Pressures', 'Def Half Entries Allowed', 'PPDA', 'Shots after Pressure Regains', 'Att. Half Regains', ]]
                #st.write(shortened_pressing_data)

            shortened_pressing_data['Team'] = shortened_pressing_data['Team'].replace({
                'Charleston Battery': 'Charleston',
                'New Mexico United': 'New Mexico',
                'Tampa Bay Rowdies': 'Tampa Bay',
                'Oakland Roots SC': 'Oakland',
                'Memphis 901': 'Memphis',
                'Sacramento Republic': 'Sacramento',
                'Colorado Springs': 'Colorado',
                'Detroit City': 'Detroit',
                'Las Vegas Lights': 'Las Vegas',
                'Indy Eleven': 'Indy',
                'Birmingham Legion': 'Birmingham',
                'Loudoun United': 'Loudoun',
                'Pittsburgh Riverhounds': 'Pitt',
                'Phoenix Rising': 'Phoenix',
                'Hartford Athletic': 'Hartford',
                'Monterey Bay': 'Monterey',
                'Orange County SC': 'Orange County',
                'El Paso Locomotive': 'El Paso'
                
            })
            shortened_pressing_data.set_index('Team', inplace=True)

            #st.dataframe(shortened_pressing_data, use_container_width=True, height = 280)
            st.dataframe(shortened_pressing_data, height = 280)

            
 
        with col2:
            

            # mins = pd.read_parquet(f"TeamMinutesPerGame.parquet")
            # def short_names(x):
            #     if x == 'Ray Serrano Lopez': return 'Ray Serrano'
            #     elif x == 'Jorge Gonzalez Asensi': return 'Jorge Gonzalez'
            #     elif x == 'Jake Francis Morris': return 'Jake Morris'
            #     elif x == 'Arturo Osuna Ordoñez': return 'Arturo Ordoñez'
            #     elif x == 'Phillip Joseph Goodrum': return 'Phillip Goodrum'
            #     else: return x

            # import matplotlib.pyplot as plt
            # import numpy as np
            # import pandas as pd
            # from mplsoccer.pitch import Pitch
            # import io
            # import streamlit as st

            # # Define pitch dimensions for a 'statsbomb' pitch
            # pitch_length = 120
            # pitch_width = 80

            # # Define the pitch
            # pitch = Pitch(pitch_type='statsbomb', pitch_color='black', line_color='#c7d5cc',
            #             half=False, pad_top=8, corner_arcs=True)

            # # Define the number of bins for x and y axes
            # n_bins_x = 6
            # n_bins_y = 5

            # # Define bin edges based on pitch dimensions
            # x_bins = np.linspace(0, pitch_length, n_bins_x + 1)
            # y_bins = np.linspace(0, pitch_width, n_bins_y + 1)

            # # Get the number of team games and league games
            

            # pressures = pd.read_parquet(f"{league}VideoPressureEvents.parquet")
            # team_pressures = pressures[(pressures['team'] == selected_team) & (pressures['match_id'].isin(selected_ids))]
            # league_pressures = pressures[pressures['team'] != selected_team]

            # team_games = len(selected_ids)
            # league_games = (len(pressures['match_id'].unique()) * 2) - len(selected_ids)

            # def get_top_players(df, mins, x_start, x_end, y_start, y_end):
            #     bin_data = df[(df['x'] >= x_start) & (df['x'] < x_end) & 
            #                 (df['y'] >= y_start) & (df['y'] < y_end)]
                
            #     player_counts = bin_data['player'].value_counts()
                
            #     if len(selected_ids) == 1:
            #         # Return raw counts without adjustment
            #         top_players = player_counts.nlargest(3)
            #         return [(player, count) for player, count in top_players.items()]
                
            #     else:
            #         total_potential_mins = len(selected_ids) * 90
            #         min_required_mins = total_potential_mins * 0.3
                    
            #         adjusted_counts = {}
            #         for player, count in player_counts.items():
            #             total_minutes = sum(mins[(mins['Player'] == player) & (mins['Game'].isin(selected_ids))]['Minutes'])
                        
            #             if total_minutes >= min_required_mins:
            #                 adjusted_count = count / (total_minutes / 90)
            #                 adjusted_counts[player] = adjusted_count
                    
            #         top_players = sorted(adjusted_counts.items(), key=lambda x: x[1], reverse=True)[:3]
            #         return [(player, count) for player, count in top_players]

            # # Aggregate the team's pressures into bins and divide by the number of team games
            # team_heatmap, xedges, yedges = np.histogram2d(team_pressures['x'], team_pressures['y'], bins=(x_bins, y_bins))
            # team_heatmap_per_game = team_heatmap / team_games

            # # Aggregate the league's pressures into bins and divide by the number of league games
            # league_heatmap, _, _ = np.histogram2d(league_pressures['x'], league_pressures['y'], bins=(x_bins, y_bins))
            # league_heatmap_per_game = league_heatmap / league_games

            # # Calculate the ratio heatmap
            # ratio_heatmap = team_heatmap_per_game / league_heatmap_per_game

            # # Visualization
            # fig, ax = pitch.draw(figsize=(12, 8))
            # fig.set_facecolor('black')

            # # Ensure the heatmap aligns correctly with the pitch dimensions
            # extent = [0, pitch_length, 0, pitch_width]

            # def get_bin_color(ratio_value):
            #     if ratio_value > 1.45:
            #         return "#df3036"
            #     elif ratio_value > 1.25:
            #         return "#e44e52"
            #     elif ratio_value > 1.15:
            #         return "#e86a6e"
            #     elif ratio_value > 1.05:
            #         return "#f2aeb1"
            #     elif ratio_value >= 1.00:
            #         return "#f7e1e3"
            #     elif ratio_value > 0.95:
            #         return "#909ba5"
            #     elif ratio_value > 0.85:
            #         return "#798590"
            #     elif ratio_value > 0.75:
            #         return "#374a5e"
            #     elif ratio_value > 0.65:
            #         return "#32455a"
            #     elif ratio_value > 0.55:
            #         return "#0d243a"
            #     else:
            #         return "#11263e"

            # # Add bin outlines and labels
            # for i in range(n_bins_x):
            #     for j in range(n_bins_y):
            #         team_pressures_value = team_heatmap_per_game[i, j]
            #         league_pressures_value = league_heatmap_per_game[i, j]
            #         ratio_value = ratio_heatmap[i, j]
                    
            #         # Get the top three players and their pressure counts for this bin
            #         # top_players = get_top_players(team_pressures, 
            #         #                             x_bins[i], x_bins[i+1],
            #         #                             y_bins[j], y_bins[j+1])
                    
            #         top_players = get_top_players(team_pressures, 
            #                                       mins, x_bins[i], x_bins[i+1], 
            #                                       y_bins[j], y_bins[j+1])

                    
            #         # Get the color for the current bin based on ratio_value
            #         bin_color = get_bin_color(ratio_value)
                    
            #         # Add a rectangle to represent the bin with the appropriate color
            #         ax.add_patch(plt.Rectangle((x_bins[i], y_bins[j]), x_bins[i + 1] - x_bins[i], y_bins[j + 1] - y_bins[j],
            #                                 color=bin_color, ec='white', lw=0.6, alpha=0.8))
                    
            # #         # Add the multiple (ratio_value) in each bin
            # #         ax.text(x_bins[i] + (x_bins[i + 1] - x_bins[i]) / 2,
            # #                 y_bins[j] + (y_bins[j + 1] - y_bins[j]) / 2 - 6,
            # #                 f"x{ratio_value:.2f}",
            # #                 ha='center', va='center', color='white', fontsize=8)

            # #         # Add team and league pressures per game values above the multiple
            # #         ax.text(x_bins[i] + (x_bins[i + 1] - x_bins[i]) / 2,
            # #                 y_bins[j] + (y_bins[j + 1] - y_bins[j]) / 2 - 2,
            # #                 f"{team_pressures_value:.2f}\n{league_pressures_value:.2f}",
            # #                 ha='center', va='center', color='white', fontsize=8)
                    
            #         # Add top three players and their pressure counts if available
            # #         if top_players:
            # #             players_text = "\n".join(f"{player} ({count})" for player, count in top_players)
            # #             ax.text(x_bins[i] + (x_bins[i + 1] - x_bins[i]) / 2,
            # #                     y_bins[j] + (y_bins[j + 1] - y_bins[j]) / 2,
            # #                     players_text,
            # #                     ha='center', va='center', color='white', fontsize=7)
                        
            #         if top_players:
            #             players_text = "\n".join(f"{idx}. {short_names(player)} ({round(count,1)})" for idx, (player, count) in enumerate(top_players, 1))
            #             ax.text(x_bins[i] + (x_bins[i + 1] - x_bins[i]) / 2,
            #                     y_bins[j] + (y_bins[j + 1] - y_bins[j]) / 1.55,
            #                     players_text,
            #                     ha='center', va='top', color='white', fontsize=9.5)
         
                    
            # # Adding title and labels
            # # ax.set_title(f"{selected_team} - {season} Pressures per Game", fontsize=20, color='white')

            # # Save the figure
            # buf = io.BytesIO()
            # plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
            # buf.seek(0)

            # # Display the image
            # st.image(buf, use_column_width=True)
            # st.write("Pressure Map over selected timeframe")



            # #st.image("/Users/malekshafei/Downloads/Seattle Reign pressures, 2024-08-26.png")

            from matplotlib.offsetbox import OffsetImage, AnnotationBbox

            mins = pd.read_parquet(f"TeamMinutesPerGame.parquet")
            def short_names(x):
                if x == 'Ray Serrano Lopez': return 'R. Serrano'
                elif x == 'Jorge Gonzalez Asensi': return 'J. Gonzalez'
                elif x == 'Jake Francis Morris': return 'J. Morris'
                elif x == 'Arturo Osuna Ordoñez': return 'A. Ordonez'
                elif x == 'Phillip Joseph Goodrum': return 'P. Goodrum'
                elif x == 'Amadou Dia': return 'A. Dia'
                elif x == 'Jansen Wilson': return 'J. Wilson'
                elif x == 'Aiden McFadden': return 'A. McFadden'
                elif x == 'Adrien Perez':  return 'A. Perez'
                elif x == 'Kyle Adams': return 'K. Adams'
                elif x == 'Damian Las':  return 'D. Las'
                elif x == 'Taylor Davila':  return 'T. Davila'
                elif x == 'Elijah Wynder': return 'E. Wynder'
                elif x == 'Wesley Charpie': return 'W. Charpie'
                elif x == 'Dylan Mares': return 'D. Mares'
                elif x == 'Niall McCabe': return 'N. McCabe'
                elif x == 'Evan Davila': return 'E. Davila'
                elif x == 'Sean Totsch': return 'S. Totsch'
                elif x == 'Sam Gleadle': return 'S. Gleadle'
                elif x == 'Carlos Moguel Jr.': return 'C. Moguel'
                elif x == 'Tola Showunmi': return 'T. Showunmi'
                elif x == 'Emmanuel Perez': return 'E. Perez'
                elif x == 'Wilson Harris': return "W. Harris"
                
                else: return x

            def playerPics(x):
                if x == 'Wilson Harris': return "LouCityPlayerPhotos/Harris.png"
                elif x == 'Arturo Osuna Ordoñez': return "LouCityPlayerPhotos/Ordonez.png"
                elif x == 'Amadou Dia': return "LouCityPlayerPhotos/Dia.png"
                elif x == 'Jansen Wilson':  return "LouCityPlayerPhotos/Wilson.png"
                elif x == 'Aiden McFadden': return "LouCityPlayerPhotos/McFadden.png" 
                elif x == 'Adrien Perez':  return "LouCityPlayerPhotos/APerez.png"
                elif x == 'Kyle Adams': return "LouCityPlayerPhotos/Adams.png"
                elif x == 'Damian Las':  return "LouCityPlayerPhotos/Las.png"
                elif x == 'Taylor Davila':  return "LouCityPlayerPhotos/TDavila.png"
                elif x == 'Elijah Wynder': return "LouCityPlayerPhotos/Wynder.png"
                elif x == 'Ray Serrano Lopez':  return "LouCityPlayerPhotos/Serrano.png"
                elif x == 'Phillip Joseph Goodrum':  return "LouCityPlayerPhotos/Goodrum.png"
                elif x == 'Wesley Charpie': return "LouCityPlayerPhotos/Charpie.png"
                elif x == 'Dylan Mares': return "LouCityPlayerPhotos/Mares.png"
                elif x == 'Niall McCabe': return "LouCityPlayerPhotos/Harris.png"
                elif x == 'Evan Davila': return "LouCityPlayerPhotos/EDavila.png"
                elif x == 'Sean Totsch': return "LouCityPlayerPhotos/Totsch.png"
                elif x == 'Jake Francis Morris':  return "LouCityPlayerPhotos/Morris.png"
                elif x == 'Sam Gleadle': return "LouCityPlayerPhotos/Gleadle.png"
                elif x == 'Carlos Moguel Jr.': return "LouCityPlayerPhotos/Moguel.png"
                elif x == 'Jorge Gonzalez Asensi':  return "LouCityPlayerPhotos/Gonzalez.png"
                elif x == 'Tola Showunmi': return "LouCityPlayerPhotos/Showunmi.png"
                elif x == 'Emmanuel Perez': return "LouCityPlayerPhotos/MPerez.png"
                else: return "LouCityPlayerPhotos/EmptyPhoto.png"
                
            def add_player_image(ax, player, x, y, width, height):
                img = plt.imread(playerPics(player))
                
                # Calculate zoom to fit the image to the bin size
                img_height, img_width = img.shape[:2]
                zoom_x = width / img_width
                zoom_y = height / img_height
                zoom = min(zoom_x, zoom_y) * 4.1  # 0.9 to leave a small margin

                im = OffsetImage(img, zoom=zoom)
                ab = AnnotationBbox(im, (x, y), xycoords='data', frameon=False, box_alignment=(0.5, 1))
                ax.add_artist(ab)

            import matplotlib.pyplot as plt
            import numpy as np
            import pandas as pd
            from mplsoccer.pitch import Pitch
            import io
            import streamlit as st

            # Define pitch dimensions for a 'statsbomb' pitch
            pitch_length = 120
            pitch_width = 80

            # Define the pitch
            pitch = Pitch(pitch_type='statsbomb', pitch_color='black', line_color='#c7d5cc',
                        half=False, pad_top=8, corner_arcs=True)

            # Define the number of bins for x and y axes
            n_bins_x = 6
            n_bins_y = 5

            # Define bin edges based on pitch dimensions
            x_bins = np.linspace(0, pitch_length, n_bins_x + 1)
            y_bins = np.linspace(0, pitch_width, n_bins_y + 1)

            # Get the number of team games and league games


            pressures = pd.read_parquet(f"{league}VideoPressureEvents.parquet")
            team_pressures = pressures[(pressures['team'] == selected_team) & (pressures['match_id'].isin(selected_ids))]
            league_pressures = pressures[pressures['team'] != selected_team]

            team_games = len(selected_ids)
            league_games = (len(pressures['match_id'].unique()) * 2) - len(selected_ids)

            # Function to get top three players and their pressure counts for a bin
            # def get_top_players(df, x_start, x_end, y_start, y_end):
            #     bin_data = df[(df['x'] >= x_start) & (df['x'] < x_end) & 
            #                 (df['y'] >= y_start) & (df['y'] < y_end)]
            #     if len(bin_data['player'].unique()) < 3:
            #         return []
            #     top_players = bin_data['player'].value_counts().nlargest(3)
            #     return [(player, count) for player, count in top_players.items()]

            # def get_top_players(df, mins, x_start, x_end, y_start, y_end):
            #     bin_data = df[(df['x'] >= x_start) & (df['x'] < x_end) & 
            #       (df['y'] >= y_start) & (df['y'] < y_end)]
            #     # if len(bin_data['player'].unique()) < 3:
            #     #     return []

            #     player_counts = bin_data['player'].value_counts()

            #     adjusted_counts = {}
            #     for player, count in player_counts.items():
            #         total_minutes = sum(mins[(mins['Player'] == player) & (mins['Game'].isin(selected_ids))]['Minutes'])
            #         adjusted_count = count / (total_minutes / 90) if total_minutes > 0 else 0
            #         adjusted_counts[player] = adjusted_count

            #     top_players = sorted(adjusted_counts.items(), key=lambda x: x[1], reverse=True)[:3]
            #     return [(player, count) for player, count in top_players]

            def get_top_players(df, mins, x_start, x_end, y_start, y_end):
                bin_data = df[(df['x'] >= x_start) & (df['x'] < x_end) & 
                            (df['y'] >= y_start) & (df['y'] < y_end)]

                player_counts = bin_data['player'].value_counts()

                if len(selected_ids) == 1:
                    # Return raw counts without adjustment
                    top_players = player_counts.nlargest(3)
                    return [(player, count) for player, count in top_players.items()]

                else:
                    total_potential_mins = len(selected_ids) * 90
                    min_required_mins = total_potential_mins * 0.3

                    adjusted_counts = {}
                    for player, count in player_counts.items():
                        total_minutes = sum(mins[(mins['Player'] == player) & (mins['Game'].isin(selected_ids))]['Minutes'])

                        if total_minutes >= min_required_mins:
                            adjusted_count = count / (total_minutes / 90)
                            adjusted_counts[player] = adjusted_count

                    top_players = sorted(adjusted_counts.items(), key=lambda x: x[1], reverse=True)[:3]
                    return [(player, count) for player, count in top_players]

            # Aggregate the team's pressures into bins and divide by the number of team games
            team_heatmap, xedges, yedges = np.histogram2d(team_pressures['x'], team_pressures['y'], bins=(x_bins, y_bins))
            team_heatmap_per_game = team_heatmap / team_games

            # Aggregate the league's pressures into bins and divide by the number of league games
            league_heatmap, _, _ = np.histogram2d(league_pressures['x'], league_pressures['y'], bins=(x_bins, y_bins))
            league_heatmap_per_game = league_heatmap / league_games

            # Calculate the ratio heatmap
            ratio_heatmap = team_heatmap_per_game / league_heatmap_per_game

            # Visualization
            fig, ax = pitch.draw(figsize=(12, 8))
            fig.set_facecolor('black')

            # Ensure the heatmap aligns correctly with the pitch dimensions
            extent = [0, pitch_length, 0, pitch_width]

            def get_bin_color(ratio_value):
                if ratio_value > 1.45:
                    return "#df3036"
                elif ratio_value > 1.25:
                    return "#e44e52"
                elif ratio_value > 1.15:
                    return "#e86a6e"
                elif ratio_value > 1.05:
                    return "#f2aeb1"
                elif ratio_value >= 1.00:
                    return "#f7e1e3"
                elif ratio_value > 0.95:
                    return "#909ba5"
                elif ratio_value > 0.85:
                    return "#798590"
                elif ratio_value > 0.75:
                    return "#374a5e"
                elif ratio_value > 0.65:
                    return "#32455a"
                elif ratio_value > 0.55:
                    return "#0d243a"
                else:
                    return "#11263e"

            # Add bin outlines and labels
            for i in range(n_bins_x):
                for j in range(n_bins_y):
                    team_pressures_value = team_heatmap_per_game[i, j]
                    league_pressures_value = league_heatmap_per_game[i, j]
                    ratio_value = ratio_heatmap[i, j]

                    # Get the top three players and their pressure counts for this bin
                    # top_players = get_top_players(team_pressures, 
                    #                             x_bins[i], x_bins[i+1],
                    #                             y_bins[j], y_bins[j+1])

                    top_players = get_top_players(team_pressures, 
                                                mins, x_bins[i], x_bins[i+1], 
                                                y_bins[j], y_bins[j+1])


                    # Get the color for the current bin based on ratio_value
                    bin_color = get_bin_color(ratio_value)

                    # Add a rectangle to represent the bin with the appropriate color
                    ax.add_patch(plt.Rectangle((x_bins[i], y_bins[j]), x_bins[i + 1] - x_bins[i], y_bins[j + 1] - y_bins[j],
                                            color=bin_color, ec='white', lw=0.6, alpha=0.8))

            #         # Add the multiple (ratio_value) in each bin
            #         ax.text(x_bins[i] + (x_bins[i + 1] - x_bins[i]) / 2,
            #                 y_bins[j] + (y_bins[j + 1] - y_bins[j]) / 2 - 6,
            #                 f"x{ratio_value:.2f}",
            #                 ha='center', va='center', color='white', fontsize=8)

            #         # Add team and league pressures per game values above the multiple
            #         ax.text(x_bins[i] + (x_bins[i + 1] - x_bins[i]) / 2,
            #                 y_bins[j] + (y_bins[j + 1] - y_bins[j]) / 2 - 2,
            #                 f"{team_pressures_value:.2f}\n{league_pressures_value:.2f}",
            #                 ha='center', va='center', color='white', fontsize=8)

                    # Add top three players and their pressure counts if available
            #         if top_players:
            #             players_text = "\n".join(f"{player} ({count})" for player, count in top_players)
            #             ax.text(x_bins[i] + (x_bins[i + 1] - x_bins[i]) / 2,
            #                     y_bins[j] + (y_bins[j + 1] - y_bins[j]) / 2,
            #                     players_text,
            #                     ha='center', va='center', color='white', fontsize=7)

                    if top_players:
                        # Calculate bin dimensions
                        bin_width = x_bins[i + 1] - x_bins[i]
                        bin_height = y_bins[j + 1] - y_bins[j]

                        # Calculate positions for image and text
                        x_center = x_bins[i] + bin_width / 2
                        y_top = y_bins[j + 1] - 3.8  # Top of the bin
                        y_text = y_top - bin_height * 0.1  # Text slightly below the top

                        # Add player image
                        add_player_image(ax, top_players[0][0], x_center, y_top - 11.5, bin_width, bin_height * 0.8)

                        # Prepare and add text
                        players_text = "\n".join(f"{idx}. {short_names(player)} ({round(count,1)})" for idx, (player, count) in enumerate(top_players, 1))
                        ax.text(x_center, y_text + 0.8, players_text,
                                ha='center', va='top', color='white', fontsize=8.5, linespacing=0.85)
                        

            # Adding title and labels
            # ax.set_title(f"{selected_team} - {season} Pressures per Game", fontsize=20, color='white')

            # Save the figure
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
            buf.seek(0)

            # Display the image
            st.image(buf, use_column_width=True)


        
    
 

        #dual_progress_bars(60, "Progress 1", 85, "Progress 2")


    
        col1, col2 = st.columns(2)
        with col1: 
            metric = st.selectbox(
            'Select Metric',
            ['Attacking Half Regains', 'Box Entries after Regains', 'Shots after Press Regains']
            )
        
        if metric == 'Attacking Half Regains': data = pd.read_parquet("att_half_regains_video_events.parquet")
        elif metric == 'Box Entries after Regains': data = pd.read_parquet("regains_to_box_entry_video_events.parquet")
        elif metric == 'Shots after Press Regains': data = pd.read_parquet("press_to_shot_video_events.parquet")
        data = data.drop_duplicates(subset = ['match_id', 'period', 'minute']).reset_index()

        data = data[data['match_id'].isin(selected_ids)].reset_index()
        if len(data) == 0: 
            st.error("No events in selected matches")
        
        # with col2:
        #     sort_method = st.selectbox(
        #         'Sort By',
        #         ['Most Recent']
        #     )
        
        if 'clip_index_t1' not in st.session_state:
            st.session_state.clip_index_t1 = 0
        def update_index(step):
            new_index = st.session_state.clip_index_t1 + step
            if 0 <= new_index < len(clip_titles):
                st.session_state.clip_index_t1 = new_index
                st.session_state.clip_selector_t1 = clip_titles[new_index]

        sorted_data = data.sort_values(by=['match_id', 'period', 'timestamp'], ascending=[False, True, True])
        clip_titles = sorted_data['title'].tolist()

        
        with col2:
            #selection = st.selectbox('Choose Clip', data.sort_values(by=['match_id', 'period', 'timestamp'], ascending=[False,True,True])['title'])
            # sorted_data = data.sort_values(by=['match_id', 'period', 'timestamp'], ascending=[False, True, True])
            # clip_titles = sorted_data['title'].tolist()


            #selection = st.selectbox('Choose Clip', clip_titles, index=st.session_state.clip_index)
            print("index", st.session_state.clip_index_t1)
            print(len(clip_titles))
            selection = st.selectbox('Choose Clip', clip_titles, index=st.session_state.clip_index_t1, key='clip_selector_t1')
            if selection != clip_titles[st.session_state.clip_index_t1]:
                st.session_state.clip_index_t1 = clip_titles.index(selection)

            
 


        match_selection = data.loc[data['title'] == selection]['match_id'].values[0]
        half_selection = data.loc[data['title'] == selection]['period'].values[0]
        time_selection = data.loc[data['title'] == selection]['timestamp'].values[0]


        def find_closest_segment_with_times(time_str, segment_length = 60, overlap = 30):
            # Convert time_str to seconds
            minutes, seconds = map(int, time_str.split(':'))
            time_in_seconds = (minutes * 60 + seconds) - 5 #5 seconds before clip

            # Calculate segment details
            step = segment_length - overlap
            segment_number = time_in_seconds // step + 1
            
            # Calculate the start time of the segment
            start_time = (segment_number - 1) * step
            end_time = start_time + segment_length
            
            # Calculate time within segment
            time_within_segment = time_in_seconds - start_time
            
            return segment_number, time_within_segment

        # # Example usage
        # segment_length = 60  # 1 minute segments
        # overlap = 30  # 30 seconds overlap

        time_str = time_selection[3:8]
        print(time_str)
        segment, time_within_segment = find_closest_segment_with_times(time_str)


        csv_file_path = 'drive_files.csv'
        files_df = pd.read_csv(csv_file_path)

        def display_video(match_selection, half_selection, segment):
            
            filename = f"{match_selection}-h{half_selection}-{segment}.mp4"
            print(filename)
            file_id = files_df.loc[files_df['File Name'] == filename]['File ID'].values[0]
            # files = list_files_in_folder(FOLDER_ID)
            # file_id = get_file_id(filename, files)
            
            if file_id:
                #video_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                #video_url = f"https://drive.google.com/file/d/{file_id}/view"
                video_url = f"https://drive.google.com/file/d/{file_id}/preview?t={time_within_segment}"


                print(f"{filename} -> Video URL: {video_url}")  # Debug print statement
                # Use an HTML video tag
                #st.markdown(f'<video width="640" height="480" controls><source src="{video_url}" type="video/mp4">Your browser does not support the video tag.</video>', unsafe_allow_html=True)
                st.markdown(f'<iframe src="{video_url}" width="704" height="528" frameborder="0" allow="autoplay"; encrypted-media" allowfullscreen></iframe>', unsafe_allow_html=True)
                

                
                #st.video(video_url)
                #
            else:
                st.error(f"Video '{filename}' not found in the folder.")


        display_video(match_selection, half_selection, segment)
        
        # col1, col2 = st.columns(2)

        # with col1:
        st.button("Previous Clip", on_click=update_index, args=(-1,), disabled=(st.session_state.clip_index_t1 <= 0), key="prev_clip_button_t1")

        # with col2:
        st.button("Next Clip", on_click=update_index, args=(1,), disabled=(st.session_state.clip_index_t1 >= len(clip_titles) - 1), key="next_clip_button_t1")

        # # Force rerun if the index has changed
        # if st.session_state.clip_index != clip_titles.index(selection):
        #     st.rerun()

        #st.video("lou-video-test/3930499-h2-93.mp4")


    with tab2:
        
        pct1 = team_rankings[team_rankings['Team'] == selected_team]['pct% of Goal Kicks Short'].values[0]
        pct2 = team_rankings[team_rankings['Team'] == selected_team]['pctPasses per Sequence'].values[0]
        pct3 = team_rankings[team_rankings['Team'] == selected_team]['pctAvg. Buildup Speed'].values[0]
        pct4 = team_rankings[team_rankings['Team'] == selected_team]['pctAvg. Distance Reached'].values[0]
        pct5 = team_rankings[team_rankings['Team'] == selected_team]['pct% -> Att. Half'].values[0]
        pct6 = team_rankings[team_rankings['Team'] == selected_team]['pct% -> Att. Third'].values[0]


        
       
        col1, col2, col3 = st.columns(3)
        with col1: custom_progress_bar(int(pct1), f"% of Goal Kicks Short   ({int(round(team_rankings[team_rankings['Team'] == selected_team]['% of Goal Kicks Short'].values[0],1))}%)")
        with col2: custom_progress_bar(int(pct1), f"Passes per Sequence   ({round(team_rankings[team_rankings['Team'] == selected_team]['Passes per Sequence'].values[0],1)})")
        with col3: custom_progress_bar(int(pct1), f"Avg. Buildup Speed   ({round(team_rankings[team_rankings['Team'] == selected_team]['Avg. Buildup Speed'].values[0],1)} m/s)")
        
        with col1: custom_progress_bar(int(pct2), f"Avg. Distance Reached   ({int(round(team_rankings[team_rankings['Team'] == selected_team]['Avg. Distance Reached'].values[0],1))}m)")
        with col2: custom_progress_bar(int(pct4), f"% -> Att. Half   ({int(round(team_rankings[team_rankings['Team'] == selected_team]['% -> Att. Half'].values[0],1))}%)")
        with col3: custom_progress_bar(int(pct5), f"% -> Att. Third   ({int(round(team_rankings[team_rankings['Team'] == selected_team]['% -> Att. Third'].values[0],1))}%)")

        
        st.write("")
        
        selected_metrics = ['Avg. Distance Reached', 'Avg. Buildup Speed']
        #df = pd.DataFrame(data) 
        df = full_team_data.sort_values(by='match_id')

        #metrics = orig_cols#[col for col in df.columns if col != 'Match']
        metrics = ['% of Goal Kicks Short',
                   'Passes per Sequence',
                    'Avg. Buildup Speed',
                    'Avg. Distance Reached',
                    '% -> Att. Half',
                    '% -> Att. Third']
        print(metrics)
        if 'selected_metrics_t2' not in st.session_state:
            #st.session_state.selected_metrics = metrics[:2]  # Default to first two metrics
            st.session_state.selected_metrics_t2 = ['Avg. Buildup Speed', '% -> Att. Half']
        

        

        # Function to update the chart based on selected metrics
        def update_chart(selected_metrics):
            fig = go.Figure()
            colors = ['white', 'purple']

            # Add traces for selected metrics
            for i, metric in enumerate(selected_metrics):
                fig.add_trace(go.Scatter(
                    x=df['Match'], y=df[metric],
                    mode='lines+markers',
                    name=metric,
                    yaxis='y' if i == 0 else 'y2',
                    line = dict(color=colors[i]),
                    showlegend=False
                ))
            title_colors = {
                selected_metrics[0]: 'white',
                selected_metrics[1] if len(selected_metrics) > 1 else None: 'purple'
            }
            
            if len(selected_metrics) == 2:
                #title = f"<b style='color:{title_colors[selected_metrics[0]]}'>{selected_metrics[0]}</b> vs <b style='color:{title_colors[selected_metrics[1]]}'>{selected_metrics[1]}</b>"
                title = f"<b style='color:{title_colors[selected_metrics[0]]}'>{selected_metrics[0]}</b> <b style='color: white'>vs</b> <b style='color:{title_colors[selected_metrics[1]]}'>{selected_metrics[1]}</b>"
            else:
                title = f"<b style='color:{title_colors[selected_metrics[0]]}'>{selected_metrics[0]}</b>"
           
           
              
            layout = {
                'title': {
                    'text': title,
                    'x': 0.5,  # Center the title horizontally
                    'xanchor': 'center',  # Anchor the title to the center horizontally
                    'yanchor': 'top',  # Anchor the title to the top vertically
                    'font': {
                        'size': 18,  # Adjust font size if needed
                        'color': 'black'  # Adjust color if needed
                    },
                    'pad': {
                        'b': 20  # Adjust this value to reduce/increase space below the title
                    }
                },
                'xaxis': {
                    'title': "Match",
                    'tickangle': -40
                    },
                'yaxis': {'title': selected_metrics[0], 'side': "left"},
                'legend': {
                    'orientation': "h",
                    'yanchor': "bottom",
                    'y': 1.02,
                    'xanchor': "center",
                    'x': 0.5,
                #   'itemclick': "toggleoff",
                #    'itemdoubleclick': "toggle"
                }
            }

            # Add second y-axis if two metrics are selected
            if len(selected_metrics) == 2:
                layout['yaxis2'] = {'title': selected_metrics[1], 'side': "right", 'overlaying': "y"}
            
            if selected_metrics[0] in neg_cols:
                layout['yaxis']['autorange'] = 'reversed'
            if len(selected_metrics) == 2 and selected_metrics[1] in neg_cols:
                layout['yaxis2']['autorange'] = 'reversed'

            fig.update_layout(layout)

            print(st.session_state.selected_metrics_t2)

            return fig

        # Create columns for metrics selection
        cols = st.columns(len(metrics))

        for i, metric in enumerate(metrics):
            with cols[i]:
                if st.checkbox(metric, value=(metric in st.session_state.selected_metrics_t2)):
                    if metric not in st.session_state.selected_metrics_t2:
                        st.session_state.selected_metrics_t2.append(metric)
                else:
                    if metric in st.session_state.selected_metrics_t2:
                        st.session_state.selected_metrics_t2.remove(metric)

        # Enforce the restriction of selecting only 1 or 2 metrics
        if len(st.session_state.selected_metrics_t2) < 1 or len(st.session_state.selected_metrics_t2) > 2:
            st.error("Please select exactly 1 or 2 metrics.")
        else:
            # Create and display the plot
            fig = update_chart(st.session_state.selected_metrics_t2)
            st.plotly_chart(fig)








        col1, col2 = st.columns(2)
        with col1:
            if len(selected_ids) <= 5:
                team_rankings2 = league_data.groupby('Team').agg(aggs).reset_index()
                for col in orig_cols:
                    team_rankings2[col] = round(team_rankings2[col],1)
                for col in orig_cols:
                    if col not in ['match_id', 'Opponent', 'Match Date', 'Team', 'Venue']:
                        if col in neg_cols:
                            team_rankings2[f"pct{col}"] = 100 - round(team_rankings2[col].rank(pct=True) * 100,2)

                        else:
                            team_rankings2[f"pct{col}"] = round(team_rankings2[col].rank(pct=True) * 100,2)

                
                                
                
                team_rankings2['Pressing'] = ((0.2 * team_rankings2['pctPPDA']) + (0.25 * team_rankings2['pctAvg. Defensive Distance']) + (0.2 * team_rankings2['pctAtt. Third Pressures']) + (0.25 * team_rankings2['pctAtt. Half Regains']) + (0.1 * team_rankings2['pctShots after Pressure Regains']))
                #team_rankings['Pressing'] = round(team_rankings['Pressing'].rank(pct=True) * 100,2)
                team_rankings2['Pressing Rating'] = round(team_rankings2['Pressing'],1)

                team_rankings2['Goal Kick Buildouts'] = ((0.3 * team_rankings2['pctAvg. Distance Reached']) + (0.15 * team_rankings2['pctAvg. Buildup Speed']) + (0.4 * team_rankings2['pct% -> Att. Half']) + (0.15 * team_rankings2['pctPasses per Sequence']))
                #team_rankings['pctShort GK Buildups'] = round(team_rankings['Short GK Buildups'].rank(pct=True) * 100,2)
                team_rankings2['Goal Kick Buildout Rating'] = round(team_rankings2['Goal Kick Buildouts'],1)




                team_rankings2 = team_rankings2[team_rankings2['Team'] != selected_team]
                team_rankings = team_rankings[team_rankings['Team'] == selected_team]
                
                team_rankings = pd.concat([team_rankings, team_rankings2], ignore_index=True)

                #print(team_rankings[team_rankings['Team'] == selected_team]['Pressing Rating'].values[0])

                
                            


            for col in orig_cols:
                team_rankings[col] = round(team_rankings[col],2)
                shortened_gk_data = team_rankings.sort_values(by = 'Goal Kick Buildout Rating', ascending=False)
                shortened_gk_data = shortened_gk_data[['Team','Matches', 'Goal Kick Buildout Rating', '% of Goal Kicks Short', 'Passes per Sequence', 'Avg. Buildup Speed', 'Avg. Distance Reached','% -> Att. Half', '% -> Att. Third']]
                #st.write(shortened_pressing_data)

            shortened_gk_data['Team'] = shortened_gk_data['Team'].replace({
                'Charleston Battery': 'Charleston',
                'New Mexico United': 'New Mexico',
                'Tampa Bay Rowdies': 'Tampa Bay',
                'Oakland Roots SC': 'Oakland',
                'Memphis 901': 'Memphis',
                'Sacramento Republic': 'Sacramento',
                'Colorado Springs': 'Colorado',
                'Detroit City': 'Detroit',
                'Las Vegas Lights': 'Las Vegas',
                'Indy Eleven': 'Indy',
                'Birmingham Legion': 'Birmingham',
                'Loudoun United': 'Loudoun',
                'Pittsburgh Riverhounds': 'Pitt',
                'Phoenix Rising': 'Phoenix',
                'Hartford Athletic': 'Hartford',
                'Monterey Bay': 'Monterey',
                'Orange County SC': 'Orange County',
                'El Paso Locomotive': 'El Paso'
                
            })
            shortened_gk_data.set_index('Team', inplace=True)

            #st.dataframe(shortened_pressing_data, use_container_width=True, height = 280)
            st.dataframe(shortened_gk_data, height = 280)

            
        with col2:
            import matplotlib.pyplot as plt
            import numpy as np
            import pandas as pd
            from mplsoccer.pitch import Pitch
            import io
            import streamlit as st

            # Define pitch dimensions for a 'statsbomb' pitch
            pitch_length = 120
            pitch_width = 80

            # Define the pitch
            pitch = Pitch(pitch_type='statsbomb', pitch_color='black', line_color='#c7d5cc',
                        half=False, pad_top=2, corner_arcs=True)

            fig,ax = pitch.draw(figsize=(6,8))
            fig.set_facecolor('black')

            gk_events = pd.read_parquet(f"{league}VideoGoalKickEvents.parquet")

            gk_events = gk_events[gk_events['match_id'].isin(selected_ids)]

            for _, row in gk_events.iterrows():
                x = row['gk_end_x']
                y = row['gk_end_y']
                pitch.scatter(x,y, ax = ax, color = 'white', s = 20)
                
              
            ax.text(60, -5,'End Location of Short Goal Kick Buildouts', color = 'white', ha = 'center', fontsize = 12.5)
            ax.text(60, -2,'Direction of Attack --->', color = 'white', ha = 'center', fontsize = 10)

            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
            buf.seek(0)

            # Display the image
            st.image(buf, use_column_width=True)


 
    
 

        #dual_progress_bars(60, "Progress 1", 85, "Progress 2")


    
        col1, col2 = st.columns(2)
        with col1: 
            metric = st.selectbox(
            'Select Metric',
            ['Short Goal Kick Buildouts', 'Own Half Turnovers', 'To Final Third', 'Long Goal Kicks']
            )
        
        if metric == 'Short Goal Kick Buildouts': data = pd.read_parquet("gk_short_buildups_video_events.parquet")
        elif metric == 'Own Half Turnovers': data = pd.read_parquet("gk_short_buildups_h1_turnover_video_events.parquet")
        elif metric == 'To Final Third': data = pd.read_parquet("gk_short_buildups_to_final_third_video_events.parquet")
        elif metric == 'Long Goal Kicks': data = pd.read_parquet("gk_long_buildups_video_events.parquet")
        data = data.drop_duplicates(subset = ['match_id', 'period', 'minute']).reset_index()

        data = data[data['match_id'].isin(selected_ids)].reset_index()
        if len(data) == 0: 
            st.error("No events in selected matches")
        
        # with col2:
        #     sort_method = st.selectbox(
        #         'Sort By',
        #         ['Most Recent']
        #     )
        
        if 'clip_index_t2' not in st.session_state:
            st.session_state.clip_index_t2 = 0
        def update_index(step):
            new_index = st.session_state.clip_index_t2 + step
            if 0 <= new_index < len(clip_titles):
                st.session_state.clip_index_t2 = new_index
                st.session_state.clip_selector_t2 = clip_titles[new_index]

        sorted_data = data.sort_values(by=['match_id', 'period', 'timestamp'], ascending=[False, True, True])
        clip_titles = sorted_data['title'].tolist()

        
        with col2:
            #selection = st.selectbox('Choose Clip', data.sort_values(by=['match_id', 'period', 'timestamp'], ascending=[False,True,True])['title'])
            # sorted_data = data.sort_values(by=['match_id', 'period', 'timestamp'], ascending=[False, True, True])
            # clip_titles = sorted_data['title'].tolist()


            #selection = st.selectbox('Choose Clip', clip_titles, index=st.session_state.clip_index)
            print("index", st.session_state.clip_index_t2)
            print(len(clip_titles))
            selection = st.selectbox('Choose Clip', clip_titles, index=st.session_state.clip_index_t2, key='clip_selector_t2')
            if selection != clip_titles[st.session_state.clip_index_t2]:
                st.session_state.clip_index_t2 = clip_titles.index(selection)

            
 


        match_selection = data.loc[data['title'] == selection]['match_id'].values[0]
        half_selection = data.loc[data['title'] == selection]['period'].values[0]
        time_selection = data.loc[data['title'] == selection]['timestamp'].values[0]


        def find_closest_segment_with_times(time_str, segment_length = 60, overlap = 30):
            # Convert time_str to seconds
            minutes, seconds = map(int, time_str.split(':'))
            time_in_seconds = (minutes * 60 + seconds) - 5 #5 seconds before clip

            # Calculate segment details
            step = segment_length - overlap
            segment_number = time_in_seconds // step + 1
            
            # Calculate the start time of the segment
            start_time = (segment_number - 1) * step
            end_time = start_time + segment_length
            
            # Calculate time within segment
            time_within_segment = time_in_seconds - start_time
            
            return segment_number, time_within_segment

        # # Example usage
        # segment_length = 60  # 1 minute segments
        # overlap = 30  # 30 seconds overlap

        time_str = time_selection[3:8]
        print(time_str)
        segment, time_within_segment = find_closest_segment_with_times(time_str)
 

        csv_file_path = 'drive_files.csv'
        files_df = pd.read_csv(csv_file_path)

        def display_video(match_selection, half_selection, segment):
            
            filename = f"{match_selection}-h{half_selection}-{segment}.mp4"
            print(filename)
            file_id = files_df.loc[files_df['File Name'] == filename]['File ID'].values[0]
            # files = list_files_in_folder(FOLDER_ID)
            # file_id = get_file_id(filename, files)
            
            if file_id:
                #video_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                #video_url = f"https://drive.google.com/file/d/{file_id}/view"
                video_url = f"https://drive.google.com/file/d/{file_id}/preview?t={time_within_segment}"


                print(f"{filename} -> Video URL: {video_url}")  # Debug print statement
                # Use an HTML video tag
                #st.markdown(f'<video width="640" height="480" controls><source src="{video_url}" type="video/mp4">Your browser does not support the video tag.</video>', unsafe_allow_html=True)
                st.markdown(f'<iframe src="{video_url}" width="704" height="528" frameborder="0" allow="autoplay"; encrypted-media" allowfullscreen></iframe>', unsafe_allow_html=True)
                

                
                #st.video(video_url)
                #
            else:
                st.error(f"Video '{filename}' not found in the folder.")


        display_video(match_selection, half_selection, segment)
        
        # col1, col2 = st.columns(2)

        # with col1:
        st.button("Previous Clip", on_click=update_index, args=(-1,), disabled=(st.session_state.clip_index_t2 <= 0), key="prev_clip_button_t2")

        # with col2:
        st.button("Next Clip", on_click=update_index, args=(1,), disabled=(st.session_state.clip_index_t2 >= len(clip_titles) - 1), key="next_clip_button_t2")
         


if individual == 'Player':    
    tab1, tab2, tab3, tab4 = st.tabs(['Tackling', 'Heading', 'Progressive Passing','Changing Point of Attack'])
