
import pandas as pd


value_roughness_9 = 0.118
value_mean_curvature_3 = 0.056
value_roughness_3 = 0.02
value_illuminance = 0.85

def filter(input):
    """
    :param input: input file
    :return: returns df
    """

    my_data = pd.read_csv(input, sep=';')
    my_data = my_data.rename(columns={'//X': 'X'})
    my_data = my_data.dropna(how='any', axis=0)

    costum = my_data[(my_data['Roughness (9)'] > value_roughness_9)
                     & (my_data['Illuminance (PCV)'] < value_illuminance)
                     & (my_data['Mean curvature (3)'] > value_mean_curvature_3)
                     & (my_data['Roughness (3)'] > value_roughness_3)]

    print("Points in filtered Cloud:", len(costum.index))

    return costum


if __name__ == '__main__':

    input_file = input("path to input file (csv): ")
    filter(input_file)