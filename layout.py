from dash import dcc, html
layout = html.Div([
    html.H1(children='Calibration Quick Tool for Elastic Scattering and TOSCA Experiment', style={'textAlign':'center'}),
    html.H2(children='''Inserisci i parametri per il calcolo:''', style={'textAlign':'center'}),
    html.Div([
    html.Div([html.H4(children='Massa Proiettile (u)',style={'display':'inline-block','margin-right':20}),
              dcc.Input(id='m_p', type='number', required=True, placeholder='Inserisci Massa Proiettile (u)', value=40, name="Massa Proiettile")]),
    html.Div([html.H4(children='Massa Target (u)',style={'display':'inline-block','margin-right':20}),
                dcc.Input(id='m_T', type='number', required=True, placeholder='Inserisci Massa Bersaglio (u)', value=208, name="Massa Bersaglio")]),
    html.Div([html.H4(children='Energia Laboratorio (MeV)',style={'display':'inline-block','margin-right':20}),
              dcc.Input(id='E_lab', type='number', required=True, placeholder='Inserisci E_lab (MeV)', value=200, name="Energia Laboratorio")]),
    html.Div([html.H4(children='Z Target',style={'display':'inline-block','margin-right':20}),
                dcc.Input(id='z_T', type='number', required=True, placeholder='Inserisci Z Bersaglio', value=82, name="Z Bersaglio")]),
    html.Div([html.H4(children='Z Proiettile',style={'display':'inline-block','margin-right':20}),
              dcc.Input(id='z_p', type='number', required=True, placeholder='Inserisci Z Proiettile', value=18, name="Z Proiettile")]),
    html.Div([html.H4(children='Incertezza Energia Laboratorio (MeV)',style={'display':'inline-block','margin-right':20}),
              dcc.Input(id='inc_E_lab', type='number', required=True, placeholder='Inserisci inc_E_lab (MeV)', value=2, name="Incertezza Energia Laboratorio")]),
    ], style={'columnCount': 2, 'margin-left': 300, 'margin-bottom': 40}),

html.Div([
    html.H3(children='''Settings Arm 1:'''),
    html.Div([
    html.Div([html.H4(children='Angolo Arm 1 (Degree)',style={'display':'inline-block','margin-right':20}),
                dcc.Input(id='angle_arm_1', type='number', required=True, placeholder='Inserisci Angolo', value=70, name="angle_arm_1", min=1, max=179)]),
    html.Div([html.H4(children='Distanza Arm 1 Start(cm)',style={'display':'inline-block','margin-right':20}),
                dcc.Input(id='distance_arm_1_start', type='number', required=True, placeholder='Inserisci Distanza', value=9, name="distance_arm_1_start")]),
    html.Div([html.H4(children='Lunghezza Arm 1 Start(cm)',style={'display':'inline-block','margin-right':20}),
                dcc.Input(id='lenght_arm_1_start', type='number', required=True, placeholder='Inserisci Lunghezza', value=7, name="lenght_arm_1_start")]),
    html.Div([html.H4(children='Distanza Arm 1 Stop(cm)',style={'display':'inline-block','margin-right':20}),
                dcc.Input(id='distance_arm_1_stop', type='number', required=True, placeholder='Inserisci Distanza', value=15, name="distance_arm_1_stop")]),
    html.Div([html.H4(children='Lunghezza Arm 1 Stop(cm)',style={'display':'inline-block','margin-right':20}),
                dcc.Input(id='lenght_arm_1_stop', type='number', required=True, placeholder='Inserisci Lunghezza', value=12, name="lenght_arm_1_stop")]),
    ], style={'columnCount': 1}),


    html.H3(children='''Settings Arm 2:'''),
    html.Div([
    html.Div([html.H4(children='Angolo Arm 2 (Degree)',style={'display':'inline-block','margin-right':20}),
                dcc.Input(id='angle_arm_2', type='number', required=True, placeholder='Inserisci Angolo', value=-70, name="angle_arm_2", min=-179, max=-1)]),
    html.Div([html.H4(children='Distanza Arm 2 Start(cm)',style={'display':'inline-block','margin-right':20}),
                dcc.Input(id='distance_arm_2_start', type='number', required=True, placeholder='Inserisci Distanza', value=9, name="distance_arm_2_start")]),
    html.Div([html.H4(children='Lunghezza Arm 2 Start(cm)',style={'display':'inline-block','margin-right':20}),
                dcc.Input(id='lenght_arm_2_start', type='number', required=True, placeholder='Inserisci Lunghezza', value=7, name="lenght_arm_2_start")]),
    html.Div([html.H4(children='Distanza Arm 2 Stop(cm)',style={'display':'inline-block','margin-right':20}),
                dcc.Input(id='distance_arm_2_stop', type='number', required=False, placeholder='Inserisci Distanza', value=15, name="distance_arm_2_stop")]),
    html.Div([html.H4(children='Lunghezza Arm 2 Stop(cm)',style={'display':'inline-block','margin-right':20}),
                dcc.Input(id='lenght_arm_2_stop', type='number', required=True, placeholder='Inserisci Lunghezza', value=12, name="lenght_arm_2_stop")]),
    ], style={'columnCount': 1}),
    ], style={'columnCount': 2, 'margin-left': 300, 'margin-bottom': 40}),

    html.Div([
    html.Button(
            "Start", id="Start", className="me-2", n_clicks=0, style={'font-size': 15}
        )
    ], style={'margin-left': 900}),
    
    html.Div([
    dcc.Graph(id='gaussiana-energie'),
    dcc.Graph(id='grafico-theta_lab', mathjax=True),
    dcc.Graph(id='grafico-energy_lab', mathjax=True)],style={'columnCount': 3}),

    html.Div([
        dcc.Graph(id='system', mathjax=True),
        dcc.Graph(id='tof_1_2', mathjax=True),
    ], style={'columnCount': 2}),

    html.H3(children='''Conteggi di coincidenza''', style={'textAlign':'center'}),
    html.Div([
        html.Div([
            html.H4(children='ARM1',style={'display':'inline-block','margin-right':20}),
            dcc.Graph(id='arm_1', mathjax=True),
            dcc.Graph(id='tof_arm_1', mathjax=True),
        ], style={'columnCount': 1}),
        html.Div([
            html.H4(children='ARM2',style={'display':'inline-block','margin-right':20}),
            dcc.Graph(id='arm_2', mathjax=True),
            dcc.Graph(id='tof_arm_2', mathjax=True),
        ], style={'columnCount': 1}),
], style={'columnCount': 2}),
    
    html.H3(children='''Conteggi scorrelati''', style={'textAlign':'center'}),
    html.Div([
        html.Div([
            html.H4(children='ARM1',style={'display':'inline-block','margin-right':20}),
            dcc.Graph(id='arm_1_single', mathjax=True),
            dcc.Graph(id='tof_arm_1_single', mathjax=True),
        ], style={'columnCount': 1}),
        html.Div([
            html.H4(children='ARM2',style={'display':'inline-block','margin-right':20}),
            dcc.Graph(id='arm_2_single', mathjax=True),
            dcc.Graph(id='tof_arm_2_single', mathjax=True),
        ], style={'columnCount': 1}),
    ], style={'columnCount': 2}),



])