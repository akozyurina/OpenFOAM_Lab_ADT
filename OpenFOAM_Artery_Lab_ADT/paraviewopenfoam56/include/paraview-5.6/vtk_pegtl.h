/*=========================================================================

  Program:   Visualization Toolkit
  Module:    vtk_pegtl.h

  Copyright (c) Ken Martin, Will Schroeder, Bill Lorensen
  All rights reserved.
  See Copyright.txt or http://www.kitware.com/Copyright.htm for details.

     This software is distributed WITHOUT ANY WARRANTY; without even
     the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
     PURPOSE.  See the above copyright notice for more information.

=========================================================================*/
#ifndef vtk_pegtl_h
#define vtk_pegtl_h

/* Use the pegtl library configured for VTK.  */
/* #undef VTK_USE_SYSTEM_PEGTL */
#ifdef VTK_USE_SYSTEM_PEGTL
# include <tao/pegtl.hpp>
#else
# include <vtkpegtl/include/tao/pegtl.hpp>
#endif

#endif
