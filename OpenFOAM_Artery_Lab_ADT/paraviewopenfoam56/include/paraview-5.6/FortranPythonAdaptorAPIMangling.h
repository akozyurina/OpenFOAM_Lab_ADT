#ifndef FortranCInterface_HEADER_INCLUDED
#define FortranCInterface_HEADER_INCLUDED

/* Mangling for Fortran global symbols without underscores. */
#define FortranCInterface_GLOBAL(name,NAME) name##_

/* Mangling for Fortran global symbols with underscores. */
#define FortranCInterface_GLOBAL_(name,NAME) name##_

/* Mangling for Fortran module symbols without underscores. */
#define FortranCInterface_MODULE(mod_name,name, mod_NAME,NAME) __##mod_name##_MOD_##name

/* Mangling for Fortran module symbols with underscores. */
#define FortranCInterface_MODULE_(mod_name,name, mod_NAME,NAME) __##mod_name##_MOD_##name

/*--------------------------------------------------------------------------*/
/* Mangle some symbols automatically.                                       */
#define coprocessorinitializewithpython FortranCInterface_GLOBAL(coprocessorinitializewithpython, COPROCESSORINITIALIZEWITHPYTHON)
#define coprocessoraddpythonscript FortranCInterface_GLOBAL(coprocessoraddpythonscript, COPROCESSORADDPYTHONSCRIPT)

#endif
