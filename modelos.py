from scipy.optimize import curve_fit
import numpy as np

# === Modelos matemáticos ===
def modelo_serie(T, a, b, c):
    """Modelo hiperbólico para motor série"""
    return a / (T + b) + c

def modelo_shunt(T, a, b):
    """Modelo linear para motor shunt (independente)"""
    return a * T + b

def modelo_composta(T, a, b, c):
    """Modelo quadrático para motor composto"""
    return a * T**2 + b * T + c

def calcular_tendencia_por_tipo(x, y, tipo):
    """
    Ajusta a tendência com base no tipo de ligação.
    Retorna uma função que calcula os valores ajustados.
    """
    mask = np.isfinite(x) & np.isfinite(y)
    x_clean = x[mask]
    y_clean = y[mask]

    if len(x_clean) < 3:
        return None  # Poucos pontos para ajustar

    try:
        if tipo == 'Serie':
            popt, _ = curve_fit(modelo_serie, x_clean, y_clean, maxfev=5000)
            return lambda t: modelo_serie(t, *popt)

        elif tipo == 'Independente':
            popt, _ = curve_fit(modelo_shunt, x_clean, y_clean)
            return lambda t: modelo_shunt(t, *popt)

        elif tipo == 'Composta':
            popt, _ = curve_fit(modelo_composta, x_clean, y_clean)
            return lambda t: modelo_composta(t, *popt)

    except RuntimeError:
        return None