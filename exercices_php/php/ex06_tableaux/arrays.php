<?php
// Inventaire simple
$inventaire = ["Epée", "Bouclier", "Potion", "Parchemin"];

array_push($inventaire, "Bottes de vitesse"); // Découverte de array_push
sort($inventaire); // Hop on range

echo "J'ai " . count($inventaire) . " objets.<br>";

// Affichage
echo "<ul>";
foreach ($inventaire as $item) {
    echo "<li>$item</li>";
}
echo "</ul>";
?>