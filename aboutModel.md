[< back to main](http://nell-byler.github.io/cloudyfsps/)
# Model Specifics
The nebular model integrated within FSPS is fully described in [Byler+2017](http://adsabs.harvard.edu/abs/2017ApJ...840...44B). We include some of the model specifics here.

## Isochrone sets
The nebular model is available for [MIST](http://waps.cfa.harvard.edu/MIST/),Padova+Geneva, and PARSEC evolutionary tracks.

## Abundances

Solar abundances are from Anders & Grevasse (1989) and depletion factors are from Dopita et al. (2000).

| Element | log Z/Zsun | log D |
| :--- | :---: | :---: |
| H   | 0.00	| 0.00 |
| He  | -1.01 | 0.00 |
| C   | -3.44 | -0.30 |
| N   | -3.95 | -0.22 |
| O   | -3.07 | -0.22 |
| Ne  | -3.91 | 0.00 |
| Mg  | -4.42 | -0.70 |
| Si  | -4.45 | -1.0 |
| S   | -4.79 | 0.00 |
| Ar  | -5.44 | 0.00 |
| Ca  | -5.64 | -2.52 |
| Fe  | -4.33 | -2.0 |

Nitrogen has a secondary nucleosynthetic contribution at high metallicities, we use the piecewise function from Dopita+2001 to describe this behavior.

log N/H = -4.57 + log Z/Zsun if log Z/Zsun <= -0.63  
log N/H = -3.94 + (2.0*logZ) if log Z/Zsun > -0.63  

## Stellar Library and IMF

The nebular model uses the C3K stellar library and a Kroupa IMF.

## Nebular Geometry

The inner radius of the nebular region is fixed at log R_inner = 19 (cm, ~3.2 pc). The density of the gas is fixed at n_H = 100 cm^-3.

# Emission lines included in the nebular model

| Wavelength (A) | Line ID | Cloudy ID |
| :--- | :---: | :---: |
| 923.148 | Ly 923 | `H  1 923.156A` |
| 926.249 | Ly 926 | `H  1 926.231A` |
| 930.751 | Ly 930 | `H  1 930.754A` |
| 937.814 | Ly 937 | `H  1 937.809A` |
| 949.742 | Ly-delta 949 | `H  1 949.749A` |
| 972.517 | Ly-gamma 972 | `H  1 972.543A` |
| 1025.728 | Ly-beta 1025 | `H  1 1025.73A` |
| 1215.6701 | Ly-alpha 1216 | `H  1 1215.68A` |
| 1640.42 | He II 1640 | `He 2 1640.00A` |
| 1661.241 | O III] 1661 | `O  3 1661.00A` |
| 1666.15 | O III] 1666 | `O  3 1666.00A` |
| 1812.205 | [Ne III] 1815 | `Ne 3 1815.00A` |
| 1854.716 | [Al III] 1855 | `Al 3 1855.00A` |
| 1862.7895 | [Al III] 1863 | `Al 3 1863.00A` |
| 1906.68 | [C III]  | `C  3 1907.00A` |
| 1908.73 | [C III]  | `C  3 1910.00A` |
| 2142.3 | N II] 2141 | `N  2 2141.00A` |
| 2321.664 | [O III] 2321 | `O  3 2321.00A` |
| 2324.21 | C II] 2326 | `C  2 2324.00A` |
| 2325.4 | C II] 2326 | `C  2 2325.00A` |
| 2326.11 | C II] 2326 | `C  2 2327.00A` |
| 2327.64 | C II] 2326 | `C  2 2328.00A` |
| 2328.83 | C II] 2326 | `C  2 2329.00A` |
| 2471.088 | [O II] 2471 | `O II 2471.00A` |
| 2661.146 | [Al II] 2660 | `Al 2 2660.00A` |
| 2669.951 | [Al II] 2670 | `Al 2 2670.00A` |
| 2796.352 | Mg II 2800 | `Mg 2 2795.53A` |
| 2803.53 | Mg II 2800 | `Mg 2 2802.71A` |
| 3109.98 | [Ar III] 3110 | `Ar 3 3109.00A` |
| 3343.5 | [Ne III] 3343 | `Ne 3 3343.00A` |
| 3722.75 | [S III] 3723 | `S  3 3722.00A` |
| 3727.1 | [O II] 3726 | `O II 3726.00A` |
| 3729.86 | [O II] 3729 | `O II 3729.00A` |
| 3798.987 | H 3798 | `H  1 3797.92A` |
| 3836.485 | H 3835 | `H  1 3835.40A` |
| 3869.86 | [Ne III] 3870 | `Ne 3 3869.00A` |
| 3889.75 | He I 3889 | `He 1 3888.63A` |
| 3890.166 | H 3889 | `H  1 3889.07A` |
| 3968.59 | [Ne III] 3968 | `Ne 3 3968.00A` |
| 3971.198 | H 3970 | `H  1 3970.09A` |
| 4069.75 | [S II] 4070 | `S II 4070.00A` |
| 4077.5 | [S II] 4078 | `S II 4078.00A` |
| 4102.892 | H-delta 4102 | `H  1 4101.76A` |
| 4341.692 | H-gamma 4340 | `H  1 4340.49A` |
| 4364.435 | [O III] 4364 | `TOTL 4363.00A` |
| 4472.735 | He I 4472 | `He 1 4471.47A` |
| 4622.864 | [C I] 4621 | `C  1 4621.00A` |
| 4725.47 | [Ne IV] 4720 | `Ne 4 4720.00A` |
| 4862.71 | H-beta 4861 | `H  1 4861.36A` |
| 4960.295 | [O III] 4960 | `O  3 4959.00A` |
| 5008.24 | [O III] 5007 | `O  3 5007.00A` |
| 5193.27 | [Ar III] 5193 | `Ar 3 5192.00A` |
| 5201.705 | [N I] 5200 | `N  1 5200.00A` |
| 5519.242 | [Cl III] 5518 | `Cl 3 5518.00A` |
| 5539.411 | [Cl III] 5538 | `Cl 3 5538.00A` |
| 5578.89 | [O I] 5578 | `O  1 5577.00A` |
| 5756.19 | [N II] 5756 | `N  2 5755.00A` |
| 5877.249 | He I 5877 | `He 1 5875.61A` |
| 6302.046 | [O I] 6302 | `O  1 6300.00A` |
| 6313.81 | [S III] 6314 | `S  3 6312.00A` |
| 6365.535 | [O I] 6365 | `O  1 6363.00A` |
| 6549.86 | [N II] 6549 | `N  2 6548.00A` |
| 6564.6 | H-alpha 6563 | `H  1 6562.85A` |
| 6585.27 | [N II] 6585 | `N  2 6584.00A` |
| 6679.995 | He I 6680 | `He 1 6678.15A` |
| 6718.294 | [S II] 6717 | `S II 6716.00A` |
| 6732.673 | [S II] 6732 | `S II 6731.00A` |
| 7067.138 | He I 7065 | `He 1 7065.18A` |
| 7137.77 | [Ar III] 7138 | `Ar 3 7135.00A` |
| 7321.94 | [O II] 7323 | `O II 7323.00A` |
| 7332.21 | [O II] 7332 | `O II 7332.00A` |
| 7334.17 | [Ar IV] 7330 | `Ar 4 7331.00A` |
| 7753.19 | [Ar III] 7753 | `Ar 3 7751.00A` |
| 8581.06 | [Cl II] 8579 | `Cl 2 8579.00A` |
| 8729.53 | [C I] 8727 | `C  1 8727.00A` |
| 9017.8 | Pa 9015 | `H  1 9014.92A` |
| 9071.1 | [S III] 9071 | `S  3 9069.00A` |
| 9126.1 | [Cl II] 9124 | `Cl 2 9124.00A` |
| 9232.2 | Pa 9229 | `H  1 9229.03A` |
| 9533.2 | [S III] 9533 | `S  3 9532.00A` |
| 9548.8 | Pa 9546 | `H  1 9545.99A` |
| 9852.96 | [C I] 9850 | `TOTL 9850.00A` |
| 10052.6 | Pa-delta 10050 | `H  1 1.00494m` |
| 10323.32 | [S II] 10331 | `S  2 1.03300m` |
| 10832.057 | He I 10829 | `He 1 1.08299m` |
| 10833.306 | He I 10833 | `He 1 1.08303m` |
| 10941.17 | Pa-gamma 10939 | `H  1 1.09381m` |
| 12570.21 | [Fe II] 1.26um | `Fe 2 1.25668m` |
| 12821.578 | Pa-beta 12819 | `H  1 1.28181m` |
| 17366.885 | Br 17363 | `H  1 1.73621m` |
| 18179.2 | Br 18175 | `H  1 1.81741m` |
| 18756.4 | Pa-alpha 18752 | `H  1 1.87511m` |
| 19450.89 | Br-delta 19447 | `H  1 1.94456m` |
| 21661.178 | Br-gamma 21657 | `H  1 2.16553m` |
| 26258.71 | Br-beta 26254 | `H  1 2.62515m` |
| 30392.02 | Pf 30386 | `H  1 3.03837m` |
| 32969.8 | Pf-delta 32964 | `H  1 3.29609m` |
| 37405.76 | Pf-gamma 37398 | `H  1 3.73953m` |
| 40522.79 | Br-alpha 40515 | `H  1 4.05116m` |
| 46537.8 | Pf-beta 46529 | `H  1 4.65250m` |
| 51286.5 | Hu-delta 51277 | `H  1 5.12725m` |
| 59082.2 | Hu-gamma 59071 | `H  1 5.90659m` |
| 69852.74 | [Ar II] 7um | `Ar 2 6.98000m` |
| 74599.0 | Pf-alpha 74585 | `H  1 7.45781m` |
| 75024.4 | Hu-beta 75011 | `H  1 7.50043m` |
| 89913.8 | [Ar III] 9um | `Ar 3 9.00000m` |
| 105105.0 | [S IV] 10.5um | `S  4 10.5100m` |
| 123719.12 | Hu-alpha 12.4um | `H  1 12.3685m` |
| 128135.48 | [Ne II] 12.8um | `Ne 2 12.8100m` |
| 143678.0 | [Cl II] 14.4um | `Cl 2 14.4000m` |
| 155551.0 | [Ne III] 15.5um | `Ne 3 15.5500m` |
| 187130.0 | [S III] 18.7um | `S  3 18.6700m` |
| 218302.0 | [Ar III] 22um | `Ar 3 21.8300m` |
| 328709.0 | [P II] 32um | `P  2 32.8700m` |
| 334800.0 | [S III] 33.5um | `S  3 33.4700m` |
| 348140.0 | [Si II] 35um | `Si 2 34.8140m` |
| 360135.0 | [Ne III] 36um | `Ne 3 36.0140m` |
| 518145.0 | [O III] 52um | `O  3 51.8000m` |
| 573300.0 | [N III] 57um | `N  3 57.2100m` |
| 606420.0 | [P II] 60um | `P  2 60.6400m` |
| 631852.0 | [O I] 63um | `O  1 63.1700m` |
| 883564.0 | [O III] 88um | `O  3 88.3300m` |
| 1218000.0 | [N II] 122um | `N  2 121.700m` |
| 1455350.0 | [O I] 145um | `O  1 145.530m` |
| 1576429.62 | [C II] 157.7um | `C  2 157.600m` |
| 2053000.0 | [N II] 205um | `N  2 205.400m` |
| 3703700.0 | [C I] 369um | `C  1 369.700m` |
| 6097000.0 | [C I] 610um | `C  1 609.200m` |
