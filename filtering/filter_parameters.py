import numpy as np
import pandas as pd
from utils import calculations


value_roughness_9 = 0.118
value_mean_curavture_3 = 0.056
value_roughness_3 = 0.02
value_illuminance = 0.85

def filter(input, output='../tmp/filter_tmp.txt'):

    my_data = pd.read_csv(input, sep=';')
    my_data = my_data.rename(columns={'//X': 'X'})
    my_data = my_data.dropna(how='any', axis=0)

    #xyzArray = my_data.filter(items=['X', 'Y', 'Z']).to_numpy()

    #my_data['Verticality (2)'] = calculations.getVerticalitiy(xyzArray)

    costum = my_data[(my_data['Roughness (9)'] > value_roughness_9) & (my_data['Illuminance (PCV)'] < value_illuminance)
                     & (my_data['Mean curvature (3)'] > value_mean_curavture_3) & (
                                 my_data['Roughness (3)'] > value_roughness_3) ]

    print("Points in filtered Cloud:", len(costum.index))

    #costum.to_csv(output, sep=';', index=False)

    return costum