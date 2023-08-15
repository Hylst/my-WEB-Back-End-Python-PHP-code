<?php
// Fiche de perso plus complexe
$perso = [
    "nom" => "Aragorn",
    "classe" => "Rôdeur",
    "race" => "Humain",
    "niveau" => 5,
    "stats" => [ "FOR" => 15, "DEX" => 16 ] // Tableau dans tableau !
];

echo "Nom : " . $perso['nom'] . "<br>";
echo "Classe : " . $perso['classe'] . "<br>";
echo "DEX : " . $perso['stats']['DEX'] . "<br>";

// Modif
$perso['niveau'] = 6;

echo "<pre>";
print_r($perso);
echo "</pre>";
?>