<?php
// On récupère les données
$nom = $_POST['nom'] ?? 'Inconnu'; // Opérateur null coalescent (découvert sur stackoverflow)
$age = $_POST['age'] ?? 0;
$ville = $_POST['ville'] ?? 'Nulle part';

echo "Bonjour <strong>$nom</strong>, tu as $age ans et tu viens de $ville.";

if ($age < 18) {
    echo "<br>Attention, c'est interdit aux mineurs ici normalement.";
}
?>