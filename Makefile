run		:	src/main.py
	python src/main.py ; rm -rf src/*/__pycache__ src/__pycache__

exe		:	src/main.py
	cd src; \
	pyinstaller -F -i ../assets/imgs/icon.ico -n DinoRush \
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
	mv dist/DinoRush.exe ../; \
	rm -rf build/ dist/ DinoRush.spec; \
	cd ..; \
	find . -name "__pycache__" -type d -exec rm -rf {} \;