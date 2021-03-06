
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

app = Dash(__name__, external_stylesheets=[dbc.themes.GRID])
server = app.server
app.title = "Strike Take Home Pay Calculator"

app.layout = html.Div([

    html.Br(),html.Br(),html.Br(),

    dbc.Row(
        [
            dbc.Col(
                html.Div('Annual salary before deductions (£)'),
                width=2
            ),
            dbc.Col(
                html.Div(dcc.Input(id="annual_salary", value='30497', type='number')),
                width=2
            ),
            dbc.Col(
                html.Div('Enter your annual, pre-tax salary here')
            ),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(
                html.Div('USS (%)'),
                width=2
            ),
            dbc.Col(
                html.Div(dcc.Input(id="USS", value='9.8', type='number')),
                width=2
            ),
            dbc.Col(
                html.Div('If you are not a member of USS, set this to zero')
            ),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(
                html.Div('Tax free allowance (£)'),
                width=2
            ),
            dbc.Col(
                html.Div(dcc.Input(id="annual_tax_free", value='12570', type='number')),
                width=2
            ),
            dbc.Col(
                html.Div('This information comes from your tax code, which is on your payslip')
            ),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(
                html.Div('Number of strike days'),
                width=2
            ),
            dbc.Col(
                html.Div(dcc.Input(id="n_strike_days", value='10', type='number')),
            ),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(
                html.Div('Fraction of annual pay deducted per day'),
                width=2
            ),
            dbc.Col(
                html.Div(dcc.RadioItems(
                    ['1/365', '1/260'], 
                    '1/365',
                    id="frac_deduction",
                ))
            ),
        ]
    ),
  
    html.Br(),html.Br(),html.Br(),
    
    dbc.Row(
        [
            dbc.Col(
                html.Div(""),
                width=2
            ),
            dbc.Col(
                html.Div("Normal Month (no strikes)"),
                width=2
            ),
            dbc.Col(
                html.Div("With strike days"),
                width=2
            ),
            dbc.Col(
                html.Div("Amount forgone"),
                width=2
            )
        ]
    ),

    html.Br(),
    
    dbc.Row(
        [
            dbc.Col(
                html.Div("Monthly Salary"),
                width=2
            ),
            dbc.Col(
                html.Div(id="mnthly_slry"),
                width=2
            ),
            dbc.Col(
                html.Div(id="deduct_mnthly_slry"),
                width=2
            ),
            dbc.Col(
                html.Div(id="forgone_mnthly_slry"),
                width=2
            )
        ]
    ),
    
    dbc.Row(
        [
            dbc.Col(
                html.Div("Monthly Tax"),
                width=2
            ),
            dbc.Col(
                html.Div(id="mnthly_tax"),
                width=2
            ),
            dbc.Col(
                html.Div(id="deduct_mnthly_tax"),
                width=2
            ),
            dbc.Col(
                html.Div(id="forgone_mnthly_tax"),
                width=2
            )
        ]
    ),
    
    dbc.Row(
        [
            dbc.Col(
                html.Div("Monthly National Insurance"),
                width=2
            ),
            dbc.Col(
                html.Div(id="mnthly_NI"),
                width=2
            ),
            dbc.Col(
                html.Div(id="deduct_mnthly_NI"),
                width=2
            ),
            dbc.Col(
                html.Div(id="forgone_NI"),
                width=2
            )
        ]
    ),
    
    html.Br(),
    
    dbc.Row(
        [
            dbc.Col(
                html.Div("Monthly Take Home Pay"),
                width=2
            ),
            dbc.Col(
                html.Div(id="mnthly_take_home"),
                width=2
            ),
            dbc.Col(
                html.Div(id="deduct_mnthly_take_home"),
                width=2
            ),
            dbc.Col(
                html.Div(id="forgone_take_home"),
                width=2
            )
        ]
    ),
    
    html.Br(),html.Br(),
    
    dbc.Row([
        dbc.Col([
            html.H4('Normal month'), 
            dcc.Graph(id="pay_pie")], 
        width=4),
        dbc.Col([
            html.H4('Month with strike deductions'),
            dcc.Graph(id="pay_pie_deduct")],
        width=4),
    ]),
    
    html.Br(),html.Br(),
    dbc.Row(html.Div("Notes:")), html.Br(),
    dbc.Row(
        html.Div(children=[
        """This is only an estimate of take home pay, and personal financial arrangements will 
        affect the pay you receive following deductions. 
        The additional rate of tax, above £150,000 per year, is not included in this calculation.
        Note that tax rates in Scotland are different to rates in other UK nations.
        Other deductions like car parking, student loan etc are also not included.
        Source code is available to view 
        """
        , html.A("here.", href="https://github.com/jim-rafferty/strike_take_home_pay_calculator"),
        """
        If you have any improvements to this tool, please send me a pull request on github and I will
        be happy to incorporate them. Please send questions and comments to """,
        html.A("j.m.rafferty@swansea.ac.uk", href="mailto:j.m.rafferty@swansea.ac.uk"),
        ],
        style={'fontSize': 12}
        )   
    ),
    
    
])


def safe_convert(str_in, dtype=float):
    """
    Takes a string and returns a number. If the string is None
    0 in the correct type is returned.
    
    No checks are currently done for non numeric characters.
    """

    if str_in is None:
        return dtype(0)
    return dtype(str_in)

@app.callback(
    Output("pay_pie", "figure"), 
    Input(component_id='mnthly_take_home', component_property='children'),
    Input(component_id='USS', component_property='value'),
    Input(component_id='mnthly_tax', component_property='children'),
    Input(component_id='mnthly_NI', component_property='children'),
    Input(component_id='annual_salary', component_property='value'),
    Input(component_id='USS', component_property='value')
)
def generate_chart_noStrike(pay_in, USS_in, tax_in, ni_in, annual_pay_in, uss_in):
    
    pay = safe_convert(pay_in.replace("£", ""))
    tax = safe_convert(tax_in.replace("£", ""))
    ni = safe_convert(ni_in.replace("£", ""))
    uss = safe_convert(uss_in)
    annual_pay = safe_convert(annual_pay_in)
    
    df = {
        "Labels": ["Take home pay", "USS", "Tax", "NI"],
        "Values": [pay, uss / 100 * annual_pay / 12, tax, ni],
    }
    
    fig = px.pie(df, values="Values", names="Labels")
    return fig
    
@app.callback(
    Output("pay_pie_deduct", "figure"), 
    Input(component_id='deduct_mnthly_take_home', component_property='children'),
    Input(component_id='USS', component_property='value'),
    Input(component_id='deduct_mnthly_tax', component_property='children'),
    Input(component_id='deduct_mnthly_NI', component_property='children'),
    Input(component_id='annual_salary', component_property='value'),
    Input(component_id='USS', component_property='value')
)
def generate_chart_strike(pay_in, USS_in, tax_in, ni_in, annual_pay_in, uss_in):
    
    pay = safe_convert(pay_in.replace("£", ""))
    tax = safe_convert(tax_in.replace("£", ""))
    ni = safe_convert(ni_in.replace("£", ""))
    uss = safe_convert(uss_in)
    annual_pay = safe_convert(annual_pay_in)
    
    df = {
        "Labels": ["Take home pay", "USS", "Tax", "NI"],
        "Values": [pay, uss / 100 * annual_pay / 12, tax, ni],
    }
    
    fig = px.pie(df, values="Values", names="Labels")
    return fig

@app.callback(
    Output(component_id='mnthly_slry', component_property='children'),
    Input(component_id='annual_salary', component_property='value')
)
def pretax_mnthly_slry(sal_in):

    sal = safe_convert(sal_in)/12
    return "£{:.2f}".format(sal)


@app.callback(
    Output(component_id='deduct_mnthly_slry', component_property='children'),
    Input(component_id='annual_salary', component_property='value'),
    Input(component_id='frac_deduction', component_property='value'),
    Input(component_id='n_strike_days', component_property='value'),
)
def deduct_pretax_mnthly_slry(sal_in, frac_in, n_strike_days):
    if frac_in == "1/365":
        frac = 1/365
    elif frac_in == "1/260":
        frac = 1/260
        
    sal = safe_convert(sal_in)/12
    return "£{:.2f}".format(sal - 12 * frac * safe_convert(n_strike_days) * sal)
    
@app.callback(
    Output(component_id='forgone_mnthly_slry', component_property='children'),
    Input(component_id='annual_salary', component_property='value'),
    Input(component_id='frac_deduction', component_property='value'),
    Input(component_id='n_strike_days', component_property='value'),
)
def forgone_mnthly_slry(sal_in, frac_in, n_strike_days):
    if frac_in == "1/365":
        frac = 1/365
    elif frac_in == "1/260":
        frac = 1/260

    sal = safe_convert(sal_in)        
    return "£{:.2f}".format((frac * safe_convert(n_strike_days) * sal))    


@app.callback(
    Output(component_id='mnthly_tax', component_property='children'),
    Input(component_id='annual_salary', component_property='value'),
    Input(component_id='USS', component_property='value'),
    Input(component_id='annual_tax_free', component_property='value')
)
def mnthly_tax(sal_in, uss_in, tax_free_in):

    uss = 1 - safe_convert(uss_in) / 100
    sal = uss * safe_convert(sal_in)/12
    tax_free = safe_convert(tax_free_in)/12
    
    tax = max([0, 0.2 * (sal - tax_free) + 0.2 * max([0, sal - 3141.75])]) # 2021: 4189.25

    return "£{:.2f}".format(tax)

@app.callback(
    Output(component_id='deduct_mnthly_tax', component_property='children'),
    Input(component_id='annual_salary', component_property='value'),
    Input(component_id='USS', component_property='value'),
    Input(component_id='annual_tax_free', component_property='value'),
    Input(component_id='frac_deduction', component_property='value'),
    Input(component_id='n_strike_days', component_property='value'),
    
)
def mnthly_tax_deduct(sal_in, uss_in, tax_free_in, frac_in, n_days_in):

    if frac_in == "1/365":
        frac = 1/365
    elif frac_in == "1/260":
        frac = 1/260
    n_days = safe_convert(n_days_in)
    uss = 1 - safe_convert(uss_in) / 100

    sal = uss * safe_convert(sal_in)/12 - safe_convert(sal_in) * n_days * frac 
    tax_free = safe_convert(tax_free_in)/12
    
    
    tax = max([0, 0.2 * (sal - tax_free) + 0.2 * max([0, sal - 3141.75])]) # 2021: 4189.25

    return "£{:.2f}".format(tax)

@app.callback(
    Output(component_id='forgone_mnthly_tax', component_property='children'),
    Input(component_id='annual_salary', component_property='value'),
    Input(component_id='USS', component_property='value'),
    Input(component_id='annual_tax_free', component_property='value'),
    Input(component_id='frac_deduction', component_property='value'),
    Input(component_id='n_strike_days', component_property='value'),
    
)
def mnthly_tax_forgone(sal_in, uss_in, tax_free_in, frac_in, n_days_in):

    if frac_in == "1/365":
        frac = 1/365
    elif frac_in == "1/260":
        frac = 1/260
    n_days = safe_convert(n_days_in)
    uss = 1 - safe_convert(uss_in) / 100
    
    sal_orig = uss * safe_convert(sal_in)/12 
    sal = uss * safe_convert(sal_in)/12 - safe_convert(sal_in) * n_days * frac 
    tax_free = safe_convert(tax_free_in)/12
    
    
    tax = ( max([0, 0.2 * (sal - tax_free) + 0.2 * max([0, sal - 3141.75])]) - 
        max([0, 0.2 * (sal_orig - tax_free) + 0.2 * max([0, sal_orig - 3141.75])])
    )

    return "£{:.2f}".format(tax)


@app.callback(
    Output(component_id='mnthly_NI', component_property='children'),
    Input(component_id='annual_salary', component_property='value'),
)
def mnthly_ni(sal_in):

    sal = safe_convert(sal_in)/12
    
    ni = max([0, 0.1325 * (sal - 823) - 0.1 * max([0, sal - 4189])])
    # 2021 : primary threshold: 797, upper earnings limit: 4190.33
    # 2021 : Rates 12%, 2%
    return "£{:.2f}".format(ni)


@app.callback(
    Output(component_id='deduct_mnthly_NI', component_property='children'),
    Input(component_id='annual_salary', component_property='value'),
    Input(component_id='frac_deduction', component_property='value'),
    Input(component_id='n_strike_days', component_property='value'),
)
def mnthly_ni_deduct(sal_in, frac_in, n_days_in):


    if frac_in == "1/365":
        frac = 1/365
    elif frac_in == "1/260":
        frac = 1/260
    n_days = safe_convert(n_days_in)
    sal = safe_convert(sal_in)/12 - n_days * frac * safe_convert(sal_in)
    
    ni = max([0, 0.1325 * (sal - 823) - 0.1 * max([0, sal - 4189])])

    return "£{:.2f}".format(ni)


@app.callback(
    Output(component_id='forgone_NI', component_property='children'),
    Input(component_id='mnthly_NI', component_property='children'),
    Input(component_id='deduct_mnthly_NI', component_property='children')
)
def forgone_ni(orig_ni_in, ni_in):

    orig_ni = safe_convert(orig_ni_in.replace('£', ''))
    ni = safe_convert(ni_in.replace('£', ''))

    return "£{:.2f}".format(ni - orig_ni)




@app.callback(
    Output(component_id='mnthly_take_home', component_property='children'),
    Input(component_id='mnthly_slry', component_property='children'),
    Input(component_id='USS', component_property='value'),
    Input(component_id='mnthly_tax', component_property='children'),
    Input(component_id='mnthly_NI', component_property='children'),
)
def mnthly_take_home(sal_in, uss_in, tax_in, ni_in):

    uss = 1 - safe_convert(uss_in) / 100
    sal = safe_convert(sal_in.replace('£', ''))
    tax = safe_convert(tax_in.replace('£', ''))
    ni = safe_convert(ni_in.replace('£', ''))

    return "£{:.2f}".format(uss * sal - tax - ni)

@app.callback(
    Output(component_id='deduct_mnthly_take_home', component_property='children'),
    Input(component_id='deduct_mnthly_slry', component_property='children'),
    Input(component_id='annual_salary', component_property='value'),
    Input(component_id='USS', component_property='value'),
    Input(component_id='deduct_mnthly_tax', component_property='children'),
    Input(component_id='deduct_mnthly_NI', component_property='children'),
)
def deduct_mnthly_take_home(sal_in, sal_orig_in, uss_in, tax_in, ni_in):

    uss = safe_convert(uss_in) / 100
    sal = safe_convert(sal_in.replace('£', ''))
    
    sal_orig = safe_convert(sal_orig_in)/12 
    tax = safe_convert(tax_in.replace('£', ''))
    ni = safe_convert(ni_in.replace('£', ''))

    return "£{:.2f}".format(sal - uss*sal_orig - tax - ni)

@app.callback(
    Output(component_id='forgone_take_home', component_property='children'),
    Input(component_id='deduct_mnthly_take_home', component_property='children'),
    Input(component_id='mnthly_take_home', component_property='children')
)
def forgone_total(deduct_take_home_in, take_home_in):

    deduct_take_home = safe_convert(deduct_take_home_in.replace('£', ''))
    take_home = safe_convert(take_home_in.replace('£', ''))

    return "£{:.2f}".format(take_home - deduct_take_home)



if __name__ == '__main__':
    app.run_server(debug=False)