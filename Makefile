.PHONY: copy
copy:
	rsync -a --exclude Makefile --exclude config.yml --exclude .git* \
		./ pi@movinghead.local:/home/pi/apps/moving-head/
