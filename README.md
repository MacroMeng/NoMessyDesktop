<a href="https://github.com/MacroMeng/NoMessyDesktop"> <img align="left" alt="logo" height="72" src="https://forum.smart-teach.cn/assets/files/2025-10-02/1759392449-319899-logo.png" width="72"/> </a>
<h1 align="left">NoMessyDesktop</h1>

> NoMessyDesktop 是一款当老师试图在桌面新建文件时弹出弹窗的软件。您可以配置许多选项，比如在弹窗里让老师选择对应文件夹存放\*、让 NoMessyDesktop 自动根据配置的规则存放文件\*等。

![](https://forum.smart-teach.cn/assets/files/2025-10-02/1759392456-113780-poster.png)

本项目使用了 Python 作为基础语言，搭配`watchdog`模块实现文件监听。后续，我们准备使用 PySide 6 并使用 Fluent Design 设计语言重构本项目。

> [!WARNING]
> 现在项目还处于早期阶段，请不要在生产环境中使用本项目。

> [!TIP]
> 本项目会分为多个阶段：Pre-Alpha 是开始开发时的阶段，此时不会发布 Release。Alpha 是一个版本发布早期的阶段。Beta 是版本发布中期，新功能已经完成，修补 Bug 的阶段。RC 是发布预选阶段，此时不会实现新功能。

> [!TIP]
> 本项目版本号采取四段式架构。第一段是大版本发布，通常包括主要功能的更新。第二段是中版本更新，通常包括重要的 Bug 修复和小功能的实现。第三段是小版本更新，通常不会包括新功能。第四段是细节更新，不会发布在 Release 中，通常来说，修复一些相似的 Bug 即可算作一次细节更新（可以参照 ICC-CE 的更新频率，它会比 ICC-CE 稍慢些。）

## 官方社区
欢迎您加入我们的社区：QQ 群`1034964927`，或者在[智教联盟论坛](https://forum.smart-teach.cn)上讨论。

## 从源代码运行
1. 安装 Python。你可以在 [Python 官网](https://www.python.org/downloads/)下载安装。
2. 进入 venv。打开命令行，切换换到项目目录，并运行`./venv/Scripts/activate.bat`(Windows) 来进入 venv。
3. 使用`python ./main.py`启动 NoMessyDesktop。

## 许可证 <img alt="GPLv3-Logo" align="right" src="https://gnu.ac.cn/graphics/gplv3-with-text-136x68.png/">
本项目使用 GPL v3 许可证。这代表了您可以自由查看、编辑、使用、再分发本项目的源代码，但是所有改编版本（即使您只是摘录）也必须使用相同的 GPL v3 许可证。

> [!WARNING]
> 请不要认为 NoMessyDesktop 有缩写 NMD，否则若别人误解您的意思并对您造成伤害，NoMessyDesktop 的作者不会承担任何责任。
