call C:\Users\issakuss\Miniconda3\Script\activate.bat
call activate s13t
call cd C:\Users\issakuss\Documents\task
start progbar.cmd
mode con lines=30 cols=90
call python main-eegonly.py
pause