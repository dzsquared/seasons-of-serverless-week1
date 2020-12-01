-- This file contains SQL statements that will be executed after the build script.

DELETE FROM INGREDIENTS;
GO

INSERT INTO INGREDIENTS (INGREDIENTNAME, UNITOFMEASURE, RATIOTOTURKEYLBS)
VALUES ('Salt', 'cups', 0.05), ('Water', 'gal', 0.66),
    ('Brown sugar', 'cups', 0.13), ('Shallots', 'each', 0.2),
    ('Garlic', 'cloves', 0.4), ('Whole peppercorns','tbsp', 0.13),
    ('Dried juniper berries', 'tbsp', 0.13), ('Fresh rosemary','tbsp', 0.13),
    ('Thyme', 'tbsp', 0.06), ('Brine time','hours', 2.4),
    ('Roast time','minutes', 15);
GO

-- if executing this on your own database
-- add the login azfunction to the server by executing
-- CREATE LOGIN azfunction WITH PASSWORD='##your##password##here##';
-- against master db

CREATE USER azfunction
FROM LOGIN azfunction
WITH DEFAULT_SCHEMA=dbo;
GO

EXEC sp_addrolemember 'db_datareader', 'azfunction';

EXEC sp_addrolemember 'db_datawriter', 'azfunction';


CREATE ROLE serverless_app;
EXEC sp_addrolemember 'serverless_app', 'azfunction';

GRANT EXECUTE ON OBJECT ::dbo.calculateRecipe  
    TO serverless_app;


