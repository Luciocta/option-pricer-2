from flask import Flask, request, render_template
import numpy as np
from scipy.stats import norm
import plotly.graph_objs as go
import plotly.io as pio
import functionlib as fl

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    price = None
    delta_value = None
    graphJSON_premium = None
    graphJSON_delta = None
    graphJSON_gamma = None
    S = 100
    K = 100
    T = 1
    r = 0.05
    sigma = 0.2
    q = 0
    option_type = "c"

    if request.method == 'POST':
        try:
            print(request.form)
            S = float(request.form['spot'])
            K = float(request.form['strike'])
            T = float(request.form['maturity'])
            r = float(request.form['rate'])
            sigma = float(request.form['volatility'])
            q = float(request.form['dividend'])
            option_type = str(request.form['option_type'])

            price = fl.black_scholes(S, K, T, r, sigma, q, option_type)
            delta_value = fl.delta(S, K, T, r, sigma, q, option_type)


        except ValueError:
            price = "Erreur dans les entrées. Veuillez entrer des nombres valides."
    
    # Génération du graphique
    S_values = list(np.linspace(50, 150, 100))
    prices = [fl.black_scholes(s, K, T, r, sigma, q, option_type) for s in S_values]
    delta_list = [fl.delta(s, K, T, r, sigma, q, option_type) for s in S_values]
    gamma_list = [fl.gamma(s, K, T, r, sigma, q) for s in S_values]
    
    #Graph Premium
    fig_premium = go.Figure()
    fig_premium.add_trace(go.Scatter(x=S_values, y=prices, mode='lines', name="Prix de l'option Call"))
    fig_premium.update_layout(
        title="Premium en fonction du Spot",
        xaxis_title="Spot",
        yaxis_title="Premium",
        xaxis=dict(range=[50, 150],dtick=10),
        yaxis=dict(range=[min(prices), max(prices)], dtick=5),
        width=800,  # Largeur fixe pour le graphique
        height=500  # Hauteur fixe pour le graphique
    )
    graphJSON_premium = pio.to_json(fig_premium)

    # Graph Delta
    fig_delta = go.Figure()
    fig_delta.add_trace(go.Scatter(x=S_values, y=delta_list, mode='lines', name="Delta"))
    fig_delta.update_layout(
        title="Delta en fonction du Spot",
        xaxis_title="Spot",
        yaxis_title="Delta",
        xaxis=dict(range=[50, 150], dtick=10),
        yaxis=dict(range=[min(delta_list), max(delta_list)], dtick=0.1),
        width=800,  # Largeur fixe pour le graphique
        height=500  # Hauteur fixe pour le graphique
    )
    graphJSON_delta = pio.to_json(fig_delta)

    # Graph Gamma
    fig_gamma = go.Figure()
    fig_gamma.add_trace(go.Scatter(x=S_values, y=gamma_list, mode='lines', name="Gamma"))
    fig_gamma.update_layout(
        title="Gamma en fonction du Spot",
        xaxis_title="Spot",
        yaxis_title="Gamma",
        xaxis=dict(range=[50, 150], dtick=10),
        yaxis=dict(range=[min(gamma_list), max(gamma_list)+0.01], dtick=0.1),
        width=800,  # Largeur fixe pour le graphique
        height=500  # Hauteur fixe pour le graphique
    )
    graphJSON_gamma = pio.to_json(fig_gamma)

    return render_template('index.html', price=price, delta_value=delta_value,
                           graphJSON_premium=graphJSON_premium,
                           graphJSON_delta=graphJSON_delta, 
                           graphJSON_gamma=graphJSON_gamma
                           )


if __name__ == '__main__':
    app.run(debug=True)
