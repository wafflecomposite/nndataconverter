import os
#import pyquaternion # pip install pyquaternion

### OPTIONS

# original MT data recordings directory
mt_data_dir = "mt_data"

# MT data + output angle delta data directory
mt_data_output_angle_delta_dir = "mt_data_oad"

# choose what to convert
conversions = {
    "MT_TO_MT_OAD": False
}



current_dir = os.path.abspath(os.getcwd())
dirs = [
    mt_data_dir, # 0
    mt_data_output_angle_delta_dir # 1
]

for index, dir in enumerate(dirs):
    dirs[index] = dir = os.path.join(current_dir, dir)
    if not os.path.exists(dir):
        os.mkdir(dir)
        


if conversions["MT_TO_MT_OAD"]:
        
    print("Converting [original MT] data to [MT + output delta angle] data")
    src = dirs[0]
    tgt = dirs[1]
    print(f"Source folder: {src}")
    print(f"Target folder: {tgt}")
    listdir = os.listdir(src)
    filecounter = 1
    for src_filename in listdir:
        src_filepath = os.path.join(src, src_filename)
        print(f"Processing {src_filename} [{filecounter}/{len(listdir)}]")
        # splitted filename
        sf = src_filename.replace("-", "_").split("_")
        tgt_filename = f"MT_OAD_{sf[1]}_{sf[2]}-{sf[3]}-{sf[4]}-{sf[5]}.txt"
        tgt_filepath = os.path.join(tgt, tgt_filename)
        # print(tgt_filepath)
        filecounter += 1
        if os.path.isfile(tgt_filepath):
            print("Skipping, file already exist.")
            continue
        with open(src_filepath) as s:
            with open(tgt_filepath, 'a') as t:
                initialized = False
                prev_roll = 0.0
                prev_pitch = 0.0
                prev_yaw = 0.0

                #md1, md2, md3 = 0.0, 0.0, 0.0
                t.write("#MT_OAD\n")
                t.write("PacketCounter\tSampleTimeFine\tAcc_X\tAcc_Y\tAcc_Z\tGyr_X\tGyr_Y\tGyr_Z\tMag_X\tMag_Y\tMag_Z\tQuat_q0\tQuat_q1\tQuat_q2\tQuat_q3\tRoll\tPitch\tYaw\tRoll_Delta\tPitch_Delta\tYaw_Delta\n")
                for line in s.readlines():
                    if line.startswith("//") or line.startswith("PacketCounter"):
                        continue
                    # splitted_line
                    sl = line.replace("\n", "").split("\t")
                    roll, pitch, yaw = float(sl[15]), float(sl[16]), float(sl[17])
                    if initialized:
                        delta_r, delta_p, delta_y = roll - prev_roll, pitch - prev_pitch, yaw - prev_yaw
                    else:
                        delta_r, delta_p, delta_y = 0.0, 0.0, 0.0
                        initialized = True

                    if delta_r < -180.0: delta_r += 360.0
                    elif delta_r > 180.0: delta_r -= 360.0

                    if delta_y < -180.0: delta_y += 360.0
                    elif delta_y > 180.0: delta_y -= 360.0

                    #if delta_r < -90.0: delta_r += 180.0
                    #elif delta_r > 90.0: delta_r -= 180.0

                    #if delta_y < -90.0: delta_y += 180.0
                    #elif delta_y > 90.0: delta_y -= 180.0

                    #if delta_p < -90.0: delta_p += 180.0
                    #elif delta_p > 90.0: delta_p -= 180.0

                    #if abs(delta_r) > md1: md1 = abs(delta_r)
                    #if abs(delta_p) > md2: md2 = abs(delta_p)
                    #if abs(delta_y) > md3: md3 = abs(delta_y)

                    prev_roll, prev_pitch, prev_yaw = roll, pitch, yaw
                    sl.extend(["{:.6f}".format(delta_r), "{:.6f}".format(delta_p), "{:.6f}".format(delta_y)])
                    t.write("\t".join(sl) + "\n")
                #print(f"{md1}, {md2}, {md3}")

