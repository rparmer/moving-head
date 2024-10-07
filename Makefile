.PHONY: copy
copy:
	rsync -a --exclude Makefile --exclude venv --exclude __pycache__ --exclude config.yml --exclude .git* \
		./ pi@movinghead.local:/home/pi/apps/moving-head/
