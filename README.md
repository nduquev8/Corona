# Corona Statistics Server

This little app is designed to clone/pull the latest [COVID-19](https://github.com/CSSEGISandData/COVID-19) data and generate dynamic plots.
The created html files are served via a simple flask app.

Requirements (linux):
 - git
 - cronie (crontab)
 - python3
   - jupyter notebook
   - pandas
   - cufflinks
   - flask

## Installation
Run the following commands as root.
```
su root
```

Clone this repository to your device.
```
mkdir /opt/corona
cd /opt/corona
git clone https://github.com/nduquev8/app_corona
```

Create a service managing the flask server. (start and enable)
```
ln -s /opt/corona/app_corona/corona.service /etc/systemd/system
systemctl daemon-reload
systemctl enable corona.service
systemctl start corona.service
```

Set sheduled data downloads and plot generation using cron.
Access the crontab:
```
crontab -e
```
Add this entry to the crontab (Eg.: updating every day at 10am and 10pm):

> 0 10,22 * * * /usr/bin/ipython /opt/corona/app_corona/generate_plots.py

Make sure the **cronie** service is active, if not enable and start it:
```
systemctl enable cronie.service
systemctl start cronie.service
```
