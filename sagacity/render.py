import json
from textwrap import dedent


# c.f view-source:https://www.chartjs.org/samples/latest/scales/time/line.html
TEMPLATE = dedent('''\
    <html>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.13.0/moment.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.6.0/Chart.min.js"></script>
    <body>
    <canvas id="canvas"></canvas>
    </body>
    <script>
    var timeFormat = 'MM/DD/YYYY HH:mm';
    function newDateString(days) {{
        return moment().add(days, 'd').format(timeFormat);
    }}
    var jsonfile = {{
        "jsonarray": {data}
    }};
    
    var data = jsonfile.jsonarray.map(function(e) {{
        return e.date;
    }});;
    
    var ctx = canvas.getContext('2d');
    var config = {{
        type: 'line',
        data: {{
            labels: [{labels}],
            datasets: [{{
                label: 'Graph Line',
                data: data,
                backgroundColor: 'rgba(0, 119, 204, 0.3)'
            }}]
        }},
        options: {{
            title: {{
                text: 'Commits Time Scale'
            }},
            scales: {{
                xAxes: [{{
                    type: 'time',
                    time: {{
                        parser: timeFormat,
                        // round: 'day'
                        tooltipFormat: 'll HH:mm'
                    }},
                    scaleLabel: {{
                        display: true,
                        labelString: 'Date'
                    }}
                }}],
                yAxes: [{{
                    scaleLabel: {{
                        display: true,
                        labelString: 'frequency'
                    }}
                }}]
            }},
        }}
    }};

    var chart = new Chart(ctx, config); 
    </script>
    </html>
''')


def chartjs(labels, data):
    return TEMPLATE.format(
        labels=",".join(labels),
        data=json.dumps(data, indent=4))
