import dash
import dash_core_components as dcc
import dash_html_components as html
from methods import AreaUnderTheCurve as auc, KolmogorovSmirnov as ks, \
    PartialGiniCoefficient as pg, BrierScore as bs, ProcentCorrectClassified as pcc, \
    HMeasure as hm



models = []
model = {}
true_class = [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1]
probability = [0, 0.1, 0.1, 0.15, 0.2, 0.2, 0.25, 0.2, 0.3, 0.3,
               0.35, 0.4, 0.45, 0.5, 0.5, 0.55, 0.6, 0.6, 0.65, 0.7,
               0.7, 0.75, 0.8, 0.8, 0.85, 0.9, 0.9, 0.9, 0.95, 0.99]
model['true_class']= true_class
model['probability'] = probability
models.append(model)


# true_class2 = [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1]
# probability2 = [0, 0.1, 0.1, 0.15, 0.2, 0.6, 0.25, 0.2, 0.3, 0.3,
#                0.5, 0.5, 0.5, 0.5, 0.5, 0.55, 0.6, 0.6, 0.65, 0.7,
#                0.7, 0.75, 0.75, 0.8, 0.85, 0.9, 0.9, 0.9, 0.95, 0.99]
# model = {}
# model['true_class'] = true_class2
# model['probability'] = probability2
# models.append(model)
#
# true_class3 = [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1]
# probability3 = [0, 0.1, 0.1, 0.15, 0.2, 0.23, 0.25, 0.2, 0.3, 0.3,
#                0.5, 0.5, 0.15, 0.5, 0.5, 0.55, 0.6, 0.7, 0.65, 0.7,
#                0.7, 0.66, 0.75, 0.8, 0.85, 0.9, 0.9, 0.9, 0.95, 0.99]
# model = {}
# model['true_class'] = true_class3
# model['probability'] = probability3
# models.append(model)


#########################
#   ROC + AUC  Start    #
#########################
roc_lines = []
roc_lines.append({'x': [0,1], 'y': [0,1], 'type': 'line',
            'name': '45-Grad Diagonale', 'line': {'dash': 'dot'}})

for k in range(len(models)):

    auc_value, fpr, tpr  = auc.area_under_the_curve_and_roc_curve(models[k]['true_class'], models[k]['probability'])
    name = 'ROC'  + ' - AUC'  +'=' + "%.2f" % auc_value

    roc_lines.append({'x': fpr, 'y': tpr, 'type': 'line',
                'name': name})


roc_chart =html.Div(className='six columns',
               children=[
                   dcc.Graph(
                       id= 'roc_chart',
                       figure={
                           'data': roc_lines,
                           'layout': {
                               'title': 'receiver operating characteristic curve',
                                'xaxis': {
                                    'title': 'false positive rate'
                               },
                                'yaxis': {
                                    'title': 'true positive rate'
                               }
                           },

                       }
                   )
               ])
#########################
#   ROC + AUC  END      #
#########################

#################################
#  partial Gini + Lorenz Start  #
#################################

lorenz_lines = [{'x': [0,1,2,3,4,5,6,7,8,9,10],
                 'y': [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1],
                 'type': 'line', 'name': '45-Degree diagonal', 'line': {'dash': 'dot'}}]

for l in range(len(models)):

    PG,x, y,  x_partial, y_partial = pg.partial_gini_coefficient(models[l]['true_class'], models[l]['probability'], 0.45)
    name = 'Lorenzkurve' + str(l+1) + ' - PG' + str(l+1) +'=' + "%.2f" % PG
    name3 = 'cut_off' + str(l+1)
    lorenz_lines.append({'x': x, 'y': y, 'type': 'line', 'name': name})
    lorenz_lines.append({'x': [x_partial,x_partial], 'y': [0,y_partial], 'type': 'line', 'name': name3})

lorenz_curve = html.Div(className='six columns',
               children=[
                   dcc.Graph(
                       id= 'lorenz_curve',
                       figure={
                           'data': lorenz_lines,
                           'layout': {
                               'title': 'partial gini',
                               'xaxis': {
                                   'title': 'decile'
                               },
                               'yaxis': {
                                   'title': 'cum number of bad %'
                               }
                           }
                       }
                   )
               ])

#################################
#   partial Gini + Lorenz End   #
#################################

############################
# Kolmogorov Smirnov start #
############################
colors = ['blue', 'red', 'orange', 'green', 'DarkOrange', 'LightSeeGreen', 'MediumPurple',
          'RoyalBlue', 'LightSkyBlue', 'LightSalmon', 'PaleTurquoise', 'black', 'gray']

ks_lines = []
for j in range(len(models)):
    KS, x, y_1, y_2, x_ks, y_top, y_bottom = ks.kolmogorov_smirnov_score_and_curve(models[j]['true_class'], models[j]['probability'])
    max_seperation_name = 'max_seperation' + ' - ' + 'KS' + str(l+1) +'=' + "%.2f" % KS
    ks_lines.append({'x': x, 'y': y_1, 'type': 'line', 'name': 'cum_bad_pcn' + str(j+1), 'line': {'color': colors[j]}})
    ks_lines.append({'x': x, 'y': y_2, 'type': 'line', 'name': 'cum_good_pcn' + str(j+1), 'line': {'color': colors[j]}})
    ks_lines.append({'x': [x_ks, x_ks], 'y': [y_bottom, y_top], 'type': 'line', 'name': max_seperation_name})

ks_chart = html.Div(className='six columns',
               children=[
                   dcc.Graph(
                       id='ks_chart',
                       figure={
                           'data': ks_lines,
                           'layout': {
                               'title': 'KS-Graph',
                               'xaxis': {
                                   'title': 'scores'
                               },
                               'yaxis': {
                                   'title': '%'
                               }
                           }
                       }
                   ),
               ])

############################
#   Kolmogorov Smirnov end #
############################

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

bs_scores = []
for g in range(len(models)):
    BS = bs.brier_score(models[g]['true_class'], models[g]['probability'])
    bs_scores.append(html.Label(children=['BS' + str(g+1) + '+' + ' = ' + "%.2f" % BS['positive_bs_score'] + '  /  ',
                                          'BS' + str(g+1) + '-' + ' = ' + "%.2f" % BS['negative_bs_score'] + '  ']))

pcc_scores= []
for f in range(len(models)):
    PCC = pcc.procent_correct_classified(models[f]['true_class'], models[f]['probability'], 0.7)
    pcc_scores.append(html.Label(children=['PCC' + str(f+1) + ' = ' + "%.2f" % PCC]))


h_scores =[]
for d in range(len(models)):
   h_measure= hm.h_measure(models[d]['true_class'], models[d]['probability'])
   h_scores.append(html.Label(children=['H-measure' + str(d+1) + ' = ' + "%.2f" % h_measure]))

app.layout = html.Div(children=[
    html.Div(className='row',
                      children=[
                            html.Div(className='six columns',
                                     style={
                                         'text-align': 'center'
                                     },
                                    children=[
                                       html.H4(children='Brier Score'),
                                       html.Label(children=bs_scores),
                                       html.H4(children=['PCC']),
                                       html.Label(children=pcc_scores),
                                       html.H4(children='H-measure'),
                                       html.Label(children=h_scores),
                                   ]),
                            ks_chart

                    ]),
    html.Div(className='row',
                      children=[
                            lorenz_curve,
                            roc_chart

                    ])

    ])
if __name__ == '__main__':
    app.run_server(debug=True)

