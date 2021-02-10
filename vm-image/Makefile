
image-create:
	qemu-img create -f raw vm-flepa-debian-amd64.raw 4G
	qemu-img info vm-flepa-debian-amd64.raw

image-debian-install:
	rm -f debian-testing-amd64-netinst.iso
	wget http://cdimage.debian.org/cdimage/daily-builds/daily/arch-latest/amd64/iso-cd/debian-testing-amd64-netinst.iso
	qemu-system-x86_64 -drive file=file,index=0,media=disk,format=raw,file=vm-flepa-debian-amd64.raw -cdrom debian-testing-amd64-netinst.iso -boot d -m 4096
	rm -f debian-testing-amd64-netinst.iso

launch:
	qemu-system-x86_64 -drive file=file,index=0,media=disk,format=raw,file=vm-flepa-debian-amd64.raw -vga virtio -boot d -m 4096
