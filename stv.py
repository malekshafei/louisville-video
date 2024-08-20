import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsbombpy import sb
creds = {"user": "rdell@racingloufc.com", "passwd": "8CStqFOa"}


from PIL import Image, ImageOps
import io
import warnings
warnings.filterwarnings('ignore')
from datetime import datetime, timedelta

def change_racing_names(x):
    #Racing
    if x == "Jaelin Marie Howell": return "Jaelin Howell"
    elif x == 'Ariadina Alves Borges': return 'Ary Boryes'
    elif x == 'Savannah Marie DeMelo': return 'Savannah DeMelo'
    elif x == 'Elexa Marie Bahr Gutiérrez': return 'Elexa Bahr'
    elif x == 'Marisa Marie DiGrande': return 'Marisa DiGrande'
    
    #Gotham
    elif x == 'Bruna Santos Nhaia': return 'Bruninha'
    elif x == 'Maitane López Millán': return 'Maitane López'
    elif x == 'Crystal Alyssia Dunn Soubrier': return 'Crystal Dunn'
    elif x == 'Esther Gonzalez Rodríguez': return 'Esther Gonzalez'
    
    #Orlando
    elif x == 'Angelina Alonso Costantino': return 'Angelina Costantino'
    elif x == 'Adriana Leal da Silva': return 'Adriana Leal'
    elif x == 'Marta Vieira da Silva Veiga': return 'Marta'
    
    #Seattle
    elif x == 'Cristian Roldán Leó': return 'Cristian Roldan'
    
    #Spirit
    elif x == 'Trinity Rain Moyer-Rodman': return 'Trinity Rodman'
    
    #LouCity
    elif x == 'Ray Serrano Lopez': return 'Ray Serrano'
    elif x == 'Jorge Gonzalez Asensi': return 'Jorge Gonzalez'
    elif x == 'Jake Francis Morris': return 'Jake Morris'
    elif x == 'Arturo Osuna Ordoñez': return 'Arturo Ordoñez'
    
    elif x == 'Charles Robbins Mertz Jr.': return 'Robbie Mertz'
    else: return x
    
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
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

selected_team = 'Louisville City'

matches = sb.matches(competition_id = 89, season_id = 282, creds=creds)
matches = matches[matches['data_version'].notna()]
matches = matches.sort_values(by = 'match_date', ascending=False)
matches = matches[(matches['home_team'] == selected_team) | (matches['away_team'] == selected_team)]
match_ids = matches.match_id.tolist()

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
    '8/17 vs Charleston'
           ]


mode_selection = 'Verticality'
col_to_check = 'ovr_verticality'
data = pd.read_parquet("vert-data.parquet")



col1, col2, col3, col4= st.columns(4)
with col1:
    mode_selection = st.selectbox(
        'Select Mode',
        ['Team', 'Player']
    )

# Place the second selectbox in the second column
with col2:
    #player_options = df[df['Competition'] == st.session_state.league1]['Player'].unique()
    match_selection = st.selectbox(
        'Select Match',
        ['All Matches'] + list(reversed(matches))
        
    )

# Place the third selectbox in the third column
with col3:
    #season_options = sorted(df[(df['Competition'] == st.session_state.league1) & (df['Player'] == st.session_state.name1)]['Season'].unique(), reverse=True)
    if mode_selection == 'Team':
        metric = st.selectbox(
            'Select Metric',
            ['Verticality', 'Chance Creation'],
            #season_options
        )
    if mode_selection == 'Player':
        metric = st.selectbox(
            'Select Metric',
            ['Progressive Passing', 'Key Passing', '1v1 Dribbles', 'Shooting'],
            #season_options
        )
with col4:
    sort_setting = st.selectbox(
        'Sort By',
        ['Most Recent', 'Best Actions']
    )

if mode_selection == 'Verticality':
    data = pd.read_parquet("vert-data.parquet")
    col_to_check = 'ovr_verticality'

if match_selection != 'All Matches':
    match_index = matches[matches == match_selection].index[0]
    match_id = match_ids[match_index]
    data = data[data['match_id'] == match_id].values[0]


if sort_setting == 'Most Recent':
    selection = st.selectbox('Select Clip',
            data.sort_values(by=['match_id', 'period', 'timestamp'], ascending=[False,True,True])['title'])
if sort_setting == 'Best Actions':
    selection = st.selectbox(
            'Select Clip',
            data.sort_values(by=[col_to_check], ascending=[False])['title']
        )

# with col1:
#     if sort_setting == 'Most Recent':
#         selection = st.selectbox(
#             'Select Clip',
#             data.sort_values(by=['match_id', 'period', 'timestamp'], ascending=[False,True,True])['title']
#         )
#     if sort_setting == 'Best Actions':
#         selection = st.selectbox(
#             'Select Clip',
#             data.sort_values(by=[col_to_check], ascending=[False])['title']
#         )
match_selection = data.loc[data['title'] == selection]['match_id'].values[0]
half_selection = data.loc[data['title'] == selection]['period'].values[0]
time_selection = data.loc[data['title'] == selection]['timestamp'].values[0]




# mode_selection = st.selectbox()
# half_selection = st.selectbox("Select Half", options = [1,2])
# selection = st.selectbox("Select Clip", options = data[data['period'] == half_selection]['title'])


import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch

sequence_id = data[data['title'] == selection]['sequence_id'].values[0]
#events = pd.read_parquet("/Users/malekshafei/Desktop/Louisville/USL-verticality.parquet")
events = pd.read_parquet("USL-verticality.parquet")
print('read file')

# Prepare the plot
pitch = Pitch(pitch_type='statsbomb', pitch_color='#400179', line_color='#c7d5cc', half=False, pad_top=4, corner_arcs=True)
fig, ax = pitch.draw(figsize=(12, 8))
fig.set_facecolor('#400179')

colors = ['white']  # Different colors for each sequence
legend_info = []


# Plot each sequence
sequence_group = events[events['sequence_id'] == sequence_id]
vert_row = data[data['sequence_id'] == sequence_id].iloc[0]
print(sequence_id)
#print(len(sequence_group))
sequence_group = sequence_group.sort_values(by=['timestamp', 'minute','second'])
first_event = sequence_group.iloc[0]
last_event = sequence_group.iloc[-1]

opponent = sequence_group['opp_team'].values[0]
date = sequence_group['clean_date'].values[0]
time = sequence_group['formatted_time'].values[0]
end_time = sequence_group['formatted_time'].values[-1]



time_info = f"{first_event['minute']}:{first_event['second']} - {last_event['minute']}:{last_event['second']}"
legend_label = f"{opponent} - {time_info}"
#legend_info.append((colors[idx % len(colors)], legend_label))




a = 1
for i, event in sequence_group.iterrows():

    if event['type'] in ['Pass', 'Carry', 'Shot']:
        event_time = event['formatted_time']
        player = change_racing_names(event['player'])
        action = event['type']
        

        x_start = event['x']
        y_start = event['y']

        if event['type'] == 'Pass':
            linestyle='solid'
            x_end = event['pass_end_x']
            y_end = event['pass_end_y']
            legend_info.append(f"{a}. {player} - {action}")

        elif event['type'] == 'Carry':
            linestyle='dashed'
            x_end = event['carry_end_x']
            y_end = event['carry_end_y']
            #print(x_end,y_end)
        else:
            #print("...")
            legend_info.append(f"{a}. {player} - {action}")
            #continue  # Skip this event if end location data is missing or not in the correct format

        # Draw lines and scatter for each event in the sequence
        pitch.lines(x_start, y_start, x_end, y_end, ax=ax, color='white', linewidth=3.5, linestyle=linestyle)
        pitch.scatter(x_start, y_start, ax=ax, color='white', s = 250)
        pitch.scatter(x_end, y_end, ax=ax, color='white', s = 250)

        ax.text(x_start, y_start, str(a), fontsize=9, color='black', ha='center', va='center')
        a += 1

if last_event['type'] == 'Ball Receipt*':
    x,y = last_event['x'], last_event['y']
    player = change_racing_names(last_event['player'])
    ax.text(x, y, str(a), fontsize=9, color='black', ha='center', va='center')
    legend_info.append(f"{a}. {player} - Reception")
    
    

def ordinal(x):
    if x >= 99: return "Top 1%"
    elif x >= 50: return f"Top {100-int(x)}%"
    elif x <= 1: return "Bottom 1%"
    else: return f"Bottom {int(x)}%"

for label in legend_info:
    ax.plot([], [], color='white', label=label)
ax.legend(loc='lower left',facecolor='#400179', edgecolor='None', title='Actions', fontsize = 12)
# Add titles and legend
ax.set_title(f"{date} Box Entry vs {opponent} - {time} - {end_time}", fontsize=20, color = 'white')




seq_pct_net_forward = int(vert_row['seq_pct_net_forward'] * 100)
pct_seq_pct_net_forward = int(vert_row['pct_seq_pct_net_forward'])
verticality_score = round(vert_row['ovr_verticality'],1)


seq_speed = round(vert_row['seq_speed'],1)
pct_seq_speed = round(vert_row['pct_seq_speed'],1)
#print(pct_seq_speed)
subtitle_1 = f"Verticality Score: {verticality_score}"
subtitle_0 = f"{seq_pct_net_forward}% of Passes Forward ({ordinal(pct_seq_pct_net_forward)})"
subtitle_2 = f"{seq_speed} m/s  ({ordinal(pct_seq_speed)})"
    
ax.text(0.5, 0.98, subtitle_1, ha='center', va='center', fontsize=14, transform=ax.transAxes, color = 'white')
ax.text(0.05, 0.98, subtitle_0, ha='left', va='center', fontsize=14, transform=ax.transAxes, color = 'white')
ax.text(0.85, 0.98, subtitle_2, ha='right', va='center', fontsize=14, transform=ax.transAxes, color = 'white')



buf = io.BytesIO()
plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)

# plt.savefig("/Users/malekshafei/Downloads/812test.png")
#fig.savefig("PIctestjuly3", format='png', bbox_inches='tight', pad_inches=0)

buf.seek(0)


# plt.savefig("PIctestjuly3.png")

#st.pyplot(plt)

    


# match_selection = data.loc[data['title'] == selection]['match_id'].values[0]
# half_selection = data.loc[data['title'] == selection]['period'].values[0]
# time_selection = data.loc[data['title'] == selection]['formatted_time'].values[0]

#minutes, seconds = map(int, time_selection.split(':'))

def find_closest_segment_with_times(time_str, segment_length = 60, overlap = 30):
    # Convert time_str to seconds
    minutes, seconds = map(int, time_str.split(':'))
    time_in_seconds = minutes * 60 + seconds

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




#video_path = f"lou-video-test/{match_selection}-h{half_selection}-{segment}.mp4"

#video_path = f"lou-video-test/{match_selection}-h{half_selection}.mp4"

#video_path = f"/Users/malekshafei/Desktop/Louisville/LouCity Video/3930487-h{half_selection}.mp4"
# minutes, seconds = map(int, time_selection.split(':'))
# start_time_seconds = minutes * 60 + seconds



# video_path = f"/Users/malekshafei/Desktop/Louisville/lou-video-test/{match_selection}-h{half_selection}-{segment}.mp4"

# st.video(video_path, start_time = time_within_segment)
# print(video_path)
# print('vid')

# import google.oauth2
# import google.auth

# from google.oauth2 import service_account
# from googleapiclient.discovery import build


# FOLDER_ID = '1_cmrY9EqRS8AuS5Wy1djNysyiZU8k-WP'

# SERVICE_ACCOUNT_FILE = '/Users/malekshafei/Downloads/louisville-video-drive-6fc10104701e.json'
# SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# credentials = service_account.Credentials.from_service_account_file(
#     SERVICE_ACCOUNT_FILE, scopes=SCOPES)


# service = build('drive', 'v3', credentials=credentials)

# # def list_files_in_folder(folder_id):
# #     query = f"'{folder_id}' in parents"
# #     results = service.files().list(q=query, fields="files(id, name)").execute()
# #     return results.get('files', [])
# def list_files_in_folder(folder_id):
#     files = []
#     page_token = None

#     while True:
#         response = service.files().list(
#             q=f"'{folder_id}' in parents",
#             fields="nextPageToken, files(id, name)",
#             pageToken=page_token
#         ).execute()

#         files.extend(response.get('files', []))
#         page_token = response.get('nextPageToken')

#         if not page_token:
#             break
    
#     # Print the number of files and their names for debugging
#     print(f"Number of files in folder: {len(files)}")
#     # for file in files:
#     #     print(f"File name: {file['name']}, File ID: {file['id']}")
    
#     return files

# def get_file_id(filename, files):
#     for file in files:
#         if file['name'] == filename:
#             return file['id']
#     return None

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

st.image(buf, use_column_width=True)
