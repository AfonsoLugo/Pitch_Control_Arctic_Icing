import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file = pd.read_csv('Aerodynamic_data.csv')
lbda = np.arange(0,20.1,0.1)
Nb = 3
angle = file['angle']
plt.style.use('seaborn-darkgrid')
#Etemaddar (2012)
d_ice = file['d_et_ice']
l_ice = file['l_et_ice']
l_clean = file['l_et_clean']
d_clean = file['d_et_clean']
####### Calculate Cp,max for each combination of theoretical Cd/Cl according to Wilson's equation
############# Icing #############
## Maximum Cp and optimum lambda
for i in range(len(angle)):
    cp_6 = (16/27)*lbda*( (Nb**(2/3) / (1.48 + (Nb**(2/3) - 0.04)*lbda + 0.0025*(lbda**2))) - ((d_ice[6]/l_ice[6])*(1.92*Nb*lbda/(1+2*Nb*lbda)))) # opt angle
    cp_5 = (16/27)*lbda*( (Nb**(2/3) / (1.48 + (Nb**(2/3) - 0.04)*lbda + 0.0025*(lbda**2))) - ((d_ice[5]/l_ice[5])*(1.92*Nb*lbda/(1+2*Nb*lbda)))) # non-opt angle

# Values for Optimized case
cp_max_6 = np.nanmax(cp_6) # Maximum Cp for angle = 6
print('Optimized Cp is: '+str(cp_max_6))
lbda_opt = lbda[np.nanargmax(cp_6)] # Lambda for maximum Cp
print('The optimum lambda for optimized condition is: '+str(lbda_opt))

############# Clean #############
## Maximum Cp and optimum lambda
for i in range(len(angle)):
    cp_c_5 = (16/27)*lbda*( (Nb**(2/3) / (1.48 + (Nb**(2/3) - 0.04)*lbda + 0.0025*(lbda**2))) - ((d_clean[5]/l_clean[5])*(1.92*Nb*lbda/(1+2*Nb*lbda))))
# Values
cp_max_c_5 = np.nanmax(cp_c_5) # Maximum Cp for angle = 0
print('The maximum Cp for clean condition is: '+str(cp_max_c_5))
lbda_c_opt = lbda[np.nanargmax(cp_c_5)] # Lambda for maximum Cp
print('The optimum lambda for clean condition is: '+str(lbda_c_opt))

# Cp for only optimized angle
index_lbdaoptc = np.nanargmax(cp_c_5) #index of the optimum lambda for clean case
cp_optangle = cp_6[index_lbdaoptc] #cp of the icing for the optimum lambda for clean case
print('Cp for only optimized angle is: ' + str(cp_optangle))

# Cp for non optimized case
cp_nonopt = cp_5[index_lbdaoptc]
print('Cp for non-optimized case is: ' + str(cp_nonopt))

# PLOT
y_max = 0.5
point_opt = [lbda_opt, cp_max_6] # point for optimized case
point_optangle = [lbda_c_opt, cp_optangle] # point for only optimized angle
point_nonopt = [lbda_c_opt, cp_nonopt] # point for non optimized case
circle_rad = 4
c_rad2 = 3

plt.plot(lbda,cp_6,label="α = 6º", color = '#1F77B4') # Curve for opt angle
plt.plot(lbda,cp_5,label="α = 5º", color = '#565656') # Curve for non-opt angle
plt.plot(lbda_opt, cp_max_6, 'o', ms=circle_rad*2, mec='g', mfc='none', mew=1) # circle for optimization
plt.axvline(lbda_opt, ymin=0, ymax=cp_max_6/y_max, color='green', linestyle='--') # dashed line for optimization
plt.annotate('Cp,opt = '+str(round(cp_max_6,4)), xy=(lbda_opt, cp_max_6), xytext=(lbda_opt-2, cp_max_6+0.03))

plt.plot(lbda_c_opt, cp_optangle, 'o', ms=c_rad2*2, mec='y', mfc='none', mew=2) # circle for optimized angle
plt.axvline(lbda_c_opt, ymin=0, ymax=cp_optangle/y_max, color='y', linestyle='--') # dashed line for icing optimized angle
plt.annotate('Cp,α-opt = '+str(round(cp_optangle,4)), xy=(lbda_c_opt, cp_optangle), xytext=(lbda_c_opt+0.5, cp_optangle))

plt.plot(lbda_c_opt, cp_nonopt, 'o', ms=c_rad2*2, mec='r', mfc='none', mew=1) # circle for optimized angle
plt.axvline(lbda_c_opt, ymin=0, ymax=cp_nonopt/y_max, color='red', linestyle='--') # dashed line for icing optimized angle
plt.annotate('Cp,non-opt = '+str(round(cp_nonopt,4)), xy=(lbda_c_opt, cp_nonopt), xytext=(lbda_c_opt+1, cp_nonopt-0.01))

plt.ylabel('Power Coefficient', fontsize = 14)
plt.yticks(fontsize = 12)
plt.ylim(0,y_max)
plt.xlabel('Tip to Speed Ratio λ', fontsize = 14)
plt.xlim(0,20)
plt.xticks(fontsize = 12)
plt.legend()
plt.tight_layout()
plt.show()
