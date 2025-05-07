SELECT 
    producto.gtin AS gtin,
	producto.nombre AS producto,
    articulo.nombre AS insumo,
    receta.cantidad AS cantidad_insumo,
    articulo.costo_unitario AS costo_insumo,    
    ROUND(receta.cantidad * articulo.costo_unitario, 2) AS total_insumo
FROM producto
LEFT JOIN receta ON receta.id_producto = producto.id
LEFT JOIN articulo ON articulo.id = id_insumo
-- WHERE producto.nombre = 'Lord Africano'
ORDER BY gtin;

-- Muestra la inversion hecha por cada producto por cada insumo, esto es:
-- (lo que necesita * lo que cuesta) = total
-- NULL SI NO ESTA LA INFORMACION REQUERIDA

-- +-------------------------+------------------------------------+--------------------+-----------------+--------------+--------------+
-- | gtin                    | producto                           | insumo             | cantidad_insumo | costo_insumo | total_insumo |
-- +-------------------------+------------------------------------+--------------------+-----------------+--------------+--------------+
-- | ALMEGACH15              | Almendras                          | NULL               |            NULL |         NULL |         NULL |
-- | BAGULOMOCANASALASNNO300 | Baguette De Lomo Canadiense Salami | NULL               |            NULL |         NULL |         NULL |
-- | BAGULOMOCANASALASNNO70  | Baguette De Lomo Canadiense Salami | NULL               |            NULL |         NULL |         NULL |
-- | BAGUPAVOSNNO120         | Baguette De Pavo                   | NULL               |            NULL |         NULL |         NULL |
-- | CAFEEXPRCACH40          | Cafe Expresso                      | Café               |             0.2 |          102 |         20.4 |
-- | CAFEEXPRCACH40          | Cafe Expresso                      | Leche              |            0.28 |           30 |          8.4 |
-- | CAFEEXPRCACH40          | Cafe Expresso                      | Vaso Desechable    |               1 |          2.5 |          2.5 |
-- | CAFÉEXPRCAGR45          | Café Expresso                      | Vaso Desechable    |               1 |          2.5 |          2.5 |
-- | CAFÉEXPRCAGR45          | Café Expresso                      | Barra De Chocolate |             0.5 |           34 |           17 |
-- | CAFÉEXPRCAGR45          | Café Expresso                      | Café               |            0.25 |          102 |         25.5 |
-- | FRESCONCREMPOEN90       | Fresas Con Crema                   | 1 Peso             |               1 |            1 |            1 |
-- +-------------------------+------------------------------------+--------------------+-----------------+--------------+--------------+