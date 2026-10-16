"""Диаграммы BPMN для варианта 13 «Автосервис» (лабораторная работа №2)."""
from bpmn import Diagram

M, A, R, IS = "Мастер-приёмщик", "Автомеханик", "Руководитель", "ИС автосервиса"


def legend():
    d = Diagram(176, 50)
    y1, y2 = 38, 15
    d.task(12, y1, "Задача")
    d.task(34, y1, "Подпроцесс", sub=True)
    d.event(52, y1, "start", label="Начальное\nсобытие")
    d.event(66, y1, "start", "message", label="Начальное\n(сообщение)")
    d.event(80, y1, "start", "timer", label="Начальное\n(таймер)")
    d.event(94, y1, "inter", "message", label="Промежуточное\n(получение\nсообщения)")
    d.event(110, y1, "inter", "message_throw", label="Промежуточное\n(отправка\nсообщения)")
    d.event(126, y1, "inter", "timer", label="Промежуточное\n(таймер)")
    d.event(141, y1, "end", label="Завершающее\nсобытие")
    d.event(157, y1, "end", "message", label="Завершающее\n(сообщение)")

    d.gateway(8, y2, "x", label="Исключающий\n(XOR)", lpos="b")
    d.gateway(24, y2, "+", label="Параллельный\n(AND)", lpos="b")
    d.gateway(40, y2, "o", label="Включающий\n(OR)", lpos="b")
    d.gateway(56, y2, "event", label="Событийный", lpos="b")
    d.flow((66, y2), (80, y2))
    d.text(73, y2 - 3.5, "Поток\nуправления", ha="center", va="top")
    d.msg((86, y2), (100, y2))
    d.text(93, y2 - 3.5, "Поток\nсообщений", ha="center", va="top")
    d.assoc((106, y2), (120, y2), arrow=False)
    d.text(113, y2 - 3.5, "Ассоциация", ha="center", va="top")
    d.data(129, y2, "Объект\nданных")
    d.store(142, y2, "Хранилище\nданных")
    d.note(154, y2, "Текстовая\nаннотация")
    d.save("bpmn_legend.png")


def overview():
    d = Diagram(200, 106)
    d.blackbox(1, 94, 198, 8, "Клиент")
    ly = d.pool(1, 88, 198, "Автосервис", [(M, 28), (A, 22), (R, 22)])
    yM, yA, yR = ly[M], ly[A], ly[R]
    top = 94  # нижняя граница пула «Клиент»

    s = d.event(20, yM, "start", "message", label="Обращение\nклиента")
    a1 = d.task(38, yM, "Принять заявку\nи зарегистри-\nровать клиента", sub=True)
    a2 = d.task(62, yM, "Спланировать\nработы, назначить\nисполнителя", w=19, sub=True)
    a3 = d.task(86, yA, "Выполнить\nремонтные\nработы", sub=True)
    g1 = d.gateway(108, yA, "x", label="Выявлены доп.\nработы?", lpos="b")
    ag = d.task(108, yM, "Согласовать\nдоп. работы\nс клиентом")
    ev = d.event(128, yA, "inter", "message_throw", label="Автомобиль\nготов")
    a4 = d.task(148, yM, "Рассчитать стоимость,\nпринять оплату,\nвыдать квитанцию", w=21, sub=True)
    e1 = d.event(176, yM, "end", label="Автомобиль выдан,\nзаказ закрыт")

    d.flow(s.r, a1.l)
    d.flow(a1.r, a2.l)
    d.flow(a2.b, (62, yA), a3.l)
    d.flow(a3.r, g1.l)
    d.flow(g1.t, ag.b, label="Да", lxy=(109, yA + 4.5))
    d.flow(ag.l, (92, yM), (92, yA + 5))
    d.flow(g1.r, ev.l, label="Нет", lxy=(112, yA + 0.6))
    d.flow(ev.r, (148, yA), a4.b)
    d.flow(a4.r, e1.l)

    d.msg((20, top), s.t, label="Заявка на ремонт", lxy=(21, 84))
    d.msg(a2.t, (62, top), label="Плановая дата\nготовности", lxy=(63, 84.5))
    d.msg(ag.at(-3), (105, top), label="Запрос", lxy=(97, 85), ha="left")
    d.msg((111, top), ag.at(3), label="Решение", lxy=(112, 85))
    d.msg(ev.t, (128, top), label="SMS о\nготовности", lxy=(129, 66))
    d.msg(a4.at(-4), (144, top), label="Квитанция", lxy=(133, 85.5))
    d.msg((152, top), a4.at(4), label="Оплата", lxy=(153, 85.5))

    s2 = d.event(20, yR, "start", "timer", label="Конец рабочего\nдня / периода")
    a5 = d.task(42, yR, "Сформировать\nотчётность", sub=True)
    an = d.task(66, yR, "Проанализировать\nотчёты", w=19)
    e2 = d.event(88, yR, "end", label="Решения\nприняты")
    d.flow(s2.r, a5.l)
    d.flow(a5.r, an.l)
    d.flow(an.r, e2.l)

    db = d.store(112, yR, "БД ИС\nавтосервиса", lpos="l")
    d.assoc(a1.at(-5, "b"), (33, 41), (112, 41), db.t)
    d.assoc(a4.at(5, "b"), (153, yR), db.r)
    d.assoc(db.b, (112, 21), (42, 21), a5.b)
    d.crop(14.5, 104)
    d.save("bpmn_overview.png")


def scaffold(w, lanes, client=True, pool="Автосервис"):
    """Пул «Клиент» (свёрнутый) сверху, пул с дорожками ниже, место под хранилище снизу."""
    total = sum(h for _, h in lanes)
    h = 1 + (13 if client else 0) + total + 14
    d = Diagram(w, h)
    top = None
    if client:
        d.blackbox(1, h - 9, w - 2, 8, "Клиент")
        top = h - 9
    y_top = h - 14 if client else h - 1
    ly = d.pool(1, y_top, w - 2, pool, lanes)
    return d, ly, top, 7


def a1():
    d, ly, top, ys = scaffold(200, [(M, 26), (IS, 26)])
    yM, yI = ly[M], ly[IS]
    s = d.event(16, yM, "start", "message", label="Получено\nобращение")
    t2 = d.task(30, yI, "Найти клиента\nпо телефону\nили госномеру")
    g1 = d.gateway(46, yI, "x", label="Клиент\nнайден?", lpos="b")
    t3 = d.task(62, yI, "Подставить\nданные клиента\nв заявку")
    t4 = d.task(62, yM, "Зарегистриро-\nвать клиента\nи автомобиль")
    g2 = d.gateway(78, yI, "x")
    t5 = d.task(96, yM, "Осмотреть\nавтомобиль,\nзаполнить заявку", w=18)
    t6 = d.task(115, yI, "Рассчитать\nпредваритель-\nную стоимость")
    t7 = d.task(133, yM, "Согласовать\nстоимость\nс клиентом")
    g3 = d.gateway(150, yM, "x", label="Клиент\nсогласен?", lpos="t")
    ej = d.event(150, yI, "end", label="Заявка\nотклонена")
    t8 = d.task(168, yI, "Сохранить заявку,\nприсвоить номер,\nпечать акта приёма", w=19)
    eo = d.event(189, yI, "end", label="Заявка\nзарегистри-\nрована")

    d.flow(s.r, (30, yM), t2.t)
    d.flow(t2.r, g1.l)
    d.flow(g1.r, t3.l, label="Да", lxy=(49.5, yI + 0.5))
    d.flow(g1.t, (46, yM), t4.l, label="Нет", lxy=(46.8, yI + 5))
    d.flow(t3.r, g2.l)
    d.flow(t4.r, (78, yM), g2.t)
    d.flow(g2.r, (84, yI), (84, yM), t5.l)
    d.flow(t5.r, (115, yM), t6.t)
    d.flow(t6.r, (133, yI), t7.b)
    d.flow(t7.r, g3.l)
    d.flow(g3.b, ej.t, label="Нет", lxy=(150.8, yM - 6))
    d.flow(g3.r, (168, yM), t8.t, label="Да", lxy=(154, yM + 0.5))
    d.flow(t8.r, eo.l)

    d.msg((16, top), s.t, label="Обращение\n(звонок, визит)", lxy=(17, yM + 8))
    d.msg(t7.at(-3), (130, top), label="Предварительная\nстоимость", lxy=(110, yM + 8.5))
    d.msg((136, top), t7.at(3), label="Согласие /\nотказ", lxy=(137, yM + 8.5))
    d.msg(t8.at(5), (173, top), label="Акт приёма\nавтомобиля", lxy=(174, yM + 8.5))

    db = d.store(100, ys, "БД клиентов и заказов", lpos="b")
    d.assoc(t2.b, (30, ys), db.l)
    d.assoc(t8.b, (168, ys), db.r)
    zv = d.data(96, yM + 9.3, "Заявка", lpos="r")
    d.assoc(t5.t, zv.b)
    d.save("bpmn_a1.png")


def a2():
    d, ly, top, ys = scaffold(200, [(M, 26), (IS, 30)])
    yM, yI = ly[M], ly[IS]
    s = d.event(19, yM, "start", label="Заявка\nзарегистри-\nрована")
    t1 = d.task(35, yM, "Определить состав\nработ по регламенту\nТО", w=20)
    t2 = d.task(54, yI, "Показать загрузку\nпостов и механиков", w=19)
    t3 = d.task(80, yM, "Выбрать пост,\nмеханика\nи время")
    t4 = d.task(100, yI, "Проверить\nпересечения\nпо графику")
    g1 = d.gateway(118, yI, "x", label="Есть\nконфликт?", lpos="t")
    t5 = d.task(138, yI, "Сформировать\nзаказ-наряд,\nстатус «Принят»", w=18)
    t6 = d.task(160, yM, "Сообщить клиенту\nплановую дату\nготовности", w=18)
    e = d.event(186, yM, "end", label="Заказ-наряд\nпередан в работу")

    d.flow(s.r, t1.l)
    d.flow(t1.r, (54, yM), t2.t)
    d.flow(t2.r, (67, yI), (67, yM), t3.l)
    d.flow(t3.r, (100, yM), t4.t)
    d.flow(t4.r, g1.l)
    d.flow(g1.b, (118, yI - 10), (80, yI - 10), t3.b, label="Да: предупредить\nо пересечении",
           lxy=(85, yI - 9.5))
    d.flow(g1.r, t5.l, label="Нет", lxy=(121.5, yI + 0.5))
    d.flow(t5.r, (160, yI), t6.b)
    d.flow(t6.r, e.l)

    d.msg(t6.at(0), (160, top), label="Плановая дата\nготовности", lxy=(161, yM + 9))
    zn = d.data(152, yI - 9, "Заказ-наряд", lpos="r")
    d.assoc(t5.b, (138, yI - 9), zn.l)
    db = d.store(100, ys, "БД клиентов и заказов", lpos="b")
    d.assoc(db.l, (54, ys), t2.b)
    d.assoc(t5.at(-5, "b"), (133, ys), db.r)
    d.save("bpmn_a2.png")


def a3():
    d, ly, top, ys = scaffold(200, [(A, 24), (M, 36), (IS, 28)])
    yA, yM, yI = ly[A], ly[M], ly[IS]
    s = d.event(18, yA, "start", label="Получен\nзаказ-наряд")
    t2 = d.task(32, yA, "Выполнить работы\nпо заказ-наряду", w=19)
    g1 = d.gateway(52, yA, "x", label="Выявлены доп.\nнеисправности?", lpos="t")
    t3 = d.task(66, yI, "Внести доп. работы,\nстатус «Ожидает\nсогласования»", w=19)
    t4 = d.task(86, yM, "Согласовать\nдоп. работы\nс клиентом")
    eg = d.gateway(102, yM, "event")
    en = d.event(116, yM + 11, "inter", "message", label="Отказ", lpos="b")
    et = d.event(116, yM, "inter", "timer", label="2 часа", lpos="b")
    ey = d.event(116, yM - 11, "inter", "message", label="Согласие", lpos="t")
    t5 = d.task(128, yI, "Добавить работы,\nпересчитать\nстоимость и срок", w=18)
    t6 = d.task(136, yM, "Зафиксировать\nотказ от\nдоп. работ")
    g2 = d.gateway(152, yA, "x")
    t7 = d.task(168, yA, "Отметить запчасти,\nзавершить работы", w=19)
    t8 = d.task(168, yI, "Статус «Выполнен»,\nучесть выработку,\nуведомить мастера", w=19)
    e = d.event(189, yI, "end", "message", label="Работы\nвыполнены")

    d.flow(s.r, t2.l)
    d.flow(t2.r, g1.l)
    d.flow(g1.b, (52, yI), t3.l, label="Да", lxy=(52.8, yA - 6))
    d.flow(t3.r, (86, yI), t4.b)
    d.flow(t4.r, eg.l)
    d.flow(eg.t, (102, yM + 11), en.l)
    d.flow(eg.r, et.l)
    d.flow(eg.b, (102, yM - 11), ey.l)
    d.flow(ey.b, (116, yI), t5.l)
    d.flow(t5.b, (128, yI - 9), (36, yI - 9), t2.at(4, "b"))
    d.flow(en.r, (136, yM + 11), t6.t)
    d.flow(et.r, t6.l)
    d.flow(t6.r, (152, yM), g2.b)
    d.flow(g1.r, g2.l, label="Нет", lxy=(56, yA + 0.5))
    d.flow(g2.r, t7.l)
    d.flow(t7.b, t8.t)
    d.flow(t8.r, e.l)

    d.msg(t4.at(-3), (83, top), label="Запрос\nсогласования", lxy=(70, yA + 7.5))
    d.msg((116, top), en.t)
    d.msg((122, top), (122, yM - 11), ey.r)
    d.text(123, yA + 7.5, "Решение\nклиента", va="center")
    d.msg(e.t, (189, top), label="SMS о\nготовности", lxy=(190, yM))
    db = d.store(100, ys, "БД клиентов и заказов", lpos="b")
    d.assoc(t3.b, (66, ys), db.l)
    d.assoc(t8.b, (168, ys), db.r)
    d.save("bpmn_a3.png")


def a4():
    d, ly, top, ys = scaffold(200, [(M, 26), (IS, 30)])
    yM, yI = ly[M], ly[IS]
    s = d.event(17, yI, "start", label="Работы\nвыполнены")
    t1 = d.task(29, yI, "Проверить\nполноту заказа")
    g0 = d.gateway(45, yI, "x", label="Заказ\nполный?", lpos="b")
    tf = d.task(45, yM, "Устранить\nрасхождения")
    t2 = d.task(64, yI, "Рассчитать\nстоимость,\nсформировать\nквитанцию", w=17)
    t4 = d.task(84, yM, "Предъявить\nквитанцию\nклиенту")
    ep = d.event(101, yM, "inter", "message", label="Оплата\nполучена")
    t5 = d.task(118, yI, "Зафиксировать\nоплату, пробить\nчек (ККТ)")
    p1 = d.gateway(135, yI, "+")
    t6 = d.task(152, yI, "Закрыть заказ,\nстатус «Выдан»")
    t7 = d.task(152, yM, "Выдать\nавтомобиль\nи документы")
    p2 = d.gateway(170, yI, "+")
    e = d.event(186, yI, "end", label="Заказ\nзакрыт")

    d.flow(s.r, t1.l)
    d.flow(t1.r, g0.l)
    d.flow(g0.t, tf.b, label="Нет", lxy=(45.8, yI + 4.5))
    d.flow(tf.l, (29, yM), t1.t)
    d.flow(g0.r, t2.l, label="Да", lxy=(48.5, yI + 0.5))
    d.flow(t2.r, (84, yI), t4.b)
    d.flow(t4.r, ep.l)
    d.flow(ep.r, (118, yM), t5.t)
    d.flow(t5.r, p1.l)
    d.flow(p1.r, t6.l)
    d.flow(p1.t, (135, yM), t7.l)
    d.flow(t6.r, p2.l)
    d.flow(t7.r, (170, yM), p2.t)
    d.flow(p2.r, e.l)

    d.msg(t4.at(0), (84, top), label="Квитанция\nна оплату", lxy=(85, yM + 9))
    d.msg((101, top), ep.t, label="Оплата", lxy=(102, yM + 9))
    d.msg(t7.at(0), (152, top), label="Автомобиль,\nквитанция, чек", lxy=(153, yM + 9))
    db = d.store(100, ys, "БД клиентов и заказов", lpos="b")
    d.assoc(db.l, (64, ys), t2.b)
    d.assoc(t6.b, (152, ys), db.r)
    d.save("bpmn_a4.png")


def a5():
    d, ly, top, ys = scaffold(196, [(R, 26), (IS, 42)], client=False)
    yR, yI = ly[R], ly[IS]
    s2 = d.event(18, yR, "start", label="Нужен\nотчёт")
    t0 = d.task(31, yR, "Задать период\nи вид отчёта")
    s1 = d.event(18, yI, "start", "timer", label="Ежедневно\nв 21:00")
    g0 = d.gateway(47, yI, "x")
    t1 = d.task(64, yI, "Выбрать закрытые\nзаказы за период", w=18)
    p1 = d.gateway(81, yI, "+")
    ta = d.task(99, yI + 13, "Выручка по\nвидам работ", h=9)
    tb = d.task(99, yI, "Выработка\nмехаников", h=9)
    tc = d.task(99, yI - 13, "Новые и повторные\nклиенты", w=18, h=9)
    p2 = d.gateway(117, yI, "+")
    t5 = d.task(133, yI, "Сформировать\nотчёт")
    t6 = d.task(151, yR, "Проанализировать\nотчёт", w=18)
    g1 = d.gateway(168, yR, "x", label="Нужна\nвыгрузка?", lpos="t")
    t7 = d.task(168, yI, "Экспортировать\nв Excel")
    e = d.event(186, yR, "end", label="Отчёт\nполучен", lpos="t")

    d.flow(s2.r, t0.l)
    d.flow(t0.r, (47, yR), g0.t)
    d.flow(s1.r, g0.l)
    d.flow(g0.r, t1.l)
    d.flow(t1.r, p1.l)
    d.flow(p1.t, (81, yI + 13), ta.l)
    d.flow(p1.r, tb.l)
    d.flow(p1.b, (81, yI - 13), tc.l)
    d.flow(ta.r, (117, yI + 13), p2.t)
    d.flow(tb.r, p2.l)
    d.flow(tc.r, (117, yI - 13), p2.b)
    d.flow(p2.r, t5.l)
    d.flow(t5.r, (151, yI), t6.b)
    d.flow(t6.r, g1.l)
    d.flow(g1.b, t7.t, label="Да", lxy=(168.8, yR - 6))
    d.flow(g1.r, e.l, label="Нет", lxy=(171.5, yR + 0.5))
    d.flow(t7.r, (186, yI), e.b)
    db = d.store(100, ys, "БД клиентов и заказов", lpos="b")
    d.assoc(db.l, (64, ys), t1.b)
    d.data(133, yI - 12, "Отчёт", lpos="r")
    d.assoc(t5.b, (133, yI - 9.3))
    d.save("bpmn_a5.png")


if __name__ == "__main__":
    legend()
    overview()
    a1()
    a2()
    a3()
    a4()
    a5()
