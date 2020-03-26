import cufflinks as cf
from plotly.offline import init_notebook_mode
import plotly.graph_objects as go
import os
import pandas as pd
from dropbox_api import update_on_dropbox

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

other = list(set(confirmed.columns) - set(known))
        
### preparing filtered data
confirmed_filtered = confirmed[known]
death_filtered = death[known]

cfrm = confirmed_filtered.iloc[-1,:]
dths = death_filtered.iloc[-1,:]
con_dea = pd.DataFrame(data={"confirmed": cfrm, "dead": dths}).transpose()

confirmed_growth = confirmed_filtered.diff()
death_growth = death_filtered.diff()

### normalizing data
confirmed_normed = pd.DataFrame()
for column in confirmed_filtered.columns:
    confirmed_normed[column] =confirmed_filtered[column].astype(float)/pop.loc[column][0]

### plotting
plot_folder = "app_corona/plots"
os.system("rm {}/*".format(plot_folder)) 

confirmed.iplot(kind="bar",
                barmode='stack',
                filename = plot_folder+"/all",
                title="Globally Confirmed Cases",
                asUrl=True)

confirmed_normed.iplot(kind="bar",
                       barmode='stack',
                       filename = plot_folder+"/norms",
                       title="Confirmed Cases Normed",
                       asUrl=True)

confirmed_normed.iplot(kind="bar",
                       filename = plot_folder+"/norm",
                       title="Confirmed Cases Normed",
                       asUrl=True)

confirmed_filtered.iplot(kind="bar",
                         barmode='stack',
                         title="Confirmed Cases",
                         filename = plot_folder+"/raws", 
                         asUrl=True)

confirmed_filtered.iplot(kind="bar",
                         filename = plot_folder+"/raw",
                         title="Confirmed Cases",
                         asUrl=True)

confirmed_growth.iplot(kind="bar", 
                       title="Growth Rate",
                       filename = plot_folder+"/ratec",
                       asUrl=True)

death_growth.iplot(kind="bar", 
                   title="Death Rate",
                   filename = plot_folder+"/rated",
                   asUrl=True)

confirmed_growth.iplot(kind="heatmap", 
                   title="Growth Rate",
                   filename = plot_folder+"/ratec_heatmap",
                   colorscale="reds")

### pie chart
confirmed_other = confirmed[other].iloc[-1,:].sum()
death_other = death[other].iloc[-1,:].sum()

labels = con_dea.columns.tolist()+["Other"]
total = (con_dea.loc["dead",:]).tolist()+[death_other]
rel_deaths = (con_dea.loc["dead",:] * 100 / con_dea.loc["confirmed",:]).tolist()+[death_other*100/confirmed_other]
labels = ["{}: {} \n death rate {:.2f}%".format(l, td, rel) for l, td, rel in zip(labels, total, rel_deaths)]
values = con_dea.loc["dead", :].tolist() + [death_other]


fig = go.Figure()
fig.add_trace(
    go.Pie(labels=labels, 
           values=values,
           
           textinfo='label', 
           hole=.3,))


fig.update_layout(showlegend=False, 
                  title="Global Deaths",
                  # Add annotations in the center of the donut pies.
                  annotations=(text=str(sum(total)), x=0, y=0, font_size=20, showarrow=False))
cf.iplot(figure=fig,
         filename=plot_folder+"/death", 
         asUrl=True)


         
### Pushing plots to dropbox
update_on_dropbox()