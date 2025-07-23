"""提供与`cst.interface`的接口。

The `cst.interface` module offers a general interface to the CST Studio Suite.

The cst.interface package provides a python interface that allows to control the
CST Studio Suite. It is possible to connect to a running DesignEnvironnent (main
screen) or start a new one. Once connected the package provides access to CST
projects (`.cst`) which can be opened, closed and saved and provide access to
the associated applications (`prj.model3d`)."""

import logging
import os
from typing import Dict, List, Union

import cst
import cst.interface

from . import _global

_logger = logging.getLogger(__name__)


class Model3D:
    """与`cst.interface.Model3D`的接口。

    This class provides an interface to the 3D Model.
    """

    def __init__(self, modeler: "cst.interface.Model3D"):
        """初始化

        Args:
            modeler (cst.interface.Model3D): 建模器对象。
        """
        self.model3d = modeler
        return

    def abort_solver(self, *, timeout: int = None) -> None:
        """Aborts the currently running (or paused) solver.

        Args:
            timeout (int, optional): 执行时间限制. Defaults to None.

        Returns:
            None
        """
        return self.model3d.abort_solver(timeout)

    def add_to_history(
        self, header: str, vba_code: str, *, timeout: int = None
    ) -> None:
        """AddToHistory creates a new history block in the modeler with the
        given header-name and executes the `vba_code`

        Args:
            header (str): 历史记录标题
            vba_code (str): VBA代码
            timeout (int, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        return self.model3d.add_to_history(header, vba_code, timeout=timeout)

    def get_active_solver_name(self, *, timeout: int = None) -> str:
        """Returns the currently active solver name.

        Args:
            timeout (int, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        return self.model3d.get_active_solver_name(timeout)

    def is_solver_running(self, *, timeout: int = None) -> bool:
        """Queries whether the solver is currently running.

        Args:
            timeout (int, optional): _description_. Defaults to None.

        Returns:
            bool: _description_
        """
        return self.model3d.is_solver_running(timeout)

    def pause_solver(self, *, timeout: int = None) -> None:
        return self.model3d.pause_solver(timeout)

    def resume_solver(self, *, timeout: int = None) -> None:
        return self.model3d.resume_solver(timeout)

    def run_solver(self, *, timeout: int = None) -> None:
        return self.model3d.run_solver(timeout)

    def start_solver(self, *, timeout: int = None) -> None:
        """Starts the currently selected solver asynchronously and gives back
        control to the calling script. It does not wait for the solver to
        finish, use in combination with `is_solver_running()`.

        Args:
            timeout (int, optional): 执行指令的限制时间，只接受整数，尚不清楚时间单位是什么. Defaults to None.

        Returns:
            None:
        """
        return self.model3d.start_solver(timeout=timeout)

    def get_solver_run_info(self, *, timeout: int = None) -> dict:
        """获取求解器运行信息
        
        Retrieves as dict containing information on the last or current solver run.
        
        Args:
            timeout (int, optional): 执行时间限制. Defaults to None.
            
        Returns:
            dict: 求解器运行信息
        """
        return self.model3d.get_solver_run_info(timeout)
    
    def full_history_rebuild(self, *, timeout: int = None) -> None:
        """触发完整的历史重建
        
        Trigger a full rebuild of the modeler history.
        
        Args:
            timeout (int, optional): 执行时间限制. Defaults to None.
            
        Returns:
            None
        """
        return self.model3d.full_history_rebuild(timeout)
    
    def get_tree_items(self, *, timeout: int = None) -> List[str]:
        """获取项目树的所有项目路径
        
        Returns a flat list of all tree paths.
        
        Args:
            timeout (int, optional): 执行时间限制. Defaults to None.
            
        Returns:
            List[str]: 所有树路径的列表
        """
        return self.model3d.get_tree_items(timeout)

    def create_object(self, obj: _global.BaseObject) -> None:
        """Creates a new object in the 3D modeler.

        Args:
            obj (_global.BaseObject): The object to create in the modeler.

        Returns:
            None
        """

        try:
            obj.create_from_attributes(self.model3d)
        except AttributeError:
            _logger.warning(
                "Object %s does not have create_from_attributes method, trying create_from_kwargs.",
                obj.__class__.__name__,
            )
            try:
                obj.create_from_kwargs(self.model3d)
            except AttributeError:
                _logger.error(
                    "Object %s does not have create_from_attributes or create_from_kwargs method.",
                    obj.__class__.__name__,
                )
        return


class Schematic:
    def __init__(self):
        pass


class InterfacePCBS:
    def __init__(self):
        pass


class Project:
    """与`cst.interface.Project`的接口

    Provides an interface to live CST projects. Offers capabilities to save and
    close projects, but also carries the associated interfaces to various
    applications.
    """

    def __init__(self, p: "cst.interface.Project"):
        self._proj = p
        self._model3d = Model3D(self._proj.model3d)
        self._dsn_env = DesignEnvironment(self._proj.design_environment)
        pass
    
    @staticmethod
    def open(path: os.PathLike) -> "Project":
        """在新的或现有的设计环境中打开项目
        
        Opens the given project in an existing or new DesignEnvironment.
        
        Args:
            path (os.PathLike): CST 项目文件的路径
            
        Returns:
            Project: 项目实例
            
        Raises:
            RuntimeError: 如果项目已经打开
        """
        proj = cst.interface.Project.open(path)
        return Project(proj)
    
    @staticmethod
    def connect(cst_file: os.PathLike) -> "Project":
        """连接到现有设计环境中的项目
        
        Connects to the given project file in an existing DesignEnvironment.
        
        Args:
            cst_file (os.PathLike): CST 项目文件的路径
            
        Returns:
            Project: 项目实例
            
        Raises:
            UserWarning: 如果项目未打开或不存在
        """
        proj = cst.interface.Project.connect(cst_file)
        return Project(proj)
    
    @staticmethod
    def connect_or_open(cst_file: os.PathLike) -> "Project":
        """连接到现有项目或打开新项目
        
        Connects to the given project file in an existing DesignEnvironment or opens it.
        
        Args:
            cst_file (os.PathLike): CST 项目文件的路径
            
        Returns:
            Project: 项目实例
            
        Raises:
            UserWarning: 如果项目不存在
        """
        proj = cst.interface.Project.connect_or_open(cst_file)
        return Project(proj)

    @property
    def model3d(self) -> Model3D:
        """Gives access to the 3D model (Model3D) associated with the project if
        it exists. Is None when there is no associated modeler.

        Returns:
            Model3D: the 3D model (Model3D) associated with the project
        """
        return self._model3d

    @property
    def design_environment(self) -> "DesignEnvironment":
        """The instance of the `DesignEnvironment` in which this Project is open"""
        return self._dsn_env

    def activate(self) -> None:
        """Makes this project the currently active project.

        Returns:
            None:
        """
        return self._proj.activate()

    def close(self) -> None:
        """Closes the project without saving.

        Returns:
            None:
        """
        return self._proj.close()

    def filename(self) -> str:
        """Returns the current filename of the project.

        Returns:
            str: current filename
        """
        return self._proj.filename()

    def folder(self) -> str:
        """Returns the folder pertaining to the project.

        Returns:
            str: folder name
        """
        return self._proj.folder()

    def get_messages(self):
        """Returns messages from the Messages Window if any."""
        return self._proj.get_messages()

    def save(
        self,
        path: os.PathLike = "",
        include_results: bool = True,
        allow_overwrite: bool = False,
    ) -> None:
        """Saves the project to the specified path and optionally includes the
        results. If no path is given (default) then the current filename will be
        used.

        Args:
            path (os.PathLike, optional): 包含文件名的绝对路径，留空则保持当前文件名. Defaults to "".
            include_results (bool, optional): 是否包含结果. Defaults to True.
            allow_overwrite (bool, optional): 是否允许覆盖. Defaults to False.

        Returns:
            None:
        """
        self._proj.save(path, include_results, allow_overwrite)
        _logger.info("project saved: %s", path)
        return


class DesignEnvironment:
    """与`cst.interface.DesignEnvironment`的接口。

    This class provides an interface to the CST Studio Suite main frontend.
    It allows to connect to, and open new CST Studio Suite instances.
    Furthermore it allows to open or create `.cst` projects.
    """

    def __init__(self, existing_env: cst.interface.DesignEnvironment = None):
        """如果不指定已有的设计环境，那就新建一个。

        Args:
            existing_env (cst.interface.DesignEnvironment, optional): 已有的设计环境. Defaults to None.
        """
        if existing_env is None:
            self._env = cst.interface.DesignEnvironment()
        else:
            self._env = existing_env
        pass
    
    @staticmethod
    def new(options: object = None, gui_linux: object = None, 
            process_info: "cst.interface.DesignEnvironment.ProcessInfo" = None, 
            env: object = None) -> "DesignEnvironment":
        """打开新的设计环境并连接
        
        Opens a new DE and connects to it.
        
        Args:
            options (object, optional): 命令行选项列表. Defaults to None.
            gui_linux (object, optional): Linux 环境下是否使用 GUI. Defaults to None.
            process_info (DesignEnvironment.ProcessInfo, optional): 进程信息. Defaults to None.
            env (object, optional): 环境变量. Defaults to None.
            
        Returns:
            DesignEnvironment: 新的设计环境实例
        """
        env_obj = cst.interface.DesignEnvironment.new(options, gui_linux, process_info, env)
        return DesignEnvironment(env_obj)
    
    @staticmethod
    def connect(pid: int = None, tcp_address: str = None) -> "DesignEnvironment":
        """连接到现有的设计环境
        
        Connects to an existing DE with given PID or TCP address.
        
        Args:
            pid (int, optional): 进程 ID. Defaults to None.
            tcp_address (str, optional): TCP 地址. Defaults to None.
            
        Returns:
            DesignEnvironment: 连接的设计环境实例
        """
        if pid is not None:
            env_obj = cst.interface.DesignEnvironment.connect(pid)
        elif tcp_address is not None:
            env_obj = cst.interface.DesignEnvironment.connect(tcp_address)
        else:
            raise ValueError("Must provide either pid or tcp_address")
        return DesignEnvironment(env_obj)
    
    @staticmethod
    def connect_to_any() -> "DesignEnvironment":
        """连接到任意现有的设计环境
        
        Connects to any existing DE.
        
        Returns:
            DesignEnvironment: 连接的设计环境实例
        """
        env_obj = cst.interface.DesignEnvironment.connect_to_any()
        return DesignEnvironment(env_obj)
    
    @staticmethod
    def connect_to_any_or_new() -> "DesignEnvironment":
        """连接到现有设计环境或创建新的
        
        Connects to any existing DE or opens a new one if none are open.
        
        Returns:
            DesignEnvironment: 设计环境实例
        """
        env_obj = cst.interface.DesignEnvironment.connect_to_any_or_new()
        return DesignEnvironment(env_obj)

    def new_mws(self) -> Project:
        """创建新的 CST Microwave Studio 项目
        
        Creates a new CST Microwave Studio project and returns an instance of Project.
        
        Returns:
            Project: 新创建的项目实例
        """
        proj = self._env.new_mws()
        return Project(proj)
    
    def open_project(self, path: os.PathLike) -> Project:
        """打开指定路径的项目
        
        Opens the project given by path in a new tab and returns an instance of Project.
        
        Args:
            path (os.PathLike): CST 项目文件的路径
            
        Returns:
            Project: 项目实例
        """
        proj = self._env.open_project(path)
        return Project(proj)
    
    def close(self) -> None:
        """关闭设计环境（CST Studio Suite）
        
        Closes the DesignEnvironment.
        
        Returns:
            None
        """
        return self._env.close()
    
    def is_connected(self) -> bool:
        """检查设计环境是否已连接
        
        Returns whether this object is still connected to a live DE.
        
        Returns:
            bool: True if connected, False otherwise
        """
        return self._env.is_connected()
    
    def active_project(self) -> Project:
        """获取当前活动项目
        
        Get the currently active project.
        
        Returns:
            Project: 当前活动项目，如果没有则返回 None
        """
        proj = self._env.active_project()
        return Project(proj) if proj else None
    
    def has_active_project(self) -> bool:
        """查询设计环境是否有活动项目
        
        Queries whether the DesignEnvironment has an active project.
        
        Returns:
            bool: True if has active project, False otherwise
        """
        return self._env.has_active_project()
    
    def get_open_projects(self, re_filter: str = ".*") -> List[Project]:
        """返回当前打开的项目列表
        
        Returns a list of currently open projects matching the regular expression filter.
        
        Args:
            re_filter (str): 项目名称的正则表达式过滤器. Defaults to ".*".
            
        Returns:
            List[Project]: 打开的项目列表
        """
        projects = self._env.get_open_projects(re_filter)
        return [Project(p) for p in projects]
    
    def list_open_projects(self) -> List[str]:
        """返回当前打开项目的路径列表
        
        Returns the paths of the currently open projects.
        
        Returns:
            List[str]: 打开项目的路径列表
        """
        return self._env.list_open_projects()
    
    def pid(self) -> int:
        """返回设计环境的进程 ID
        
        Return the Process ID (PID) to which this DesignEnvironment is connected.
        
        Returns:
            int: 进程 ID
        """
        return self._env.pid()
    
    def set_quiet_mode(self, flag: bool) -> None:
        """设置静默模式
        
        When flag is set to True message boxes are suppressed.
        
        Args:
            flag (bool): True 启用静默模式，False 禁用静默模式
            
        Returns:
            None
        """
        return self._env.set_quiet_mode(flag)
    
    def in_quiet_mode(self) -> bool:
        """查询是否处于静默模式
        
        Queries whether message boxes are currently suppressed.
        
        Returns:
            bool: True if in quiet mode, False otherwise
        """
        return self._env.in_quiet_mode()


def running_design_environments() -> List[int]:
    """返回当前运行的设计环境进程 ID 列表
    
    Returns a list of process IDs (PIDs) of currently running DesignEnvironments.
    
    Returns:
        List[int]: 运行中的设计环境进程 ID 列表
    """
    return cst.interface.running_design_environments()
