import os
def add_navbar_to_plots(folder="plots"):
    
    header="""
    <head>
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
    </head>
    """
    
    navbar = """
    <nav class="navbar navbar-light bg-light navbar-right">
        <a class="navbar-brand" href="#">Corona Statistics</a>

        <form class="form-inline my-2 my-lg-0">
          <a class="btn btn-outline-secondary mr-sm-2" href="index_es.html" role="button">Inicio</a>
          <a class="btn btn-outline-secondary my-2 my-sm-0" href="index.html" role="button">Home</a>
        </form>
    </nav>
    """
    
    footer = """
    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
    """
    
    head = '<html>\n<head><meta charset="utf-8" /></head>\n<body>\n    <div>\n'
    head_new = '<html>\n{}\n<body>\n{}\n    <div>\n'.format(header, navbar)

    foot = '</div>\n</body>\n</html>'
    foot_new = '</div>\n{}\n</body>\n</html>'.format(footer)
    
    htmls = os.listdir(folder)
    
    for html in htmls:
        if not html.startswith("index"):
            with open(os.path.join(folder,html)) as f:
                content = f.read()
            
            content = content.replace(head, head_new)
            content = content.replace(foot, foot_new)
            
            with open(os.path.join(folder,html),"w") as f:
                f.write(content)
    
def link(name, ref):
     return '<u><a href="{ref}" class="text-dark alert-link">{name}</a></u>'.format(**locals())
 
def entry(text, **links):
    return text.format(**links)+"<br/>"

def alert(typ, title, entries):
    """
    typ like on https://getbootstrap.com/docs/4.4/components/alerts/
    eg.:
        info
        warning
        danger
        success
        ...
    """
    
    alert="""
    <div class="alert alert-{typ}" role="alert">
    <h4 class="alert-heading text-dark"><b>{title}</b></h4>
      <p>
      {entry_section}
      </p>
    </div>
    """.format(typ=typ,
               title=title, 
               entry_section="\n".join(entries))
    return alert

def page(title, alerts):
    alert_section = "\n".join(alerts)
    page="""
    <!doctype html>
    <html lang="en">
      <head>
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">

      <title>{title}</title>
      </head>
      <body>

        <nav class="navbar navbar-light bg-light navbar-right">
        <a class="navbar-brand" href="#">Corona Statistics</a>
            <form class="form-inline my-2 my-lg-0">
            </form>

          <form class="form-inline my-2 my-lg-0">
            <a class="btn btn-outline-secondary mr-sm-2" href="index_es.html" role="button">Espa&ntildeol</a>
            <a class="btn btn-outline-success my-2 my-sm-0" href="index.html" role="button">English</a>
          </form>
        </nav>
                
        <div class="pt-5 container">

        <h1>{title}</h1>
        <br/>
        {alert_section}
        
        </div>
        <!-- Optional JavaScript -->
        <!-- jQuery first, then Popper.js, then Bootstrap JS -->
        <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
      </body>
    </html>
    """.format(title=title, alert_section=alert_section)
    return page

def save_page(page, path):
    with open(path,"w") as html:
        html.write(page)

def generate_index():
    
    ### SPANISH
    l1 = link('Total', 'all.html')
    l2 = link('Total', 'raw.html')
    l3 = link('Datos agregados', 'raws.html')
    l4 = link('Proporcio&#769n', 'norm.html')
    l5 = link('Datos agregados', 'norms.html')
    l6 = link('Crecimiento diario', 'ratec.html')
    l7 = link('Mapa de calor normalizado', 'ratec_heatmap.html')
    l8 = link('Total', 'death.html')
    l9 = link('Crecimiento diario', 'rated.html')
    l10 = link('Comparacio&#769n','course.html')
    
    links_est = {}
    for f in os.listdir("plots"):
        if f.endswith("_est.html"):
            name = f[:-9]
            links_est[name]=link(name, f)
    estimate = "{" + "}, {".join(links_est.keys()) + "}"
    estimate = "Revisa estas estimaciones."\
               " Las curvas gaussianas se ajustaron para " + estimate + "."
    
    
    e1 = entry("1. {link} de contagios por pais.", 
               link=l1)
    e2 = entry("2. {link1} de contagios en paises de intere&#769s. ({link2})", 
               link1=l2, link2=l3)
    e3 = entry("3. {link1} de contagios en paises de intere&#769s de acuerdo con la poblacio&#769n.({link2})", 
               link1=l4, link2=l5)
    e4 = entry("4. {link1} de contagios en paises de intere&#769s.({link2})", 
               link1=l6, link2=l7)
    e5 = entry("1. {link1} de muertes en paises de intere&#769s.", 
               link1=l8)
    e6 = entry("2. {link1} de muertes en paises de intere&#769s.", 
               link1=l9)
    e7 = entry(estimate, 
               **links_est)
    e8 = entry("1. {link1} de los casos activos, recuperados y mortales del virus.", 
               link1=l10)
    
    a0 = alert("success", "Recuperar", 
               [e8])
    a1 = alert("warning", "Contagios", 
               [e1, e2, e3, e4])
    a2 = alert("danger", "Muertes", 
               [e5, e6])
    a3 = alert("info", "Extrapolacio&#769n",
               [e7])

    p_es = page("Estadi&#769sticas COVID-19", 
                [a0, a1, a2, a3])

    save_page(p_es, "plots/index_es.html")

    ### ENGLISH
    l1 = link('Total', 'all.html')
    l2 = link('Total', 'raw.html')
    l3 = link('Aggregated data', 'raws.html')
    l4 = link('Portion', 'norm.html')
    l5 = link('Aggregated data', 'norms.html')
    l6 = link('Daily growth', 'ratec.html')
    l7 = link('Normalized heat map', 'ratec_heatmap.html')
    l8 = link('Total', 'death.html')
    l9 = link('Daily growth', 'rated.html')
    l10 = link('Comparison','course.html')
    
    links_est = {}
    for f in os.listdir("plots"):
        if f.endswith("_est.html"):
            name = f[:-9]
            links_est[name]=link(name, f)
    estimate = "{" + "}, {".join(links_est.keys()) + "}"
    estimate = "Check out these estimates."\
               " Gaussian curves were fitted for " + estimate + "."
    
    
    e1 = entry("1. {link1} number of infections by country.", 
               link1=l1)
    e2 = entry("2. {link1} number of infections in countries of interest. ({link2})", 
               link1=l2, link2=l3)
    e3 = entry("3. {link1} of infections in countries of interest according to population.({link2})", 
               link1=l4, link2=l5)
    e4 = entry("4. {link1} of infections in countries of interest.({link2})", 
               link1=l6, link2=l7)
    e5 = entry("1. {link1} deaths in countries of interest.", 
               link1=l8)
    e6 = entry("2. {link1} of deaths in countries of interest.", 
               link1=l9)
    e7  =entry(estimate, 
               **links_est)
    e8 = entry("1. {link1} of the active, recovered and fatal cases of the virus.", 
               link1=l10)
    
    a0 = alert("success", "Recovered", 
               [e8])
    a1=alert("warning", "Confirmed", 
             [e1, e2, e3, e4])
    a2=alert("danger", "Deaths", 
             [e5, e6])
    a3=alert("info", "Extrapolation",
             [e7])

    p_en=page("COVID-19 Statistics", 
           [a0, a1, a2, a3])

    save_page(p_en, "plots/index.html")
    
    
    add_navbar_to_plots()

