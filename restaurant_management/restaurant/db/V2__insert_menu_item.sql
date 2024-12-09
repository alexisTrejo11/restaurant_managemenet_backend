-- Inserting Menu Items
INSERT INTO menu_items (name, price, description, category) VALUES
    -- Drinks
    ('Freshly Brewed Coffee', 3.50, 'Rich, aromatic house blend', 'DRINKS'),
    ('Iced Tea', 3.25, 'Refreshing cold brew with lemon', 'DRINKS'),
    ('Fresh Orange Juice', 4.00, 'Squeezed daily', 'DRINKS'),
    ('Coca-Cola', 2.75, 'Classic cold soda', 'DRINKS'),
    ('Mineral Water', 2.50, 'Sparkling or still', 'DRINKS'),

    -- Alcohol Drinks
    ('House Red Wine', 8.50, 'Smooth cabernet sauvignon', 'ALCOHOL_DRINKS'),
    ('House White Wine', 8.50, 'Crisp chardonnay', 'ALCOHOL_DRINKS'),
    ('Craft Beer', 6.00, 'Local brewery selection', 'ALCOHOL_DRINKS'),
    ('Mimosa', 7.50, 'Champagne and fresh orange juice', 'ALCOHOL_DRINKS'),

    -- Breakfasts
    ('Classic Breakfast', 12.95, 'Two eggs, bacon, toast, and hash browns', 'BREAKFASTS'),
    ('Vegetarian Breakfast', 11.50, 'Scrambled tofu, roasted vegetables, avocado toast', 'BREAKFASTS'),
    ('Pancake Stack', 9.75, 'Fluffy buttermilk pancakes with maple syrup', 'BREAKFASTS'),
    ('Eggs Benedict', 13.50, 'Poached eggs, hollandaise sauce on English muffin', 'BREAKFASTS'),

    -- Starters
    ('Chicken Wings', 10.95, '6 wings with choice of sauce: BBQ, Buffalo, or Honey Garlic', 'STARTERS'),
    ('Nachos', 12.50, 'Loaded with cheese, jalapeños, salsa, and sour cream', 'STARTERS'),
    ('Caesar Salad', 8.75, 'Crisp romaine, croutons, parmesan, house dressing', 'STARTERS'),

    -- Meals
    ('Classic Burger', 14.95, 'Angus beef, cheese, lettuce, tomato, brioche bun', 'MEALS'),
    ('Grilled Salmon', 18.50, 'Fresh salmon, roasted vegetables, lemon butter sauce', 'MEALS'),
    ('Vegetarian Pasta', 15.25, 'Penne with roasted vegetables, marinara sauce', 'MEALS'),
    ('Chicken Parmesan', 16.75, 'Breaded chicken, marinara, melted mozzarella', 'MEALS'),

    -- Desserts
    ('New York Cheesecake', 7.50, 'Classic style with berry compote', 'DESSERTS'),
    ('Chocolate Lava Cake', 8.25, 'Warm chocolate cake with vanilla ice cream', 'DESSERTS'),
    ('Apple Pie', 6.75, 'Homemade with vanilla ice cream', 'DESSERTS'),

    -- Extras
    ('Extra Bacon', 3.50, 'Additional crispy bacon strips', 'EXTRAS'),
    ('Gluten-Free Bread', 2.50, 'Substitute for regular bread', 'EXTRAS'),
    ('Side Salad', 4.25, 'Small garden salad', 'EXTRAS');

-- Inserting Menu Extras
INSERT INTO menu_extras (name) VALUES
    ('Gluten-Free Option'),
    ('Vegetarian Option'),
    ('Vegan Option'),
    ('Dairy-Free Option'),
    ('Nut-Free Option');