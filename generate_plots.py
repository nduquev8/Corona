import cufflinks as cf
from plotly.offline import init_notebook_mode
import os
import pandas as pd
cf.go_offline()

init_notebook_mode(connected=True)

homedir = "/home/alarm/corona"
#homedir = "/home/christian/Downloads/"
os.chdir(homedir)
git_repo = os.path.join(homedir, "COVID-19")
if os.path.exists(git_repo):
    os.chdir(git_repo)
    os.system("git pull")
    os.chdir(homedir)
else:
    os.system("git clone https://github.com/CSSEGISandData/COVID-19")


_map = {"Cape Verde": "Cabo Verde",
        "Czech Republic": 'Czechia',
        "South Korea": "Korea, South",
        "Taiwan": "Taiwan*", 
        "United States": "US"}

pop = pd.read_csv("app/population.csv")[["name","pop2019"]]
pop.replace(_map,inplace=True)
pop.index = pop.name
del pop["name"]
pop.pop2019*=1000


confirmed_global = "COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
#confirmed2_global = "COVID-19/archived_data/archived_time_series/time_series_2019-ncov-Confirmed.csv"
df = pd.read_csv(confirmed_global)
df = df.groupby("Country/Region").sum()
df.drop(labels=["Lat", "Long"],axis=1, inplace= True)
df = df.transpose()
df.index = pd.to_datetime(df.index, format="%m/%d/%y")

_exclude = ['Congo (Brazzaville)', 
            'Congo (Kinshasa)', 
            "Cote d'Ivoire", 
            'Cruise Ship',
            'Eswatini', 
            "Holy See",
            'North Macedonia']

df.drop(labels=_exclude, axis=1, inplace=True)

# Normalized data
normed = pd.DataFrame()
for column in df.columns:
    normed[column] =df[column].astype(float)/pop.loc[column][0]

def gen_plots(df, name):
    df.iplot(kind="bar",filename = "app/plots/{}".format(name), asUrl=True)
    countries = ["Colombia", "Germany", "Italy", "Switzerland", "US"]
    # countries = df.columns.tolist() # in case you want all countries as single plots
    for country in countries:
        df[country].iplot(fill=True, filename = "app/plots/{}_{}".format(country.replace(" ","_").lower(), name), asUrl=True)

        

gen_plots(df, "raw")
gen_plots(normed, "norm")
