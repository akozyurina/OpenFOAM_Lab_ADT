set(vtktiff_LOADED 1)
set(vtktiff_DEPENDS "vtkjpeg;vtkzlib")
set(vtktiff_LIBRARIES "vtktiff")
set(vtktiff_INCLUDE_DIRS "${VTK_INSTALL_PREFIX}/include/paraview-5.6")
set(vtktiff_LIBRARY_DIRS "")
set(vtktiff_RUNTIME_LIBRARY_DIRS "${VTK_INSTALL_PREFIX}/lib")
set(vtktiff_WRAP_HIERARCHY_FILE "${CMAKE_CURRENT_LIST_DIR}/vtktiffHierarchy.txt")
set(vtktiff_KIT "")
set(vtktiff_TARGETS_FILE "")
set(vtktiff_EXCLUDE_FROM_WRAPPING 1)


