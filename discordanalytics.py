import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

#st.set_page_config(layout='wide')
@st.cache
def get_df():
    file = 'Peasts Kenis - Text Chats - general [94235299445493760].csv'
    df = pd.read_csv(file)
    df.Date = pd.to_datetime(df.Date, format='%d-%b-%y %I:%M %p')
    return df

df = get_df()

defaultDink = ['Mo#8516','Bryan#5357','Goat 🤠#4059','SamtyClaws#7243']
certifiedDink = ['Mo#8516','Bryan#5357','Goat 🤠#4059','tornadotom50#8420','UrineTrouble#0784',
                 'SamtyClaws#7243','Frozen Tofu#8827','rasdori#5703','jack phelps#4293','Hunter#1550']

# Display in streamlit
st.title('Discord Analytics')

dink_selection = st.multiselect('Choose your Dinks:',certifiedDink,default=defaultDink)
filtered_df = df.loc[df.Author.isin(dink_selection)]
filtered_df['count'] = ""
filtered_df = filtered_df.set_index('Date')
filtered_df = filtered_df.groupby('Author').resample('1M').count()
filtered_df = filtered_df.unstack(fill_value=0).T
filtered_df = filtered_df.reset_index()


bar_chart = px.bar(filtered_df,x='Date',y=dink_selection,barmode='stack')
st.plotly_chart(bar_chart,use_container_width=True)

