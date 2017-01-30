python makebin.py -fc ifort -mc -ar intel64 ../src mf2005.exe
python makebin.py -fc ifort -mc -ar intel64 --double ../src mf2005dbl.exe
python makebin.py -fc ifort -mc -ar ia32 ../src mf2005_ia32.exe
python makebin.py -fc ifort -mc -ar ia32 --double ../src mf2005dbl_ia32.exe
pause
