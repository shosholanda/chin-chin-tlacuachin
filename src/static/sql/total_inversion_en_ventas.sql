WITH total_ventas_por_producto AS (
    -- SUBQUERY para obtener el número de ventas por producto des-relacionado
    SELECT 
        producto.gtin,
        producto.nombre,
        COALESCE(SUM(transaccion.cantidad), 0) AS total
    FROM venta
    JOIN transaccion ON venta.referencia = transaccion.id_referencia
    RIGHT JOIN producto ON producto.id = transaccion.id_producto
    -- WHERE producto.nombre = 'Lord Africano'
    GROUP BY producto.gtin
    ORDER BY total DESC
),

total_inversion_por_producto AS (
    -- SUBQUERY para obtener el total de inversion por producto
    SELECT 
        producto.gtin,
        ROUND(COALESCE(SUM(receta.cantidad * articulo.costo_unitario), 0), 2) AS inversion
    FROM producto
    LEFT JOIN receta ON receta.id_producto = producto.id
    LEFT JOIN articulo ON articulo.id = receta.id_insumo
    -- WHERE producto.nombre = 'Lord Africano'
    GROUP BY producto.gtin
    ORDER BY inversion DESC
) SELECT 
    -- Unir SUBQUERIES donde cada valor es independiente. Deben coincidir en número de filas
    s.gtin,
    s.nombre,
    s.total AS total_ventas,
    c.inversion AS inversion_por_prod,
    ROUND(s.total * c.inversion, 2) AS total_inversion
FROM total_ventas_por_producto s
JOIN total_inversion_por_producto c ON s.gtin = c.gtin
ORDER BY total DESC;



-- Muestra el total de inversion que se ha hecho en insumos de cada producto vendido
-- podemos ordenar por cualquier columna.

-- +-------------------------+------------------------------------+--------------+--------------------+-----------------+
-- | gtin                    | nombre                             | total_ventas | inversion_por_prod | total_inversion |
-- +-------------------------+------------------------------------+--------------+--------------------+-----------------+
-- | BAGUPAVOSNNO120         | Baguette De Pavo                   |           34 |                  0 |               0 |
-- | ROLECANEGANO45          | Roles De Canela                    |           20 |                  0 |               0 |
-- | TAROCACH65              | Taro                               |           16 |                  0 |               0 |
-- | CAFEEXPRCACH40          | Cafe Expresso                      |           13 |               31.3 |           406.9 |
-- | BAGULOMOCANASALASNNO300 | Baguette De Lomo Canadiense Salami |           11 |                  0 |               0 |
-- | SANDCHORSNNO123         | Sandwich De Chorizo                |            9 |                  0 |               0 |
-- | MAZAFRNO80              | Mazapan                            |            7 |                  0 |               0 |
-- | LORDAFRISNNO80          | Lord Africano                      |            6 |              77.32 |          463.92 |
-- | CAFÉEXPRCAGR45          | Café Expresso                      |            4 |                 45 |             180 |
-- | TAROCAGR70              | Taro                               |            4 |                1.9 |             7.6 |
-- | BAGULOMOCANASALASNNO70  | Baguette De Lomo Canadiense Salami |            3 |                  0 |               0 |
-- | GALLSNNO10              | Galleta                            |            2 |                  0 |               0 |
-- | PANAJOPANO45            | Pan De Ajo                         |            2 |                  0 |               0 |
-- | FRESCONCREMPOEN90       | Fresas Con Crema                   |            1 |                  3 |               3 |
-- | ALMEGACH15              | Almendras                          |            0 |                  0 |               0 |
-- +-------------------------+------------------------------------+--------------+--------------------+-----------------+
