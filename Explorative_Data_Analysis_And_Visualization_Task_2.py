import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

# Read data from csv
url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
data = pd.read_csv(url)

data['date'] = pd.to_datetime(data['date'], errors='coerce')

# Prepare data for visualization
countries = ['Germany', 'France', 'Italy', 'Spain', 'United Kingdom', 'United States']
data_filtered = data[data['location'].isin(countries)].dropna(subset=['total_cases', \
                                                'total_deaths', 'total_vaccinations'])

# Normalized Bar Chart of cases per million
top_countries = data_filtered.nlargest(3, 'total_cases_per_million')
top_countries_locations = top_countries['location'].tolist()

# Barplot erstellen
plt.figure(figsize=(10, 6))
ax = sns.barplot(x='location', y='total_cases_per_million', data=data_filtered, palette='Blues_d')

# Top 3 Länder für Highlighten suchen
for i, patch in enumerate(ax.patches):
    # Hole den Ländernamen basierend auf der Reihenfolge des Barplots
    country = ax.get_xticklabels()[i].get_text()  # Name des Landes aus den xticklabels holen
    if country in top_countries_locations:
        patch.set_facecolor('red')  # Top 3 Länder rot einfärben

plt.title('COVID-19 cases per million population')
plt.xlabel('Country')
plt.ylabel('Cases per million')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("normalized_bar_chart_of_cases_per_million.png")
plt.show()

# Time Series Line Chart of cases progression
plt.figure(figsize=(10, 6))
for country in countries:
    country_data = data_filtered[data_filtered['location'] == country]
    plt.plot(country_data['date'], country_data['total_cases'], label=country)
plt.title('Development of COVID-19 cases over time')
plt.xlabel('Date')
plt.ylabel('Caese cumulated')
plt.legend(title='Country')
plt.xticks(rotation=45)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
plt.tight_layout()
plt.grid(True)
plt.savefig("time_series_line_chart_of_cases_progression.png")
plt.show()

# Scatterplot of vacciantion rates vs. deaths per million
plt.figure(figsize=(10, 6))
sns.scatterplot(x='people_vaccinated_per_hundred', y='total_deaths_per_million', \
                hue='location', data=data_filtered, palette='Set1', size='total_cases', \
                    sizes=(20,200))
plt.title('Vaccination rate vs. deaths per million inhabitants')
plt.xlabel('People vaccinated per 100 inhabitants (%)')
plt.ylabel('Deaths per million population')
plt.legend(handles=handles, labels=labels, title='Country',
           ncol=2,frameon=True)
plt.tight_layout()
plt.savefig("scatterplot_of_vaccination_rates_vs_deaths_per_million.png")
plt.show()

