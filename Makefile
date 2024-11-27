MAKEFLAGS += --no-print-directory -k -s -i

clean			:
	find . -type f -name "*.py[co]" -delete; \
	find . -type d -name "__pycache__" -delete; \
	rm -rf src/build src/dist src/DinoRush.spec

run				:	_run_target clean
_run_target		:	src/main.py
	trap 'make clean' SIGINT; \
	src/main.py || true

server			:	_server_target clean
_server_target	:	src/networking/dino_rush_server.py
	trap 'make clean' SIGINT; \
	src/networking/dino_rush_server.py || true

exe				:	_exe_target clean
_exe_target		:	src/main.py
	trap 'cd /d/repos/DinoRush; make clean' SIGINT; \
	(cd src; \
	pyinstaller -F --noconsole \
	-i ../assets/imgs/icon.ico -n DinoRush \
	--add-data "../assets/imgs/parallaxes/*:assets/imgs/parallaxes" \
	--add-data "../assets/imgs/sprite_sheets/players/*:assets/imgs/sprite_sheets/players" \
	--add-data "../assets/imgs/tilesets/*:assets/imgs/tilesets" \
	--add-data "../assets/imgs/world_objects/*:assets/imgs/world_objects" \
	--add-data "../assets/imgs/title_icon.png:assets/imgs" \
	--add-data "../assets/players/*:assets/players" \
	--add-data "../assets/worlds/*:assets/worlds" \
	--add-data "networking/*:networking" \
	--add-data "player/*:player" \
	--add-data "world/*:world" \
	--add-data "camera.py:." \
	--add-data "constants.py:." \
	--add-data "engine.py:." \
	main.py;\
	mv dist/DinoRush.exe ../;) || true \
	cd ..;