"""通用绘图对象。"""
import logging

from .. import interface
from .._global import BaseObject, Parameter
from ..common import NEW_LINE, quoted
from ..shape_operations import Solid

_logger = logging.getLogger(__name__)


class Background(BaseObject):
    """The background object defines the kind of material that surrounds your
    structure. And defines its volume. By default the volume is defined by the
    maximum distances of your structure.

    Attributes:
        Type (str):
            Sets the material type used for the background.

            `Type` can have one of the following values ->

            `"normal"` (Not conducting, with relative permittivity epsilon and
            relative permeability mu);

            `"pec"` (Perfect electric conducting material).
        Epsilon (str):
            Defines the electric permittivity of the background material.
        Mu (str):
            Defines the permeability of the background material.
        ElConductivity (str):
            Defines the electric conductivity of the background material. This
            value is considered only for Low Frequency simulations.
        XminSpace (str):
            Adds space to the lower or upper x, y or z boundary of the current
            calculation volume respectively.
        XmaxSpace (str):
            same as `XminSpace`.
        YminSpace (str):
            same as `XminSpace`.
        YmaxSpace (str):
            same as `XminSpace`.
        ZminSpace (str):
            same as `XminSpace`.
        ZmaxSpace (str):
            same as `XminSpace`.
        ThermalType (str):
            Sets the material type used for the background. `ThermalType` can
            have one of the following values: `"normal"` (Not thermal
            conducting, with relative permittivity epsilon and relative
            permeability mu.); `"ptc"` (Perfect thermal conducting material).
        ThermalConductivity (str): Thermal conductivity is a property of
            materials that expresses the heat flux f (`W/m2`) that will flow
            through the material if a certain temperature gradient DT (`K/m`)
            exists over the material. The unit for value is `W/K/m`.
        ApplyInAllDirections (bool):
            Is at the moment used for the background dialog to identify if the
            xmin value should be applied in all directions.



    Default Settings::
        Type ("pec")
        Epsilon (1.0)
        Mu (1.0)
        XminSpace (0.0)
        XmaxSpace (0.0)
        YminSpace (0.0)
        YmaxSpace (0.0)
        ZminSpace (0.0)
        ZmaxSpace (0.0)
        ThermalType ("normal")
        ThermalConductivity (0.0)
        ApplyInAllDirections (False)
    """

    def __init__(self, *, attributes: dict[str, str] = None, **kwargs):
        super().__init__(attributes=attributes, **kwargs)
        self._history_title = "define background"
        return

    def create_from_attributes(self, modeler) -> "Background":
        """从属性列表设置背景属性。

        Args:
            modeler (interface.Model3D): 建模环境。

        Returns:
            self (Background): self
        """
        if not self._attributes:
            _logger.error("No valid properties.")
        else:
            scmd1 = [
                "With Background  ",
                ".ResetBackground ",
            ]
            cmd1 = NEW_LINE.join(scmd1)
            scmd2 = []
            for k, v in self._attributes.items():
                scmd2.append(f".{k} {v}")
            cmd2 = NEW_LINE.join(scmd2)
            scmd3 = [
                "End With",
            ]
            cmd3 = NEW_LINE.join(scmd3)
            cmd = NEW_LINE.join((cmd1, cmd2, cmd3))
            modeler.add_to_history(self._history_title, cmd)
        return self


class Boundary(BaseObject):
    """Represents the boundary condition of the calculation domain for each 
    boundary plane. You may either have a magnetic, electric or an open boundary 
    condition.

    Attributes:
        Xmin (str):
            `Xmin (enum boundaryType)`.
            `Xmin`, `Xmax`, `Ymin`, `Ymax`, `Zmin` and `Zmax` specifiy the
            boundary conditions for the lower or upper x, y or z calculation
            domain boundary respectively.
            `boundaryType` can have one of the following values ->
            `"electric"` Electric boundary condition (Etan = 0)
            `"magnetic"` Magnetic boundary condition (Htan = 0)
            `"tangential"` All tangential field components for all sorts of
            fields are zero.
            `"normal"` All normal field components for all sorts of  fields are
            zero.
            `"open"` Simulates the open space.
            `"expanded open"` Same as "open" but adds some extra space to the
            calculation domain.
            `"periodic"` Simulates a periodic expansion of the calculation
            domain.
            `"conducting wall"` This boundary behaves like a wall of lossy metal
            material.
            `"unit cell"` Simulates a unit cell structure.
        Xmax (str): see `Xmin`.
        Ymin (str): see `Xmin`.
        Ymax (str): see `Xmin`.
        Zmin (str): see `Xmin`.
        Zmax (str): see `Xmin`.

        Xsymmetry (str):
            `Xsymmetry (enum symmetryType)`.
            `Xsymmetry`, `Ysymmetry` and `Zsymmetry` define if the structure is
            electrically or magnetically symmetric regarding the origin of the
            x, y or z-axis respectively.
            `symmetryType` can have one of the following values ↓↓↓
            `"electric"` All tangential E-fields are considered zero at the
            symmetry plane.
            `"magnetic"` All tangential H-fields are considered zero at the
            symmetry plane.
            `"none"` No symmetry.
        Ysymmetry (str): see `Xsymmetry`.
        Zsymmetry (str): see `Xsymmetry`.

        ApplyInAllDirections (str):
            `ApplyInAllDirections (bool switch)`.
            Is used by the background dialog to identify if the `Xmin` value
            should be applied in all the other directions.

        XminPotentialType (str):
            `XminPotentialType (enum type)`.
            Specifies the potential type of the lower and upper boundaries. The
            setting of a potential value is only enabled if the type of the
            boundary is set to "normal" or "electric". The potential type can
            have one of the following values ->
            `"none"` No potential is considered on the corresponding boundary.
            `"fixed"` On the boundaries a fixed potential can be defined by use
            of the corresponding Potential methods (see below).
            `"floating"` The potential is defined as floating on the
            corresponding boundary.
        XmaxPotentialType (str): see `XminPotentialType`.
        YminPotentialType (str): see `XminPotentialType`.
        YmaxPotentialType (str): see `XminPotentialType`.
        ZminPotentialType (str): see `XminPotentialType`.
        ZmaxPotentialType (str): see `XminPotentialType`.

        XminPotential (str):
            `XminPotential (double potvalue)`.
            Specifies the potential values of the lower and upper boundaries.
            The setting of a potential value has only an effect if the type of
            the boundary is set to "normal" or "electric" and the corresponding
            `PotentialType` is set to "fixed".
        YminPotential (str): see `XminPotential`.
        ZminPotential (str): see `XminPotential`.
        XmaxPotential (str): see `XminPotential`.
        YmaxPotential (str): see `XminPotential`.
        ZmaxPotential (str):see `XminPotential`.

        XminThermal (str):
            `XminThermal (enum ThermalBoundaryType)`.
            `thermalBoundaryType` can have one of the following values ->
            `"isothermal"` Boundary condition with constant temperature
            (T=const). This boundary type can carry a temperature definition.
            `"adiabatic"` Boundary condition without any heat-flow through the
            boundary (dT / dN = 0).
            `"open"` Simulates the open space.
            `"expanded open"` Same as ”open” but adds some extra space to the
            calculation domain.
        XmaxThermal (str): see `XminThermal`.
        YminThermal (str): see `XminThermal`.
        YmaxThermal (str): see `XminThermal`.
        ZminThermal (str): see `XminThermal`.
        ZmaxThermal (str): see `XminThermal`.

        XsymmetryThermal (str):
            `XsymmetryThermal (enum ThermalSymmetryType)`.
            `thermalSymmetryType` can have one of the following values ->
            "isothermal" Symmetry condition with constant temperature at the symmetry plane (T=const).
            "adiabatic" Symmetry condition without any heat-flow through the symmetry plane (dT / dN = 0).
            "none" No symmetry.
            ”expanded open” Same as ”open” but adds some extra space to the calculation domain.
        YsymmetryThermal (str): see `XsymmetryThermal`.
        ZsymmetryThermal (str): see `XsymmetryThermal`.

        XminTemperature (str):
            `XminTemperatureType (enum type)`.
            Specifies the temperature values of the lower and upper boundaries.
            This settings has only an effect if the type of the corresponding
            `TemperatureType` is set to "fixed".
        XmaxTemperature (str): see `XminTemperature`.
        YminTemperature (str): see `XminTemperature`.
        YmaxTemperature (str): see `XminTemperature`.
        ZminTemperature (str): see `XminTemperature`.
        ZmaxTemperature (str): see `XminTemperature`.

        Layer (str):
            `Layer (int numLayers)`.
            Specifies the number of PML layers. Usually 4 layers are sufficient.
        MinimumLinesDistance (str):
            `MinimumLinesDistance (double value)`.
            Specifies the minimum distance from the PML boundary to the
            structure to be modeled. The distance is determined by the absolute
            number of grid lines.
        MinimumDistanceType (str):
            `MinimumDistanceReferenceFrequencyType (enum {"Center", "Centernmonitors", "User"} type)`.
            Selecting the Fraction option activates the geometrical domain
            enlargement computed as a fraction of the wavelength. With the
            Absolute option the distance is directly given in geometrical user
            units. To this purpose use the SetAbsoluteDistance command.
        SetAbsoluteDistance  (str):
            `SetAbsoluteDistance (double value)`.
            Specifies the absolute distance to enlarge the simulation domain.
            To be used selecting the Absolute option with the command
            `MinimumDistanceType`.
        MinimumDistanceReferenceFrequencyType (str):
            `MinimumDistanceReferenceFrequencyType (enum {"Center", "Centernmonitors", "User"} type)`.
            The command determines the reference frequency where the wavelength
            has to be computed. The command should be used jointly with the
            MinimumDistanceType command activating the Fraction option.
            `"Center"` means that the reference frequency is the mid simulation
            frequency, in formula (FMin+FMax)/2.
            The second choice `"Centernmonitors"` computes the reference frequency
            as the minimum non zero frequency selected among the center
            frequency and the user defined relevant  monitor frequencies.
            The third possibility is `"User"`, which enables to specify directly
            the frequency with the companion FrequencyForMinimumDistance command.
        MinimumDistancePerWavelength (str):
            `MinimumDistancePerWavelength (double value)`.
            Specifies the minimum distance from the PML boundary to the
            structure to be modeled. The distance is determined relatively to
            the wavelength, either in respect to the center frequency, center
            and monitor frequencies or to a user defined frequency value. See
            also the `MinimumDistanceReferenceFrequencyType` command.
        FrequencyForMinimumDistance (str):
            `FrequencyForMinimumDistance (double value)`.
            Specifies the frequency which represents the reference value for the
            `MinimumDistancePerWavelength` method.

        XPeriodicShift (float):
            `XPeriodicShift (double value)`.
            Enables to define a phase shift value for a periodic boundary
            condition. Please note that the phase shift only applies to the
            frequency domain solver and the eigenmode solver. The settings are
            ignored by the transient solver.
        YPeriodicShift (float): see `XPeriodicShift`.
        ZPeriodicShift (float): see `XPeriodicShift`.

        PeriodicUseConstantAngles (bool):
            `PeriodicUseConstantAngles (bool bFlag)`
            In contrast to the definition of a constant phase shift between two
            opposite periodic boundaries (using the `XPeriodicShift`,
            `YPeriodicShift` or `ZPeriodicShift` methods) it is also possible to
            define an incident angle value of the normal propagation direction
            of a virtual plane wave entering the calculation domain. The angle
            can be defined in a spherical coordinate system using the
            `SetPeriodicBoundaryAngles` method. In fact this procedure also
            realizes a phase shift between the periodic boundaries, however,
            this time it depends on the current frequency sample. You can
            activate (bFlag = True) or deactivate (bFlag = False) this option
            using the present method.

        SetPeriodicBoundaryAngles (str):
            `SetPeriodicBoundaryAngles (double theta, double phi)`
            Defines the angle in a spherical coordinate system using theta and
            phi values for the calculation of phase shifts between periodic
            boundaries. The z-axis corresponds to that of the global coordinate
            system.

            Please note that this method is only relevant for the frequency
            domain solver and in case that the `PeriodicUseConstantAngles`
            method is activated or unit cell boundaries are used.
        SetPeriodicBoundaryAnglesDirection (str):
            `SetPeriodicBoundaryAnglesDirection (enum direction)`.
            `direction` defines whether the scan angle defined with
            `SetPeriodicBoundaryAngles` refers to an inward or outward (with
            respect to the radial unit vector in the spherical coordinate
            system) propagating plane wave, and can have one of the following
            values ->
            `”outward”` The phase is set for an outward traveling plane wave.
            Floquet modes should be excited at Zmin.
            `”inward”` The phase is set for an inward traveling plane wave.
            Floquet modes should be excited at Zmax.


        UnitCellDs1 (str):
            `UnitCellDs1 (double value)`.
            These two methods specify the distances between two neighboring unit
            cells in two different coordinate directions, whereby the first axis
            (UnitCellDs1) is always aligned to the x-axis of the global
            coordinate system. The spatial relation between these two axes is
            defined by the `UnitCellAngle` method.
        UnitCellDs2 (str): see `UnitCellDs1`.

        UnitCellAngle (str):
            `UnitCellAngle (double value)`.
            Specifies the spatial relation between the two axes defined by the
            methods `UnitCellDs1` and `UnitCellDs2`.
            Please note, that the hexahedral frequency domain solver needs a
            value of 90 degree for this value.
        UnitCellOrigin (str):
            `UnitCellOrigin  ( double posx, double posy )`.
            Allows to shift the origin of the unit cell and thereby the
            calculation domain for the frequency domain solver with tetrahedral
            mesh. The values may range from zero to one, where the default zero
            lets the center of the bounding box and the center of the unit cell
            coincide, while a value of one moves the origin by half the size of
            the unit cell lattice in the corresponding direction.
        UnitCellFitToBoundingBox (str):
            `UnitCellFitToBoundingBox  ( bool bFlag )`.
            If this method is activated, the structure model will be repeated at
            its bounding box borders, neglecting any settings of the methods
            `UnitCellDs1`, `UnitCellDs2` and `UnitCellAngle`.


    """

    def __init__(self, *, attributes=None, vba=None, **kwargs):
        super().__init__(attributes=attributes, vba=vba, **kwargs)
        return

    def create_from_attributes(self, modeler):
        """从属性字典定义边界条件。下面的实现给出了一个通用的范式。

        Args:
            modeler (interface.Model3D): 建模环境。

        Returns:
            self (BaseObject): self
        """
        if not self._attributes:
            _logger.error("No valid properties.")
        else:
            scmd1 = [
                "With Boundary ",
            ]
            cmd1 = NEW_LINE.join(scmd1)
            scmd2 = []
            for k, v in self._attributes.items():
                scmd2.append(f".{k} {v}")
            cmd2 = NEW_LINE.join(scmd2)
            scmd3 = [
                "End With",
            ]
            cmd3 = NEW_LINE.join(scmd3)
            cmd = NEW_LINE.join((cmd1, cmd2, cmd3))
            modeler.add_to_history(self._history_title, cmd)
        return self


class LayerStacking(BaseObject):
    """The `layerstacking` object can be used to define one or more background 
    items to the project. The specified layers differ in thickness and material 
    and are aligned at the borders of the bounding box.

    Attributes:
        param1 (type): 1st attribute.
    """

    def __init__(self, *, attributes=None, vba=None, **kwargs):
        super().__init__(attributes=attributes, vba=vba, **kwargs)
        return


class ParameterSweep(BaseObject):
    """参数扫描控制类
    
    Allows to automatically perform several simulations with varying parameters.
    """

    def __init__(self, *, attributes=None, vba=None, **kwargs):
        super().__init__(attributes=attributes, vba=vba, **kwargs)
        self._parameters = {}
        self._sweep_type = "Linear"
        return
    
    def add_parameter(self, parameter_name: str, start_value: float, 
                     end_value: float, steps: int, sweep_type: str = "Linear") -> None:
        """添加扫描参数
        
        Args:
            parameter_name (str): 参数名称
            start_value (float): 起始值
            end_value (float): 结束值
            steps (int): 步数
            sweep_type (str): 扫描类型 ("Linear", "Logarithmic")
        """
        self._parameters[parameter_name] = {
            'start': start_value,
            'end': end_value,
            'steps': steps,
            'type': sweep_type
        }
    
    def add_parameter_sequence(self, parameter_name: str, values: list) -> None:
        """添加参数序列
        
        Args:
            parameter_name (str): 参数名称
            values (list): 参数值列表
        """
        self._parameters[parameter_name] = {
            'values': values,
            'type': 'Sequence'
        }
    
    def create_parameter_sweep(self, modeler) -> None:
        """创建参数扫描
        
        Args:
            modeler (interface.Model3D): 建模环境
        """
        if not self._parameters:
            _logger.error("No parameters defined for sweep")
            return
        
        # 生成 VBA 代码
        vba_lines = []
        
        # 开始参数扫描定义
        vba_lines.append("With ParameterSweep")
        vba_lines.append("    .DeleteAll")
        
        # 添加每个参数
        for param_name, param_config in self._parameters.items():
            if param_config.get('type') == 'Sequence':
                # 序列类型参数
                values_str = ";".join(str(v) for v in param_config['values'])
                vba_lines.extend([
                    f'    .AddParameter_Samples "{param_name}", "{values_str}"'
                ])
            else:
                # 线性或对数扫描
                sweep_type = param_config.get('type', 'Linear')
                vba_lines.extend([
                    f'    .AddParameter_Linear "{param_name}", {param_config["start"]}, {param_config["end"]}, {param_config["steps"]}'
                ])
        
        vba_lines.append("End With")
        
        # 执行 VBA 代码
        vba_code = NEW_LINE.join(vba_lines)
        modeler.add_to_history("Define Parameter Sweep", vba_code)
    
    def start_parameter_sweep(self, modeler) -> None:
        """启动参数扫描
        
        Args:
            modeler (interface.Model3D): 建模环境
        """
        vba_code = "ParameterSweep.Start"
        modeler.add_to_history("Start Parameter Sweep", vba_code)
    
    def get_sweep_results(self, modeler) -> dict:
        """获取扫描结果（通过 VBA 查询）
        
        Args:
            modeler (interface.Model3D): 建模环境
            
        Returns:
            dict: 扫描结果信息
        """
        # 这里可以添加查询扫描结果的 VBA 代码
        # 返回基本状态信息
        return {
            'parameters': list(self._parameters.keys()),
            'sweep_configured': len(self._parameters) > 0
        }


class Optimizer(BaseObject):
    """优化控制类
    
    With the optimizer object you may start an optimization run. For the 
    optimization you have to define a set of parameters that will be changed by 
    the optimizer and at least one goal function that is tried to be optimized.  
    The kind of goal function depends on the chosen solver type.
    """

    def __init__(self, *, attributes=None, vba=None, **kwargs):
        super().__init__(attributes=attributes, vba=vba, **kwargs)
        self._parameters = {}
        self._goals = {}
        self._method = "Trust Region"
        return
    
    def add_optimization_parameter(self, parameter_name: str, min_value: float, 
                                 max_value: float, start_value: float = None) -> None:
        """添加优化参数
        
        Args:
            parameter_name (str): 参数名称
            min_value (float): 最小值
            max_value (float): 最大值
            start_value (float, optional): 起始值
        """
        if start_value is None:
            start_value = (min_value + max_value) / 2
            
        self._parameters[parameter_name] = {
            'min': min_value,
            'max': max_value,
            'start': start_value
        }
    
    def add_optimization_goal(self, goal_name: str, goal_type: str, 
                            target_value: float = None, weight: float = 1.0) -> None:
        """添加优化目标
        
        Args:
            goal_name (str): 目标名称（如 "S1,1"）
            goal_type (str): 目标类型 ("minimize", "maximize", "target")
            target_value (float, optional): 目标值（对于 target 类型）
            weight (float): 权重
        """
        self._goals[goal_name] = {
            'type': goal_type,
            'target': target_value,
            'weight': weight
        }
    
    def set_optimization_method(self, method: str) -> None:
        """设置优化方法
        
        Args:
            method (str): 优化方法 ("Trust Region", "Genetic Algorithm", "Nelder Mead Simplex")
        """
        self._method = method
    
    def create_optimization(self, modeler) -> None:
        """创建优化配置
        
        Args:
            modeler (interface.Model3D): 建模环境
        """
        if not self._parameters:
            _logger.error("No parameters defined for optimization")
            return
        
        if not self._goals:
            _logger.error("No goals defined for optimization")
            return
        
        # 生成 VBA 代码
        vba_lines = []
        
        # 开始优化定义
        vba_lines.append("With Optimizer")
        vba_lines.append("    .Reset")
        vba_lines.append(f'    .SetOptimizerType "{self._method}"')
        
        # 添加优化参数
        for param_name, param_config in self._parameters.items():
            vba_lines.extend([
                f'    .SelectParameter "{param_name}"',
                f'    .SetParameterInit {param_config["start"]}',
                f'    .SetParameterMin {param_config["min"]}',
                f'    .SetParameterMax {param_config["max"]}',
                f'    .AddParameter'
            ])
        
        # 添加优化目标
        for goal_name, goal_config in self._goals.items():
            goal_type = goal_config['type']
            if goal_type == "target" and goal_config['target'] is not None:
                vba_lines.extend([
                    f'    .AddGoal "{goal_name}"',
                    f'    .SetGoalTarget {goal_config["target"]}',
                    f'    .SetGoalWeight {goal_config["weight"]}'
                ])
            elif goal_type in ["minimize", "maximize"]:
                vba_lines.extend([
                    f'    .AddGoal_{goal_type.capitalize()} "{goal_name}"',
                    f'    .SetGoalWeight {goal_config["weight"]}'
                ])
        
        vba_lines.append("End With")
        
        # 执行 VBA 代码
        vba_code = NEW_LINE.join(vba_lines)
        modeler.add_to_history("Define Optimization", vba_code)
    
    def start_optimization(self, modeler) -> None:
        """启动优化
        
        Args:
            modeler (interface.Model3D): 建模环境
        """
        vba_code = "Optimizer.Start"
        modeler.add_to_history("Start Optimization", vba_code)
    
    def get_optimization_results(self, modeler) -> dict:
        """获取优化结果（通过 VBA 查询）
        
        Args:
            modeler (interface.Model3D): 建模环境
            
        Returns:
            dict: 优化结果信息
        """
        # 这里可以添加查询优化结果的 VBA 代码
        # 返回基本状态信息
        return {
            'parameters': list(self._parameters.keys()),
            'goals': list(self._goals.keys()),
            'method': self._method,
            'optimization_configured': len(self._parameters) > 0 and len(self._goals) > 0
        }


class SolverParameter(BaseObject):
    """This object controls the model simplification settings for a specific solver.

    Attributes:
        param1 (type): 1st attribute.
    """

    def __init__(self, *, attributes=None, vba=None, **kwargs):
        super().__init__(attributes=attributes, vba=vba, **kwargs)
        return


class ADSCosimulation(BaseObject):
    """In addition to its tight integration into the CST Design Environment, CST 
    Microwave Studio also features strong interfaces to Keysight ADS®. Besides 
    the ”static” link option offering the possibility to use pre-computed 
    S-parameter data in ADS circuit simulations, the ”co-simulation” alternative 
    enables ADS to launch CST Microwave Studio in order to automatically 
    calculate required data. All information is then stored together with the 
    CST Microwave Studio model in order to avoid unnecessary repetitions of 
    lengthy EM simulations.

    Please note that this advanced interface requires ADS 2005A or above and 
    needs CST Microwave Studio and ADS being installed on the same computer. CST 
    Microwave Studio manages an ADS Design Kit which contains a dynamically 
    extended list of EM simulation components. Once the ADS Design Kit is 
    installed, the library based on CST Microwave Studio models will be 
    accessible through the ADS library browser.

    For more detailed information about this and the installation of the ADS 
    Design Kit please refer to the CST Studio Suite - Getting Started manual or 
    the ADS documentation which is located in the CST Microwave Studio global 
    macro directory in the subfolder "ADS\\DesignKit".

    Attributes:
        param1 (type): 1st attribute.
    """

    def __init__(self, *, attributes=None, vba=None, **kwargs):
        super().__init__(attributes=attributes, vba=vba, **kwargs)
        return


class SimuliaCSE(BaseObject):
    """This object offers the possibility to run a co-simulation using Simulia 
    Co-Simulation Engine (CSE).

    Attributes:
        param1 (type): 1st attribute.
    """

    def __init__(self, *, attributes=None, vba=None, **kwargs):
        super().__init__(attributes=attributes, vba=vba, **kwargs)
        return
