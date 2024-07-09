# SAS4Tool
Simple SAS 4: Zombie Assault profile editor written in Python. (Windows Only)

- Download latest here: [download](https://github.com/dstvx/SAS4Tool/releases/latest)
- Install python: `winget install -e --id Python.Python.3.12`

## How to run
- `git clone https://github.com/dstvx/SAS4Tool.git`
- `cd SAS4Tool`
- `pip install -r requirements.txt`
- `python main.py`

## How to build (must be already installed) (must have upx installed)
- `pip install pyinstaller`
- `pyinstaller main.py --onefile --add-data "lib;lib" -n SAS4Tool`
- `upx /dist/SAS4Tool.exe --lzma --best`
