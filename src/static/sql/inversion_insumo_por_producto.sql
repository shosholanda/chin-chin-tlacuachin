SELECT 
	producto.gtin,
    producto.precio,
	ROUND(COALESCE(SUM(receta.cantidad * articulo.costo_unitario), 0), 2) AS inversion,
    ROUND(producto.precio - COALESCE(SUM(receta.cantidad * articulo.costo_unitario), 0), 2) AS restante
FROM producto
LEFT JOIN receta ON receta.id_producto = producto.id
LEFT JOIN articulo ON articulo.id = receta.id_insumo
-- WHERE producto.nombre = 'Lord Africano'
GROUP BY producto.gtin


-- Muestra la inversion hecha por cada producto, es decir lo que se gasta en hacer cada producto, mas su ganancia
-- SIN INCLUIR OTROS GASTOS, solo los del mismo producto

-- +-------------------------+--------+-----------+----------+
-- | gtin                    | precio | inversion | restante |
-- +-------------------------+--------+-----------+----------+
-- | CAFEEXPRCACH40          |     40 |      31.3 |      8.7 |
-- | CAFÉEXPRCAGR45          |     45 |        45 |        0 |
-- | TAROCACH65              |     65 |         0 |       65 |
-- | TAROCAGR70              |     70 |       1.9 |     68.1 |
-- | MAZAFRNO80              |     80 |         0 |       80 |
-- | BAGUPAVOSNNO120         |    120 |         0 |      120 |
-- | BAGULOMOCANASALASNNO300 |    300 |         0 |      300 |
-- | SANDCHORSNNO123         |    123 |         0 |      123 |
-- | GALLSNNO10              |     10 |         0 |       10 |
-- | LORDAFRISNNO80          |     80 |     77.32 |     2.68 |
-- | ROLECANEGANO45          |     45 |         0 |       45 |
-- | PANAJOPANO45            |     45 |         0 |       45 |
-- | BAGULOMOCANASALASNNO70  |     70 |         0 |       70 |
-- | FRESCONCREMPOEN90       |     90 |         3 |       87 |
-- | ALMEGACH15              |     15 |         0 |       15 |
-- +-------------------------+--------+-----------+----------+

