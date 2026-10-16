"""Минимальная библиотека отрисовки диаграмм BPMN 2.0 средствами matplotlib."""
import math
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle, Ellipse

plt.rcParams["font.family"] = "Arial"

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "img")
UNIT = 0.08  # дюймов на единицу координат
FS = 9

TASK_FC, TASK_EC = "#eef4fb", "#2f5d8a"
START_FC, START_EC = "#e8f5e9", "#2e7d32"
END_FC, END_EC = "#fdecea", "#c62828"
INT_FC, INT_EC = "#fff8e1", "#b26a00"
GW_FC, GW_EC = "#fffde7", "#8d7b00"
POOL_EC = "#555555"


class Node:
    """Элемент с точками привязки: l, r, t, b (лево, право, верх, низ)."""

    def __init__(self, x, y, hw, hh):
        self.x, self.y, self.hw, self.hh = x, y, hw, hh

    @property
    def l(self):
        return (self.x - self.hw, self.y)

    @property
    def r(self):
        return (self.x + self.hw, self.y)

    @property
    def t(self):
        return (self.x, self.y + self.hh)

    @property
    def b(self):
        return (self.x, self.y - self.hh)

    @property
    def c(self):
        return (self.x, self.y)

    def at(self, dx=0.0, side="t"):
        """Точка на верхней/нижней стороне со смещением dx от центра."""
        return (self.x + dx, self.y + (self.hh if side == "t" else -self.hh))

    def side(self, side, dy=0.0):
        """Точка на левой/правой стороне со смещением dy."""
        return (self.x + (self.hw if side == "r" else -self.hw), self.y + dy)


class Diagram:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.fig = plt.figure(figsize=(w * UNIT, h * UNIT), dpi=200)
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(0, w)
        self.ax.set_ylim(0, h)
        self.ax.set_aspect("equal")
        self.ax.axis("off")
        self.lanes = {}

    # ------------------------------------------------------------ пулы
    def pool(self, x, y_top, w, name, lanes, head=5.5):
        """Пул с дорожками. lanes = [(имя, высота), ...]. Возвращает центры дорожек по y."""
        total = sum(hh for _, hh in lanes)
        y0 = y_top - total
        self.ax.add_patch(Rectangle((x, y0), w, total, fill=False, ec=POOL_EC, lw=1.3, zorder=1))
        self.ax.plot([x + head, x + head], [y0, y_top], color=POOL_EC, lw=1.3, zorder=1)
        self.ax.text(x + head / 2, y0 + total / 2, name, rotation=90, ha="center", va="center",
                     fontsize=FS + 1.5, weight="bold", zorder=1)
        y = y_top
        for lname, hh in lanes:
            if len(lanes) > 1:
                self.ax.plot([x + head, x + head * 2], [y, y], color=POOL_EC, lw=1.0, zorder=1)
                self.ax.plot([x + head * 2, x + head * 2], [y, y - hh], color=POOL_EC, lw=1.0, zorder=1)
                self.ax.plot([x + head, x + w], [y - hh, y - hh], color=POOL_EC, lw=1.0, zorder=1)
                self.ax.text(x + head * 1.5, y - hh / 2, lname, rotation=90, ha="center",
                             va="center", fontsize=FS, zorder=1)
            self.lanes[lname] = (y - hh, y, y - hh / 2)
            y -= hh
        return {n: c for n, (_, _, c) in self.lanes.items()}

    def blackbox(self, x, y, w, h, name):
        """Свёрнутый пул (участник «чёрный ящик»)."""
        self.ax.add_patch(Rectangle((x, y), w, h, fill=True, fc="#fafafa", ec=POOL_EC, lw=1.3, zorder=1))
        self.ax.text(x + w / 2, y + h / 2, name, ha="center", va="center", fontsize=FS + 1.5,
                     weight="bold", zorder=1)
        return Node(x + w / 2, y + h / 2, w / 2, h / 2)

    # ------------------------------------------------------------ действия
    def task(self, x, y, text, w=17, h=10, sub=False, fs=FS):
        self.ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                         boxstyle="round,pad=0,rounding_size=1.6",
                                         fc=TASK_FC, ec=TASK_EC, lw=1.3, zorder=4))
        self.ax.text(x, y + (0.8 if sub else 0), text, ha="center", va="center", fontsize=fs,
                     zorder=5, linespacing=1.1)
        if sub:
            s = 2.2
            self.ax.add_patch(Rectangle((x - s / 2, y - h / 2 + 0.4), s, s, fill=False,
                                        ec=TASK_EC, lw=1.0, zorder=5))
            self.ax.plot([x - 0.7, x + 0.7], [y - h / 2 + 0.4 + s / 2] * 2, color=TASK_EC, lw=1.0, zorder=5)
            self.ax.plot([x, x], [y - h / 2 + 0.4 + 0.4, y - h / 2 + 0.4 + s - 0.4], color=TASK_EC,
                         lw=1.0, zorder=5)
        return Node(x, y, w / 2, h / 2)

    # ------------------------------------------------------------ события
    def event(self, x, y, kind="start", trigger=None, label=None, lpos="b", r=2.4, fs=FS - 0.5):
        fc, ec, lw = {"start": (START_FC, START_EC, 1.3), "end": (END_FC, END_EC, 3.0),
                      "inter": (INT_FC, INT_EC, 1.2)}[kind]
        self.ax.add_patch(Circle((x, y), r, fc=fc, ec=ec, lw=lw, zorder=4))
        if kind == "inter":
            self.ax.add_patch(Circle((x, y), r - 0.5, fill=False, ec=ec, lw=1.0, zorder=5))
        if trigger in ("message", "message_throw"):
            self._envelope(x, y, filled=trigger == "message_throw" or kind == "end")
        elif trigger == "timer":
            self.ax.add_patch(Circle((x, y), r * 0.62, fc="white", ec="k", lw=0.9, zorder=5))
            for a in range(0, 360, 30):
                ra = math.radians(a)
                self.ax.plot([x + r * 0.5 * math.cos(ra), x + r * 0.62 * math.cos(ra)],
                             [y + r * 0.5 * math.sin(ra), y + r * 0.62 * math.sin(ra)],
                             color="k", lw=0.5, zorder=6)
            self.ax.plot([x, x + 0.25], [y, y + r * 0.45], color="k", lw=0.9, zorder=6)
            self.ax.plot([x, x + r * 0.35], [y, y - 0.1], color="k", lw=0.9, zorder=6)
        elif trigger in ("link", "link_throw"):
            a = r * 0.45
            pts = [(x - a, y - a * 0.4), (x + a * 0.1, y - a * 0.4), (x + a * 0.1, y - a * 0.85),
                   (x + a, y), (x + a * 0.1, y + a * 0.85), (x + a * 0.1, y + a * 0.4), (x - a, y + a * 0.4)]
            self.ax.add_patch(Polygon(pts, closed=True, fc="#222222" if trigger == "link_throw" else "white",
                                      ec="#222222", lw=0.8, zorder=6))
        if label:
            self._label(x, y, r, label, lpos, fs)
        return Node(x, y, r, r)

    def _envelope(self, x, y, filled):
        w, h = 2.3, 1.5
        fc, lc = ("#222222", "white") if filled else ("white", "#222222")
        self.ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fc=fc, ec="#222222", lw=0.8, zorder=6))
        self.ax.plot([x - w / 2, x, x + w / 2], [y + h / 2, y - 0.05, y + h / 2], color=lc, lw=0.8, zorder=7)

    def _label(self, x, y, r, text, lpos, fs):
        if lpos == "b":
            self.ax.text(x, y - r - 0.6, text, ha="center", va="top", fontsize=fs, zorder=6, linespacing=1.05)
        elif lpos == "t":
            self.ax.text(x, y + r + 0.6, text, ha="center", va="bottom", fontsize=fs, zorder=6, linespacing=1.05)
        elif lpos == "r":
            self.ax.text(x + r + 0.8, y, text, ha="left", va="center", fontsize=fs, zorder=6, linespacing=1.05)
        elif lpos == "l":
            self.ax.text(x - r - 0.8, y, text, ha="right", va="center", fontsize=fs, zorder=6, linespacing=1.05)

    # ------------------------------------------------------------ шлюзы
    def gateway(self, x, y, kind="x", label=None, lpos="t", s=3.2, fs=FS - 0.5):
        self.ax.add_patch(Polygon([(x - s, y), (x, y + s), (x + s, y), (x, y - s)], closed=True,
                                  fc=GW_FC, ec=GW_EC, lw=1.3, zorder=4))
        k = s * 0.38
        if kind == "x":
            self.ax.plot([x - k, x + k], [y - k, y + k], color="k", lw=1.8, zorder=5)
            self.ax.plot([x - k, x + k], [y + k, y - k], color="k", lw=1.8, zorder=5)
        elif kind == "+":
            self.ax.plot([x - k * 1.3, x + k * 1.3], [y, y], color="k", lw=2.0, zorder=5)
            self.ax.plot([x, x], [y - k * 1.3, y + k * 1.3], color="k", lw=2.0, zorder=5)
        elif kind == "o":
            self.ax.add_patch(Circle((x, y), k * 1.25, fill=False, ec="k", lw=1.6, zorder=5))
        elif kind == "event":
            self.ax.add_patch(Circle((x, y), s * 0.55, fill=False, ec="k", lw=0.9, zorder=5))
            self.ax.add_patch(Circle((x, y), s * 0.45, fill=False, ec="k", lw=0.9, zorder=5))
            pr = s * 0.28
            pts = [(x + pr * math.cos(math.radians(90 + 72 * i)), y + pr * math.sin(math.radians(90 + 72 * i)))
                   for i in range(5)]
            self.ax.add_patch(Polygon(pts, closed=True, fill=False, ec="k", lw=0.9, zorder=5))
        if label:
            self._label(x, y, s, label, lpos, fs)
        return Node(x, y, s, s)

    # ------------------------------------------------------------ данные и артефакты
    def data(self, x, y, label=None, w=4.2, h=5.4, lpos="b", fs=FS - 1):
        f = 1.3
        pts = [(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2 - f),
               (x + w / 2 - f, y + h / 2), (x - w / 2, y + h / 2)]
        self.ax.add_patch(Polygon(pts, closed=True, fc="white", ec="#333333", lw=1.0, zorder=4))
        self.ax.plot([x + w / 2 - f, x + w / 2 - f, x + w / 2], [y + h / 2, y + h / 2 - f, y + h / 2 - f],
                     color="#333333", lw=0.8, zorder=5)
        if label:
            self._label(x, y, h / 2, label, lpos, fs)
        return Node(x, y, w / 2, h / 2)

    def store(self, x, y, label=None, w=7, h=6, lpos="b", fs=FS - 1):
        e = 1.6
        self.ax.add_patch(Rectangle((x - w / 2, y - h / 2 + e / 2), w, h - e, fc="white", ec="none", zorder=4))
        self.ax.plot([x - w / 2, x - w / 2], [y - h / 2 + e / 2, y + h / 2 - e / 2], color="#333333", lw=1.0, zorder=5)
        self.ax.plot([x + w / 2, x + w / 2], [y - h / 2 + e / 2, y + h / 2 - e / 2], color="#333333", lw=1.0, zorder=5)
        self.ax.add_patch(Ellipse((x, y - h / 2 + e / 2), w, e, fc="white", ec="#333333", lw=1.0, zorder=3))
        self.ax.add_patch(Ellipse((x, y + h / 2 - e / 2), w, e, fc="white", ec="#333333", lw=1.0, zorder=5))
        if label:
            self._label(x, y, h / 2, label, lpos, fs)
        return Node(x, y, w / 2, h / 2)

    def group(self, x0, y0, x1, y1, title, fs=FS - 0.5):
        """Группа (артефакт BPMN): пунктирная рамка со скруглёнными углами и заголовком."""
        self.ax.add_patch(FancyBboxPatch((x0, y0), x1 - x0, y1 - y0,
                                         boxstyle="round,pad=0,rounding_size=2.0", fill=False,
                                         ec="#7a7a7a", lw=1.0, ls=(0, (6, 2, 1, 2)), zorder=1))
        self.ax.text(x0 + 1.5, y1 - 1.2, title, ha="left", va="top", fontsize=fs, color="#555555",
                     weight="bold", zorder=1)

    def note(self, x, y, text, h=8, fs=FS - 1):
        """Текстовая аннотация: открытая скобка слева."""
        self.ax.plot([x + 2, x, x, x + 2], [y + h / 2, y + h / 2, y - h / 2, y - h / 2], color="#333333", lw=0.9, zorder=4)
        self.ax.text(x + 1, y, text, ha="left", va="center", fontsize=fs, zorder=4, linespacing=1.1)
        return Node(x, y, 0, h / 2)

    # ------------------------------------------------------------ связи
    def flow(self, *pts, label=None, lxy=None, ha="left", va="bottom", fs=FS - 0.5):
        """Поток управления (сплошная линия, закрашенная стрелка)."""
        xs, ys = zip(*pts)
        self.ax.plot(xs, ys, color="#222222", lw=1.0, zorder=3, solid_joinstyle="miter")
        self.ax.annotate("", xy=pts[-1], xytext=pts[-2], zorder=3,
                         arrowprops=dict(arrowstyle="-|>", color="#222222", lw=1.0, mutation_scale=9,
                                         shrinkA=0, shrinkB=0))
        if label:
            lx, ly = lxy if lxy else (pts[0][0] + 0.8, pts[0][1] + 0.5)
            self.ax.text(lx, ly, label, ha=ha, va=va, fontsize=fs, zorder=6, style="italic")

    def msg(self, *pts, label=None, lxy=None, ha="left", va="center", fs=FS - 1):
        """Поток сообщений (пунктир, кружок в начале, полая стрелка)."""
        xs, ys = zip(*pts)
        self.ax.plot(xs, ys, color="#444444", lw=0.9, ls=(0, (4, 2.5)), zorder=2)
        self.ax.add_patch(Circle(pts[0], 0.55, fc="white", ec="#444444", lw=0.9, zorder=3))
        self.ax.annotate("", xy=pts[-1], xytext=pts[-2], zorder=3,
                         arrowprops=dict(arrowstyle="-|>", fc="white", ec="#444444", lw=0.9,
                                         mutation_scale=10, shrinkA=0, shrinkB=0))
        if label:
            lx, ly = lxy if lxy else (pts[0][0] + 0.8, (pts[0][1] + pts[-1][1]) / 2)
            self.ax.text(lx, ly, label, ha=ha, va=va, fontsize=fs, zorder=6,
                         bbox=dict(fc="white", ec="none", pad=0.2))

    def assoc(self, *pts, arrow=True):
        """Ассоциация данных (точечная линия)."""
        xs, ys = zip(*pts)
        self.ax.plot(xs, ys, color="#555555", lw=0.9, ls=(0, (1, 1.6)), zorder=2)
        if arrow:
            self.ax.annotate("", xy=pts[-1], xytext=pts[-2], zorder=3,
                             arrowprops=dict(arrowstyle="->", color="#555555", lw=0.9,
                                             mutation_scale=8, shrinkA=0, shrinkB=0))

    def text(self, x, y, s, **kw):
        kw.setdefault("fontsize", FS - 0.5)
        kw.setdefault("zorder", 6)
        self.ax.text(x, y, s, **kw)

    def crop(self, y0, y1):
        """Оставить только полосу координат y0..y1."""
        self.ax.set_ylim(y0, y1)
        self.fig.set_size_inches(self.w * UNIT, (y1 - y0) * UNIT)

    def save(self, name):
        os.makedirs(OUT_DIR, exist_ok=True)
        self.fig.savefig(os.path.join(OUT_DIR, name), dpi=200, facecolor="white",
                         bbox_inches="tight", pad_inches=0.04)
        plt.close(self.fig)
