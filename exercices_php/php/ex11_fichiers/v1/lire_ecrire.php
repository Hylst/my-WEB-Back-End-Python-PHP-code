<?php
// Version bourrin
$fichier = "test.txt";
$handle = fopen($fichier, 'w') or die("Impossible d'ouvrir le fichier");
$txt = "Première ligne\n";
fwrite($handle, $txt);
$txt = "Deuxième ligne\n";
fwrite($handle, $txt);
fclose($handle);

echo "Fichier écrit.";
?>