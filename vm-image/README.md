# FLEPA VM Training Image


## Username and Password

john:john
root:root

# Installed Editors

- mcedit
- vim (-nox)
- nano

# Installed Perf Tools



# VM Creation

> Internal information to build this VM

- make image-create
- make image-debian-install
- Language EN, Timezone & Keyhoard: DE
- root with password root, user john with password john
- use whole disk (3GB), remove swap space
- tasksel: deselect everything, we want a minimal distribution (should be 850MB at the end)
- reboot and cancel second install screen
- make launch
- login as root root
- apt-get --yes install git
- cd /tmp
- git clone https://github.com/hgn/flepa-examples.git
- execute ./flepa-examples/vm-image/vm-bootstrap/setup.sh
