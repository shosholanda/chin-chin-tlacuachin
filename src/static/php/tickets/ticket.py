"""Clase para ayudar a formatear el texto en 32 caracteres."""
import datetime as dt
import os


class Ticket:
    """Crea un Ticket para ser impreso y entregado a los clientes.

    Existe con la opción para facturar o solo ticket.
    """

    def __init__(self, cliente, productos, total, referencia, rfc=False):
        """Construye un objeto de ticket."""
        self.cliente = cliente
        self.productos = productos
        self.total = total
        self.referencia = referencia
        self.date = dt.datetime.now().strftime("%d/%m/%Y %I:%M:%S")
        self.rfc = rfc
        self.php = None
        self.create_php()

    def create_php(self):
        """Crea el String del php."""
        php = open("./src/static/php/tickets/ticket_template.php", 'r').read()
        if self.rfc:
            php = php.replace('//__RFC__', '')
        php = php.replace('__DATE__', self.date)
        php = php.replace('__CLIENTE__', self.cliente)

        for p in self.productos:
            prod = self.compress_row(p['cantidad'], p['nombre'], p['precio'])
            code = '$printer -> text("' + prod + '\n");'
            php = php.replace('__PRODUCT__', code + '\n__PRODUCT__')
        php = php.replace('__PRODUCT__', '')

        total = '{:.2f}'.format(self.total)
        if self.total < 100:
            le = len(str(self.total))
            total = " "*(3-le) + total
        total = '$' + total
        total = "TOTAL:" + " "*(32 - 6 - len(total)) + total
        code = '$printer -> text("' + total + '\n");'

        php = php.replace('__TOTAL__', code)

        ref = '{:09d}'.format(self.referencia)
        php = php.replace('__REFERENCIA__', ref)
        self.php = php

    def print_ticket(self, route):
        """Imprime un ticket en un POS (Point of sale)."""
        try:
            tmp_ticket = '/tmp/ticket' + '{:09d}'.format(self.referencia) + '.php'
            f = open(tmp_ticket, 'w')
            f.write(self.php)
            f.close()

            os.system("php " + tmp_ticket + " > " + route)
        except Exception as e:
            return "No se pudo imprimir. \n" + str(e)
        return "OK"

    def fit_space(self, s, n, char=" "):
        """Rellena hasta la columna n de espacios."""
        while len(s) < n:
            s += char
        return s

    def compress_row(self, quant, prod, price, leng=32):
        """Agrega los productos en un espacio de |leng| caracteres."""
        row = str(quant) + "x"
        # 12345678901234567890123456789012
        # 99x.Baguette de pavo.....$999.00
        row = self.fit_space(row, 4)
        prod = prod[:21]
        row += prod
        row = self.fit_space(row, 25, ".")
        row += "$"

        if price < 100:
            row += " "*(3 - len(str(price)))

        row += '{:.2f}'.format(price)
        return row

    def __repr__(self):
        """."""
        return self.__str__()

    def __str__(self):
        """."""
        return self.php


if __name__ == '__main__':
    # TESTS
    prod = [{'nombre': 'Lord African',
             'cantidad': 1,
             'precio': 143},
            {'nombre': 'Tisana',
             'cantidad': 1,
             'precio': 60},
            {'nombre': 'Homerosky',
             'cantidad': 20,
             'precio': 70}
            ]

    ticket = Ticket("Davidshiro Pichu", prod, 3320, 99999999)
    print(ticket.php)
