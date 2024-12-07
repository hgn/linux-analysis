QEMU_IMG        := qemu-img
QEMU            := qemu-system-x86_64
VM_NAME         := vm-flepa-debian-amd64.qcow2
VM_SIZE         := 12G
DEBIAN_ISO_URL  := https://cdimage.debian.org/cdimage/release/current/amd64/iso-cd/debian-12.8.0-amd64-netinst.iso
DEBIAN_ISO      := $(notdir $(DEBIAN_ISO_URL))

KERNEL           = /boot/vmlinuz-6.11.5-amd64
INITRD           = /boot/initrd.img-6.11.5-amd64
KERNEL           = /boot/vmlinuz-6.13.0-rc1-hgn-00316-gb5f217084ab3
INITRD           = /boot/initrd.img-6.13.0-rc1-hgn-00316-gb5f217084ab3

QEMU=qemu-system-x86_64
DISK=vm-flepa-debian-amd64.qcow2
MEMORY=4G
CPUS=4
APPEND="root=/dev/sda1 rw modprobe.blacklist=floppy console=ttyS0"

CORES           := 4
THREADS         := 2
SOCKETS         := 1
VGA_DEVICE      := std
BOOT_DEVICE     := d
GDB_PORT        := 1234

.DEFAULT_GOAL := launch

.PHONY: all image-create image-debian-install launch debug clean

image-create:
	@echo "Creating VM disk image..."
	$(QEMU_IMG) create -f qcow2 $(VM_NAME) $(VM_SIZE)
	$(QEMU_IMG) info $(VM_NAME)

image-debian-install:
	@echo "Downloading Debian ISO..."
	rm -f $(DEBIAN_ISO)
	wget $(DEBIAN_ISO_URL) -O $(DEBIAN_ISO)
	@echo "Booting the VM with the installer ISO..."
	$(QEMU) -enable-kvm \
		-M pc \
		-cpu max \
		-smp cores=2,threads=1,sockets=1 \
		-drive file=$(VM_NAME),index=0,media=disk,format=qcow2 \
		-cdrom $(DEBIAN_ISO) \
		-boot $(BOOT_DEVICE) \
		-m $(MEMORY)
	@echo "Cleaning up the installer ISO..."
	rm -f $(DEBIAN_ISO)

launch:
	@echo "Launching Debian VM..."
	$(QEMU) \
	-M pc \
	-enable-kvm \
	-smp cores=$(CORES),threads=$(THREADS),sockets=$(SOCKETS) \
	-m $(MEMORY) \
	-kernel $(KERNEL) \
	-initrd $(INITRD) \
	-append $(APPEND)  \
	-drive file=$(DISK),if=ide,format=qcow2 \
	-device virtio-keyboard-pci \
	-vga $(VGA_DEVICE) \
	-net nic -net user \
	-gdb tcp::1234


clean:
	@echo "Cleaning up generated files..."
	rm -f $(VM_NAME)
