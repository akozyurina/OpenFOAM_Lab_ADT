set(vtkFiltersPython_LOADED 1)
set(vtkFiltersPython_DEPENDS "vtkCommonCore;vtkCommonExecutionModel;vtkPython;vtkWrappingPythonCore")
set(vtkFiltersPython_LIBRARIES "vtkFiltersPython")
set(vtkFiltersPython_INCLUDE_DIRS "${VTK_INSTALL_PREFIX}/include/paraview-5.6")
set(vtkFiltersPython_LIBRARY_DIRS "")
set(vtkFiltersPython_RUNTIME_LIBRARY_DIRS "${VTK_INSTALL_PREFIX}/lib")
set(vtkFiltersPython_WRAP_HIERARCHY_FILE "${CMAKE_CURRENT_LIST_DIR}/vtkFiltersPythonHierarchy.txt")
set(vtkFiltersPython_KIT "vtkWrapping")
set(vtkFiltersPython_TARGETS_FILE "")


