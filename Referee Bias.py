import sqlite3
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import dash
from dash import dcc, html
import plotly.express as px

# Create a SQL connection to the SQLite database in order to load data
con = sqlite3.connect('C:/Users/sayuj/Downloads/archive (1)/basketball.sqlite')

# Run SQL query to pull relevant information into a Pandas dataframe
df = pd.read_sql_query('SELECT Game_Officials.FIRST_NAME, Game_Officials.LAST_NAME, Game.WL_HOME, Game.PF_HOME, Game.WL_AWAY, Game.PF_AWAY FROM Game_Officials LEFT JOIN Game ON Game_Officials.GAME_ID = Game.GAME_ID WHERE Game.SEASON_ID = 22020', con)

# Close the connection
con.close()

# Encode W/L values to integers
df['WL_HOME'] = df['WL_HOME'].map(
                   {'W': 1 ,'L': 0})
df['WL_AWAY'] = df['WL_AWAY'].map(
                   {'W': 1 ,'L': 0})

# Merge first and last name columns into one column
df['Full Name'] = df[['FIRST_NAME', 'LAST_NAME']].apply(lambda x: ' '.join(x), axis=1)
df = df.drop(['FIRST_NAME', 'LAST_NAME'], axis=1)

# Group table by referree and add additional calculation columns
grouped_df = df.groupby(['Full Name']).sum()
grouped_df['Total Number of Games Officiated'] = df.groupby(['Full Name']).size()

# Function that is used for calculating relevant information per referee
def new_column(newCol, col1, col2):
        grouped_df[newCol] = grouped_df[col1]/grouped_df[col2]

# Adding win % and fouls per game calculation columns
new_column('Home Win %', 'WL_HOME', 'Total Number of Games Officiated')
new_column('Away Win %', 'WL_AWAY', 'Total Number of Games Officiated')
new_column('Home Fouls Per Game', 'PF_HOME', 'Total Number of Games Officiated')
new_column('Away Fouls Per Game', 'PF_AWAY', 'Total Number of Games Officiated')

# Calculating referee bias by finding the difference in fouls called per game home vs. away
grouped_df['Win Bias'] = abs(grouped_df['Home Win %'] - grouped_df['Away Win %'])
grouped_df['Foul Bias'] = abs(grouped_df['Home Fouls Per Game'] - grouped_df['Away Fouls Per Game'])

# Reset index
referee_data = grouped_df.reset_index(drop=False)

# Find outliers by seeing which refs have officiated too few games to extract relevant information
print(referee_data['Total Number of Games Officiated'].describe())
print(referee_data['Total Number of Games Officiated'].nsmallest(10))

# Drop the outliers
referee_data = referee_data[referee_data['Total Number of Games Officiated'] > 15]

# Create bar plot to see which referees have the highest proportion of the home team winning the game
sns.barplot(x='Home Win %', y='Full Name', data=referee_data.nlargest(10, 'Home Win %'))
plt.show()

# Create bar plot to see which referees have the highest proportion of the away team winning the game
sns.barplot(x='Away Win %', y='Full Name', data=referee_data.nlargest(10, 'Away Win %'))
plt.show()

# Create bar plot to see which referees have the highest bias in game outcome
sns.barplot(x='Win Bias', y='Full Name', data=referee_data.nlargest(10, 'Win Bias'))
plt.show()

# Create bar plot to see which referees have the highest bias when calling fouls
sns.barplot(x='Foul Bias', y='Full Name', data=referee_data.nlargest(10, 'Foul Bias'))
plt.show()

# While this shows some interesting visualizations on its own and provides plenty context. I want to create a more user-friendly dashboard that relays more information at once. Hence, I will use Dash to develop an application that provides further context of the data
app = dash.Dash(__name__)

fig1 = px.bar(referee_data, x='Full Name', y='Home Win %', barmode='group', title='Home Win Percent Based on Referee')
fig2 = px.bar(referee_data, x='Full Name', y='Away Win %', barmode='group', title='Away Win Percent Based on Referee')
fig3 = px.bar(referee_data, x='Full Name', y='Foul Bias', barmode='group', title='Overall Bias for Calling Fouls Per Referee')
fig4 = px.bar(referee_data, x='Full Name', y='Win Bias', barmode='group', title='Overall Bias on Game Outcome Based on Referee')
fig5 = px.bar(referee_data.nlargest(10, 'Win Bias'), x='Full Name', y='Win Bias', barmode='group', title='10 Most Biased Referees')
fig6 = px.scatter(referee_data, x='Foul Bias', y='Win Bias', color='Full Name', title='Comparison of Foul Bias Effect on Game Outcome')

app.layout = html.Div(
    children=[
        html.H1(children='Referee Bias Analytics',),
        html.P(
            children='An analysis of the bias individual NBA referees may have when it comes to calling fouls and game outcomes.'
        ),
        dcc.Graph(
            figure=fig1
        ),
        dcc.Graph(
            figure=fig2
        ),
        dcc.Graph(
            figure=fig3
        ),
        dcc.Graph(
            figure=fig4
        ),
        dcc.Graph(
            figure=fig5
        ),
        dcc.Graph(
            figure=fig6
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=False)