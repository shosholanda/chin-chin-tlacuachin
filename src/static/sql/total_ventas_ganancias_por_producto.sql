SELECT producto.nombre, 
	ROUND(COALESCE(SUM(cantidad), 0), 2) AS total_vendido, 
    categoria.nombre AS categoria, 
    precio,
    ROUND(COALESCE(SUM(cantidad) * precio, 0), 2) AS total_ganancias
    FROM transaccion
RIGHT JOIN producto ON producto.id = id_producto
JOIN categoria ON categoria.id = id_categoria
-- WHERE categoria.nombre = "SNACK"
GROUP BY id_producto, producto.nombre, categoria.nombre, producto.precio
ORDER BY total_vendido DESC;

-- Muestra todas las ventas + ganancias de cada producto.
-- se puede ordenar por #ventas o por #ganancias. 0 si no se ha vendido el producto

-- +------------------------------------+---------------+-----------+--------+-----------------+
-- | nombre                             | total_vendido | categoria | precio | total_ganancias |
-- +------------------------------------+---------------+-----------+--------+-----------------+
-- | Baguette De Pavo                   |            34 | Snack     |    120 |            4080 |
-- | Roles De Canela                    |            20 | Galletas  |     45 |             900 |
-- | Taro                               |            16 | Caliente  |     65 |            1040 |
-- | Cafe Expresso                      |            13 | Caliente  |     40 |             520 |
-- | Baguette De Lomo Canadiense Salami |            11 | Snack     |    300 |            3300 |
-- | Sandwich De Chorizo                |             9 | Snack     |    123 |            1107 |
-- | Mazapan                            |             7 | Frappé    |     80 |             560 |
-- | Lord Africano                      |             6 | Snack     |     80 |             480 |
-- | Café Expresso                      |             4 | Caliente  |     45 |             180 |
-- | Taro                               |             4 | Caliente  |     70 |             280 |
-- | Baguette De Lomo Canadiense Salami |             3 | Snack     |     70 |             210 |
-- | Galleta                            |             2 | Snack     |     10 |              20 |
-- | Pan De Ajo                         |             2 | Panes     |     45 |              90 |
-- | Fresas Con Crema                   |             1 | Postres   |     90 |              90 |
-- +------------------------------------+---------------+-----------+--------+-----------------+