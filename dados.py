import pandas as pd

# Criando o DataFrame com todos os dados
data = {
    'Ligacao': [],
    'Tensao_V': [],
    'Torque_Nm': [],
    'Ia_A': [],
    'Rotacao_rpm': [],
    'Rotacao_rps': [],
    'Pmec_W': [],
    'Peletrica_W': [],
    'Rendimento': []
}

# Ligação Independente 220V
independente_220v = [
    [0.43, 0.0, 1644, 172.1592774, 74.02848929, 0, '#DIV/0!'],
    [1.91, 2.6, 1609, 168.494086, 321.8237042, 572, '56.26%'],
    [3.16, 4.1, 1590, 166.5044106, 526.1539376, 902, '58.33%'],
    [4.6, 5.7, 1553, 162.6297797, 748.0969866, 1254, '59.66%'],
    [5.75, 7.1, 1516, 158.7551488, 912.8421054, 1562, '58.44%'],
    [7.39, 9.0, 1472, 154.1474795, 1139.149874, 1980, '57.53%'],
    [7.84, 9.6, 1460, 152.8908425, 1198.664205, 2112, '56.75%']
]

# Ligação Independente 110V
independente_110v = [
    [0.3, 0.0, 807, 84.50884238, 25.35265271, 0, '#DIV/0!'],
    [2.36, 3.1, 784, 82.10028801, 193.7566797, 341, '56.82%'],
    [3.58, 4.5, 751, 78.64453609, 281.5474392, 495, '56.88%'],
    [5.12, 6.3, 736, 77.07373977, 394.6175476, 693, '56.94%'],
    [6.85, 8.3, 714, 74.76990516, 512.1738503, 913, '56.10%']
]

# Ligação Série 220V
serie_220v = [
    [2.9, 5.6, 2193, 229.650423, 665.9862266, 1232, '54.06%'],
    [4.72, 7.2, 1763, 184.6209283, 871.4107815, 1584, '55.01%'],
    [5.71, 8.0, 1615, 169.1224045, 965.6889298, 1760, '54.87%'],
    [6.8, 8.8, 1484, 155.4041166, 1056.747993, 1936, '54.58%'],
    [8.18, 9.8, 1350, 141.3716694, 1156.420256, 2156, '53.64%']
]

# Ligação Série 110V
serie_110v = [
    [1.61, 4.2, 1302, 136.3451212, 219.5156451, 462, '47.51%'],
    [2.8, 5.4, 1017, 106.499991, 298.1999747, 594, '50.20%'],
    [4.56, 7.1, 809, 84.71828189, 386.3153654, 781, '49.46%'],
    [6.25, 8.3, 691, 72.36135079, 452.2584424, 913, '49.54%'],
    [7.3, 9.0, 634, 66.39232475, 484.6639706, 990, '48.96%']
]

# Ligação Composta 220V
composta_220v = [
    [0.42, 0.0, 1779, 186.2964444, 78.24450663, 0, '#DIV/0!'],
    [2.05, 2.9, 1657, 173.5206342, 355.7173002, 638, '55.76%'],
    [2.96, 3.8, 1598, 167.3421687, 495.3328193, 836, '59.25%'],
    [4.93, 5.9, 1477, 154.6710783, 762.5284161, 1298, '58.75%'],
    [7.27, 8.2, 1356, 141.9999879, 1032.339912, 1804, '57.23%']
]

# Ligação Composta 110V
composta_110v = [
    [0.26, 0.0, 835, 87.44099552, 22.73465884, 0, '#DIV/0!'],
    [2.31, 3.1, 760, 79.58701389, 183.8460021, 341, '53.91%'],
    [4.01, 4.9, 709, 74.24630638, 297.7276886, 539, '55.24%'],
    [5.68, 6.6, 665, 69.63863715, 395.547459, 726, '54.48%'],
    [7.12, 8.0, 623, 65.24040744, 464.511701, 880, '52.79%']
]

# Função para adicionar dados ao DataFrame
def adicionar_dados(ligacao, tensao, dados):
    for linha in dados:
        data['Ligacao'].append(ligacao)
        data['Tensao_V'].append(tensao)
        data['Torque_Nm'].append(linha[0])
        data['Ia_A'].append(linha[1])
        data['Rotacao_rpm'].append(linha[2])
        data['Rotacao_rps'].append(linha[3])
        data['Pmec_W'].append(linha[4])
        data['Peletrica_W'].append(linha[5])
        data['Rendimento'].append(linha[6])

# Adicionando todos os dados
adicionar_dados('Independente', 220, independente_220v)
adicionar_dados('Independente', 110, independente_110v)
adicionar_dados('Serie', 220, serie_220v)
adicionar_dados('Serie', 110, serie_110v)
adicionar_dados('Composta', 220, composta_220v)
adicionar_dados('Composta', 110, composta_110v)

# Criando o DataFrame
df = pd.DataFrame(data)

# Convertendo rendimento para numérico (tratando divisões por zero)
def converter_rendimento(valor):
    if valor == '#DIV/0!':
        return 0.0
    else:
        return float(valor.replace('%', '')) / 100

df['Rendimento_decimal'] = df['Rendimento'].apply(converter_rendimento)


