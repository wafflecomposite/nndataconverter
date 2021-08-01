import pandas as pd
import matplotlib.pyplot as plt

import os

current_dir = os.path.abspath(os.getcwd())

mt_data_output_angle_delta_dir = "mt_data_oad"
data_file_name = "MT_OAD_03782067_000-2021-07-05.txt"

t = pd.read_csv(os.path.join(current_dir, mt_data_output_angle_delta_dir, data_file_name), sep='	', skiprows=1)
print(t.describe())

plt.plot(t["SampleTimeFine"], t["Roll_Delta"],  label = "Roll_Delta"  )
plt.plot(t["SampleTimeFine"], t["Pitch_Delta"], label = "Pitch_Delta" )
plt.plot(t["SampleTimeFine"], t["Yaw_Delta"],   label = "Yaw_Delta"   )
plt.legend()
plt.show()