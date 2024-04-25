#%% chamda

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy 

def indice_temp(vetor, temp):
    index_of_element = -1
    for i in range(len(vetor)):
        if vetor[i] >= temp:
            index_of_element = i
            break
    return index_of_element

def indice_temp_menor(vetor, temp):
    index_of_element = -1
    for i in range(len(vetor)):
        if vetor[i] <= temp:
            index_of_element = i
            break
    return index_of_element

def encontra_max(vetor):
    maximo = vetor[0]
    for i in range(len(vetor)):
        if vetor[i] > maximo:
            maximo = vetor[i]
    return maximo

def encontra_min(vetor):
    minimo = vetor[0]
    for i in range(len(vetor)):
        if vetor[i] < minimo:
            minimo = vetor[i]
    return minimo

arq = "aco_carbono_exemplo"

nome = "exemplo"

path = arq + ".csv"

ge = pd.read_csv(path, skiprows=4, delimiter=";")

length = ge.iloc[:,3]
temp = ge.iloc[:,2]
nom_temp = ge.iloc[:,4]

###############################################################################
#                   Adicione informações
###############################################################################

# print("A temperatura de tratamento isotérmico do exemplo foi de 850 °C")
# temp_iso = float(input("Coloque a temperatura de tratamento isotérmico: "))
# print("A temperatura Ac1 do exemplo está proxima de 740 °C")
# Ac1_estimado = float(input("Coloque a temperatura Ac1 estimado: "))
# print("A temperatura Ac1 do exemplo está proxima de 760 °C")
# Ac3_estimado = float(input("Coloque a temperatura Ac3 estimado: "))
# print("A temperatura Ac1 do exemplo está proxima de 160 °C")
# Ms_estimado = float(input("Coloque a temperatura Ac3 estimado: "))


# =============================================================================
# Padrão
# =============================================================================

temp_iso = 850
Ac1_estimado =725
Ac3_estimado =820
Ms_estimado = 190

###############################################################################
#                   Aquecimento
###############################################################################

#%% Aquecimento


temp_iso_index = indice_temp(nom_temp, temp_iso)

length_aq = length[:temp_iso_index]
temp_aq = temp[:temp_iso_index]

length_aq = length_aq.tolist()
temp_aq = temp_aq.tolist()

index_ac1_1_1 = indice_temp(temp_aq, Ac1_estimado-20)
index_ac1_1_2 = indice_temp(temp_aq, Ac1_estimado-10)

aux1 = temp_aq[index_ac1_1_1:index_ac1_1_2]
auy1 = length_aq[index_ac1_1_1:index_ac1_1_2]

slope1, intercept1, r_value, p_value, std_err = scipy.stats.linregress(aux1, auy1)

reg1 = []

for i in range(len(temp_aq)):
    a = slope1*temp_aq[i] + intercept1
    reg1 = np.append(reg1, a)
reg1 = reg1. tolist()

index_ac3_1_1 = indice_temp(temp, Ac3_estimado+5)
index_ac3_1_2 = indice_temp(temp, Ac3_estimado+30)

aux2 = temp[index_ac3_1_1:index_ac3_1_2]
auy2 = length[index_ac3_1_1:index_ac3_1_2]

slope2, intercept2, r_value, p_value, std_err = scipy.stats.linregress(aux2, auy2)

reg2 = []

for i in range(len(temp_aq)):
    a = slope2*temp_aq[i] + intercept2
    reg2 = np.append(reg2, a)
reg2 = reg2.tolist()

y1 = indice_temp(temp_aq, Ac1_estimado)
y2 = indice_temp(temp_aq, Ac3_estimado)

length_graf1 = length[y1:y2].tolist()

maxy = encontra_max(length_graf1)

miny = encontra_min(length_graf1)

plt.plot(temp_aq,length_aq, color='Blue', label=nome, linewidth=3)
plt.plot(temp_aq, reg1, ls='--', color='Black', label='Fitted line 1', linewidth=1)
plt.plot(temp_aq, reg2, ls='--', color='Black',  label='Fitted line 2', linewidth=1)
plt.xlabel('Temperature (°C)')
plt.ylabel('Change in Length (µm)')
plt.xticks(np.arange(Ac1_estimado-20, temp_iso, step=10))
plt.yticks(np.arange(miny-10, maxy+10, step=5))
plt.legend()
plt.xlim([Ac1_estimado-10, Ac3_estimado+10])
plt.ylim([miny-10 , maxy+10])
# plt.savefig(nome + "-1" + ".png", dpi = 300)
plt.show()



# =============================================================================
#               Encontrar os indices de alavanca
# =============================================================================

#%% Alavanca

alavanca_per = []
alavanca_aus = []

ind1 = indice_temp(temp_aq, Ac1_estimado)
ind2 = indice_temp(temp_aq, Ac3_estimado)

x_alavanca = temp_aq[ind1:ind2]

for i in range(ind1, ind2):
    aus = (reg1[i]-length_aq[i])/(reg1[i]-reg2[i])
    per = (length_aq[i]-reg2[i])/(reg1[i]-reg2[i])
    if per <= 0:
        per = 0
    if aus <= 0:
        aus = 0
    if per >= 1:
        per = 1
    if aus >= 1:
        aus = 1
    alavanca_per =np.append(alavanca_per, per) 
    alavanca_aus =np.append(alavanca_aus, aus) 

plt.plot(x_alavanca,alavanca_per, color='Orange', label='Perlite', linewidth=2)
plt.plot(x_alavanca,alavanca_aus, color='Blue', label='Austenite', linewidth=2)
plt.xlabel('Temperature (°C)')
plt.ylabel('Phase fraction')
plt.xlim([Ac1_estimado, Ac3_estimado])
plt.legend()
# plt.savefig(nome + "-2" + ".png", dpi = 300)
plt.show()

###############################################################################
#                   Cálculo de Ac1 e Acm
###############################################################################

t_aus_s = 0

for i in range(len(alavanca_aus)):
    if alavanca_aus[i] >= 0.99:
        t_aus_s = x_alavanca[i]
        break

for i in range(len(alavanca_per)):
    if alavanca_aus[i] >= 0.01:
        t_per_s = x_alavanca[i]
        break

print("Ac1: ", t_per_s)
print("Acm: ", t_aus_s)



###############################################################################
#                   Resfriamento
###############################################################################

#%% resfriamento

index_of_element = -1
for i in range(500,len(nom_temp)):
    if nom_temp[i] >= 850:
        index_of_element = i
        break

length_resfr = length[index_of_element:]
temp_resfr = temp[index_of_element:]

length_resfr = length_resfr.tolist()
temp_resfr = temp_resfr. tolist()

index_Ms_1_1 = indice_temp_menor(temp_resfr, Ms_estimado+10)
index_Ms_1_2 = indice_temp_menor(temp_resfr, Ms_estimado+50)

aux3 = temp_resfr[index_Ms_1_2:index_Ms_1_1]
auy3 = length_resfr[index_Ms_1_2:index_Ms_1_1]

slope3, intercept3, r_value, p_value, std_err = scipy.stats.linregress(aux3, auy3)

reg3 = []

for i in range(len(temp_resfr)):
    a = slope3*temp_resfr[i] + intercept3
    reg3 = np.append(reg3, a)
reg3 = reg3.tolist()

Ms = 0

ind2 = indice_temp_menor(temp_resfr, Ms_estimado+20)

for i in range(ind2,len(temp_resfr)):
    aux4 = length_resfr[i] - reg3[i]
    if aux4 > 0.01:
        Ms = temp_resfr[i]
        break


y3 = length_resfr[indice_temp_menor(temp_resfr, 100)]
y4 = length_resfr[indice_temp_menor(temp_resfr, Ms)]

plt.plot(temp_resfr,length_resfr, color='Blue', label=nome, linewidth=3)
plt.plot(temp_resfr, reg3, label='Fitted line', ls='--', color='Black', linewidth=1)
plt.xlabel('Temperature (°C)')
plt.ylabel('Change in Length (µm)')
plt.legend()

if Ms>200:
    plt.xlim([100, Ms+10])
else:
    plt.xlim([100, 200])
plt.ylim([y4-20, y3])
# plt.savefig(nome + "-3" + ".png", dpi = 300)
plt.show()

###############################################################################
#                   Cálculo de Ms
###############################################################################

Ms = 0

ind2 = indice_temp_menor(temp_resfr, Ms_estimado+20)

for i in range(ind2,len(temp_resfr)):
    aux4 = length_resfr[i] - reg3[i]
    if aux4 > 0.02:
        Ms = temp_resfr[i]
        break
    
print("Ms: ", Ms)


# =============================================================================
# Plotagem do grafico geral
# =============================================================================

#%% gráfico geralresfriamento

plt.plot(temp,length, color='Blue', label=nome, linewidth=1)
plt.xlabel('Temperature (°C)')
plt.ylabel('Change in Length (µm)')
plt.xticks(np.arange(0, temp_iso+10, step=100))
plt.yticks(np.arange(int(y4-10)-10, int(length_aq[-1])+20, step=10))
plt.legend()
plt.xlim([0, temp_iso+10])
plt.ylim([int(y4-10)-10, int(length_aq[-1])+10])
# plt.savefig(nome + "-geral" + "png", dpi = 300)
plt.show()

















