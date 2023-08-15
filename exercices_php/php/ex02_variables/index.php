<?php
// Les variables... ça me rappelle mes fiches de perso D&D
$nom_perso = "Grog";
$force = 18; // 18/00 même si possible
$agile = false; // C'est un barbare en même temps...

echo "Nom : " . $nom_perso . "<br>";
echo "Force : $force <br>"; 
echo "Agilité : " . ($agile ? 'Oui' : 'Non') . "<br>"; // J'ai découvert le ternaire !

// Test de concaténation
$niveau = 1;
echo "Le perso " . $nom_perso . " est niveau " . $niveau;

// Debug type
echo "<br>Type de force : " . gettype($force);
?>