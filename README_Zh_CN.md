# 自述文件

| 中文 | [English](http://aspidites.org) |

* * *

- Woma 编程语言适合哪些人？
  - 首先，它适用于想要为 CPython 编写扩展的人。 传统上，这些是用 C++ 和 C 编写的。Cython 工具用于静态编译纯 Python 模块。Woma 的优点是它是纯 python 模块的简写，这些模块具有良好的约束和类型检查，并且这些模块可以使用 Cython 轻松编译。

- 这不是带有额外步骤的 Cython 吗？
  - 嗯，是的，但目标完全不同。 Cython 打算成为 python 的句法超集，其中 Woma 语法从各种来源中汲取灵感。您可以将 Aspidites 视为 Cython 的包装器，它将 Woma 代码解析为 Cython 的 Python 超集。 Cython 做了很多“繁重的工作”。 Woma 编程语言的细节正在被标准化为一系列 WEEP（Woma 扩展和评估建议）。

- 为什么使用 Aspidites 这个名字？什么是 Woma？
  - 还有一个叫做 Aspidites 的 Python 属，拉丁语是盾牌承载者，这就是这个项目的同名。它们是澳大利亚大陆特有的，也被称为沃玛蟒。

- 我如何获得 Aspidites？
  - 我们为 Aspidites 维护了几个包，但是，我们建议使用 PyPI 安装以获得最新的稳定版本。 Docker 是获取 Aspidites 最前沿开发版本的地方。

- 怎样才能真正学会Woma编程语言？
  - 使用 https://woma.rtfd.io 上的文档

### 安装
--------------

[![PyPI](https://img.shields.io/pypi/v/aspidites?label=PyPI&logo=pypi)](https://pypi.org/project/Aspidites/)[![PyPI - Wheel](https://img.shields.io/pypi/wheel/Aspidites)](https://pypi.org/project/Aspidites/#files)![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Aspidites?label=CPython)![PyPI - Downloads](https://img.shields.io/pypi/dd/Aspidites)
```
$ pip install Aspidites
```
-----------
![Docker Image Version (latest by date)](https://img.shields.io/docker/v/rjdbcm/aspidites?label=Docker&logo=docker)[![Docker Image Size (latest semver)](https://img.shields.io/docker/image-size/rjdbcm/aspidites)](https://hub.docker.com/r/rjdbcm/aspidites/tags?page=1&ordering=last_updated)![Docker Pulls](https://img.shields.io/docker/pulls/rjdbcm/aspidites)
```
$ docker pull ghcr.io/rjdbcm/aspidites:latest
```
-----------
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/rjdbcm/Aspidites?label=Github&logo=github&logoColor=black)![GitHub commits since tagged version (branch)](https://img.shields.io/github/commits-since/rjdbcm/Aspidites/latest/main)
```
$ gh repo clone rjdbcm/Aspidites
```

### 跑步
这很简单，只需使用：
```shell
$ aspidites -h
```

或者使用码头工人：
```shell
$ docker run -v $PWD:/workdir rjdbcm/aspidites:latest -h
```

