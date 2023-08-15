<?php
// Boucles... pour grinder les XP

echo "<h3>Boucle For</h3>";
// Compter jusqu'à 10
for ($i = 1; $i <= 10; $i++) {
    echo "Niveau $i atteint <br>";
}

echo "<h3>Boucle While</h3>";
// Tant qu'on n'a pas fait 6 au dé...
$de = 0;
$tentatives = 0;
while ($de != 6) {
    $de = rand(1, 6);
    $tentatives++;
    echo "Lancer $tentatives : $de <br>";
}
echo "Enfin un 6 !";

echo "<h3>Do While</h3>";
// Au moins une fois
$j = 0;
do {
    echo "Tour de chauffe $j <br>";
    $j++;
} while ($j < 3);
?>