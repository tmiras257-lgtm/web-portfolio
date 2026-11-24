#!/usr/bin/env python3
"""Generates personalised demo-concept sites for real leads into web-portfolio/for/<slug>/.
All business facts come from the public 2GIS card (fetched 2026-11-23). Nothing invented:
unknown prices are shown as «уточняется», no fake reviews/masters/stats."""
import html, json, os, urllib.parse

OUT = os.path.dirname(os.path.abspath(__file__))
E = html.escape

NICHE = {
    "barber": dict(video="ostriyo-barbershop", acc="#d63a2f", acc2="#d9b26a", bg="#0e0e10", bg2="#17171a",
                   font="Oswald", credit="Mixkit (Mixkit Stock Video Free License), клип №271", kind="барбершоп"),
    "nails": dict(video="mirra-nail-brow", acc="#c9786b", acc2="#e8c4a8", bg="#140f0e", bg2="#1d1615",
                  font="Unbounded", credit="Mixkit (Mixkit Stock Video Free License)", kind="салон красоты"),
    "spa": dict(video="mirra-nail-brow", acc="#8fae9a", acc2="#e6d3b3", bg="#0f1311", bg2="#171d1a",
                font="Unbounded", credit="Mixkit (Mixkit Stock Video Free License)", kind="СПА-салон"),
    "gym": dict(video=None, acc="#ff5a1f", acc2="#ffd23f", bg="#0b0b0c", bg2="#161618",
                font="Oswald", credit="", kind="фитнес"),
    "gymsoft": dict(video=None, acc="#d98ca3", acc2="#f2d9c9", bg="#1a1315", bg2="#251a1d",
                    font="Unbounded", credit="", kind="женская фитнес-студия"),
    "hair": dict(video=None, acc="#c08a5b", acc2="#efd5b2", bg="#130f0d", bg2="#1d1714",
                 font="Unbounded", credit="", kind="салон красоты и парикмахерская"),
    "dental": dict(video="zhemchug-dental", acc="#3aa6b9", acc2="#cfeff3", bg="#0c1214", bg2="#131c1f",
                   font="Unbounded", credit="Mixkit (Mixkit Stock Video Free License), клип №21977", kind="стоматология"),
}

U = "уточняется"
SITES = [
 dict(slug="el-chapo", name="El Chapo", niche="barber", city="Шымкент", addr="Шымкент, ул. Жандосова, 5/7, 1 этаж",
      wa="77072171616", phone="+7 707 217 16 16", ig="https://instagram.com/el_chapo.kz",
      gis="https://2gis.kz/shymkent/firm/70000001064819237", rating=4.9, ratings=416, reviews=216, opens="11:00",
      h1=["Стрижка", "уровня", "шефа"], lead="Мужские и детские стрижки, борода, королевское бритьё головы и уход за лицом. Можно вызвать мастера на дом.",
      words=["Стрижка", "Борода", "Бритьё", "Маски", "Укладка"],
      tabs=[("Стрижки", [("Мужская стрижка", "5 000 ₸"), ("Стрижка от шеф-барбера", "6 000 ₸"), ("Детская стрижка", "5 000 ₸"),
                         ("Под машинку", "1 500 ₸"), ("Окантовка", "1 500 ₸"), ("Укладка", "1 500 ₸")]),
            ("Борода и бритьё", [("Стрижка + борода", "7 000–8 000 ₸"), ("Борода и усы", "3 000 ₸"), ("Тонировка бороды", "3 000 ₸"),
                                 ("Королевское бритьё головы", "5 000 ₸")]),
            ("Уход", [("Комплексная чистка лица", "5 000 ₸"), ("Глиняная маска", "3 000 ₸"), ("Скрабирование лица", "3 000 ₸"),
                      ("Чёрная маска", "3 000 ₸"), ("Воск (нос + уши)", "1 000 ₸"), ("Тонировка волос", "4 000 ₸"),
                      ("Химическая / биозавивка", "15 000–30 000 ₸")])],
      perks=["Выезд мастера на дом", "Wi-Fi", "Парковка на 5 мест рядом", "Пандус", "Оплата наличными и по QR"]),
 dict(slug="kreslo", name="Kreslo", niche="barber", city="Караганда", addr="Караганда, ул. Таттимбета, 10/14, ЖК Crystal",
      wa="77085201434", phone="+7 708 520 14 34", ig="https://instagram.com/kreslo_barbershop_krg",
      gis="https://2gis.kz/karaganda/firm/70000001066562700", rating=5.0, ratings=390, reviews=232, opens=None, award=True,
      h1=["Ваше", "кресло", "ждёт"], lead="Барбершоп в ЖК Crystal: мужские стрижки и борода. Онлайн-запись в пару касаний.",
      words=["Стрижка", "Борода", "Fade", "Укладка"],
      tabs=[("Услуги", [("Мужская стрижка", U), ("Стрижка + борода", U), ("Оформление бороды", U), ("Детская стрижка", U)])],
      perks=["Номинант 2ГИС Awards 2026", "Онлайн-запись", "5.0 по 390 оценкам"]),
 dict(slug="ghost", name="Ghost barbershop", niche="barber", city="Караганда", addr="Караганда, ул. Сарыарка, 6, ЖК Комфортный дом",
      wa="77770519008", phone="+7 777 051 90 08", ig="https://instagram.com/ghost_barbershop_krg",
      gis="https://2gis.kz/karaganda/firm/70000001083359147", rating=4.9, ratings=294, reviews=127, opens="10:00",
      booking="https://zapis.me/ghost-barbershop",
      h1=["Тихо.", "Чётко.", "Ghost."], lead="Два филиала в Караганде. Работаем по предварительной записи, без очередей.",
      words=["Стрижка", "Борода", "Fade", "Укладка"],
      tabs=[("Услуги", [("Мужская стрижка", U), ("Стрижка + борода", U), ("Оформление бороды", U), ("Детская стрижка", U)])],
      perks=["2 филиала", "Только по записи, без очередей", "Онлайн-запись на zapis.me"]),
 dict(slug="magellan", name="Magellan", niche="barber", city="Павлодар", addr="Павлодар, пр. Назарбаева, 32, 1 этаж",
      wa="77059910811", phone="+7 705 991 08 11", ig="https://instagram.com/magellan_barbershop",
      gis="https://2gis.kz/pavlodar/firm/70000001057291401", rating=4.9, ratings=410, reviews=205, opens="10:00", award=True,
      h1=["Курс", "на", "стиль"], lead="Барбершоп на проспекте Назарбаева: мужские и детские стрижки, химзавивка. Работаем по записи.",
      words=["Стрижка", "Кудри", "Борода", "Fade"],
      tabs=[("Услуги", [("Мужская стрижка", "от 4 500 ₸"), ("Детская стрижка", U), ("Мужская химзавивка", U)])],
      perks=["Номинант 2ГИС Awards 2026", "Парковка на 13 мест", "Остановка «Экономический колледж» в 150 м", "Оплата картой, наличными, переводом и QR"]),
 dict(slug="urban-kokshetau", name="URBAN barbershop", niche="barber", city="Кокшетау", addr="Кокшетау, ул. Абая, 59",
      wa="77766266660", phone="+7 776 626 66 60", ig="https://instagram.com/urban_barbershop_kokshe",
      gis="https://2gis.kz/kokshetau/firm/70000001033428604", rating=4.9, ratings=350, reviews=189, opens="10:00",
      h1=["Город.", "Стиль.", "URBAN."], lead="Мужские и детские стрижки, химзавивка, мужской маникюр и педикюр, солярий. Всё в одном месте на Абая.",
      words=["Стрижка", "Маникюр", "Солярий", "Кудри"],
      tabs=[("Стрижки", [("Мужская стрижка", "от 6 000 ₸"), ("Детская стрижка", U), ("Мужская химзавивка", U)]),
            ("Уход", [("Мужской маникюр", U), ("Мужской педикюр", U)]),
            ("Солярий", [("Вертикальный солярий", U), ("Турбосолярий", U)])],
      perks=["Wi-Fi", "Парковка на 22 места", "Остановка «Кенесары» в 300 м", "Оплата картой, наличными и QR"]),
 dict(slug="spa-studio-semey", name="Spa studio", niche="spa", city="Семей", addr="Семей, ул. Кашаганова, 18, БЦ Ахметов, каб. 101–102",
      wa="77471101292", phone="+7 747 110 12 92", ig="https://instagram.com/spastudio_semey",
      gis="https://2gis.kz/semej/firm/70000001082761964", rating=4.9, ratings=368, reviews=325, opens="08:00",
      h1=["Время", "для", "себя"], lead="СПА-салон в БЦ Ахметов. 325 гостей уже оставили отзыв в 2ГИС. Запишитесь в WhatsApp за минуту.",
      words=["СПА", "Массаж", "Уход", "Релакс"],
      tabs=[("Процедуры", [("Массаж", U), ("СПА-программы", U), ("Уход за телом", U)])],
      perks=["325 отзывов в 2ГИС", "Открываемся в 08:00", "Запись в WhatsApp"]),
 dict(slug="mona-beauty", name="Mona beauty home", niche="nails", city="Атырау", addr="Атырау, ЖК Модерн, ул. Таумуш Жумагалиева, 10, блок 9",
      wa="77787886685", phone="+7 778 788 66 85", ig="https://instagram.com/mona.beautyhome",
      gis="https://2gis.kz/atyrau/firm/70000001088192318", rating=4.8, ratings=242, reviews=111, opens="10:00",
      h1=["Красота", "как", "дома"], lead="Маникюр и педикюр, наращивание, ресницы и брови, причёски, эпиляция. Всё в одном салоне в ЖК Модерн.",
      words=["Маникюр", "Ресницы", "Брови", "Причёски"],
      tabs=[("Ногти", [("Японский маникюр", U), ("Аппаратный маникюр", U), ("Гель-лак", U), ("Наращивание гелем", U),
                       ("Наращивание акрилом", U), ("Женский педикюр", U)]),
            ("Ресницы и брови", [("Наращивание ресниц", U), ("Ламинирование ресниц", U), ("Окрашивание ресниц", U),
                                 ("Коррекция бровей", U), ("Окрашивание бровей", U), ("Ламинирование бровей", U)]),
            ("Волосы и кожа", [("Свадебные и вечерние причёски", U), ("Лазерная эпиляция", U), ("Шугаринг", U)])],
      perks=["Пандус", "Парковка на 9 мест", "Оплата картой, наличными, переводом и QR"]),
 dict(slug="alpha-gym", name="Alpha gym", niche="gym", city="Актобе", addr="Актобе, пр. Санкибай батыра, 1/3а, 1 этаж",
      wa="77711969650", phone="+7 771 196 96 50", ig="https://instagram.com/alpha.gym.aqtobe",
      gis="https://2gis.kz/aktobe/firm/70000001057651900", rating=4.9, ratings=866, reviews=242, opens=None,
      h1=["Стань", "сильнее", "здесь"], lead="Тренажёрный зал, боевые искусства, кроссфит и TRX. Персональные тренеры и массаж после тренировки.",
      words=["Кроссфит", "TRX", "Единоборства", "Железо"],
      tabs=[("Абонементы", [("Месячный абонемент", "от 16 000 ₸"), ("Годовой абонемент", "от 180 000 ₸"), ("Разовое посещение", U)]),
            ("Направления", [("Боевые искусства", U), ("Кроссфит", U), ("TRX-тренировки", U), ("Персональный тренер", U), ("Массаж", U)])],
      perks=["866 оценок в 2ГИС", "Парковка на 7 мест", "Остановка «ПОШ» в 150 м", "Оплата картой, наличными и QR"]),
 dict(slug="ns-fitness", name="NS Fitness", niche="gym", city="Уральск", addr="Уральск, мкр Астана, 8, 2 этаж",
      wa="77714937001", phone="+7 771 493 70 01", ig="https://instagram.com/nsfitness_uralsk",
      gis="https://2gis.kz/uralsk/firm/70000001094763356", rating=5.0, ratings=360, reviews=204, opens=None, award=True,
      h1=["Фитнес", "для", "всей семьи"], lead="Тренажёрный зал, групповые программы, сауны, фитнес-бар и детский уголок. Ребёнок занят, пока вы тренируетесь.",
      words=["Сайкл", "Зумба", "Йога", "Джампинг", "Кроссфит"],
      tabs=[("Абонементы", [("Месячный абонемент", "от 65 000 ₸"), ("Годовой абонемент", "от 320 000 ₸"), ("Разовое посещение", U)]),
            ("Группы", [("Сайкл", U), ("Зумба", U), ("Джампинг", U), ("Аэробика", U), ("Стретчинг", U), ("Йога", U),
                        ("Цигун", U), ("Hot Iron", U), ("Фитнес-бокс", U), ("Танцевальные программы", U)]),
            ("Ещё", [("Персональный тренер", U), ("Фитнес для детей", U), ("Массаж", U), ("Сауны", U)])],
      perks=["Номинант 2ГИС Awards 2026", "Детский уголок", "Фитнес-бар и сауны", "Бесплатная парковка на 20 мест"]),
 dict(slug="vysotsky-dental", name="Стоматология доктора Высоцкого", niche="dental", city="Павлодар", addr="Павлодар, ул. Естая, 85, 1 этаж",
      wa="77058011798", phone="+7 706 703 12 86", ig="https://instagram.com/s.vysotsky",
      gis="https://2gis.kz/pavlodar/firm/70000001018644145", rating=4.5, ratings=84, reviews=44, opens="09:00",
      h1=["Улыбка", "без", "страха"], lead="Хирургия, ортопедия и имплантация в одном комплексе. Срочная помощь при острой зубной боли.",
      words=["Имплантация", "Ортопедия", "Хирургия", "Снимки"],
      tabs=[("Услуги", [("Имплантация", U), ("Ортопедия (коронки, протезы)", U), ("Хирургия, удаление", U),
                        ("Прицельный снимок зуба", U), ("Срочная помощь при острой боли", U)])],
      perks=["Срочный приём при боли", "Пандус", "Парковка на 20 мест", "Оплата картой, наличными и QR"]),
 dict(slug="gravity-fit", name="Gravity Fit", niche="gymsoft", city="Алматы", addr="Алматы, мкр. Думан-2, 57/1 (цокольный этаж, 2 подъезд)",
      wa="77075360613", phone="+7 707 536 06 13", ig="https://www.instagram.com/gravity_fit.kz",
      gis="https://2gis.kz/almaty/firm/70000001080551882", rating=5.0, ratings=116, reviews=57, opens=None, hours="по предварительной записи",
      h1=["Сила", "в твоём", "ритме"], lead="Женская фитнес-студия в Думан-2: йога, пилатес, стретчинг, персональный тренер и массаж. Запись заранее, в WhatsApp.",
      words=["Йога", "Пилатес", "Стретчинг", "Массаж"],
      tabs=[("Абонементы", [("Месячный абонемент", "от 21 000 ₸"), ("Разовое посещение", "возможно, цена уточняется"), ("Персональный тренер", U)]),
            ("Направления", [("Йога", U), ("Пилатес", U), ("Стретчинг", U), ("Персональный тренер", U), ("Массаж", U)])],
      perks=["Только для женщин", "Запись заранее, без толпы", "Возможны разовые посещения", "Оплата картой, наличными, через банк и по QR"]),
 dict(slug="maira-kyzylorda", name="Майра", niche="hair", city="Кызылорда", addr="Кызылорда, ул. Гани Муратбаева, 18",
      wa="77770048888", phone="+7 777 004 88 88", ig=None,
      gis="https://2gis.kz/kyzylorda/firm/70000001063135116", rating=5.0, ratings=128, reviews=37, opens="09:00", hours="ежедневно 09:00–19:00",
      h1=["Стрижка", "с душой", "и вкусом"], lead="Парикмахерская и салон красоты в Кызылорде: стрижки, наращивание волос, плетение кос, свадебные и вечерние причёски.",
      words=["Стрижка", "Причёски", "Косы", "Наращивание"],
      tabs=[("Услуги", [("Мужская стрижка", "от 2 500 ₸"), ("Детская стрижка", U), ("Наращивание волос", U), ("Плетение кос", U),
                        ("Свадебные и вечерние причёски", U)])],
      perks=["Работаем каждый день, 09:00–19:00", "Запись в WhatsApp", "Оплата наличными и по QR"]),
]

WA_ICON = '<svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.5-3.9-4.7-4.1-.1-.2-1.1-1.5-1.1-2.9s.7-2 1-2.3c.3-.3.6-.3.8-.3h.6c.2 0 .4 0 .6.5l.9 2.1c.1.2.1.4 0 .5l-.3.5-.4.4c-.1.1-.3.3-.1.6.2.3.7 1.2 1.6 1.9 1.1 1 2 1.3 2.3 1.4.3.1.4.1.6-.1l.8-1c.2-.3.4-.2.6-.1l2 1c.3.1.5.2.5.4.1.2.1.8-.1 1.4z"/></svg>'


def page(s):
    n = NICHE[s["niche"]]
    wa = f"https://wa.me/{s['wa']}?text=" + urllib.parse.quote(f"Здравствуйте! Хочу записаться в {s['name']}")
    title = f"{s['name']} — {n['kind']} в {s['city']}е" if False else f"{s['name']} · {s['city']}"
    hero_media = (f'<video class="hv" autoplay muted loop playsinline preload="metadata" poster="../../{n["video"]}/assets/hero-poster.webp" aria-hidden="true" tabindex="-1">'
                  f'<source src="../../{n["video"]}/assets/hero-m.mp4" type="video/mp4" media="(max-width:799px)"><source src="../../{n["video"]}/assets/hero.mp4" type="video/mp4"></video>') if n["video"] else ""
    tabs_btn = "".join(f'<button class="{"on" if i == 0 else ""}" data-t="{i}">{E(t)}</button>' for i, (t, _) in enumerate(s["tabs"]))
    lists = "".join(
        f'<div class="list {"on" if i == 0 else ""}">' + "".join(
            f'<div class="item"><h3>{E(a)}</h3><span class="dots"></span><span class="pr {"q" if p == U else ""}">{E(p)}</span></div>' for a, p in items) + "</div>"
        for i, (_, items) in enumerate(s["tabs"]))
    has_unknown = any(p == U for _, it in s["tabs"] for _, p in it)
    stats = [(s["rating"], "рейтинг в 2ГИС", 1, ""), (s["ratings"], "оценок", 0, ""), (s["reviews"], "отзывов", 0, "")]
    stat4 = (f'<div class="stat rv"><b>{E(s["opens"])}</b><span>открываемся</span></div>' if s.get("opens")
             else '<div class="stat rv"><b>2026</b><span>номинант 2ГИС Awards</span></div>' if s.get("award")
             else '<div class="stat rv"><b>WA</b><span>запись в 1 касание</span></div>')
    stats_html = "".join(f'<div class="stat rv"><b data-c="{v}" data-d="{d}">0</b><span>{E(l)}</span></div>' for v, l, d, _ in stats) + stat4
    perks = "".join(f'<li class="rv">{E(p)}</li>' for p in s["perks"])
    words = "".join(f"<span>{E(w)}</span>" for w in s["words"] * 2)
    book = f'<a class="btn ghost" href="{E(s["booking"])}" rel="noopener">Онлайн-запись</a>' if s.get("booking") else f'<a class="btn ghost" href="#prices">Цены</a>'
    h1 = " ".join(f'<span class="w">{E(w)}</span>' for w in s["h1"])
    head_font = n["font"]
    fonts = "Oswald:wght@500;700" if head_font == "Oswald" else "Unbounded:wght@600;800"
    upper = "uppercase" if head_font == "Oswald" else "none"
    credit = f" · Видео: {n['credit']}" if n["credit"] else ""
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{E(title)} — демо-концепт сайта</title>
<meta name="description" content="Демо-концепт сайта для {E(s['name'])} ({E(s['city'])}). Подготовил веб-разработчик Мирас. Не официальный сайт заведения.">
<meta name="theme-color" content="{n['bg']}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family={fonts}&family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
<style>
:root{{--bg:{n['bg']};--bg2:{n['bg2']};--ink:#f2efe9;--muted:#aaa69f;--acc:{n['acc']};--acc2:{n['acc2']};--line:rgba(242,239,233,.14)}}
*{{box-sizing:border-box;margin:0;padding:0}}html{{scroll-behavior:smooth}}
body{{background:var(--bg);color:var(--ink);font-family:Inter,system-ui,sans-serif;overflow-x:hidden;-webkit-font-smoothing:antialiased;line-height:1.5}}
a{{color:inherit;text-decoration:none}}
h1,h2,h3{{font-family:'{head_font}',Impact,sans-serif;text-transform:{upper};line-height:1;letter-spacing:.01em}}
#gl{{position:fixed;inset:0;width:100%;height:100%;z-index:0;pointer-events:none}}
main{{position:relative;z-index:2}}
section{{padding:72px 20px;max-width:1100px;margin:auto}}
.eyebrow{{font-size:13px;letter-spacing:.22em;text-transform:uppercase;color:var(--acc2);font-weight:700}}
h2{{font-size:clamp(34px,8vw,68px);margin:10px 0 28px}}
.btn{{display:inline-flex;align-items:center;justify-content:center;gap:10px;padding:16px 26px;border-radius:6px;background:var(--acc);color:#fff;font-weight:700;font-size:15px;text-transform:uppercase;letter-spacing:.06em;transition:transform .25s,filter .25s;min-height:52px}}
.btn:active{{transform:scale(.97)}}.btn.ghost{{background:transparent;border:1px solid var(--line)}}
@media(hover:hover){{.btn:hover{{transform:translateY(-2px);filter:brightness(1.1)}}.btn.ghost:hover{{border-color:var(--acc2)}}}}
.btn.wa{{background:#25d366;color:#06240f}}
.demo{{position:relative;z-index:25;background:var(--acc2);color:#111;font-size:12.5px;text-align:center;padding:8px 14px;font-weight:600}}
header{{position:sticky;top:0;z-index:20;display:flex;justify-content:space-between;align-items:center;padding:12px 16px;background:linear-gradient(var(--bg),transparent)}}
.logo{{font-family:'{head_font}';font-weight:700;font-size:20px;letter-spacing:.06em;text-transform:{upper};min-height:44px;display:inline-flex;align-items:center}}
header .btn{{padding:10px 16px;min-height:42px;font-size:12px}}header nav{{display:none}}
@media(min-width:800px){{header{{padding:14px 40px}}header nav{{display:flex;gap:28px;font-size:14px;color:var(--muted)}}header nav a:hover{{color:var(--ink)}}}}
.hero{{min-height:92svh;max-width:none;display:flex;flex-direction:column;justify-content:flex-end;padding:80px 20px 56px;margin-top:-70px;position:relative;isolation:isolate}}
.hero .hv{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-1;opacity:.5}}
.hero::after{{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(0,0,0,.55),rgba(0,0,0,.2) 40%,var(--bg) 100%)}}
.hero .wrap{{max-width:1100px;width:100%;margin-inline:auto}}
.hero h1{{font-size:clamp(52px,13vw,150px);letter-spacing:-.01em}}
{'.hero h1{font-size:clamp(34px,9.4vw,120px);overflow-wrap:anywhere}.hero p{max-width:100%}.hero .wrap{padding-right:4px}' if s['niche'] in ('gymsoft','hair') else ''}
.hero h1 .w{{display:inline-block;animation:up 1s cubic-bezier(.2,.8,.2,1) both}}
.hero h1 .w:nth-child(2){{animation-delay:.12s;color:transparent;-webkit-text-stroke:2px var(--ink)}}
.hero h1 .w:nth-child(3){{animation-delay:.24s;color:var(--acc)}}
@keyframes up{{from{{opacity:0;transform:translateY(60px) rotate(2deg);filter:blur(10px)}}to{{opacity:1;transform:none;filter:none}}}}
.hero p{{color:#d6d1c9;max-width:480px;margin:22px 0 26px;font-size:17px}}
.hero .row{{display:flex;gap:12px;flex-wrap:wrap}}
.stats{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.stat{{border:1px solid var(--line);background:color-mix(in srgb,var(--bg2) 85%,transparent);padding:22px 18px;border-radius:8px}}
.stat b{{font:700 clamp(32px,8vw,54px) '{head_font}';display:block;color:var(--acc2)}}.stat span{{color:var(--muted);font-size:14px}}
@media(min-width:800px){{.stats{{grid-template-columns:repeat(4,1fr)}}}}
.bg{{background:var(--bg2);max-width:none;border-block:1px solid var(--line)}}.bg>.in{{max-width:1100px;margin:auto}}
.tabs{{display:flex;gap:8px;overflow-x:auto;margin-bottom:18px;scrollbar-width:none}}
.tabs button{{flex:none;background:none;border:1px solid var(--line);color:var(--muted);padding:10px 18px;border-radius:99px;font:600 14px Inter;cursor:pointer;min-height:44px}}
.tabs button.on{{background:var(--ink);color:#111;border-color:var(--ink)}}
.list{{display:none}}.list.on{{display:block;animation:fade .4s}}@keyframes fade{{from{{opacity:0;transform:translateY(10px)}}}}
.item{{display:flex;align-items:baseline;gap:12px;padding:16px 0;border-bottom:1px solid var(--line)}}
.item h3{{font-size:clamp(18px,4.4vw,26px);flex:none;max-width:64%}}
.item .dots{{flex:1;border-bottom:2px dotted #ffffff33;transform:translateY(-6px);min-width:16px}}
.item .pr{{font:700 clamp(17px,4.4vw,24px) '{head_font}';color:var(--acc2);white-space:nowrap}}.item .pr.q{{color:var(--muted);font:500 14px Inter}}
.note{{color:var(--muted);font-size:13px;margin-top:14px}}
.perks{{list-style:none;display:grid;gap:10px}}
.perks li{{border:1px solid var(--line);border-radius:8px;padding:18px 18px 18px 52px;position:relative;font-size:17px;background:color-mix(in srgb,var(--bg2) 80%,transparent)}}
.perks li::before{{content:"";position:absolute;left:18px;top:50%;width:18px;height:18px;margin-top:-9px;border-radius:50%;background:var(--acc);box-shadow:0 0 0 5px color-mix(in srgb,var(--acc) 25%,transparent)}}
@media(min-width:800px){{.perks{{grid-template-columns:1fr 1fr}}}}
.score{{display:flex;align-items:center;gap:22px;flex-wrap:wrap;border:1px solid var(--line);border-radius:10px;padding:26px;background:color-mix(in srgb,var(--bg2) 85%,transparent)}}
.score b{{font:700 clamp(60px,14vw,110px) '{head_font}';color:var(--acc2);line-height:1}}
.score .st{{color:var(--acc2);font-size:26px;letter-spacing:4px}}.score p{{color:var(--muted)}}
.mq{{overflow:hidden;border-block:1px solid var(--line);padding:20px 0;background:color-mix(in srgb,var(--bg) 85%,transparent)}}
.trk{{display:flex;gap:40px;width:max-content;font:700 clamp(28px,7vw,58px) '{head_font}';text-transform:{upper};white-space:nowrap}}
.trk span:nth-child(even){{color:transparent;-webkit-text-stroke:1px var(--acc2)}}
.visit{{display:grid;gap:14px}}
.info{{border:1px solid var(--line);border-radius:8px;padding:24px;background:color-mix(in srgb,var(--bg2) 85%,transparent)}}
.info div{{display:flex;justify-content:space-between;gap:14px;padding:13px 0;border-bottom:1px solid var(--line);font-size:15px}}
.info div span:last-child{{color:var(--muted);text-align:right}}
.cta{{text-align:center;padding:90px 20px}}
.cta .btn{{font-size:clamp(17px,4.5vw,24px);padding:22px 34px;width:100%;max-width:520px;animation:pulse 2.4s infinite}}
@keyframes pulse{{0%{{box-shadow:0 0 0 0 #25d36680}}70%,100%{{box-shadow:0 0 0 22px #25d36600}}}}
footer{{padding:30px 20px 110px;color:var(--muted);font-size:13px;text-align:center}}
.fab{{position:fixed;left:14px;right:14px;bottom:14px;z-index:30;display:flex;justify-content:center;align-items:center;gap:10px;height:56px;border-radius:8px;background:#25d366;color:#06240f;font:700 16px Inter;letter-spacing:.06em;text-transform:uppercase;box-shadow:0 10px 30px #000a;transform:translateY(120px);transition:transform .4s}}
.fab.show{{transform:none}}@media(min-width:800px){{.fab{{left:auto;right:24px;bottom:24px;padding:0 26px}}}}
.rv{{opacity:0;transform:translateY(34px)}}
:focus-visible{{outline:3px solid var(--acc2);outline-offset:3px;border-radius:6px}}
@media(prefers-reduced-motion:reduce){{.hero h1 .w{{animation:none}}.rv{{opacity:1!important;transform:none!important}}.cta .btn{{animation:none}}}}
</style>
</head>
<body>
<div class="demo">Демо-концепт сайта для «{E(s['name'])}». Подготовил веб-разработчик Мирас, это не официальный сайт заведения.</div>
<canvas id="gl" aria-hidden="true"></canvas>
<header>
  <a class="logo" href="#top">{E(s['name'])}</a>
  <nav><a href="#prices">Услуги</a><a href="#why">Почему мы</a><a href="#reviews">Отзывы</a><a href="#visit">Контакты</a></nav>
  <a class="btn" href="{E(wa)}">Записаться</a>
</header>
<main id="top">
  <section class="hero">{hero_media}<div class="wrap">
    <span class="eyebrow">{E(n['kind'])} · {E(s['city'])}</span>
    <h1>{h1}</h1>
    <p>{E(s['lead'])}</p>
    <div class="row"><a class="btn wa" id="heroWa" href="{E(wa)}">{WA_ICON} Записаться в WhatsApp</a>{book}</div>
  </div></section>
  <section><div class="stats">{stats_html}</div></section>
  <div class="mq"><div class="trk" id="trk">{words}</div></div>
  <div class="bg" id="prices"><section class="in">
    <span class="eyebrow">Услуги и цены</span><h2 class="rv">Что делаем</h2>
    <div class="tabs" role="tablist">{tabs_btn}</div>{lists}
    <p class="note">Цены и услуги взяты из открытой карточки 2ГИС.{' Где написано «уточняется», в рабочей версии будут ваши цены.' if has_unknown else ''}</p>
  </section></div>
  <section id="why"><span class="eyebrow">Удобно</span><h2 class="rv">Почему к нам</h2><ul class="perks">{perks}</ul></section>
  <section id="reviews"><span class="eyebrow">Отзывы</span><h2 class="rv">Нам доверяют</h2>
    <div class="score rv"><b>{s['rating']:.1f}</b><div><div class="st">★★★★★</div><p>{s['ratings']} оценок и {s['reviews']} отзывов в 2ГИС</p></div>
    <a class="btn ghost" style="margin-left:auto" href="{E(s['gis'])}" rel="noopener">Читать в 2ГИС</a></div>
    <p class="note">В рабочей версии здесь будут карточки ваших настоящих отзывов и фото работ.</p></section>
  <section id="visit"><span class="eyebrow">Как нас найти</span><h2 class="rv">Адрес</h2>
    <div class="visit"><div class="info">
      <div><span>Адрес</span><span>{E(s['addr'])}</span></div>
      <div><span>Телефон</span><span><a href="tel:{E(s['phone'].replace(' ', ''))}">{E(s['phone'])}</a></span></div>
      {f'<div><span>Открываемся</span><span>в {E(s["opens"])}</span></div>' if s.get('opens') and not s.get('hours') else ''}
      {f'<div><span>Часы</span><span>{E(s["hours"])}</span></div>' if s.get('hours') else ''}
      {f'<div><span>Instagram</span><span><a href="{E(s["ig"])}" rel="noopener">@{E(s["ig"].rstrip("/").split("/")[-1])}</a></span></div>' if s.get('ig') else ''}
      <a class="btn ghost" style="width:100%;margin-top:18px" href="{E(s['gis'])}" rel="noopener">Маршрут в 2ГИС</a>
    </div></div></section>
  <div class="cta"><h2 class="rv" style="margin-bottom:26px">Ждём вас</h2><a class="btn wa" href="{E(wa)}">{WA_ICON} Записаться в WhatsApp</a></div>
  <footer>Демо-концепт для «{E(s['name'])}» · данные из открытой карточки 2ГИС · сайт: веб-разработчик Мирас{E(credit)}</footer>
</main>
<a class="fab" id="fab" href="{E(wa)}">{WA_ICON} Записаться</a>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script>
const lists=[...document.querySelectorAll('.list')];
document.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>{{document.querySelectorAll('.tabs button').forEach(x=>x.classList.toggle('on',x===b));lists.forEach((l,i)=>l.classList.toggle('on',i==b.dataset.t))}});
const fab=document.getElementById('fab');new IntersectionObserver(([e])=>fab.classList.toggle('show',!e.isIntersecting)).observe(document.getElementById('heroWa'));
</script>
<script type="module">
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';
gsap.registerPlugin(ScrollTrigger);
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches,mobile=innerWidth<800;
document.querySelectorAll('.rv').forEach(el=>{{if(reduce)return;gsap.to(el,{{opacity:1,y:0,duration:.9,ease:'power3.out',scrollTrigger:{{trigger:el,start:'top 88%'}}}})}});
document.querySelectorAll('[data-c]').forEach(el=>{{const to=+el.dataset.c,d=+el.dataset.d,o={{v:0}};const set=()=>el.textContent=d?o.v.toFixed(d):Math.round(o.v).toLocaleString('ru-RU');
  if(reduce){{o.v=to;set();return}}ScrollTrigger.create({{trigger:el,start:'top 90%',once:true,onEnter:()=>gsap.to(o,{{v:to,duration:1.8,ease:'power2.out',onUpdate:set}})}})}});
const mq=gsap.to('#trk',{{xPercent:-50,duration:22,ease:'none',repeat:-1}});if(reduce)mq.pause();
let r;try{{r=new THREE.WebGLRenderer({{canvas:document.getElementById('gl'),antialias:!mobile,alpha:true}})}}catch(e){{}}
if(r&&!reduce){{
  r.setPixelRatio(Math.min(devicePixelRatio,mobile?1.5:2));const sc=new THREE.Scene(),cam=new THREE.PerspectiveCamera(45,1,.1,100);cam.position.z=9;
  const N=mobile?700:1600,p=new Float32Array(N*3);for(let i=0;i<N;i++){{const a=Math.random()*6.283,b=Math.acos(2*Math.random()-1),rr=3+Math.random()*1.2;
    p[i*3]=rr*Math.sin(b)*Math.cos(a);p[i*3+1]=rr*Math.sin(b)*Math.sin(a)*.55;p[i*3+2]=rr*Math.cos(b)}}
  const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.BufferAttribute(p,3));
  const m=new THREE.PointsMaterial({{color:new THREE.Color('{n['acc2']}'),size:.04,transparent:true,opacity:.7,depthWrite:false,blending:THREE.AdditiveBlending}});
  const pts=new THREE.Points(g,m);sc.add(pts);
  const ring=new THREE.Mesh(new THREE.TorusGeometry(2.2,.025,16,160),new THREE.MeshBasicMaterial({{color:new THREE.Color('{n['acc']}'),transparent:true,opacity:.8}}));sc.add(ring);
  const fit=()=>{{cam.aspect=innerWidth/innerHeight;cam.updateProjectionMatrix();r.setSize(innerWidth,innerHeight);const x=innerWidth<800?0:3.4;pts.position.x=ring.position.x=x}};fit();addEventListener('resize',fit);
  let mx=0,my=0,sp=0;addEventListener('pointermove',e=>{{mx=e.clientX/innerWidth-.5;my=e.clientY/innerHeight-.5}});
  ScrollTrigger.create({{onUpdate:s=>sp=s.progress}});
  (function f(t){{t*=.001;pts.rotation.y=t*.08+mx;pts.rotation.x=my*.5+sp*2;ring.rotation.x=1.1+my*.4+sp*3;ring.rotation.y=t*.3+mx;m.opacity=Math.max(.12,.7-sp);r.render(sc,cam);requestAnimationFrame(f)}})(0);
}}
</script>
</body>
</html>
"""


if __name__ == "__main__":
    index = {}
    for s in SITES:
        d = os.path.join(OUT, s["slug"])
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page(s))
        index[s["name"]] = f"https://tmiras257-lgtm.github.io/web-portfolio/for/{s['slug']}/"
    open(os.path.join(OUT, "robots-note.txt"), "w").write("Personal demo concepts for prospects; pages carry noindex.\n")
    print(json.dumps(index, ensure_ascii=False, indent=1))
