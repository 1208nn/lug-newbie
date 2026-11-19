#!/usr/bin/env python3
"""ZJUT LUG · Linux 新手村 —— 终端互动闯关。"""

from __future__ import annotations

import argparse
import random
import sys
import time

from game import Session
from term import Terminal
from ui import UI


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="lug-newbie", description="ZJUT LUG · Linux 新手村")
    ap.add_argument("--seed", type=int, default=None, help="固定随机种子（调试用）")
    args = ap.parse_args(argv or sys.argv[1:])

    seed = args.seed if args.seed is not None else random.randrange(1_000_000)
    session = Session(seed)
    try:
        term = Terminal()
    except Exception as e:
        print(f"启动失败：{e}", file=sys.stderr)
        return 1

    screen = "welcome"
    id_text = ""
    id_error = ""
    placed_key = None
    last_size = None
    idle = 0.0
    last = time.monotonic()
    running = True

    def go(new_screen: str) -> None:
        nonlocal screen, placed_key, idle
        screen = new_screen
        placed_key = None
        idle = 0.0
        term.clear_image()
        term.clear()

    def to_welcome() -> None:
        nonlocal screen, placed_key, idle, id_text, id_error
        screen = "welcome"
        id_text = ""
        id_error = ""
        placed_key = None
        idle = 0.0
        term.clear_image()
        term.clear()

    with term:
        ui = UI(term.protocol, term.hint)
        while running:
            frame_start = time.monotonic()
            now = frame_start
            dt = min(0.25, frame_start - last)
            last = frame_start
            idle += dt
            w, h = term.size()
            if (w, h) != last_size:
                last_size = (w, h)
                placed_key = None
                term.clear_image()
                term.clear()

            key = term.read_key(0.03)
            if key is not None:
                idle = 0.0

            if key == "ctrl-c":
                running = False

            elif w < 80 or h < 24:
                # 太小：只等放大或退出
                pass

            elif screen == "welcome":
                if key in ("enter", "space"):
                    screen = "id"
                    placed_key = None
                    term.clear_image()
                    term.clear()
                elif key == "esc":
                    pass
                elif key is not None and len(key) == 1:
                    screen = "id"
                    placed_key = None
                    term.clear_image()
                    term.clear()

            elif screen == "id":
                if key == "esc":
                    to_welcome()
                elif key == "backspace":
                    id_text = id_text[:-1]
                    id_error = ""
                elif key == "enter":
                    if session.begin(id_text):
                        go("question")
                    else:
                        id_error = "学号需要是 8-15 位数字。"
                elif key is not None and len(key) == 1 and key.isdigit():
                    if len(id_text) < 15:
                        id_text += key
                        id_error = ""

            elif screen == "question":
                if key == "esc":
                    to_welcome()
                elif key is not None and len(key) == 1:
                    ch = key.upper()
                    if ch in ("1", "2", "3"):
                        ch = "ABC"[int(ch) - 1]
                    if ch in session.letters:
                        if session.answer(ch):
                            screen = "feedback"

            elif screen == "feedback":
                if key in ("enter", "space"):
                    nxt = session.next()
                    go(nxt)
                elif key == "esc":
                    to_welcome()

            elif screen == "result":
                if key in ("n", "N", "enter", "space"):
                    session = Session(random.randrange(1_000_000))
                    id_text = ""
                    id_error = ""
                    go("id")
                elif key in ("q", "Q", "esc"):
                    running = False

            # 空闲保护
            if screen == "id" and idle > 90:
                to_welcome()
            elif screen == "result" and idle > 120:
                session = Session(random.randrange(1_000_000))
                id_text = ""
                id_error = ""
                go("id")

            frame = ui.render(screen, session, id_text, id_error, now, w, h)
            term.write(frame.text)
            if frame.png is not None and frame.rect is not None:
                if frame.art_key != placed_key:
                    term.clear_image()
                    term.place_image(frame.img, frame.png, *frame.rect)
                    placed_key = frame.art_key
            elif placed_key is not None:
                term.clear_image()
                placed_key = None

            spent = time.monotonic() - frame_start
            if spent < 1 / 20:
                time.sleep(1 / 20 - spent)

    print("新手村收摊了。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
