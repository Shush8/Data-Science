import pandas as pd
import matplotlib.pyplot as plt



# Beispiel-URL (falls du den direkten Link zur Rohdatei hast)
url = "https://raw.githubusercontent.com/martj42/international_results/master/results.csv"

# Pandas liest die Datei direkt aus dem Internet
df = pd.read_csv(url)

print(df.head())



# Datum konvertieren und das Jahr extrahieren
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year

# Funktion zur Ermittlung des Gewinners
def get_winner(row):
    if row['home_score'] > row['away_score']:
        return row['home_team']
    elif row['away_score'] > row['home_score']:
        return row['away_team']
    else:
        return 'Unentschieden'

df['winner'] = df.apply(get_winner, axis=1)

# 1. Spiele zählen
home_games = df['home_team'].value_counts()
away_games = df['away_team'].value_counts()
total_games = home_games.add(away_games, fill_value=0).astype(int)

# 2. Siege zählen
wins = df[df['winner'] != 'Unentschieden']['winner'].value_counts()
wins = wins.reindex(total_games.index, fill_value=0).astype(int)

# 3. In einem neuen DataFrame zusammenführen
stats = pd.DataFrame({
    'Spiele': total_games,
    'Siege': wins
})

# 4. Siegquote berechnen
stats['Siegquote_%'] = round((stats['Siege'] / stats['Spiele']) * 100, 2)

# Filter setzen für etablierte Teams
top_teams = stats[stats['Spiele'] >= 200].sort_values(by='Siegquote_%', ascending=False)

print("--- DIE TOP 5 TEAMS ALLER ZEITEN (NACH SIEGQUOTE) ---")
print(top_teams.head(5))

## Top 10 für die Grafik vorbereiten (Spaltennamen korrigieren)
top_10 = top_teams.head(10).reset_index()
top_10.columns = ['Team', 'Spiele', 'Siege', 'Siegquote_%']

# Plot erstellen
plt.figure(figsize=(12, 6))

# Ein horizontales Balkendiagramm mit reinem matplotlib (barh)
bars = plt.barh(top_10['Team'], top_10['Siegquote_%'], color='#1f77b4', edgecolor='black')

# Achsen umkehren, damit Platz 1 oben steht
plt.gca().invert_yaxis()

# Titel und Beschriftungen
plt.title('Top 10 Nationalmannschaften aller Zeiten (mind. 200 Spiele)', fontsize=14, fontweight='bold')
plt.xlabel('Siegquote in %', fontsize=12)
plt.ylabel('Team', fontsize=12)

# Werte direkt an die Balken schreiben
for bar in bars:
    width = bar.get_width()
    plt.text(width + 1, bar.get_y() + bar.get_height()/2, f'{width:.2f}%', 
             va='center', ha='left', fontsize=10)

# Layout optimieren und anzeigen
plt.tight_layout()
plt.show()