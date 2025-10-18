import sqlite3
conn = sqlite3.connect('restaurant.db')
cursor = conn.cursor()
cursor.execute("DELETE FROM menu_items")

menu_data = [
    ("Masala Dosa", 60, "masala_dosa.webp", "A crispy rice crepe filled with spiced potato masala.", "Veg", "Breakfast"),
    ("Idli Sambar", 40, "idly.webp", "Soft steamed rice cakes served with hot sambar and chutney.", "Veg", "Breakfast"),
    ("Pongal & Vada", 50, "pongal_vada.webp", "Comforting South Indian breakfast served with chutney and sambar.", "Veg", "Breakfast"),
    ("Chapathi & Kurma", 80, "chapathi.webp", "Soft chapathis served with delicious mixed-veg kurma.", "Veg", "Breakfast"),
    ("Poori Masala", 70, "poori.webp", "Fluffy pooris served with spiced potato masala.", "Veg", "Breakfast"),
    ("Upma", 45, "upma.webp", "Savory semolina porridge with vegetables and ghee.", "Veg", "Breakfast"),
    ("Bread Omelette", 50, "bread_egg.webp", "Toasted bread layered with a fluffy spiced omelette.", "Non-Veg", "Breakfast"),
    ("Curd Rice", 70, "curd_rice.webp", "Refreshing curd mixed with rice and seasoned with mustard and curry leaves.", "Veg", "Breakfast"),
    ("Sweet Lassi", 60, "lassi.webp", "Thick yogurt drink flavored with sugar and cardamom.", "Veg", "Breakfast"),
    ("Filter Coffee", 30, "coffee.webp", "Traditional South Indian coffee brewed to perfection.", "Veg", "Breakfast"),
    ("Veg Fried Rice", 120, "veg_rice.webp", "Aromatic rice stir-fried with fresh vegetables and soy sauce.", "Veg", "Lunch"),
    ("Veg Pulao", 110, "veg_pulao.webp", "Fragrant rice cooked with fresh vegetables and mild spices.", "Veg", "Lunch"),
    ("Chicken Biriyani", 180, "biriyani.webp", "Fragrant basmati rice layered with spicy chicken masala.", "Non-Veg", "Lunch"),
    ("Mutton Curry", 200, "mutton_curry.webp", "Tender mutton pieces cooked in traditional spicy gravy.", "Non-Veg", "Lunch"),
    ("Fish Fry", 170, "fish_fry.webp", "Crispy fried fish marinated with South Indian spices.", "Non-Veg", "Lunch"),
    ("Egg Curry", 100, "egg_curry.webp", "Boiled eggs cooked in flavorful onion-tomato gravy.", "Non-Veg", "Lunch"),
    ("Prawn Curry", 210, "prawn_curry.webp", "Fresh prawns cooked in coconut-based spicy gravy.", "Non-Veg", "Lunch"),
    ("Aloo Gobi", 100, "aloo.webp", "Potatoes and cauliflower cooked with aromatic spices.", "Veg", "Lunch"),
    ("Butter Naan", 50, "naan.webp", "Soft tandoor-baked naan brushed with butter.", "Veg", "Lunch"),
    ("Paneer Butter Masala", 150, "panner_masala.webp", "Creamy paneer cubes simmered in a rich tomato gravy.", "Veg", "Lunch"),
    ("Parotta & Chicken Gravy", 130, "poratta.webp", "Flaky layered parotta served with spicy chicken gravy.", "Non-Veg", "Dinner"),
    ("Grilled Chicken", 200, "grilled_chicken.webp", "Juicy grilled chicken marinated in Indian herbs and spices.", "Non-Veg", "Dinner"),
    ("Chicken 65", 150, "chicken_65.webp", "Crispy fried chicken pieces with spicy seasoning.", "Non-Veg", "Dinner"),
    ("Gobi Manchurian", 130, "gobi_manchu.webp", "Crispy cauliflower tossed in tangy Indo-Chinese sauce.", "Veg", "Dinner"),
    ("Mushroom Masala", 140, "mushroom_masala.webp", "Mushrooms simmered in spicy onion-tomato gravy.", "Veg", "Dinner"),
    ("Paneer Tikka", 160, "panner_tikka.webp", "Grilled paneer cubes marinated in yogurt and spices.", "Veg", "Dinner"),
    ("Veg Noodles", 120, "veg_noodles.webp", "Stir-fried noodles loaded with fresh vegetables.", "Veg", "Dinner"),
    ("Chicken Fried Rice", 150, "chicken_rice.webp", "Rice stir-fried with egg, chicken, and flavorful sauces.", "Non-Veg", "Dinner"),
    ("Egg Kothu Parotta", 130, "egg_kothu.webp", "Shredded parotta mixed with egg and spicy masala.", "Non-Veg", "Dinner"),
    ("Falooda", 90, "falooda.webp", "Refreshing dessert drink with vermicelli, jelly, and ice cream.", "Veg", "Dinner")
]

cursor.executemany("INSERT INTO menu_items (name, price, image, description, type, category) VALUES (?, ?, ?, ?, ?, ?)", menu_data)
conn.commit()
conn.close()
