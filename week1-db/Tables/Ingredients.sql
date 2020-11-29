CREATE TABLE [dbo].[Ingredients]
(
  IngredientName NVARCHAR(200) NOT NULL PRIMARY KEY,
  UnitofMeasure NVARCHAR(20) NOT NULL,
  RatioToTurkeyLBs DECIMAL(10,4) NOT NULL
);
GO
