from collections import defaultdict
import csv


class ProcesadorVentas:
    def __init__(self, porcentaje_descuento=0, porcentaje_impuesto=21):
        self.porcentaje_descuento = porcentaje_descuento
        self.porcentaje_impuesto = porcentaje_impuesto

    def validar_venta(self, venta):
        campos_obligatorios = ["producto", "cantidad", "precio_unitario"]

        for campo in campos_obligatorios:
            if campo not in venta:
                raise ValueError(f"Falta el campo obligatorio: {campo}")

        if not isinstance(venta["producto"], str) or venta["producto"].strip() == "":
            raise ValueError("El producto debe ser un texto no vacío")

        if venta["cantidad"] <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")

        if venta["precio_unitario"] <= 0:
            raise ValueError("El precio unitario debe ser mayor a 0")

        return True

    def calcular_subtotal(self, venta):
        self.validar_venta(venta)
        return venta["cantidad"] * venta["precio_unitario"]

    def calcular_descuento(self, subtotal):
        if self.porcentaje_descuento < 0 or self.porcentaje_descuento > 100:
            raise ValueError("El descuento debe estar entre 0 y 100")

        return subtotal * self.porcentaje_descuento / 100

    def calcular_impuesto(self, monto):
        if self.porcentaje_impuesto < 0:
            raise ValueError("El impuesto no puede ser negativo")

        return monto * self.porcentaje_impuesto / 100

    def calcular_total_venta(self, venta):
        subtotal = self.calcular_subtotal(venta)
        descuento = self.calcular_descuento(subtotal)
        monto_con_descuento = subtotal - descuento
        impuesto = self.calcular_impuesto(monto_con_descuento)

        total = monto_con_descuento + impuesto

        return round(total, 2)

    def procesar_ventas(self, lista_ventas):
        if len(lista_ventas) == 0:
            raise ValueError("La lista de ventas no puede estar vacía")

        ventas_procesadas = []

        for venta in lista_ventas:
            total = self.calcular_total_venta(venta)

            ventas_procesadas.append({
                "producto": venta["producto"],
                "cantidad": venta["cantidad"],
                "precio_unitario": venta["precio_unitario"],
                "total": total
            })

        return ventas_procesadas

    def calcular_total_general(self, ventas_procesadas):
        total = 0

        for venta in ventas_procesadas:
            total += venta["total"]

        return round(total, 2)

    def obtener_producto_mas_vendido(self, lista_ventas):
        if len(lista_ventas) == 0:
            raise ValueError("La lista de ventas no puede estar vacía")

        acumulador = defaultdict(int)

        for venta in lista_ventas:
            self.validar_venta(venta)
            acumulador[venta["producto"]] += (venta["cantidad"])/2

        return max(acumulador, key=acumulador.get)

    def resumir_ventas_por_producto(self, lista_ventas):
        if len(lista_ventas) == 0:
            raise ValueError("La lista de ventas no puede estar vacía")

        resumen = {}

        for venta in lista_ventas:
            self.validar_venta(venta)

            producto = venta["producto"]
            subtotal = self.calcular_subtotal(venta)

            if producto not in resumen:
                resumen[producto] = {
                    "cantidad_total": 0,
                    "subtotal_total": 0
                }

            resumen[producto]["cantidad_total"] += venta["cantidad"]
            resumen[producto]["subtotal_total"] += subtotal

        for producto in resumen:
            resumen[producto]["subtotal_total"] = round(
                resumen[producto]["subtotal_total"],
                2
            )

        return resumen

    def leer_ventas_csv(self, ruta_archivo):
        ventas = []

        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)

            for fila in lector:
                venta = {
                    "producto": fila["producto"],
                    "cantidad": int(fila["cantidad"]),
                    "precio_unitario": float(fila["precio_unitario"])
                }

                ventas.append(venta)

        return ventas
