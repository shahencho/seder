import re
import json
import html as html_lib
from pathlib import Path

SAR_TO_USD = 1 / 3.75
BASE_DIR = Path(__file__).resolve().parent
MENU_HTML_PATH = BASE_DIR / "seder-palms-menu.html"

def slugify(name):
    s = name.lower()
    s = s.replace("&", "and")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s

def usd(sar):
    return f"{sar * SAR_TO_USD:.2f}"

# ---------------------------------------------------------------------------
# TRANSLATIONS
#
# Every dish is (name, price_sar, description, tags, i18n) where i18n is an
# OPTIONAL 5th element: a dict keyed by language code, each holding a "name"
# and/or "desc" override, e.g. {"ru": {"name": "...", "desc": "..."}}.
#
# It sits right next to the English text it translates so a native speaker
# reviewing/correcting it can compare both on the same line. A missing
# language key (or a missing "name"/"desc" inside it) just falls back to the
# English value automatically -- so translations can be filled in gradually
# and never break the page.
#
# To add Arabic later: add an "ar": {"name": ..., "desc": ...} entry next to
# the existing "ru" entry for each item. No code changes needed.
# ---------------------------------------------------------------------------

# (name, price_sar, description, tags[, i18n])
DATA = {
    "food": [
        ("Breakfast", [
            ("American Steak Breakfast", 47, "Steak, over easy egg, mushroom, grill tomato, roasted potato, toast bread, coffee.", ["halal"],
             {"ru": {"name": "Американский завтрак со стейком", "desc": "Стейк, яйцо-глазунья, грибы, жареный томат, картофель по-деревенски, тост, кофе."}}),
            ("English Breakfast Platter", 37, "Fried egg, grilled hot dog, saute mushroom, baked beans, bacon, grilled tomato, toast, coffee.", ["halal"],
             {"ru": {"name": "Английский завтрак", "desc": "Яичница, гриль-сосиска, тушёные грибы, печёная фасоль, бекон, жареный томат, тост, кофе."}}),
            ("Hash Brown Egg Benedict", 36, "Crispy hash brown eggs benedict, hollandaise sauce and sriracha mayo.", ["halal", "vegetarian", "spicy"],
             {"ru": {"name": "Яйца Бенедикт на картофельных драниках", "desc": "Хрустящие картофельные драники с яйцом пашот, соусом холландез и шрирача-майонезом."}}),
            ("Avocado Toast With Poached Egg", 38, "Guacamole in multigrain bread served with poached egg and horseradish sauce.", ["halal", "vegetarian"],
             {"ru": {"name": "Тост с авокадо и яйцом пашот", "desc": "Гуакамоле на мультизерновом хлебе, яйцо пашот и соус из хрена."}}),
            ("Your Choice Omelette", 20, "Vegetable or cheese omelette, served with hash brown or toast bread.", ["halal", "vegetarian"],
             {"ru": {"name": "Омлет на выбор", "desc": "Овощной или сырный омлет, подаётся с картофельными оладьями или тостом."}}),
            ("Philly Steak Omelette", 24, "Egg, steak, mozzarella cheese, bell peppers & onion.", ["halal"],
             {"ru": {"name": "Омлет со стейком по-филадельфийски", "desc": "Яйцо, стейк, сыр моцарелла, болгарский перец и лук."}}),
            ("Egg Any Style", 20, "Eggs cooked any style, served with hash brown, salsa and toast.", ["halal", "vegetarian"],
             {"ru": {"name": "Яйца по вашему выбору", "desc": "Яйца, приготовленные любым способом, подаются с картофельными оладьями, сальсой и тостом."}}),
            ("Egg N Bun", 24, "Two fried eggs in a brioche bun with caramelized onion, beef bacon, cheese and our special sauce, served with fries.", ["halal"],
             {"ru": {"name": "Яйцо в булочке", "desc": "Два яйца-глазуньи в бриоши с карамелизированным луком, беконом из говядины, сыром и фирменным соусом, подаётся с картофелем фри."}}),
            ("Chicken Schnitzel", 27, "Fried chicken, fries, sunny side up egg, hollandaise sauce.", ["halal"],
             {"ru": {"name": "Куриный шницель", "desc": "Жареная курица, картофель фри, яйцо-глазунья, соус холландез."}}),
            ("Shakshuka Slider", 27, "Our homemade shakshuka with feta cheese served in warm mini brioche buns.", ["halal", "vegetarian", "spicy"],
             {"ru": {"name": "Слайдер с шакшукой", "desc": "Домашняя шакшука с сыром фета в тёплых мини-бриошах."}}),
        ]),
        ("Salad", [
            ("Crispy Quinoa Salad", 37, "Crispy corn salad with feta, pomegranate, bell pepper, edamame, cherry tomato, spring onion and honey mustard vinaigrette.", ["halal", "vegetarian"],
             {"ru": {"name": "Хрустящий салат с киноа", "desc": "Хрустящий кукурузный салат с фетой, гранатом, болгарским перцем, эдамаме, черри и медово-горчичной заправкой."}}),
            ("Cobb Salmon Salad", 42, "Grilled salmon cubes, avocado, blue cheese, bacon, tomato, egg & mixed greens tossed in our vinaigrette.", ["halal", "seafood"],
             {"ru": {"name": "Салат Кобб с лососем", "desc": "Кубики лосося на гриле, авокадо, сыр с плесенью, бекон, томат, яйцо и микс зелени с фирменной заправкой."}}),
            ("Signature Steak Salad", 36, "Arugula leaves, warm potato salad, steak slices, edamame, parmesan cheese, balsamic reduction.", ["halal"],
             {"ru": {"name": "Фирменный салат со стейком", "desc": "Листья рукколы, тёплый картофельный салат, ломтики стейка, эдамаме, пармезан, соус бальзамик."}}),
            ("The Greek Salad", 29, "Lettuce, feta cheese, cucumber, olives, tomato, white onion, oregano vinaigrette.", ["halal", "vegetarian"],
             {"ru": {"name": "Греческий салат", "desc": "Салат латук, сыр фета, огурец, оливки, томат, белый лук, заправка с орегано."}}),
            ("Falafel Salad", 22, "Falafel, iceberg, cucumber, tomato, cucumber pickle, parsley, fries, tahina sauce.", ["halal", "vegetarian"],
             {"ru": {"name": "Салат с фалафелем", "desc": "Фалафель, айсберг, огурец, томат, маринованный огурец, петрушка, картофель фри, соус тахини."}}),
            ("Shrimp Cocktail Avocado Salad", 40, "Avocado salsa with de-shelled prawns drizzled with cocktail sauce.", ["halal", "seafood"],
             {"ru": {"name": "Салат с креветками и авокадо", "desc": "Сальса из авокадо с очищенными креветками, политыми соусом коктейль."}}),
            ("Classic Waldorf Salad", 28, "Apple slices, celery, yogurt, English mustard, lemon juice, grapes, cranberries, baby greens & romaine, candied walnuts.", ["halal", "vegetarian"],
             {"ru": {"name": "Классический салат Вальдорф", "desc": "Ломтики яблока, сельдерей, йогурт, английская горчица, лимонный сок, виноград, клюква, молодая зелень с романо, засахаренные грецкие орехи."}}),
            ("Exotic Rocca Salad", 25, "Rocca leaves, sundried tomato, grilled halloumi, parmesan served with pomegranate dressing.", ["halal", "vegetarian"],
             {"ru": {"name": "Экзотический салат Рокка", "desc": "Листья рукколы, вяленые томаты, халуми на гриле, пармезан с гранатовой заправкой."}}),
            ("Fattoush Salad", 20, "A healthy mix of fresh vegetables with toasted bread and pomegranate molasses.", ["halal", "vegetarian"],
             {"ru": {"name": "Салат Фаттуш", "desc": "Полезный микс свежих овощей с поджаренным хлебом и гранатовой патокой."}}),
            ("Caesar Chicken Salad", 26, "Grilled chicken, lettuce with Caesar dressing and parmesan.", ["halal"],
             {"ru": {"name": "Салат Цезарь с курицей", "desc": "Курица гриль, салат латук с соусом Цезарь и пармезаном."}}),
            ("Hummus", 14, "A smooth, creamy blend of chick peas, tahini, garlic, lemon & olive oil served with pita bread.", ["halal", "vegetarian"],
             {"ru": {"name": "Хумус", "desc": "Нежная паста из нута, тахини, чеснока, лимона и оливкового масла, подаётся с питой."}}),
        ]),
        ("Main Course", [
            ("Grilled Chicken Breast", 45, "Plain grilled chicken breast served with mash potato and vegetable.", ["halal"],
             {"ru": {"name": "Куриная грудка на гриле", "desc": "Куриная грудка на гриле с картофельным пюре и овощами."}}),
            ("Chicken Parmigiana", 37, "Breaded chicken breast topped with parmesan, turkey ham and marinara sauce with mash potato & veg.", ["halal"],
             {"ru": {"name": "Курица пармиджана", "desc": "Куриная грудка в панировке с пармезаном, индюшиной ветчиной и соусом маринара, картофельное пюре и овощи."}}),
            ("Chicken Marsala & Mushrooms", 36, "Thinly sliced chicken breast sauteed with shitake, porcini mushroom in a cream sauce, served with mash potato & steamed veg.", ["halal"],
             {"ru": {"name": "Курица марсала с грибами", "desc": "Тонко нарезанная куриная грудка с шиитаке и грибами порчини в сливочном соусе, картофельное пюре и овощи на пару."}}),
            ("Crispy Honey Lemon Chicken", 35, "Crispy fried chicken in honey lemon sauce served with steamed rice.", ["halal"],
             {"ru": {"name": "Хрустящая курица в медово-лимонном соусе", "desc": "Хрустящая жареная курица в медово-лимонном соусе, подаётся с рисом на пару."}}),
            ("Country Fried Chicken", 39, "Fried chicken breast, gravy sauce, mash potato, green beans.", ["halal"],
             {"ru": {"name": "Жареная курица по-деревенски", "desc": "Жареная куриная грудка, соус гриви, картофельное пюре, зелёная фасоль."}}),
            ("Chilli Chicken", 39, "Fried chicken cubes with bell peppers and Chinese sauce served with steamed rice or noodles.", ["halal", "spicy"],
             {"ru": {"name": "Курица чили", "desc": "Обжаренные кусочки курицы с болгарским перцем в китайском соусе, рис на пару или лапша."}}),
            ("Steak Tenderloin", 50, "Tenderloin fillet in mushroom sauce served with mash potato & veg.", ["halal"],
             {"ru": {"name": "Стейк из вырезки", "desc": "Вырезка в грибном соусе с картофельным пюре и овощами."}}),
            ("Beef Roulade", 54, "Beef stuffed with spinach & cheese served with mash potato & veg.", ["halal"],
             {"ru": {"name": "Рулет из говядины", "desc": "Говядина, фаршированная шпинатом и сыром, с картофельным пюре и овощами."}}),
            ("Mongolian Beef", 37, "Thin slices of caramelized beef in a balanced sauce tossed with green onions, served with steamed rice.", ["halal"],
             {"ru": {"name": "Говядина по-монгольски", "desc": "Тонко нарезанная карамелизированная говядина в пикантном соусе с зелёным луком, рис на пару."}}),
            ("Grilled Lamb Chops", 62, "Lamb chops served with roasted potatoes and tzatziki sauce.", ["halal"],
             {"ru": {"name": "Бараньи рёбрышки на гриле", "desc": "Бараньи рёбрышки с печёным картофелем и соусом дзадзики."}}),
            ("Rib Eye Steak", 90, "Rib eye steak rubbed & seasoned with fresh Italian herbs & fresh peppercorn sauce, served with mash potato and vegetable.", ["halal"],
             {"ru": {"name": "Стейк Рибай", "desc": "Стейк рибай, приправленный итальянскими травами и соусом из свежего перца, картофельное пюре и овощи."}}),
            ("Smoked Ribs", 68, "Short ribs with pure honey & BBQ sauce served with potato salad.", ["halal"],
             {"ru": {"name": "Копчёные рёбрышки", "desc": "Короткие рёбрышки в медовом соусе барбекю с картофельным салатом."}}),
            ("Braised Lamb Shank", 76, "Lamb shank in burgundy sauce served with mash potato.", ["halal"],
             {"ru": {"name": "Тушёная баранья голяшка", "desc": "Баранья голяшка в бургундском соусе с картофельным пюре."}}),
            ("Beef Stroganoff", 38, "Beef thin slices in creamy mushroom sauce served with steamed rice.", ["halal"],
             {"ru": {"name": "Бефстроганов", "desc": "Тонко нарезанная говядина в сливочно-грибном соусе, рис на пару."}}),
            ("Arabic Mixed Grill", 36, "Awsal, kabab, shishtawook served with hummus, garlic sauce, fries & bread.", ["halal"],
             {"ru": {"name": "Арабское мясное ассорти гриль", "desc": "Авсаль, кебаб, шиштавук с хумусом, чесночным соусом, картофелем фри и хлебом."}}),
            ("Peri Peri Chicken", 37, "Peri peri marinated chicken thigh served with nan bread, fries & garlic sauce.", ["halal", "spicy"],
             {"ru": {"name": "Курица пери-пери", "desc": "Куриное бедро в маринаде пери-пери с наан-хлебом, картофелем фри и чесночным соусом."}}),
            ("Grilled Rosemary Salmon", 50, "Grilled salmon on a bed of steamed fresh spinach served with mash potato.", ["halal", "seafood"],
             {"ru": {"name": "Лосось на гриле с розмарином", "desc": "Лосось на гриле на подушке из свежего шпината на пару с картофельным пюре."}}),
            ("Tepanyaki Salmon", 52, "Tepanyaki marinated salmon fillet served with garlic mashed potato and saute spinach.", ["halal", "seafood"],
             {"ru": {"name": "Лосось теппаняки", "desc": "Филе лосося в маринаде теппаняки с чесночным картофельным пюре и тушёным шпинатом."}}),
            ("Lobster Thermidor", 94, "Lobster tails served with lemon butter sauce, mash potato & veg.", ["halal", "seafood"],
             {"ru": {"name": "Лобстер термидор", "desc": "Хвосты лобстера с лимонно-масляным соусом, картофельным пюре и овощами."}}),
            ("Fish & Chips", 31, "Battered fish fillet served with mushy peas, coleslaw, tartar sauce.", ["halal", "seafood"],
             {"ru": {"name": "Рыба с картофелем фри", "desc": "Рыбное филе в кляре с зелёным горошком, коулслоу, соусом тартар."}}),
            ("Grilled Seafood Platter", 66, "Grilled shrimp, salmon, hamour, mussels & calamari served with saute veg & lemon butter sauce.", ["halal", "seafood"],
             {"ru": {"name": "Ассорти из морепродуктов гриль", "desc": "Креветки, лосось, хамур, мидии и кальмары на гриле с тушёными овощами и лимонно-масляным соусом."}}),
            ("Sriracha Grilled Shrimp", 53, "Shrimp with sriracha sauce served with cilantro rice.", ["halal", "seafood", "spicy"],
             {"ru": {"name": "Креветки гриль со шрирачей", "desc": "Креветки с соусом шрирача, рис с кинзой."}}),
            ("Nasi Goreng", 46, "Beef or chicken in goreng rice, cracker, over easy egg, peanut butter gravy.", ["halal"],
             {"ru": {"name": "Наси горенг", "desc": "Говядина или курица с жареным рисом по-индонезийски, крекер, яйцо-глазунья, соус на основе арахисового масла."}}),
            ("Butter Chicken", 33, "Traditional instant pot butter chicken masala served with ghee rice.", ["halal"],
             {"ru": {"name": "Баттер чикен", "desc": "Традиционная курица масала в сливочном соусе, рис гхи."}}),
            ("Tandoor Chicken Biryani", 34, "Tandoor marinated chicken biryani served with pickle, papad & raitha.", ["halal", "spicy"],
             {"ru": {"name": "Куриный бирьяни тандури", "desc": "Бирьяни с курицей, маринованной по рецепту тандури, подаётся с соленьями, папад и райта."}}),
            ("Kadai Masala", 33, "Chicken or beef marinated in kadai masala served with ghee rice.", ["halal", "spicy"],
             {"ru": {"name": "Кадай масала", "desc": "Курица или говядина в маринаде кадай масала, рис гхи."}}),
            ("Thai Red Curry", 33, "Chicken or beef in red coconut curry sauce served with steam rice.", ["halal", "spicy"],
             {"ru": {"name": "Тайское красное карри", "desc": "Курица или говядина в красном кокосовом соусе карри, рис на пару."}}),
        ]),
        ("Appetizer", [
            ("Dynamite Shrimp", 40, "Fried shrimp served with homemade dynamite sauce.", ["halal", "seafood", "spicy"],
             {"ru": {"name": "Креветки динамит", "desc": "Жареные креветки с домашним соусом динамит."}}),
            ("Nachos", 31, "Tortilla chips, guacamole, chili con carne, sour cream, jalapeno, olives, mozzarella cheese, salsa.", ["halal", "spicy"],
             {"ru": {"name": "Начос", "desc": "Кукурузные чипсы, гуакамоле, чили кон карне, сметана, халапеньо, оливки, сыр моцарелла, сальса."}}),
            ("Jalapeno Chicken Wings", 30, "Crispy chicken wings coated with homemade jalapeno sauce.", ["halal", "spicy"],
             {"ru": {"name": "Куриные крылышки с халапеньо", "desc": "Хрустящие куриные крылышки в домашнем соусе с халапеньо."}}),
            ("French Dip Slider", 32, "Beef, lettuce, cheddar cheese, slider sauce, caramelized onions.", ["halal"],
             {"ru": {"name": "Слайдер French Dip", "desc": "Говядина, салат латук, сыр чеддер, соус для слайдеров, карамелизированный лук."}}),
            ("Homemade Chicken Nuggets", 21, "Freshly made chicken fillet served with French fries.", ["halal"],
             {"ru": {"name": "Домашние куриные наггетсы", "desc": "Свежеприготовленное куриное филе, подаётся с картофелем фри."}}),
            ("Bacon Wrapped Steak Bites", 32, "Minced beef stuffed with Emmental cheese wrapped with bacon and BBQ glaze.", ["halal"],
             {"ru": {"name": "Кусочки стейка в беконе", "desc": "Рубленая говядина с сыром эмменталь, обёрнутая беконом, в соусе барбекю."}}),
            ("Buffalo Popcorn Chicken", 30, "Small bites of crispy deep fried chicken with spicy buffalo sauce, garnished with spring onion.", ["halal", "spicy"],
             {"ru": {"name": "Куриный попкорн буффало", "desc": "Небольшие кусочки хрустящей жареной курицы с острым соусом буффало, украшено зелёным луком."}}),
        ]),
        ("Sandwiches", [
            ("Pulled Smoked Beef Sandwich", 39, "Pulled beef, caramelized onion, Emmental cheese, multigrain bed, served with potato wedges and coleslaw.", ["halal"],
             {"ru": {"name": "Сэндвич с тушёной копчёной говядиной", "desc": "Тушёная говядина, карамелизированный лук, сыр эмменталь на мультизерновом хлебе, подаётся с картофельными дольками и коулслоу."}}),
            ("Chicken Avocado Panini Sandwich", 33, "Sandwich in panini bread stuffed with avocado, chicken and chef's sauce.", ["halal"],
             {"ru": {"name": "Панини с курицей и авокадо", "desc": "Панини с авокадо, курицей и фирменным соусом шефа."}}),
            ("Quesadilla", 33, "Tortilla filled with chicken, melted cheese, chilies, served with guacamole, salsa & sour cream with fries.", ["halal", "spicy"],
             {"ru": {"name": "Кесадилья", "desc": "Тортилья с курицей, расплавленным сыром, перцем чили, подаётся с гуакамоле, сальсой, сметаной и картофелем фри."}}),
            ("Beef Tenderloin Steak Sandwich", 36, "Beef tenderloin steak sandwich with sauteed onion, mushroom, melted cheese, garlic mustard mayo and smoked jalapeno sauce with fries.", ["halal", "spicy"],
             {"ru": {"name": "Сэндвич со стейком из говяжьей вырезки", "desc": "Стейк из говяжьей вырезки с обжаренным луком, грибами, расплавленным сыром, чесночно-горчичным майонезом и копчёным соусом халапеньо, подаётся с картофелем фри."}}),
            ("Classic Club Sandwich", 30, "Chicken salad, bacon, fried egg, tomato, lettuce, cheese & fries.", ["halal"],
             {"ru": {"name": "Классический клаб-сэндвич", "desc": "Куриный салат, бекон, яичница, томат, салат латук, сыр и картофель фри."}}),
            ("Bacon Cheese Beef Burger", 35, "Angus beef patty covered with melted cheddar & American cheese, crispy beef bacon and secret sauce with fries.", ["halal"],
             {"ru": {"name": "Бургер с говядиной, беконом и сыром", "desc": "Котлета из говядины ангус с расплавленным чеддером и американским сыром, хрустящий говяжий бекон и секретный соус, подаётся с картофелем фри."}}),
            ("Korean Crispy Fried Chicken Burger", 32, "Crispy fried chicken with jalapeno, cabbage slaw, in sriracha aioli with fries.", ["halal", "spicy"],
             {"ru": {"name": "Бургер с хрустящей курицей по-корейски", "desc": "Хрустящая жареная курица с халапеньо, капустным слоу в соусе шрирача-айоли, подаётся с картофелем фри."}}),
            ("Chicken Shawarma", 18, "Shawarma marinated chicken, cucumber pickle, fries, lettuce, garlic sauce in margoog bread served with fries.", ["halal", "spicy"],
             {"ru": {"name": "Куриная шаурма", "desc": "Курица, маринованная для шаурмы, маринованный огурец, картофель фри, салат латук, чесночный соус в лепёшке маргук, подаётся с картофелем фри."}}),
            ("Honey Mustard Chicken Sandwich", 30, "Grilled chicken breast, bacon, cheddar cheese, honey mustard sauce, fries.", ["halal"],
             {"ru": {"name": "Сэндвич с курицей в медово-горчичном соусе", "desc": "Куриная грудка гриль, бекон, сыр чеддер, медово-горчичный соус, картофель фри."}}),
            ("Felafel Wrap", 19, "Falafel, lettuce, cucumber pickle with tahina sauce in margoog bread served with fries.", ["halal", "vegetarian"],
             {"ru": {"name": "Ролл с фалафелем", "desc": "Фалафель, салат латук, маринованный огурец с соусом тахини в лепёшке маргук, подаётся с картофелем фри."}}),
            ("Tuna Sandwich", 20, "Tuna, tomato, cucumber, in toast bread with fries.", ["halal", "seafood"],
             {"ru": {"name": "Сэндвич с тунцом", "desc": "Тунец, томат, огурец в тостовом хлебе с картофелем фри."}}),
        ]),
        ("Pizza", [
            ("Chicken Fajita Pizza", 35, "Tomato sauce, spiced chicken, cheese, bell pepper, jalapeno, fajita sauce.", ["halal", "spicy"],
             {"ru": {"name": "Пицца с курицей фахита", "desc": "Томатный соус, острая курица, сыр, болгарский перец, халапеньо, соус фахита."}}),
            ("Dynamite Chicken Pizza", 33, "Shredded chicken, mozzarella, dynamite sauce.", ["halal", "spicy"],
             {"ru": {"name": "Пицца с курицей динамит", "desc": "Курица, моцарелла, соус динамит."}}),
            ("Marinara Meatballs Pizza", 34, "Minced meat, mozzarella cheese, marinara sauce.", ["halal"],
             {"ru": {"name": "Пицца с фрикадельками маринара", "desc": "Рубленое мясо, сыр моцарелла, соус маринара."}}),
            ("Classic Margarita", 27, "Tomato sauce, mozzarella, basil.", ["halal", "vegetarian"],
             {"ru": {"name": "Классическая Маргарита", "desc": "Томатный соус, моцарелла, базилик."}}),
            ("Peri Peri Chicken Pizza", 32, "Peri peri grilled chicken, mozzarella, tomato sauce, onion, bell pepper.", ["halal", "spicy"],
             {"ru": {"name": "Пицца с курицей пери-пери", "desc": "Курица гриль пери-пери, моцарелла, томатный соус, лук, болгарский перец."}}),
            ("Veg Pizza", 24, "Mozzarella, mushroom, peppers, onion, olives.", ["halal", "vegetarian"],
             {"ru": {"name": "Овощная пицца", "desc": "Моцарелла, грибы, перец, лук, оливки."}}),
            ("Hawaiian Pizza", 32, "Beef pepperoni, mozzarella, pineapple, tomato sauce.", ["halal"],
             {"ru": {"name": "Гавайская пицца", "desc": "Говяжья пепперони, моцарелла, ананас, томатный соус."}}),
            ("Four Cheese Pizza", 34, "Mozzarella, cheddar, akawi, parmesan, tomato sauce.", ["halal", "vegetarian"],
             {"ru": {"name": "Пицца четыре сыра", "desc": "Моцарелла, чеддер, акави, пармезан, томатный соус."}}),
        ]),
        ("Create Your Own Pasta", [
            ("Bistro Shrimp Pasta", 37, "Pan seared shrimp, fresh mushroom, tomato & arugula with spaghetti and a basil garlic lemon cream sauce.", ["halal", "seafood"],
             {"ru": {"name": "Паста с креветками по-бистро", "desc": "Обжаренные креветки, свежие грибы, томат и руккола со спагетти в сливочном соусе с базиликом, чесноком и лимоном."}}),
            ("Pad Thai Noodles", 29, "Veg & chicken option available.", ["halal"],
             {"ru": {"name": "Лапша Пад Тай", "desc": "Доступен вегетарианский вариант или с курицей."}}),
        ]),
        ("Soup", [
            ("Tom Yum Soup", 34, "Classic Thai hot & sour soup.", ["halal", "seafood", "spicy"],
             {"ru": {"name": "Суп Том Ям", "desc": "Классический тайский острый и кислый суп."}}),
            ("Beef Broth Soup", 30, "Slow simmered beef broth.", ["halal"],
             {"ru": {"name": "Бульон из говядины", "desc": "Говяжий бульон долгой варки."}}),
            ("Chicken Corn Soup", 24, "Creamy chicken and sweet corn soup.", ["halal"],
             {"ru": {"name": "Куриный суп с кукурузой", "desc": "Кремовый суп с курицей и сладкой кукурузой."}}),
            ("Texas Chilli Chicken Soup", 27, "Spiced chicken chilli soup.", ["halal", "spicy"],
             {"ru": {"name": "Техасский острый куриный суп", "desc": "Острый куриный суп чили."}}),
            ("Lentil Soup", 24, "Classic Middle Eastern lentil soup.", ["halal", "vegetarian"],
             {"ru": {"name": "Чечевичный суп", "desc": "Классический ближневосточный чечевичный суп."}}),
        ]),
        ("Sides", [
            ("Creamy Spinach", 12, "Sauteed spinach in a light cream sauce.", ["halal", "vegetarian"],
             {"ru": {"name": "Шпинат в сливочном соусе", "desc": "Тушёный шпинат в лёгком сливочном соусе."}}),
            ("Mashed Potato", 10, "Classic buttery mashed potato.", ["halal", "vegetarian"],
             {"ru": {"name": "Картофельное пюре", "desc": "Классическое сливочное картофельное пюре."}}),
            ("Saute Vegetable", 8, "Seasonal vegetables sauteed lightly.", ["halal", "vegetarian"],
             {"ru": {"name": "Овощи соте", "desc": "Сезонные овощи, слегка обжаренные."}}),
            ("French Fries", 10, "Crispy golden fries.", ["halal", "vegetarian"],
             {"ru": {"name": "Картофель фри", "desc": "Хрустящий золотистый картофель фри."}}),
            ("Potato Wedges", 10, "Seasoned potato wedges.", ["halal", "vegetarian"],
             {"ru": {"name": "Картофельные дольки", "desc": "Приправленные картофельные дольки."}}),
            ("Fried Rice", 12, "Classic wok-fried rice.", ["halal", "vegetarian"],
             {"ru": {"name": "Жареный рис", "desc": "Классический рис, жаренный в воке."}}),
            ("Steamed Rice", 8, "Plain steamed rice.", ["halal", "vegetarian"],
             {"ru": {"name": "Рис на пару", "desc": "Простой рис на пару."}}),
        ]),
    ],
    "dessert": [
        ("Dessert Menu", [
            ("Vanilla Cream Brulee", 17, "Classic vanilla custard with a caramelized sugar crust.", ["halal", "vegetarian"],
             {"ru": {"name": "Ванильный крем-брюле", "desc": "Классический ванильный крем с карамелизированной сахарной корочкой."}}),
            ("Apple Pie", 18, "Warm spiced apple pie.", ["halal", "vegetarian"],
             {"ru": {"name": "Яблочный пирог", "desc": "Тёплый пряный яблочный пирог."}}),
            ("Chocolate Brownies", 16, "Rich chocolate brownie squares.", ["halal", "vegetarian"],
             {"ru": {"name": "Шоколадные брауни", "desc": "Насыщенные шоколадные квадратики брауни."}}),
            ("Red Velvet Cheese Cake", 20, "Red velvet cheesecake with cream cheese frosting.", ["halal", "vegetarian"],
             {"ru": {"name": "Чизкейк «Красный бархат»", "desc": "Чизкейк красный бархат со сливочно-сырной глазурью."}}),
            ("Blueberry Cobbler Cake", 20, "Warm blueberry cobbler cake.", ["halal", "vegetarian"],
             {"ru": {"name": "Пирог-коблер с черникой", "desc": "Тёплый черничный пирог коблер."}}),
            ("Panna Cotta", 20, "Silky Italian cream dessert.", ["halal", "vegetarian"],
             {"ru": {"name": "Панна-котта", "desc": "Нежный итальянский сливочный десерт."}}),
            ("Ice Cream", 10, "Choice of classic flavors.", ["halal", "vegetarian"],
             {"ru": {"name": "Мороженое", "desc": "На выбор из классических вкусов."}}),
            ("Crepe", 20, "Choice of Nutella, pistachio or caramel filling.", ["halal", "vegetarian"],
             {"ru": {"name": "Крепы", "desc": "На выбор начинка: нутелла, фисташка или карамель."}}),
            ("Your Choice of Pancake", 18, "Choice of Nutella, honey or caramel topping.", ["halal", "vegetarian"],
             {"ru": {"name": "Панкейки на выбор", "desc": "На выбор топпинг: нутелла, мёд или карамель."}}),
        ]),
    ],
    "beverages": [
        ("Frappe & Coffee", [
            ("Mocha Frappe", 22, "Blended coffee with chocolate.", ["halal", "vegetarian"],
             {"ru": {"name": "Фраппе мокко", "desc": "Взбитый кофе с шоколадом."}}),
            ("Caramel Frappe", 22, "Blended coffee with caramel.", ["halal", "vegetarian"],
             {"ru": {"name": "Карамельный фраппе", "desc": "Взбитый кофе с карамелью."}}),
            ("Vanilla Frappe", 22, "Blended coffee with vanilla.", ["halal", "vegetarian"],
             {"ru": {"name": "Ванильный фраппе", "desc": "Взбитый кофе с ванилью."}}),
            ("Cold Coffee", 22, "Chilled iced coffee.", ["halal", "vegetarian"],
             {"ru": {"name": "Холодный кофе", "desc": "Охлаждённый кофе со льдом."}}),
            ("Cappuccino", 14, "Espresso with steamed milk foam.", ["halal", "vegetarian"],
             {"ru": {"name": "Капучино", "desc": "Эспрессо с взбитой молочной пенкой."}}),
            ("American Coffee", 10, "Classic filtered black coffee.", ["halal", "vegetarian"],
             {"ru": {"name": "Американо", "desc": "Классический фильтрованный чёрный кофе."}}),
            ("Hot Chocolate", 16, "Rich hot chocolate.", ["halal", "vegetarian"],
             {"ru": {"name": "Горячий шоколад", "desc": "Насыщенный горячий шоколад."}}),
            ("Cafe Late", 14, "Espresso with steamed milk.", ["halal", "vegetarian"],
             {"ru": {"name": "Кафе латте", "desc": "Эспрессо с горячим молоком."}}),
            ("Espresso", 6, "Single shot of espresso.", ["halal", "vegetarian"],
             {"ru": {"name": "Эспрессо", "desc": "Одна порция эспрессо."}}),
            ("Tea", 5, "Classic brewed tea.", ["halal", "vegetarian"],
             {"ru": {"name": "Чай", "desc": "Классический заваренный чай."}}),
        ]),
        ("Fresh Juice", [
            ("Pinacolada", 18, "Pineapple and coconut blend, non-alcoholic.", ["halal", "vegetarian"],
             {"ru": {"name": "Пина колада", "desc": "Смесь ананаса и кокоса, безалкогольная."}}),
            ("Fresh Orange Juice", 18, "Freshly squeezed orange juice.", ["halal", "vegetarian"],
             {"ru": {"name": "Свежевыжатый апельсиновый сок", "desc": "Свежевыжатый апельсиновый сок."}}),
            ("Fresh Cocktail Juice", 18, "Mixed fresh fruit blend.", ["halal", "vegetarian"],
             {"ru": {"name": "Свежий фруктовый коктейль", "desc": "Смесь свежих фруктов."}}),
            ("Lemon with Mint", 16, "Fresh lemon mint juice.", ["halal", "vegetarian"],
             {"ru": {"name": "Лимон с мятой", "desc": "Свежий сок лимона с мятой."}}),
            ("Pineapple with Ginger", 20, "Pineapple juice with fresh ginger.", ["halal", "vegetarian"],
             {"ru": {"name": "Ананас с имбирём", "desc": "Ананасовый сок со свежим имбирём."}}),
            ("Mango Mania", 23, "Fresh mango blend.", ["halal", "vegetarian"],
             {"ru": {"name": "Манго Мания", "desc": "Смесь свежего манго."}}),
        ]),
        ("Smoothies", [
            ("Banana Oats Smoothie", 25, "Banana and oats blended smoothie.", ["halal", "vegetarian"],
             {"ru": {"name": "Смузи банан-овсянка", "desc": "Смузи из банана и овсянки."}}),
            ("Avocado Smoothie", 24, "Creamy avocado smoothie.", ["halal", "vegetarian"],
             {"ru": {"name": "Смузи из авокадо", "desc": "Кремовый смузи из авокадо."}}),
            ("Mango & Almond Smoothie", 25, "Mango and almond blended smoothie.", ["halal", "vegetarian"],
             {"ru": {"name": "Смузи манго-миндаль", "desc": "Смузи из манго и миндаля."}}),
            ("Watermelon Smoothie", 24, "Fresh watermelon smoothie.", ["halal", "vegetarian"],
             {"ru": {"name": "Смузи из арбуза", "desc": "Освежающий смузи из арбуза."}}),
            ("Milkshake", 24, "Classic milkshake.", ["halal", "vegetarian"],
             {"ru": {"name": "Молочный коктейль", "desc": "Классический молочный коктейль."}}),
        ]),
        ("Mojitos", [
            ("Classic Mojito", 19, "Non-alcoholic mint lime mojito.", ["halal", "vegetarian"],
             {"ru": {"name": "Классический мохито", "desc": "Безалкогольный мохито с мятой и лаймом."}}),
            ("Mix Berries Mojito", 22, "Non-alcoholic mixed berry mojito.", ["halal", "vegetarian"],
             {"ru": {"name": "Мохито с ягодами", "desc": "Безалкогольный мохито с ягодным миксом."}}),
            ("Strawberry Mojito", 20, "Non-alcoholic strawberry mojito.", ["halal", "vegetarian"],
             {"ru": {"name": "Клубничный мохито", "desc": "Безалкогольный мохито с клубникой."}}),
            ("Blueberry Mojito", 20, "Non-alcoholic blueberry mojito.", ["halal", "vegetarian"],
             {"ru": {"name": "Черничный мохито", "desc": "Безалкогольный мохито с черникой."}}),
            ("Ice Tea", 17, "Chilled iced tea.", ["halal", "vegetarian"],
             {"ru": {"name": "Холодный чай", "desc": "Охлаждённый чай со льдом."}}),
        ]),
        ("Soft Drinks", [
            ("Coke / 7Up / Pepsi / Diet", 4, "Choice of soft drink.", ["halal", "vegetarian"],
             {"ru": {"name": "Кола / 7Up / Пепси / Диет", "desc": "На выбор безалкогольный напиток."}}),
            ("Perrier Small", 6, "Sparkling water, small bottle.", ["halal", "vegetarian"],
             {"ru": {"name": "Перье, маленькая", "desc": "Газированная вода, маленькая бутылка."}}),
            ("Perrier Medium", 10, "Sparkling water, medium bottle.", ["halal", "vegetarian"],
             {"ru": {"name": "Перье, средняя", "desc": "Газированная вода, средняя бутылка."}}),
            ("Perrier Large", 15, "Sparkling water, large bottle.", ["halal", "vegetarian"],
             {"ru": {"name": "Перье, большая", "desc": "Газированная вода, большая бутылка."}}),
            ("Small Water", 2, "Bottled still water, small.", ["halal", "vegetarian"],
             {"ru": {"name": "Вода, маленькая", "desc": "Негазированная вода в бутылке, маленькая."}}),
            ("Large Water", 5, "Bottled still water, large.", ["halal", "vegetarian"],
             {"ru": {"name": "Вода, большая", "desc": "Негазированная вода в бутылке, большая."}}),
            ("Soda", 5, "Club soda.", ["halal", "vegetarian"],
             {"ru": {"name": "Содовая", "desc": "Клубная содовая."}}),
            ("Beer (Non-Alcoholic)", 10, "Non-alcoholic malt beverage.", ["halal", "vegetarian"],
             {"ru": {"name": "Пиво (безалкогольное)", "desc": "Безалкогольный солодовый напиток."}}),
            ("Tonic Water Small", 10, "Tonic water, small bottle.", ["halal", "vegetarian"],
             {"ru": {"name": "Тоник, маленький", "desc": "Тоник, маленькая бутылка."}}),
            ("Tonic Water Large", 15, "Tonic water, large bottle.", ["halal", "vegetarian"],
             {"ru": {"name": "Тоник, большой", "desc": "Тоник, большая бутылка."}}),
        ]),
    ],
}

# Fixed "chrome" text -- not per-dish, but small, stable UI vocabulary.
# Keyed by the English label used in DATA / the HTML template so it stays
# obviously matched to what it translates. Add "ar": {...} keys later.

TAB_I18N = {
    "food":       {"en": "Food",       "ru": "Еда"},
    "dessert":    {"en": "Dessert",    "ru": "Десерт"},
    "beverages":  {"en": "Beverages",  "ru": "Напитки"},
}

SUBCAT_I18N = {
    "Breakfast":              {"ru": "Завтрак"},
    "Salad":                  {"ru": "Салаты"},
    "Main Course":             {"ru": "Основные блюда"},
    "Appetizer":               {"ru": "Закуски"},
    "Sandwiches":              {"ru": "Сэндвичи"},
    "Pizza":                   {"ru": "Пицца"},
    "Create Your Own Pasta":   {"ru": "Паста на выбор"},
    "Soup":                    {"ru": "Супы"},
    "Sides":                   {"ru": "Гарниры"},
    "Dessert Menu":            {"ru": "Десерты"},
    "Frappe & Coffee":         {"ru": "Фраппе и кофе"},
    "Fresh Juice":             {"ru": "Свежевыжатые соки"},
    "Smoothies":               {"ru": "Смузи"},
    "Mojitos":                 {"ru": "Мохито"},
    "Soft Drinks":             {"ru": "Безалкогольные напитки"},
}

TAG_I18N = {
    "halal":       {"en": "Halal",       "ru": "Халяль"},
    "vegetarian":  {"en": "Vegetarian",  "ru": "Вегетарианское"},
    "seafood":     {"en": "Seafood",     "ru": "Морепродукты"},
    "spicy":       {"en": "Spicy",       "ru": "Острое"},
}

# Static header/footer/hint strings (data-i18n="<key>" in the HTML template).
UI_I18N = {
    "brandName": {
        "ru": "Ресторан Seder Palms",
    },
    "welcome": {
        "ru": "Свежие современные блюда в Seder Palms",
    },
    "filterHint": {
        "ru": "Нажмите один раз, чтобы показать только это, ещё раз — чтобы скрыть, и снова — чтобы сбросить",
    },
    "noResults": {
        "ru": "Нет блюд, соответствующих выбранным фильтрам. Попробуйте сбросить фильтр выше.",
    },
    "footer": {
        "ru": "Цены указаны без НДС · Visa · MasterCard · mada",
    },
    "photoPending": {
        "ru": "ФОТО СКОРО",
    },
}

TAB_LABELS = {k: v["en"] for k, v in TAB_I18N.items()}


def render_item(item):
    name, price, desc, tags = item[0], item[1], item[2], item[3]
    i18n = item[4] if len(item) > 4 else {}
    slug = slugify(name)
    esc_name = html_lib.escape(name)
    esc_desc = html_lib.escape(desc)
    visible_tags = "".join(
        f'<span class="tag{" spicy" if t=="spicy" else ""}{" veg" if t=="vegetarian" else ""}" data-i18n-tag="{t}">{html_lib.escape(TAG_I18N[t]["en"])}</span>'
        for t in tags
    )
    data_tags = " ".join(tags)
    return f'''    <div class="item-card" data-tags="{data_tags}" data-slug="{slug}">
      <div class="item-photo placeholder" data-slug="{slug}">
        <img src="photos/{slug}.jpg" alt="{esc_name}" loading="lazy" decoding="async" width="84" height="84"
             onerror="this.parentElement.classList.add('placeholder'); this.style.display='none';"
             onload="this.parentElement.classList.remove('placeholder');">
        <span class="ph-label" data-i18n="photoPending">PHOTO PENDING</span>
      </div>
      <div class="item-body">
        <div class="item-top">
          <div class="item-name">{esc_name}</div>
          <div class="item-price">
            <div class="price-sar">{price} SAR</div>
            <div class="price-usd">&asymp; ${usd(price)}</div>
          </div>
        </div>
        <div class="item-desc">{esc_desc}</div>
        <div class="tags">{visible_tags}</div>
      </div>
    </div>
''', slug, i18n

def render_subcategory(title, items):
    esc_title = html_lib.escape(title)
    out = f'    <h2 class="category-title" data-i18n-cat="{esc_title}">{esc_title}</h2>\n'
    item_i18n = {}
    for item in items:
        item_html, slug, i18n = render_item(item)
        out += item_html
        if i18n:
            item_i18n[slug] = i18n
    return out, item_i18n

def render_tab(tab_key):
    out = f'  <section class="category-block" id="{tab_key}">\n'
    all_item_i18n = {}
    for subcat_title, items in DATA[tab_key]:
        sub_html, sub_i18n = render_subcategory(subcat_title, items)
        out += sub_html
        all_item_i18n.update(sub_i18n)
    out += '    <div class="no-results" data-i18n="noResults">No dishes match your current filters. Try resetting a filter above.</div>\n'
    out += '  </section>\n'
    return out, all_item_i18n

def build_main_html():
    all_item_i18n = {}
    tabs_html = []
    for k in ["food", "dessert", "beverages"]:
        tab_html, tab_item_i18n = render_tab(k)
        tabs_html.append(tab_html)
        all_item_i18n.update(tab_item_i18n)
    return "\n".join(tabs_html), all_item_i18n

def build_i18n_js(item_i18n):
    langs = ["ru"]  # add "ar" here once Arabic copy is filled in above

    translations = {}
    for lang in langs:
        table = {key: entry[lang] for key, entry in UI_I18N.items() if lang in entry}
        if table:
            translations[lang] = table

    cat_translations = {}
    for lang in langs:
        table = {key: entry[lang] for key, entry in SUBCAT_I18N.items() if lang in entry}
        if table:
            cat_translations[lang] = table

    tab_translations = {}
    for lang in langs:
        table = {key: entry[lang] for key, entry in TAB_I18N.items() if lang in entry and lang != "en"}
        if table:
            tab_translations[lang] = table

    tag_translations = {}
    for lang in langs:
        table = {key: entry[lang] for key, entry in TAG_I18N.items() if lang in entry and lang != "en"}
        if table:
            tag_translations[lang] = table

    item_translations = {}
    for slug, entry in item_i18n.items():
        langs_for_item = {}
        for lang in langs:
            if lang in entry:
                langs_for_item[lang] = entry[lang]
        if langs_for_item:
            item_translations[slug] = langs_for_item

    def dump(obj):
        return json.dumps(obj, ensure_ascii=False, indent=2)

    return (
        f"  const translations = {dump(translations)};\n"
        f"  const catTranslations = {dump(cat_translations)};\n"
        f"  const tabTranslations = {dump(tab_translations)};\n"
        f"  const tagTranslations = {dump(tag_translations)};\n"
        f"  const itemTranslations = {dump(item_translations)};\n"
    )

def splice_into_html(main_html, i18n_js):
    html_text = MENU_HTML_PATH.read_text(encoding="utf-8")

    main_start = html_text.index("<main>") + len("<main>")
    main_end = html_text.index("</main>")
    html_text = html_text[:main_start] + "\n" + main_html + html_text[main_end:]

    start_marker = "// === I18N DATA START (auto-generated by generate_menu.py -- do not hand-edit below) ==="
    end_marker = "// === I18N DATA END ==="
    start_idx = html_text.index(start_marker) + len(start_marker)
    end_idx = html_text.index(end_marker)
    html_text = html_text[:start_idx] + "\n" + i18n_js + "  " + html_text[end_idx:]

    MENU_HTML_PATH.write_text(html_text, encoding="utf-8")

def build_photo_manifest():
    manifest_lines = ["SEDER PALMS RESTAURANT — PHOTO NAMING GUIDE", "=" * 50, "",
                       "Save every photo as a .jpg file using the exact filename below.",
                       "Drop all files into a folder named 'photos' next to the menu HTML file.",
                       "Filenames are case-sensitive and must match exactly.", ""]
    total_items = 0
    for tab_key in ["food", "dessert", "beverages"]:
        manifest_lines.append(f"\n[{TAB_LABELS[tab_key].upper()}]")
        for subcat_title, items in DATA[tab_key]:
            manifest_lines.append(f"\n  {subcat_title}:")
            for item in items:
                name = item[0]
                slug = slugify(name)
                manifest_lines.append(f"    {name}  ->  photos/{slug}.jpg")
                total_items += 1
    manifest_lines.append(f"\n\nTotal photos needed: {total_items}")
    (BASE_DIR / "photo-naming-guide.txt").write_text("\n".join(manifest_lines), encoding="utf-8")
    return total_items


if __name__ == "__main__":
    main_html, item_i18n = build_main_html()
    i18n_js = build_i18n_js(item_i18n)
    splice_into_html(main_html, i18n_js)
    total_items = build_photo_manifest()
    print(f"Generated {total_items} items.")
    print(f"Updated: {MENU_HTML_PATH.name}")
    print("Updated: photo-naming-guide.txt")
