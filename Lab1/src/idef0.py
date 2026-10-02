"""Построение диаграмм IDEF0 (A-0 и A0) для варианта 13 «Автосервис»."""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

plt.rcParams["font.family"] = "Arial"

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "img")
FS = 10  # размер шрифта подписей стрелок


class Diagram:
    def __init__(self, w, h, node, title, number):
        self.w, self.h = w, h
        self.fig = plt.figure(figsize=(w * 0.08, h * 0.08), dpi=200)
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(0, w)
        self.ax.set_ylim(0, h)
        self.ax.axis("off")
        # рамка и штамп
        self.ax.add_patch(Rectangle((0.5, 0.5), w - 1, h - 1, fill=False, lw=1.2))
        self.ax.plot([0.5, w - 0.5], [7, 7], color="k", lw=1.2)
        self.ax.plot([28, 28], [0.5, 7], color="k", lw=1.2)
        self.ax.plot([w - 28, w - 28], [0.5, 7], color="k", lw=1.2)
        self.ax.text(2, 3.7, "УЗЕЛ:", fontsize=7, va="center")
        self.ax.text(12, 3.7, node, fontsize=12, va="center", weight="bold")
        self.ax.text(30, 3.7, "НАЗВАНИЕ:", fontsize=7, va="center")
        self.ax.text(w / 2 + 6, 3.7, title, fontsize=12, va="center", ha="center", weight="bold")
        self.ax.text(w - 26, 3.7, "НОМЕР:", fontsize=7, va="center")
        self.ax.text(w - 10, 3.7, number, fontsize=12, va="center", ha="center", weight="bold")

    def box(self, x, y, bw, bh, text, num, fs=10):
        self.ax.add_patch(Rectangle((x, y), bw, bh, fill=True, fc="white", ec="k", lw=1.6, zorder=3))
        self.ax.text(x + bw / 2, y + bh / 2 + 0.6, text, ha="center", va="center",
                     fontsize=fs, zorder=4, linespacing=1.15)
        self.ax.text(x + bw - 0.8, y + 0.8, num, ha="right", va="bottom", fontsize=9,
                     weight="bold", zorder=4)

    def line(self, pts, arrow=True):
        xs, ys = zip(*pts)
        self.ax.plot(xs, ys, color="k", lw=1.0, zorder=2, solid_joinstyle="round")
        if arrow:
            self.ax.annotate("", xy=pts[-1], xytext=pts[-2], zorder=2,
                             arrowprops=dict(arrowstyle="-|>", color="k", lw=1.0,
                                             mutation_scale=11, shrinkA=0, shrinkB=0))

    def label(self, x, y, text, ha="left", va="bottom", fs=FS):
        self.ax.text(x, y, text, ha=ha, va=va, fontsize=fs, linespacing=1.1, zorder=5,
                     bbox=dict(fc="white", ec="none", pad=0.3))

    def save(self, name):
        os.makedirs(OUT_DIR, exist_ok=True)
        self.fig.savefig(os.path.join(OUT_DIR, name), dpi=200)
        plt.close(self.fig)


def context():
    W, H = 160, 100
    d = Diagram(W, H, "A-0", "Обслуживать заказ клиента автосервиса", "1")
    bx, by, bw, bh = 38, 40, 84, 26
    d.box(bx, by, bw, bh, "Обслуживать заказ\nклиента автосервиса", "A0", fs=15)

    # Входы
    for y, t in [(59, "Обращение клиента\n(заявка на ремонт)"),
                 (53, "Автомобиль клиента"),
                 (47, "Запчасти и материалы")]:
        d.line([(1, y), (bx, y)])
        d.label(3, y + 0.5, t)
    # Управление
    for x, t in [(44, "Прейскурант\nна работы\nи запчасти"),
                 (60, "Регламенты ТО,\nтехнологи-\nческие карты"),
                 (76, "График\nзагрузки\nпостов и\nмехаников"),
                 (92, "Закон «О\nзащите прав\nпотребителей»,\nправила услуг"),
                 (108, "Требования\nк отчётности")]:
        d.line([(x, H - 1), (x, by + bh)])
        d.label(x + 1, H - 12, t, va="top")
    # Выходы
    for y, t in [(60, "Отремонтированный\nавтомобиль"),
                 (53, "Квитанция (акт\nвыполненных работ)"),
                 (46, "Отчёты по заказам\nи клиентам")]:
        d.line([(bx + bw, y), (W - 1, y)])
        d.label(bx + bw + 4, y + 0.5, t)
    # Механизмы
    for x, t in [(46, "Мастер-\nприёмщик"), (62, "Автомеханики"),
                 (78, "Оборудование"), (94, "ИС\nавтосервиса"), (110, "Руководитель")]:
        d.line([(x, 7), (x, by)])
        d.label(x + 1, 11, t)

    d.ax.text(3, 30, "Цель: определить границы ИС\nучёта заказов и клиентов\nавтосервиса.\n\n"
              "Точка зрения: руководитель\nавтосервиса.", fontsize=FS, va="top", linespacing=1.2)
    d.save("idef0_context.png")


def decomposition():
    W, H = 192, 122
    d = Diagram(W, H, "A0", "Обслуживать заказ клиента автосервиса", "2")
    bw, bh = 26, 15
    A = {1: (14, 93), 2: (48, 74), 3: (82, 55), 4: (116, 36), 5: (150, 17)}
    titles = {
        1: "Принять заявку\nи зарегистри-\nровать клиента",
        2: "Спланировать\nработы, назна-\nчить исполнителя",
        3: "Выполнить\nремонтные\nработы",
        4: "Рассчитать стои-\nмость, принять\nоплату, выдать\nквитанцию",
        5: "Сформировать\nотчётность",
    }
    for k, (x, y) in A.items():
        d.box(x, y, bw, bh, titles[k], f"A{k}", fs=10)
    L = {k: x for k, (x, y) in A.items()}
    R = {k: x + bw for k, (x, y) in A.items()}
    B = {k: y for k, (x, y) in A.items()}
    T = {k: y + bh for k, (x, y) in A.items()}
    top, bot = H - 1, 7

    # ---- Входы ----
    d.line([(1, 102), (L[1], 102)])
    d.label(2, 102.5, "Обращение\nклиента")
    d.line([(1, 65), (L[3], 65)])
    d.label(2, 65.5, "Автомобиль\nклиента")
    d.line([(1, 59), (L[3], 59)])
    d.label(2, 58.5, "Запчасти и\nматериалы", va="top")

    # ---- Управление ----
    d.line([(20, top), (20, T[1])])                        # прейскурант -> A1
    d.line([(20, 117), (126, 117), (126, T[4])])           # прейскурант -> A4
    d.label(70, 117.5, "Прейскурант на работы и запчасти")
    d.line([(136, top), (136, T[4])])                      # закон -> A4
    d.label(137, 105, "Закон «О защите\nправ потребителей»,\nправила оказания\nуслуг по ТО", va="top")
    d.line([(56, top), (56, T[2])])                        # регламенты -> A2
    d.line([(56, 109), (100, 109), (100, T[3])])           # регламенты -> A3
    d.label(68, 109.5, "Регламенты ТО, техкарты")
    d.line([(66, top), (66, T[2])])                        # график -> A2
    d.label(67, 96, "График загрузки\nпостов и механиков")
    d.line([(168, top), (168, T[5])])                      # требования -> A5
    d.label(169, 104, "Требования\nк отчётности", va="top")

    # ---- Внутренние связи ----
    d.line([(R[1], 99), (44, 99), (44, 81), (L[2], 81)])   # A1 -> A2
    d.label(43, 82, "Зарегистри-\nрованная\nзаявка", ha="right")
    d.line([(R[2], 83), (88, 83), (88, T[3])])             # A2 -> A3 (управление)
    d.label(75, 83.5, "Заказ-наряд")
    d.line([(R[3], 67), (114, 67), (114, 93), (70, 93), (70, T[2])])  # обратная связь A3 -> A2
    d.label(113, 75, "Выявленные\nдоп. работы", ha="right")
    d.line([(R[3], 59), (112, 59), (112, 43), (L[4], 43)])  # A3 -> A4
    d.label(111, 44, "Выполненные\nработы,\nзапчасти", ha="right")
    d.line([(R[4], 40), (146, 40), (146, 25), (L[5], 25)])  # A4 -> A5
    d.label(145, 26, "Данные\nзакрытого\nзаказа", ha="right")

    # ---- Выходы ----
    d.line([(R[3], 63), (W - 1, 63)])
    d.label(171, 63.5, "Отремонтиро-\nванный\nавтомобиль")
    d.line([(R[4], 47), (W - 1, 47)])
    d.label(171, 47.5, "Квитанция\n(акт выпол-\nненных работ)")
    d.line([(R[5], 28), (W - 1, 28)])
    d.label(R[5] + 1.5, 28.5, "Отчёты по\nзаказам и\nклиентам")

    # ---- Механизмы ----
    d.line([(18, bot), (18, B[1])])                        # мастер-приёмщик
    d.line([(18, 10), (52, 10), (52, B[2])])
    d.line([(52, 10), (120, 10), (120, B[4])])
    d.label(17, 7.3, "Мастер-приёмщик", ha="right", fs=8.5)
    d.line([(26, bot), (26, B[1])])                        # ИС автосервиса
    d.line([(26, 13.5), (60, 13.5), (60, B[2])])
    d.line([(60, 13.5), (128, 13.5), (128, B[4])])
    d.line([(128, 13.5), (158, 13.5), (158, B[5])])
    d.label(27, 14, "ИС автосервиса")
    d.line([(86, bot), (86, B[3])])
    d.label(85, 30, "Автомеханики", ha="right")
    d.line([(94, bot), (94, B[3])])
    d.label(95, 30, "Оборудование")
    d.line([(166, bot), (166, B[5])])
    d.label(167, 7.4, "Руководитель", fs=9)

    d.save("idef0_a0.png")


if __name__ == "__main__":
    context()
    decomposition()
