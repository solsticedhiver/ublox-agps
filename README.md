# ublox-agps
Script to send aiding data to a u-blox GPS module (aka agps)

This is a simple example in python to write AssistNow GPS data downloaded from u-blox server to a u-blox GPS Module.

1. Request an access token

  To do so, go to the web site: https://www.u-blox.com/en/assistnow-service-registration-form and submit the form. In 24 hours, you will receive a message similar to this:

> Get a token
>
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

2. Configure the script

You can either specify the token and the device on the command line by using the `-t` switch and the `-d` switch, or you can modify the script to hard-code both of the variables.

3. Run the script with

`python ublox-agps.py -t YYYYYYYYYY -d /dev/ttyACM0`

**Note:** The idea of this project came from: https://gist.github.com/veproza/55ec6eaa612781ac29e7

Tested in ublox-7 (u7) module
