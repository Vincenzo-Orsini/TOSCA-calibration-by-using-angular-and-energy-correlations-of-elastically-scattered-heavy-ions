from dash import Dash, dcc, html, Input, Output, State
from layout import layout
import plotly.express as px
import pandas as pd
from mc import execute

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
MATHJAX_CDN = "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML"
app = Dash(__name__, external_stylesheets=external_stylesheets, external_scripts=[MATHJAX_CDN])


# Definisci il layout dell'app
app.layout = layout

# Definisci la callback per aggiornare il grafico in base al parametro inserito
@app.callback(
    [Output('gaussiana-energie', 'figure'),
    Output('grafico-theta_lab', 'figure'),
    Output('grafico-energy_lab', 'figure'),
    Output('arm_1', 'figure'),
    Output('tof_arm_1', 'figure'),
    Output('arm_1_single', 'figure'),
    Output('tof_arm_1_single', 'figure'),
    Output('arm_2', 'figure'),
    Output('tof_arm_2', 'figure'),
    Output('arm_2_single', 'figure'),
    Output('tof_arm_2_single', 'figure'),
    Output('tof_1_2', 'figure'),
    Output('system', 'figure'),],
    [Input("Start", "n_clicks")],
    [State('m_p', 'value')],
    [State('m_T', 'value')],
    [State('z_p', 'value')],
    [State('z_T', 'value')],
    [State('E_lab', 'value')],
    [State('inc_E_lab', 'value')],
    [State('angle_arm_1', 'value')],
    [State('distance_arm_1_start', 'value')],
    [State('lenght_arm_1_start', 'value')],
    [State('distance_arm_1_stop', 'value')],
    [State('lenght_arm_1_stop', 'value')],
    [State('angle_arm_2', 'value')],
    [State('distance_arm_2_start', 'value')],
    [State('lenght_arm_2_start', 'value')],
    [State('distance_arm_2_stop', 'value')],
    [State('lenght_arm_2_stop', 'value')],
)


def update_graph(n, m_p, m_T, z_p, z_T, E_lab_0, inc_E_lab,
                 angle_arm_1, distance_arm_1_start, lenght_arm_1_start,
                 distance_arm_1_stop, lenght_arm_1_stop,
                 angle_arm_2, distance_arm_2_start, lenght_arm_2_start, 
                 distance_arm_2_stop, lenght_arm_2_stop):
    elements = execute(m_p, m_T, z_p, z_T, E_lab_0, inc_E_lab,
                 angle_arm_1, distance_arm_1_start, lenght_arm_1_start,
                 angle_arm_1, distance_arm_1_stop, lenght_arm_1_stop,
                 angle_arm_2, distance_arm_2_start, lenght_arm_2_start,
                 angle_arm_2, distance_arm_2_stop, lenght_arm_2_stop)
    
    df = elements[0]
    #istogramma gaussiano
    fig_gauss_e = px.histogram(df, x='E_lab', nbins=100, labels={'E_lab':'Energia Laboratorio (Mev)'}, title='Distribuzione Energia Laboratorio')

    #matrice di correlazione angoli
    fig_theta_lab = px.line(df, x='theta_t_lab', y='theta_p_lab', markers=True, title='Matrice di Correlazione fra angoli di diffusione nel Laboratorio')
    fig_theta_lab.update_traces(marker=dict(size=2))
    fig_theta_lab.update_xaxes(title=dict(text=r'$\theta_{T,LAB}(°)$'))
    fig_theta_lab.update_yaxes(title=dict(text=r'$\theta_{p,LAB}(°)$'))

    #matrice di correlazione energie
    fig_E_lab = px.scatter(df, x='E_t_lab', y='E_p_lab', title='Matrice di Correlazione fra Energie di diffusione nel Laboratorio')
    fig_E_lab.update_traces(marker=dict(size=2))
    fig_E_lab.update_xaxes(title=dict(text=r'$E_{T,LAB}(Mev)$'))
    fig_E_lab.update_yaxes(title=dict(text=r'$E_{p,LAB}(Mev)$'))

    
    dt = elements[1]
    filtered_dt = dt[(dt['detection_arm_1_tof_single'] <= 1000) & (dt['detection_arm_2_tof_single'] <= 1000)]

    #istogramma angoli arm 1 correlato
    fig_arm_1 = px.histogram(filtered_dt, x='detection_arm_1_angle', nbins=10, title='Distribuzione dei rilevamenti per angolo ARM 1')
    fig_arm_1.update_xaxes(title=dict(text=r'$\theta_{T,LAB}(°)$'))

    #istogramma angoli arm 1 non correlato
    fig_arm_1_single = px.histogram(filtered_dt, x='detection_arm_1_angle_single', nbins=10, title='Distribuzione dei rilevamenti per angolo ARM 1 (non correlati)')
    fig_arm_1_single.update_xaxes(title=dict(text=r'$\theta_{T,LAB}(°)$'))

    #istogramma angoli arm 2 correlato
    fig_arm_2 = px.histogram(filtered_dt, x='detection_arm_2_angle', nbins=10, title='Distribuzione dei rilevamenti per angolo ARM 2')
    fig_arm_2.update_xaxes(title=dict(text=r'$\theta_{p,LAB}(°)$'))

    #istogramma angoli arm 2 non correlato
    fig_arm_2_single = px.histogram(filtered_dt, x='detection_arm_2_angle_single', nbins=10, title='Distribuzione dei rilevamenti per angolo ARM 2 (non correlati)')
    fig_arm_2_single.update_xaxes(title=dict(text=r'$\theta_{p,LAB}(°)$'))

    #istogramma tof arm 1 correlato
    tof_arm_1 = px.histogram(filtered_dt, x='detection_arm_1_tof', nbins=1000, title='Distribuzione TOF ARM 1')
    tof_arm_1.update_xaxes(title=dict(text=r'$TOF_1 (ns)$'))

    #istogramma tof arm 1 non correlato
    tof_arm_1_single = px.histogram(filtered_dt, x='detection_arm_1_tof_single', nbins=1000, title='Distribuzione TOF ARM 1 (non correlati)')
    tof_arm_1_single.update_xaxes(title=dict(text=r'$TOF_1 (ns)$'))

    #istogramma tof arm 2 correlato
    tof_arm_2 = px.histogram(filtered_dt, x='detection_arm_2_tof', nbins=1000, title='Distribuzione TOF ARM 2')
    tof_arm_2.update_xaxes(title=dict(text=r'$TOF_2 (ns)$'))

    #istogramma tof arm 2 non correlato
    tof_arm_2_single = px.histogram(filtered_dt, x='detection_arm_2_tof_single', nbins=1000, title='Distribuzione TOF ARM 2 (non correlati)')
    tof_arm_2_single.update_xaxes(title=dict(text=r'$TOF_2 (ns)$'))
    
    #matrice di correlazione tof
    tof_1_2 = px.scatter(filtered_dt, x='detection_arm_1_tof', y='detection_arm_2_tof', title="Matrice di Correlazione TOF ARM 1 e ARM 2", width=1000, height=700)
    tof_1_2.update_xaxes(title=dict(text=r'$TOF_1 (ns)$'))
    tof_1_2.update_yaxes(title=dict(text=r'$TOF_2 (ns)$'))

    #geometria dello spettrometro
    graph=elements[2]
    fig_system = px.scatter(graph, x='d_graph_x_1_stop', y='d_graph_y_1_stop', title='Geometria dello Spettrometro', width=1000, height=700)
    fig_system.add_scatter(x=graph['d_graph_x_1_stop'], y=graph['d_graph_y_1_stop'], mode='lines', name='Arm 1')
    fig_system.add_scatter(x=graph['d_graph_x_2_stop'], y=graph['d_graph_y_2_stop'], mode='lines', name='Arm 2')
    fig_system.add_scatter(x=graph['x_graph_1_start'], y=graph['y_graph_1_start'], mode='lines', name='Start Arm 1')
    fig_system.add_scatter(x=graph['x_graph_2_start'], y=graph['y_graph_2_start'], mode='lines', name='Start Arm 2')
    fig_system.add_scatter(x=graph['x_graph_1_stop'], y=graph['y_graph_1_stop'], mode='lines', name='Stop Arm 1')
    fig_system.add_scatter(x=graph['x_graph_2_stop'], y=graph['y_graph_2_stop'], mode='lines', name='Stop Arm 2')
    fig_system.update_traces(marker=dict(size=2))
    fig_system.update_xaxes(title=dict(text=r'$X (cm)$'))
    fig_system.update_yaxes(title=dict(text=r'$Y (cm)$'), scaleanchor="x", scaleratio=1)

    return fig_gauss_e, fig_theta_lab, fig_E_lab, fig_arm_1, tof_arm_1, fig_arm_1_single, tof_arm_1_single, fig_arm_2, tof_arm_2, fig_arm_2_single, tof_arm_2_single, tof_1_2, fig_system

if __name__ == '__main__':
    app.run(debug=True)

