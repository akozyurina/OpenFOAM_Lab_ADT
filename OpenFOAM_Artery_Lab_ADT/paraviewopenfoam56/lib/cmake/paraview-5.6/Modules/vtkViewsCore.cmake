set(vtkViewsCore_LOADED 1)
set(vtkViewsCore_DEPENDS "vtkCommonCore;vtkCommonDataModel;vtkCommonExecutionModel;vtkFiltersGeneral;vtkInteractionWidgets;vtkRenderingCore")
set(vtkViewsCore_LIBRARIES "vtkViewsCore")
set(vtkViewsCore_INCLUDE_DIRS "${VTK_INSTALL_PREFIX}/include/paraview-5.6")
set(vtkViewsCore_LIBRARY_DIRS "")
set(vtkViewsCore_RUNTIME_LIBRARY_DIRS "${VTK_INSTALL_PREFIX}/lib")
set(vtkViewsCore_WRAP_HIERARCHY_FILE "${CMAKE_CURRENT_LIST_DIR}/vtkViewsCoreHierarchy.txt")
set(vtkViewsCore_KIT "vtkViews")
set(vtkViewsCore_TARGETS_FILE "")


