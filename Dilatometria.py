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


ge = pd.read_csv("/home/henrique/pCloudDrive/Pos-doutorado/Resultados/Dilatometria/aco_carbono_exemplo.csv", skiprows=4, delimiter=";")

length = ge.iloc[:,3]
temp = ge.iloc[:,2]
nom_temp = ge.iloc[:,4]

###############################################################################
#                   Adicione informações
###############################################################################

print("A temperatura de tratamento isotérmico do exemplo foi de 850 °C")
temp_iso = float(input("Coloque a temperatura de tratamento isotérmico: "))
print("A temperatura Ac1 do exemplo está proxima de 740 °C")
Ac1_estimado = float(input("Coloque a temperatura Ac1 estimado: "))
print("A temperatura Ac1 do exemplo está proxima de 760 °C")
Ac3_estimado = float(input("Coloque a temperatura Ac3 estimado: "))
print("A temperatura Ac1 do exemplo está proxima de 160 °C")
Ms_estimado = float(input("Coloque a temperatura Ac3 estimado: "))


###############################################################################
#                   Aquecimento
###############################################################################

temp_iso_index = indice_temp(temp, temp_iso)

length_aq = length[:temp_iso_index]
temp_aq = temp[:temp_iso_index]

length_aq = length_aq.tolist()
temp_aq = temp_aq.tolist()

index_ac1_1_1 = indice_temp(temp, Ac1_estimado-20)
index_ac1_1_2 = indice_temp(temp, Ac1_estimado-10)

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

plt.plot(temp_aq,length_aq, color='Blue', label='UHC', linewidth=3)
plt.plot(temp_aq, reg1, ls='--', color='Black', label='Fitted line 1', linewidth=1)
plt.plot(temp_aq, reg2, ls='--', color='Black',  label='Fitted line 2', linewidth=1)
plt.xlabel('Temperature (°C)')
plt.ylabel('Change in Length (µm)')
plt.xticks(np.arange(700, 801, step=10))
plt.yticks(np.arange(90, 131, step=2))
plt.legend()
plt.xlim([720, 800])
plt.ylim([100, 120])
#plt.savefig('UHC-1.png', dpi = 300)
plt.show()

alavanca_per = []
alavanca_aus = []
x_alavanca = temp_aq[424:457]

for i in range(424, 457):
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
plt.xlim([740, 780])
plt.legend()
#plt.savefig('DHH-2.png', dpi = 300)
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

#######################################Ac1:  746.17144775
Acm:  767.82568359
Ms:  147.51338196########################################
#                   Resfriamento
###############################################################################

index_of_element = -1
for i in range(500,len(nom_temp)):
    if nom_temp[i] < 850:
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

plt.plot(temp_resfr,length_resfr, color='Blue', label='UHC', linewidth=3)
plt.plot(temp_resfr, reg3, label='Fitted line', ls='--', color='Black', linewidth=1)
plt.xlabel('Temperature (°C)')
plt.ylabel('Change in Length (µm)')
plt.legend()
plt.xlim([40, 250])
plt.ylim([-40, 20])
#plt.savefig('UHC-3.png', dpi = 300)
plt.show()

###############################################################################
#                   Cálculo de Ms
###############################################################################

Ms = 0

for i in range(1026,len(temp_resfr)):
    aux4 = length_resfr[i] - reg3[i]
    if aux4 > 0.2:
        Ms = temp_resfr[i]
        break
    
print("Ms: ", Ms)





















