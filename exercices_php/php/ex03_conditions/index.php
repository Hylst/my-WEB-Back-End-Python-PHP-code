<?php
// Conditions, le coeur du gameplay

$score_des = rand(1, 20); // Un d20, classique
echo "Résultat du dé : " . $score_des . "<br>";

if ($score_des == 20) {
    echo "Critique ! Dégâts doublés !";
} elseif ($score_des == 1) {
    echo "Echec critique... L'épée te glisse des mains.";
} else {
    echo "Coup normal.";
}

echo "<hr>";

// Test Switch
switch ($score_des) {
    case 20:
        echo "Perfect !";
        break;
    case 1:
        echo "Fumble !";
        break;
    default:
        echo "Roll standard.";
}
?>