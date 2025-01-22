<?php
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
$printer -> text($location);
/* If rfc required */
//__RFC__$rfc = "Anahy Lorena Vera Trejo RFC.\nVETA950117MZ8 Col. Sta. Catarina\nCP. 01320 RESICO\n";
//__RFC__$printer -> text($rfc);

$date = date("__DATE__");
$printer -> text("Fecha: " . $date . "\n");
$printer -> feed();
$printer -> text("Orden de: __CLIENTE__\n");
$printer -> setJustification(Printer::JUSTIFY_LEFT);
$hr = "________________________________\n";
$printer -> text($hr);
__PRODUCT__
// $printer -> text("PRODUCT");
$printer -> text($hr);
__TOTAL__

$printer -> setJustification(Printer::JUSTIFY_CENTER);
$printer -> selectPrintMode(Printer::MODE_EMPHASIZED);
$printer -> feed();

$printer -> setBarcodeHeight(100);
$printer -> setBarcodeTextPosition(Printer::BARCODE_TEXT_BELOW);
$printer -> barcode("__REFERENCIA__");
$printer -> feed();
$printer -> text("¡Gracias por su visita!");

$printer -> cut();
$printer -> close();
