
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc


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
    
    html.Br(),html.Br(),html.Br(),
    dbc.Row(html.Div("Notes:")), html.Br(),
    dbc.Row(
        html.Div(children=[
        """This is only an estimate of take home pay, and personal financial arrangements will 
        affect the pay you receive following deductions. 
        The additional rate of tax, above £150,000 per year, is not included in this calculation.
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

@app.callback(
    Output(component_id='mnthly_slry', component_property='children'),
    Input(component_id='annual_salary', component_property='value')
)
def pretax_mnthly_slry(sal_in):
    return "£{:.2f}".format(float(sal_in)/12)


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
    return "£{:.2f}".format((float(sal_in))/12 - frac * float(n_strike_days) * float(sal_in))
    
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
    return "£{:.2f}".format((frac * float(n_strike_days) * float(sal_in)))    


@app.callback(
    Output(component_id='mnthly_tax', component_property='children'),
    Input(component_id='annual_salary', component_property='value'),
    Input(component_id='USS', component_property='value'),
    Input(component_id='annual_tax_free', component_property='value')
)
def mnthly_tax(sal_in, uss_in, tax_free_in):

    uss = 1 - float(uss_in) / 100
    sal = uss * float(sal_in)/12
    tax_free = float(tax_free_in)/12
    
    tax = max([0, 0.2 * (sal - tax_free) + 0.2 * max([0, sal - 4189.25])])

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
    n_days = float(n_days_in)
    uss = 1 - float(uss_in) / 100
    
    sal = uss * float(sal_in)/12 - float(sal_in) * n_days * frac 
    tax_free = float(tax_free_in)/12
    
    
    tax = max([0, 0.2 * (sal - tax_free) + 0.2 * max([0, sal - 4189.25])])

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
    n_days = float(n_days_in)
    uss = 1 - float(uss_in) / 100
    
    sal_orig = uss * float(sal_in)/12 
    sal = uss * float(sal_in)/12 - float(sal_in) * n_days * frac 
    tax_free = float(tax_free_in)/12
    
    
    tax = ( max([0, 0.2 * (sal - tax_free) + 0.2 * max([0, sal - 4189.25])]) - 
        max([0, 0.2 * (sal_orig - tax_free) + 0.2 * max([0, sal_orig - 4189.25])])
    )

    return "£{:.2f}".format(tax)


@app.callback(
    Output(component_id='mnthly_NI', component_property='children'),
    Input(component_id='annual_salary', component_property='value'),
)
def mnthly_ni(sal_in):

    sal = float(sal_in)/12
    
    ni = max([0, 0.12 * (sal - 797) - 0.1 * max([0, sal - 4190.33])])

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
    n_days = float(n_days_in)
    sal = float(sal_in)/12 - n_days * frac * float(sal_in)
    
    ni = max([0, 0.12 * (sal - 797) - 0.1 * max([0, sal - 4190.33])])

    return "£{:.2f}".format(ni)


@app.callback(
    Output(component_id='forgone_NI', component_property='children'),
    Input(component_id='mnthly_NI', component_property='children'),
    Input(component_id='deduct_mnthly_NI', component_property='children')
)
def forgone_ni(orig_ni_in, ni_in):

    orig_ni = float(orig_ni_in.replace('£', ''))
    ni = float(ni_in.replace('£', ''))

    return "£{:.2f}".format(ni - orig_ni)




@app.callback(
    Output(component_id='mnthly_take_home', component_property='children'),
    Input(component_id='mnthly_slry', component_property='children'),
    Input(component_id='USS', component_property='value'),
    Input(component_id='mnthly_tax', component_property='children'),
    Input(component_id='mnthly_NI', component_property='children'),
)
def mnthly_take_home(sal_in, uss_in, tax_in, ni_in):

    uss = 1 - float(uss_in) / 100
    sal = float(sal_in.replace('£', ''))
    tax = float(tax_in.replace('£', ''))
    ni = float(ni_in.replace('£', ''))

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

    uss = float(uss_in) / 100
    sal = float(sal_in.replace('£', ''))
    sal_orig = float(sal_orig_in)/12 
    tax = float(tax_in.replace('£', ''))
    ni = float(ni_in.replace('£', ''))

    return "£{:.2f}".format(sal - uss*sal_orig - tax - ni)

@app.callback(
    Output(component_id='forgone_take_home', component_property='children'),
    Input(component_id='deduct_mnthly_take_home', component_property='children'),
    Input(component_id='mnthly_take_home', component_property='children')
)
def forgone_total(deduct_take_home_in, take_home_in):

    deduct_take_home = float(deduct_take_home_in.replace('£', ''))
    take_home = float(take_home_in.replace('£', ''))

    return "£{:.2f}".format(take_home - deduct_take_home)



if __name__ == '__main__':
    app.run_server(debug=False)