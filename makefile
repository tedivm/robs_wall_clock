
install:
	circup install -r requirements.txt

freeze_deps:
	circup freeze | tail -n +2 | sort > requirements.txt

upload:
	cp main.py /Volumes/CIRCUITPY/code.py
	cp -r modes /Volumes/CIRCUITPY/
	cp -r utils /Volumes/CIRCUITPY/
