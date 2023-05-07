import numpy as np
import pandas as pd
import pytest

from src import generate_features as gf


log_entropy_result = [-3.673006104957646,
                    -3.653512310276645,
                    -2.682382454353632,
                    -3.7172789286356345,
                    -3.803168600516064,
                    -3.223888366691745,
                    -2.913231052042247,
                    -2.2219271899765913,
                    -3.233989462678249,
                    -2.0786418615092717]
log_entropy_result = [round(x,5) for x in log_entropy_result]
entropy_x_contrast_result = [21.916179179999997,
                            17.87952369,
                            21.09170772,
                            21.24964287,
                            18.065510980000003,
                            15.46213284,
                            13.622512500000001,
                            19.55310528,
                            17.075140479999998,
                            29.317184999999995]
entropy_x_contrast_result = [round(x,5) for x in entropy_x_contrast_result]
IR_range_result = [26.644499999999994,
                    25.281200000000013,
                    12.41409999999999,
                    41.7227,
                    49.980500000000006,
                    40.6875,
                    45.85159999999999,
                    18.48830000000001,
                    32.30860000000001,
                    19.964799999999997]
IR_range_result = [round(x,5) for x in IR_range_result]
IR_norm_range_result = [0.16346319018404903,
                        0.15138443113772462,
                        0.07134540229885052,
                        0.26917870967741936,
                        0.33320333333333335,
                        0.3013888888888889,
                        0.48778297872340415,
                        0.11927935483870974,
                        0.2125565789473685,
                        0.12556477987421383]
IR_norm_range_result = [round(x,5) for x in IR_norm_range_result]


visible_mean = [3.0, 3.0, 2.0, 4.0, 7.0, 5.0, 5.0, 3.0, 3.0, 3.0]
visible_max = [140.0, 135.0, 126.0, 197.0, 193.0, 190.0, 144.0, 130.0, 136.0, 124.0]
visible_min = [43.5, 41.9063, 21.0586, 77.4805, 88.8398, 57.1836, 42.0391, 18.2188, 44.7813, 28.5781]
visible_mean_distribution = [0.0833, 0.079, 0.0406, 0.089, 0.0884, 0.0568, 0.0418, 0.0297, 0.0592, 0.0359]
visible_contrast = [862.8417, 690.3291, 308.3583, 874.4709, 810.1126, 388.4958, 250.875, 180.3792, 433.3792, 234.35]
visible_entropy = [0.0254, 0.0259, 0.0684, 0.0243, 0.0223, 0.0398, 0.0543, 0.1084, 0.0394, 0.1251]
visible_second_angular_momentum = [3.889, 3.834, 3.1702, 3.9442, 3.9318, 3.5269, 3.2405, 2.8236, 3.5576, 2.8862]
IR_mean = [163.0, 167.0, 174.0, 155.0, 150.0, 135.0, 94.0, 155.0, 152.0, 159.0]
IR_max = [240.0, 239.0, 240.0, 239.0, 236.0, 236.0, 225.0, 235.0, 238.0, 240.0]
IR_min = [213.3555, 213.7188, 227.5859, 197.2773, 186.0195, 195.3125, 179.1484, 216.5117, 205.6914, 220.0352]
data = {
    'visible_mean': visible_mean,
    'visible_max': visible_max,
    'visible_min': visible_min,
    'visible_mean_distribution': visible_mean_distribution,
    'visible_contrast': visible_contrast,
    'visible_entropy': visible_entropy,
    'visible_second_angular_momentum': visible_second_angular_momentum,
    'IR_mean': IR_mean,
    'IR_max': IR_max,
    'IR_min': IR_min,
}
df_in = pd.DataFrame(data)

config = {'calculate_range': {'IR_range': {'min_col': 'IR_min', 'max_col': 'IR_max'}}, 
         'calculate_norm_range': {'IR_norm_range': {'min_col': 'IR_min', 'max_col': 'IR_max', 'mean_col': 'IR_mean'}}, 
         'log_transform': {'log_entropy': 'visible_entropy'}, 
         'multiply': {'entropy_x_contrast': {'col_a': 'visible_contrast', 'col_b': 'visible_entropy'}}}
config_keyError = {'calculate_range': {'IR_range': {'min_col_wrongKey': 'IR_min', 'max_col': 'IR_max'}}, 
         'calculate_norm_range': {'IR_norm_range': {'min_col_wrongKey': 'IR_min', 'max_col': 'IR_max', 'mean_col': 'IR_mean'}}, 
         'log_transform': {'log_entropy': 'visible_entropy_wrongKey'}, 
         'multiply': {'entropy_x_contrast': {'col_a': 'visible_contrast_wrongKey', 'col_b': 'visible_entropy'}}}


# Unit tests for log transformation on entropy feature =======================================
# Happy path
def test_generate_features_log_transform():
    print(config)
    result_df = gf.log_transform(df_in, config['log_transform'])
    calculated_log_entropy = [round(x,5) for x in result_df['log_entropy']]
    assert calculated_log_entropy==log_entropy_result

# Unhappy path
def test_generate_features_log_transform_wrong_key():
    with pytest.raises(KeyError):
            gf.log_transform(df_in, config_keyError['log_transform'])

# Unit tests for interactions on entropy and contrast feature =======================================
# Happy path
def test_generate_features_multiply():
    result_df = gf.multiply(df_in, config['multiply'])
    calculated_entropy_x_contrast = [round(x,5) for x in result_df['entropy_x_contrast']]
    assert calculated_entropy_x_contrast==entropy_x_contrast_result

# Unhappy path
def test_generate_features_multiply_wrong_key():
    with pytest.raises(KeyError):
            gf.multiply(df_in, config_keyError['multiply'])

# Unit tests for range calculation on IR feature =======================================
# Happy path
def test_generate_features_calculate_range():
    result_df = gf.calculate_range(df_in, config['calculate_range'])
    calculated_range = [round(x,5) for x in result_df['IR_range']]
    assert calculated_range==IR_range_result

# Unhappy path
def test_generate_features_calculate_range_wrong_key():
    with pytest.raises(KeyError):
            gf.calculate_range(df_in, config_keyError['calculate_range'])

# Unit tests for normalized range calculation on IR feature =======================================
# Happy path
def test_generate_features_calculate_norm_range():
    result_df = gf.calculate_norm_range(df_in, config['calculate_norm_range'])
    calculated_norm_range = [round(x,5) for x in result_df['IR_norm_range']]
    assert calculated_norm_range==IR_norm_range_result

# Unhappy path
def test_generate_features_calculate_norm_range_wrong_key():
    with pytest.raises(KeyError):
            gf.calculate_norm_range(df_in, config_keyError['calculate_norm_range'])