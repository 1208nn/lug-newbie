"""三关题库。素材与文案都可以直接改这里。"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Question:
    id: str
    prompt: str
    image: str | None
    answer: str
    options: tuple[str, ...]
    explanation: str


LEVELS = (
    ("系统识别", "这是 Linux，还是 Windows？", "桌面环境是线索，不要只看壁纸。"),
    ("命令行猜词", "这条命令是做什么的？", "只是选择题，不会真的执行命令。"),
    ("发行版盲盒", "这个 Logo 属于哪个发行版？", "看形状和配色，不用背介绍。"),
)

LEVEL1: list[Question] = [
    Question("OS-01", "这是 Linux，还是 Windows？", "assets/os_win11.png",
             "Windows", ("Linux", "Windows"),
             "Windows 11：底部居中任务栏、圆角窗口、居中的 Start 按钮。"),
    Question("OS-02", "这是 Linux，还是 Windows？", "assets/os_win10.png",
             "Windows", ("Linux", "Windows"),
             "Windows 10：左下角 Start、全宽任务栏、方角窗口。"),
    Question("OS-03", "这是 Linux，还是 Windows？", "assets/os_ubuntu.png",
             "Linux", ("Linux", "Windows"),
             "Ubuntu GNOME：顶部 Activities 栏、左侧 Dock、橙色主题。"),
    Question("OS-04", "这是 Linux，还是 Windows？", "assets/os_kde.png",
             "Linux", ("Linux", "Windows"),
             "KDE Plasma：底部面板、Dolphin 文件管理器、Breeze 风格。"),
    Question("OS-05", "这是 Linux，还是 Windows？", "assets/os_mint.png",
             "Linux", ("Linux", "Windows"),
             "Linux Mint Cinnamon：绿色主题、底部 Menu、Nemo 文件管理器。"),
    Question("OS-06", "这是 Linux，还是 Windows？", "assets/os_fedora.png",
             "Linux", ("Linux", "Windows"),
             "Fedora GNOME：顶部 Activities 栏、左侧 Dock、蓝色主题。"),
]

LEVEL2: list[Question] = [
    Question("CMD-01", "`ls` 是做什么的？", None,
             "查看目录内容", ("查看目录内容", "创建目录", "关闭电脑"),
             "ls 列出当前目录的文件和子目录。"),
    Question("CMD-02", "`cd` 是做什么的？", None,
             "切换目录", ("切换目录", "删除文件", "复制文件"),
             "cd 改变当前工作目录，cd .. 回上一级。"),
    Question("CMD-03", "`mkdir hello` 是做什么的？", None,
             "创建名为 hello 的目录", ("创建名为 hello 的目录", "删除 hello 目录", "打开浏览器"),
             "mkdir 创建目录，hello 是新目录的名字。"),
    Question("CMD-04", "`pwd` 是做什么的？", None,
             "显示当前工作目录路径", ("显示当前工作目录路径", "修改密码", "下载文件"),
             "pwd = print working directory，打印当前路径。"),
    Question("CMD-05", "`cp a.txt b.txt` 是做什么的？", None,
             "把 a.txt 复制为 b.txt", ("把 a.txt 复制为 b.txt", "删除 a.txt", "修改系统时间"),
             "cp 复制文件，第一个参数是源，第二个是目标。"),
    Question("CMD-06", "`rm a.txt` 是做什么的？", None,
             "删除指定文件", ("删除指定文件", "创建文件", "查看文件内容"),
             "rm 删除文件；终端里它不会进回收站，要小心。"),
]

LEVEL3: list[Question] = [
    Question("DISTRO-01", "这个 Logo 属于哪个发行版？", "assets/logo_ubuntu.png",
             "Ubuntu", ("Ubuntu", "Debian", "Fedora"),
             "Ubuntu：橙色圆环和三个白点，基于 Debian。"),
    Question("DISTRO-02", "这个 Logo 属于哪个发行版？", "assets/logo_debian.png",
             "Debian", ("Debian", "Arch Linux", "Linux Mint"),
             "Debian：红色螺旋，稳定、自由，很多发行版的母体。"),
    Question("DISTRO-03", "这个 Logo 属于哪个发行版？", "assets/logo_arch.png",
             "Arch Linux", ("Arch Linux", "openSUSE", "Ubuntu"),
             "Arch Linux：蓝色三角，滚动更新，文档是 Arch Wiki。"),
    Question("DISTRO-04", "这个 Logo 属于哪个发行版？", "assets/logo_fedora.png",
             "Fedora", ("Fedora", "Debian", "Linux Mint"),
             "Fedora：蓝色圆和 f，上游技术尝鲜，默认 GNOME。"),
    Question("DISTRO-05", "这个 Logo 属于哪个发行版？", "assets/logo_mint.png",
             "Linux Mint", ("Linux Mint", "Arch Linux", "Fedora"),
             "Linux Mint：绿色叶子，基于 Ubuntu，Cinnamon 桌面很常见。"),
    Question("DISTRO-06", "这个 Logo 属于哪个发行版？", "assets/logo_suse.png",
             "openSUSE", ("openSUSE", "Ubuntu", "Debian"),
             "openSUSE：绿色变色龙，YaST 和 Snapper 很有名。"),
]

BANK = (LEVEL1, LEVEL2, LEVEL3)

# 给第三关的干扰项用：所有发行版名
DISTROS = ("Ubuntu", "Debian", "Arch Linux", "Fedora", "Linux Mint", "openSUSE")
