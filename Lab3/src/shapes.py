"""Отрисовка диаграмм EPC (eEPC) и DFD (нотация Гейна–Сарсона) средствами matplotlib."""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Polygon, Rectangle

plt.rcParams["font.family"] = "Arial"

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "img")
UNIT = 0.08  # дюймов на единицу координат
FS = 9.5


class Node:
    """Элемент с точками привязки: l, r, t, b."""

    def __init__(self, x, y, hw, hh):
        self.x, self.y, self.hw, self.hh = x, y, hw, hh

    l = property(lambda s: (s.x - s.hw, s.y))
    r = property(lambda s: (s.x + s.hw, s.y))
    t = property(lambda s: (s.x, s.y + s.hh))
    b = property(lambda s: (s.x, s.y - s.hh))

    def at(self, side, d=0.0):
        """Точка на стороне side ('l','r','t','b') со смещением d вдоль стороны."""
        return {"l": (self.x - self.hw, self.y + d), "r": (self.x + self.hw, self.y + d),
                "t": (self.x + d, self.y + self.hh), "b": (self.x + d, self.y - self.hh)}[side]


class Diagram:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.fig = plt.figure(figsize=(w * UNIT, h * UNIT), dpi=200)
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(0, w)
        self.ax.set_ylim(0, h)
        self.ax.set_aspect("equal")
        self.ax.axis("off")

    def text(self, x, y, s, **kw):
        kw.setdefault("fontsize", FS - 1)
        kw.setdefault("zorder", 6)
        self.ax.text(x, y, s, **kw)

    def arrow(self, *pts, label=None, lxy=None, ha="left", va="center", both=False, fs=FS - 1.5,
              color="#222222", lw=1.0, ls="-", head=True):
        xs, ys = zip(*pts)
        self.ax.plot(xs, ys, color=color, lw=lw, ls=ls, zorder=3, solid_joinstyle="miter")
        if head:
            self.ax.annotate("", xy=pts[-1], xytext=pts[-2], zorder=3,
                             arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=9,
                                             shrinkA=0, shrinkB=0))
        if both:
            self.ax.annotate("", xy=pts[0], xytext=pts[1], zorder=3,
                             arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=9,
                                             shrinkA=0, shrinkB=0))
        if label:
            lx, ly = lxy if lxy else ((pts[0][0] + pts[1][0]) / 2, (pts[0][1] + pts[1][1]) / 2)
            self.ax.text(lx, ly, label, ha=ha, va=va, fontsize=fs, zorder=7, linespacing=1.05,
                         bbox=dict(fc="white", ec="none", pad=0.25))

    def line(self, *pts, color="#555555", lw=0.9):
        xs, ys = zip(*pts)
        self.ax.plot(xs, ys, color=color, lw=lw, zorder=2)

    def crop(self, y0, y1):
        self.ax.set_ylim(y0, y1)
        self.fig.set_size_inches(self.w * UNIT, (y1 - y0) * UNIT)

    def save(self, name):
        os.makedirs(OUT_DIR, exist_ok=True)
        self.fig.savefig(os.path.join(OUT_DIR, name), dpi=200, facecolor="white",
                         bbox_inches="tight", pad_inches=0.04)
        plt.close(self.fig)


# ====================================================================== EPC
EV_FC, EV_EC = "#f6dcef", "#9c2a7f"
FN_FC, FN_EC = "#ddf1d4", "#3b7a2b"
ORG_FC, ORG_EC = "#fff1bd", "#9a7d00"
DOC_FC, DOC_EC = "#e3edfb", "#2f5d8a"
APP_FC, APP_EC = "#eceff1", "#455a64"


class EPC(Diagram):
    EW, EH = 27, 6.4   # событие
    FW, FH = 27, 8.4   # функция
    R = 2.7            # оператор

    def event(self, x, y, text, w=None, h=None, fs=FS - 0.5):
        w, h = w or self.EW, h or self.EH
        d = 2.2
        pts = [(x - w / 2, y), (x - w / 2 + d, y + h / 2), (x + w / 2 - d, y + h / 2), (x + w / 2, y),
               (x + w / 2 - d, y - h / 2), (x - w / 2 + d, y - h / 2)]
        self.ax.add_patch(Polygon(pts, closed=True, fc=EV_FC, ec=EV_EC, lw=1.2, zorder=4))
        self.ax.text(x, y, text, ha="center", va="center", fontsize=fs, zorder=5, linespacing=1.05)
        return Node(x, y, w / 2, h / 2)

    def func(self, x, y, text, w=None, h=None, num=None, sub=False, fs=FS - 0.5):
        w, h = w or self.FW, h or self.FH
        self.ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                         boxstyle="round,pad=0,rounding_size=1.8",
                                         fc=FN_FC, ec=FN_EC, lw=1.2, zorder=4))
        self.ax.text(x, y, text, ha="center", va="center", fontsize=fs, zorder=5, linespacing=1.05)
        if num:
            self.ax.text(x + w / 2 - 0.8, y - h / 2 + 0.5, num, ha="right", va="bottom", fontsize=FS - 2.5,
                         weight="bold", color=FN_EC, zorder=5)
        if sub:  # значок декомпозиции (иерархия)
            bx, by = x - w / 2 + 1.0, y - h / 2 + 0.6
            self.ax.add_patch(Rectangle((bx + 0.6, by + 1.3), 1.0, 0.7, fc="white", ec=FN_EC, lw=0.6, zorder=5))
            self.ax.add_patch(Rectangle((bx, by), 0.9, 0.7, fc="white", ec=FN_EC, lw=0.6, zorder=5))
            self.ax.add_patch(Rectangle((bx + 1.3, by), 0.9, 0.7, fc="white", ec=FN_EC, lw=0.6, zorder=5))
            self.ax.plot([bx + 1.1, bx + 1.1], [by + 0.7, by + 1.3], color=FN_EC, lw=0.6, zorder=5)
        return Node(x, y, w / 2, h / 2)

    def path(self, x, y, text, w=None, h=None, fs=FS - 1):
        """Интерфейс процесса: функция на фоне события."""
        w, h = w or self.FW, h or self.FH
        d = 2.0
        ex, ey = x + 1.6, y - 1.4
        pts = [(ex - w / 2, ey), (ex - w / 2 + d, ey + h / 2), (ex + w / 2 - d, ey + h / 2), (ex + w / 2, ey),
               (ex + w / 2 - d, ey - h / 2), (ex - w / 2 + d, ey - h / 2)]
        self.ax.add_patch(Polygon(pts, closed=True, fc=EV_FC, ec=EV_EC, lw=1.0, zorder=3))
        self.ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0,rounding_size=1.8",
                                         fc=FN_FC, ec=FN_EC, lw=1.2, zorder=4))
        self.ax.text(x, y, text, ha="center", va="center", fontsize=fs, zorder=5, linespacing=1.05,
                     style="italic")
        return Node(x, y, w / 2, h / 2)

    def conn(self, x, y, kind="XOR"):
        self.ax.add_patch(Circle((x, y), self.R, fc="white", ec="#333333", lw=1.2, zorder=4))
        sym = {"XOR": "XOR", "AND": "∧", "OR": "∨"}[kind]
        self.ax.text(x, y - (0.05 if kind == "XOR" else 0.15), sym, ha="center", va="center",
                     fontsize=6.0 if kind == "XOR" else 11, weight="bold", zorder=5,
                     fontfamily="Arial" if kind == "XOR" else "DejaVu Sans")
        return Node(x, y, self.R, self.R)

    def org(self, x, y, text, w=19, h=6.4, fs=FS - 1):
        self.ax.add_patch(Ellipse((x, y), w, h, fc=ORG_FC, ec=ORG_EC, lw=1.0, zorder=4))
        self.ax.plot([x - w / 2 + 2.2, x - w / 2 + 2.2], [y - h / 2 + 1.05, y + h / 2 - 1.05],
                     color=ORG_EC, lw=1.0, zorder=5)
        self.ax.text(x + 0.9, y, text, ha="center", va="center", fontsize=fs, zorder=5, linespacing=1.0)
        return Node(x, y, w / 2, h / 2)

    def doc(self, x, y, text, w=20, h=6.4, fs=FS - 1):
        """Информационный объект (документ) – прямоугольник с волнистым низом."""
        import numpy as np
        xs = np.linspace(x - w / 2, x + w / 2, 30)
        wave = (y - h / 2) + 0.6 * np.sin((xs - (x - w / 2)) / w * 2 * np.pi)
        pts = [(x - w / 2, y + h / 2), (x + w / 2, y + h / 2)] + list(zip(xs[::-1], wave[::-1]))
        self.ax.add_patch(Polygon(pts, closed=True, fc=DOC_FC, ec=DOC_EC, lw=1.0, zorder=4))
        self.ax.text(x, y + 0.3, text, ha="center", va="center", fontsize=fs, zorder=5, linespacing=1.0)
        return Node(x, y, w / 2, h / 2)

    def app(self, x, y, text, w=19, h=6.4, fs=FS - 1):
        """Прикладная система."""
        self.ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fc=APP_FC, ec=APP_EC, lw=1.0, zorder=4))
        for dx in (1.3, 2.1):
            self.ax.plot([x - w / 2 + dx] * 2, [y - h / 2, y + h / 2], color=APP_EC, lw=0.8, zorder=5)
        self.ax.text(x + 1.0, y, text, ha="center", va="center", fontsize=fs, zorder=5, linespacing=1.0)
        return Node(x, y, w / 2, h / 2)

    # ---------- связи
    def down(self, a, b):
        """Поток управления сверху вниз (по одной вертикали или с изломом)."""
        if abs(a.x - b.x) < 0.01:
            self.arrow(a.b, b.t)
        else:
            mid = (a.b[1] + b.t[1]) / 2
            self.arrow(a.b, (a.x, mid), (b.x, mid), b.t)

    def split(self, c, *targets):
        for t in targets:
            if abs(t.x - c.x) < 0.01:
                self.arrow(c.b, t.t)
            else:
                side = c.r if t.x > c.x else c.l
                self.arrow(side, (t.x, c.y), t.t)

    def join(self, c, *sources):
        for s in sources:
            if abs(s.x - c.x) < 0.01:
                self.arrow(s.b, c.t)
            else:
                side = c.r if s.x > c.x else c.l
                self.arrow(s.b, (s.x, c.y), side)

    def attach(self, fn, obj, direction=None):
        """Связь функции с исполнителем/объектом. direction: 'in' (объект→функция), 'out', None."""
        if obj.x < fn.x:
            p_fn, p_ob = fn.l, obj.r
        else:
            p_fn, p_ob = fn.r, obj.l
        p_ob = (p_ob[0], fn.y) if abs(obj.y - fn.y) < 0.01 else p_ob
        if direction == "in":
            self.arrow(p_ob, p_fn, color="#555555", lw=0.8)
        elif direction == "out":
            self.arrow(p_fn, p_ob, color="#555555", lw=0.8)
        else:
            self.line(p_fn, p_ob)


# ====================================================================== DFD (Гейн–Сарсон)
PR_FC, PR_EC = "#eef4fb", "#2f5d8a"
EN_FC, EN_EC = "#fff4e0", "#8a5a00"
ST_FC, ST_EC = "#f3f3f3", "#444444"


class DFD(Diagram):
    @staticmethod
    def _slab(n, ox, oy, dx, dy):
        """Диапазон параметра t, на котором прямая o + t·d находится внутри прямоугольника узла n."""
        lo, hi = -1e9, 1e9
        for o, d, c, h in ((ox, dx, n.x, n.hw), (oy, dy, n.y, n.hh)):
            if abs(d) < 1e-9:
                continue
            t1, t2 = (c - h - o) / d, (c + h - o) / d
            lo, hi = max(lo, min(t1, t2)), min(hi, max(t1, t2))
        return lo, hi

    def link(self, a, b, label=None, both=False, off=0.0, t=0.5, side=None, gap=1.0, fs=FS - 1.5,
             lx=None, ly=None):
        """Поток данных a → b по прямой; off – параллельный сдвиг, подпись – снаружи (side)."""
        vx, vy = b.x - a.x, b.y - a.y
        ln = (vx * vx + vy * vy) ** 0.5
        ux, uy = vx / ln, vy / ln
        nx, ny = -uy, ux
        ox, oy = a.x + nx * off, a.y + ny * off
        t0 = self._slab(a, ox, oy, vx, vy)[1]
        t1 = self._slab(b, ox, oy, vx, vy)[0]
        p0 = (ox + vx * t0, oy + vy * t0)
        p1 = (ox + vx * t1, oy + vy * t1)
        self.arrow(p0, p1, both=both)
        if label:
            s = side if side is not None else (1 if off >= 0 else -1)
            px = p0[0] + (p1[0] - p0[0]) * t + nx * s * gap
            py = p0[1] + (p1[1] - p0[1]) * t + ny * s * gap
            kx, ky = nx * s, ny * s
            ha = "left" if kx > 0.35 else "right" if kx < -0.35 else "center"
            va = "bottom" if ky > 0.35 else "top" if ky < -0.35 else "center"
            self.ax.text(lx if lx is not None else px, ly if ly is not None else py, label, ha=ha, va=va,
                         fontsize=fs, zorder=7, linespacing=1.05, bbox=dict(fc="white", ec="none", pad=0.2))

    def process(self, x, y, num, text, w=26, h=15, fs=FS - 0.5):
        self.ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0,rounding_size=1.8",
                                         fc=PR_FC, ec=PR_EC, lw=1.4, zorder=4))
        band = 3.4
        self.ax.plot([x - w / 2, x + w / 2], [y + h / 2 - band] * 2, color=PR_EC, lw=1.0, zorder=5)
        self.ax.text(x, y + h / 2 - band / 2, num, ha="center", va="center", fontsize=fs - 0.5,
                     weight="bold", zorder=5)
        self.ax.text(x, y - band / 2, text, ha="center", va="center", fontsize=fs, zorder=5, linespacing=1.05)
        return Node(x, y, w / 2, h / 2)

    def entity(self, x, y, text, w=22, h=9, fs=FS - 0.5, dup=False):
        s = 1.0
        self.ax.add_patch(Rectangle((x - w / 2 + s, y - h / 2 - s), w, h, fc="#b8a17a", ec="none", zorder=3))
        self.ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fc=EN_FC, ec=EN_EC, lw=1.3, zorder=4))
        if dup:  # повторное изображение внешней сущности
            self.ax.plot([x - w / 2, x - w / 2 + 2.4], [y - h / 2 + 2.4, y - h / 2], color=EN_EC, lw=1.0, zorder=5)
        self.ax.text(x, y, text, ha="center", va="center", fontsize=fs, zorder=5, weight="bold", linespacing=1.05)
        return Node(x, y, w / 2, h / 2)

    def store(self, x, y, sid, text, w=30, h=6.5, fs=FS - 1):
        idw = 5.0
        self.ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fc=ST_FC, ec="none", zorder=3))
        self.ax.plot([x + w / 2, x - w / 2, x - w / 2, x + w / 2],
                     [y + h / 2, y + h / 2, y - h / 2, y - h / 2], color=ST_EC, lw=1.3, zorder=4)
        self.ax.plot([x - w / 2 + idw] * 2, [y - h / 2, y + h / 2], color=ST_EC, lw=1.0, zorder=4)
        self.ax.text(x - w / 2 + idw / 2, y, sid, ha="center", va="center", fontsize=fs, weight="bold", zorder=5)
        self.ax.text(x + idw / 2, y, text, ha="center", va="center", fontsize=fs, zorder=5, linespacing=1.0)
        return Node(x, y, w / 2, h / 2)
