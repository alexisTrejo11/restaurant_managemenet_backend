-- Inserting Menu Items
INSERT INTO menu_items (name, price, description, category, created_at, updated_at) VALUES
    -- Drinks
    ('Freshly Brewed Coffee', 3.50, 'Rich, aromatic house blend', 'DRINKS', NOW(), NOW()),
    ('Iced Tea', 3.25, 'Refreshing cold brew with lemon', 'DRINKS', NOW(), NOW()),
    ('Fresh Orange Juice', 4.00, 'Squeezed daily', 'DRINKS', NOW(), NOW()),
    ('Coca-Cola', 2.75, 'Classic cold soda', 'DRINKS', NOW(), NOW()),
    ('Mineral Water', 2.50, 'Sparkling or still', 'DRINKS', NOW(), NOW()),

    -- Alcohol Drinks
    ('House Red Wine', 8.50, 'Smooth cabernet sauvignon', 'ALCOHOL_DRINKS', NOW(), NOW()),
    ('House White Wine', 8.50, 'Crisp chardonnay', 'ALCOHOL_DRINKS', NOW(), NOW()),
    ('Craft Beer', 6.00, 'Local brewery selection', 'ALCOHOL_DRINKS', NOW(), NOW()),
    ('Mimosa', 7.50, 'Champagne and fresh orange juice', 'ALCOHOL_DRINKS', NOW(), NOW()),

    -- Breakfasts
    ('Classic Breakfast', 12.95, 'Two eggs, bacon, toast, and hash browns', 'BREAKFASTS', NOW(), NOW()),
    ('Vegetarian Breakfast', 11.50, 'Scrambled tofu, roasted vegetables, avocado toast', 'BREAKFASTS', NOW(), NOW()),
    ('Pancake Stack', 9.75, 'Fluffy buttermilk pancakes with maple syrup', 'BREAKFASTS', NOW(), NOW()),
    ('Eggs Benedict', 13.50, 'Poached eggs, hollandaise sauce on English muffin', 'BREAKFASTS', NOW(), NOW()),

    -- Starters
    ('Chicken Wings', 10.95, '6 wings with choice of sauce: BBQ, Buffalo, or Honey Garlic', 'STARTERS', NOW(), NOW()),
    ('Nachos', 12.50, 'Loaded with cheese, jalapeños, salsa, and sour cream', 'STARTERS', NOW(), NOW()),
    ('Caesar Salad', 8.75, 'Crisp romaine, croutons, parmesan, house dressing', 'STARTERS', NOW(), NOW()),

    -- Meals
    ('Classic Burger', 14.95, 'Angus beef, cheese, lettuce, tomato, brioche bun', 'MEALS', NOW(), NOW()),
    ('Grilled Salmon', 18.50, 'Fresh salmon, roasted vegetables, lemon butter sauce', 'MEALS', NOW(), NOW()),
    ('Vegetarian Pasta', 15.25, 'Penne with roasted vegetables, marinara sauce', 'MEALS', NOW(), NOW()),
    ('Chicken Parmesan', 16.75, 'Breaded chicken, marinara, melted mozzarella', 'MEALS', NOW(), NOW()),

    -- Desserts
    ('New York Cheesecake', 7.50, 'Classic style with berry compote', 'DESSERTS', NOW(), NOW()),
    ('Chocolate Lava Cake', 8.25, 'Warm chocolate cake with vanilla ice cream', 'DESSERTS', NOW(), NOW()),
    ('Apple Pie', 6.75, 'Homemade with vanilla ice cream', 'DESSERTS', NOW(), NOW()),

    -- Extras
    ('Extra Bacon', 3.50, 'Additional crispy bacon strips', 'EXTRAS', NOW(), NOW()),
    ('Gluten-Free Bread', 2.50, 'Substitute for regular bread', 'EXTRAS', NOW(), NOW()),
    ('Side Salad', 4.25, 'Small garden salad', 'EXTRAS', NOW(), NOW());


-- Inserting Menu Extras
INSERT INTO menu_extras (name, price, created_at, updated_at) VALUES
    ('Gluten-Free Option', 1.00, NOW(), NOW()),
    ('Vegetarian Option',  1.50, NOW(), NOW()),
    ('Vegan Option', 1.25, NOW(), NOW()),
    ('Dairy-Free Option', 0.50, NOW(), NOW()),
    ('Nut-Free Option', 1.00, NOW(), NOW());
