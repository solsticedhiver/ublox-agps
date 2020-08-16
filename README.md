# ublox-agps

This is a simple python script to download AssistNow data from the u-blox server and then upload it to a u-blox GPS device.

1. Request an access token

  To do so, go to the web site: https://www.u-blox.com/en/assistnow-service-registration-form and submit the form. In a few working days, you will receive a message similar to this:

> Dear XXXXXX
>
> Thank you for your interest in u-blox' online, globally-available assisted GNSS service, AssistNow.
> The service ensures a fast Time-To-First-Fix when using u-blox GNSS receivers, even under poor satellite signal conditions.
>
> The token you will require for initial setup of the service is below.
>
> Token: YYYYYYYYYY
>
> A description of the AssistNow features and services can be found on the following web page:
>
> http://www.u-blox.com/en/assisted-gps.html
>
>
> Kind regards
> u-blox

2. Run the script with the token and your gps device

For example:

    $ python3 ublox-agps.py -t YYYYYYYYYY -d /dev/gps0
    Downloading A-GPS data from u-blox server
    Checksums are OK
    Waiting for GPS to be free
    Writing AGPS data to /dev/gps0
    Done
    :: Warning: we have not checked that the dongle acknowledged the data sent

You can specify your latitude and longitude to get better ephemeris from the server:

    ./ublox-agps.py -t YYYYYYYYYY -d /dev/gps0 --lat 49 --lon 4.78


Tested with ublox-7 (u7) module. Use at your own risk.
