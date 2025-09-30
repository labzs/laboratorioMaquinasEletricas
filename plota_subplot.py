
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import seaborn as sns
from dados import df  # Importando o DataFrame do arquivo dados.py 
from modelos import calcular_tendencia_por_tipo

# Configuração do estilo dos gráficos
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Função para calcular linha de tendência genérica
def calcular_tendencia(x, y, grau=2):
    """Calcula polinômio de tendência"""
    if len(x) < grau + 1:
        return None
    
    try:
        coef = np.polyfit(x, y, grau)
        return np.poly1d(coef)
    except:
        return None

# Função única para plotar com tendência
def plotar_com_tendencia(ax, x, y, label, color, marker='o', tipo='Independente', rotacao_por_torque=False):
    """Plota pontos e linha de tendência"""
    # Plota os pontos medidos
    ax.scatter(x, y, color=color, alpha=0.7, s=50, marker=marker)
    
    # Decide qual tipo de ajuste usar
    if rotacao_por_torque and tipo in ['Serie', 'Independente', 'Composta']:
        # Usa modelos físicos específicos
        trend_func = calcular_tendencia_por_tipo(x, y, tipo)
        if trend_func is not None:
            x_trend = np.linspace(min(x), max(x), 200)
            y_trend = trend_func(x_trend)
            ax.plot(x_trend, y_trend, color=color, label=label, linewidth=2)
        else:
            # Fallback para ajuste polinomial
            trendline = calcular_tendencia(x, y)
            if trendline is not None:
                x_trend = np.linspace(min(x), max(x), 50)
                y_trend = trendline(x_trend)
                ax.plot(x_trend, y_trend, color=color, label=label, linewidth=2)
    else:
        # Ajuste polinomial genérico
        trendline = calcular_tendencia(x, y)
        if trendline is not None:
            x_trend = np.linspace(min(x), max(x), 50)
            y_trend = trendline(x_trend)
            ax.plot(x_trend, y_trend, color=color, label=label, linewidth=2)

# Configurações dos gráficos
tensoes = [110, 220]
ligacoes = ['Independente', 'Serie', 'Composta']
cores = {'Independente': 'blue', 'Serie': 'red', 'Composta': 'green'}
marcadores = {'Independente': 'o', 'Serie': 's', 'Composta': '^'}

# 1. GRÁFICOS TORQUE x CORRENTE (Ia)
print("Gerando gráficos Torque x Corrente...")

fig, axes = plt.subplots(1, 2, figsize=(8, 5))

for i, tensao in enumerate(tensoes):
    ax = axes[i]
    for ligacao in ligacoes:
        dados = df[(df['Ligacao'] == ligacao) & (df['Tensao_V'] == tensao)]
        if not dados.empty:
            torque = dados['Torque_Nm'].values
            corrente = dados['Ia_A'].values
            plotar_com_tendencia(ax, corrente, torque,
                                 ligacao, cores[ligacao], marcadores[ligacao])
    ax.set_xlabel('Ia (A)', fontsize=12)
    if i == 0:
        ax.set_ylabel('T (N.m)', fontsize=12)
    ax.set_title(f'{tensao}V', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)

fig.suptitle('Torque vs Corrente', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('torque_corrente_comparativo.png', dpi=300, bbox_inches='tight')
plt.show()

# 2. GRÁFICOS TORQUE x ROTAÇÃO
print("Gerando gráficos Torque x Rotação...")

fig, axes = plt.subplots(1, 2, figsize=(9, 5))

for i, tensao in enumerate(tensoes):
    ax = axes[i]
    for ligacao in ligacoes:
        dados = df[(df['Ligacao'] == ligacao) & (df['Tensao_V'] == tensao)]
        if not dados.empty:
            torque = dados['Torque_Nm'].values
            rotacao = dados['Rotacao_rpm'].values
            plotar_com_tendencia(ax, torque, rotacao,
                                 ligacao, cores[ligacao], marcadores[ligacao],
                                 tipo=ligacao, rotacao_por_torque=True)
    ax.set_xlabel('T (N.m)', fontsize=12)
    if i == 0:
        ax.set_ylabel('n (rpm)', fontsize=12)
    ax.set_title(f'{tensao}V', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)

fig.suptitle('Rotação vs Torque', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('torque_rotacao_comparativo.png', dpi=300, bbox_inches='tight')
plt.show()

# 3. GRÁFICOS RENDIMENTO x POTÊNCIA MECÂNICA
print("Gerando gráficos Rendimento x Potência...")

fig, axes = plt.subplots(1, 2, figsize=(9, 5))

for i, tensao in enumerate(tensoes):
    ax = axes[i]
    for ligacao in ligacoes:
        dados = df[(df['Ligacao'] == ligacao) & 
                   (df['Tensao_V'] == tensao) & 
                   (df['Rendimento_decimal'] > 0)]
        if not dados.empty:
            potencia = dados['Pmec_W'].values
            rendimento = dados['Rendimento_decimal'].values * 100
            plotar_com_tendencia(ax, potencia, rendimento,
                                 ligacao, cores[ligacao], marcadores[ligacao])
    ax.set_xlabel('Potência Mecânica (W)', fontsize=12)
    if i == 0:
        ax.set_ylabel('Rendimento (%)', fontsize=12)
    ax.set_title(f'{tensao}V', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)

fig.suptitle('Rendimento vs Potência Mecânica', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('rendimento_potencia_comparativo.png', dpi=300, bbox_inches='tight')

# 4. GRÁFICOS RENDIMENTO x POTÊNCIA MECÂNICA
print("Gerando gráficos Rendimento x Corrente de Armadura...")

fig, axes = plt.subplots(1, 2, figsize=(9, 5))

for i, tensao in enumerate(tensoes):
    ax = axes[i]
    for ligacao in ligacoes:
        dados = df[(df['Ligacao'] == ligacao) & 
                   (df['Tensao_V'] == tensao) & 
                   (df['Rendimento_decimal'] > 0)]
        if not dados.empty:
            corrente = dados['Ia_A'].values
            rendimento = dados['Rendimento_decimal'].values * 100
            plotar_com_tendencia(ax, corrente, rendimento,
                                 ligacao, cores[ligacao], marcadores[ligacao])
    ax.set_xlabel('Ia (A)', fontsize=12)
    if i == 0:
        ax.set_ylabel('Rendimento (%)', fontsize=12)
    ax.set_title(f'{tensao}V', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)

fig.suptitle('Rendimento vs Ia', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('rendimento_corrente_comparativo.png', dpi=300, bbox_inches='tight')

plt.show()
