# ZJUT LUG · Linux 新手村

给线下摊位用的 **终端互动闯关**。不收集身份信息、不联网、不写数据库；玩家直接连过三关，最后在终端里得到一张适合手机拍照的成绩单。

- 第一关：操作系统桌面画面的 **Linux / Windows** 二选一
- 第二关：模拟终端里的 **命令猜词** 三选一
- 第三关：**发行版 Logo 盲盒** 三选一
- 每关最多 2 次机会，第一次答错会换一道题，第二次答错才公布答案
- 三关结束显示通过情况、奖品和完成时间，直接手机拍照领奖

没有 Flask、没有二维码、没有局域网核销、没有管理员后台、没有数据库、没有联网。所有素材和逻辑都在本地。

## 运行

需要 [uv](https://docs.astral.sh/uv/)，Pillow 会在 `uv sync` 时自动装好。活动前联网执行一次，现场就可以完全离线运行：

```bash
cd lug-newbie
mise exec -- uv sync
./lug
```

或者：

```bash
mise exec -- uv run python main.py
```

终端至少 **80 x 24**；推荐 100x30 全屏。窗口放大后会自动重排。

## 玩法

1. 欢迎页按 `Enter`（或任意键）直接开始。
2. 三关按顺序进行：
   - 第一关：看桌面画面，按 `A` 或 `B`（也可以按 `1`/`2`）选 Linux / Windows。
   - 第二关：看终端里的命令，按 `A/B/C` 选择它做什么。
   - 第三关：看发行版 Logo，按 `A/B/C` 选择发行版。
3. 答对：本关通过；第一次答错：不公布答案，换一道题；第二次答错：本关失败，公布正确答案和一句解释。
4. 三关结束进入成绩单，用手机拍下页面即可领奖。
5. `N` 下一位，`Q` 退出。

| 键 | 作用 |
| --- | --- |
| `Enter` | 开始 / 继续 / 下一位 |
| `A/B/C` | 选择答案 |
| `1/2/3` | 等同 `A/B/C` |
| `Esc` | 返回 / 放弃本局 |
| `N` | 成绩单：下一位 |
| `Q` / `Ctrl-C` | 退出 |

## 奖品

| 通关数 | 可领取 |
| --- | --- |
| 0～1 | 暂无奖励 |
| 2 | Tux 贴纸 |
| 3 | Tux 贴纸 + Linux 明信片 |

成绩单会完整显示三关通过/失败、总通关数、可领奖品和完成时间，并明确写：

> 请用手机拍下此页面，向工作人员展示后领取奖品

**不显示任何身份信息，也不需要输入。**

## 终端图片

自动检测图片协议：

- Kitty / Ghostty：Kitty 图形协议
- WezTerm：iTerm2 内联图片（`OSC 1337`）
- Tabby：Sixel（Tabby 会吞掉 `OSC 1337`，所以走 DCS）
- 其他 / ConPTY：真彩半块字符 `▀` 兜底

如果看到的是半块字符，说明当前链路不支持图片（最常见的是 Windows 本地 shell 里再 `ssh`，中间隔着 ConPTY）。绕过方式：

- WezTerm：`wezterm ssh 用户@主机`
- Tabby：用「设置 → 连接」里的 SSH 配置

## 素材说明

`assets/` 里的桌面画面、发行版 Logo 和 Tux 都是**本地生成的风格化插画**，不是真实系统截图。这样项目可以完全离线、无版权素材依赖，桌面 UI 线索也足够区分 Linux / Windows。

## 项目结构

```text
lug             启动脚本
main.py         状态机、按键、主循环
ui.py           欢迎 / 三关 / 反馈 / 成绩单
game.py         两轮机会、随机换题、奖品结算
questions.py    三关题库与图片路径
assetslib.py    PNG / RGB / 半块降采样
assets/         本地插画素材
canvas.py       真彩画布，图片区域跳过
term.py         图片协议、终端输入
gfx.py          RGB 缓冲与 PNG
sixel.py        Sixel 编码器
tools/          素材与调色板生成脚本
```

## 测试

```bash
mise exec -- uv run python -m py_compile main.py ui.py game.py questions.py assetslib.py canvas.py term.py
```

已验证：

- 三关全对 → 3/3，显示 Tux 贴纸 + Linux 明信片
- 两关通过 → 2/3，只显示 Tux 贴纸
- 0/1 关 → 暂无奖励
- 第一次答错换题，第二次答错才失败
- 欢迎页直接开始
- 80x24 / 100x30 布局
- WezTerm / Tabby / 半块三种图片链路
- `N` 下一位清空当前局
