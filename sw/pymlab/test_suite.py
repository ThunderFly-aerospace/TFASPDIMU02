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
            "device": "hid",
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


#### Measurement ###################################################
log_index = 0
meas_freq = 10; #rough frequency of diff. pressure measurement (gps data frequency is 1 Hz)
error = False
hdg_vect = []
ma_len = 15   # length of moving average window filter
prev_hdg_ma = 0

def heading_ma(new_hdg, hdg_vect, ma_len, prev_hdg_ma): # function for smoothing heading values with moving average filter

    if new_hdg + 180 < prev_hdg_ma:
            new_hdg += 360
    if new_hdg - 180 > prev_hdg_ma:
        new_hdg -= 360

    prev_hdg_ma = new_hdg
    hdg_vect.append(new_hdg)
    hdg_ma = float(sum(hdg_vect)) / max(len(hdg_vect), 1)
    hdg_ma = hdg_ma % 360

    if hdg_ma < 0:
        hdg_ma += 360

    if len(hdg_vect) == ma_len:
        hdg_vect.pop(0)

    return(hdg_ma, hdg_vect, prev_hdg_ma)

while True:

    try:
        if error == True:
            windgauge.reset()
            windgauge.initialize()
            error = False

        time.sleep(1/meas_freq)

        mag_hdg_comp = windgauge.get_mag_hdg()
        new_hdg = mag_hdg_comp
        hdg_ma, hdg_vect, prev_hdg_ma = heading_ma(new_hdg, hdg_vect, ma_len, prev_hdg_ma)

        dp, spd_from_dp = windgauge.get_dp_spd()
        temp = windgauge.get_temp()

        ts = datetime.datetime.utcfromtimestamp(time.time()).isoformat()

        # print ("Heading: %6.2f [deg]; Diff. P: %7.2f [Pa]; Speed from diff. P: %5.2f [km/h]" % (hdg_ma, dp, spd_from_dp))
        msg = ("%d;%s;%0.2f;%0.2f;%0.2f;%0.3f\n"% (log_index, ts, dp, hdg_ma, spd_from_dp, temp))
        sys.stdout.write("%s; %s; Dp: %+4.2f [Pa]; T: %2.3f [degC]; " % (str(log_index).zfill(4), ts, dp, temp))
        sys.stdout.write("MAG_HDG: %+4.2f; SPD_W_DP: %+4.2f [km/h]\n" % (hdg_ma, spd_from_dp))
        sys.stdout.flush()

    except KeyboardInterrupt:
        windgauge.stop()
        print("\nMeasurement stopped!\n")

        sys.exit(0)

    except IOError:

        sys.stdout.write("\r\n************ I2C Error\r\n\n")
        time.sleep(0.1)
        windgauge.reset()
        windgauge.initialize()

