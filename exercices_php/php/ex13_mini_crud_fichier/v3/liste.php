<?php
$data_file = "../v1/data.txt";
if (file_exists($data_file)) {
    $lignes = file($data_file);
    if (empty($lignes)) {
        echo "<p>Aucune tâche.</p>";
    } else {
        echo "<ul>";
        foreach ($lignes as $num => $ligne) {
            if (trim($ligne) != "")
                echo "<li>" . htmlspecialchars($ligne) . " <a href='del.php?id=$num'>[x]</a></li>";
        }
        echo "</ul>";
    }
} else {
    echo "Fichier de données introuvable.";
}
?>