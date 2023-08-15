<?php
$lignes = file("data.txt");
foreach ($lignes as $num => $ligne) {
    echo $num . ": " . $ligne . " <a href='del.php?id=$num'>X</a><br>";
}
?>