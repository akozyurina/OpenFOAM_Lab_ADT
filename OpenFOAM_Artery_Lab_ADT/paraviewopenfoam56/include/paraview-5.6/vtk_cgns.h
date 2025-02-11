/*=========================================================================

  Program:   ParaView
  Module:    vtk_cgns.h.in

  Copyright (c) Kitware, Inc.
  All rights reserved.
  See Copyright.txt or http://www.paraview.org/HTML/Copyright.html for details.

     This software is distributed WITHOUT ANY WARRANTY; without even
     the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
     PURPOSE.  See the above copyright notice for more information.

=========================================================================*/
#ifndef vtk_cgns_h
#define vtk_cgns_h

/* #undef VTK_USE_SYSTEM_CGNS */
#ifdef VTK_USE_SYSTEM_CGNS
# include <cgnslib.h> // DataType, and other definition
# include <cgns_io.h> // Low level IO for fast parsing
#else
# include <vtkcgns/src/cgnslib.h> // DataType, and other definition
# include <vtkcgns/src/cgns_io.h> // Low level IO for fast parsing
#endif

#endif
