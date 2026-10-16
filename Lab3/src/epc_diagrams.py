"""Диаграммы EPC для варианта 13 «Автосервис» (лабораторная работа №3)."""
from shapes import EPC

P = 9.6  # шаг строк


def rows(h, top=6):
    return lambda r: h - top - r * P


def a1():
    H = 166
    d, y = EPC(130, H), rows(H)
    ORG, L, M, R, INF = 12, 36, 60, 86, 116
    BW = 24

    e0 = d.event(M, y(0), "Поступило обращение\nклиента")
    f1 = d.func(M, y(1), "Найти клиента по телефону\nили госномеру")
    d.attach(f1, d.app(ORG, y(1), "ИС\nавтосервиса"))
    d.attach(f1, d.doc(INF, y(1), "Клиенты и\nавтомобили"), "in")
    x1 = d.conn(M, y(2))
    eL = d.event(L, y(3), "Клиент найден", w=BW)
    eR = d.event(R, y(3), "Клиент не найден", w=BW)
    fL = d.func(L, y(4), "Подставить данные\nклиента в заявку", w=BW)
    d.attach(fL, d.app(ORG, y(4), "ИС\nавтосервиса"))
    fR = d.func(R, y(4), "Зарегистрировать\nклиента и автомобиль", w=BW)
    d.attach(fR, d.doc(INF, y(4), "Карточка клиента,\nсогласие на ПД"), "out")
    x2 = d.conn(M, y(5))
    e3 = d.event(M, y(6), "Данные клиента\nвнесены в заявку")
    f3 = d.func(M, y(7), "Осмотреть автомобиль,\nзаполнить заявку")
    d.attach(f3, d.org(ORG, y(7), "Мастер-\nприёмщик"))
    d.attach(f3, d.doc(INF, y(7), "Заявка"), "out")
    e4 = d.event(M, y(8), "Заявка заполнена")
    f4 = d.func(M, y(9), "Рассчитать предвари-\nтельную стоимость")
    d.attach(f4, d.app(ORG, y(9), "ИС\nавтосервиса"))
    d.attach(f4, d.doc(INF, y(9), "Прейскурант"), "in")
    e5 = d.event(M, y(10), "Стоимость\nрассчитана")
    f5 = d.func(M, y(11), "Согласовать стоимость\nс клиентом")
    d.attach(f5, d.org(ORG, y(11), "Мастер-\nприёмщик"))
    d.attach(f5, d.org(INF, y(11), "Клиент"))
    x3 = d.conn(M, y(12))
    eN = d.event(L, y(13), "Клиент\nотказался", w=BW)
    eY = d.event(R, y(13), "Клиент\nсогласен", w=BW)
    fN = d.func(L, y(14), "Зафиксировать\nотказ и причину", w=BW)
    d.attach(fN, d.app(ORG, y(14), "ИС\nавтосервиса"))
    fY = d.func(R, y(14), "Сохранить заявку,\nнапечатать акт приёма", w=BW)
    d.attach(fY, d.doc(INF, y(14), "Акт приёма\nавтомобиля"), "out")
    eNe = d.event(L, y(15), "Заявка\nотклонена", w=BW)
    eYe = d.event(R, y(15), "Заявка\nзарегистрирована", w=BW)
    pa = d.path(R, y(16), "Процесс A2 «Спланировать\nработы…»", w=BW + 2)

    d.down(e0, f1)
    d.down(f1, x1)
    d.split(x1, eL, eR)
    d.down(eL, fL)
    d.down(eR, fR)
    d.join(x2, fL, fR)
    d.down(x2, e3)
    for a, b in [(e3, f3), (f3, e4), (e4, f4), (f4, e5), (e5, f5), (f5, x3)]:
        d.down(a, b)
    d.split(x3, eN, eY)
    for a, b in [(eN, fN), (fN, eNe), (eY, fY), (fY, eYe), (eYe, pa)]:
        d.down(a, b)
    d.save("epc_a1.png")


def a0():
    H = 100
    d, y = EPC(194, H), rows(H)
    ORG, M, INF = 14, 56, 100
    e0 = d.event(M, y(0), "Поступило обращение\nклиента")
    f1 = d.func(M, y(1), "Принять заявку и\nзарегистрировать клиента", num="A1", sub=True)
    d.attach(f1, d.org(ORG, y(1), "Мастер-\nприёмщик"))
    d.attach(f1, d.doc(INF, y(1), "Заявка"), "out")
    x1 = d.conn(M, y(2))
    e2 = d.event(M, y(3), "Заявка\nзарегистрирована")
    er = d.event(INF, y(3), "Клиент\nотказался", w=24)
    f2 = d.func(M, y(4), "Спланировать работы,\nназначить исполнителя", num="A2", sub=True)
    d.attach(f2, d.org(ORG, y(4), "Мастер-\nприёмщик"))
    d.attach(f2, d.doc(INF, y(4), "Заказ-наряд"), "out")
    e3 = d.event(M, y(5), "Заказ-наряд\nпередан в работу")
    f3 = d.func(M, y(6), "Выполнить\nремонтные работы", num="A3", sub=True)
    d.attach(f3, d.org(ORG, y(6), "Автомеханик"))
    d.attach(f3, d.doc(INF, y(6), "Заказ-наряд"), "in")
    e4 = d.event(M, y(7), "Работы\nвыполнены")
    f4 = d.func(M, y(8), "Рассчитать стоимость,\nпринять оплату,\nвыдать квитанцию", num="A4", sub=True, h=10)
    d.attach(f4, d.org(ORG, y(8), "Мастер-\nприёмщик"))
    d.attach(f4, d.doc(INF, y(8), "Квитанция,\nкассовый чек"), "out")
    e5 = d.event(M, y(9), "Заказ закрыт")
    d.down(e0, f1)
    d.down(f1, x1)
    d.split(x1, e2, er)
    for a, b in [(e2, f2), (f2, e3), (e3, f3), (f3, e4), (e4, f4), (f4, e5)]:
        d.down(a, b)

    # отдельный процесс отчётности
    X = 154
    s1 = d.event(136, y(0), "Наступил конец\nрабочего дня", w=24)
    s2 = d.event(172, y(0), "Руководителю\nнужен отчёт", w=24)
    xj = d.conn(X, y(1))
    f5 = d.func(X, y(2), "Сформировать\nотчётность", num="A5", sub=True)
    d.attach(f5, d.org(128, y(3.2), "Руководитель"))
    d.attach(f5, d.doc(182, y(3.2), "Данные заказов\nи оплат"), "in")
    e6 = d.event(X, y(4), "Отчёт\nсформирован")
    d.join(xj, s1, s2)
    d.down(xj, f5)
    d.down(f5, e6)
    d.save("epc_a0.png")


def a2():
    H = 148
    d, y = EPC(132, H), rows(H)
    ORG, M, R, INF = 12, 60, 100, 116
    p0 = d.path(M, y(0), "Процесс A1 «Принять\nзаявку…»")
    e1 = d.event(M, y(1), "Заявка\nзарегистрирована")
    f1 = d.func(M, y(2), "Определить состав\nработ по регламенту ТО")
    d.attach(f1, d.org(ORG, y(2), "Мастер-\nприёмщик"))
    d.attach(f1, d.doc(INF, y(2), "Регламенты ТО"), "in")
    e2 = d.event(M, y(3), "Состав работ\nопределён")
    xj = d.conn(M, y(4))
    f2 = d.func(M, y(5), "Выбрать пост,\nмеханика и время")
    d.attach(f2, d.org(ORG, y(5), "Мастер-\nприёмщик"))
    d.attach(f2, d.doc(INF, y(5), "График\nзагрузки"), "in")
    e3 = d.event(M, y(6), "Исполнитель и\nвремя выбраны")
    f3 = d.func(M, y(7), "Проверить пересечения\nпо графику")
    d.attach(f3, d.app(ORG, y(7), "ИС\nавтосервиса"))
    d.attach(f3, d.doc(INF, y(7), "График\nзагрузки"), "in")
    xs = d.conn(M, y(8))
    eok = d.event(M, y(9), "Пересечений\nнет")
    ebad = d.event(R, y(9), "Обнаружено\nпересечение", w=24)
    f4 = d.func(M, y(10), "Сформировать\nзаказ-наряд")
    d.attach(f4, d.app(ORG, y(10), "ИС\nавтосервиса"))
    d.attach(f4, d.doc(INF, y(10), "Заказ-наряд"), "out")
    e4 = d.event(M, y(11), "Заказ-наряд\nсформирован")
    f5 = d.func(M, y(12), "Сообщить клиенту плано-\nвую дату готовности")
    d.attach(f5, d.org(ORG, y(12), "Мастер-\nприёмщик"))
    d.attach(f5, d.doc(INF, y(12), "SMS-\nуведомление"), "out")
    e5 = d.event(M, y(13), "Клиент уведомлён\nо сроке")
    p1 = d.path(M, y(14), "Процесс A3 «Выполнить\nремонтные работы»")
    for a, b in [(p0, e1), (e1, f1), (f1, e2), (e2, xj), (xj, f2), (f2, e3), (e3, f3), (f3, xs)]:
        d.down(a, b)
    d.split(xs, eok, ebad)
    d.arrow(ebad.r, (128.5, y(9)), (128.5, y(4)), xj.r)
    for a, b in [(eok, f4), (f4, e4), (e4, f5), (f5, e5), (e5, p1)]:
        d.down(a, b)
    d.save("epc_a2.png")


def a3():
    H = 166
    d, y = EPC(138, H), rows(H)
    ORG, M, B, S = 12, 40, 84, 122
    p0 = d.path(M, y(0), "Процесс A2 «Спланировать\nработы…»")
    e1 = d.event(M, y(1), "Заказ-наряд\nпередан в работу")
    xj = d.conn(M, y(2))
    f1 = d.func(M, y(3), "Выполнить работы\nпо заказ-наряду")
    d.attach(f1, d.org(ORG, y(3), "Автомеханик"))
    d.attach(f1, d.doc(B, y(3), "Заказ-наряд"), "in")
    xs = d.conn(M, y(4))
    eno = d.event(M, y(5), "Доп. неисправности\nне выявлены")
    eyes = d.event(B, y(5), "Выявлены доп.\nнеисправности", w=24)
    fa = d.func(B, y(6), "Согласовать доп.\nработы с клиентом", w=26)
    d.attach(fa, d.org(S, y(6), "Мастер-\nприёмщик"))
    xb = d.conn(B, y(7))
    eok = d.event(B, y(8), "Клиент\nсогласен", w=24)
    erf = d.event(S, y(8), "Отказ или нет\nответа за 2 ч", w=24)
    fadd = d.func(B, y(9), "Добавить работы, пере-\nсчитать стоимость и срок", w=26)
    frf = d.func(S, y(9), "Зафиксировать\nотказ", w=24)
    ech = d.event(B, y(10), "Заказ-наряд\nизменён", w=24)
    erd = d.event(S, y(10), "Отказ\nзафиксирован", w=24)
    xm = d.conn(M, y(11))
    f2 = d.func(M, y(12), "Отметить запчасти,\nзавершить работы")
    d.attach(f2, d.org(ORG, y(12), "Автомеханик"))
    d.attach(f2, d.doc(B, y(12), "Израсходованные\nзапчасти"), "out")
    e2 = d.event(M, y(13), "Работы\nзавершены")
    f3 = d.func(M, y(14), "Установить статус «Вы-\nполнен», уведомить клиента")
    d.attach(f3, d.app(ORG, y(14), "ИС\nавтосервиса"))
    d.attach(f3, d.doc(B, y(14), "SMS-\nуведомление"), "out")
    e3 = d.event(M, y(15), "Автомобиль готов\nк выдаче")
    p1 = d.path(M, y(16), "Процесс A4 «Рассчитать\nстоимость…»")

    for a, b in [(p0, e1), (e1, xj), (xj, f1), (f1, xs)]:
        d.down(a, b)
    d.split(xs, eno, eyes)
    d.down(eyes, fa)
    d.down(fa, xb)
    d.split(xb, eok, erf)
    for a, b in [(eok, fadd), (fadd, ech), (erf, frf), (frf, erd)]:
        d.down(a, b)
    d.arrow(ech.l, (62, y(10)), (62, y(2)), xj.r)
    d.arrow(eno.b, xm.t)
    d.arrow(erd.b, (S, y(11)), xm.r)
    for a, b in [(xm, f2), (f2, e2), (e2, f3), (f3, e3), (e3, p1)]:
        d.down(a, b)
    d.save("epc_a3.png")


def a4():
    H = 156
    d, y = EPC(130, H), rows(H)
    ORG, L, M, R, INF = 12, 36, 60, 92, 116
    p0 = d.path(M, y(0), "Процесс A3 «Выполнить\nремонтные работы»")
    e1 = d.event(M, y(1), "Работы\nвыполнены")
    xj = d.conn(M, y(2))
    f1 = d.func(M, y(3), "Проверить полноту\nзаказа")
    d.attach(f1, d.app(ORG, y(3), "ИС\nавтосервиса"))
    d.attach(f1, d.doc(INF, y(3), "Заказ-наряд"), "in")
    xs = d.conn(M, y(4))
    eok = d.event(M, y(5), "Заказ\nполный")
    ebad = d.event(R, y(5), "Обнаружены\nрасхождения", w=24)
    f2 = d.func(M, y(6), "Рассчитать стоимость,\nсформировать квитанцию")
    d.attach(f2, d.app(ORG, y(6), "ИС\nавтосервиса"))
    ffix = d.func(R, y(6), "Устранить\nрасхождения", w=24)
    e2 = d.event(M, y(7), "Квитанция\nсформирована")
    efix = d.event(R, y(7), "Расхождения\nустранены", w=24)
    f3 = d.func(M, y(8), "Предъявить квитанцию\nклиенту")
    d.attach(f3, d.org(ORG, y(8), "Мастер-\nприёмщик"))
    d.attach(f3, d.doc(INF, y(8), "Квитанция"), "out")
    e3 = d.event(M, y(9), "Оплата\nполучена")
    f4 = d.func(M, y(10), "Зафиксировать оплату,\nпробить чек на ККТ")
    d.attach(f4, d.app(ORG, y(10), "ИС\nавтосервиса"))
    d.attach(f4, d.doc(INF, y(10), "Кассовый\nчек"), "out")
    e4 = d.event(M, y(11), "Оплата\nзафиксирована")
    xa = d.conn(M, y(12), "AND")
    fc = d.func(L, y(13), "Закрыть заказ,\nстатус «Выдан»", w=24)
    d.attach(fc, d.app(ORG, y(13), "ИС\nавтосервиса"))
    fg = d.func(R, y(13), "Выдать автомобиль\nи документы", w=24)
    d.attach(fg, d.org(INF, y(13), "Мастер-\nприёмщик"))
    xb = d.conn(M, y(14), "AND")
    e5 = d.event(M, y(15), "Заказ закрыт")

    for a, b in [(p0, e1), (e1, xj), (xj, f1), (f1, xs)]:
        d.down(a, b)
    d.split(xs, eok, ebad)
    for a, b in [(eok, f2), (f2, e2), (ebad, ffix), (ffix, efix)]:
        d.down(a, b)
    d.arrow(efix.l, (77, y(7)), (77, y(2)), xj.r)
    for a, b in [(e2, f3), (f3, e3), (e3, f4), (f4, e4), (e4, xa)]:
        d.down(a, b)
    d.split(xa, fc, fg)
    d.join(xb, fc, fg)
    d.down(xb, e5)
    d.save("epc_a4.png")


def a5():
    H = 167
    d, y = EPC(130, H), rows(H)
    ORG, L, M, R, INF = 12, 36, 62, 88, 116
    s1 = d.event(L, y(0), "Наступило время\n21:00 (ежедневно)", w=26)
    s2 = d.event(R, y(0), "Руководителю\nнужен отчёт", w=24)
    fp = d.func(R, y(1), "Задать период\nи вид отчёта", w=24)
    d.attach(fp, d.org(INF, y(1), "Руководитель"))
    ep = d.event(R, y(2), "Параметры\nотчёта заданы", w=24)
    xj = d.conn(M, y(3))
    f1 = d.func(M, y(4), "Выбрать закрытые\nзаказы за период")
    d.attach(f1, d.app(ORG, y(4), "ИС\nавтосервиса"))
    d.attach(f1, d.doc(INF, y(4), "Заказы\nи оплаты"), "in")
    e1 = d.event(M, y(5), "Данные\nвыбраны")
    xa = d.conn(M, y(6), "AND")
    pa = d.func(28, y(7), "Рассчитать выручку\nпо видам работ", w=26)
    pb = d.func(M, y(7), "Рассчитать выра-\nботку механиков", w=26)
    pc = d.func(96, y(7), "Подсчитать новых и\nповторных клиентов", w=26)
    xb = d.conn(M, y(8), "AND")
    e2 = d.event(M, y(9), "Показатели\nрассчитаны")
    f2 = d.func(M, y(10), "Сформировать\nотчёт")
    d.attach(f2, d.app(ORG, y(10), "ИС\nавтосервиса"))
    d.attach(f2, d.doc(INF, y(10), "Отчёт"), "out")
    e3 = d.event(M, y(11), "Отчёт\nсформирован")
    f3 = d.func(M, y(12), "Проанализировать\nотчёт")
    d.attach(f3, d.org(ORG, y(12), "Руководитель"))
    xs = d.conn(M, y(13))
    ey = d.event(L, y(14), "Требуется\nвыгрузка", w=24)
    en = d.event(R, y(14), "Выгрузка не\nтребуется", w=24)
    fx = d.func(L, y(15), "Экспортировать\nотчёт в Excel", w=24)
    d.attach(fx, d.app(ORG, y(15) - 0.0, "ИС\nавтосервиса"))
    d.attach(fx, d.doc(INF - 30, y(15), "Файл XLSX"), "out")
    ex = d.event(L, y(16), "Отчёт\nвыгружен", w=24)

    d.down(s2, fp)
    d.down(fp, ep)
    d.arrow(s1.b, (L, y(3)), xj.l)
    d.arrow(ep.b, (R, y(3)), xj.r)
    for a, b in [(xj, f1), (f1, e1), (e1, xa)]:
        d.down(a, b)
    d.split(xa, pa, pb, pc)
    d.join(xb, pa, pb, pc)
    for a, b in [(xb, e2), (e2, f2), (f2, e3), (e3, f3), (f3, xs)]:
        d.down(a, b)
    d.split(xs, ey, en)
    d.down(ey, fx)
    d.down(fx, ex)
    d.save("epc_a5.png")


def legend():
    d = EPC(176, 34)
    y1, y2 = 24, 8
    d.event(18, y1, "Событие")
    d.func(52, y1, "Функция")
    d.func(86, y1, "Функция с\nдекомпозицией", sub=True)
    d.path(120, y1, "Интерфейс\nпроцесса")
    d.conn(146, y1, "XOR")
    d.conn(158, y1, "AND")
    d.conn(170, y1, "OR")
    d.text(158, y1 - 5, "Логические операторы", ha="center", va="top")
    d.org(14, y2, "Орг. единица")
    d.doc(42, y2, "Информ. объект")
    d.app(70, y2, "Прикладная\nсистема")
    d.arrow((86, y2), (102, y2))
    d.text(94, y2 - 2, "Поток\nуправления", ha="center", va="top")
    d.line((110, y2), (126, y2))
    d.text(118, y2 - 2, "Связь с испол-\nнителем", ha="center", va="top")
    d.arrow((134, y2), (150, y2), color="#555555", lw=0.8)
    d.text(142, y2 - 2, "Вход / выход\nданных", ha="center", va="top")
    d.save("epc_legend.png")


if __name__ == "__main__":
    legend()
    a0()
    a1()
    a2()
    a3()
    a4()
    a5()
