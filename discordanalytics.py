import pymysql
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
#from streamlit_lottie import st_lottie

st.set_page_config(layout='wide')
#@st.cache
def get_df():
    file = 'Peasts Kenis - Text Chats - general [94235299445493760].csv'
    df = pd.read_csv(file)
    df.Date = pd.to_datetime(df.Date, format='%d-%b-%y %I:%M %p')
    return df

df = get_df()

defaultDink = ['Mo#8516','Bryan#5357','Goat 🤠#4059','SamtyClaws#7243']
certifiedDink = ['Mo#8516','Bryan#5357','Goat 🤠#4059','tornadotom50#8420','UrineTrouble#0784',
                 'SamtyClaws#7243','Frozen Tofu#8827','rasdori#5703','jack phelps#4293','Hunter#1550']

current_emotes =[":updatebrb:",":Trump2:",":Trump1:",":SteveDab:",":ResidentSleeper:",":PickleRick2:",
                 ":nut~1:",":NotWhikeThis:",":longho:",":LulCuckXd:",":Mo420:",":MoFace:",":monkaS:",
                 ":Moshroom:",":naughtychike:",":naughtysam:",":LennyLenny420:",":KeastOldMan:",":keastato:",
                 ":Kappa:",":JackieEggs:",":HunnaRage:",":HunnaB:",":emoji_51:",":FeelsBadMan:",":FeelsGoodMan:",
                 ":greensam:",":GreenShirt:",":HoFace:",":HoThumbsUp:",":HUH:",":doge:",":DatHeffy:",
                 ":DanThumbsDown:",":DannyTheElf:",":DannyePride:",":DanGasm:",":DanChamp:",":DanBrokeBack:",
                 ":beta:",":BibleThump:",":Bog:",":BogChamp:",":Bojangles:",":BryanLUL:",":CuteChike:",
                 ":Dan420:",":bdoe:",":Ban:",":5head:"]

df['Content'] = df['Content'].astype(str)
content = df['Content']
emoji = [i[0] for i in content.str.findall(':(?![\n])[()\w]+:') if len(i)>0]
emojiCount = pd.Series(emoji).value_counts(ascending = False)
emojiCount_df = emojiCount.to_frame()
FilterEmojiCount_df = emojiCount_df[emojiCount_df.index.isin(current_emotes)]
FilterEmojiCount_df.columns=['count']


# get sql connection
host = 'discord.cx7k4hmr40ql.us-east-1.rds.amazonaws.com'
user = 'admin'
password = 'peterdink'
tablename ='firstlist'
conn = pymysql.connect(host=host, user=user,password=password)
cursor = conn.cursor()
cursor.execute('use discordbot')

# get table as pandas df
query = f'SELECT * FROM {tablename}'
df_first = pd.read_sql_query(query, conn)
# localize to UTC time and convert to EST
df_first['timesent'] = df_first['timesent'].dt.tz_localize('utc').dt.tz_convert('US/Eastern')
# calculate juice to the second
hours = df_first['timesent'].dt.hour
minutes = df_first['timesent'].dt.minute
seconds = df_first['timesent'].dt.second
total_mins = (seconds/60)+minutes+(hours*60)
df_first['Juice'] = total_mins
df_grouped = df_first[['username','Juice']].groupby('username').mean()
df_grouped = df_grouped.sort_values('Juice',ascending=False).iloc[1:len(df_grouped)]

df_first['_1st to date'] = df_first.groupby('username').cumcount()+1

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Display in streamlit
st.title('Welcome to our Dashboard')
#lottie_discord = load_lottieurl('https://assets2.lottiefiles.com/packages/lf20_xtvomr66.json')
#st_lottie(lottie_discord,width=800,height=300)

dink_selection = st.multiselect('Choose your Dinks:',certifiedDink,default=defaultDink)
filtered_df = df.loc[df.Author.isin(dink_selection)]
filtered_df['count'] = ""
filtered_df = filtered_df.set_index('Date')
filtered_df = filtered_df.groupby('Author').resample('1M').count()
filtered_df = filtered_df.unstack(fill_value=0).T
filtered_df = filtered_df.reset_index()

bar_chart = px.bar(filtered_df,x='Date',y=dink_selection,title='Monthly messages',barmode='stack')
bar_chart.update_layout(width=1600,height=800)
st.plotly_chart(bar_chart)

# pie_chart = px.pie(FilterEmojiCount_df,names=FilterEmojiCount_df.index,values='count',title='Most Used Emojis')
# pie_chart.update_layout(width=800,height=800)
# st.plotly_chart(pie_chart)

line = px.line(df_first,x='timesent',y='_1st to date',color='username',width=1000,height=600)
line.update_layout(width=1600,height=800)
st.title('1st Leaderboard')
st.plotly_chart(line)
st.title('Juiciest Message 🧃')
st.dataframe(data=df_grouped)

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
