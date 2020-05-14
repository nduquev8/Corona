import cufflinks as cf
from plotly.offline import init_notebook_mode
import plotly.graph_objects as go
import plotly.express as px
import os
import pandas as pd
import numpy as np
from dropbox_api import update_on_dropbox
from index import generate_index
from gauss import Gauss

cf.go_offline()
init_notebook_mode(connected=True)

### 
countries_to_track = [
    'Australia',
    'Austria',
    'China',
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
    'United Kingdom',
    'Brazil'
]

states_to_track = ['Illinois']

###

homedir = os.path.dirname(os.path.realpath(__file__))
os.chdir(homedir)
git_repo = os.path.join(homedir, "..","COVID-19")
if os.path.exists(git_repo):
    os.chdir(git_repo)
    os.system("git pull")
    os.chdir(homedir)
else:
    os.chdir(os.path.join(homedir, ".."))
    os.system("git clone https://github.com/CSSEGISandData/COVID-19")
    os.chdir(homedir)

if not os.path.exists("plots"):
    os.mkdir("plots")

_map = {"Cape Verde": "Cabo Verde",
        "Czech Republic": 'Czechia',
        "South Korea": "Korea, South",
        "Taiwan": "Taiwan*", 
        "United States": "US"}

pop = pd.read_csv("population.csv")[["name","pop2019"]]
pop.replace(_map,inplace=True)
pop.index = pop.name
del pop["name"]
pop.pop2019*=1000


recovered_global = "../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
confirmed_global = "../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
death_global = "../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
confirmed_US_series = "../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
deaths_US_series = "../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"


def parse_time_series(path):
    df = pd.read_csv(path)
    df = df.groupby("Country/Region").sum()
    df.drop(labels=["Lat", "Long"],axis=1, inplace= True)
    df = df.transpose()
    df.index = pd.to_datetime(df.index, format="%m/%d/%y")
    return df

recovered = parse_time_series(recovered_global)
confirmed = parse_time_series(confirmed_global)
death = parse_time_series(death_global)


def parse_time_series_states(path):
    labels=["UID","code3","FIPS","Lat", "Long_", "Population"]
    df = pd.read_csv(path)
    df = df.groupby("Province_State").sum()
    for l in labels:
        if l in df.columns:
            df.drop(labels=l,axis=1, inplace= True)
    df = df.transpose()
    df.index = pd.to_datetime(df.index, format="%m/%d/%y")
    return df

confirmed_US = parse_time_series_states(confirmed_US_series)
deaths_US = parse_time_series_states(deaths_US_series)

## check if country names are right
unknown = []
known = []
for country  in countries_to_track:
    if country not in confirmed.columns:
        unknown.append(country)
    else:
        known.append(country)

other = list(set(confirmed.columns) - set(known))

## check if ### US state names are right
unknown_US = []
known_US = []
for state  in states_to_track:
    if state not in confirmed_US.columns:
        unknown_US.append(state)
    else:
        known_US.append(state)

other = list(set(confirmed_US.columns) - set(known_US))
        
### preparing filtered data
### Global
confirmed_filtered = confirmed[known]
death_filtered = death[known]

cfrm = confirmed_filtered.iloc[-1,:]
dths = death_filtered.iloc[-1,:]
con_dea = pd.DataFrame(data={"confirmed": cfrm, "dead": dths}).transpose()

confirmed_growth = confirmed_filtered.diff().iloc[1:,:]
all_growth = confirmed.diff().iloc[1:,:]
death_growth = death_filtered.diff().iloc[1:,:]

### US
confirmed_filtered_US = confirmed_US[known_US]
death_filtered_US = deaths_US[known_US]

cfrm_us = confirmed_filtered_US.iloc[-1,:]
dths_us = death_filtered_US.iloc[-1,:]
con_dea_us = pd.DataFrame(data={"confirmed_US": cfrm_us, "dead_US": dths_us}).transpose()

confirmed_growth_us = confirmed_filtered_US.diff().iloc[1:,:]
all_growth_us = confirmed_US.diff().iloc[1:,:]
death_growth_us = death_filtered_US.diff().iloc[1:,:]


### normalizing data
confirmed_normed = pd.DataFrame()
for column in confirmed_filtered.columns:
    confirmed_normed[column] =confirmed_filtered[column].astype(float)/pop.loc[column][0]

confirmed_growth_max_norm = pd.DataFrame()
for col in confirmed_growth.columns:
    vals = confirmed_growth[col].values
    confirmed_growth_max_norm[col] = vals/vals.max()

rec = recovered.T.iloc[:,-1]
rec.name = "Recovered"
dea = death.T.iloc[:,-1]
dea.name = "Deceased"
con = confirmed.T.iloc[:,-1]
unk = con - dea - rec
unk.name = "Active"
rec_dea_unk = pd.concat([rec,dea,unk], axis=1)


### plotting
with open("colors") as colors:
    palette = [line.strip("\n") for line in colors if line != "\n"]

plot_folder = "plots"
os.system("rm {}/*".format(plot_folder)) 

confirmed.iplot(kind="bar",
                barmode='stack',
                filename = plot_folder+"/all",
                title="Globally Confirmed Cases",
                yTitle="Capita [-]",
                colors=palette,
                asUrl=True)

confirmed_normed.iplot(kind="bar",
                       barmode='stack',
                       filename = plot_folder+"/norms",
                       title="Confirmed Cases Normed",
                       yTitle="Capita/Population [-]",
                       colors=palette,
                       asUrl=True)

confirmed_normed.iplot(kind="bar",
                       filename = plot_folder+"/norm",
                       title="Confirmed Cases Normed",
                       yTitle="Capita/Population [-]",
                       colors=palette,
                       asUrl=True)

confirmed_filtered.iplot(kind="bar",
                         barmode='stack',
                         title="Confirmed Cases",
                         yTitle="Capita [-]",
                         filename = plot_folder+"/raws", 
                         colors=palette,
                         asUrl=True)

confirmed_filtered.iplot(kind="bar",
                         filename = plot_folder+"/raw",
                         title="Confirmed Cases",
                         yTitle="Capita [-]",
                         colors=palette,
                         asUrl=True)

confirmed_growth.iplot(kind="bar", 
                       title="Daily Confirmed Cases",
                       filename = plot_folder+"/ratec",
                       yTitle="Capita [-]",
                       colors=palette,
                       asUrl=True)

death_growth.iplot(kind="bar", 
                   title="Daily Fatalities",
                   filename = plot_folder+"/rated",
                   yTitle="Capita [-]",
                   colors=palette,
                   asUrl=True)

confirmed_growth_max_norm.iplot(kind="heatmap", 
                   title="Trend Daily Confirmed Cases",
                   filename = plot_folder+"/ratec_heatmap",
                   colorscale="reds",
                   asUrl=True)

### pie chart
worst=death.iloc[-1,:].sort_values(ascending=False).head(5)

our_countries = ["Colombia", "Germany", "Switzerland", "US"]

for c in our_countries:
    if not c in worst.keys():

        worst[c]=death[c].iloc[-1]
worst=pd.DataFrame(worst).transpose()

other = list(set(death.columns) - set(worst.columns))

confirmed_other = confirmed[other].iloc[-1,:].sum()
death_other = death[other].iloc[-1,:].sum()

labels = worst.columns.tolist()+["Other"]
total = worst.iloc[-1,:].tolist()+[death_other]
total_deaths ="Total deaths: <br> {}".format(sum(total))
total_deaths

rel_deaths = (worst.iloc[-1,:] * 100 / confirmed[worst.columns.tolist()].iloc[-1,:]).tolist()+[death_other*100/confirmed_other]

labels = ["{}: {} <br> death rate {:.2f}%".format(l, td, rel) for l, td, rel in zip(labels, total, rel_deaths)]
values = total

vs = sorted(zip(values, labels), key=lambda x: x[0], )
values, labels = list(zip(*vs))
colorscale = [
    'rgb(255,255,204)',
    'rgb(255,239,165)',
    'rgb(254,221,128)',
    'rgb(254,191,90)',
    'rgb(253,157,67)',
    'rgb(252,112,51)',
    'rgb(243,60,37)',
    'rgb(217,19,30)',
    'rgb(181,0,38)',
    'rgb(128,0,38)'
]

fig = go.Figure()

fig.add_trace(go.Pie(labels=labels,
                     values=values,
                     textinfo='label',
                     #textfont=dict(size=20),
                     marker=dict(colors=colorscale),
                     hole=.3,))

fig.update_layout(autosize=True,
                  showlegend=True, 
                  legend  = dict(font=dict(
                                 family='sans-serif',
                                 #size=20,
                                 color='#000'),),
                  title=dict(text="Global Fatalities", 
                             font=(dict(#size=40,
                                        color='#000'))),
                  # Add annotations in the center of the donut pies.
                  annotations=[dict(text=total_deaths, 
                                    align = "center", showarrow=False)])

cf.iplot(figure=fig,
         filename=plot_folder+"/death", 
         asUrl=True)


def plot_fit(series, filename):
    y=series.tolist()
    x = np.array(range(len(y)))
    gauss = Gauss(x,y)
    y_pred = gauss.fit()
    fit_series = pd.Series(y_pred, series.index, name="Fitted Curve")
    
    _,m,s = gauss.par
    current = int(sum(y))
    estimate = gauss.estimate_total()
    
    fig1 = series.iplot(kind="bar",asFigure=True)
    fig2 = fit_series.iplot(asFigure=True,
                            colors=['blue'],
                            width=2,
                            dash="dashdot")

    fig = cf.tools.merge_figures([fig1, fig2])
    fig = go.Figure(fig)
    fig.update_layout(
        title_text="Total Infection Estimate<br>-------------------------------"\
                   "<br>Current: {} people,"\
                   " Estimate: {} people".format(current,estimate),
        yaxis_title="Capita [-]")
    
    cf.iplot(figure=fig,
             asUrl=True, 
             filename=filename)
    return

for country in worst:
    plot_fit(all_growth[country],
             filename = plot_folder+"/{}_est".format(country))

for state in states_to_track:
    plot_fit(all_growth_us[state],
             filename = plot_folder+"/{}_est".format(state))

rec_dea_unk.loc[countries_to_track].iplot(
    kind="bar", 
    barmode="stack", 
    colors=["green", "red", "gray"],
    title="Course of the Infection",
    filename = plot_folder+"/course",
    yTitle="Capita [-]",
    asUrl=True
)

         
### Generate index table of all the plots
generate_index()

         
### Pushing plots to dropbox
update_on_dropbox()

for file in os.listdir("plots"):
    if os.path.exists("/srv/http/"):
        os.rename("plots/"+file, "/srv/http/"+file)
