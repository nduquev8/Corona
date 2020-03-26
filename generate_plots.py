import cufflinks as cf
from plotly.offline import init_notebook_mode
import plotly.graph_objects as go
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

if not os.path.exists("app_corona/plots"):
    os.mkdir("app_corona/plots")

_map = {"Cape Verde": "Cabo Verde",
        "Czech Republic": 'Czechia',
        "South Korea": "Korea, South",
        "Taiwan": "Taiwan*", 
        "United States": "US"}

pop = pd.read_csv("app_corona/population.csv")[["name","pop2019"]]
pop.replace(_map,inplace=True)
pop.index = pop.name
del pop["name"]
pop.pop2019*=1000


confirmed_global = "COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
death_global = "COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"

def parse_time_series(path):
    df = pd.read_csv(path)
    df = df.groupby("Country/Region").sum()
    df.drop(labels=["Lat", "Long"],axis=1, inplace= True)
    df = df.transpose()
    df.index = pd.to_datetime(df.index, format="%m/%d/%y")
    return df

confirmed = parse_time_series(confirmed_global)
death = parse_time_series(death_global)


## check if country names are right
unknown = []
known = []
for country  in countries_to_track:
    if country not in confirmed.columns:
        unknown.append(country)
    else:
        known.append(country)

### preparing filtered data
confirmed_filtered = confirmed[known]
death_filtered = death[known]

cfrm = confirmed_filtered.iloc[-1,:]
dths = death_filtered.iloc[-1,:]
con_dea = pd.DataFrame(data={"confirmed": cfrm, "dead": dths}).transpose()


### normalizing data
confirmed_normed = pd.DataFrame()
for column in confirmed_filtered.columns:
    confirmed_normed[column] =confirmed_filtered[column].astype(float)/pop.loc[column][0]

### plotting
plot_folder = "app_corona/plots"

confirmed.iplot(kind="bar",
                barmode='stack',
                filename = plot_folder+"/all", asUrl=True)

confirmed_normed.iplot(kind="bar",
                       barmode='stack',
                       filename = plot_folder+"/ns", asUrl=True)

confirmed_normed.iplot(kind="bar",
                       filename = plot_folder+"/n", asUrl=True)

confirmed_filtered.iplot(kind="bar",
                         barmode='stack',
                         filename = plot_folder+"/rs", 
                         colorscale='dflt',
                         asUrl=True)

confirmed_filtered.iplot(kind="bar",
                         filename = plot_folder+"/r",
                         asUrl=True)

### pie chart
labels = con_dea.columns.tolist()
total_deaths = con_dea.loc["dead", :].tolist()
labels = ["{}: {}".format(l, td) for l, td in zip(labels, total_deaths)]
values = (con_dea.loc["dead",:] / con_dea.loc["confirmed",:]).tolist()

fig = go.Figure()
fig.add_trace(
    go.Pie(labels=labels, 
           values=values,
           textinfo='label', 
           hole=.3,))

fig.update_layout(showlegend=False)
cf.iplot(figure=fig,
         filename=plot_folder+"/pie", 
         asUrl=True,)
