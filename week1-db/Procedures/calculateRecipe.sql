CREATE PROCEDURE [dbo].[calculateRecipe]
  @turkeySize DECIMAL(10,5)
AS
BEGIN
  SELECT IngredientName, UnitofMeasure,
    cast(round((RatioToTurkeyLBs*@turkeySize),2) as decimal(6,2)) AS IngredientAmount
  FROM Ingredients
  FOR JSON PATH
END
