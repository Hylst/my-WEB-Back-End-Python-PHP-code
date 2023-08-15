<?php
// Fonctions pour organiser le chaos

function calculerDegats($base, $bonus) {
    return $base + $bonus;
}

$degat_arme = 10;
$bonus_str = 3;

$total = calculerDegats($degat_arme, $bonus_str);
echo "Dégâts totaux : " . $total;

function saluer($nom = "Aventurier") {
    echo "<br>Salutations, $nom.";
}

saluer("Gimli");
saluer(); // Par défaut

// Fonction anonyme (ça a l'air compliqué mais pratique)
$potion = function($kv) {
    return $kv * 2;
};
echo "<br>Potion PV : " . $potion(15);
?>