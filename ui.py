"""终端界面：欢迎、学号、三关、反馈与拍照结算。"""

from __future__ import annotations

import re
import time

import assetslib
import gfx
from canvas import (
    AMBER, AMBER2, BG, BLUE, BLUE2, DIM, FAINT, GREEN, INK, PANEL, PANEL2,
    RED, TEAL, WHITE, Canvas, Frame, truncate, width,
)
from game import Session
from questions import LEVELS

MIN_W, MIN_H = 80, 24

LINUX_ART = (
    "██╗     ██╗███╗   ██╗██╗   ██╗██╗  ██╗",
    "██║     ██║████╗  ██║██║   ██║╚██╗██╔╝",
    "██║     ██║██╔██╗ ██║██║   ██║ ╚███╔╝ ",
    "██║     ██║██║╚██╗██║██║   ██║ ██╔██╗ ",
    "███████╗██║██║ ╚████║╚██████╔╝██╔╝ ██╗",
    "╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝",
)


def wrap_text(s: str, w: int) -> list[str]:
    if w <= 0:
        return [""]
    out: list[str] = []
    line = ""
    used = 0
    for ch in s:
        cw = width(ch)
        if used + cw > w:
            out.append(line)
            line = ""
            used = 0
        line += ch
        used += cw
    out.append(line)
    return out


def draw_stars(c: Canvas, w: int, h: int, now: float, strong: bool = False) -> None:
    for i in range(46):
        x = (i * 47 + int(now * (7 if i % 3 else 13))) % max(1, w)
        y = 2 + (i * 19 + i * i * 3) % max(1, h - 2)
        ch = "✦" if i % 7 == 0 else "·"
        color = (60, 96, 156) if not strong else (90, 140, 210)
        c.put(x, y, ch, color, BG)


class UI:
    def __init__(self, protocol: str = "half", hint: str = ""):
        self.protocol = protocol
        self.hint = hint

    # ---------- 图片 ----------

    def _image(self, c: Canvas, name: str, x: int, y: int, w: int, h: int,
               key: tuple, title: str) -> tuple[tuple | None, bytes | None, gfx.Img | None]:
        c.box(x - 1, y - 1, w + 2, h + 2, BLUE, title, BLUE2, BG)
        asset = assetslib.load(name)
        if asset is None:
            c.fill(x, y, w, h, " ", INK, PANEL2)
            c.center(y + h // 2, "素材缺失", RED, PANEL2, bold=True)
            return None, None, None
        if self.protocol == "half":
            small = assetslib.half(name, w, h)
            if small is None:
                return None, None, None
            for yy in range(small.h // 2):
                for xx in range(small.w):
                    i = (yy * 2 * small.w + xx) * 3
                    j = ((yy * 2 + 1) * small.w + xx) * 3
                    top = (small.buf[i], small.buf[i + 1], small.buf[i + 2])
                    bot = (small.buf[j], small.buf[j + 1], small.buf[j + 2])
                    c.put(x + xx, y + yy, "▀", top, bot)
            return None, None, None
        return (x, y, w, h), asset.png, asset.img

    # ---------- 公共 ----------

    def _header(self, c: Canvas, w: int, section: str, right: str = "",
                right_color=DIM) -> None:
        c.put(0, 0, " ZJUT LUG ", BG, BLUE, bold=True)
        c.put(12, 0, "Linux 新手村", INK, BG, bold=True)
        c.center(0, section, WHITE, BG, bold=True)
        if right:
            c.right(w - 1, 0, right, right_color, BG, bold=True)
        c.hline(0, 1, w, "─", FAINT, BG)

    def _footer(self, c: Canvas, w: int, h: int, left: str, right: str) -> None:
        c.hline(0, h - 1, w, "─", FAINT, BG)
        c.put(1, h - 1, left, FAINT, BG)
        c.right(w - 1, h - 1, right, FAINT, BG)

    def _progress(self, c: Canvas, x: int, y: int, session: Session) -> None:
        for i in range(3):
            if session.results[i] == "pass":
                ch, col = "●", GREEN
            elif session.results[i] == "fail":
                ch, col = "×", RED
            elif i == session.level:
                ch, col = "◆", BLUE2
            else:
                ch, col = "○", FAINT
            c.put(x + i * 4, y, ch, col, BG, bold=True)
            if i < 2:
                c.put(x + i * 4 + 2, y, "─", FAINT, BG)

    # ---------- 欢迎 ----------

    def _welcome(self, c: Canvas, w: int, h: int, now: float) -> Frame:
        c.fill(0, 0, w, h, " ", INK, BG)
        draw_stars(c, w, h, now, True)
        self._header(c, w, "开源 · 学习 · 分享 · 实践", "READY", AMBER)
        c.put(2, 2, "OPEN SOURCE / LINUX / ZJUT", FAINT, BG)

        tw, th = (22, 11) if w >= 96 else (18, 9)
        tx = w - tw - 3
        ty = max(4, (h - th) // 2 - 1)
        rect, png, img = self._image(c, "assets/tux.png", tx, ty, tw, th,
                                     ("tux", w, h), "TUX")

        x = 5
        y = max(4, (h - 10) // 2 - 2)
        for i, line in enumerate(LINUX_ART):
            c.put(x, y + i, line, BLUE2 if i < 3 else BLUE, BG, bold=True)
        c.put(x + 1, y + 7, "新 手 村", AMBER, BG, bold=True)
        c.put(x + 1, y + 9, "Linux 新手村 · 三关挑战", INK, BG)
        c.put(x + 1, y + 10, "每关 2 次机会 · 答对即可通过", DIM, BG)
        c.put(x + 1, y + 12, "按 Enter 开始", AMBER2 if int(now * 2) % 2 == 0 else AMBER,
              BG, bold=True)
        c.put(x + 16, y + 12, "· Ctrl-C 退出", FAINT, BG)

        c.put(2, h - 3, "活动：ZJUT LUG · Linux 新手村", DIM, BG)
        c.right(w - 2, h - 3, "开源 · 学习 · 分享 · 实践", FAINT, BG)
        if self.hint:
            c.put(1, h - 2, truncate(self.hint, w - 2), AMBER, BG)
        self._footer(c, w, h, "Enter 开始", "Ctrl-C 退出")
        key = ("welcome", w, h, self.protocol)
        return Frame(c.render(rect), png, rect, key, img)

    # ---------- 学号 ----------

    def _id(self, c: Canvas, w: int, h: int, text: str, error: str, now: float) -> Frame:
        c.fill(0, 0, w, h, " ", INK, BG)
        draw_stars(c, w, h, now, False)
        self._header(c, w, "输入学号", "STEP 1 / 4", DIM)
        cw = min(64, w - 10)
        cx = (w - cw) // 2
        cy = max(4, (h - 15) // 2)
        c.box(cx, cy, cw, 15, BLUE, "玩家信息", BLUE2, PANEL, fill_inner=True)
        c.put(cx + 3, cy + 2, "请把学号写在这里，结算时用于拍照核对。", DIM)
        c.put(cx + 3, cy + 4, "学号", FAINT, PANEL)
        shown = text or "__________"
        c.put(cx + 9, cy + 4, shown, WHITE, PANEL, bold=True)
        if int(now * 3) % 2 == 0:
            c.put(cx + 9 + width(shown), cy + 4, "█", AMBER, PANEL, bold=True)
        c.put(cx + 3, cy + 6, "8-15 位数字 · 不对接学校系统，仅作活动记录", FAINT)
        if error:
            c.put(cx + 3, cy + 8, error, RED, PANEL, bold=True)
        c.put(cx + 3, cy + 10, "Enter 确认", GREEN, PANEL, bold=True)
        c.put(cx + 16, cy + 10, "· Esc 返回", FAINT, PANEL)
        c.put(cx + 3, cy + 12, "输入的数字不会上传网络。", FAINT, PANEL)
        self._footer(c, w, h, "数字输入 · Backspace 删除", "Esc 返回 · Ctrl-C 退出")
        return Frame(c.render())

    # ---------- 关卡 ----------

    def _terminal(self, c: Canvas, command: str, x: int, y: int, w: int, h: int,
                  now: float) -> None:
        c.box(x, y, w, h, TEAL, "终端", TEAL, BG, fill_inner=True)
        c.put(x + 2, y + 2, "lug@booth", GREEN, BG, bold=True)
        c.put(x + 11, y + 2, ":~$", TEAL, BG, bold=True)
        c.put(x + 15, y + 2, command, AMBER2, BG, bold=True)
        if int(now * 3) % 2 == 0:
            c.put(x + 15 + width(command), y + 2, "█", AMBER, BG, bold=True)
        c.put(x + 2, y + h - 2, "Linux / shell", FAINT, BG)

    def _question(self, c: Canvas, session: Session, w: int, h: int,
                  now: float, feedback: bool) -> Frame:
        c.fill(0, 0, w, h, " ", INK, BG)
        q = session.question
        if q is None:
            return Frame(c.render())
        title, prompt, note = LEVELS[session.level]
        remaining = 2 - session.attempts
        self._header(c, w, f"第 {session.level + 1} / 3 关 · {title}",
                     f"机会 {remaining} / 2", GREEN if remaining > 1 else AMBER)
        self._progress(c, 2, 2, session)

        big = w >= 96
        if session.level == 0:
            iw, ih = (58, 16) if big else (46, 13)
            rect, png, img = self._image(c, q.image, 2, 4, iw, ih,
                                         ("q", q.id, w, h), "桌面画面")
            px = iw + 5
        elif session.level == 2:
            iw, ih = (22, 11) if big else (18, 9)
            rect, png, img = self._image(c, q.image, 2, 4, iw, ih,
                                         ("q", q.id, w, h), "发行版 Logo")
            px = iw + 5
        else:
            iw, ih = (58, 16) if big else (46, 13)
            m = re.search(r"`([^`]+)`", q.prompt)
            command = m.group(1) if m else q.prompt
            self._terminal(c, command, 2, 4, iw, ih, now)
            rect = png = img = None
            px = iw + 5

        pw = w - px - 2
        if session.level == 2:
            c.put(px, 4, "这是哪个发行版的 Logo？", INK, BG, bold=True)
        else:
            for i, line in enumerate(wrap_text(prompt, pw)):
                c.put(px, 4 + i, line, INK, BG, bold=(i == 0))
        c.put(px, 7, truncate(note, pw), FAINT, BG)
        if feedback and session.feedback:
            fb = session.feedback
            col = GREEN if fb.kind == "correct" else RED if fb.kind == "fail" else AMBER
            c.put(px, 9, fb.title, col, BG, bold=True)
            yy = 11
            for line in wrap_text(fb.detail, pw):
                c.put(px, yy, line, INK, BG)
                yy += 1
            if fb.kind == "fail":
                c.put(px, yy + 1, f"正确答案：{fb.answer}", AMBER, BG, bold=True)
                yy += 3
            c.put(px, yy + 1, "Enter 继续", GREEN, BG, bold=True)
            if fb.kind == "retry":
                c.put(px, yy + 3, "换一道题，机会还在。", DIM, BG)
        else:
            y = 9
            for i, opt in enumerate(session.options):
                letter = session.letters[i]
                c.put(px, y, f"[{letter}]", BLUE2, BG, bold=True)
                lines = wrap_text(opt, max(4, pw - 5))
                for j, line in enumerate(lines):
                    c.put(px + 5, y + j, line, INK, BG)
                y += len(lines) + 1
            c.put(px, min(h - 3, y + 1), "A/B/C 或 1/2/3 选择", FAINT, BG)

        self._footer(c, w, h,
                     "Enter 继续" if feedback else "A/B/C 选择 · 1/2/3 也可以",
                     "Esc 放弃 · Ctrl-C 退出")
        key = ("q", q.id, w, h, self.protocol)
        return Frame(c.render(rect), png, rect, key, img)

    # ---------- 结算 ----------

    def _result(self, c: Canvas, session: Session, w: int, h: int, now: float) -> Frame:
        c.fill(0, 0, w, h, " ", INK, BG)
        draw_stars(c, w, h, now, True)
        self._header(c, w, "★ 挑战完成 ★", "SESSION REPORT", AMBER)
        cw = w - 6
        ch = h - 5
        x, y = 3, 2
        c.box(x, y, cw, ch, AMBER, "ZJUT LUG · Linux 新手村", AMBER, PANEL, fill_inner=True)
        tw, th = (18, 9) if w >= 96 else (14, 7)
        tx = x + cw - tw - 2
        ty = y + 2
        rect, png, img = self._image(c, "assets/tux.png", tx, ty, tw, th,
                                     ("result", w, h, session.passed), "")

        c.put(x + 3, y + 2, "学号", FAINT, PANEL)
        c.put(x + 9, y + 2, session.player_id, WHITE, PANEL, bold=True)
        c.put(x + 3, y + 4, "三关结果", DIM, PANEL)
        labels = ("系统识别", "命令行猜词", "发行版盲盒")
        for i in range(3):
            yy = y + 5 + i
            ok = session.results[i] == "pass"
            mark = "✓ 通过" if ok else "✗ 失败"
            c.put(x + 3, yy, f"第 {i + 1} 关", FAINT, PANEL)
            c.put(x + 12, yy, labels[i], INK, PANEL)
            c.put(x + 25, yy, mark, GREEN if ok else RED, PANEL, bold=True)

        c.put(x + 3, y + 9, "通关", FAINT, PANEL)
        c.put(x + 8, y + 9, f"{session.passed} / 3", AMBER2, PANEL, bold=True)
        c.put(x + 3, y + 10, "可领取", FAINT, PANEL)
        c.put(x + 10, y + 10, session.prize, WHITE, PANEL, bold=True)
        c.put(x + 3, y + 12, "完成时间", FAINT, PANEL)
        c.put(x + 12, y + 12, session.finished_text, INK, PANEL)

        msg = "请用手机拍下此页面，向工作人员展示后领取奖品"
        yy = y + ch - 4
        for i, line in enumerate(wrap_text(msg, cw - 6)):
            c.put(x + 3, yy + i, line, AMBER, PANEL, bold=True)
        c.put(x + 3, y + ch - 2, "N 下一位 · Q 退出", DIM, PANEL)
        self._footer(c, w, h, "拍照凭证 · 请保持此页面", "N 下一位 · Q 退出")
        key = ("result", w, h, session.passed)
        return Frame(c.render(rect), png, rect, key, img)

    # ---------- 太小 ----------

    def _too_small(self, c: Canvas, w: int, h: int) -> Frame:
        c.fill(0, 0, w, h, " ", INK, BG)
        c.center(max(0, h // 2 - 2), "终端太小了", AMBER, BG, bold=True)
        c.center(max(0, h // 2), f"至少需要 {MIN_W} x {MIN_H}", DIM, BG)
        c.center(max(0, h // 2 + 1), f"当前 {w} x {h}", FAINT, BG)
        c.center(max(0, h // 2 + 3), "放大窗口后自动继续", FAINT, BG)
        return Frame(c.render())

    # ---------- 入口 ----------

    def render(self, screen: str, session: Session, id_text: str = "",
               id_error: str = "", now: float | None = None,
               w: int = 100, h: int = 30) -> Frame:
        now = time.monotonic() if now is None else now
        c = Canvas(w, h)
        if w < MIN_W or h < MIN_H:
            return self._too_small(c, w, h)
        if screen == "welcome":
            return self._welcome(c, w, h, now)
        if screen == "id":
            return self._id(c, w, h, id_text, id_error, now)
        if screen in ("question", "feedback"):
            return self._question(c, session, w, h, now, screen == "feedback")
        return self._result(c, session, w, h, now)
