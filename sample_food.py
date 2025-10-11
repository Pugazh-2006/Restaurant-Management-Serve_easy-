import sqlite3
conn = sqlite3.connect('restaurant.db')
cursor = conn.cursor()
cursor.execute("DELETE FROM menu_items")

menu_data = [
    ("Masala Dosa", 60, "masala_dosa.jpg", "A crispy rice crepe filled with spiced potato masala."),
    ("Paneer Butter Masala", 150, "panner_masala.jpg", "Creamy paneer cubes simmered in a rich tomato gravy."),
    ("Chicken Biryani", 180, "biriyani.jpg", "Fragrant basmati rice layered with spicy chicken masala."),
    ("Idli Sambar", 40, "idly.jpg", "Soft steamed rice cakes served with hot sambar and chutney."),
    ("Veg Fried Rice", 120, "veg_rice.jpg", "Aromatic rice stir-fried with fresh vegetables and soy sauce."),
    ("Gobi Manchurian", 130, "gobi_manchu.jpg", "Crispy cauliflower tossed in tangy Indo-Chinese sauce."),
    ("Mutton Curry", 200, "mutton_curry.jpg", "Tender mutton pieces cooked in traditional spicy gravy."),
    ("Fish Fry", 170, "fish_fry.jpg", "Crispy fried fish marinated with South Indian spices."),
    ("Egg Curry", 100, "egg_curry.jpg", "Boiled eggs cooked in flavorful onion-tomato gravy."),
    ("Chapathi & Kurma", 80, "chapathi.jpg", "Soft chapathis served with delicious mixed-veg kurma."),
    ("Chicken 65", 150, "chicken_65.jpg", "Crispy fried chicken pieces with spicy seasoning."),
    ("Veg Pulao", 110, "veg_pulao.jpg", "Fragrant rice cooked with fresh vegetables and mild spices."),
    ("Mushroom Masala", 140, "mushroom_masala.jpg", "Mushrooms simmered in spicy onion-tomato gravy."),
    ("Parotta & Chicken Gravy", 130, " ", "Flaky layered parotta served with spicy chicken gravy."),
    ("Curd Rice", 70, " ", "Refreshing curd mixed with rice and seasoned with mustard and curry leaves."),
    ("Grilled Chicken", 200, " ", "Juicy grilled chicken marinated in Indian herbs and spices."),
    ("Aloo Gobi", 100, " ", "Potatoes and cauliflower cooked with aromatic spices."),
    ("Butter Naan", 50, " ", "Soft tandoor-baked naan brushed with butter."),
    ("Prawn Curry", 210, " ", "Fresh prawns cooked in coconut-based spicy gravy."),
    ("Sweet Lassi", 60, " ", "Thick yogurt drink flavored with sugar and cardamom.")
]

cursor.executemany("INSERT INTO menu_items (name, price, image, description) VALUES (?, ?, ?, ?)", menu_data)
conn.commit()
conn.close()
