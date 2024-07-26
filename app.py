#import pandas
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import openpyxl
# read xlsx file in this work directory
df = pd.read_excel('bayern-bvb-fichajes-filtro@3.xlsx')
print(df.columns)

# Create filters by year with interactive dropdown including an option to display data for all years
st.sidebar.subheader("Season")
year_options = ["All Seasons"] + list(df["Torneo"].unique())
year_filter = st.sidebar.selectbox("Season", year_options)

# Filter data based on the selected year
if year_filter != "All Seasons":
    df_filtered = df[df["Torneo"] == year_filter]
else:
    df_filtered = df

player_filtered_unique=list(df_filtered['Jugador'].unique())

#make nodes and links for a sankey graph to visualize the flow of players to Bayern Munich and Borussia Dortmund
nodes = list(df_filtered['Liga_origen'].unique()) + list(df_filtered['Club_destino'].unique())+ list(df_filtered['Jugador'].unique())
nodes = list(dict.fromkeys(nodes))
print(len(nodes))

links = []
for index, row in df_filtered.iterrows():
    links.append({'source': nodes.index(row['Liga_origen']), 'target': nodes.index(row['Club_destino']), 'player': nodes.index(row['Jugador']), 'value': 1})
print(len(links))
#create a sankey graph. Please assign red as line color for bayern munich and gold as line color for borussia dortmund
# include player name in hover infobox
fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = list(df_filtered['Liga_origen'].unique()),
      customdata=nodes,
      hovertemplate='Node %{customdata} has total value %{value}<extra></extra>',
      color = ["orange" if node in ["Bundesliga", "Bayern Múnich", "Borussia Dortmund"] else "white" for node in nodes]
    ),
    link = dict(
      source = [link['source'] for link in links],
      target = [link['target'] for link in links],
      value = [link['value'] for link in links],
      label=df_filtered['Jugador'],
      customdata= df_filtered['Jugador'].unique(),
      hovertemplate = "Source: %{source.customdata}<br>Target: %{target.customdata}<br>Player: %{label}<extra></extra>",
      color = ["red" if nodes[link['target']] == "Bayern Múnich" else "gold" for link in links]
    )
)]
)

#make the graph look better by adjusting the font size, title and layout
fig.update_layout(title_text=f"Flow of Players to Bayern Munich and Borussia Dortmund {year_filter}", font_size=15, title_font_size= 25)
fig.update_layout(width=1000, height=800)
st.plotly_chart(fig)
