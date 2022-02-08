
image-create:
	qemu-img create -f qcow2 vm-flepa-debian-amd64.qcow2 12G
	qemu-img info vm-flepa-debian-amd64.qcow2

image-debian-install:
	rm -f debian-testing-amd64-netinst.iso
	wget http://cdimage.debian.org/cdimage/daily-builds/daily/arch-latest/amd64/iso-cd/debian-testing-amd64-netinst.iso
	qemu-system-x86_64 -enable-kvm -M pc -cpu max -smp cores=2,threads=1,sockets=1 -drive file=file,index=0,media=disk,format=qcow2,file=vm-flepa-debian-amd64.qcow2 -cdrom debian-testing-amd64-netinst.iso -boot d -m 4096
	rm -f debian-testing-amd64-netinst.iso

launch:
	# -cpu max
	qemu-system-x86_64 -enable-kvm -M pc -cpu Skylake-Client -smp cores=4,threads=2,sockets=1 -drive file=file,index=0,media=disk,format=qcow2,file=vm-flepa-debian-amd64.qcow2 -vga virtio -boot d -m 12192
