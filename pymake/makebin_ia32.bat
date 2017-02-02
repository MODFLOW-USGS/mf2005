rem mf2005
python makebin.py -fc ifort -mc -ar ia32 ../src mf2005_ia32.exe
python makebin.py -fc ifort -mc -ar ia32 --double ../src mf2005dbl_ia32.exe

rem hydfmt
python makebin.py -fc ifort -mc -ar ia32 ../src/hydprograms hydfmt_ia32.exe

pause
