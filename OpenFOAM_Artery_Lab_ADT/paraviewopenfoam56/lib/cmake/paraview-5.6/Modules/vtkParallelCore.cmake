set(vtkParallelCore_LOADED 1)
set(vtkParallelCore_DEPENDS "vtkCommonCore;vtkCommonDataModel;vtkCommonSystem;vtkIOLegacy;vtksys")
set(vtkParallelCore_LIBRARIES "vtkParallelCore")
set(vtkParallelCore_INCLUDE_DIRS "${VTK_INSTALL_PREFIX}/include/paraview-5.6")
set(vtkParallelCore_LIBRARY_DIRS "")
set(vtkParallelCore_RUNTIME_LIBRARY_DIRS "${VTK_INSTALL_PREFIX}/lib")
set(vtkParallelCore_WRAP_HIERARCHY_FILE "${CMAKE_CURRENT_LIST_DIR}/vtkParallelCoreHierarchy.txt")
set(vtkParallelCore_KIT "vtkParallel")
set(vtkParallelCore_TARGETS_FILE "")


