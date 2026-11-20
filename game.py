"""三关闯关状态：两轮机会、随机换题、结算奖品。"""

from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import datetime

from questions import BANK, DISTROS, Question

PRIZES = {
    3: "Tux 贴纸 + Linux 明信片",
    2: "Tux 贴纸",
    1: "暂无奖励",
    0: "暂无奖励",
}


@dataclass
class Outcome:
    kind: str          # correct / retry / fail
    title: str
    detail: str
    answer: str = ""


class Session:
    def __init__(self, seed: int | None = None):
        self.rng = random.Random(seed)
        self.level = 0
        self.results: list[str | None] = [None, None, None]
        self.used: list[set[str]] = [set(), set(), set()]
        self.question: Question | None = None
        self.options: list[str] = []
        self.attempts = 0          # 本关已用机会：0 / 1（换题不会重置）
        self.feedback: Outcome | None = None
        self.finished_at: datetime | None = None
        self.state = "id"          # id / question / feedback / result

    # ---------- 开局 ----------

    def begin(self) -> None:
        self.level = 0
        self.results = [None, None, None]
        self.used = [set(), set(), set()]
        self.attempts = 0
        self.finished_at = None
        self._new_question()
        self.state = "question"

    # ---------- 题目 ----------

    def _new_question(self) -> None:
        pool = [q for q in BANK[self.level] if q.id not in self.used[self.level]]
        if not pool:
            pool = list(BANK[self.level])
        q = self.rng.choice(pool)
        self.used[self.level].add(q.id)
        self.question = q
        self.feedback = None
        if self.level == 2:
            wrong = [d for d in DISTROS if d != q.answer]
            opts = [q.answer] + self.rng.sample(wrong, 2)
        else:
            opts = list(q.options)
        self.rng.shuffle(opts)
        self.options = opts

    @property
    def letters(self) -> tuple[str, ...]:
        return tuple("ABC"[:len(self.options)])

    def answer(self, letter: str) -> Outcome | None:
        if self.state != "question" or self.question is None:
            return None
        letter = letter.upper()
        if letter not in self.letters:
            return None
        choice = self.options[self.letters.index(letter)]
        q = self.question
        if choice == q.answer:
            self.results[self.level] = "pass"
            self.feedback = Outcome("correct", "✓ 正确", q.explanation, q.answer)
            self.state = "feedback"
            return self.feedback
        if self.attempts == 0:
            self.attempts = 1
            self.feedback = Outcome("retry", "× 不对，再试一次", "还有 1 次机会，换一道题。")
            self.state = "feedback"
            return self.feedback
        self.results[self.level] = "fail"
        self.feedback = Outcome("fail", "× 本关失败", q.explanation, q.answer)
        self.state = "feedback"
        return self.feedback

    def next(self) -> str:
        """离开反馈页，返回下一个状态：question / result。"""
        if self.feedback and self.feedback.kind == "retry":
            self._new_question()
            self.state = "question"
            return "question"
        self.level += 1
        if self.level >= 3:
            self.finished_at = datetime.now()
            self.state = "result"
            return "result"
        self.attempts = 0
        self._new_question()
        self.state = "question"
        return "question"

    # ---------- 结算 ----------

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r == "pass")

    @property
    def prize(self) -> str:
        return PRIZES[self.passed]

    @property
    def finished_text(self) -> str:
        return (self.finished_at or datetime.now()).strftime("%Y-%m-%d %H:%M")

    def option_line(self, i: int) -> str:
        return self.options[i]
