import pytest
from ventas import ProcesadorVentas


def test_validar_venta_correcta():
    procesador = ProcesadorVentas()

    venta = {
        "producto": "Notebook",
        "cantidad": 2,
        "precio_unitario": 1000
    }

    assert procesador.validar_venta(venta) is True


def test_validar_venta_sin_producto():
    procesador = ProcesadorVentas()

    venta = {
        "cantidad": 2,
        "precio_unitario": 1000
    }

    with pytest.raises(ValueError):
        procesador.validar_venta(venta)


def test_calcular_subtotal():
    procesador = ProcesadorVentas()

    venta = {
        "producto": "Monitor",
        "cantidad": 3,
        "precio_unitario": 200
    }

    assert procesador.calcular_subtotal(venta) == 600


def test_calcular_total_venta_sin_descuento():
    procesador = ProcesadorVentas()

    venta = {
        "producto": "Notebook",
        "cantidad": 1,
        "precio_unitario": 1000
    }

    assert procesador.calcular_total_venta(venta) == 1210


def test_calcular_total_venta_con_descuento():
    procesador = ProcesadorVentas(porcentaje_descuento=10)

    venta = {
        "producto": "Notebook",
        "cantidad": 1,
        "precio_unitario": 1000
    }

    assert procesador.calcular_total_venta(venta) == 1089


def test_descuento_invalido():
    procesador = ProcesadorVentas(porcentaje_descuento=150)

    venta = {
        "producto": "Notebook",
        "cantidad": 1,
        "precio_unitario": 1000
    }

    with pytest.raises(ValueError):
        procesador.calcular_total_venta(venta)


def test_impuesto_negativo():
    procesador = ProcesadorVentas(porcentaje_impuesto=-21)

    venta = {
        "producto": "Notebook",
        "cantidad": 1,
        "precio_unitario": 1000
    }

    with pytest.raises(ValueError):
        procesador.calcular_total_venta(venta)


def test_procesar_ventas():
    procesador = ProcesadorVentas()

    ventas = [
        {
            "producto": "Notebook",
            "cantidad": 1,
            "precio_unitario": 1000
        },
        {
            "producto": "Mouse",
            "cantidad": 2,
            "precio_unitario": 50
        }
    ]

    resultado = procesador.procesar_ventas(ventas)

    assert len(resultado) == 2
    assert resultado[0]["total"] == 1210
    assert resultado[1]["total"] == 121


def test_total_general():
    procesador = ProcesadorVentas()

    ventas_procesadas = [
        {
            "producto": "Notebook",
            "cantidad": 1,
            "precio_unitario": 1000,
            "total": 1210
        },
        {
            "producto": "Mouse",
            "cantidad": 2,
            "precio_unitario": 50,
            "total": 121
        }
    ]

    assert procesador.calcular_total_general(ventas_procesadas) == 1331


def test_producto_mas_vendido():
    procesador = ProcesadorVentas()

    ventas = [
        {
            "producto": "Notebook",
            "cantidad": 1,
            "precio_unitario": 1000
        },
        {
            "producto": "Mouse",
            "cantidad": 5,
            "precio_unitario": 50
        },
        {
            "producto": "Notebook",
            "cantidad": 2,
            "precio_unitario": 1000
        }
    ]

    assert procesador.obtener_producto_mas_vendido(ventas) == "Mouse"


def test_resumen_por_producto():
    procesador = ProcesadorVentas()

    ventas = [
        {
            "producto": "Notebook",
            "cantidad": 1,
            "precio_unitario": 1000
        },
        {
            "producto": "Mouse",
            "cantidad": 5,
            "precio_unitario": 50
        },
        {
            "producto": "Notebook",
            "cantidad": 2,
            "precio_unitario": 1000
        }
    ]

    resumen = procesador.resumir_ventas_por_producto(ventas)

    assert resumen["Notebook"]["cantidad_total"] == 3
    assert resumen["Notebook"]["subtotal_total"] == 3000
    assert resumen["Mouse"]["cantidad_total"] == 5
    assert resumen["Mouse"]["subtotal_total"] == 250


def test_leer_ventas_csv(tmp_path):
    procesador = ProcesadorVentas()

    archivo = tmp_path / "ventas.csv"

    archivo.write_text(
        "producto,cantidad,precio_unitario\n"
        "Notebook,2,1000\n"
        "Mouse,3,50\n",
        encoding="utf-8"
    )

    ventas = procesador.leer_ventas_csv(archivo)

    assert len(ventas) == 2
    assert ventas[0]["producto"] == "Notebook"
    assert ventas[0]["cantidad"] == 2
    assert ventas[0]["precio_unitario"] == 1000
    assert ventas[1]["producto"] == "Mouse"
