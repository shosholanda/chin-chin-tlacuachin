SELECT 
	producto.gtin,
	producto.nombre,
	categoria.nombre AS categoria,
	COALESCE(SUM(transaccion.cantidad), 0) AS total_ventas
FROM venta
JOIN transaccion ON venta.referencia = transaccion.id_referencia
RIGHT JOIN producto ON producto.id = transaccion.id_producto
JOIN categoria ON categoria.id = producto.id_categoria
-- WHERE categoria.nombre = 'Panes'
GROUP BY producto.gtin, producto.nombre, categoria.nombre
ORDER BY total_ventas DESC;


-- muestra todas las ventas realizados de estos productos

-- +-------------------------+------------------------------------+-----------+-------------+
-- | gtin                    | nombre                             | categoria | total_ventas|
-- +-------------------------+------------------------------------+-----------+-------------+
-- | BAGUPAVOSNNO120         | Baguette De Pavo                   | Snack     |          34 |
-- | ROLECANEGANO45          | Roles De Canela                    | Galletas  |          20 |
-- | TAROCACH65              | Taro                               | Caliente  |          16 |
-- | CAFEEXPRCACH40          | Cafe Expresso                      | Caliente  |          13 |
-- | BAGULOMOCANASALASNNO300 | Baguette De Lomo Canadiense Salami | Snack     |          11 |
-- | SANDCHORSNNO123         | Sandwich De Chorizo                | Snack     |           9 |
-- | MAZAFRNO80              | Mazapan                            | Frappé    |           7 |
-- | LORDAFRISNNO80          | Lord Africano                      | Snack     |           6 |
-- | CAFÉEXPRCAGR45          | Café Expresso                      | Caliente  |           4 |
-- | TAROCAGR70              | Taro                               | Caliente  |           4 |
-- | BAGULOMOCANASALASNNO70  | Baguette De Lomo Canadiense Salami | Snack     |           3 |
-- | GALLSNNO10              | Galleta                            | Snack     |           2 |
-- | PANAJOPANO45            | Pan De Ajo                         | Panes     |           2 |
-- | FRESCONCREMPOEN90       | Fresas Con Crema                   | Postres   |           1 |
-- | ALMEGACH15              | Almendras                          | Galletas  |           0 |
-- +-------------------------+------------------------------------+-----------+-------------+