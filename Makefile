run		:	src/main.py
	python src/main.py ; rm -rf src/*/__pycache__ src/__pycache__

exe		:	src/main.py
	rm -f DinoRush.exe ; pyinstaller -F --icon=".\\assets\\imgs\\icon.ico" src/main.py ; mv dist/DinoRush.exe ./ ; rm -rf build/ dist/ DinoRush.spec
