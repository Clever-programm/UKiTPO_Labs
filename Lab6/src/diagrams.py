"""Диаграммы лабораторной работы №6: классы UML, структурная схема, развёртывание."""
import os

os.environ.setdefault("MPLCONFIGDIR", "/tmp/mplconfig")
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon, Rectangle

FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
OUT = os.path.join(os.path.dirname(__file__), "..", "img")

fp = FontProperties(fname=FONT_PATH)
fp_b = FontProperties(fname=FONT_BOLD)
fp_i = FontProperties(fname=FONT_PATH, style="italic")
fp_bi = FontProperties(fname=FONT_BOLD, style="italic")


def _fp(size, bold=False, italic=False):
    if bold and italic:
        f = FontProperties(fname=FONT_BOLD, style="italic")
    elif bold:
        f = FontProperties(fname=FONT_BOLD)
    elif italic:
        f = FontProperties(fname=FONT_PATH, style="italic")
    else:
        f = FontProperties(fname=FONT_PATH)
    f.set_size(size)
    return f


class UClass:
    def __init__(self, key, name, stereotype="", attrs=None, methods=None,
                 abstract=False, enum=False, fill="#FFFFFF", subtitle=""):
        self.key = key
        self.name = name
        self.stereotype = stereotype
        self.subtitle = subtitle
        self.attrs = attrs or []
        self.methods = methods or []
        self.abstract = abstract
        self.enum = enum
        self.fill = fill
        self.x = self.y = self.w = self.h = 0
        self.cx = self.cy = 0

    def header_lines(self):
        lines = []
        if self.stereotype:
            lines.append(("stereo", self.stereotype))
        lines.append(("name", self.name))
        if self.subtitle:
            lines.append(("sub", self.subtitle))
        return lines


def measure(ax, cls, name_size=9, body_size=7.4):
    fig = ax.figure
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()

    def width_of(text, size, bold=False, italic=False):
        t = ax.text(0, 0, text, fontproperties=_fp(size, bold, italic))
        bb = t.get_window_extent(renderer=renderer)
        t.remove()
        return bb.width / fig.dpi

    def height_of(size):
        return size / 72 * 1.22

    pad_x = 0.10
    max_w = width_of(cls.name, name_size, bold=True, italic=cls.abstract)
    if cls.stereotype:
        max_w = max(max_w, width_of(cls.stereotype, body_size - 0.4, italic=True))
    if cls.subtitle:
        max_w = max(max_w, width_of(cls.subtitle, body_size - 0.6, italic=True))
    for a in cls.attrs:
        max_w = max(max_w, width_of(a, body_size))
    for m in cls.methods:
        max_w = max(max_w, width_of(m, body_size))
    cls.w = max_w + pad_x * 2

    h = 0.06
    h += height_of(body_size - 0.4) if cls.stereotype else 0
    h += height_of(name_size)
    h += height_of(body_size - 0.6) if cls.subtitle else 0
    h += 0.06
    if cls.enum:
        for _ in cls.attrs:
            h += height_of(body_size)
        h += 0.06
    else:
        if cls.attrs or cls.methods:
            h += 0.02
        for _ in cls.attrs:
            h += height_of(body_size)
        if cls.methods:
            h += 0.02
        if cls.attrs and cls.methods:
            h += 0.04
        for _ in cls.methods:
            h += height_of(body_size)
        h += 0.06
    cls.h = max(h, 0.55)
    cls._name_size = name_size
    cls._body_size = body_size


def place(cls, cx, cy):
    cls.cx, cls.cy = cx, cy
    cls.x = cx - cls.w / 2
    cls.y = cy - cls.h / 2


def draw_class(ax, cls):
    ax.add_patch(Rectangle(
        (cls.x, cls.y), cls.w, cls.h,
        facecolor=cls.fill, edgecolor="#1A1A1A", linewidth=1.05, zorder=3,
    ))
    ns = cls._name_size
    bs = cls._body_size
    y = cls.y + cls.h - 0.04
    if cls.stereotype:
        y -= (bs - 0.4) / 72 * 1.05
        ax.text(cls.cx, y, cls.stereotype, ha="center", va="center",
                fontproperties=_fp(bs - 0.4, italic=True), color="#333333", zorder=4)
        y -= (bs - 0.4) / 72 * 0.25
    y -= ns / 72 * 0.55
    ax.text(cls.cx, y, cls.name, ha="center", va="center",
            fontproperties=_fp(ns, bold=True, italic=cls.abstract), zorder=4)
    y -= ns / 72 * 0.62
    if cls.subtitle:
        y -= (bs - 0.6) / 72 * 0.45
        ax.text(cls.cx, y, cls.subtitle, ha="center", va="center",
                fontproperties=_fp(bs - 0.6, italic=True), color="#444444", zorder=4)
        y -= (bs - 0.6) / 72 * 0.55
    # divider under header
    div1 = y - 0.03
    ax.plot([cls.x, cls.x + cls.w], [div1, div1], color="#1A1A1A", lw=0.8, zorder=4)
    y = div1 - 0.02
    if cls.enum:
        for val in cls.attrs:
            y -= bs / 72 * 0.62
            ax.text(cls.cx, y, val, ha="center", va="center",
                    fontproperties=_fp(bs), zorder=4)
            y -= bs / 72 * 0.55
        return
    left = cls.x + 0.08
    for a in cls.attrs:
        y -= bs / 72 * 0.58
        ax.text(left, y, a, ha="left", va="center", fontproperties=_fp(bs), zorder=4)
        y -= bs / 72 * 0.58
    if cls.methods:
        div2 = y - 0.02
        ax.plot([cls.x, cls.x + cls.w], [div2, div2], color="#1A1A1A", lw=0.8, zorder=4)
        y = div2 - 0.02
        for m in cls.methods:
            y -= bs / 72 * 0.58
            ax.text(left, y, m, ha="left", va="center", fontproperties=_fp(bs), zorder=4)
            y -= bs / 72 * 0.58


def _side_point(cls, side, shift=0.0):
    if side == "left":
        return cls.x, cls.cy + shift
    if side == "right":
        return cls.x + cls.w, cls.cy + shift
    if side == "top":
        return cls.cx + shift, cls.y + cls.h
    return cls.cx + shift, cls.y


def _pick_sides(a, b):
    dx = b.cx - a.cx
    dy = b.cy - a.cy
    if abs(dx) >= abs(dy) * 0.85:
        return ("right", "left") if dx > 0 else ("left", "right")
    return ("top", "bottom") if dy > 0 else ("bottom", "top")


def _shorten(x1, y1, x2, y2, dist):
    import math
    L = math.hypot(x2 - x1, y2 - y1) or 1
    k = dist / L
    return x2 - (x2 - x1) * k, y2 - (y2 - y1) * k


def _draw_path(ax, points, dashed=False, arrow=False):
    style = (0, (3.4, 2.0)) if dashed else "solid"
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        last = i == len(points) - 2
        if last and arrow:
            ax.annotate(
                "", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(
                    arrowstyle="-|>", color="#1A1A1A", lw=1.0,
                    linestyle=style, shrinkA=0, shrinkB=0, mutation_scale=9,
                ),
                zorder=2,
            )
        else:
            ax.plot([x1, x2], [y1, y2], color="#1A1A1A", lw=1.0, linestyle=style, zorder=2)


def _diamond(ax, border, outward, filled):
    """Ромб с вершиной на границе класса-целого, телом наружу."""
    import math
    ang = math.atan2(outward[1] - border[1], outward[0] - border[0])
    ux, uy = math.cos(ang), math.sin(ang)
    px, py = -uy, ux
    L, W = 0.17, 0.075
    contact = border
    back = (border[0] + ux * L, border[1] + uy * L)
    side1 = (border[0] + ux * L / 2 + px * W, border[1] + uy * L / 2 + py * W)
    side2 = (border[0] + ux * L / 2 - px * W, border[1] + uy * L / 2 - py * W)
    ax.add_patch(Polygon(
        [contact, side1, back, side2], closed=True,
        facecolor="#1A1A1A" if filled else "white",
        edgecolor="#1A1A1A", lw=0.95, zorder=4,
    ))
    return back


def _mult_near(ax, border, nxt, text, dist=0.34):
    if not text:
        return
    import math
    ang = math.atan2(nxt[1] - border[1], nxt[0] - border[0])
    ux, uy = math.cos(ang), math.sin(ang)
    px, py = -uy, ux
    # подпись кратности — по другую сторону линии, чем текстовая метка связи
    x = border[0] + ux * dist - px * 0.20
    y = border[1] + uy * dist - py * 0.20
    ax.text(x, y, text, ha="center", va="center", fontproperties=_fp(7.2, bold=True),
            color="#111111", zorder=6,
            bbox=dict(facecolor="white", edgecolor="none", pad=0.15))


def relate(ax, points, kind, m1="", m2="", label=""):
    """Ломаная. Для агрегации и композиции ромб стоит у первой точки (класс-целое)."""
    pts = [tuple(p) for p in points]
    m1_from = pts[0]
    if kind in ("aggr", "comp"):
        back = _diamond(ax, pts[0], pts[1], filled=(kind == "comp"))
        pts[0] = back
        m1_from = back
    _draw_path(ax, pts, dashed=(kind == "depend"), arrow=(kind == "depend"))
    _mult_near(ax, m1_from, pts[1] if pts[1] != m1_from else points[1], m1, dist=0.10)
    _mult_near(ax, points[-1], points[-2], m2, dist=0.14)
    if label:
        best = max(
            range(len(points) - 1),
            key=lambda i: abs(points[i + 1][0] - points[i][0]) + abs(points[i + 1][1] - points[i][1]),
        )
        mx = (points[best][0] + points[best + 1][0]) / 2
        my = (points[best][1] + points[best + 1][1]) / 2
        ax.text(mx, my + 0.10, label, ha="center", va="bottom",
                fontproperties=_fp(6.7, italic=True), color="#222222", zorder=6,
                bbox=dict(facecolor="white", edgecolor="none", pad=0.25))


def draw_inherit(ax, parent, children):
    """Обобщение: треугольная стрелка у родителя, шина к потомкам снизу."""
    import math
    xs = [c.cx for c in children]
    bus_y = min(parent.y, min(c.y + c.h for c in children) + 0.28)
    # keep the bus between parent bottom and children tops
    child_top = max(c.y + c.h for c in children)
    bus_y = (parent.y + child_top) / 2
    top_x = parent.cx
    # triangle
    tw, th = 0.16, 0.12
    tip = (top_x, parent.y)
    base_y = parent.y - th
    tri = [(tip[0], tip[1]), (tip[0] - tw / 2, base_y), (tip[0] + tw / 2, base_y)]
    ax.add_patch(Polygon(tri, closed=True, facecolor="white", edgecolor="#1A1A1A",
                         lw=0.95, zorder=4))
    ax.plot([top_x, top_x], [base_y, bus_y], color="#1A1A1A", lw=0.95, zorder=2)
    ax.plot([min(xs), max(xs)], [bus_y, bus_y], color="#1A1A1A", lw=0.95, zorder=2)
    for c in children:
        ax.plot([c.cx, c.cx], [bus_y, c.y + c.h], color="#1A1A1A", lw=0.95, zorder=2)


def new_fig(w, h):
    fig, ax = plt.subplots(figsize=(w, h), dpi=160)
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    fig.subplots_adjust(0, 0, 1, 1)
    return fig, ax


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=160)
    plt.close(fig)
    print(name, os.path.getsize(path))


FILL_E = "#FFF8EC"
FILL_B = "#EAF3FB"
FILL_C = "#E9F6EA"
FILL_N = "#F4F4F4"
FILL_U = "#F7F1FA"


def build_all():
    domain_uc1()
    domain_uc2()
    users()
    bce()
    structure()
    deployment()


def _ready(ax, classes, name_size=8.6, body_size=7.2):
    for c in classes:
        measure(ax, c, name_size=name_size, body_size=body_size)


def domain_uc1():
    """Клиент, автомобиль, заказ-наряд и расписание (UC-1)."""
    fig, ax = new_fig(10.2, 6.65)
    client = UClass(
        "client", "Клиент", "«entity»",
        ["+ id: UUID", "+ фио: String", "+ телефон: String",
         "+ согласиеПД: Boolean", "+ датаСогласия: Date"],
        ["+ selectByPhone(телефон): Клиент",
         "+ зарегистрировать(данные): Клиент"],
        fill=FILL_E, subtitle="накопитель D1",
    )
    car = UClass(
        "car", "Автомобиль", "«entity»",
        ["+ id: UUID", "+ госномер: String", "+ vin: String",
         "+ марка: String", "+ модель: String", "+ пробегКм: int"],
        ["+ selectByPlateOrVin(ключ): Автомобиль"],
        fill=FILL_E, subtitle="накопитель D1",
    )
    mech = UClass(
        "mech", "Автомеханик", "«entity»",
        ["+ табельныйНомер: String", "+ фио: String", "+ специализация: String"],
        ["+ назначенныеЗаказы(): List"],
        fill=FILL_U, subtitle="подкласс Сотрудник",
    )
    order = UClass(
        "order", "ЗаказНаряд", "«entity»",
        ["+ номер: String", "+ статус: СтатусЗаказа", "+ создан: DateTime",
         "+ плановаяДата: Date", "+ предвСумма: Money", "+ итогСумма: Money",
         "+ причинаОтказа: String"],
        ["+ createOrder(...): ЗаказНаряд",
         "+ setStatus(статус, момент)",
         "+ closeOrder()"],
        fill=FILL_E, subtitle="накопитель D2",
    )
    status = UClass(
        "st", "СтатусЗаказа", "«enumeration»",
        ["Принят", "Отклонён", "ВРаботе", "ОжидаетСогласования", "Выполнен", "Выдан"],
        enum=True, fill=FILL_N,
    )
    slot = UClass(
        "slot", "СлотРасписания", "«entity»",
        ["+ начало: DateTime", "+ окончание: DateTime"],
        ["+ checkOverlap(...): Boolean",
         "+ bookSlotAtomic(...): UUID"],
        fill=FILL_E, subtitle="накопитель D4",
    )
    post = UClass(
        "post", "Пост", "«entity»",
        ["+ код: String", "+ наименование: String"],
        [],
        fill=FILL_E, subtitle="накопитель D4",
    )
    classes = [client, car, mech, order, status, slot, post]
    _ready(ax, classes, name_size=8.2, body_size=7.0)
    place(client, 1.90, 5.30)
    place(car, 5.05, 5.30)
    place(mech, 7.20, 5.45)
    place(post, 9.30, 5.50)
    place(status, 1.15, 2.35)
    place(order, 3.55, 2.30)
    place(slot, 7.20, 2.40)
    for c in classes:
        draw_class(ax, c)

    # Клиент агрегирует автомобили: пустой ромб у Клиента
    relate(ax, [(client.x + client.w, client.cy), (car.x, car.cy)],
           "aggr", "1", "1..*", "владеет")
    # Клиент 1 — 0..* ЗаказНаряд
    relate(ax, [
        (client.cx, client.y),
        (client.cx, 3.85),
        (order.cx - 0.22, 3.85),
        (order.cx - 0.22, order.y + order.h),
    ], "assoc", "1", "0..*")
    # Автомобиль 1 — 0..* ЗаказНаряд
    relate(ax, [
        (car.cx, car.y),
        (car.cx, 4.05),
        (order.cx + 0.22, 4.05),
        (order.cx + 0.22, order.y + order.h),
    ], "assoc", "1", "0..*")
    # зависимость типа статуса: стрелка к перечислению
    relate(ax, [(order.x, order.cy), (status.x + status.w, status.cy)],
           "depend", label="тип статуса")
    # бронь слота
    relate(ax, [(order.x + order.w, order.cy), (slot.x, slot.cy)],
           "assoc", "1", "0..1", "бронь")
    # слот — пост, обход справа
    relate(ax, [
        (slot.x + slot.w, slot.cy),
        (post.cx, slot.cy),
        (post.cx, post.y),
    ], "assoc", "*", "1")
    # слот — механик
    relate(ax, [(slot.cx, slot.y + slot.h), (mech.cx, mech.y)],
           "assoc", "*", "1", "исполнитель")

    ax.text(0.15, 0.12,
            "Пустой ромб — агрегация (клиент владеет автомобилями). Сплошная линия — ассоциация. "
            "Пунктир — зависимость от перечисления статуса.",
            fontproperties=_fp(6.5), color="#333333")
    save(fig, "class_uc1.png")


def domain_uc2():
    fig, ax = new_fig(10.2, 6.75)
    order = UClass(
        "order", "ЗаказНаряд", "«entity»",
        ["+ номер: String", "+ статус: СтатусЗаказа",
         "+ времяНачала: DateTime", "+ времяОкончания: DateTime",
         "+ предвСумма: Money", "+ итогСумма: Money"],
        ["+ recalcCostAndDeadline(): Money",
         "+ savePartsAndSetDone(запчасти)",
         "+ closeOrder()"],
        fill=FILL_E, subtitle="D2, состав заказа",
    )
    work = UClass(
        "work", "ПозицияРаботы", "«entity»",
        ["+ нормоЧасы: Decimal", "+ цена: Money",
         "+ допРабота: Boolean", "+ согласована: Boolean"],
        [], fill=FILL_E,
    )
    part = UClass(
        "part", "ПозицияЗапчасти", "«entity»",
        ["+ штрихкод: String", "+ наименование: String",
         "+ количество: int", "+ цена: Money"],
        [], fill=FILL_E,
    )
    kind = UClass(
        "kind", "ВидРаботы", "«entity»",
        ["+ код: String", "+ наименование: String",
         "+ нормоЧасы: Decimal", "+ цена: Money", "+ действуетС: Date"],
        [], fill=FILL_E, subtitle="прейскурант D3",
    )
    regl = UClass(
        "regl", "РегламентТО", "«entity»",
        ["+ модельАвто: String", "+ пробегОт: int", "+ пробегДо: int"],
        ["+ getChecklistAndPrices(...): List"],
        fill=FILL_E, subtitle="регламенты D3",
    )
    pay = UClass(
        "pay", "Оплата", "«entity»",
        ["+ сумма: Money", "+ способ: СпособОплаты",
         "+ фискальныйПризнак: String", "+ статусЧека: String",
         "+ датаОплаты: DateTime"],
        ["+ сохранить(статусЧека: String)"],
        fill=FILL_E, subtitle="накопитель D5",
    )
    how = UClass(
        "how", "СпособОплаты", "«enumeration»",
        ["Наличные", "Карта"], enum=True, fill=FILL_N,
    )
    note = UClass(
        "note", "Уведомление", "«entity»",
        ["+ телефон: String", "+ текст: String", "+ тип: String",
         "+ статусДоставки: String", "+ отправлено: DateTime"],
        [], fill=FILL_E, subtitle="журнал К7",
    )
    report = UClass(
        "rep", "Отчёт", "«entity»",
        ["+ вид: String", "+ периодС: Date", "+ периодПо: Date",
         "+ автор: String", "+ создан: DateTime"],
        ["+ открытьБезПересчёта(): Файл"],
        fill=FILL_E, subtitle="архив D6",
    )
    classes = [order, work, part, kind, regl, pay, how, note, report]
    _ready(ax, classes, name_size=8.2, body_size=7.0)
    place(order, 1.55, 4.70)
    place(work, 4.55, 5.50)
    place(part, 6.70, 5.50)
    place(kind, 4.55, 3.45)
    place(regl, 7.20, 3.45)
    place(pay, 1.55, 1.50)
    place(how, 3.70, 1.40)
    place(note, 5.70, 1.45)
    place(report, 8.40, 1.50)
    for c in classes:
        draw_class(ax, c)

    # композиция: залитый ромб у ЗаказНаряд
    relate(ax, [
        (order.x + order.w, 5.05),
        (3.55, 5.05),
        (3.55, work.cy),
        (work.x, work.cy),
    ], "comp", "1", "1..*")
    # к позиции запчасти — справа от блока работ, чтобы кратность не попала на линию «читает»
    relate(ax, [
        (order.x + order.w, 4.50),
        (5.55, 4.50),
        (5.55, part.cy),
        (part.x, part.cy),
    ], "comp", "1", "0..*")
    relate(ax, [(work.cx, work.y), (kind.cx, kind.y + kind.h)],
           "assoc", "*", "1", "снимок цены")
    # регламент агрегирует виды работ: пустой ромб у РегламентТО
    relate(ax, [(regl.x, regl.cy), (kind.x + kind.w, kind.cy)],
           "aggr", "0..*", "1..*")
    relate(ax, [(order.cx, order.y), (pay.cx, pay.y + pay.h)],
           "assoc", "1", "0..1")
    relate(ax, [(pay.x + pay.w, pay.cy), (how.x, how.cy)], "depend")
    relate(ax, [
        (order.x + order.w, 4.05),
        (3.45, 4.05),
        (3.45, 2.55),
        (note.cx, 2.55),
        (note.cx, note.y + note.h),
    ], "assoc", "1", "0..*")
    # отчёт читает заказы, линия по правому и верхнему полю
    relate(ax, [
        (report.x + report.w, report.cy),
        (9.75, report.cy),
        (9.75, 6.52),
        (order.cx, 6.52),
        (order.cx, order.y + order.h),
    ], "depend", label="читает")
    ax.text(0.15, 0.12,
            "Залитый ромб — композиция: позиции работ и запчастей удаляются вместе с заказом. "
            "Пустой ромб — агрегация: вид работы живёт в прейскуранте и входит в несколько регламентов ТО.",
            fontproperties=_fp(6.4), color="#333333")
    save(fig, "class_uc2.png")


def users():
    fig, ax = new_fig(9.9, 6.15)
    user = UClass(
        "user", "Пользователь", "«abstract»",
        ["+ логин: String", "+ хэшПароля: String", "+ фио: String", "+ активен: Boolean"],
        ["+ проверитьПароль(пароль: String): Boolean"],
        abstract=True, fill=FILL_N,
    )
    emp = UClass(
        "emp", "Сотрудник", "«abstract»",
        ["+ табельныйНомер: String", "+ должность: String"],
        ["+ имеетРоль(роль: String): Boolean"],
        abstract=True, fill=FILL_N,
    )
    master = UClass(
        "master", "МастерПриёмщик", "«entity»",
        ["+ участокПриёмки: String"],
        [],
        fill=FILL_U,
    )
    mech = UClass(
        "mech", "Автомеханик", "«entity»",
        ["+ специализация: String"],
        ["+ назначенныеЗаказы(): List"],
        fill=FILL_U,
    )
    boss = UClass(
        "boss", "Руководитель", "«entity»",
        ["+ почтаДляОтчётов: String"],
        [],
        fill=FILL_U,
    )
    client = UClass(
        "client", "Клиент", "«entity»",
        ["+ телефон: String", "+ согласиеПД: Boolean"],
        ["+ зарегистрировать(...): Клиент"],
        fill=FILL_E, subtitle="не учётная запись, D1",
    )
    classes = [user, emp, master, mech, boss, client]
    _ready(ax, classes, name_size=9, body_size=7.6)
    place(user, 4.3, 5.05)
    place(emp, 4.3, 3.15)
    place(master, 1.7, 1.25)
    place(mech, 4.3, 1.20)
    place(boss, 6.9, 1.25)
    place(client, 8.85, 4.55)
    for c in classes:
        draw_class(ax, c)
    draw_inherit(ax, user, [emp])
    draw_inherit(ax, emp, [master, mech, boss])
    ax.annotate(
        "", xy=(client.x, client.cy), xytext=(user.x + user.w, user.cy),
        arrowprops=dict(arrowstyle="-|>", color="#A33B3B", lw=1.0,
                        linestyle=(0, (3, 2)), shrinkA=2, shrinkB=2),
        zorder=2,
    )
    ax.text(6.7, 5.55, "не является\nобобщением", ha="center", va="bottom",
            fontproperties=_fp(7, italic=True), color="#A33B3B")
    ax.text(0.15, 0.12,
            "Клиент интернет-записи не наследует Пользователь: онлайн-запись не создаёт учётную запись (U-06). "
            "Права АРМ задаются подклассом сотрудника (F-17).",
            fontproperties=_fp(6.6), color="#333333")
    save(fig, "class_users.png")


def bce():
    fig, ax = new_fig(11.2, 7.15)
    form = UClass(
        "form", "ФормаЗаявки", "«boundary»",
        [],
        ["+ openNewOrderForm()", "+ enterNewClient()",
         "+ selectServiceWorks()", "+ choosePostAndSlot()"],
        fill=FILL_B, subtitle="интерфейс К1, К2",
    )
    screen = UClass(
        "screen", "ЭкранМеханика", "«boundary»",
        [],
        ["+ startWork()", "+ addDefects()", "+ scanPartsAndFinish()"],
        fill=FILL_B, subtitle="планшет К3",
    )
    bill = UClass(
        "bill", "ФормаРасчёта", "«boundary»",
        [],
        ["+ openBillingForm()", "+ confirmPayment()"],
        fill=FILL_B, subtitle="интерфейс К4",
    )
    sms = UClass(
        "sms", "ШлюзSMS", "«boundary»",
        [],
        ["+ enqueueSms()", "+ sendApprovalSms()", "+ sendElectronicReceipt()"],
        fill=FILL_B, subtitle="адаптер К7",
    )
    kkt = UClass(
        "kkt", "ДрайверККТ", "«boundary»",
        [],
        ["+ printFiscalReceipt(сумма, позиции): String", "+ saveNoCheck()"],
        fill=FILL_B, subtitle="адаптер ККТ",
    )
    m1 = UClass(
        "m1", "МенеджерЗаявок", "«control»",
        [],
        ["+ findClient(телефон, госномер): Клиент",
         "+ registerClient(данные, согласиеПД): Клиент",
         "+ computeTotal(ставки): Money",
         "+ checkAndBookSlot(...): UUID",
         "+ createOrder(...): ЗаказНаряд",
         "+ rejectApplication(причина)"],
        fill=FILL_C, subtitle="К1, К2; create / destroy",
    )
    m3 = UClass(
        "m3", "МенеджерРемонта", "«control»",
        [],
        ["+ beginExecution(orderId)",
         "+ requestApproval(orderId, работы)",
         "+ onClientReply(orderId, решение)",
         "+ onTimeoutOrReject(orderId, причина)",
         "+ completeRepair(orderId, запчасти)"],
        fill=FILL_C, subtitle="К3",
    )
    m4 = UClass(
        "m4", "МенеджерОплаты", "«control»",
        [],
        ["+ validateCompleteness(заказ): Boolean",
         "+ calcFinalAndBuildReceipt(заказ): PDF",
         "+ processPayment(сумма)",
         "+ closeOrder(orderId)"],
        fill=FILL_C, subtitle="К4; create / destroy",
    )
    m7 = UClass(
        "m7", "МенеджерУведомлений", "«control»",
        [],
        ["+ enqueueSms(телефон, текст)",
         "+ sendApprovalSms(телефон, ссылка)",
         "+ sendElectronicReceipt(телефон, pdf)"],
        fill=FILL_C, subtitle="К7",
    )
    e_client = UClass("ec", "Клиент", "«entity»", [], [], fill=FILL_E, subtitle="D1")
    e_order = UClass("eo", "ЗаказНаряд", "«entity»", [], [], fill=FILL_E, subtitle="D2")
    e_slot = UClass("es", "СлотРасписания", "«entity»", [], [], fill=FILL_E, subtitle="D4")
    e_price = UClass("ep", "РегламентТО", "«entity»", [], [], fill=FILL_E, subtitle="D3")
    e_pay = UClass("epay", "Оплата", "«entity»", [], [], fill=FILL_E, subtitle="D5")
    e_note = UClass("en", "Уведомление", "«entity»", [], [], fill=FILL_E, subtitle="журнал К7")

    bounds = [form, screen, bill, sms, kkt]
    ctrls = [m1, m3, m4, m7]
    ents = [e_client, e_order, e_slot, e_price, e_pay, e_note]
    _ready(ax, bounds + ctrls + ents, name_size=8.0, body_size=6.6)

    # Пары boundary–control выровнены по горизонтали, чтобы стрелки не пересекали классы.
    place(form, 1.85, 6.15)
    place(screen, 1.85, 4.55)
    place(bill, 1.85, 3.15)
    place(sms, 1.85, 1.75)
    place(kkt, 1.85, 0.62)
    place(m1, 5.55, 6.15)
    place(m3, 5.55, 4.55)
    place(m4, 5.55, 3.15)
    place(m7, 5.55, 1.75)
    ey = 6.35
    for e in ents:
        place(e, 9.85, ey)
        ey -= 0.95
    for c in bounds + ctrls + ents:
        draw_class(ax, c)

    def hdep(a, b):
        relate(ax, [(a.x + a.w, a.cy), (b.x, b.cy)], "depend")

    def to_entity(src, dst, gutter):
        relate(ax, [
            (src.x + src.w, src.cy),
            (gutter, src.cy),
            (gutter, dst.cy),
            (dst.x, dst.cy),
        ], "depend")

    hdep(form, m1)
    hdep(screen, m3)
    hdep(bill, m4)
    hdep(m7, sms)
    to_entity(m1, e_client, 7.55)
    to_entity(m1, e_order, 7.75)
    to_entity(m1, e_slot, 7.95)
    to_entity(m1, e_price, 8.15)
    to_entity(m3, e_order, 8.35)
    to_entity(m4, e_order, 8.55)
    to_entity(m4, e_pay, 8.75)
    to_entity(m7, e_note, 8.95)
    # К3 и К1 вызывают К7 в обход колонки контроллеров
    relate(ax, [
        (m3.x + m3.w, m3.cy - 0.12),
        (7.35, m3.cy - 0.12),
        (7.35, m7.cy),
        (m7.x + m7.w, m7.cy),
    ], "depend")
    relate(ax, [
        (m1.x + m1.w, m1.y + 0.08),
        (7.15, m1.y + 0.08),
        (7.15, m7.y + m7.h - 0.06),
        (m7.x + m7.w, m7.y + m7.h - 0.06),
    ], "depend")
    # оплата вызывает драйвер ККТ ниже шлюза SMS, не пересекая его
    relate(ax, [
        (m4.x, m4.cy),
        (3.55, m4.cy),
        (3.55, kkt.cy),
        (kkt.x + kkt.w, kkt.cy),
    ], "depend")
    relate(ax, [(m4.cx, m4.y), (m7.cx, m7.y + m7.h)], "depend")

    ax.text(1.85, 6.95, "«boundary»", ha="center", fontproperties=_fp(8, bold=True), color="#1A4E7A")
    ax.text(5.55, 6.95, "«control»", ha="center", fontproperties=_fp(8, bold=True), color="#1E6B32")
    ax.text(9.85, 6.95, "«entity»", ha="center", fontproperties=_fp(8, bold=True), color="#8A5A00")
    save(fig, "class_bce.png")


def rbox(ax, x, y, w, h, text, edge, face, size=8.5, bold=False, lw=1.6, valign="center"):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
        facecolor=face, edgecolor=edge, linewidth=lw, zorder=3,
    ))
    if valign == "top":
        ax.text(x + w / 2, y + h - 0.14, text, ha="center", va="top",
                fontproperties=_fp(size, bold=bold), color="#1A1A1A", zorder=4, linespacing=1.35)
    else:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                fontproperties=_fp(size, bold=bold), color="#1A1A1A", zorder=4, linespacing=1.25)


def structure():
    fig, ax = new_fig(11.0, 6.55)
    ax.add_patch(Rectangle((0, 0), 11, 6.55, facecolor="white", edgecolor="none"))
    rbox(ax, 3.15, 5.85, 4.7, 0.52, "АИС учёта заказов и клиентов автосервиса",
         "#1565C0", "#E3F2FD", size=10, bold=True, lw=1.8)
    # bus
    ax.plot([5.5, 5.5], [5.85, 5.55], color="#37474F", lw=1.2, zorder=2)
    ax.plot([0.95, 10.05], [5.55, 5.55], color="#37474F", lw=1.2, zorder=2)

    cols = [
        ("Интерфейсы\nпользователей", "#2E7D32", "#E8F5E9",
         "— АРМ мастера-приёмщика\n— Планшет автомеханика\n— Онлайн-запись клиента\n— Кабинет руководителя"),
        ("К1. Клиенты\nи заявки", "#C2185B", "#FCE4EC",
         "— Поиск и регистрация клиента\n— Учёт автомобилей\n— Приём заявки\n— Акт приёма автомобиля"),
        ("К2–К3. Заказ\nи ремонт", "#00695C", "#E0F2F1",
         "— Подбор поста и механика\n— Учёт хода ремонта\n— Согласование доп. работ\n— Списание запчастей"),
        ("К4. Расчёты\nи оплата", "#F9A825", "#FFF8E1",
         "— Проверка полноты заказа\n— Квитанция PDF\n— Приём оплаты\n— Фискализация чека (ККТ)"),
        ("К5–К7. Отчёты\nи уведомления", "#5E35B1", "#EDE7F6",
         "— Очередь SMS\n— Отчёты и архив\n— Прейскурант и регламенты\n— Выгрузка XLSX"),
        ("База данных\nPostgreSQL", "#EF6C00", "#FFF3E0",
         "— D1 клиенты и авто\n— D2 заказы\n— D3 прейскурант\n— D4 график, D5 оплаты, D6 архив"),
    ]
    n = len(cols)
    gap = 0.12
    left = 0.18
    width = (11.0 - left * 2 - gap * (n - 1)) / n
    for i, (title, edge, face, body) in enumerate(cols):
        x = left + i * (width + gap)
        ax.plot([x + width / 2, x + width / 2], [5.55, 5.22], color="#37474F", lw=1.1, zorder=2)
        rbox(ax, x, 4.28, width, 0.94, title, edge, face, size=7.6, bold=True, lw=1.7)
        ax.annotate(
            "", xy=(x + width / 2, 3.82), xytext=(x + width / 2, 4.28),
            arrowprops=dict(arrowstyle="-|>", color=edge, lw=1.15), zorder=2,
        )
        rbox(ax, x, 2.05, width, 1.77, body, edge, "white", size=7.1, bold=False, lw=1.15, valign="top")

    rbox(ax, 0.18, 0.22, 10.64, 1.12,
         "Внешние системы (за границей АИС)\n"
         "SMS-шлюз — HTTPS API, очередь К7 не блокирует приём заказа     ·     "
         "ККТ / ОФД — драйвер, ФФД 1.2, сбой кассы не блокирует выдачу авто\n"
         "Клиент отвечает по SMS-ссылке (до 2 ч)     ·     "
         "Таймер 21:00 запускает ежедневный отчёт руководителя",
         "#546E7A", "#F5F7F8", size=7.3, lw=1.1)
    save(fig, "structure.png")


def deployment():
    fig, ax = new_fig(9.9, 4.55)
    def box(x, y, w, h, text, face, edge, size=8.2):
        rbox(ax, x, y, w, h, text, edge, face, size=size, bold=False, lw=1.3)

    box(0.25, 3.15, 2.15, 1.05, "ПК мастера\nи руководителя\nбраузер, ЛВС", "#E8F5E9", "#2E7D32", 7.6)
    box(2.6, 3.15, 2.15, 1.05, "Планшет механика\nWi-Fi цеха\nбез ПД клиента", "#E8F5E9", "#2E7D32", 7.6)
    box(4.95, 3.15, 2.25, 1.05, "Браузер клиента\nонлайн-запись\nи SMS-ссылка", "#E3F2FD", "#1565C0", 7.6)
    box(7.4, 3.35, 2.25, 0.85, "SMS-шлюз\nпровайдера\nHTTPS", "#FCE4EC", "#C2185B", 7.6)
    box(7.4, 2.15, 2.25, 0.85, "ККТ и ОФД\nФФД 1.2", "#FFF8E1", "#F9A825", 7.6)

    box(1.7, 1.35, 4.7, 1.15, "Сервер автосервиса  ·  Linux\nприложение К1–К7 (модульный монолит)\nвеб-интерфейс и внутренний API", "#E0F2F1", "#00695C", 8.0)
    box(1.7, 0.18, 4.7, 0.85, "PostgreSQL  ·  таблицы D1–D6\nежедневная шифрованная копия", "#FFF3E0", "#EF6C00", 8.0)

    def arrow(x1, y1, x2, y2, text=""):
        ax.annotate(
            "", xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(arrowstyle="<->", color="#37474F", lw=1.0),
            zorder=2,
        )
        if text:
            ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.08, text, ha="center",
                    fontproperties=_fp(6.4), color="#333333",
                    bbox=dict(facecolor="white", edgecolor="none", pad=0.2))

    arrow(1.32, 3.15, 3.2, 2.50, "HTTPS")
    arrow(3.67, 3.15, 3.9, 2.50)
    arrow(6.05, 3.15, 4.8, 2.50, "HTTPS")
    arrow(6.4, 1.95, 7.4, 3.6, "HTTPS")
    arrow(6.4, 1.7, 7.4, 2.55, "драйвер")
    arrow(4.05, 1.35, 4.05, 1.03, "SQL")
    ax.text(0.25, 4.32, "Локальная сеть автосервиса", fontproperties=_fp(8, bold=True), color="#1A1A1A")
    save(fig, "deploy.png")


if __name__ == "__main__":
    build_all()
