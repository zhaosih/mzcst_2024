"""Monitors and post-processing objects for CST simulations.

This module provides objects to create field monitors, S-parameter monitors,
and post-processing templates for CST simulations.
"""

import logging
from typing import List, Dict, Any, Optional, Tuple

from .. import interface
from .._global import BaseObject, Parameter
from ..common import NEW_LINE, quoted

_logger = logging.getLogger(__name__)


class FieldMonitor(BaseObject):
    """Field monitor for electromagnetic field recording.
    
    Creates monitors to record electric and magnetic fields at specific 
    frequencies or time points.
    """
    
    def __init__(self, *, attributes=None, vba=None, **kwargs):
        super().__init__(attributes=attributes, vba=vba, **kwargs)
        self._history_title = "define field monitor"
        self._monitor_type = "efield"  # efield, hfield, powerflow, current
        self._frequency = None
        self._name = "monitor1"
        return
    
    def set_field_type(self, field_type: str) -> "FieldMonitor":
        """Set the field type to monitor.
        
        Args:
            field_type: Type of field ("efield", "hfield", "powerflow", "current")
        """
        self._monitor_type = field_type
        return self
    
    def set_frequency(self, frequency: float) -> "FieldMonitor":
        """Set the frequency for the monitor.
        
        Args:
            frequency: Frequency value in project units
        """
        self._frequency = frequency
        return self
    
    def set_name(self, name: str) -> "FieldMonitor":
        """Set the monitor name.
        
        Args:
            name: Monitor name
        """
        self._name = name
        return self
    
    def create_from_attributes(self, modeler) -> "FieldMonitor":
        """Create field monitor from attributes.
        
        Args:
            modeler: CST Model3D interface
        """
        vba_lines = [
            "With Monitor",
            f'    .Reset',
            f'    .Name "{self._name}"',
            f'    .Frequency "{self._frequency if self._frequency else "0"}"',
            f'    .FieldType "{self._monitor_type}"',
            f'    .Create',
            "End With"
        ]
        
        vba_code = NEW_LINE.join(vba_lines)
        modeler.add_to_history(self._history_title, vba_code)
        return self


class SParameterMonitor(BaseObject):
    """S-parameter monitor for network parameter recording."""
    
    def __init__(self, *, attributes=None, vba=None, **kwargs):
        super().__init__(attributes=attributes, vba=vba, **kwargs)
        self._history_title = "define S-parameter monitor"
        return
    
    def create_from_attributes(self, modeler) -> "SParameterMonitor":
        """Create S-parameter monitor.
        
        Args:
            modeler: CST Model3D interface
        """
        vba_lines = [
            "With Monitor",
            f'    .Reset',
            f'    .Name "S-Parameters"',
            f'    .FieldType "Sparameter"',
            f'    .Create',
            "End With"
        ]
        
        vba_code = NEW_LINE.join(vba_lines)
        modeler.add_to_history(self._history_title, vba_code)
        return self


class FarfieldMonitor(BaseObject):
    """Farfield monitor for radiation pattern recording."""
    
    def __init__(self, *, attributes=None, vba=None, **kwargs):
        super().__init__(attributes=attributes, vba=vba, **kwargs)
        self._history_title = "define farfield monitor"
        self._frequency = None
        self._name = "farfield"
        return
    
    def set_frequency(self, frequency: float) -> "FarfieldMonitor":
        """Set the frequency for farfield calculation."""
        self._frequency = frequency
        return self
    
    def set_name(self, name: str) -> "FarfieldMonitor":
        """Set the monitor name."""
        self._name = name
        return self
    
    def create_from_attributes(self, modeler) -> "FarfieldMonitor":
        """Create farfield monitor.
        
        Args:
            modeler: CST Model3D interface
        """
        vba_lines = [
            "With Monitor",
            f'    .Reset',
            f'    .Name "{self._name}"',
            f'    .Frequency "{self._frequency if self._frequency else "0"}"',
            f'    .FieldType "Farfield"',
            f'    .Create',
            "End With"
        ]
        
        vba_code = NEW_LINE.join(vba_lines)
        modeler.add_to_history(self._history_title, vba_code)
        return self


class PostProcess1D(BaseObject):
    """1D post-processing for creating plots and exporting data."""
    
    def __init__(self, *, attributes=None, vba=None, **kwargs):
        super().__init__(attributes=attributes, vba=vba, **kwargs)
        self._history_title = "1D post-processing"
        self._plot_type = "rectangular"
        self._result_id = "S1,1"
        return
    
    def set_plot_type(self, plot_type: str) -> "PostProcess1D":
        """Set the plot type.
        
        Args:
            plot_type: Type of plot ("rectangular", "polar", "smith")
        """
        self._plot_type = plot_type
        return self
    
    def set_result_id(self, result_id: str) -> "PostProcess1D":
        """Set the result ID to plot.
        
        Args:
            result_id: Result identifier (e.g., "S1,1", "S2,1")
        """
        self._result_id = result_id
        return self
    
    def create_plot(self, modeler) -> bool:
        """Create 1D plot.
        
        Args:
            modeler: CST Model3D interface
            
        Returns:
            Success status
        """
        vba_lines = [
            "With Plot1D",
            f'    .Reset',
            f'    .PlotView "{self._plot_type}"',
            f'    .Add "{self._result_id}"',
            f'    .Plot',
            "End With"
        ]
        
        vba_code = NEW_LINE.join(vba_lines)
        modeler.add_to_history(self._history_title, vba_code)
        return True
    
    def export_data(self, modeler, filename: str, format_type: str = "txt") -> bool:
        """Export 1D data to file.
        
        Args:
            modeler: CST Model3D interface
            filename: Output filename
            format_type: Export format ("txt", "csv", "touchstone")
            
        Returns:
            Success status
        """
        vba_lines = [
            "With Plot1D",
            f'    .Reset',
            f'    .Add "{self._result_id}"',
            f'    .Save "{filename}"',
            "End With"
        ]
        
        vba_code = NEW_LINE.join(vba_lines)
        modeler.add_to_history(f"export 1D data to {filename}", vba_code)
        return True


class PostProcess2D(BaseObject):
    """2D post-processing for field visualization and data export."""
    
    def __init__(self, *, attributes=None, vba=None, **kwargs):
        super().__init__(attributes=attributes, vba=vba, **kwargs)
        self._history_title = "2D post-processing"
        self._field_type = "efield"
        self._component = "abs"
        self._frequency = None
        self._plane = "xy"
        self._position = 0.0
        return
    
    def set_field_type(self, field_type: str) -> "PostProcess2D":
        """Set the field type for visualization.
        
        Args:
            field_type: Field type ("efield", "hfield", "powerflow")
        """
        self._field_type = field_type
        return self
    
    def set_component(self, component: str) -> "PostProcess2D":
        """Set the field component.
        
        Args:
            component: Component ("abs", "x", "y", "z", "real", "imag")
        """
        self._component = component
        return self
    
    def set_frequency(self, frequency: float) -> "PostProcess2D":
        """Set the frequency for field visualization."""
        self._frequency = frequency
        return self
    
    def set_plane(self, plane: str, position: float = 0.0) -> "PostProcess2D":
        """Set the cutting plane.
        
        Args:
            plane: Plane orientation ("xy", "xz", "yz")
            position: Position along the normal axis
        """
        self._plane = plane
        self._position = position
        return self
    
    def create_plot(self, modeler) -> bool:
        """Create 2D field plot.
        
        Args:
            modeler: CST Model3D interface
            
        Returns:
            Success status
        """
        # Determine normal coordinate based on plane
        if self._plane == "xy":
            normal_coord = "z"
        elif self._plane == "xz":
            normal_coord = "y"
        else:  # yz
            normal_coord = "x"
        
        vba_lines = [
            "With Plot2D",
            f'    .Reset',
            f'    .Type "{self._field_type}"',
            f'    .Component "{self._component}"',
            f'    .Frequency "{self._frequency if self._frequency else "0"}"',
            f'    .PlaneCoordinate "{normal_coord}"',
            f'    .PlanePosition "{self._position}"',
            f'    .Plot',
            "End With"
        ]
        
        vba_code = NEW_LINE.join(vba_lines)
        modeler.add_to_history(self._history_title, vba_code)
        return True
    
    def export_data(self, modeler, filename: str, format_type: str = "txt") -> bool:
        """Export 2D field data to file.
        
        Args:
            modeler: CST Model3D interface
            filename: Output filename
            format_type: Export format ("txt", "csv", "vtk")
            
        Returns:
            Success status
        """
        vba_lines = [
            "With Plot2D",
            f'    .Reset',
            f'    .Type "{self._field_type}"',
            f'    .Component "{self._component}"',
            f'    .Frequency "{self._frequency if self._frequency else "0"}"',
            f'    .Save "{filename}"',
            "End With"
        ]
        
        vba_code = NEW_LINE.join(vba_lines)
        modeler.add_to_history(f"export 2D data to {filename}", vba_code)
        return True


class FarfieldPostProcess(BaseObject):
    """Farfield post-processing for antenna pattern analysis."""
    
    def __init__(self, *, attributes=None, vba=None, **kwargs):
        super().__init__(attributes=attributes, vba=vba, **kwargs)
        self._history_title = "farfield post-processing"
        self._frequency = None
        self._plot_type = "polar"
        self._component = "abs"
        return
    
    def set_frequency(self, frequency: float) -> "FarfieldPostProcess":
        """Set frequency for farfield calculation."""
        self._frequency = frequency
        return self
    
    def set_plot_type(self, plot_type: str) -> "FarfieldPostProcess":
        """Set farfield plot type.
        
        Args:
            plot_type: Plot type ("polar", "cartesian", "3d")
        """
        self._plot_type = plot_type
        return self
    
    def set_component(self, component: str) -> "FarfieldPostProcess":
        """Set farfield component.
        
        Args:
            component: Component ("abs", "theta", "phi", "axial_ratio")
        """
        self._component = component
        return self
    
    def create_plot(self, modeler) -> bool:
        """Create farfield plot."""
        vba_lines = [
            "With FarfieldPlot",
            f'    .Reset',
            f'    .Frequency "{self._frequency if self._frequency else "0"}"',
            f'    .PlotType "{self._plot_type}"',
            f'    .Component "{self._component}"',
            f'    .Plot',
            "End With"
        ]
        
        vba_code = NEW_LINE.join(vba_lines)
        modeler.add_to_history(self._history_title, vba_code)
        return True
    
    def export_data(self, modeler, filename: str) -> bool:
        """Export farfield data to file."""
        vba_lines = [
            "With FarfieldPlot",
            f'    .Reset',
            f'    .Frequency "{self._frequency if self._frequency else "0"}"',
            f'    .Save "{filename}"',
            "End With"
        ]
        
        vba_code = NEW_LINE.join(vba_lines)
        modeler.add_to_history(f"export farfield data to {filename}", vba_code)
        return True


# Convenience functions for common monitoring tasks
def create_standard_monitors(modeler, frequencies: List[float]) -> List[str]:
    """Create standard monitoring setup for antenna simulations.
    
    Args:
        modeler: CST Model3D interface
        frequencies: List of frequencies for monitoring
        
    Returns:
        List of created monitor names
    """
    monitor_names = []
    
    # Create S-parameter monitor
    s_monitor = SParameterMonitor()
    s_monitor.create_from_attributes(modeler)
    monitor_names.append("S-Parameters")
    
    # Create farfield monitors at key frequencies
    for i, freq in enumerate(frequencies):
        ff_monitor = FarfieldMonitor()
        ff_monitor.set_frequency(freq)
        ff_monitor.set_name(f"farfield_f{i+1}")
        ff_monitor.create_from_attributes(modeler)
        monitor_names.append(f"farfield_f{i+1}")
    
    # Create E-field monitors at key frequencies
    for i, freq in enumerate(frequencies):
        ef_monitor = FieldMonitor()
        ef_monitor.set_field_type("efield")
        ef_monitor.set_frequency(freq)
        ef_monitor.set_name(f"efield_f{i+1}")
        ef_monitor.create_from_attributes(modeler)
        monitor_names.append(f"efield_f{i+1}")
    
    return monitor_names


def export_all_1d_results(modeler, output_dir: str, result_types: List[str] = None) -> List[str]:
    """Export all 1D results to files.
    
    Args:
        modeler: CST Model3D interface
        output_dir: Output directory path
        result_types: List of result types to export (default: common S-parameters)
        
    Returns:
        List of exported filenames
    """
    if result_types is None:
        result_types = ["S1,1", "S2,1", "S1,2", "S2,2"]
    
    exported_files = []
    
    for result_type in result_types:
        filename = f"{output_dir}/{result_type.replace(',', '_')}.txt"
        
        post_proc = PostProcess1D()
        post_proc.set_result_id(result_type)
        success = post_proc.export_data(modeler, filename)
        
        if success:
            exported_files.append(filename)
    
    return exported_files


def export_field_maps_2d(modeler, output_dir: str, frequency: float, 
                        planes: List[str] = None) -> List[str]:
    """Export 2D field maps for multiple cutting planes.
    
    Args:
        modeler: CST Model3D interface
        output_dir: Output directory path
        frequency: Frequency for field calculation
        planes: List of cutting planes (default: ["xy", "xz", "yz"])
        
    Returns:
        List of exported filenames
    """
    if planes is None:
        planes = ["xy", "xz", "yz"]
    
    exported_files = []
    
    for plane in planes:
        for field_type in ["efield", "hfield"]:
            filename = f"{output_dir}/{field_type}_{plane}_f{frequency}.txt"
            
            post_proc = PostProcess2D()
            post_proc.set_field_type(field_type)
            post_proc.set_component("abs")
            post_proc.set_frequency(frequency)
            post_proc.set_plane(plane, 0.0)
            
            success = post_proc.export_data(modeler, filename)
            
            if success:
                exported_files.append(filename)
    
    return exported_files