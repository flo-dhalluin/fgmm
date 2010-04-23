import os.path
import Options

srcdir = '.'
blddir = '_build_'


def set_options(opt):
    # command-line options provided by a waf tool
    opt.tool_options('compiler_cc')
    opt.tool_options('compiler_cxx')
    opt.add_option('--gprof', dest = "use_gprof", action='store_true', 
                   default=False, help='Link with gprof for profiling')

    opt.add_option('--old',dest="oldGMR",action='store_true',
                   default=False, help='Build test using old GMR lib for comparison')

#     opt.add_option('--check',dest="check",action='store_true',
#                    default=False, help='run the tests')

def configure(conf) :
    #print "configuring"
   
    conf.check_tool('compiler_cc')  
    conf.check_tool('compiler_cxx')  
    conf.env.CCFLAGS = ['-Wall','-O2','-g','--fast-math'] 

    if Options.options.use_gprof :
        conf.env.CCFLAGS.append('-pg')
        conf.env.LINKFLAGS = ['-pg']

    if Options.options.oldGMR :
        conf.env['LIBPATH_MATRIX'] = '/home/fdhalluin/code/MathLib/lib/'
        conf.env['LIB_MATRIX'] = 'Matrix'
        conf.env['LIBPATH_GMR'] = '/home/fdhalluin/code/GMR/lib/'
        conf.env['LIB_GMR'] = 'GMR'

   
def build(bld) :
    print "compiling"
    print dir(bld)
    print bld.lst_variants
    obj_src = bld.path.ant_glob("src/*.c")
    test_src = bld.path.ant_glob("tests/test_*.c")
    obj = []
    
#     for src in obj_src.split():
#         print src
#         targ_name = os.path.splitext(src)[0]+'.o'
#         bld(features='cc',
#             target = targ_name,
#             source=src)
#         obj.append(targ_name)

    bld(features='cc cstaticlib',
        target = 'fgmm',
        source = obj_src,
        export_incdirs="src/")

    for src in test_src.split():

        targ_name = os.path.basename(src)
        targ_name = os.path.splitext(targ_name)[0]

        bld(features = 'cc cprogram',
                source = src,
                target = targ_name,
                includes = '.',
                lib = ['m'],
                uselib_local="fgmm")
            #add_objects=obj)

    bld(target="run_test.py",
        source = "tests/run_test.py",
        rule= "cp ${SRC} ${TGT}")
        
    if Options.options.oldGMR :
        cpgmr = bld(features = 'cxx cprogram',
                    source = 'tests/oldGMR.cpp',
                    target = 'oldGMR',
                    includes = '/home/fdhalluin/code/MathLib/include/ /home/fdhalluin/code/GMR/include/',
                    uselib = ['GMR','MATRIX'])    

def test(ctx) :
    print ctx.env
    print ctx.curdir
    print dir(ctx)
    print "launching tests .. hihi"
