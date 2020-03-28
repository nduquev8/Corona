import cufflinks as cf
from plotly.offline import init_notebook_mode
import plotly.graph_objects as go
import plotly.express as px
import os
import pandas as pd
from dropbox_api import update_on_dropbox
from index import generate_index
import matplotlib.pyplot as plt
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

confirmed_growth = confirmed_filtered.diff().iloc[1:,:]
all_growth = confirmed.diff().iloc[1:,:]
death_growth = death_filtered.diff().iloc[1:,:]

### normalizing data
confirmed_normed = pd.DataFrame()
for column in confirmed_filtered.columns:
    confirmed_normed[column] =confirmed_filtered[column].astype(float)/pop.loc[column][0]

confirmed_growth_max_norm = pd.DataFrame()
for col in confirmed_growth.columns:
    vals = confirmed_growth[col].values
    confirmed_growth_max_norm[col] = vals/vals.max()


### plotting
def color_gen(cm='YlOrRd',n=10):
    # https://matplotlib.org/tutorials/colors/colormaps.html
    colmap = plt.get_cmap(cm)
    colors = []
    for i in range(n):
        colors.append(
            "rgb("+",".join([str(int(255*u)) for u in colmap(i/(n-1))[:-1]])+")"
        )
    return colors

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
                       title="Daily Confirmed Cases",
                       filename = plot_folder+"/ratec",
                       asUrl=True)

death_growth.iplot(kind="bar", 
                   title="Daily Fatalities",
                   filename = plot_folder+"/rated",
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
colorscale = color_gen('YlOrRd',len(values))

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
    current = sum(y)
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
                   "<br>Mean: {:.2f} days, Standard Deviation: {:.2f} days<br>Current: {} people,"\
                   " Estimate: {} people".format(m,s,current,estimate))
    
    cf.iplot(figure=fig,
             asUrl=True, 
             filename=filename)
    return

for country in worst:
    plot_fit(all_growth[country],
             filename = plot_folder+"/{}_est".format(country))


         
### Generate index table of all the plots
generate_index()

         
### Pushing plots to dropbox
update_on_dropbox()
