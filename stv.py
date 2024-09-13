import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsbombpy import sb
import plotly.express as px
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events
print('')
print('new run')
print('')
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
    page_title="LouCity Video",
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
# div[data-testid="stVerticalBlock"] {{
#     gap: 0rem;
# }}
# div[data-testid="stHorizontalBlock"] {{
#         gap: 0rem;
#         margin-bottom: 0rem;
#     }}
st.markdown(custom_css, unsafe_allow_html=True)
def show_video(video_url):
    st.session_state.video_url = video_url
    st.session_state.show_video = True
def close_video():
    st.session_state.show_video = False
    st.session_state.video_url = ""
if 'show_video' not in st.session_state:
    st.session_state.show_video = True
    st.session_state.video_url = ""



# st.logo("https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Louisville_City_FC_2020_logo_primary.svg/160px-Louisville_City_FC_2020_logo_primary.svg.png")

selected_team = 'Louisville City'
league = 'USL'
men_matches = [
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

men_match_ids = [3930232, 3930247, 3930255, 3930266, 3930274, 3930288, 3930307,
            3930327, 3930340, 3930351, 3930354, 3930357, 3930369, 3930382,
            3930392, 3930399, 3930412, 3930424, 3930444, 3930456, 3930475,
            3930487, 3930499, 3930506, 3930524, 3930527]

women_matches = [
    '3/16 vs Orlando',
    '3/23 @ Houston',
    '3/30 @ Portland',
    '4/13 vs San Diego',
    '4/20 vs Utah',
    '4/28 @ Gotham',
    '5/5 @ Orlando',
    '5/10 vs Washington',
    '5/18 vs Kansas City',
    '5/25 @ Chicago',
    '6/7 vs Houston',
    '6/15 vs Gotham',
    '6/19 @ Angel City',
    '6/23 @ Seattle',
    '6/29 vs Bay',
    '6/7 @ North Carolina',
    '8/24 vs Chicago',
    '8/31 vs Seattle',
    '9/7 @ Bay'
]
women_match_ids = [3931339, 3931349, 3931357, 3931362, 3931368, 3931379,
                    3931388, 3931393, 3931403, 3931413, 3931414, 3931422, 3931429, 3931435,
                    3931439, 3931449, 3931455, 3931460, 3931467]



import plotly.graph_objects as go

def create_pitch(fw = 600, fh = 400):
    """
    Creates a soccer pitch figure using Plotly.
    
    Parameters:
    pitch_length (int): Length of the pitch in meters.
    pitch_width (int): Width of the pitch in meters.
    
    Returns:
    fig (go.Figure): A Plotly figure object representing the soccer pitch.
    """
    # Create a figure
    fig = go.Figure()
    pitch_length=120
    pitch_width=80

    # Add the pitch outline (four lines)
    fig.add_shape(type="rect", x0=0, y0=0, x1=pitch_length, y1=pitch_width, line=dict(color="white"))

    # Halfway line
    fig.add_shape(type="line", x0=pitch_length/2, y0=0, x1=pitch_length/2, y1=pitch_width, line=dict(color="white"))

    # Penalty areas
    fig.add_shape(type="rect", x0=0, y0=pitch_width/2 - 18, x1=18, y1=pitch_width/2 + 18, line=dict(color="white"))
    fig.add_shape(type="rect", x0=pitch_length - 18, y0=pitch_width/2 - 18, x1=pitch_length, y1=pitch_width/2 + 18, line=dict(color="white"))

    # 6-yard boxes
    fig.add_shape(type="rect", x0=0, y0=pitch_width/2 - 6, x1=6, y1=pitch_width/2 + 6, line=dict(color="white"))
    fig.add_shape(type="rect", x0=pitch_length - 6, y0=pitch_width/2 - 6, x1=pitch_length, y1=pitch_width/2 + 6, line=dict(color="white"))

    # Circles for center and penalty spots
    fig.add_shape(type="circle", x0=pitch_length/2 - 10, y0=pitch_width/2 - 10, x1=pitch_length/2 + 10, y1=pitch_width/2 + 10, line=dict(color="white"))
    fig.add_shape(type="circle", x0=pitch_length/2 - 0.5, y0=pitch_width/2 - 0.5, x1=pitch_length/2 + 0.5, y1=pitch_width/2 + 0.5, fillcolor="white", line=dict(color="white"))

    # Left and Right penalty spots
    fig.add_shape(type="circle", x0=12 - 0.3, y0=pitch_width/2 - 0.3, x1=12 + 0.3, y1=pitch_width/2 + 0.3, fillcolor="white", line=dict(color="white"))
    fig.add_shape(type="circle", x0=pitch_length - 12 - 0.3, y0=pitch_width/2 - 0.3, x1=pitch_length - 12 + 0.3, y1=pitch_width/2 + 0.3, fillcolor="white", line=dict(color="white"))

    # Penalty arcs (left and right)
    fig.add_shape(type="path", path=f"M 18 {pitch_width/2 + 10} Q 24 {pitch_width/2} 18 {pitch_width/2 - 10}", line=dict(color="white"))
    fig.add_shape(type="path", path=f"M {pitch_length - 18} {pitch_width/2 + 10} Q {pitch_length - 24} {pitch_width/2} {pitch_length - 18} {pitch_width/2 - 10}", line=dict(color="white"))

    # Set the background color of the pitch and configure axes
    fig.update_layout(
        plot_bgcolor="black",
        paper_bgcolor="black",
        xaxis=dict(range=[0, pitch_length], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[pitch_width, 0], showgrid=False, zeroline=False, visible=False),
        margin=dict(t=30, b=30, l=30, r=30),
        autosize=False,
        width=fw,
        height=fh
    )

    return fig


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
    selected_team = st.radio('Select Team', ['LouCity', 'Racing'])
    if selected_team == 'LouCity':
        selected_team = 'Louisville City'
        matches = men_matches
        match_ids = men_match_ids
        st.logo("https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Louisville_City_FC_2020_logo_primary.svg/160px-Louisville_City_FC_2020_logo_primary.svg.png")
        league = 'USL'

    if selected_team == 'Racing':
        selected_team = 'Racing Louisville FC'
        matches = women_matches
        match_ids = women_match_ids
        st.logo("https://upload.wikimedia.org/wikipedia/en/thumb/3/37/Racing_Louisville_FC_logo.svg/1024px-Racing_Louisville_FC_logo.svg.png")
        league = 'NWSL'


    #team = st.selectbox('Select Team', ['Louisville City'])
    #individual = st.radio('Team or Player Analyis?', ['Team', 'Player'])
    individual = st.radio('Team or Player Analyis?', ['Team'])
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
                '% -> Att. Third',

                'Vertical Sequences',
                '% of Passes Forward',
                'Avg Sequence Speed',
                'Box Entries from Vertical Sequences',
                'xG from Vertical Sequences',
                'Goals from Vertical Sequences',

                'Switches',
                'Switch Accuracy',
                'Switches Leading to Shots',

                'Crosses Completed',
                'Cross Accuracy',
                'Crosses Leading to Shots',
                'Crosses Leading to Goals',
                'Deep Crosses',
                'Deep Crosses Leading to Shots']
    
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
    team_rankings['Buildout Score'] = round(team_rankings['Goal Kick Buildouts'],1)

    team_rankings['Verticality'] = (0.4 * team_rankings['pctVertical Sequences']) + (0.15 * team_rankings['pctxG from Vertical Sequences']) + (0.1 * team_rankings['pctBox Entries from Vertical Sequences']) + (0.25 * team_rankings['pct% of Passes Forward']) + (0.1 * team_rankings['pctAvg Sequence Speed'])
    team_rankings['Verticality Score'] = round(team_rankings['Verticality'],1)

    team_rankings['Changing Point of Attack'] = (0.65 * team_rankings['pctSwitches']) + (0.1 * team_rankings['pctSwitch Accuracy']) + (0.25 * team_rankings['pctSwitches Leading to Shots'])
    team_rankings['Switch Score'] = round(team_rankings['Changing Point of Attack'],1)

    team_rankings['Crossing'] = (0.35 * team_rankings['pctCrosses Completed']) + (0.1 * team_rankings['pctCross Accuracy']) + (0.4 * team_rankings['pctCrosses Leading to Shots']) + (0.15 * team_rankings['pctCrosses Leading to Goals'])
    team_rankings['Cross Score'] = round(team_rankings['Crossing'],1)










    #print(selected_ids)
    if individual == 'Team' and len(selected_ids) > 0:
        print(team_rankings['Team'].unique())
        pct1 = team_rankings[team_rankings['Team'] == selected_team]['Pressing Rating'].values[0]
        
        pct2 = team_rankings[team_rankings['Team'] == selected_team]['Buildout Score'].values[0]
        pct3 = team_rankings[team_rankings['Team'] == selected_team]['Verticality Score'].values[0]
        pct4 = team_rankings[team_rankings['Team'] == selected_team]['Switch Score'].values[0] 
        pct5 = team_rankings[team_rankings['Team'] == selected_team]['Cross Score'].values[0] 
        custom_progress_bar(int(round(pct1,0)), "Pressing")
        custom_progress_bar(int(round(pct2,0)), "Goal Kick Buildouts")
        custom_progress_bar(int(round(pct3,0)), "Verticality")
        custom_progress_bar(int(round(pct4,0)), "Changing Point of Attack")
        custom_progress_bar(int(round(pct5,0)), "Crossing")

   


    if 'selected_points_t2' not in st.session_state:
        st.session_state.selected_points_t2 = False

    if 'selected_points_t3' not in st.session_state:
        st.session_state.selected_points_t3 = False

    if 'selected_points_t4' not in st.session_state:
        st.session_state.selected_points_t4 = False 

    if 'selected_points_t5' not in st.session_state:
        st.session_state.selected_points_t5 = False 

    n1 = 0
    n2 = 0

    print(n1,n2)

   

    # if st.button("Close Video"):
    #     print('stoppp')
    #     st.session_state.selected_points = False
    #     st.session_state.show_video = False
    #     #st.session_state.video_url = ""
    closed = st.button("Close Video")

    if closed:
        #st.session_state.selected_points = False
        st.session_state.show_video = False
        n2 += 1
            


     
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

    # if 'active_tab' not in st.session_state:
    #     st.session_state.active_tab = "Verticality"

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
        #print(metrics)
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
                'yaxis': {
                    'title': selected_metrics[0], 
                    'side': "left",
                    'titlefont': {'color': 'white'}

                    },
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
                layout['yaxis2'] = {
                    'title': selected_metrics[1], 
                    'side': "right", 
                    'overlaying': "y",
                    'titlefont': {'color': 'purple'}
                }
            
            if selected_metrics[0] in neg_cols:
                layout['yaxis']['autorange'] = 'reversed'
            if len(selected_metrics) == 2 and selected_metrics[1] in neg_cols:
                layout['yaxis2']['autorange'] = 'reversed'

            fig.update_layout(layout)

            #print(st.session_state.selected_metrics_t1)

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
                'El Paso Locomotive': 'El Paso',
                'Orlando Pride': 'Orlando',
                'Washington Spirit': 'Washington',
                'NJ/NY Gotham FC': 'Gotham',
                'North Carolina Courage': 'NC Courage',
                'Portland Thorns': 'Portland',
                'Chicago Red Stars': 'Chicago',
                'Seattle Reign': 'Seattle',
                'San Diego Wave': 'San Diego',
                'Houston Dash': 'Houston',
                'Utah Royals': 'Utah'
                
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

            mins = pd.read_parquet(f"{league}TeamMinutesPerGame.parquet")
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
                elif x == 'Savannah Marie DeMelo': return 'S. DeMelo'
                elif x == 'Elexa Marie Bahr Gutiérrez': return 'E. Bahr'
                elif x == 'Reilyn Turner': return 'R. Turner'
                elif x == 'Elli Pikkujämsä': return 'E. Pikkujämsä'
                elif x == 'Katie Lund': return 'K. Lund'
                elif x == 'Taylor Flint': return 'T. Flint'
                elif x == 'Uchenna Kanu': return 'U. Kanu'
                elif x == 'Carson Pickett': return 'Carson Pickett'
                elif x == 'Jordan Elisabeth Baggett': return 'J.Baggett'
                elif x == 'Lauren Milliet': return 'L. Milliet'
                elif x == 'Abby Erceg': return 'A. Erceg'
                elif x == 'Emma Sears': return 'E. Sears'
                elif x == 'Jaelin Marie Howell': return 'J. Howell'
                elif x == 'Kayla Fischer': return 'K. Fischer'
                elif x == 'Linda Maserame Motlhalo': return 'L. Motlhalo'
                elif x == 'Parker Goins': return 'P. Goins'
                elif x == 'Arin Wright': return 'A. Wright'
                elif x == 'Maddie Ann Pokorny': return 'M. Pokorny'
                elif x == 'Marisa Marie DiGrande': return 'M. DiGrande'
                elif x == 'Ellie Charlotte Jean': return 'E. ean'
                elif x == 'Ariadina Alves Borges': return 'A. Borges'
                elif x == 'Bethany Balcer': return 'B. Balcer'
                elif x == 'Janine Elizabeth Beckie': return 'J. Beckie'
                elif x == 'Courtney Petersen': return 'C. Petersen'

                
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
        
        if metric == 'Attacking Half Regains': data = pd.read_parquet(f"{league}att_half_regains_video_events.parquet")
        elif metric == 'Box Entries after Regains': data = pd.read_parquet(f"{league}regains_to_box_entry_video_events.parquet")
        elif metric == 'Shots after Press Regains': data = pd.read_parquet(f"{league}press_to_shot_video_events.parquet")
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
        def update_index_t1(step):
            new_index = st.session_state.clip_index_t1 + step
            if 0 <= new_index < len(clip_titles_t1):
                st.session_state.clip_index_t1 = new_index
                # print("")
                # print("")
                # print("")

                # print(st.session_state.clip_index_t1)
                # print(st.session_state.clip_selector_t1)

                st.session_state.clip_selector_t1 = clip_titles_t1[new_index]

        sorted_data_t1 = data.sort_values(by=['match_id', 'period', 'timestamp'], ascending=[False, True, True])
        clip_titles_t1 = sorted_data_t1['title'].tolist()

        
        with col2:
            #selection = st.selectbox('Choose Clip', data.sort_values(by=['match_id', 'period', 'timestamp'], ascending=[False,True,True])['title'])
            # sorted_data_t1 = data.sort_values(by=['match_id', 'period', 'timestamp'], ascending=[False, True, True])
            # clip_titles_t1 = sorted_data_t1['title'].tolist()


            #selection = st.selectbox('Choose Clip', clip_titles_t1, index=st.session_state.clip_index)
            #print("index", st.session_state.clip_index_t1)
            #print(len(clip_titles_t1))
            selection = st.selectbox('Choose Clip', clip_titles_t1, index=st.session_state.clip_index_t1, key='clip_selector_t1')
            if selection != clip_titles_t1[st.session_state.clip_index_t1]:
                st.session_state.clip_index_t1 = clip_titles_t1.index(selection)

            
 


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
        #print(time_str)
        segment, time_within_segment = find_closest_segment_with_times(time_str)


        csv_file_path = 'drive_files.csv'
        files_df = pd.read_csv(csv_file_path)

        def display_video(match_selection, half_selection, segment):
            
            filename = f"{match_selection}-h{half_selection}-{segment}.mp4"
            #print(filename)
            file_id = files_df.loc[files_df['File Name'] == filename]['File ID'].values[0]
            # files = list_files_in_folder(FOLDER_ID)
            # file_id = get_file_id(filename, files)
            
            if file_id:
                #video_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                #video_url = f"https://drive.google.com/file/d/{file_id}/view"
                video_url = f"https://drive.google.com/file/d/{file_id}/preview?t={time_within_segment}"


                #print(f"{filename} -> Video URL: {video_url}")  # Debug print statement
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
        st.button("Previous Clip", on_click=update_index_t1, args=(-1,), disabled=(st.session_state.clip_index_t1 <= 0), key="prev_clip_button_t1")

        # with col2:
        st.button("Next Clip", on_click=update_index_t1, args=(1,), disabled=(st.session_state.clip_index_t1 >= len(clip_titles_t1) - 1), key="next_clip_button_t1")

        # # Force rerun if the index has changed
        # if st.session_state.clip_index != clip_titles_t1.index(selection):
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
        with col2: custom_progress_bar(int(pct2), f"Passes per Sequence   ({round(team_rankings[team_rankings['Team'] == selected_team]['Passes per Sequence'].values[0],1)})")
        with col3: custom_progress_bar(int(pct3), f"Avg. Buildup Speed   ({round(team_rankings[team_rankings['Team'] == selected_team]['Avg. Buildup Speed'].values[0],1)} m/s)")
        
        with col1: custom_progress_bar(int(pct4), f"Avg. Distance Reached   ({int(round(team_rankings[team_rankings['Team'] == selected_team]['Avg. Distance Reached'].values[0],1))}m)")
        with col2: custom_progress_bar(int(pct5), f"% -> Att. Half   ({int(round(team_rankings[team_rankings['Team'] == selected_team]['% -> Att. Half'].values[0],1))}%)")
        with col3: custom_progress_bar(int(pct6), f"% -> Att. Third   ({int(round(team_rankings[team_rankings['Team'] == selected_team]['% -> Att. Third'].values[0],1))}%)")

        
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
        #print(metrics)
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
                layout['yaxis2'] = {
                    'title': selected_metrics[1], 
                    'side': "right", 
                    'overlaying': "y",
                    'titlefont': {'color': 'purple'}
                }
            
            if selected_metrics[0] in neg_cols:
                layout['yaxis']['autorange'] = 'reversed'
            if len(selected_metrics) == 2 and selected_metrics[1] in neg_cols:
                layout['yaxis2']['autorange'] = 'reversed'

            fig.update_layout(layout)

            #print(st.session_state.selected_metrics_t2)

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








        col1, col2 = st.columns([0.9, 2])#st.columns(2)
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
                team_rankings2['Buildout Score'] = round(team_rankings2['Goal Kick Buildouts'],1)




                team_rankings2 = team_rankings2[team_rankings2['Team'] != selected_team]
                team_rankings = team_rankings[team_rankings['Team'] == selected_team]
                
                team_rankings = pd.concat([team_rankings, team_rankings2], ignore_index=True)

                #print(team_rankings[team_rankings['Team'] == selected_team]['Pressing Rating'].values[0])

                
                            


            for col in orig_cols:
                team_rankings[col] = round(team_rankings[col],2)
                shortened_gk_data = team_rankings.sort_values(by = 'Buildout Score', ascending=False)
                #shortened_gk_data = shortened_gk_data[['Team','Matches', 'Buildout Score', '% of Goal Kicks Short', 'Passes per Sequence', 'Avg. Buildup Speed', 'Avg. Distance Reached','% -> Att. Half', '% -> Att. Third']]
                shortened_gk_data = shortened_gk_data[['Team','Buildout Score','Matches',  '% of Goal Kicks Short', 'Passes per Sequence', 'Avg. Buildup Speed', 'Avg. Distance Reached','% -> Att. Half', '% -> Att. Third']]
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
                'El Paso Locomotive': 'El Paso',
                'Orlando Pride': 'Orlando',
                'Washington Spirit': 'Washington',
                'NJ/NY Gotham FC': 'Gotham',
                'North Carolina Courage': 'NC Courage',
                'Portland Thorns': 'Portland',
                'Chicago Red Stars': 'Chicago',
                'Seattle Reign': 'Seattle',
                'San Diego Wave': 'San Diego',
                'Houston Dash': 'Houston',
                'Utah Royals': 'Utah'
                
            })
            shortened_gk_data.set_index('Team', inplace=True)

            #st.dataframe(shortened_pressing_data, use_container_width=True, height = 280)
            st.dataframe(shortened_gk_data, height = 280)

            
        with col2:
            
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
            #             half=False, pad_top=2, corner_arcs=True)

            # fig,ax = pitch.draw(figsize=(6,8))
            # fig.set_facecolor('black')

            # gk_events = pd.read_parquet(f"{league}VideoGoalKickEvents.parquet")

            # gk_events = gk_events[gk_events['match_id'].isin(selected_ids)]

            # for _, row in gk_events.iterrows():
            #     x = row['gk_end_x']
            #     y = row['gk_end_y']
            #     pitch.scatter(x,y, ax = ax, color = 'white', s = 20)
                
              
            # ax.text(60, -5,'End Location of Short Goal Kick Buildouts', color = 'white', ha = 'center', fontsize = 12.5)
            # ax.text(60, -2,'Direction of Attack --->', color = 'white', ha = 'center', fontsize = 10)

            # buf = io.BytesIO()
            # plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
            # buf.seek(0)

            # # Display the image
            # st.image(buf, use_column_width=True)
            st.session_state.old_selected_points_t2 = st.session_state.selected_points_t2
            fig = create_pitch(480,320)
            #fig = create_pitch(600,400) 
            
            # Load Goal Kick Event Data
            # Replace this with your parquet file, and make sure you have your dataframe loaded.
            gk_events = pd.read_parquet(f"{league}VideoGoalKickEvents.parquet")

            # Filter based on selected match ids
            gk_events = gk_events[gk_events['match_id'].isin(selected_ids)]

            customdata = gk_events['title']

        
            # Plot the goal kick events
            fig.add_trace(go.Scatter(
                x=gk_events['gk_end_x'],
                y=gk_events['gk_end_y'],
                mode='markers',
                marker=dict(color='purple', size=5),
                name="Switch End",
                hoverinfo="text",
                #text=switch_events['title'].astype(str)# + ", " + gk_events['gk_end_y'].astype(str)
                hovertemplate="<b>%{customdata}</b><extra></extra>",
                customdata=customdata,
                hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial"),
            ))

            fig.update_layout(
                hoverdistance=10,  # Increase hover area
                hovermode="closest",
                showlegend=False
            )

            
            


            # Add title and direction of attack
            fig.add_annotation(text="End Location of Short Goal Kick Buildouts", xref="paper", yref="paper",
                            x=0.5, y=1.05, showarrow=False, font=dict(color="white", size=14), align="center")
            fig.add_annotation(text="Direction of Attack --->", xref="paper", yref="paper",
                            x=0.5, y=-0.05, showarrow=False, font=dict(color="white", size=12), align="center")

            # Display in Streamlit
            #st.plotly_chart(fig)
            #overlay_container = st.empty()

            show_mode = st.session_state.show_video
            
            
            selected_points_t2 = True
            selected_points_t2 = plotly_events(fig, click_event=True)
            
            # if st.session_state.show_video == False and selected_points_t2:
            
            # if st.session_state.selected_points_t2




            

            print(f"old: {st.session_state.old_selected_points_t2}")
            #if st.session_state.show_video and selected_points_t2:
            if st.session_state.old_selected_points_t2 != selected_points_t2:
            #if selected_points_t2:
                
                #st.session_state.show_video = True
                if len(selected_points_t2) > 0:
                    clicked_point = selected_points_t2[0]  # If multiple points, handle accordingly
                    clicked_index = clicked_point['pointIndex']
                    clicked_event = gk_events.iloc[clicked_index]
                
                    filename = clicked_event['filename']
                    start_time = clicked_event['start_time']
                    file_id = files_df.loc[files_df['File Name'] == filename]['File ID'].values[0]
                    # Extract video info (filename and start_time)
                    video_url = f"https://drive.google.com/file/d/{file_id}/preview?t={start_time}"
                    if st.session_state.show_video or selected_points_t2:
                        st.markdown(f'''
                        <div id="video-popup" style="position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.8); display:flex; align-items:center; justify-content:center; z-index:999;">
                            <div style="position:relative; width:60%; max-width:800px; height:60%; max-height:450px;">
                                <iframe src="{video_url}" width="100%" height="100%" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)

                        st.session_state.selected_points_t2 = selected_points_t2


        #dual_progress_bars(60, "Progress 1", 85, "Progress 2")

        col1, col2 = st.columns(2)
        with col1: 
            metric = st.selectbox(
            'Select Metric',
            ['Short Goal Kick Buildouts', 'Own Half Turnovers', 'To Final Third', 'Long Goal Kicks']
            )
        
        if metric == 'Short Goal Kick Buildouts': data = pd.read_parquet(f"{league}gk_short_buildups_video_events.parquet")
        elif metric == 'Own Half Turnovers': data = pd.read_parquet(f"{league}gk_short_buildups_h1_turnover_video_events.parquet")
        elif metric == 'To Final Third': data = pd.read_parquet(f"{league}gk_short_buildups_to_final_third_video_events.parquet")
        elif metric == 'Long Goal Kicks': data = pd.read_parquet(f"{league}gk_long_buildups_video_events.parquet")
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
        def update_index_t2(step):
            new_index = st.session_state.clip_index_t2 + step
            if 0 <= new_index < len(clip_titles_t2):
                st.session_state.clip_index_t2 = new_index
                st.session_state.clip_selector_t2 = clip_titles_t2[new_index]

        sorted_data_t2 = data.sort_values(by=['match_id', 'period', 'timestamp'], ascending=[False, True, True])
        clip_titles_t2 = sorted_data_t2['title'].tolist()

        
        with col2:
            #selection = st.selectbox('Choose Clip', data.sort_values(by=['match_id', 'period', 'timestamp'], ascending=[False,True,True])['title'])
            # sorted_data = data.sort_values(by=['match_id', 'period', 'timestamp'], ascending=[False, True, True])
            # clip_titles_t2 = sorted_data['title'].tolist()


            #selection = st.selectbox('Choose Clip', clip_titles_t2, index=st.session_state.clip_index)
            # print("index", st.session_state.clip_index_t2)
            # print(len(clip_titles_t2))
            selection = st.selectbox('Choose Clip', clip_titles_t2, index=st.session_state.clip_index_t2, key='clip_selector_t2')
            print("")
            print(len(clip_titles_t2))
            print(st.session_state.clip_index_t2)
            print("")
            if len(clip_titles_t2) > 0:
                if selection != clip_titles_t2[st.session_state.clip_index_t2]:
                    st.session_state.clip_index_t2 = clip_titles_t2.index(selection)

            
 

        if len(clip_titles_t2) > 0:
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
            #print(time_str)
            segment, time_within_segment = find_closest_segment_with_times(time_str)
    

            csv_file_path = 'drive_files.csv'
            files_df = pd.read_csv(csv_file_path)

            def display_video(match_selection, half_selection, segment):
                
                filename = f"{match_selection}-h{half_selection}-{segment}.mp4"
                #(filename)
                file_id = files_df.loc[files_df['File Name'] == filename]['File ID'].values[0]
                # files = list_files_in_folder(FOLDER_ID)
                # file_id = get_file_id(filename, files)
                
                if file_id:
                    #video_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                    #video_url = f"https://drive.google.com/file/d/{file_id}/view"
                    video_url = f"https://drive.google.com/file/d/{file_id}/preview?t={time_within_segment}"


                    #print(f"{filename} -> Video URL: {video_url}")  # Debug print statement
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
            st.button("Previous Clip", on_click=update_index_t2, args=(-1,), disabled=(st.session_state.clip_index_t2 <= 0), key="prev_clip_button_t2")

            # with col2:
            st.button("Next Clip", on_click=update_index_t2, args=(1,), disabled=(st.session_state.clip_index_t2 >= len(clip_titles_t2) - 1), key="next_clip_button_t2")
            
        

        # st.session_state.old_selected_points = st.session_state.selected_points
        # fig = create_pitch()
        # # Load Goal Kick Event Data
        # # Replace this with your parquet file, and make sure you have your dataframe loaded.
        # gk_events = pd.read_parquet(f"{league}VideoGoalKickEvents.parquet")

        # # Filter based on selected match ids
        # gk_events = gk_events[gk_events['match_id'].isin(selected_ids)]

    
        # # Plot the goal kick events
        # fig.add_trace(go.Scatter(
        #     x=gk_events['gk_end_x'],
        #     y=gk_events['gk_end_y'],
        #     mode='markers',
        #     marker=dict(color='white', size=8),
        #     name="Goal Kick End",
        #     hoverinfo="text",
        #     text=gk_events['title'].astype(str) + " -> " + gk_events['gk_end_player'].astype(str)# + ", " + gk_events['gk_end_y'].astype(str)
        # ))
        
        


        # # Add title and direction of attack
        # fig.add_annotation(text="End Location of Short Goal Kick Buildouts", xref="paper", yref="paper",
        #                 x=0.5, y=1.05, showarrow=False, font=dict(color="white", size=14), align="center")
        # fig.add_annotation(text="Direction of Attack --->", xref="paper", yref="paper",
        #                 x=0.5, y=-0.05, showarrow=False, font=dict(color="white", size=12), align="center")

        # # Display in Streamlit
        # #st.plotly_chart(fig)
        # #overlay_container = st.empty()

        # show_mode = st.session_state.show_video
        
        
        # selected_points = True
        # selected_points = plotly_events(fig, click_event=True)
        
        # # if st.session_state.show_video == False and selected_points:
        
        # # if st.session_state.selected_points

 


        

        # print(f"old: {st.session_state.old_selected_points}")
        # #if st.session_state.show_video and selected_points:
        # if st.session_state.old_selected_points != selected_points:
        # #if selected_points:
            
        #     #st.session_state.show_video = True
        #     if len(selected_points) > 0:
        #         clicked_point = selected_points[0]  # If multiple points, handle accordingly
        #         clicked_index = clicked_point['pointIndex']
        #         clicked_event = gk_events.iloc[clicked_index]
            
        #         filename = clicked_event['filename']
        #         start_time = clicked_event['start_time']
        #         file_id = files_df.loc[files_df['File Name'] == filename]['File ID'].values[0]
        #         # Extract video info (filename and start_time)
        #         video_url = f"https://drive.google.com/file/d/{file_id}/preview?t={start_time}"
        #         if st.session_state.show_video or selected_points:
        #             st.markdown(f'''
        #             <div id="video-popup" style="position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.8); display:flex; align-items:center; justify-content:center; z-index:999;">
        #                 <div style="position:relative; width:60%; max-width:800px; height:60%; max-height:450px;">
        #                     <iframe src="{video_url}" width="100%" height="100%" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
        #                 </div>
        #             </div>
        #             ''', unsafe_allow_html=True)

        #             st.session_state.selected_points = selected_points

    
    with tab3:
        
        pct1 = team_rankings[team_rankings['Team'] == selected_team]['pctVertical Sequences'].values[0]
        pct2 = team_rankings[team_rankings['Team'] == selected_team]['pct% of Passes Forward'].values[0]
        pct3 = team_rankings[team_rankings['Team'] == selected_team]['pctAvg Sequence Speed'].values[0]
        pct4 = team_rankings[team_rankings['Team'] == selected_team]['pctBox Entries from Vertical Sequences'].values[0]
        pct5 = team_rankings[team_rankings['Team'] == selected_team]['pctxG from Vertical Sequences'].values[0]
        pct6 = team_rankings[team_rankings['Team'] == selected_team]['pctGoals from Vertical Sequences'].values[0]


        
       
        col1, col2, col3 = st.columns(3)
        with col1: custom_progress_bar(int(pct1), f"Vertical Sequences   ({round(team_rankings[team_rankings['Team'] == selected_team]['Vertical Sequences'].values[0],1)})")
        with col2: custom_progress_bar(int(pct2), f"% of Passes Forward   ({int(round(team_rankings[team_rankings['Team'] == selected_team]['% of Passes Forward'].values[0],2) * 100)}%)")
        with col3: custom_progress_bar(int(pct3), f"Avg. Seq. Speed   ({round(team_rankings[team_rankings['Team'] == selected_team]['Avg Sequence Speed'].values[0],1)} m/s)")
        
        with col1: custom_progress_bar(int(pct4), f"Box Entries from Vert.   ({round(team_rankings[team_rankings['Team'] == selected_team]['Box Entries from Vertical Sequences'].values[0],1)})")
        with col2: custom_progress_bar(int(pct5), f"xG from Vert.   ({round(team_rankings[team_rankings['Team'] == selected_team]['xG from Vertical Sequences'].values[0],1)})")
        with col3: custom_progress_bar(int(pct6), f"Goals from Vert.   ({round(team_rankings[team_rankings['Team'] == selected_team]['Goals from Vertical Sequences'].values[0],1)})")

        
        st.write("")
        
        selected_metrics = ['Avg. Distance Reached', 'Avg. Buildup Speed']
        #df = pd.DataFrame(data) 
        df = full_team_data.sort_values(by='match_id')

        #metrics = orig_cols#[col for col in df.columns if col != 'Match']
        metrics = ['Vertical Sequences',
                   '% of Passes Forward',
                    'Avg Sequence Speed',
                    'Box Entries from Vertical Sequences',
                    'xG from Vertical Sequences',
                    'Goals from Vertical Sequences']
        #print(metrics)
        if 'selected_metrics_t3' not in st.session_state:
            #st.session_state.selected_metrics = metrics[:2]  # Default to first two metrics
            st.session_state.selected_metrics_t3 = ['Vertical Sequences', 'xG from Vertical Sequences']
        

        

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
                layout['yaxis2'] = {
                    'title': selected_metrics[1], 
                    'side': "right", 
                    'overlaying': "y",
                    'titlefont': {'color': 'purple'}
                }
            
            if selected_metrics[0] in neg_cols:
                layout['yaxis']['autorange'] = 'reversed'
            if len(selected_metrics) == 2 and selected_metrics[1] in neg_cols:
                layout['yaxis2']['autorange'] = 'reversed'

            fig.update_layout(layout)

            #print(st.session_state.selected_metrics_t2)

            return fig

        # Create columns for metrics selection
        cols = st.columns(len(metrics))

        for i, metric in enumerate(metrics):
            with cols[i]:
                if st.checkbox(metric, value=(metric in st.session_state.selected_metrics_t3)):
                    if metric not in st.session_state.selected_metrics_t3:
                        st.session_state.selected_metrics_t3.append(metric)
                else:
                    if metric in st.session_state.selected_metrics_t3:
                        st.session_state.selected_metrics_t3.remove(metric)

        # Enforce the restriction of selecting only 1 or 2 metrics
        if len(st.session_state.selected_metrics_t3) < 1 or len(st.session_state.selected_metrics_t3) > 2:
            st.error("Please select exactly 1 or 2 metrics.")
        else:
            # Create and display the plot
            fig = update_chart(st.session_state.selected_metrics_t3)
            st.plotly_chart(fig)








        col1, col2 = st.columns([0.9, 2])#st.columns(2)
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

                
                                
                
                # team_rankings2['Pressing'] = ((0.2 * team_rankings2['pctPPDA']) + (0.25 * team_rankings2['pctAvg. Defensive Distance']) + (0.2 * team_rankings2['pctAtt. Third Pressures']) + (0.25 * team_rankings2['pctAtt. Half Regains']) + (0.1 * team_rankings2['pctShots after Pressure Regains']))
                # #team_rankings['Pressing'] = round(team_rankings['Pressing'].rank(pct=True) * 100,2)
                # team_rankings2['Pressing Rating'] = round(team_rankings2['Pressing'],1)

                # team_rankings2['Goal Kick Buildouts'] = ((0.3 * team_rankings2['pctAvg. Distance Reached']) + (0.15 * team_rankings2['pctAvg. Buildup Speed']) + (0.4 * team_rankings2['pct% -> Att. Half']) + (0.15 * team_rankings2['pctPasses per Sequence']))
                # #team_rankings['pctShort GK Buildups'] = round(team_rankings['Short GK Buildups'].rank(pct=True) * 100,2)
                # team_rankings2['Buildout Score'] = round(team_rankings2['Goal Kick Buildouts'],1)

                team_rankings2['Verticality'] = (0.4 * team_rankings2['pctVertical Sequences']) + (0.15 * team_rankings2['pctxG from Vertical Sequences']) + (0.1 * team_rankings2['pctBox Entries from Vertical Sequences']) + (0.25 * team_rankings2['pct% of Passes Forward']) + (0.1 * team_rankings2['pctAvg Sequence Speed'])
                team_rankings2['Verticality Score'] = round(team_rankings2['Verticality'],1)




                team_rankings2 = team_rankings2[team_rankings2['Team'] != selected_team]
                team_rankings = team_rankings[team_rankings['Team'] == selected_team]
                
                team_rankings = pd.concat([team_rankings, team_rankings2], ignore_index=True)

                #print(team_rankings[team_rankings['Team'] == selected_team]['Pressing Rating'].values[0])

                
                            


            for col in orig_cols:
                team_rankings[col] = round(team_rankings[col],2)
                shortened_vert_data = team_rankings.sort_values(by = 'Verticality Score', ascending=False)
                #shortened_gk_data = shortened_gk_data[['Team','Matches', 'Buildout Score', '% of Goal Kicks Short', 'Passes per Sequence', 'Avg. Buildup Speed', 'Avg. Distance Reached','% -> Att. Half', '% -> Att. Third']]
                shortened_vert_data = shortened_vert_data[['Team','Verticality Score','Matches',  'Vertical Sequences', '% of Passes Forward', 'Avg Sequence Speed', 'Box Entries from Vertical Sequences','xG from Vertical Sequences', 'Goals from Vertical Sequences']]
                #st.write(shortened_pressing_data)

            shortened_vert_data['Team'] = shortened_vert_data['Team'].replace({
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
                'El Paso Locomotive': 'El Paso',
                'Orlando Pride': 'Orlando',
                'Washington Spirit': 'Washington',
                'NJ/NY Gotham FC': 'Gotham',
                'North Carolina Courage': 'NC Courage',
                'Portland Thorns': 'Portland',
                'Chicago Red Stars': 'Chicago',
                'Seattle Reign': 'Seattle',
                'San Diego Wave': 'San Diego',
                'Houston Dash': 'Houston',
                'Utah Royals': 'Utah'
                
            })
            shortened_vert_data.set_index('Team', inplace=True)

            #st.dataframe(shortened_pressing_data, use_container_width=True, height = 280)
            st.dataframe(shortened_vert_data, height = 280)

            
        with col2:
            
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
            #             half=False, pad_top=2, corner_arcs=True)

            # fig,ax = pitch.draw(figsize=(6,8))
            # fig.set_facecolor('black')

            # gk_events = pd.read_parquet(f"{league}VideoGoalKickEvents.parquet")

            # gk_events = gk_events[gk_events['match_id'].isin(selected_ids)]

            # for _, row in gk_events.iterrows():
            #     x = row['gk_end_x']
            #     y = row['gk_end_y']
            #     pitch.scatter(x,y, ax = ax, color = 'white', s = 20)
                
              
            # ax.text(60, -5,'End Location of Short Goal Kick Buildouts', color = 'white', ha = 'center', fontsize = 12.5)
            # ax.text(60, -2,'Direction of Attack --->', color = 'white', ha = 'center', fontsize = 10)

            # buf = io.BytesIO()
            # plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
            # buf.seek(0)

            # # Display the image
            # st.image(buf, use_column_width=True)
            st.session_state.old_selected_points_t3 = st.session_state.selected_points_t3
            fig = create_pitch(480,320)
            #fig = create_pitch(600,400)
            
            # Load Goal Kick Event Data
            # Replace this with your parquet file, and make sure you have your dataframe loaded.
            vert_events = pd.read_parquet(f"{league}VideoVerticalityEvents.parquet")

            # Filter based on selected match ids
            vert_events = vert_events[vert_events['match_id'].isin(selected_ids)] 

            customdata = vert_events['title']



        
            # Plot the goal kick events
            fig.add_trace(go.Scatter(
                x= vert_events['vert_end_x'],
                y= vert_events['vert_end_y'],
                
                mode='markers',
                marker=dict(color='purple', size=5),
                name="Vert End",
                hoverinfo="text",
                #text=vert_events['title'].astype(str)# + ", " + gk_events['gk_end_y'].astype(str)
                hovertemplate="<b>%{customdata}</b><extra></extra>",
                customdata=customdata,
                hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial"),
            
            ))
            fig.update_layout(
                hoverdistance=10,  # Increase hover area
                hovermode="closest",
                showlegend=False
            )
            
            


            # Add title and direction of attack
            fig.add_annotation(text="End Location of Vertical Sequences", xref="paper", yref="paper",
                            x=0.5, y=1.05, showarrow=False, font=dict(color="white", size=14), align="center")
            fig.add_annotation(text="Direction of Attack --->", xref="paper", yref="paper",
                            x=0.5, y=-0.05, showarrow=False, font=dict(color="white", size=12), align="center")

            # Display in Streamlit
            #st.plotly_chart(fig)
            #overlay_container = st.empty()

            show_mode = st.session_state.show_video
            
            
            selected_points_t3 = True
            selected_points_t3 = plotly_events(fig, click_event=True)
            
            # if st.session_state.show_video == False and selected_points_t3:
            
            # if st.session_state.selected_points_t3




            

            print(f"old: {st.session_state.old_selected_points_t3}")
            #if st.session_state.show_video and selected_points_t3:
            if st.session_state.old_selected_points_t3 != selected_points_t3:
            #if selected_points_t3:
                
                #st.session_state.show_video = True
                if len(selected_points_t3) > 0:
                    clicked_point = selected_points_t3[0]  # If multiple points, handle accordingly
                    clicked_index = clicked_point['pointIndex']
                    clicked_event = vert_events.iloc[clicked_index]
                
                    filename = clicked_event['filename']
                    start_time = clicked_event['start_time']
                    file_id = files_df.loc[files_df['File Name'] == filename]['File ID'].values[0]
                    # Extract video info (filename and start_time)
                    video_url = f"https://drive.google.com/file/d/{file_id}/preview?t={start_time}"
                    if st.session_state.show_video or selected_points_t3:
                        st.markdown(f'''
                        <div id="video-popup" style="position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.8); display:flex; align-items:center; justify-content:center; z-index:999;">
                            <div style="position:relative; width:60%; max-width:800px; height:60%; max-height:450px;">
                                <iframe src="{video_url}" width="100%" height="100%" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)

                        st.session_state.selected_points_t3 = selected_points_t3


        #dual_progress_bars(60, "Progress 1", 85, "Progress 2")

        col1, col2 = st.columns(2)
        with col1: 
            metric = st.selectbox(
            'Select Metric',
            ['Vertical Sequences', 'Final Quarter Entries', 'Box Entries', 'Shots', 'Goals']
            )
        
        if metric == 'Vertical Sequences': data = pd.read_parquet(f"{league}VideoVerticalityEvents.parquet")
        elif metric == 'Final Quarter Entries': data = pd.read_parquet(f"{league}vert_final_quarter_entries_video_events.parquet")
        elif metric == 'Box Entries': data = pd.read_parquet(f"{league}vert_box_entries_video_events.parquet")
        elif metric == 'Shots': data = pd.read_parquet(f"{league}vert_shots_video_events.parquet")
        elif metric == 'Goals': data = pd.read_parquet(f"{league}vert_goals_video_events.parquet")
        data = data.drop_duplicates(subset = ['match_id', 'period']).reset_index()

        data = data[data['match_id'].isin(selected_ids)].reset_index()
        if len(data) == 0: 
            st.error("No events in selected matches")
        
        # with col2:
        #     sort_method = st.selectbox(
        #         'Sort By',
        #         ['Most Recent']
        #     )
        
        if 'clip_index_t3' not in st.session_state:
            st.session_state.clip_index_t3 = 0
        def update_index_t3(step):
            new_index = st.session_state.clip_index_t3 + step
            if 0 <= new_index < len(clip_titles_t3):
                st.session_state.clip_index_t3 = new_index
                st.session_state.clip_selector_t3 = clip_titles_t3[new_index]

        sorted_data_t3 = data.sort_values(by=['match_id', 'period', 'timestamp'], ascending=[False, True, True])
        clip_titles_t3 = sorted_data_t3['title'].tolist()

        
        with col2:
            #selection = st.selectbox('Choose Clip', data.sort_values(by=['match_id', 'period', 'timestamp'], ascending=[False,True,True])['title'])
            # sorted_data = data.sort_values(by=['match_id', 'period', 'timestamp'], ascending=[False, True, True])
            # clip_titles_t2 = sorted_data['title'].tolist()


            #selection = st.selectbox('Choose Clip', clip_titles_t2, index=st.session_state.clip_index)
            # print("index", st.session_state.clip_index_t2)
            # print(len(clip_titles_t2))
            selection = st.selectbox('Choose Clip', clip_titles_t3, index=st.session_state.clip_index_t3, key='clip_selector_t3')
            if selection != clip_titles_t3[st.session_state.clip_index_t3]:
                st.session_state.clip_index_t3 = clip_titles_t3.index(selection)

            
 


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
        #print(time_str)
        segment, time_within_segment = find_closest_segment_with_times(time_str)
 

        csv_file_path = 'drive_files.csv'
        files_df = pd.read_csv(csv_file_path)

        def display_video(match_selection, half_selection, segment):
            
            filename = f"{match_selection}-h{half_selection}-{segment}.mp4"
            #(filename)
            file_id = files_df.loc[files_df['File Name'] == filename]['File ID'].values[0]
            # files = list_files_in_folder(FOLDER_ID)
            # file_id = get_file_id(filename, files)
            
            if file_id:
                #video_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                #video_url = f"https://drive.google.com/file/d/{file_id}/view"
                video_url = f"https://drive.google.com/file/d/{file_id}/preview?t={time_within_segment}"


                #print(f"{filename} -> Video URL: {video_url}")  # Debug print statement
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
        st.button("Previous Clip", on_click=update_index_t3, args=(-1,), disabled=(st.session_state.clip_index_t3 <= 0), key="prev_clip_button_t3")

        # with col2:
        st.button("Next Clip", on_click=update_index_t3, args=(1,), disabled=(st.session_state.clip_index_t3 >= len(clip_titles_t3) - 1), key="next_clip_button_t3")
         
        

        # st.session_state.old_selected_points = st.session_state.selected_points
        # fig = create_pitch()
        # # Load Goal Kick Event Data
        # # Replace this with your parquet file, and make sure you have your dataframe loaded.
        # gk_events = pd.read_parquet(f"{league}VideoGoalKickEvents.parquet")

        # # Filter based on selected match ids
        # gk_events = gk_events[gk_events['match_id'].isin(selected_ids)]

    
        # # Plot the goal kick events
        # fig.add_trace(go.Scatter(
        #     x=gk_events['gk_end_x'],
        #     y=gk_events['gk_end_y'],
        #     mode='markers',
        #     marker=dict(color='white', size=8),
        #     name="Goal Kick End",
        #     hoverinfo="text",
        #     text=gk_events['title'].astype(str) + " -> " + gk_events['gk_end_player'].astype(str)# + ", " + gk_events['gk_end_y'].astype(str)
        # ))
        
        


        # # Add title and direction of attack
        # fig.add_annotation(text="End Location of Short Goal Kick Buildouts", xref="paper", yref="paper",
        #                 x=0.5, y=1.05, showarrow=False, font=dict(color="white", size=14), align="center")
        # fig.add_annotation(text="Direction of Attack --->", xref="paper", yref="paper",
        #                 x=0.5, y=-0.05, showarrow=False, font=dict(color="white", size=12), align="center")

        # # Display in Streamlit
        # #st.plotly_chart(fig)
        # #overlay_container = st.empty()

        # show_mode = st.session_state.show_video
        
        
        # selected_points = True
        # selected_points = plotly_events(fig, click_event=True)
        
        # # if st.session_state.show_video == False and selected_points:
        
        # # if st.session_state.selected_points




        

        # print(f"old: {st.session_state.old_selected_points}")
        # #if st.session_state.show_video and selected_points:
        # if st.session_state.old_selected_points != selected_points:
        # #if selected_points:
            
        #     #st.session_state.show_video = True
        #     if len(selected_points) > 0:
        #         clicked_point = selected_points[0]  # If multiple points, handle accordingly
        #         clicked_index = clicked_point['pointIndex']
        #         clicked_event = gk_events.iloc[clicked_index]
            
        #         filename = clicked_event['filename']
        #         start_time = clicked_event['start_time']
        #         file_id = files_df.loc[files_df['File Name'] == filename]['File ID'].values[0]
        #         # Extract video info (filename and start_time)
        #         video_url = f"https://drive.google.com/file/d/{file_id}/preview?t={start_time}"
        #         if st.session_state.show_video or selected_points:
        #             st.markdown(f'''
        #             <div id="video-popup" style="position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.8); display:flex; align-items:center; justify-content:center; z-index:999;">
        #                 <div style="position:relative; width:60%; max-width:800px; height:60%; max-height:450px;">
        #                     <iframe src="{video_url}" width="100%" height="100%" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
        #                 </div>
        #             </div>
        #             ''', unsafe_allow_html=True)

        #             st.session_state.selected_points = selected_points

    with tab4:
        
        pct1 = team_rankings[team_rankings['Team'] == selected_team]['pctSwitches'].values[0]
        pct2 = team_rankings[team_rankings['Team'] == selected_team]['pctSwitch Accuracy'].values[0]
        pct3 = team_rankings[team_rankings['Team'] == selected_team]['pctSwitches Leading to Shots'].values[0]
        
        
       
        col1, col2, col3 = st.columns(3)
        with col1: custom_progress_bar(int(pct1), f"Switches Completed   ({round(team_rankings[team_rankings['Team'] == selected_team]['Switches'].values[0],1)})")
        with col2: custom_progress_bar(int(pct2), f"Switch Accuracy   ({int(round(team_rankings[team_rankings['Team'] == selected_team]['Switch Accuracy'].values[0],2) * 100)}%)")
        with col3: custom_progress_bar(int(pct3), f"Switches to Shots   ({round(team_rankings[team_rankings['Team'] == selected_team]['Switches Leading to Shots'].values[0],1)})")
        
        
        
        st.write("")
        
        selected_metrics = ['Switches', 'Switches Leading to Shots']
        #df = pd.DataFrame(data) 
        df = full_team_data.sort_values(by='match_id')

        #metrics = orig_cols#[col for col in df.columns if col != 'Match']
        metrics = ['Switches',
                   'Switch Accuracy',
                    'Switches Leading to Shots'
                   ]
        #print(metrics)
        if 'selected_metrics_t4' not in st.session_state:
            #st.session_state.selected_metrics = metrics[:2]  # Default to first two metrics
            st.session_state.selected_metrics_t4 = ['Switches', 'Switches Leading to Shots']
        

        

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
                layout['yaxis2'] = {
                    'title': selected_metrics[1], 
                    'side': "right", 
                    'overlaying': "y",
                    'titlefont': {'color': 'purple'}
                }
            
            if selected_metrics[0] in neg_cols:
                layout['yaxis']['autorange'] = 'reversed'
            if len(selected_metrics) == 2 and selected_metrics[1] in neg_cols:
                layout['yaxis2']['autorange'] = 'reversed'

            fig.update_layout(layout)

            #print(st.session_state.selected_metrics_t2)

            return fig

        # Create columns for metrics selection
        cols = st.columns(len(metrics))

        for i, metric in enumerate(metrics):
            with cols[i]:
                if st.checkbox(metric, value=(metric in st.session_state.selected_metrics_t4)):
                    if metric not in st.session_state.selected_metrics_t4:
                        st.session_state.selected_metrics_t4.append(metric)
                else:
                    if metric in st.session_state.selected_metrics_t4:
                        st.session_state.selected_metrics_t4.remove(metric)

        # Enforce the restriction of selecting only 1 or 2 metrics
        if len(st.session_state.selected_metrics_t4) < 1 or len(st.session_state.selected_metrics_t4) > 2:
            st.error("Please select exactly 1 or 2 metrics.")
        else:
            # Create and display the plot
            fig = update_chart(st.session_state.selected_metrics_t4)
            st.plotly_chart(fig)








        col1, col2 = st.columns([0.9, 2])#st.columns(2)
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

                
                                
                
                # team_rankings2['Pressing'] = ((0.2 * team_rankings2['pctPPDA']) + (0.25 * team_rankings2['pctAvg. Defensive Distance']) + (0.2 * team_rankings2['pctAtt. Third Pressures']) + (0.25 * team_rankings2['pctAtt. Half Regains']) + (0.1 * team_rankings2['pctShots after Pressure Regains']))
                # #team_rankings['Pressing'] = round(team_rankings['Pressing'].rank(pct=True) * 100,2)
                # team_rankings2['Pressing Rating'] = round(team_rankings2['Pressing'],1)

                # team_rankings2['Goal Kick Buildouts'] = ((0.3 * team_rankings2['pctAvg. Distance Reached']) + (0.15 * team_rankings2['pctAvg. Buildup Speed']) + (0.4 * team_rankings2['pct% -> Att. Half']) + (0.15 * team_rankings2['pctPasses per Sequence']))
                # #team_rankings['pctShort GK Buildups'] = round(team_rankings['Short GK Buildups'].rank(pct=True) * 100,2)
                # team_rankings2['Buildout Score'] = round(team_rankings2['Goal Kick Buildouts'],1)

                team_rankings2['Changing Point of Attack'] = (0.65 * team_rankings2['pctSwitches']) + (0.1 * team_rankings2['pctSwitch Accuracy']) + (0.25 * team_rankings2['pctSwitches Leading to Shots'])
                team_rankings2['Switch Score'] = round(team_rankings2['Changing Point of Attack'],1)




                team_rankings2 = team_rankings2[team_rankings2['Team'] != selected_team]
                team_rankings = team_rankings[team_rankings['Team'] == selected_team]
                
                team_rankings = pd.concat([team_rankings, team_rankings2], ignore_index=True)

                #print(team_rankings[team_rankings['Team'] == selected_team]['Pressing Rating'].values[0])

                
                            


            for col in orig_cols:
                team_rankings[col] = round(team_rankings[col],2)
                shortened_switch_data = team_rankings.sort_values(by = 'Switch Score', ascending=False)
                #shortened_gk_data = shortened_gk_data[['Team','Matches', 'Buildout Score', '% of Goal Kicks Short', 'Passes per Sequence', 'Avg. Buildup Speed', 'Avg. Distance Reached','% -> Att. Half', '% -> Att. Third']]
                shortened_switch_data = shortened_switch_data[['Team','Switch Score','Matches',  'Switches', 'Switch Accuracy', 'Switches Leading to Shots']]
                #st.write(shortened_pressing_data)

            shortened_switch_data['Team'] = shortened_switch_data['Team'].replace({
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
                'El Paso Locomotive': 'El Paso',
                'Orlando Pride': 'Orlando',
                'Washington Spirit': 'Washington',
                'NJ/NY Gotham FC': 'Gotham',
                'North Carolina Courage': 'NC Courage',
                'Portland Thorns': 'Portland',
                'Chicago Red Stars': 'Chicago',
                'Seattle Reign': 'Seattle',
                'San Diego Wave': 'San Diego',
                'Houston Dash': 'Houston',
                'Utah Royals': 'Utah'
                
            })
            shortened_switch_data.set_index('Team', inplace=True)

            #st.dataframe(shortened_pressing_data, use_container_width=True, height = 280)
            st.dataframe(shortened_switch_data, height = 280)

            
        with col2:
            
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
            #             half=False, pad_top=2, corner_arcs=True)

            # fig,ax = pitch.draw(figsize=(6,8))
            # fig.set_facecolor('black')

            # gk_events = pd.read_parquet(f"{league}VideoGoalKickEvents.parquet")

            # gk_events = gk_events[gk_events['match_id'].isin(selected_ids)]

            # for _, row in gk_events.iterrows():
            #     x = row['gk_end_x']
            #     y = row['gk_end_y']
            #     pitch.scatter(x,y, ax = ax, color = 'white', s = 20)
                
              
            # ax.text(60, -5,'End Location of Short Goal Kick Buildouts', color = 'white', ha = 'center', fontsize = 12.5)
            # ax.text(60, -2,'Direction of Attack --->', color = 'white', ha = 'center', fontsize = 10)

            # buf = io.BytesIO()
            # plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
            # buf.seek(0)

            # # Display the image
            # st.image(buf, use_column_width=True)
            st.session_state.old_selected_points_t4 = st.session_state.selected_points_t4
            fig = create_pitch(480,320)
            #fig = create_pitch(600,400)
            
            # Load Goal Kick Event Data
            # Replace this with your parquet file, and make sure you have your dataframe loaded.
            switch_events = pd.read_parquet(f"{league}VideoSwitchEvents.parquet")

            # Filter based on selected match ids
            switch_events = switch_events[switch_events['match_id'].isin(selected_ids)] 

            customdata = switch_events['title']

            for index, row in switch_events.iterrows():
                fig.add_trace(go.Scatter(
                    x=[row['x'], row['pass_end_x']],
                    y=[row['y'], row['pass_end_y']],
                    mode='lines',
                    line=dict(color='rgba(255, 255, 255, 0.5)', width=1),
                    showlegend=False,
                    hoverinfo='skip'
                ))

            # Plot the goal kick events
            fig.add_trace(go.Scatter(
                x= switch_events['x'],
                y= switch_events['y'],
                
                mode='markers',
                marker=dict(color='purple', size=5),
                name="Switch End",
                hoverinfo="text",
                #text=switch_events['title'].astype(str)# + ", " + gk_events['gk_end_y'].astype(str)
                hovertemplate="<b>%{customdata}</b><extra></extra>",
                customdata=customdata,
                hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial"),
            ))
            fig.update_layout(
                hoverdistance=10,  # Increase hover area
                hovermode="closest",
                showlegend=False
            )
            
            


            # Add title and direction of attack
            fig.add_annotation(text="Switches", xref="paper", yref="paper",
                            x=0.5, y=1.05, showarrow=False, font=dict(color="white", size=14), align="center")
            fig.add_annotation(text="Direction of Attack --->", xref="paper", yref="paper",
                            x=0.5, y=-0.05, showarrow=False, font=dict(color="white", size=12), align="center")

            # Display in Streamlit
            #st.plotly_chart(fig)
            #overlay_container = st.empty()

            show_mode = st.session_state.show_video
            
            
            selected_points_t4 = True
            selected_points_t4 = plotly_events(fig, click_event=True)
            
            # if st.session_state.show_video == False and selected_points_t3:
            
            # if st.session_state.selected_points_t3




            

            print(f"old: {st.session_state.old_selected_points_t4}")
            #if st.session_state.show_video and selected_points_t3:
            if st.session_state.old_selected_points_t4 != selected_points_t4:
            #if selected_points_t3:
                
                #st.session_state.show_video = True
                if len(selected_points_t4) > 0:
                    clicked_point = selected_points_t4[0]  # If multiple points, handle accordingly
                    clicked_index = clicked_point['pointIndex']
                    clicked_event = switch_events.iloc[clicked_index]
                
                    filename = clicked_event['filename']
                    print(filename)
                    start_time = clicked_event['start_time']
                    file_id = files_df.loc[files_df['File Name'] == filename]['File ID'].values[0]
                    # Extract video info (filename and start_time)
                    video_url = f"https://drive.google.com/file/d/{file_id}/preview?t={start_time}"
                    if st.session_state.show_video or selected_points_t4:
                        st.markdown(f'''
                        <div id="video-popup" style="position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.8); display:flex; align-items:center; justify-content:center; z-index:999;">
                            <div style="position:relative; width:60%; max-width:800px; height:60%; max-height:450px;">
                                <iframe src="{video_url}" width="100%" height="100%" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)

                        st.session_state.selected_points_t4 = selected_points_t4


        #dual_progress_bars(60, "Progress 1", 85, "Progress 2")

        col1, col2 = st.columns(2)
        with col1: 
            metric = st.selectbox(
            'Select Metric',
            ['Switches', '-> Box Entries', '-> Shots', 'Inaccurate Switches']
            )
        
        if metric == 'Switches': data = pd.read_parquet(f"{league}VideoSwitchEvents.parquet")
        elif metric == '-> Box Entries': data = pd.read_parquet(f"{league}switch_box_entries_video_events.parquet")
        elif metric == '-> Shots': data = pd.read_parquet(f"{league}switch_shots_video_events.parquet")
        elif metric == 'Inaccurate Switches': data = pd.read_parquet(f"{league}innacurate_switches_video_events.parquet")
        data = data.drop_duplicates(subset = ['match_id', 'period']).reset_index()

        data = data[data['match_id'].isin(selected_ids)].reset_index()
        if len(data) == 0: 
            st.error("No events in selected matches")
        
        # with col2:
        #     sort_method = st.selectbox(
        #         'Sort By',
        #         ['Most Recent']
        #     )
        
        if 'clip_index_t4' not in st.session_state:
            st.session_state.clip_index_t4 = 0
        def update_index_t4(step):
            new_index = st.session_state.clip_index_t4 + step
            if 0 <= new_index < len(clip_titles_t4):
                st.session_state.clip_index_t4 = new_index
                st.session_state.clip_selector_t4 = clip_titles_t4[new_index]

        sorted_data_t4 = data.sort_values(by=['match_id', 'period', 'timestamp'], ascending=[False, True, True])
        clip_titles_t4 = sorted_data_t4['title'].tolist()

        
        with col2:
            #selection = st.selectbox('Choose Clip', data.sort_values(by=['match_id', 'period', 'timestamp'], ascending=[False,True,True])['title'])
            # sorted_data = data.sort_values(by=['match_id', 'period', 'timestamp'], ascending=[False, True, True])
            # clip_titles_t2 = sorted_data['title'].tolist()


            #selection = st.selectbox('Choose Clip', clip_titles_t2, index=st.session_state.clip_index)
            # print("index", st.session_state.clip_index_t2)
            # print(len(clip_titles_t2))
            selection = st.selectbox('Choose Clip', clip_titles_t4, index=st.session_state.clip_index_t4, key='clip_selector_t4')
            if selection != clip_titles_t4[st.session_state.clip_index_t4]:
                st.session_state.clip_index_t4 = clip_titles_t4.index(selection)

            
 


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
        #print(time_str)
        segment, time_within_segment = find_closest_segment_with_times(time_str)
 

        csv_file_path = 'drive_files.csv'
        files_df = pd.read_csv(csv_file_path)

        def display_video(match_selection, half_selection, segment):
            
            filename = f"{match_selection}-h{half_selection}-{segment}.mp4"
            #(filename)
            file_id = files_df.loc[files_df['File Name'] == filename]['File ID'].values[0]
            # files = list_files_in_folder(FOLDER_ID)
            # file_id = get_file_id(filename, files)
            
            if file_id:
                #video_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                #video_url = f"https://drive.google.com/file/d/{file_id}/view"
                video_url = f"https://drive.google.com/file/d/{file_id}/preview?t={time_within_segment}"


                #print(f"{filename} -> Video URL: {video_url}")  # Debug print statement
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
        st.button("Previous Clip", on_click=update_index_t4, args=(-1,), disabled=(st.session_state.clip_index_t4 <= 0), key="prev_clip_button_t4")

        # with col2:
        st.button("Next Clip", on_click=update_index_t4, args=(1,), disabled=(st.session_state.clip_index_t4 >= len(clip_titles_t4) - 1), key="next_clip_button_t4")
         
        

        # st.session_state.old_selected_points = st.session_state.selected_points
        # fig = create_pitch()
        # # Load Goal Kick Event Data
        # # Replace this with your parquet file, and make sure you have your dataframe loaded.
        # gk_events = pd.read_parquet(f"{league}VideoGoalKickEvents.parquet")

        # # Filter based on selected match ids
        # gk_events = gk_events[gk_events['match_id'].isin(selected_ids)]

    
        # # Plot the goal kick events
        # fig.add_trace(go.Scatter(
        #     x=gk_events['gk_end_x'],
        #     y=gk_events['gk_end_y'],
        #     mode='markers',
        #     marker=dict(color='white', size=8),
        #     name="Goal Kick End",
        #     hoverinfo="text",
        #     text=gk_events['title'].astype(str) + " -> " + gk_events['gk_end_player'].astype(str)# + ", " + gk_events['gk_end_y'].astype(str)
        # ))
        
        


        # # Add title and direction of attack
        # fig.add_annotation(text="End Location of Short Goal Kick Buildouts", xref="paper", yref="paper",
        #                 x=0.5, y=1.05, showarrow=False, font=dict(color="white", size=14), align="center")
        # fig.add_annotation(text="Direction of Attack --->", xref="paper", yref="paper",
        #                 x=0.5, y=-0.05, showarrow=False, font=dict(color="white", size=12), align="center")

        # # Display in Streamlit
        # #st.plotly_chart(fig)
        # #overlay_container = st.empty()

        # show_mode = st.session_state.show_video
        
        
        # selected_points = True
        # selected_points = plotly_events(fig, click_event=True)
        
        # # if st.session_state.show_video == False and selected_points:
        
        # # if st.session_state.selected_points




        

        # print(f"old: {st.session_state.old_selected_points}")
        # #if st.session_state.show_video and selected_points:
        # if st.session_state.old_selected_points != selected_points:
        # #if selected_points:
            
        #     #st.session_state.show_video = True
        #     if len(selected_points) > 0:
        #         clicked_point = selected_points[0]  # If multiple points, handle accordingly
        #         clicked_index = clicked_point['pointIndex']
        #         clicked_event = gk_events.iloc[clicked_index]
            
        #         filename = clicked_event['filename']
        #         start_time = clicked_event['start_time']
        #         file_id = files_df.loc[files_df['File Name'] == filename]['File ID'].values[0]
        #         # Extract video info (filename and start_time)
        #         video_url = f"https://drive.google.com/file/d/{file_id}/preview?t={start_time}"
        #         if st.session_state.show_video or selected_points:
        #             st.markdown(f'''
        #             <div id="video-popup" style="position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.8); display:flex; align-items:center; justify-content:center; z-index:999;">
        #                 <div style="position:relative; width:60%; max-width:800px; height:60%; max-height:450px;">
        #                     <iframe src="{video_url}" width="100%" height="100%" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
        #                 </div>
        #             </div>
        #             ''', unsafe_allow_html=True)

        #             st.session_state.selected_points = selected_points

    with tab5:
        
        pct1 = team_rankings[team_rankings['Team'] == selected_team]['pctCrosses Completed'].values[0]
        pct2 = team_rankings[team_rankings['Team'] == selected_team]['pctCross Accuracy'].values[0]
        pct3 = team_rankings[team_rankings['Team'] == selected_team]['pctDeep Crosses'].values[0]
        pct4 = team_rankings[team_rankings['Team'] == selected_team]['pctCrosses Leading to Shots'].values[0]
        pct5 = team_rankings[team_rankings['Team'] == selected_team]['pctCrosses Leading to Goals'].values[0]
        pct6 = team_rankings[team_rankings['Team'] == selected_team]['pctDeep Crosses Leading to Shots'].values[0]
        
        
       
        col1, col2, col3 = st.columns(3)
        with col1: custom_progress_bar(int(pct1), f"Crosses Completed   ({round(team_rankings[team_rankings['Team'] == selected_team]['Crosses Completed'].values[0],1)})")
        with col2: custom_progress_bar(int(pct2), f"Cross Accuracy   ({int(round(team_rankings[team_rankings['Team'] == selected_team]['Cross Accuracy'].values[0],2) * 100)}%)")
        with col3: custom_progress_bar(int(pct3), f"Deep Crosses   ({round(team_rankings[team_rankings['Team'] == selected_team]['Deep Crosses'].values[0],1)})")
        
        with col1: custom_progress_bar(int(pct4), f"Crosses to Shots   ({round(team_rankings[team_rankings['Team'] == selected_team]['Crosses Leading to Shots'].values[0],1)})")
        with col2: custom_progress_bar(int(pct5), f"Crosses to Goals   ({round(team_rankings[team_rankings['Team'] == selected_team]['Crosses Leading to Goals'].values[0],1)})")
        with col3: custom_progress_bar(int(pct6), f"Deep Crosses to Shots   ({round(team_rankings[team_rankings['Team'] == selected_team]['Deep Crosses Leading to Shots'].values[0],1)})")
        
        
        
        st.write("")
        
        selected_metrics = ['Crosses Completed', 'Crosses Leading to Shots']
        #df = pd.DataFrame(data) 
        df = full_team_data.sort_values(by='match_id')

        #metrics = orig_cols#[col for col in df.columns if col != 'Match']
        metrics = ['Crosses Completed',
                   'Cross Accuracy',
                   'Deep Crosses',
                   'Crosses Leading to Shots',
                   'Crosses Leading to Goals',
                   'Deep Crosses Leading to Shots'

                   ]
        #print(metrics)
        if 'selected_metrics_t5' not in st.session_state:
            #st.session_state.selected_metrics = metrics[:2]  # Default to first two metrics
            st.session_state.selected_metrics_t5 = ['Crosses Completed', 'Crosses Leading to Shots']
        

        

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
                layout['yaxis2'] = {
                    'title': selected_metrics[1], 
                    'side': "right", 
                    'overlaying': "y",
                    'titlefont': {'color': 'purple'}
                }
            
            if selected_metrics[0] in neg_cols:
                layout['yaxis']['autorange'] = 'reversed'
            if len(selected_metrics) == 2 and selected_metrics[1] in neg_cols:
                layout['yaxis2']['autorange'] = 'reversed'

            fig.update_layout(layout)

            #print(st.session_state.selected_metrics_t2)

            return fig

        # Create columns for metrics selection
        cols = st.columns(len(metrics))

        for i, metric in enumerate(metrics):
            with cols[i]:
                if st.checkbox(metric, value=(metric in st.session_state.selected_metrics_t5)):
                    if metric not in st.session_state.selected_metrics_t5:
                        st.session_state.selected_metrics_t5.append(metric)
                else:
                    if metric in st.session_state.selected_metrics_t5:
                        st.session_state.selected_metrics_t5.remove(metric)

        # Enforce the restriction of selecting only 1 or 2 metrics
        if len(st.session_state.selected_metrics_t5) < 1 or len(st.session_state.selected_metrics_t5) > 2:
            st.error("Please select exactly 1 or 2 metrics.")
        else:
            # Create and display the plot
            fig = update_chart(st.session_state.selected_metrics_t5)
            st.plotly_chart(fig)








        col1, col2 = st.columns([0.9, 2])#st.columns(2)
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

                
                                
                
                # team_rankings2['Pressing'] = ((0.2 * team_rankings2['pctPPDA']) + (0.25 * team_rankings2['pctAvg. Defensive Distance']) + (0.2 * team_rankings2['pctAtt. Third Pressures']) + (0.25 * team_rankings2['pctAtt. Half Regains']) + (0.1 * team_rankings2['pctShots after Pressure Regains']))
                # #team_rankings['Pressing'] = round(team_rankings['Pressing'].rank(pct=True) * 100,2)
                # team_rankings2['Pressing Rating'] = round(team_rankings2['Pressing'],1)

                # team_rankings2['Goal Kick Buildouts'] = ((0.3 * team_rankings2['pctAvg. Distance Reached']) + (0.15 * team_rankings2['pctAvg. Buildup Speed']) + (0.4 * team_rankings2['pct% -> Att. Half']) + (0.15 * team_rankings2['pctPasses per Sequence']))
                # #team_rankings['pctShort GK Buildups'] = round(team_rankings['Short GK Buildups'].rank(pct=True) * 100,2)
                # team_rankings2['Buildout Score'] = round(team_rankings2['Goal Kick Buildouts'],1)

                team_rankings2['Crossing'] = (0.35 * team_rankings2['pctCrosses Completed']) + (0.1 * team_rankings2['pctCross Accuracy']) + (0.4 * team_rankings2['pctCrosses Leading to Shots']) + (0.15 * team_rankings2['pctCrosses Leading to Goals'])
                team_rankings2['Cross Score'] = round(team_rankings2['Crossing'],1)




                team_rankings2 = team_rankings2[team_rankings2['Team'] != selected_team]
                team_rankings = team_rankings[team_rankings['Team'] == selected_team]
                
                team_rankings = pd.concat([team_rankings, team_rankings2], ignore_index=True)

                #print(team_rankings[team_rankings['Team'] == selected_team]['Pressing Rating'].values[0])

                
                            


            for col in orig_cols:
                team_rankings[col] = round(team_rankings[col],2)
                shortened_cross_data = team_rankings.sort_values(by = 'Cross Score', ascending=False)
                #shortened_gk_data = shortened_gk_data[['Team','Matches', 'Buildout Score', '% of Goal Kicks Short', 'Passes per Sequence', 'Avg. Buildup Speed', 'Avg. Distance Reached','% -> Att. Half', '% -> Att. Third']]
                shortened_cross_data = shortened_cross_data[['Team','Cross Score','Matches',  'Crosses Completed', 'Cross Accuracy', 'Crosses Leading to Shots', 'Crosses Leading to Goals', 'Deep Crosses','Deep Crosses Leading to Shots']]
                #st.write(shortened_pressing_data)

            shortened_cross_data['Team'] = shortened_cross_data['Team'].replace({
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
                'El Paso Locomotive': 'El Paso',
                'Orlando Pride': 'Orlando',
                'Washington Spirit': 'Washington',
                'NJ/NY Gotham FC': 'Gotham',
                'North Carolina Courage': 'NC Courage',
                'Portland Thorns': 'Portland',
                'Chicago Red Stars': 'Chicago',
                'Seattle Reign': 'Seattle',
                'San Diego Wave': 'San Diego',
                'Houston Dash': 'Houston',
                'Utah Royals': 'Utah'
                
            })
            shortened_cross_data.set_index('Team', inplace=True)

            #st.dataframe(shortened_pressing_data, use_container_width=True, height = 280)
            st.dataframe(shortened_cross_data, height = 280)

            
        with col2:
            
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
            #             half=False, pad_top=2, corner_arcs=True)

            # fig,ax = pitch.draw(figsize=(6,8))
            # fig.set_facecolor('black')

            # gk_events = pd.read_parquet(f"{league}VideoGoalKickEvents.parquet")

            # gk_events = gk_events[gk_events['match_id'].isin(selected_ids)]

            # for _, row in gk_events.iterrows():
            #     x = row['gk_end_x']
            #     y = row['gk_end_y']
            #     pitch.scatter(x,y, ax = ax, color = 'white', s = 20)
                
              
            # ax.text(60, -5,'End Location of Short Goal Kick Buildouts', color = 'white', ha = 'center', fontsize = 12.5)
            # ax.text(60, -2,'Direction of Attack --->', color = 'white', ha = 'center', fontsize = 10)

            # buf = io.BytesIO()
            # plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
            # buf.seek(0)

            # # Display the image
            # st.image(buf, use_column_width=True)
            st.session_state.old_selected_points_t5 = st.session_state.selected_points_t5
            fig = create_pitch(480,320)
            #fig = create_pitch(600,400) 
            
            # Load Goal Kick Event Data
            # Replace this with your parquet file, and make sure you have your dataframe loaded.
            #cross_events = pd.read_parquet(f"{league}VideoCrossEvents.parquet")
            cross_events = pd.read_parquet(f"{league}crosses_to_shots_video_events.parquet")

            # Filter based on selected match ids
            cross_events = cross_events[cross_events['match_id'].isin(selected_ids)] 

            customdata = cross_events['title']
            colors = ['green' if goal else 'purple' for goal in cross_events['cross_leading_to_goal']]



        
            # Plot the goal kick events
            fig.add_trace(go.Scatter(
                x= cross_events['x'],
                y= cross_events['y'],
                
                mode='markers',
                marker=dict(color=colors, size=5),
                name="Cross End",
                hoverinfo="text",
                #text=cross_events['title'].astype(str)# + ", " + gk_events['gk_end_y'].astype(str)
                hovertemplate="<b>%{customdata}</b><extra></extra>",
                customdata=customdata,
                hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial"),
            ))
            fig.update_layout(
                hoverdistance=10,  # Increase hover area
                hovermode="closest",
                showlegend=False
            )
            
            


            # Add title and direction of attack
            fig.add_annotation(text="Crosses Leading to Shots", xref="paper", yref="paper",
                            x=0.5, y=1.05, showarrow=False, font=dict(color="white", size=14), align="center")
            # fig.add_annotation(text="Direction of Attack --->", xref="paper", yref="paper",
            #                 x=0.5, y=-0.05, showarrow=False, font=dict(color="white", size=12), align="center")

            # Display in Streamlit
            #st.plotly_chart(fig)
            #overlay_container = st.empty()

            show_mode = st.session_state.show_video
            
            
            selected_points_t5 = True
            selected_points_t5 = plotly_events(fig, click_event=True)
            
            # if st.session_state.show_video == False and selected_points_t3:
            
            # if st.session_state.selected_points_t3




            

            print(f"old: {st.session_state.old_selected_points_t5}")
            #if st.session_state.show_video and selected_points_t3:
            if st.session_state.old_selected_points_t5 != selected_points_t5:
            #if selected_points_t3:
                
                #st.session_state.show_video = True
                if len(selected_points_t5) > 0:
                    clicked_point = selected_points_t5[0]  # If multiple points, handle accordingly
                    clicked_index = clicked_point['pointIndex']
                    clicked_event = cross_events.iloc[clicked_index]
                
                    filename = clicked_event['filename']
                    start_time = clicked_event['start_time']
                    file_id = files_df.loc[files_df['File Name'] == filename]['File ID'].values[0]
                    # Extract video info (filename and start_time)
                    video_url = f"https://drive.google.com/file/d/{file_id}/preview?t={start_time}"
                    if st.session_state.show_video or selected_points_t5:
                        st.markdown(f'''
                        <div id="video-popup" style="position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.8); display:flex; align-items:center; justify-content:center; z-index:999;">
                            <div style="position:relative; width:60%; max-width:800px; height:60%; max-height:450px;">
                                <iframe src="{video_url}" width="100%" height="100%" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)

                        st.session_state.selected_points_t5 = selected_points_t5


        #dual_progress_bars(60, "Progress 1", 85, "Progress 2")

        col1, col2 = st.columns(2)
        with col1: 
            metric = st.selectbox(
            'Select Metric',
            ['Crosses Completed', '-> Shots', '-> Goals', 'Deep Crosses']
            )
        
        if metric == 'Crosses Completed': data = pd.read_parquet(f"{league}crosses_completed_video_events.parquet")
        elif metric == '-> Shots': data = pd.read_parquet(f"{league}crosses_to_shots_video_events.parquet")
        elif metric == '-> Goals': data = pd.read_parquet(f"{league}crosses_to_goals_video_events.parquet")
        elif metric == 'Deep Crosses': data = pd.read_parquet(f"{league}deep_crosses_to_shots_video_events.parquet")
        data = data.drop_duplicates(subset = ['match_id', 'period']).reset_index()

        data = data[data['match_id'].isin(selected_ids)].reset_index()
        if len(data) == 0: 
            st.error("No events in selected matches")
        
        # with col2:
        #     sort_method = st.selectbox(
        #         'Sort By',
        #         ['Most Recent']
        #     )
        
        if 'clip_index_t5' not in st.session_state:
            st.session_state.clip_index_t5 = 0
        def update_index_t5(step):
            new_index = st.session_state.clip_index_t5 + step
            if 0 <= new_index < len(clip_titles_t5):
                st.session_state.clip_index_t5 = new_index
                st.session_state.clip_selector_t5 = clip_titles_t5[new_index]

        sorted_data_t5 = data.sort_values(by=['match_id', 'period', 'timestamp'], ascending=[False, True, True])
        clip_titles_t5 = sorted_data_t5['title'].tolist()

        
        with col2:
            #selection = st.selectbox('Choose Clip', data.sort_values(by=['match_id', 'period', 'timestamp'], ascending=[False,True,True])['title'])
            # sorted_data = data.sort_values(by=['match_id', 'period', 'timestamp'], ascending=[False, True, True])
            # clip_titles_t2 = sorted_data['title'].tolist()


            #selection = st.selectbox('Choose Clip', clip_titles_t2, index=st.session_state.clip_index)
            # print("index", st.session_state.clip_index_t2)
            # print(len(clip_titles_t2))
            selection = st.selectbox('Choose Clip', clip_titles_t5, index=st.session_state.clip_index_t5, key='clip_selector_t5')
            if selection != clip_titles_t5[st.session_state.clip_index_t5]:
                st.session_state.clip_index_t5 = clip_titles_t5.index(selection)

            
 


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
        #print(time_str)
        segment, time_within_segment = find_closest_segment_with_times(time_str)
 

        csv_file_path = 'drive_files.csv'
        files_df = pd.read_csv(csv_file_path)

        def display_video(match_selection, half_selection, segment):
            
            filename = f"{match_selection}-h{half_selection}-{segment}.mp4"
            #(filename)
            file_id = files_df.loc[files_df['File Name'] == filename]['File ID'].values[0]
            # files = list_files_in_folder(FOLDER_ID)
            # file_id = get_file_id(filename, files)
            
            if file_id:
                #video_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                #video_url = f"https://drive.google.com/file/d/{file_id}/view"
                video_url = f"https://drive.google.com/file/d/{file_id}/preview?t={time_within_segment}"


                #print(f"{filename} -> Video URL: {video_url}")  # Debug print statement
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
        st.button("Previous Clip", on_click=update_index_t5, args=(-1,), disabled=(st.session_state.clip_index_t5 <= 0), key="prev_clip_button_t5")

        # with col2:
        st.button("Next Clip", on_click=update_index_t5, args=(1,), disabled=(st.session_state.clip_index_t5 >= len(clip_titles_t4) - 1), key="next_clip_button_t5")
         
        

        # st.session_state.old_selected_points = st.session_state.selected_points
        # fig = create_pitch()
        # # Load Goal Kick Event Data
        # # Replace this with your parquet file, and make sure you have your dataframe loaded.
        # gk_events = pd.read_parquet(f"{league}VideoGoalKickEvents.parquet")

        # # Filter based on selected match ids
        # gk_events = gk_events[gk_events['match_id'].isin(selected_ids)]

    
        # # Plot the goal kick events
        # fig.add_trace(go.Scatter(
        #     x=gk_events['gk_end_x'],
        #     y=gk_events['gk_end_y'],
        #     mode='markers',
        #     marker=dict(color='white', size=8),
        #     name="Goal Kick End",
        #     hoverinfo="text",
        #     text=gk_events['title'].astype(str) + " -> " + gk_events['gk_end_player'].astype(str)# + ", " + gk_events['gk_end_y'].astype(str)
        # ))
        
        


        # # Add title and direction of attack
        # fig.add_annotation(text="End Location of Short Goal Kick Buildouts", xref="paper", yref="paper",
        #                 x=0.5, y=1.05, showarrow=False, font=dict(color="white", size=14), align="center")
        # fig.add_annotation(text="Direction of Attack --->", xref="paper", yref="paper",
        #                 x=0.5, y=-0.05, showarrow=False, font=dict(color="white", size=12), align="center")

        # # Display in Streamlit
        # #st.plotly_chart(fig)
        # #overlay_container = st.empty()

        # show_mode = st.session_state.show_video
        
        
        # selected_points = True
        # selected_points = plotly_events(fig, click_event=True)
        
        # # if st.session_state.show_video == False and selected_points:
        
        # # if st.session_state.selected_points




        

        # print(f"old: {st.session_state.old_selected_points}")
        # #if st.session_state.show_video and selected_points:
        # if st.session_state.old_selected_points != selected_points:
        # #if selected_points:
            
        #     #st.session_state.show_video = True
        #     if len(selected_points) > 0:
        #         clicked_point = selected_points[0]  # If multiple points, handle accordingly
        #         clicked_index = clicked_point['pointIndex']
        #         clicked_event = gk_events.iloc[clicked_index]
            
        #         filename = clicked_event['filename']
        #         start_time = clicked_event['start_time']
        #         file_id = files_df.loc[files_df['File Name'] == filename]['File ID'].values[0]
        #         # Extract video info (filename and start_time)
        #         video_url = f"https://drive.google.com/file/d/{file_id}/preview?t={start_time}"
        #         if st.session_state.show_video or selected_points:
        #             st.markdown(f'''
        #             <div id="video-popup" style="position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.8); display:flex; align-items:center; justify-content:center; z-index:999;">
        #                 <div style="position:relative; width:60%; max-width:800px; height:60%; max-height:450px;">
        #                     <iframe src="{video_url}" width="100%" height="100%" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
        #                 </div>
        #             </div>
        #             ''', unsafe_allow_html=True)

        #             st.session_state.selected_points = selected_points

    
        
            
            

if individual == 'Player':    
    tab1, tab2, tab3, tab4 = st.tabs(['Tackling', 'Heading', 'Progressive Passing','Changing Point of Attack'])
