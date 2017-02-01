rem mf2005
python makebin.py -fc ifort -mc -ar intel64 ../src mf2005.exe
python makebin.py -fc ifort -mc -ar intel64 --double ../src mf2005dbl.exe

rem hydfmt
python makebin.py -fc ifort -mc -ar intel64 ../src/hydprograms hydfmt.exe

pause
