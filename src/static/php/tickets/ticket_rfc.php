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
$rfc = "Anahy Lorena Vera Trejo RFC.\nVETA950117MZ8 Col. Sta. Catarina\nCP. 01320 RESICO\n";
$printer -> text($rfc);

$printer -> text("Fecha: {date}\n");
$printer -> feed();
$printer -> text("Orden de: {cliente}\n");
$hr = "________________________________\n";
$printer -> text($hr);

$printer -> text("13x Americano............$176.00\n");
$printer -> text("3x  Capuchino............$  4.00\n");
$printer -> text("12x Chocolate............$104.00\n");
$printer -> text("7x  Dieguito thunder.....$ 42.00\n");
$printer -> text("7x  Ostión ahumado.......$193.00\n");
$printer -> text("8x  La michi berta.......$189.00\n");
$printer -> text("8x  Galleta limón con ama$ 37.00\n");
$printer -> text("1x  Baguette de pavo.....$138.00\n");
$printer -> text($hr);
$printer -> text("TOTAL:                   $123.00\n");

$printer -> setJustification(Printer::JUSTIFY_CENTER);
$printer -> selectPrintMode(Printer::MODE_EMPHASIZED);
$printer -> feed();

$printer -> setBarcodeHeight(100);
$printer -> setBarcodeTextPosition(Printer::BARCODE_TEXT_BELOW);
$printer -> barcode("0000000001");
$printer -> feed();
$printer -> text("!Gracias por su visita!");
  
$printer -> cut();
$printer -> close();
