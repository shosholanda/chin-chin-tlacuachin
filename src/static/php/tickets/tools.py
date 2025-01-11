"""Clase para ayudar a formatear el texto en 32 caracteres."""
import random as r
import datetime as dt


# Q sucio me siento
header = '''<?php
/**
 * Ruta relativa
 * Debe instalarse con composer require mike42/escpos-php
 * desde ~/
 */
$homeDir = getenv("HOME");
require $homeDir . "/vendor/autoload.php";

/* Controladores */
use Mike42\Escpos\PrintConnectors\FilePrintConnector;
use Mike42\Escpos\Printer;

$connector = new FilePrintConnector("php://stdout");
$printer = new Printer($connector);

$printer -> setJustification(Printer::JUSTIFY_CENTER);
$printer -> selectPrintMode(Printer::MODE_DOUBLE_WIDTH);
$printer -> text("¡CHIN CHIN!\n");
$printer -> selectPrintMode(Printer::MODE_UNDERLINE | Printer::MODE_DOUBLE_WIDTH);
$printer -> text("Tlacuachin\n");
$printer -> selectPrintMode();
$location = "Guanajuato 28 Bis, Roma Norte.,\nCuauhtémoc, CP. 06700, CDMX.\n";
$printer -> text($location);'''

rfc = '''/* If rfc required */
$rfc = "Anahy Lorena Vera Trejo RFC.\nVETA950117MZ8 Col. Sta. Catarina\nCP. 01320 RESICO\n";
$printer -> text($rfc);'''

info = '''$printer -> text("Fecha: {date}\n");
$printer -> feed();
$printer -> text("Orden de: {cliente}\n");
$hr = "________________________________\n";
$printer -> text($hr);'''

item = '''$printer -> text("{product}\n");'''

finish = '''$printer -> text($hr);
$printer -> text("{suma}\n");

$printer -> setJustification(Printer::JUSTIFY_CENTER);
$printer -> selectPrintMode(Printer::MODE_EMPHASIZED);
$printer -> feed();

$printer -> setBarcodeHeight(100);
$printer -> setBarcodeTextPosition(Printer::BARCODE_TEXT_BELOW);
$printer -> barcode("{referencia}");
$printer -> feed();
$printer -> text("!Gracias por su visita!");
  
$printer -> cut();
$printer -> close();
'''


def fit_space(s, n, char=" "):
    while len(s) < n:
        s+= char
    return s

def compress_row(quant, prod, price, l=32 ):
    row = str(quant) + "x"
    #12345678901234567890123456789012
    #99x.Baguette de pavo.....$999.00
    row = fit_space(row, 4)
    prod = prod[:21]
    row += prod
    row = fit_space(row, 25, ".")
    row += "$"
   
    if len(str(price)) < 3:
        row += " "*(3 - len(str(price)))
        
    row += '{:.2f}'.format(price)
    return row 

def t(n):
    row = '{:.2f}'.format(n)
    row = "$" + row
    total = 'TOTAL:'
    row = " "*(32 - len(total) -len(row)) + row
    row = total + row
    return row


def create_php(cliente, productos, total, referencia, date=dt.datetime.now().strftime("%d/%m/%Y %I:%M:%S"), rfc_required=False):
    php = header
    if True:
    # if rfc:
        php += rfc
    php += info.format(date=date, cliente=cliente);

    for p in productos:
        php += item.format(product=compress_row(p['cantidad'], p['nombre'], p['precio']))

    ref = '{:09d}'.format(referencia)
    php += finish.format(suma=t(total), referencia=ref)
    return php

if __name__ == '__main__':
    prod = [{'nombre': 'Galleta',
             'cantidad': 2,
             'precio': 30},
            {'nombre': 'Taro',
             'cantidad': 1,
             'precio': 40}
            ]

    print(create_php("Davidshiro", prod, 100, 1))
    
