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
#define coprocessorinitialize FortranCInterface_GLOBAL(coprocessorinitialize, COPROCESSORINITIALIZE)
#define coprocessorfinalize FortranCInterface_GLOBAL(coprocessorfinalize, COPROCESSORFINALIZE)
#define requestdatadescription FortranCInterface_GLOBAL(requestdatadescription, REQUESTDATADESCRIPTION)
#define needtocreategrid FortranCInterface_GLOBAL(needtocreategrid, NEEDTOCREATEGRID)
#define coprocess FortranCInterface_GLOBAL(coprocess, COPROCESS)

#endif
