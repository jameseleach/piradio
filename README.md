# Install Instructions

1. Install Raspberry Pi OS to an SD Card.

    Using the the [Raspberry Pi Imager](https://www.raspberrypi.org/software/):
    - Choose "Raspberry Pi OS (other)" > "Raspberry Pi OS Lite (32-bit)"
    - Insert and then select an SD Card.

        **Warning:** All data on this SD Card will be erased

    - Choose "Write", wait until it's complete and then eject the SD Card.

    Reference [https://www.raspberrypi.org](https://www.raspberrypi.org/documentation/installation/installing-images/)

2. Enable SSH and Configure Wi-Fi

    - Re-insert the SD Card.  This should allow you to see a volume named 'boot'.

    - Configure WiFi by creating a file named `wpa_supplicant.conf` on the 'boot' volume.  Here is an example of the proper content:

        ```
        ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
        update_config=1
        country=<Insert 2 letter ISO 3166-1 country code here>

        network={
        ssid="<Name of your wireless LAN>"
        psk="<Password for your wireless LAN>"
        }
        ```

    - Enable SSH by creating an (empty) file named `ssh` on the 'boot' volume.

    - Reference: https://www.raspberrypi.org/documentation/configuration/wireless/headless.md

3. Log in to the Raspberry Pi using SSH and update the system:

    ```
    sudo apt update
    sudo apt upgrade
    ```

4. Run `raspi-config` and make these changes:

    Under "System Options"

    - Change Password
    - Change Hostname

    Under "Interface Options"

    - Enable i2c

    Under "Localisation Options"

    - Change Locale
    - Set TimeZone
    - Set WLAN Country

5. Set the i2c bus speed to 1mhz by adding this to `/boot/config.txt`:

    ```
    # Set i2c bus speed to 1Mhz
    dtparam=i2c_arm_baudrate=1000000
    ```

6. Install and configure Mopidy

    Reference: [https://docs.mopidy.com](https://docs.mopidy.com/en/latest/installation/raspberrypi/#how-to-for-raspbian)

7. Install Mopidy extensions and other required Python modules:

    Search for packages available using `apt search mopidy` first as installing via `apt` is the preferred method of installation.

    Mopidy-AlsaMixer, Mopidy-SomaFM, and Mopidy-MPD are required for this project.  
    Install them using this command:

    ```
    sudo apt install mopidy-alsamixer/stable mopidy-somafm/stable mopidy-mpd/stable
    ```
    
    This is optional:  Mopidy-Local (`sudo apt install mopidy-local/stable`)

    Other packages are only (currently) avaialble via `pip`.  Searching for avaialble packages with `python3 -m pip search mopidy` is broken and likely to remain broken.  Use the web search at https://pypi.org/search/?q=mopidy instead.

    First you might need to install `pip` by using the command:
    
    ```
    sudo apt install python3-pip
    ```

    These packages are required or recommended:

    - [Mopidy-Iris](https://pypi.org/project/Mopidy-Iris/) *
    - [Mopidy-Muse](https://pypi.org/project/Mopidy-Muse/) *
    - [Mopidy-DefaultPlayList](https://pypi.org/project/Mopidy-DefaultPlaylist/)
    - [python-mpd2](https://pypi.org/project/python-mpd2/)
    - [gpiozero](https://pypi.org/project/gpiozero/)
    - [Pillow](https://pypi.org/project/Pillow/)
    - [luma.oled](https://pypi.org/project/luma.oled/)

    You can install them with this command:

    ```
    sudo apt install python3-gpiozero
    sudo python3 -m pip install --upgrade Mopidy-Iris Mopidy-Muse Mopidy-DefaultPlayList python-mpd2 Pillow luma.oled
    ```
    
    Add these configuration blocks to `/etc/mopidy/mopidy.conf`

    ```
    [iris]
    country = US
    locale = en_US

    [muse]
    enabled = true
    # the following are optional values
    mopidy_host = localhost
    mopidy_port = 6680
    mopidy_ssl = false
    snapcast_host = localhost
    snapcast_port = 1780
    snapcast_ssl = false
    
    [defaultplaylist]
    enabled = true
    defaultplaylist_name = Top Hits
    autoplay = true
    shuffle = true
    ```

These new modules might be required... The next bit of time will tell!

* [Mopidy-Pidi](https://pypi.org/project/mopidy-pidi/)
* [Mopidy-Raspberry-GPIO](https://pypi.org/project/mopidy-raspberry-gpio/)
* [PiDi-Display-PIL](https://pypi.org/project/pidi-display-pil/)
* [Mopidy-RotaryEncoder](https://pypi.org/project/Mopidy-RotaryEncoder/)
    `sudo adduser mopidy gpio`

Install them with `sudo python3 -m pip install --upgrade Mopidy-PiDi Mopidy-Raspberry-GPIO pidi-display-pil`

# ToDo:

- Implement default volume
- Timeout for volume screen - return to channel?
- Shorter static sound - no hard stop when the sound is playing?

# Mopidy Config File:

```
pi@jukebox:~ $ sudo cat /etc/mopidy/mopidy.conf
# For information about configuration values that can be set in this file see:
#
#   https://docs.mopidy.com/en/latest/config/
#
# Run `sudo mopidyctl config` to see the current effective config, based on
# both defaults and this configuration file.

[audio]
mixer = alsamixer

[iris]
country = US
locale = en_US

[http]
hostname = ::

[mpd]
hostname = ::

[local]
media_dir = $XDG_DATA_DIR/media

[alsamixer]
card = 0
control = Headphone

[somafm]
dj_as_artist = true
```
