import os
import pandas as pd
import numpy as np
import dws_processing_transpositions as transpos
import dws_processing_plotting as plot

#dir = r"C:\Users\xkadj\OneDrive\valeo\dewesoft"
#input_file = "TEST_UFO_20191017.txt"
dir = r"C:\Users\xkadj\OneDrive\valeo\191114_ARM_DEWESOFT_NOVATEL\dewesoft_data\petr_posvic\DATA\used"
input_files = []
input_files.append("Precision_test_OSTRY_2019_11_14_0000_B.txt")
input_files.append("Precision_test_OSTRY_2019_11_14_0001_B.txt")
#input_files.append("Precision_test_OSTRY_2019_11_14_0002_B.txt")
#input_files.append("Precision_test_OSTRY_2019_11_14_0003_B.txt")
#input_files.append("Precision_test_OSTRY_2019_11_14_0004_B.txt")
#input_files.append("Precision_test_OSTRY_2019_11_14_0005_B.txt")
#input_files.append("Precision_test_OSTRY_2019_11_14_0006_B.txt")
#input_files.append("Precision_test_OSTRY_2019_11_14_0007_B.txt")



#point_zero = [50.07478605085059,14.52025289904692,235.05]
point_zero = [50.07478605085059,14.52025289904692,235.05]



#50.074778, 14.520278
#50.0747752316345 	15.520285814262566

for input_file in input_files:

    print(' - file:' + str(os.path.join(dir, input_file)))
    print(' - reference point:')
    print('   - latitude: ' + str(point_zero[0]) + '°')
    print('   - longitude: ' + str(point_zero[1]) + '°')
    print('   - altitude: ' + str(point_zero[2]) + ' m')
    print(' - dewesoft parsing started')

#    dewesoft = pd.read_csv(os.path.join(dir, input_file), sep='[	,\t]', skiprows=10, nrows = 50, engine='python')
    dewesoft = pd.read_csv(os.path.join(dir, input_file), sep='[	,\t]', skiprows=10, engine='python')

    dewesoft = dewesoft.reset_index()
    dewesoft["utc_time"] = transpos.get_seconds(dewesoft["index"].str.split(" ", expand = True)[1].str.split(":", expand = True))
    #dewesoft["lat"] = transpos.get_coordinate_dws(dewesoft["Latitude (')"])
    #dewesoft["lon"] = transpos.get_coordinate_dws(dewesoft["Longitude (')"])
    dewesoft["lat"] = transpos.get_coordinate_dws(dewesoft["Lat_Rear_antena (')"])
    dewesoft["lon"] = transpos.get_coordinate_dws(dewesoft["Long_Rear_antena (')"])

    dewesoft = dewesoft.rename(columns={"System_status (-)": "status_sys",
                                        "GNSS_status (-)": "status_gnss",
                                        "Height (m)": "height"})

    dewesoft = dewesoft[["utc_time","lat","lon","height","status_gnss","status_sys"]]

    frequence = 20
    dewesoft = dewesoft.loc[(dewesoft['utc_time'] * frequence) % 1 == 0]

    dewesoft.insert(len(dewesoft.count())-3, 'lat_in_rad', dewesoft.lat*np.pi/180, allow_duplicates=False)
    dewesoft.insert(len(dewesoft.count())-3, 'lon_in_rad', dewesoft.lon*np.pi/180, allow_duplicates=False)

    wgs = dewesoft[['lat_in_rad','lon_in_rad','height']].values
    xyz = transpos.wgs2xyz(wgs)
    enu = transpos.xyz2enu(xyz,point_zero)

    dewesoft["east"], dewesoft["north"], dewesoft["up"] = enu.T[0], enu.T[1], enu.T[2]
    print(' - dewesoft parsing done, ' + str(len(dewesoft)) + ' points')
    #
    ##dewesoft["time_dev"] = dewesoft.utc_time - dewesoft.log_time
    #max_time_dev = max([abs(max(dewesoft.utc_time - dewesoft.log_time)), abs(min(dewesoft.utc_time - dewesoft.log_time))])
    #print(' - maximal deviation (utc_time - log_time) = ' + str(max_time_dev) + ' s')

    dewesoft["raw_speed"] = ((dewesoft.east.diff().pow(2) + dewesoft.north.diff().pow(2)).pow(1/2) / dewesoft.utc_time.diff()).fillna(0) * 3.6


    dewesoft = dewesoft.drop(['lat_in_rad','lon_in_rad'],1)
#    dewesoft = dewesoft.drop(['east','north','up','raw_speed'],1)


    # =============================================================================
    # PLOTTING
    # =============================================================================
    plot.plot_map(dewesoft)
    plot.plot_status(dewesoft)
    plot.plot_height(dewesoft)
    plot.plot_speed(dewesoft)

    print(' - dewesoft plotting done')

#    output_path = os.path.join(dir, str(input_file[:-4] + '_parsed.csv'))
#    dewesoft.drop(['east','north','up','raw_speed'],1).to_csv(output_path,sep=';')
#
#    print(' - dewesoft parsed file saved as:' + output_path)