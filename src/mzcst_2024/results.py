"""提供与`cst.results`交互的接口。

This module allows reading one-dimensional result curves and data points of
CST project files. These results are referred to as “0D/1D Results”.

No running instance of CST Studio Suite is required for data access.

Supported are unpacked and unprotected project files generated with CST Studio
Suite 2023 or CST Studio Suite 2024.

To understand how this module can be used, see the Examples section of the
documentation.

General Notes
-------

This module supports only access to unpacked CST files. A packed CST project
file (generated via “Archive As”) can be extracted by opening it with CST Studio
Suite. If the project has subprojects (see Examples), they need to be unpacked
recursively as well (i.e. by double-clicking on the corresponding subproject
tree entry in Schematic, then saving the parent project).

Protected project files are not supported.

Please also note that access to projects which are being simulated in an open
CST Studio Suite is not supported.

"""

import os

import cst.results
import numpy
from cst.results import get_version_info, print_version_info

# -pylint: disable=no-member


class ProjectFile:
    """提供与`cst.results.ProjectFile`的接口。

    This class allows loading a CST file to access its results."""

    def __init__(
        self, filepath: os.PathLike = None, allow_interactive: bool = False
    ):
        """

        Initialize a ProjectFile with a filepath to a CST file. The setting
        `allow_interactive=True` allows accessing a project which can be
        simultaneously opened in CST Studio Suite. In this interactive mode,
        data access can be done after ‘Save’ was triggered in CST Studio Suite.
        If any changes are made in CST Studio Suite to the project without
        saving (e.g. a solver is started), the retrieved data will be outdated
        or ill-formed. It is up to the user to ensure that the project is not in
        an intermediate state.
        """

        self._pf = cst.results.ProjectFile(filepath, allow_interactive)

        return

    def __str__(self):
        return str(self._pf)

    def __repr__(self):
        return repr(self._pf)

    @classmethod
    def init(cls, pf: "cst.results.ProjectFile"):
        """_summary_

        Parameters
        ----------
        rm : cst.results.ResultModule
            cst 库的 ProjectFile 对象

        Returns
        -------
        ResultModule
            mzcst 库的接口对象
        """
        _new = cls()
        _new._pf = pf
        return _new

    @property
    def filename(self) -> str:
        """The filename of the CST project."""
        return self._pf.filename

    def get_3d(self) -> "ResultModule":
        """Get the 3D submodule of a CST project."""
        g3 = self._pf.get_3d()
        return ResultModule.init(g3)

    def get_schematic(self):
        """Get the Schematic submodule of a CST project."""
        gs = self._pf.get_schematic()
        return ResultModule.init(gs)

    def list_subprojects(self) -> list[str]:
        """List tree paths which represent subprojects (i.e. Simulation Projects
        Tasks or Block Simulation Tasks).

        Returns
        -------
        list[str]
            包含子项目的树状路径。
        """
        return self._pf.list_subprojects()

    def load_subproject(self) -> "ProjectFile":
        """Load a subproject from a tree path.

        Returns
        -------
        ProjectFile
            project file object of subproject
        """
        ls = self._pf.load_subproject()
        return ProjectFile.init(ls)


class ResultModule:
    """提供与`cst.results.ResultModule`的接口。

    This class provides an interface to access the 3D or Schematic results
    submodule of a of a CST project.
    """

    def __init__(self):
        self._rm = None
        return

    def __str__(self):
        return str(self._rm)

    def __repr__(self):
        return repr(self._rm)

    @classmethod
    def init(cls, rm: "cst.results.ResultModule"):
        """从 `cst.results.ResultModule` 对象创建 ResultItem 接口。

        Parameters
        ----------
        rm : cst.results.ResultModule
            cst库的ResultModule对象

        Returns
        -------
        ResultModule
            mzcst库的接口对象
        """
        _new = cls()
        _new._rm = rm
        return _new

    def get_all_run_ids(self, max_mesh_passes_only: bool = True) -> list[int]:
        """Get all existing run ids (independent of a tree path).

        Parameters
        ----------
        max_mesh_passes_only : bool, optional
            if `max_mesh_passes_only` is True, this method yields only
        results with the highest mesh pass, by default True

        Returns
        -------
        list[int]
            all existing run ids.
        """
        return self._rm.get_all_run_ids(max_mesh_passes_only)

    def get_parameter_combination(self, run_id: int) -> dict:
        """Return the parameter combination which corresponds to the provided run id.

        Parameters
        ----------
        run_id : int
            _description_

        Returns
        -------
        dict
            _description_
        """
        return self._rm.get_parameter_combination(run_id)

    def get_result_item(
        self, treepath: str, run_id: int = 0, load_impedances: bool = True
    ) -> "ResultItem":
        """Get result of a navigation tree item. The setting `load_impedances=False` omits automatic loading of reference impedances.

        Parameters
        ----------
        treepath : str
            path of result item
        run_id : int, optional
            run id, by default 0
        load_impedances : bool, optional
            if set to `False`, this method omits automatic loading of reference impedances, by default True

        Returns
        -------
        ResultItem
            _description_
        """
        temp: "cst.results.ResultItem" = self._rm.get_result_item(
            treepath, run_id, load_impedances
        )
        return ResultItem.init(temp)

    def get_run_ids(
        self, treepath: str, skip_nonparametric: bool = False
    ) -> list[int]:
        """Get all existing run ids for a tree item.

        Parameters
        ----------
        treepath : str
            _description_
        skip_nonparametric : bool, optional
            if `True`, it enforces run id = 0 to be excluded from the list, by default False

        Returns
        -------
        list[int]
            all existing run ids
        """
        return self._rm.get_run_ids(treepath, skip_nonparametric)

    def get_tree_items(self, filter_: str = "0D/1D") -> list[str]:
        """List navigation tree items.

        Parameters
        ----------
        filter : str, optional
            filter, by default '0D/1D'

        Returns
        -------
        list[str]
            navigation tree items
        """
        return self._rm.get_tree_items(filter_)


class ResultItem:
    """提供与`cst.results.ResultItem`的接口。

    This class represents the result data of a navigation tree item of a CST
    project for a single parameter combination.
    """

    def __init__(self):
        self._ri = None
        return

    @classmethod
    def init(cls, ri: "cst.results.ResultItem"):
        """从 `cst.results.ResultItem` 对象创建 ResultItem 接口。

        Parameters
        ----------
        rm : cst.results.ResultItem
            cst库的ResultModule对象

        Returns
        -------
        ResultItem
            mzcst库的接口对象
        """
        _new = cls()
        _new._ri = ri
        return _new

    def __str__(self):
        return str(self._ri)

    def __repr__(self):
        return repr(self._ri)

    def get_data(self) -> list:
        """The data as list of tuples, or a double value."""
        return self._ri.get_data()

    def get_parameter_combination(self) -> dict:
        """The parameter combination which was used to generate the result."""
        return self._ri.get_parameter_combination()

    def get_ref_imp_data(self) -> list:
        """The reference impedance of the result."""
        return self._ri.get_ref_imp_data()

    def get_xdata(self) -> list:
        """The x-axis of the result."""
        return self._ri.get_xdata()

    def get_ydata(self) -> list:
        """The y-axis of the result."""
        return self._ri.get_ydata()

    @property
    def length(self) -> int:
        """The number of points returned by ‘get_ydata’."""
        return self._ri.length

    @property
    def run_id(self) -> int:
        """The run id of the result."""
        return self._ri.run_id

    @property
    def title(self) -> str:
        """The title of the result."""
        return self._ri.title

    @property
    def treepath(self) -> str:
        """The navigation tree path of the result."""
        return self._ri.treepath

    @property
    def xlabel(self) -> str:
        """The x-label of the result."""
        return self._ri.xlabel

    @property
    def ylabel(self) -> str:
        """The y-label of the result."""
        return self._ri.ylabel
    
    def export_to_file(self, filename: str, format_type: str = "txt") -> bool:
        """Export result data to file.
        
        Args:
            filename: Output filename
            format_type: Export format ("txt", "csv", "touchstone")
            
        Returns:
            Success status
        """
        try:
            if format_type.lower() == "csv":
                return self._export_csv(filename)
            elif format_type.lower() == "touchstone":
                return self._export_touchstone(filename)
            else:  # Default to txt
                return self._export_txt(filename)
        except Exception:
            return False
    
    def _export_txt(self, filename: str) -> bool:
        """Export to text file format."""
        try:
            import os
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            with open(filename, 'w') as f:
                f.write(f"# {self.title}\n")
                f.write(f"# {self.xlabel}\t{self.ylabel}\n")
                
                xdata = self.get_xdata()
                ydata = self.get_ydata()
                
                for x, y in zip(xdata, ydata):
                    if isinstance(y, complex):
                        f.write(f"{x}\t{y.real}\t{y.imag}\t{abs(y)}\t{numpy.angle(y)}\n")
                    else:
                        f.write(f"{x}\t{y}\n")
            return True
        except Exception:
            return False
    
    def _export_csv(self, filename: str) -> bool:
        """Export to CSV format."""
        try:
            import os
            import csv
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([self.xlabel, f"{self.ylabel}_Real", f"{self.ylabel}_Imag", f"{self.ylabel}_Abs", f"{self.ylabel}_Phase"])
                
                xdata = self.get_xdata()
                ydata = self.get_ydata()
                
                for x, y in zip(xdata, ydata):
                    if isinstance(y, complex):
                        writer.writerow([x, y.real, y.imag, abs(y), numpy.angle(y)])
                    else:
                        writer.writerow([x, y, "", "", ""])
            return True
        except Exception:
            return False
    
    def _export_touchstone(self, filename: str) -> bool:
        """Export to Touchstone format for S-parameters."""
        try:
            import os
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            # This is a simplified Touchstone export
            # Real implementation would need proper port mapping
            with open(filename, 'w') as f:
                f.write("# Hz S RI R 50\n")
                f.write(f"! {self.title}\n")
                
                xdata = self.get_xdata()
                ydata = self.get_ydata()
                
                for x, y in zip(xdata, ydata):
                    if isinstance(y, complex):
                        f.write(f"{x} {y.real} {y.imag}\n")
                    else:
                        f.write(f"{x} {y} 0\n")
            return True
        except Exception:
            return False


class ResultExporter:
    """Enhanced result export functionality."""
    
    def __init__(self, project_file: ProjectFile):
        self.project_file = project_file
        self.result_module = project_file.get_3d()
    
    def export_s_parameters(self, output_dir: str, ports: list = None, 
                           format_type: str = "touchstone") -> list:
        """Export S-parameters for specified ports.
        
        Args:
            output_dir: Output directory
            ports: List of port numbers (default: auto-detect)
            format_type: Export format
            
        Returns:
            List of exported filenames
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        exported_files = []
        
        # Get all S-parameter results
        tree_items = self.result_module.get_tree_items("S-Parameters")
        
        for item in tree_items:
            try:
                result_item = self.result_module.get_result_item(item)
                filename = os.path.join(output_dir, f"{item.replace('/', '_')}.{format_type}")
                
                if result_item.export_to_file(filename, format_type):
                    exported_files.append(filename)
            except Exception:
                continue
        
        return exported_files
    
    def export_all_1d_results(self, output_dir: str, format_type: str = "txt") -> dict:
        """Export all 1D results to files.
        
        Args:
            output_dir: Output directory
            format_type: Export format
            
        Returns:
            Dictionary with result types and exported files
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        exported_results = {}
        
        # Get all 1D results
        tree_items = self.result_module.get_tree_items("0D/1D")
        
        for item in tree_items:
            try:
                result_item = self.result_module.get_result_item(item)
                safe_name = item.replace('/', '_').replace('\\', '_').replace(':', '_')
                filename = os.path.join(output_dir, f"{safe_name}.{format_type}")
                
                if result_item.export_to_file(filename, format_type):
                    exported_results[item] = filename
            except Exception:
                continue
        
        return exported_results
    
    def export_field_data_2d(self, output_dir: str, monitor_names: list = None) -> dict:
        """Export 2D field data.
        
        Args:
            output_dir: Output directory
            monitor_names: List of monitor names to export
            
        Returns:
            Dictionary with monitor names and exported files
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        exported_fields = {}
        
        # Get all 2D field results
        tree_items = self.result_module.get_tree_items("2D/3D")
        
        for item in tree_items:
            if monitor_names and not any(name in item for name in monitor_names):
                continue
                
            try:
                result_item = self.result_module.get_result_item(item)
                safe_name = item.replace('/', '_').replace('\\', '_').replace(':', '_')
                filename = os.path.join(output_dir, f"{safe_name}.txt")
                
                if result_item.export_to_file(filename, "txt"):
                    exported_fields[item] = filename
            except Exception:
                continue
        
        return exported_fields
    
    def get_result_summary(self) -> dict:
        """Get summary of all available results.
        
        Returns:
            Dictionary with result categories and counts
        """
        summary = {
            "1D_results": [],
            "2D_results": [],
            "S_parameters": [],
            "farfield_results": [],
            "total_results": 0
        }
        
        try:
            # Count 1D results
            items_1d = self.result_module.get_tree_items("0D/1D")
            summary["1D_results"] = items_1d
            
            # Count 2D/3D results
            items_2d = self.result_module.get_tree_items("2D/3D")
            summary["2D_results"] = items_2d
            
            # Filter S-parameters
            s_params = [item for item in items_1d if "S-Parameter" in item or "S(" in item]
            summary["S_parameters"] = s_params
            
            # Filter farfield results
            farfield = [item for item in items_2d if "farfield" in item.lower()]
            summary["farfield_results"] = farfield
            
            summary["total_results"] = len(items_1d) + len(items_2d)
            
        except Exception as e:
            summary["error"] = str(e)
        
        return summary


# Convenience functions for enhanced result processing
def load_and_export_project_results(project_path: str, output_dir: str, 
                                   export_formats: list = None) -> dict:
    """Load project and export all results.
    
    Args:
        project_path: Path to CST project file
        output_dir: Output directory for exported files
        export_formats: List of formats to export (default: ["txt", "csv"])
        
    Returns:
        Summary of exported results
    """
    if export_formats is None:
        export_formats = ["txt", "csv"]
    
    try:
        # Load project
        project = ProjectFile(project_path)
        exporter = ResultExporter(project)
        
        export_summary = {
            "project_path": project_path,
            "output_dir": output_dir,
            "exported_files": {},
            "summary": {}
        }
        
        # Export in each requested format
        for fmt in export_formats:
            export_summary["exported_files"][fmt] = {
                "1d_results": exporter.export_all_1d_results(f"{output_dir}/1D", fmt),
                "s_parameters": exporter.export_s_parameters(f"{output_dir}/S_Parameters", format_type=fmt),
                "field_data": exporter.export_field_data_2d(f"{output_dir}/Fields")
            }
        
        # Get result summary
        export_summary["summary"] = exporter.get_result_summary()
        
        return export_summary
        
    except Exception as e:
        return {"error": str(e), "project_path": project_path}


def analyze_antenna_performance(project_path: str, target_frequency: float = None) -> dict:
    """Analyze antenna performance from CST results.
    
    Args:
        project_path: Path to CST project file
        target_frequency: Target frequency for analysis
        
    Returns:
        Performance analysis results
    """
    try:
        project = ProjectFile(project_path)
        result_module = project.get_3d()
        
        analysis = {
            "project_path": project_path,
            "target_frequency": target_frequency,
            "s_parameters": {},
            "bandwidth": {},
            "gain": {},
            "efficiency": {}
        }
        
        # Get S11 data
        s11_items = [item for item in result_module.get_tree_items("0D/1D") 
                     if "S1,1" in item or "S(1,1)" in item]
        
        if s11_items:
            s11_result = result_module.get_result_item(s11_items[0])
            freq_data = s11_result.get_xdata()
            s11_data = s11_result.get_ydata()
            
            # Convert to dB if complex
            if s11_data and isinstance(s11_data[0], complex):
                s11_db = [20 * numpy.log10(abs(s)) for s in s11_data]
            else:
                s11_db = list(s11_data)
            
            analysis["s_parameters"]["S11_dB"] = {
                "frequency": list(freq_data),
                "magnitude": s11_db,
                "min_value": min(s11_db) if s11_db else None,
                "min_frequency": freq_data[s11_db.index(min(s11_db))] if s11_db else None
            }
            
            # Calculate bandwidth (frequencies where S11 < -10 dB)
            bw_freqs = [f for f, s in zip(freq_data, s11_db) if s < -10]
            if len(bw_freqs) >= 2:
                analysis["bandwidth"] = {
                    "lower_freq": min(bw_freqs),
                    "upper_freq": max(bw_freqs),
                    "bandwidth": max(bw_freqs) - min(bw_freqs),
                    "fractional_bandwidth": (max(bw_freqs) - min(bw_freqs)) / ((max(bw_freqs) + min(bw_freqs)) / 2)
                }
        
        return analysis
        
    except Exception as e:
        return {"error": str(e), "project_path": project_path}


if __name__ == "__main__":
    a = cst.results.ProjectFile
    pass
