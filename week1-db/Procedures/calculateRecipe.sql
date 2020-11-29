CREATE PROCEDURE [dbo].[calculateRecipe]
  @turkeySize DECIMAL(10,5)
AS
BEGIN
  SELECT IngredientName, UnitofMeasure,
    cast(cast(round((RatioToTurkeyLBs*@turkeySize),2) as decimal(6,2)) as varchar(10)) AS IngredientAmount
  FROM Ingredients

END


GRANT EXECUTE ON OBJECT ::dbo.calculateRecipe  
    TO serverless_app;