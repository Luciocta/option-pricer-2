from flask import Flask, request, render_template
import numpy as np
from scipy.stats import norm
import plotly.graph_objs as go
import plotly.io as pio

app = Flask(__name__)

def black_scholes_call(S, K, T, r, sigma, q=0):
    """
    Calcule le prix d'un call européen selon la formule de Black-Scholes.
    """
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

@app.route('/', methods=['GET', 'POST'])
def index():
    price = None
    graphJSON = None
    S = 100
    K = 100
    T = 1
    r = 0.05
    sigma = 0.2
    q = 0

    if request.method == 'POST':
        try:
            S = float(request.form['spot'])
            K = float(request.form['strike'])
            T = float(request.form['maturity'])
            r = float(request.form['rate'])
            sigma = float(request.form['volatility'])
            q = float(request.form['dividend'])
            
            price = black_scholes_call(S, K, T, r, sigma, q)
        except ValueError:
            price = "Erreur dans les entrées. Veuillez entrer des nombres valides."
    
    # Génération du graphique
    S_values = np.linspace(50, 150, 100)
    prices = [black_scholes_call(s, K, T, r, sigma, q) for s in S_values]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=S_values, y=prices, mode='lines', name="Prix de l'option Call"))
    fig.update_layout(title="Premium en fonction du Spot",
                      xaxis_title="Spot",
                      yaxis_title="Premium")
    
    graphJSON = pio.to_json(fig)
    
    return render_template('index.html', price=price, graphJSON=graphJSON)

if __name__ == '__main__':
    app.run(debug=True)
