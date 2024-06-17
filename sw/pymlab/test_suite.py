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


#    windgauge.calib_mag(cal)

#### Measurement ###################################################
log_index = 0
meas_freq = 1; #rough frequency of diff. pressure measurement (gps data frequency is 1 Hz)

while True:

    try:
        time.sleep(1/meas_freq)

        mag_hdg_comp = windgauge.get_mag_hdg()
        hdg_ma = mag_hdg_comp

        dp, spd_from_dp = windgauge.get_dp_spd()
        temp = windgauge.get_temp()

        ts = datetime.datetime.utcfromtimestamp(time.time()).isoformat()

        msg = ("%d;%s;%0.2f;%0.2f;%0.2f;%0.3f\n"% (log_index, ts, dp, hdg_ma, spd_from_dp, temp))
        sys.stdout.write("%s; %s; Dp: %+4.2f [Pa]; T: %2.3f [degC]; " % (str(log_index).zfill(4), ts, dp, temp))
        sys.stdout.write("MAG_HDG: %+4.2f; SPD_W_DP: %+4.2f [km/h]\n" % (hdg_ma, spd_from_dp))
        sys.stdout.flush()

    except KeyboardInterrupt:
        windgauge.stop()
        print("\nMeasurement stopped!\n")
        log_file.close()
        sys.exit(0)

    except IOError:

        sys.stdout.write("\r\n************ I2C Error\r\n\n")
        time.sleep(0.1)
        windgauge.reset()
        windgauge.initialize()

