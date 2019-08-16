#! /usr/bin/env python
try:
    import pymake
except:
    msg =  'Error. Pymake package is not available.\n'
    msg += 'Try installing using the following command:\n'
    msg += ' pip install https://github.com/modflowpy/pymake/zipball/master'
    print(msg)
    raise Exception()

#get the arguments
args = pymake.pymake.parser()

#call main -- note that this form allows main to be called
#from python as a function.

pymake.pymake.main(args.srcdir, args.target, fc=args.fc, cc=args.cc, 
                   makeclean=args.makeclean, expedite=args.expedite, 
                   dryrun=args.dryrun, double=args.double, 
                   debug=args.debug, include_subdirs=args.subdirs, 
                   fflags=args.fflags, cflags=args.cflags, 
                   arch=args.arch)
