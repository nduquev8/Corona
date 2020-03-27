
def generate_index():
     
    hyperlink_format = '<a href="{link}" class="text-primary alert-link">{text}</a>'
    links = dict(
        all = hyperlink_format.format(link='all.html', text='Total'),
        raw = hyperlink_format.format(link='raw.html', text=' Total'),
        raws = hyperlink_format.format(link='raws.html', text=' Datos agregados')
        norm = hyperlink_format.format(link='norm.html', text=' Proporción'),
        norms = hyperlink_format.format(link='norms.html', text=' Datos agregados'),
        ratec = hyperlink_format.format(link='ratec.html', text=' Tasa de crecimiento diario')
        death = hyperlink_format.format(link='death.html', text=' Total'),
        rated = hyperlink_format.format(link='rated.html', text=' Tasa de crecimiento diario')
    )

    

    # HTML text 
    t = """
    <!doctype html>
    <html lang="en">
      <head>
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">

        <title>Estadisticas COVID-19</title>
      </head>
      <body>
        <div class="pt-5 container">

            <h1>Estadi&#769sticas COVID-19</h1>
            <div class="alert alert-light" role="alert">
            
            Contagios:
              1. {} de contagios por pais.<br/>
              2. {} de contagios en paises de intere&#769s. ({})<br/>
              3. {} de contagios en paises de intere&#769s de acuerdo con la poblacio&#769n.({})<br/>
              4. {} de contagios en paises de intere&#769s.
              
              
            Muertes:
              2. {} de muertes en paises de intere&#769s.({})<br/>
              4. {} de muertes en paises de intere&#769s.
              5. 
            </div>
        </div>
        <!-- Optional JavaScript -->
        <!-- jQuery first, then Popper.js, then Bootstrap JS -->
        <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
      </body>
    </html>
    """.format(*list(links.values()))


    # write html index file
    with open(r"plots/index.html", "w") as file:
        file.write(t)
