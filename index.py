
def generate_index():
    
    ### ADD FILES AND LINK TITLES FOR ES HERE
    file_to_es = {
        'all.html': 'Total',
        'raw.html': 'Total',
        'raws.html': 'Datos agregados',
        'norm.html': 'Proporcio&#769n',
        'norms.html': 'Datos agregados',
        'ratec.html': 'Tasa de crecimiento diario',
        'death.html': 'Total',
        'rated.html': 'Tasa de crecimiento diario'
    }
    ### ADD FILES AND LINK TITLES FOR ENG HERE
    file_to_en = {
        'all.html': 'Total',
        'raw.html': 'Total',
        'raws.html': 'Aggregated data',
        'norm.html': 'Portion',
        'norms.html': 'Aggregated data',
        'ratec.html': 'Daily growth rate',
        'death.html': 'Total',
        'rated.html': 'Daily growth rate'
    }
        
    hyperlink_format = '<u><a href="{link}" class="text-dark alert-link">{text}</a></u>'
    
    languages = [
        ### ADD TEXT FOR ES HERE
        """<title>Estadisticas COVID-19</title>
              </head>
              <body>
              
                <nav class="navbar navbar-light bg-light navbar-right">
                    <form class="form-inline my-2 my-lg-0">
                    </form>

                  <form class="form-inline my-2 my-lg-0">
                    <a class="btn btn-outline-success mr-sm-2" href="index_es.html" role="button">Español</a>
                    <a class="btn btn-outline-secondary my-2 my-sm-0" href="index_en.html" role="button">English</a>
                  </form>
                </nav>
              
                <div class="pt-5 container">

                    <h1>Estadi&#769sticas COVID-19</h1>
                    <br/>
                    <div class="alert alert-warning" role="alert">
                    <h4 class="alert-heading text-dark"><b>Contagios</b></h4>
                      <p>1. {} de contagios por pais.<br/>
                      2. {} de contagios en paises de intere&#769s. ({})<br/>
                      3. {} de contagios en paises de intere&#769s de acuerdo con la poblacio&#769n.({})<br/>
                      4. {} de contagios en paises de intere&#769s.<br/></p>
                      <br/>
                    </div>
                    <div class="alert alert-danger" role="alert">
                    <h4 class="alert-heading text-dark"><b>Muertes</b></h4>
                      <p>1. {} de muertes en paises de intere&#769s.<br/>
                      2. {} de muertes en paises de intere&#769s.<br/></p>

                    </div>
                </div>""".format(*[hyperlink_format.format(link=key, text=val) for key,val in file_to_es.items()]),
                
        ### ADD TEXT FOR ENG HERE
        """<title>COVID-19 Statistics</title>
              </head>
              <body>
              
                <nav class="navbar navbar-light bg-light navbar-right">
                    <form class="form-inline my-2 my-lg-0">
                    </form>

                  <form class="form-inline my-2 my-lg-0">
                    <a class="btn btn-outline-secondary mr-sm-2" href="index_es.html" role="button">Español</a>
                    <a class="btn btn-outline-success my-2 my-sm-0" href="index_en.html" role="button">English</a>
                  </form>
                </nav>
              
              
                <div class="pt-5 container">

                    <h1>COVID-19 Statistics</h1>
                    <br/>
                    <div class="alert alert-warning" role="alert">
                    <h4 class="alert-heading text-dark"><b>Confirmed Cases</b></h4>
                      <p>1. {} number of infections by country.<br/>
                      2. {} number of infections in countries of interest. ({})<br/>
                      3. {} of infections in countries of interest according to population.({})<br/>
                      4. {} of infections in countries of interest.<br/></p>
                      <br/>
                    </div>
                    <div class="alert alert-danger" role="alert">
                    <h4 class="alert-heading text-dark"><b>Deaths</b></h4>
                      <p>1. {} deaths in countries of interest.<br/>
                      2. {} of deaths in countries of interest.<br/></p>

                    </div>
                </div>""".format(*[hyperlink_format.format(link=key, text=val) for key,val in file_to_en.items()])
    ]

    index = []
    for language in languages:
        index.append(
            
            """
            <!doctype html>
            <html lang="en">
              <head>
                <!-- Required meta tags -->
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

                <!-- Bootstrap CSS -->
                <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">

                {}
                <!-- Optional JavaScript -->
                <!-- jQuery first, then Popper.js, then Bootstrap JS -->
                <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
                <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
                <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
              </body>
            </html>
            """.format(language)
        )



    # write html index file for es
    with open(r"app_corona/plots/index_es.html", "w") as file:
        file.write(index[0])
        
    # write html index file for eng
    with open(r"app_corona/plots/index_en.html", "w") as file:
        file.write(index[1])
