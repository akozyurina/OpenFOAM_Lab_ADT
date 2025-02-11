/*=========================================================================

  Program:   Visualization Toolkit
  Module:    vtkPythonConfigure.h.in

  Copyright (c) Ken Martin, Will Schroeder, Bill Lorensen
  All rights reserved.
  See Copyright.txt or http://www.kitware.com/Copyright.htm for details.

     This software is distributed WITHOUT ANY WARRANTY; without even
     the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
     PURPOSE.  See the above copyright notice for more information.

=========================================================================*/
#ifndef vtkPythonConfigure_h
#define vtkPythonConfigure_h

/* This header is configured by VTK's build process.  */

/* E.g. on BlueGene and Cray there is no multithreading */
#define VTK_NO_PYTHON_THREADS
/* #undef VTK_PYTHON_FULL_THREADSAFE */

/* Whether the real python debug library has been provided.  */
/* #undef VTK_WINDOWS_PYTHON_DEBUGGABLE */

/* build specific site-packages suffix. This is used to setup Python
 * module paths during initialization.
 */
#define VTK_PYTHON_SITE_PACKAGES_SUFFIX "python2.7/site-packages"

#endif
