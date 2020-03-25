import cufflinks as cf
from plotly.offline import init_notebook_mode
import os
import pandas as pd

cf.go_offline()
init_notebook_mode(connected=True)

### 
countries_to_track = [
    'Australia',
    'Austria',
    'Canada',
    'China',
    'Croatia',
    'Czechia',
    'Colombia',
    'France',
    'Germany',
    'India',
    'Italy',
    'Norway',
    'Spain',
    'Sweden',
    'Switzerland',
    'US',
    'United Kingdom'
]

###

homedir = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
os.chdir(homedir)
git_repo = os.path.join(homedir, "COVID-19")
if os.path.exists(git_repo):
    os.chdir(git_repo)
    os.system("git pull")
    os.chdir(homedir)
else:
    os.system("git clone https://github.com/CSSEGISandData/COVID-19")

if not os.path.exists("corona/plots"):
    os.mkdir("corona/plots")

_map = {"Cape Verde": "Cabo Verde",
        "Czech Republic": 'Czechia',
        "South Korea": "Korea, South",
        "Taiwan": "Taiwan*", 
        "United States": "US"}

pop = pd.read_csv("corona/population.csv")[["name","pop2019"]]
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

## check if country names are right
unknown = []
known = []
for country  in countries_to_track:
    if country not in df.columns:
        unknown.append(country)
    else:
        known.append(country)

### preparing filtered data
filtered = df[known]

### normalizing data
normed = pd.DataFrame()
for column in filtered.columns:
    normed[column] =filtered[column].astype(float)/pop.loc[column][0]


### plotting
df.iplot(kind="bar",
         barmode='stack',
         filename = "corona/plots/all", asUrl=True)

normed.iplot(kind="bar",
             barmode='stack',
             filename = "corona/plots/norm_stack", asUrl=True)

normed.iplot(kind="bar",
             filename = "corona/plots/norm", asUrl=True)

filtered.iplot(kind="bar",
               barmode='stack',
               filename = "corona/plots/raw_stack", 
               colorscale='dflt',
               asUrl=True)


countries = filtered.columns.tolist() # in case you want all countries as single plots
for country in countries:
    filtered[country].iplot(kind="bar",filename = "corona/plots/{}".format(country.replace(" ","_").lower()), asUrl=True)

