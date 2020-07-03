import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file = pd.read_csv('Aerodynamic_data.csv')
lbda = np.arange(0,20.1,0.1)
Nb = 3
angle = file['angle']
plt.style.use('seaborn-darkgrid')
# Homola (2010)
d_ice = file['d_hu_ice']
l_ice = file['l_hu_ice']
l_clean = file['l_hu_clean']
d_clean = file['d_hu_clean']
####### Calculate Cp,max for each combination of theoretical Cd/Cl according to Wilson's equation
############# Icing #############
## Maximum Cp and optimum lambda
for i in range(len(angle)):
    cp_9 = (16/27)*lbda*( (Nb**(2/3) / (1.48 + (Nb**(2/3) - 0.04)*lbda + 0.0025*(lbda**2))) - ((d_ice[9]/l_ice[9])*(1.92*Nb*lbda/(1+2*Nb*lbda))))
    cp_4 = (16/27)*lbda*( (Nb**(2/3) / (1.48 + (Nb**(2/3) - 0.04)*lbda + 0.0025*(lbda**2))) - ((d_ice[4]/l_ice[4])*(1.92*Nb*lbda/(1+2*Nb*lbda))))

cp_max_9 = np.nanmax(cp_9) # Maximum Cp for angle = 0
print('The Optimized Cp is: '+str(round(cp_max_9,4)))
lbda_opt = lbda[np.nanargmax(cp_9)] # Lambda for maximum Cp
print('The optimum lambda for optimized condition is: '+str(round(lbda_opt,1)))

############# Clean #############
for i in range(len(angle)):
    cp_max_c = (16/27)*lbda*( (Nb**(2/3) / (1.48 + (Nb**(2/3) - 0.04)*lbda + 0.0025*(lbda**2))) - ((d_clean[i]/l_clean[i])*(1.92*Nb*lbda/(1+2*Nb*lbda))))

## Maximum Cp and optimum lambda
for i in range(len(angle)):
    cp_c_4 = (16/27)*lbda*( (Nb**(2/3) / (1.48 + (Nb**(2/3) - 0.04)*lbda + 0.0025*(lbda**2))) - ((d_clean[4]/l_clean[4])*(1.92*Nb*lbda/(1+2*Nb*lbda))))
cp_max_c_4 = np.nanmax(cp_c_4) # Maximum Cp for angle = 0
print('The maximum Cp for clean condition is: '+str(round(cp_max_c_4,4)))
lbda_c_opt = lbda[np.nanargmax(cp_c_4)] # Lambda for maximum Cp
print('The optimum lambda for clean condition is: '+str(round(lbda_c_opt,1)))

# Cp for icing case using parameters of clean case
index_lbdaoptc = np.nanargmax(cp_c_4) #index of the optimum lambda for clean case
cp_optangle = cp_9[index_lbdaoptc] #cp of the icing for the optimum lambda for clean case
print('Cp with only angle optimized is: ' + str(round(cp_optangle,4)))

# Cp with no optimization
cp_nonopt = cp_4[index_lbdaoptc]
print('Cp with no optimization is: '+str(round(cp_nonopt,4)))

# PLOT
y_max = 0.5
point_opt = [lbda_opt, cp_max_9] # point for optimized case
point_nonopt = [lbda_c_opt, cp_nonopt] # point for non optimized case
circle_rad = 4
c_rad2 = 3

plt.plot(lbda,cp_4, label="α = 4º", color = '#565656') # Curve for non-optimized angle
plt.plot(lbda,cp_9, label="α = 9º", color = '#1F77B4') # Curve for optimized angle

plt.plot(lbda_opt, cp_max_9, 'o', ms=circle_rad*2, mec='g', mfc='none', mew=1) # circle for optimization
plt.axvline(lbda_opt, ymin=0, ymax=cp_max_9/y_max, color='green', linestyle='--') # dashed line for optimization
plt.annotate('Cp,opt = '+str(round(cp_max_9,4)), xy=(lbda_opt, cp_max_9), xytext=(lbda_opt-2.2, cp_max_9+0.022))

plt.plot(lbda_c_opt, cp_optangle, 'o', ms=c_rad2*2, mec='y', mfc='none', mew=2) # circle for optimized angle
plt.axvline(lbda_c_opt, ymin=0, ymax=cp_optangle/y_max, color='y', linestyle='--') # dashed line for icing optimized angle
plt.annotate('Cp,α-opt = '+str(round(cp_optangle,4)), xy=(lbda_c_opt, cp_optangle), xytext=(lbda_c_opt+0.5, cp_optangle))

plt.plot(lbda_c_opt, cp_nonopt, 'o', ms=c_rad2*2, mec='#DC3838', mfc='none', mew=1) # circle for optimized angle
plt.axvline(lbda_c_opt, ymin=0, ymax=cp_nonopt/y_max, color='#CD4E4E', linestyle='--') # dashed line for icing optimized angle
plt.annotate('Cp,non-opt = '+str(round(cp_nonopt,4)), xy=(lbda_c_opt, cp_nonopt), xytext=(lbda_c_opt+0.5, cp_nonopt-0.01))

plt.ylabel('Power Coefficient', fontsize = 14)
plt.yticks(fontsize = 12)
plt.ylim(0,y_max)
plt.xlabel('Tip to Speed Ratio λ', fontsize = 14)
plt.xlim(0,20)
plt.xticks(fontsize = 12)
plt.legend()
plt.tight_layout()
plt.show()
