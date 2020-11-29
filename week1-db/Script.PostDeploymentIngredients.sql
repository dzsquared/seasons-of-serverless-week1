-- This file contains SQL statements that will be executed after the build script.

DELETE FROM INGREDIENTS;
GO

INSERT INTO INGREDIENTS (INGREDIENTNAME, UNITOFMEASURE, RATIOTOTURKEYLBS)
VALUES ('Salt', 'cups', 0.05), ('Water', 'gal', 0.66),
    ('Brown sugar', 'cups', 0.13), ('Shallots', 'each', 0.2),
    ('Garlic', 'cloves', 0.4), ('Whole peppercorns','tbsp', 0.13),
    ('Dried juniper berries', 'tbsp', 0.13), ('Fresh rosemary','tbsp', 0.13),
    ('Thyme', 'tbsp', 0.06), ('Brine time','hours', 2.4),
    ('Roast time','minutes', 15)
