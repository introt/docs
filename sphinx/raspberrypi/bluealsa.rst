*********************************************************
Bluetooth audio on a headless Raspberry Pi using BlueAlsa
*********************************************************

.. meta::
   :description: Configuring BlueAlsa on a headless Raspberry Pi
   :keywords: Raspberry Pi, Rasbian, Bluetooth, audio, BlueAlsa, ALSA, PulseAudio, BlueZ, mpv, headless, command line, console, terminal

Intro
=====

How to connect a Bluetooth speaker or a pair of Bluetooth headphones to a Rapberry Pi using the command line. **No PulseAudio required!**

Tested on a Raspberry Pi 400 running freshly installed [#install]_ Raspberry Pi OS Lite aka **Rasbian GNU/Linux 10 (Buster)**. Report any issues `on GitHub <https://github.com/introt/docs/issues>`_.

BlueAlsa [#bluealsa]_ is a Bluetooth audio backend for ALSA. It bridges the gap between BlueZ 5 (the Bluetooth stack) and ALSA (the audio stack) without the need for PulseAudio (a fat sound server).

.. Note::

        These instructions don't apply to Rasbian 11 as it doesn't ship a BlueAlsa package.

        Rasbian 12 should include ``bluez-alsa-utils`` [#debianwiki]_; this page will be updated thereafter.

Command lines
=============

:download:`A full terminal log is available here. <bluealsa.txt>`

.. Note:: 

        The prompts have been removed for the best copy-pasting experience. You can highlight whole code blocks, no need to aim for corners!

        Worried about "Pastejacking"? You can clone this website's `git repo <https://github.com/introt/docs>`_ and get hit by malicious build scripts instead or `view this page's raw reST source <https://introt.github.io/docs/_sources/raspberrypi/bluealsa.rst.txt>`_.

Adding the 'pi' user to the 'bluetooth' group
---------------------------------------------

.. code-block:: shell

        sudo usermod -G bluetooth -a pi && logout

Logout is needed for the change to take effect.

Installing and starting the BlueAlsa daemon
-------------------------------------------

.. code-block:: shell

        sudo apt update && sudo apt install bluealsa -y && \ 
        sudo service bluealsa start

On Debian and derivatives the service will be enabled on startup by default.

Connecting a Bluetooth device
-----------------------------

.. warning::

        The code blocks in this section can not be copy-pasted.

        Lines with commands to enter are emphasized.

The ``00:00:00:00:00:00`` and ``AA:BB:CC:DD:EE:FF`` below stand for the MAC addresses of your Bluetooth controller and audio device, respectively. You'll find them out soon.

Using bluetoothctl interactively
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Automating ``bluetoothctl`` is currently not covered in this article. I've listed some pointers here [#autobtctl]_.

Start the ``bluetoothctl`` shell. On Raspbian Lite Bluetooth is enabled out of the box and the agent is registered automatically.

.. code-block:: none
        :emphasize-lines: 1

        pi@raspberrypi:~ $ bluetoothctl
        Agent registered
        [bluetooth]# 

The last line shows the ``bluetoothctl`` prompt; the following commands are executed in the ``bluetoothctl`` shell.

.. tip:: Tab completion works here, no need to type the full address!

To discover your Bluetooth device's MAC, turn ``scan on``. **Make sure the device is in pairing mode!**

.. code-block:: none
        :emphasize-lines: 1

        [bluetooth]# scan on
        Discovery started
        [CHG] Controller 00:00:00:00:00:00 Discovering: yes

``bluetoothctl`` will keep spitting out scan results so you might want to turn ``scan off`` after recognizing your device. Exiting ``bluetoothctl`` will turn off scanning automatically, but we're not there yet!

Next up: pairing, trusting and connecting. Trusting enables connecting automatically, including after reboot. Yet you need to connect manually for the first time.

.. code-block:: none
        :emphasize-lines: 1,10,14

        [bluetooth]# pair AA:BB:CC:DD:EE:FF
        Attempting to pair with AA:BB:CC:DD:EE:FF
        [CHG] Device AA:BB:CC:DD:EE:FF Connected: yes
        [CHG] Device AA:BB:CC:DD:EE:FF ServicesResolved: yes
        [CHG] Device AA:BB:CC:DD:EE:FF Paired: yes
        Pairing successful
        [CHG] Device AA:BB:CC:DD:EE:FF ServicesResolved: no
        [CHG] Device AA:BB:CC:DD:EE:FF Connected: no

        [bluetooth]# trust AA:BB:CC:DD:EE:FF
        [CHG] Device AA:BB:CC:DD:EE:FF Trusted: yes
        Changing AA:BB:CC:DD:EE:FF trust succeeded     

        [bluetooth]# connect AA:BB:CC:DD:EE:FF
        Attempting to connect to AA:BB:CC:DD:EE:FF
        [CHG] Device AA:BB:CC:DD:EE:FF Connected: yes
        Connection successful

The prompt changes to reflect connection status. Exit the ``bluetoothctl`` shell with either ``^D`` or typing ``quit``.

.. code-block:: none
        :emphasize-lines: 1

        [BT DEVICE NAME]# quit

Your Bluetooth device's MAC address is needed in the next step, so let's save it into a variable as follows:

.. code-block:: shell
        :emphasize-lines: 1

        pi@raspberrypi:~ $ MAC="AA:BB:CC:DD:EE:FF"



Playing audio
-------------

The following barebones system-wide config for ``bluealsa`` defaults to using A2DP (ie. not sounding like a cheap handsfree); see the Gentoo Wiki article on Bluetooth headphones [#gentoowiki]_, the BlueALSA README [#bluealsa]_ and the ALSA Wiki [#alsawiki]_ for more information about configuration, listed here in order of thoroughness and relevance.

:download:`A simple multi-device asound.conf can be found here. <asound.conf>`

The following lines are indented with four spaces; the tab key doesn't work as expected in here documents [#heretutorial]_, but it does in your text editor.

.. note:: ``$MAC`` is your Bluetooth device's MAC address and is substituted automatically (as long as you did the previous section in the same shell). Feel free to copypaste!

.. code-block:: shell

        sudo tee /etc/asound.conf <<EOF
        defaults.bluealsa {
            interface "hci0"
            device "$MAC"
            profile "a2dp"
        }
        EOF

All done. Test with ``aplay``:

.. warning:: Loud!

.. code-block:: shell

        aplay -D bluealsa /usr/share/sounds/alsa/Front_Center.wav

The file should play without throwing any errors.

Example of streaming audio from YouTube using mpv
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``youtube-dl`` [#ytdl]_ version installed in tandem with ``mpv`` is really old; the package from PyPI is used here instead.

.. code-block:: shell

        sudo apt install -y python3-pip mpv && \ 
        sudo apt purge -y youtube-dl && \ 
        sudo pip3 install youtube-dl && \
        mpv --no-video --audio-device=alsa/bluealsa ytdl://dQw4w9WgXcQ

``mpv`` can be configured to use BlueAlsa by default. Below is a simple system-wide ``mpv.conf`` for audio-only Bluetooth usage; ``~/.config/mpv/mpv.conf`` is where per-user configuration resides. For more information, search for "Configuration files" in the mpv manual [#manmpv]_. ``alsa/$PCM_NAME`` (for example ``alsa/btheadset``) is used to refer to a spesific device.

.. code-block:: shell

        sudo tee /etc/mpv/mpv.conf <<EOF
        no-video
        volume=50
        audio-device=alsa/bluealsa
        EOF

Disabling SAP (optional)
------------------------

.. code-block:: shell

        sudo mkdir /etc/systemd/system/bluetooth.service.d && \ 
        cd /etc/systemd/system/bluetooth.service.d && \ 
        sudo tee 01-disable-sap-plugin.conf <<EOF
        [Service]
        ExecStart=
        ExecStart=/usr/lib/bluetooth/bluetoothd --noplugin=sap
        EOF
        sudo systemctl daemon-reload && \ 
        sudo systemctl restart bluetooth.service

The empty ``ExecStart=`` line is required for replacing the daemon's start command and not just appending to it [#disapble]_.

Reloading daemon configurations and restarting the ``bluetooth`` service requires no reboot. [#pun]_

Further reading
===============

I have found the following resources useful. Feel free to look elsewhere, but be wary of everything assuming you have or need PulseAudio. To prevent link rot, I've made sure both `the Internet Archive Wayback Machine <https://web.archive.org/>`_ and archive.today have a copy available as well as forked the repos/gists on GitHub.

See also the open GitHub issue "`Add a mention on setting the sound device as default <https://github.com/introt/docs/issues/5>`_" for some discussion regarding ALSA defaults and fallbacks, as well as how to set a higher baud rate to fix sound stuttering.

.. [#install] Shameless self-promotion: Check out my `headless Raspberry Pi setup script <https://github.com/introt/headless-rpi-setup-script>`_ that takes care of writing the disk image, configuring the wifi and setting up SSH keys for login. Makes testing these tutorials with latest software really straightforward, just need to download the latest image and run the script.

.. [#bluealsa] See `the project README <https://github.com/Arkq/bluez-alsa>`_ for more information about BlueAlsa and its configuration & usage.

.. [#debianwiki] "Bluetooth/Alsa", `Debian Wiki <https://wiki.debian.org/Bluetooth/Alsa>`_. Raspbian is based on Debian.

.. [#gentoowiki] "Bluetooth headset", `Gentoo Linux Wiki <https://wiki.gentoo.org/wiki/Bluetooth_headset>`_. A good resource for troubleshooting, includes some ALSA configuration examples.

.. [#alsawiki] ".asoundrc", `(Unofficial) ALSA wiki <https://alsa.opensrc.org/Asoundrc>`_. Doesn't include Bluetooth stuff, see [#bluealsa]_ for that part.

.. [#autobtctl] ``bluetoothctl`` can be automated with ``expect`` (`example gist <https://gist.github.com/RamonGilabert/046727b302b4d9fb0055>`_ by RamonGilabert; ``expect`` is not installed by default) or plain old ``echo`` as can be seen `on the Arch Linux forums <https://bbs.archlinux.org/viewtopic.php?id=171144>`_

.. [#heretutorial] "Here documents", `nixCraft Linux Shell Scripting Tutorial <https://bash.cyberciti.biz/guide/Here_documents>`_. Haven't personally used this one, but looks beginner-friendly. Who needs a text editor anyway?

.. [#ytdl] ``youtube-dl`` is a powerful tool that can be used for both downloading and streaming media from a plethora of websites including ``v.redd.it`` and even TikTok! Other download methods and more information available at the `youtube-dl homepage <https://ytdl-org.github.io/youtube-dl/>`_.

.. [#manmpv] See ``man mpv`` for the installed version. The manual for the latest version is available online `here <https://mpv.io/manual/master/>`_.

.. [#disapble] "SAP error on bluetooth service status", `Raspberry Pi Stack Exchange <https://raspberrypi.stackexchange.com/a/99920>`_. SAP stands for "SIM Access Profile" and is used for, you guessed it, accessing SIM card data over Bluetooth.

.. [#pun] While I tend to avoid reboots, I do approve of MCU Spidey in place of "Amazing" Spider-Man sequels.

