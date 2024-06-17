from pymlab import config
import time
import sys
import math
import datetime
import os

#### Script Arguments ###############################################

if len(sys.argv) not in (2, 3, 4):
    sys.stderr.write("Invalid number of arguments.\n")
    sys.stderr.write("Usage: %s #I2CPORT [Config number] \n" % (sys.argv[0], ))
    sys.exit(1)

port = eval(sys.argv[1])


cfg_number = 0

cfglist=[
    config.Config(
        i2c = {
            "port": port,
            "device": "smbus",
        },
        bus = [
            {
                "name":        "windgauge",
                "type":        "WINDGAUGE03A",
            },
        ],
    ),
]

try:
    cfg = cfglist[cfg_number]
except IndexError:
    sys.stdout.write("Invalid configuration number.\n")
    sys.exit(1)

windgauge = cfg.get_device("windgauge")
windgauge.reset()
windgauge.initialize()
time.sleep(0.1)

if cal > 0:
    windgauge.calib_mag(cal)

#### Measurement ###################################################
log_index = 0
meas_freq = 10; #rough frequency of diff. pressure measurement (gps data frequency is 1 Hz)
gps_raw = ""
first = True

while True:

    try:
        if error == True:
            windgauge.reset()
            windgauge.initialize()
            error = False

        time.sleep(0.01)

        mag_hdg_comp = windgauge.get_mag_hdg()
        new_hdg = mag_hdg_comp
        hdg_ma, hdg_vect, prev_hdg_ma = heading_ma(new_hdg, hdg_vect, ma_len, prev_hdg_ma)

        dp, spd_from_dp = windgauge.get_dp_spd()
        temp = windgauge.get_temp()

        ts = datetime.datetime.utcfromtimestamp(time.time()).isoformat()

        # print ("Heading: %6.2f [deg]; Diff. P: %7.2f [Pa]; Speed from diff. P: %5.2f [km/h]" % (hdg_ma, dp, spd_from_dp))
        if gps:

            gps_data = gpsd.get_current()
            # gps_heading = gps_data.get_time().timestamp()
            gps_heading = gps_data.track
            gps_time = gps_data.time
            gps_gspd = gps_data.hspeed
            # gps_pos= gps_data.position()
            lat, lon, alt = gps_data.lat, gps_data.lon, gps_data.alt
            print(lat, lon, alt)

            msg = ("%d;%s;%0.2f;%0.2f;%0.2f;%0.3f;%s;%s;%s;%s;%s;%f\n"% (log_index, ts, dp, hdg_ma, spd_from_dp, temp, gps_time, gps_heading, gps_gspd, lat, lon, alt))
            # print(msg)
            log_file.write(msg)
            sys.stdout.write("%s; %s; Dp: %+4.2f [Pa]; T: %2.3f [degC];" % (str(log_index).zfill(4), ts, dp, temp))
            sys.stdout.write(" gps_heading: %s; GPS_HDG: %s [deg]; GPS_GS: %s [m/s]\n" % (gps_heading, gps_time, gps_gspd))
            sys.stdout.write("      MAG_HDG: %+4.2f; SPD_W_DP: %+4.2f [km/h]\n" % (hdg_ma, spd_from_dp))
            sys.stdout.flush()

        else:
            msg = ("%d;%s;%0.2f;%0.2f;%0.2f;%0.3f\n"% (log_index, ts, dp, hdg_ma, spd_from_dp, temp))
            sys.stdout.write("%s; %s; Dp: %+4.2f [Pa]; T: %2.3f [degC]; " % (str(log_index).zfill(4), ts, dp, temp))
            sys.stdout.write("MAG_HDG: %+4.2f; SPD_W_DP: %+4.2f [km/h]\n" % (hdg_ma, spd_from_dp))
            sys.stdout.flush()
            log_file.write(msg)

        log_index += 1

    except KeyboardInterrupt:
        windgauge.stop()
        print("\nMeasurement stopped!\n")
        log_file.close()
        sys.exit(0)

    except IOError:

        sys.stdout.write("\r\n************ I2C Error\r\n\n")
        time.sleep(0.1)
        error = True
