run		:	DinoRush.py
	python DinoRush.py ; rm -rf src/__pycache__/

exe		:	DinoRush.py
	rm -f DinoRush.exe ; pyinstaller -F --icon=".\\assets\\imgs\\icon.ico" DinoRush.py ; mv dist/DinoRush.exe ./ ; rm -rf build/ dist/ DinoRush.spec
