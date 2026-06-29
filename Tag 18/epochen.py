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

df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year

# Funktion zur Einteilung in historische Epochen
def get_era(year):
    if year < 1930:
        return '1. Die Anfänge (Vor der ersten WM: 1872-1929)'
    elif year < 1960:
        return '2. Nachkriegszeit & Pioniere (1930-1959)'
    elif year < 1980:
        return '3. Die goldene Ära & Totaler Fußball (1960-1979)'
    elif year < 2000:
        return '4. Taktik & Globalisierung (1980-1999)'
    else:
        return '5. Der moderne Spitzenfußball (2000-Heute)'

df['era'] = df['year'].apply(get_era)


print("--- DOMINANTE TEAMS JE NACH EPOCHE ---\n")

# Wir gehen jede Epoche Schritt für Schritt durch
for era_name, era_df in df.groupby('era'):
    
    # 1. Spiele in dieser Epoche zählen
    home = era_df['home_team'].value_counts()
    away = era_df['away_team'].value_counts()
    total = home.add(away, fill_value=0).astype(int)
    
    # 2. Siege in dieser Epoche zählen
    wins = era_df[era_df['gewinner'] != 'Unentschieden']['gewinner'].value_counts()
    wins = wins.reindex(total.index, fill_value=0).astype(int)
    
    # 3. Tabelle für die aktuelle Epoche bauen
    era_stats = pd.DataFrame({'Spiele': total, 'Siege': wins})
    era_stats['Siegquote_%'] = round((era_stats['Siege'] / era_stats['Spiele']) * 100, 2)
    
    # 4. Nur Teams mit einer Mindestanzahl an Spielen in dieser Epoche (z.B. mind. 30 Spiele)
    top_team_era = era_stats[era_stats['Spiele'] >= 30].sort_values(by='Siegquote_%', ascending=False).head(1)
    
    print(f"{era_name}:")
    print(top_team_era[['Spiele', 'Siegquote_%']], "\n" + "-"*40)


    df['gewinner'] = df.apply(get_gewinner, axis=1)