DEVICE_PATH:=/Volumes/CIRCUITPY


install:
	circup install -r requirements.txt

console:
	screen $(ls -1 /dev/tty.* | grep usb) 115200

freeze_deps:
	circup freeze | tail -n +2 | sort > requirements.txt

upload:
	cp main.py $(DEVICE_PATH)/code.py
	cp -r modes $(DEVICE_PATH)/
	cp -r utils $(DEVICE_PATH)/

pull_from_device: freeze_deps
	cp $(DEVICE_PATH)/code.py main.py
	cp -r $(DEVICE_PATH)/modes ./
	cp -r $(DEVICE_PATH)/utils ./
