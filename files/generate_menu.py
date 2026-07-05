import re
import html as html_lib

SAR_TO_USD = 1 / 3.75

def slugify(name):
    s = name.lower()
    s = s.replace("&", "and")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s

def usd(sar):
    return f"{sar * SAR_TO_USD:.2f}"

# (name, price_sar, description, tags)
DATA = {
    "food": [
        ("Breakfast", [
            ("American Steak Breakfast", 47, "Steak, over easy egg, mushroom, grill tomato, roasted potato, toast bread, coffee.", ["halal"]),
            ("English Breakfast Platter", 37, "Fried egg, grilled hot dog, saute mushroom, baked beans, bacon, grilled tomato, toast, coffee.", ["halal"]),
            ("Hash Brown Egg Benedict", 36, "Crispy hash brown eggs benedict, hollandaise sauce and sriracha mayo.", ["halal", "vegetarian", "spicy"]),
            ("Avocado Toast With Poached Egg", 38, "Guacamole in multigrain bread served with poached egg and horseradish sauce.", ["halal", "vegetarian"]),
            ("Your Choice Omelette", 20, "Vegetable or cheese omelette, served with hash brown or toast bread.", ["halal", "vegetarian"]),
            ("Philly Steak Omelette", 24, "Egg, steak, mozzarella cheese, bell peppers & onion.", ["halal"]),
            ("Egg Any Style", 20, "Eggs cooked any style, served with hash brown, salsa and toast.", ["halal", "vegetarian"]),
            ("Egg N Bun", 24, "Two fried eggs in a brioche bun with caramelized onion, beef bacon, cheese and our special sauce, served with fries.", ["halal"]),
            ("Chicken Schnitzel", 27, "Fried chicken, fries, sunny side up egg, hollandaise sauce.", ["halal"]),
            ("Shakshuka Slider", 27, "Our homemade shakshuka with feta cheese served in warm mini brioche buns.", ["halal", "vegetarian", "spicy"]),
        ]),
        ("Salad", [
            ("Crispy Quinoa Salad", 37, "Crispy corn salad with feta, pomegranate, bell pepper, edamame, cherry tomato, spring onion and honey mustard vinaigrette.", ["halal", "vegetarian"]),
            ("Cobb Salmon Salad", 42, "Grilled salmon cubes, avocado, blue cheese, bacon, tomato, egg & mixed greens tossed in our vinaigrette.", ["halal", "seafood"]),
            ("Signature Steak Salad", 36, "Arugula leaves, warm potato salad, steak slices, edamame, parmesan cheese, balsamic reduction.", ["halal"]),
            ("The Greek Salad", 29, "Lettuce, feta cheese, cucumber, olives, tomato, white onion, oregano vinaigrette.", ["halal", "vegetarian"]),
            ("Falafel Salad", 22, "Falafel, iceberg, cucumber, tomato, cucumber pickle, parsley, fries, tahina sauce.", ["halal", "vegetarian"]),
            ("Shrimp Cocktail Avocado Salad", 40, "Avocado salsa with de-shelled prawns drizzled with cocktail sauce.", ["halal", "seafood"]),
            ("Classic Waldorf Salad", 28, "Apple slices, celery, yogurt, English mustard, lemon juice, grapes, cranberries, baby greens & romaine, candied walnuts.", ["halal", "vegetarian"]),
            ("Exotic Rocca Salad", 25, "Rocca leaves, sundried tomato, grilled halloumi, parmesan served with pomegranate dressing.", ["halal", "vegetarian"]),
            ("Fattoush Salad", 20, "A healthy mix of fresh vegetables with toasted bread and pomegranate molasses.", ["halal", "vegetarian"]),
            ("Caesar Chicken Salad", 26, "Grilled chicken, lettuce with Caesar dressing and parmesan.", ["halal"]),
            ("Hummus", 14, "A smooth, creamy blend of chick peas, tahini, garlic, lemon & olive oil served with pita bread.", ["halal", "vegetarian"]),
        ]),
        ("Main Course", [
            ("Grilled Chicken Breast", 45, "Plain grilled chicken breast served with mash potato and vegetable.", ["halal"]),
            ("Chicken Parmigiana", 37, "Breaded chicken breast topped with parmesan, turkey ham and marinara sauce with mash potato & veg.", ["halal"]),
            ("Chicken Marsala & Mushrooms", 36, "Thinly sliced chicken breast sauteed with shitake, porcini mushroom in a cream sauce, served with mash potato & steamed veg.", ["halal"]),
            ("Crispy Honey Lemon Chicken", 35, "Crispy fried chicken in honey lemon sauce served with steamed rice.", ["halal"]),
            ("Country Fried Chicken", 39, "Fried chicken breast, gravy sauce, mash potato, green beans.", ["halal"]),
            ("Chilli Chicken", 39, "Fried chicken cubes with bell peppers and Chinese sauce served with steamed rice or noodles.", ["halal", "spicy"]),
            ("Steak Tenderloin", 50, "Tenderloin fillet in mushroom sauce served with mash potato & veg.", ["halal"]),
            ("Beef Roulade", 54, "Beef stuffed with spinach & cheese served with mash potato & veg.", ["halal"]),
            ("Mongolian Beef", 37, "Thin slices of caramelized beef in a balanced sauce tossed with green onions, served with steamed rice.", ["halal"]),
            ("Grilled Lamb Chops", 62, "Lamb chops served with roasted potatoes and tzatziki sauce.", ["halal"]),
            ("Rib Eye Steak", 90, "Rib eye steak rubbed & seasoned with fresh Italian herbs & fresh peppercorn sauce, served with mash potato and vegetable.", ["halal"]),
            ("Smoked Ribs", 68, "Short ribs with pure honey & BBQ sauce served with potato salad.", ["halal"]),
            ("Braised Lamb Shank", 76, "Lamb shank in burgundy sauce served with mash potato.", ["halal"]),
            ("Beef Stroganoff", 38, "Beef thin slices in creamy mushroom sauce served with steamed rice.", ["halal"]),
            ("Arabic Mixed Grill", 36, "Awsal, kabab, shishtawook served with hummus, garlic sauce, fries & bread.", ["halal"]),
            ("Peri Peri Chicken", 37, "Peri peri marinated chicken thigh served with nan bread, fries & garlic sauce.", ["halal", "spicy"]),
            ("Grilled Rosemary Salmon", 50, "Grilled salmon on a bed of steamed fresh spinach served with mash potato.", ["halal", "seafood"]),
            ("Tepanyaki Salmon", 52, "Tepanyaki marinated salmon fillet served with garlic mashed potato and saute spinach.", ["halal", "seafood"]),
            ("Lobster Thermidor", 94, "Lobster tails served with lemon butter sauce, mash potato & veg.", ["halal", "seafood"]),
            ("Fish & Chips", 31, "Battered fish fillet served with mushy peas, coleslaw, tartar sauce.", ["halal", "seafood"]),
            ("Grilled Seafood Platter", 66, "Grilled shrimp, salmon, hamour, mussels & calamari served with saute veg & lemon butter sauce.", ["halal", "seafood"]),
            ("Sriracha Grilled Shrimp", 53, "Shrimp with sriracha sauce served with cilantro rice.", ["halal", "seafood", "spicy"]),
            ("Nasi Goreng", 46, "Beef or chicken in goreng rice, cracker, over easy egg, peanut butter gravy.", ["halal"]),
            ("Butter Chicken", 33, "Traditional instant pot butter chicken masala served with ghee rice.", ["halal"]),
            ("Tandoor Chicken Biryani", 34, "Tandoor marinated chicken biryani served with pickle, papad & raitha.", ["halal", "spicy"]),
            ("Kadai Masala", 33, "Chicken or beef marinated in kadai masala served with ghee rice.", ["halal", "spicy"]),
            ("Thai Red Curry", 33, "Chicken or beef in red coconut curry sauce served with steam rice.", ["halal", "spicy"]),
        ]),
        ("Appetizer", [
            ("Dynamite Shrimp", 40, "Fried shrimp served with homemade dynamite sauce.", ["halal", "seafood", "spicy"]),
            ("Nachos", 31, "Tortilla chips, guacamole, chili con carne, sour cream, jalapeno, olives, mozzarella cheese, salsa.", ["halal", "spicy"]),
            ("Jalapeno Chicken Wings", 30, "Crispy chicken wings coated with homemade jalapeno sauce.", ["halal", "spicy"]),
            ("French Dip Slider", 32, "Beef, lettuce, cheddar cheese, slider sauce, caramelized onions.", ["halal"]),
            ("Homemade Chicken Nuggets", 21, "Freshly made chicken fillet served with French fries.", ["halal"]),
            ("Bacon Wrapped Steak Bites", 32, "Minced beef stuffed with Emmental cheese wrapped with bacon and BBQ glaze.", ["halal"]),
            ("Buffalo Popcorn Chicken", 30, "Small bites of crispy deep fried chicken with spicy buffalo sauce, garnished with spring onion.", ["halal", "spicy"]),
        ]),
        ("Sandwiches", [
            ("Pulled Smoked Beef Sandwich", 39, "Pulled beef, caramelized onion, Emmental cheese, multigrain bed, served with potato wedges and coleslaw.", ["halal"]),
            ("Chicken Avocado Panini Sandwich", 33, "Sandwich in panini bread stuffed with avocado, chicken and chef's sauce.", ["halal"]),
            ("Quesadilla", 33, "Tortilla filled with chicken, melted cheese, chilies, served with guacamole, salsa & sour cream with fries.", ["halal", "spicy"]),
            ("Beef Tenderloin Steak Sandwich", 36, "Beef tenderloin steak sandwich with sauteed onion, mushroom, melted cheese, garlic mustard mayo and smoked jalapeno sauce with fries.", ["halal", "spicy"]),
            ("Classic Club Sandwich", 30, "Chicken salad, bacon, fried egg, tomato, lettuce, cheese & fries.", ["halal"]),
            ("Bacon Cheese Beef Burger", 35, "Angus beef patty covered with melted cheddar & American cheese, crispy beef bacon and secret sauce with fries.", ["halal"]),
            ("Korean Crispy Fried Chicken Burger", 32, "Crispy fried chicken with jalapeno, cabbage slaw, in sriracha aioli with fries.", ["halal", "spicy"]),
            ("Chicken Shawarma", 18, "Shawarma marinated chicken, cucumber pickle, fries, lettuce, garlic sauce in margoog bread served with fries.", ["halal", "spicy"]),
            ("Honey Mustard Chicken Sandwich", 30, "Grilled chicken breast, bacon, cheddar cheese, honey mustard sauce, fries.", ["halal"]),
            ("Felafel Wrap", 19, "Falafel, lettuce, cucumber pickle with tahina sauce in margoog bread served with fries.", ["halal", "vegetarian"]),
            ("Tuna Sandwich", 20, "Tuna, tomato, cucumber, in toast bread with fries.", ["halal", "seafood"]),
        ]),
        ("Pizza", [
            ("Chicken Fajita Pizza", 35, "Tomato sauce, spiced chicken, cheese, bell pepper, jalapeno, fajita sauce.", ["halal", "spicy"]),
            ("Dynamite Chicken Pizza", 33, "Shredded chicken, mozzarella, dynamite sauce.", ["halal", "spicy"]),
            ("Marinara Meatballs Pizza", 34, "Minced meat, mozzarella cheese, marinara sauce.", ["halal"]),
            ("Classic Margarita", 27, "Tomato sauce, mozzarella, basil.", ["halal", "vegetarian"]),
            ("Peri Peri Chicken Pizza", 32, "Peri peri grilled chicken, mozzarella, tomato sauce, onion, bell pepper.", ["halal", "spicy"]),
            ("Veg Pizza", 24, "Mozzarella, mushroom, peppers, onion, olives.", ["halal", "vegetarian"]),
            ("Hawaiian Pizza", 32, "Beef pepperoni, mozzarella, pineapple, tomato sauce.", ["halal"]),
            ("Four Cheese Pizza", 34, "Mozzarella, cheddar, akawi, parmesan, tomato sauce.", ["halal", "vegetarian"]),
        ]),
        ("Create Your Own Pasta", [
            ("Bistro Shrimp Pasta", 37, "Pan seared shrimp, fresh mushroom, tomato & arugula with spaghetti and a basil garlic lemon cream sauce.", ["halal", "seafood"]),
            ("Pad Thai Noodles", 29, "Veg & chicken option available.", ["halal"]),
        ]),
        ("Soup", [
            ("Tom Yum Soup", 34, "Classic Thai hot & sour soup.", ["halal", "seafood", "spicy"]),
            ("Beef Broth Soup", 30, "Slow simmered beef broth.", ["halal"]),
            ("Chicken Corn Soup", 24, "Creamy chicken and sweet corn soup.", ["halal"]),
            ("Texas Chilli Chicken Soup", 27, "Spiced chicken chilli soup.", ["halal", "spicy"]),
            ("Lentil Soup", 24, "Classic Middle Eastern lentil soup.", ["halal", "vegetarian"]),
        ]),
        ("Sides", [
            ("Creamy Spinach", 12, "Sauteed spinach in a light cream sauce.", ["halal", "vegetarian"]),
            ("Mashed Potato", 10, "Classic buttery mashed potato.", ["halal", "vegetarian"]),
            ("Saute Vegetable", 8, "Seasonal vegetables sauteed lightly.", ["halal", "vegetarian"]),
            ("French Fries", 10, "Crispy golden fries.", ["halal", "vegetarian"]),
            ("Potato Wedges", 10, "Seasoned potato wedges.", ["halal", "vegetarian"]),
            ("Fried Rice", 12, "Classic wok-fried rice.", ["halal", "vegetarian"]),
            ("Steamed Rice", 8, "Plain steamed rice.", ["halal", "vegetarian"]),
        ]),
    ],
    "dessert": [
        ("Dessert Menu", [
            ("Vanilla Cream Brulee", 17, "Classic vanilla custard with a caramelized sugar crust.", ["halal", "vegetarian"]),
            ("Apple Pie", 18, "Warm spiced apple pie.", ["halal", "vegetarian"]),
            ("Chocolate Brownies", 16, "Rich chocolate brownie squares.", ["halal", "vegetarian"]),
            ("Red Velvet Cheese Cake", 20, "Red velvet cheesecake with cream cheese frosting.", ["halal", "vegetarian"]),
            ("Blueberry Cobbler Cake", 20, "Warm blueberry cobbler cake.", ["halal", "vegetarian"]),
            ("Panna Cotta", 20, "Silky Italian cream dessert.", ["halal", "vegetarian"]),
            ("Ice Cream", 10, "Choice of classic flavors.", ["halal", "vegetarian"]),
            ("Crepe", 20, "Choice of Nutella, pistachio or caramel filling.", ["halal", "vegetarian"]),
            ("Your Choice of Pancake", 18, "Choice of Nutella, honey or caramel topping.", ["halal", "vegetarian"]),
        ]),
    ],
    "beverages": [
        ("Frappe & Coffee", [
            ("Mocha Frappe", 22, "Blended coffee with chocolate.", ["halal", "vegetarian"]),
            ("Caramel Frappe", 22, "Blended coffee with caramel.", ["halal", "vegetarian"]),
            ("Vanilla Frappe", 22, "Blended coffee with vanilla.", ["halal", "vegetarian"]),
            ("Cold Coffee", 22, "Chilled iced coffee.", ["halal", "vegetarian"]),
            ("Cappuccino", 14, "Espresso with steamed milk foam.", ["halal", "vegetarian"]),
            ("American Coffee", 10, "Classic filtered black coffee.", ["halal", "vegetarian"]),
            ("Hot Chocolate", 16, "Rich hot chocolate.", ["halal", "vegetarian"]),
            ("Cafe Late", 14, "Espresso with steamed milk.", ["halal", "vegetarian"]),
            ("Espresso", 6, "Single shot of espresso.", ["halal", "vegetarian"]),
            ("Tea", 5, "Classic brewed tea.", ["halal", "vegetarian"]),
        ]),
        ("Fresh Juice", [
            ("Pinacolada", 18, "Pineapple and coconut blend, non-alcoholic.", ["halal", "vegetarian"]),
            ("Fresh Orange Juice", 18, "Freshly squeezed orange juice.", ["halal", "vegetarian"]),
            ("Fresh Cocktail Juice", 18, "Mixed fresh fruit blend.", ["halal", "vegetarian"]),
            ("Lemon with Mint", 16, "Fresh lemon mint juice.", ["halal", "vegetarian"]),
            ("Pineapple with Ginger", 20, "Pineapple juice with fresh ginger.", ["halal", "vegetarian"]),
            ("Mango Mania", 23, "Fresh mango blend.", ["halal", "vegetarian"]),
        ]),
        ("Smoothies", [
            ("Banana Oats Smoothie", 25, "Banana and oats blended smoothie.", ["halal", "vegetarian"]),
            ("Avocado Smoothie", 24, "Creamy avocado smoothie.", ["halal", "vegetarian"]),
            ("Mango & Almond Smoothie", 25, "Mango and almond blended smoothie.", ["halal", "vegetarian"]),
            ("Watermelon Smoothie", 24, "Fresh watermelon smoothie.", ["halal", "vegetarian"]),
            ("Milkshake", 24, "Classic milkshake.", ["halal", "vegetarian"]),
        ]),
        ("Mojitos", [
            ("Classic Mojito", 19, "Non-alcoholic mint lime mojito.", ["halal", "vegetarian"]),
            ("Mix Berries Mojito", 22, "Non-alcoholic mixed berry mojito.", ["halal", "vegetarian"]),
            ("Strawberry Mojito", 20, "Non-alcoholic strawberry mojito.", ["halal", "vegetarian"]),
            ("Blueberry Mojito", 20, "Non-alcoholic blueberry mojito.", ["halal", "vegetarian"]),
            ("Ice Tea", 17, "Chilled iced tea.", ["halal", "vegetarian"]),
        ]),
        ("Soft Drinks", [
            ("Coke / 7Up / Pepsi / Diet", 4, "Choice of soft drink.", ["halal", "vegetarian"]),
            ("Perrier Small", 6, "Sparkling water, small bottle.", ["halal", "vegetarian"]),
            ("Perrier Medium", 10, "Sparkling water, medium bottle.", ["halal", "vegetarian"]),
            ("Perrier Large", 15, "Sparkling water, large bottle.", ["halal", "vegetarian"]),
            ("Small Water", 2, "Bottled still water, small.", ["halal", "vegetarian"]),
            ("Large Water", 5, "Bottled still water, large.", ["halal", "vegetarian"]),
            ("Soda", 5, "Club soda.", ["halal", "vegetarian"]),
            ("Beer (Non-Alcoholic)", 10, "Non-alcoholic malt beverage.", ["halal", "vegetarian"]),
            ("Tonic Water Small", 10, "Tonic water, small bottle.", ["halal", "vegetarian"]),
            ("Tonic Water Large", 15, "Tonic water, large bottle.", ["halal", "vegetarian"]),
        ]),
    ],
}

TAB_LABELS = {"food": "Food", "dessert": "Dessert", "beverages": "Beverages"}

def render_item(name, price, desc, tags):
    slug = slugify(name)
    esc_name = html_lib.escape(name)
    esc_desc = html_lib.escape(desc)
    tag_labels = {
        "halal": "Halal", "seafood": "Seafood", "vegetarian": "Vegetarian", "spicy": "Spicy"
    }
    visible_tags = "".join(f'<span class="tag{" spicy" if t=="spicy" else ""}{" veg" if t=="vegetarian" else ""}">{tag_labels[t]}</span>' for t in tags)
    data_tags = " ".join(tags)
    return f'''    <div class="item-card" data-tags="{data_tags}">
      <div class="item-photo placeholder" data-slug="{slug}">
        <img src="photos/{slug}.jpg" alt="{esc_name}" loading="lazy" decoding="async" width="84" height="84"
             onerror="this.parentElement.classList.add('placeholder'); this.style.display='none';"
             onload="this.parentElement.classList.remove('placeholder');">
        <span class="ph-label">PHOTO<br>PENDING</span>
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
'''

def render_subcategory(title, items):
    out = f'    <h2 class="category-title">{html_lib.escape(title)}</h2>\n'
    for item in items:
        out += render_item(*item)
    return out

def render_tab(tab_key):
    out = f'  <section class="category-block" id="{tab_key}">\n'
    for subcat_title, items in DATA[tab_key]:
        out += render_subcategory(subcat_title, items)
    out += '    <div class="no-results">No dishes match your current filters. Try resetting a filter above.</div>\n'
    out += '  </section>\n'
    return out

all_tabs_html = "\n".join(render_tab(k) for k in ["food", "dessert", "beverages"])

with open("/home/claude/menu_sections.html", "w", encoding="utf-8") as f:
    f.write(all_tabs_html)

# Build photo naming manifest
manifest_lines = ["SEDER PALMS RESTAURANT — PHOTO NAMING GUIDE", "=" * 50, "",
                   "Save every photo as a .jpg file using the exact filename below.",
                   "Drop all files into a folder named 'photos' next to the menu HTML file.",
                   "Filenames are case-sensitive and must match exactly.", ""]

total_items = 0
for tab_key in ["food", "dessert", "beverages"]:
    manifest_lines.append(f"\n[{TAB_LABELS[tab_key].upper()}]")
    for subcat_title, items in DATA[tab_key]:
        manifest_lines.append(f"\n  {subcat_title}:")
        for name, price, desc, tags in items:
            slug = slugify(name)
            manifest_lines.append(f"    {name}  ->  photos/{slug}.jpg")
            total_items += 1

manifest_lines.append(f"\n\nTotal photos needed: {total_items}")

with open("/home/claude/photo-naming-guide.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(manifest_lines))

print(f"Generated {total_items} items.")
print("Files written: menu_sections.html, photo-naming-guide.txt")
