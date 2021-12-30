import pandas as pd
import numpy as np
import streamlit as st


file = 'Peasts Kenis - Text Chats - general [94235299445493760].csv'
general_df = pd.read_csv(file)

general_df.Date = pd.to_datetime(general_df.Date, format='%d-%b-%y %I:%M %p')
certifiedDink = ['Mo#8516','Bryan#5357','Goat 🤠#4059','tornadotom50#8420','Jalapeño Cheez-It#0784',
                 'SamtyClaws#7243','Frozen Tofu#8827','rasdori#5703','jack phelps#4293','Hunter#1550']
certified_general_df = general_df.loc[general_df.Author.isin(certifiedDink)]


#Show tabular data frame in streamlit
st.title('Discord Analytics')
general_df


