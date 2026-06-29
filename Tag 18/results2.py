import pandas as pd
import matplotlib.pyplot as plt

url = "https://raw.githubusercontent.com/martj42/international_results/master/results.csv"

df = pd.read_csv(url)

def get_gewinner(row):
    if row['home_score'] > row['away_score']:
        return row['home_team']

    elif row['away_score'] > row['home_score']:
        return row['away_team']
    else:
        return 'Unentschieden'


df['gewinner'] = df.apply(get_gewinner, axis=1)

home_games = df['home_team'].value_counts()
away_games = df['away_team'].value_counts()


total_games = home_games.add(away_games, fill_value=0).astype(int)

wins = df[df['gewinner'] != 'Unentschieden']['gewinner'].value_counts()

wins = wins.reindex(total_games.index, fill_value=0).astype(int)

stats = pd.DataFrame ({
    'Spiele': total_games,
    'Siege': wins
})
stats['Siegquote_%'] = round((stats['Siege'] / stats['Spiele'])*100, 2)

top_teams = stats[stats['Spiele'] >= 200].sort_values(by='Siegquote_%', ascending=False)


top_10 = top_teams.head(10).reset_index()
top_10.columns = ['Team', 'Spiele', 'Siege', 'Siegquote_%']

plt.figure(figsize=(12, 6))

bars = plt.barh(top_10['Team'], top_10['Siegquote_%'], color='#1f77b4', edgecolor='black')

plt.gca().invert_yaxis()


plt.title('Top 10 Nationalmannschaften aller Zeiten (mind. 200 Spiele)', fontsize=14, fontweight='bold')
plt.xlabel('Siegquote in %', fontsize=12)
plt.ylabel('Team', fontsize=12)

for bar in bars:
    width = bar.get_width()
    plt.text(width + 1, bar.get_y() + bar.get_height()/2, f'{width:.2f}%', 
             va='center', ha='left', fontsize=10)


plt.tight_layout()
plt.show()
