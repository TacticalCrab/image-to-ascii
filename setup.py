import PyInstaller.__main__

PyInstaller.__main__.run([
    'src/main.py',
    '--name=ImageToAscii',
    '--windowed',
    '--distpath=C:\\Program Files\\ImageToAscii',
    '--add-data=src;src' 
])