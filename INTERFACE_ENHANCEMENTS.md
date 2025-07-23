# mzcst_2024 Interface Enhancements

## 更新时间
2025-01-22

## 更新说明

本次更新为 `mzcst_2024.interface` 模块添加了完整的 CST Studio Suite 接口功能，特别是项目管理和设计环境控制功能。

## 新增功能

### DesignEnvironment 类新增方法

#### 项目管理
- `open_project(path)` - 打开指定路径的 CST 项目文件
- `active_project()` - 获取当前活动项目
- `has_active_project()` - 检查是否有活动项目
- `get_open_projects(re_filter=".*")` - 获取打开的项目列表（支持正则过滤）
- `list_open_projects()` - 获取打开项目的路径列表

#### 连接和环境控制
- `close()` - 关闭设计环境（CST Studio Suite）
- `is_connected()` - 检查设计环境连接状态
- `pid()` - 获取设计环境进程 ID
- `set_quiet_mode(flag)` - 设置静默模式
- `in_quiet_mode()` - 查询是否处于静默模式

#### 静态方法
- `DesignEnvironment.new()` - 创建新的设计环境
- `DesignEnvironment.connect(pid/tcp_address)` - 连接到现有设计环境
- `DesignEnvironment.connect_to_any()` - 连接到任意现有设计环境
- `DesignEnvironment.connect_to_any_or_new()` - 连接到现有或创建新的设计环境

### Project 类新增方法

#### 静态方法
- `Project.open(path)` - 在新的或现有设计环境中打开项目
- `Project.connect(cst_file)` - 连接到现有设计环境中的项目
- `Project.connect_or_open(cst_file)` - 连接到现有项目或打开新项目

### 模块级函数
- `running_design_environments()` - 获取运行中的设计环境进程 ID 列表

## 使用示例

### 1. 打开现有项目

```python
import mzcst_2024 as mz

# 方法1：通过设计环境打开
de = mz.interface.DesignEnvironment()
project = de.open_project("C:/path/to/project.cst")

# 方法2：直接打开项目（推荐）
project = mz.interface.Project.open("C:/path/to/project.cst")
```

### 2. 连接到现有设计环境

```python
import mzcst_2024 as mz

# 连接到任意现有设计环境
de = mz.interface.DesignEnvironment.connect_to_any()

# 连接到指定 PID 的设计环境
de = mz.interface.DesignEnvironment.connect(pid=12345)

# 获取活动项目
if de.has_active_project():
    project = de.active_project()
```

### 3. 管理项目和环境

```python
import mzcst_2024 as mz

de = mz.interface.DesignEnvironment()

# 查看打开的项目
open_projects = de.get_open_projects()
project_paths = de.list_open_projects()

# 设置静默模式
de.set_quiet_mode(True)

# 关闭项目和环境
project.close()  # 关闭项目
de.close()       # 关闭设计环境
```

### 4. 检查运行状态

```python
import mzcst_2024 as mz

# 获取所有运行中的设计环境
running_pids = mz.interface.running_design_environments()
print(f"运行中的设计环境: {running_pids}")

# 检查连接状态
de = mz.interface.DesignEnvironment()
if de.is_connected():
    print(f"连接到进程 {de.pid()}")
```

## 兼容性

- 基于 CST Studio Suite 2024/2025 原生 Python API
- 保持与现有 mzcst_2024 代码的完全兼容性
- 支持所有现有的项目操作（创建、保存、关闭等）

## 技术细节

所有新增方法都是对 CST 原生 `cst.interface` 模块的直接封装，提供了：
- 完整的类型提示
- 中英文双语文档
- 错误处理和异常传递
- 与 mzcst_2024 风格一致的 API 设计

## 测试建议

更新后建议测试以下场景：
1. 打开现有 CST 项目文件
2. 在多个设计环境间切换
3. 项目的保存和关闭操作
4. 设计环境的连接和关闭
5. 静默模式的设置和查询

## 后续计划

这些功能将在下一个版本中提交到 mzcst_2024 主分支，为 CHATEM 项目提供完整的 CST 控制能力。