import math
import numpy as np
import pandas as pd
from scipy.stats import norm


def black_scholes(S0, K, T, r, vol, q, opt_type="c"):
    """
    S0 : spot price at time t=0
    K : strike price
    T : maturity (in years)
    r : risk-free rate
    vol : implied volatility
    opt_type : "C" for a call option and "P" for a put option

    Return the price of a vanilla option (for either a call option or a put option) with Black-Scholes formula
    """

    d1=(np.log(S0/K) + (r-q+vol**2/2)*T)/(vol*np.sqrt(T))
    d2=d1-vol*np.sqrt(T)
    
    try:
        if opt_type=="c":
            price=S0*np.exp(-q*T)*norm.cdf(d1, 0, 1)-K*np.exp(-r*T)*norm.cdf(d2, 0, 1)
        elif opt_type=="p":
            price=K*np.exp(-r*T)*norm.cdf(-d2, 0, 1)-S0*norm.cdf(-d1, 0, 1)
        return round(price, 2)
    except:
        raise ValueError("Please confirm option type, either 'c' for Call or 'p' for Put")


def delta(S0, K, T, r, vol, q, opt_type='c'):
    """
    S0 : spot price at time t=0
    K : strike price
    T : maturity (in years)
    r : risk-free rate
    vol : implied volatility
    opt_type : "C" for a call option and "P" for a put option

    Return the delta of a vanilla option (for either a call option or a put option) with Black-Scholes formula
    """
    d1=(np.log(S0/K) + (r-q+vol**2/2)*T)/(vol*np.sqrt(T))

    if opt_type=="c":
        delta = norm.cdf(d1, 0, 1)
    elif opt_type=="p":
        delta = norm.cdf(d1, 0, 1) - 1
    return round(delta, 2)

def gamma(S0, K, T, r, sigma, q):

    d1=(np.log(S0/K) + (r+sigma**2/2)*T)/(sigma*np.sqrt(T))
    Nprime = lambda x: np.exp(-x**2/2)/np.sqrt(2*np.pi)

    return Nprime(d1)*np.exp(-q*T)/(S0*sigma*np.sqrt(T))