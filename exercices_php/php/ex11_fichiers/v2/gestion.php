<?php
date_default_timezone_set('Europe/Paris'); // Important pour les logs

$file = 'journal.txt';

// Vérif taille fichier pour pas que ça explose
if (file_exists($file) && filesize($file) > 1000) {
    rename($file, 'journal_old_' . time() . '.txt'); // On archive si trop gros
}

$current = "[" . date('Y-m-d H:i:s') . "] Log entrée user\n";
file_put_contents($file, $current, FILE_APPEND);

echo "Log ajouté avec succès.";

// Lecture
if (file_exists($file)) {
    $contenu = file_get_contents($file);
    echo "<h3>Derniers logs :</h3>";
    echo "<div style='background:#f0f0f0; padding:10px; border:1px solid #ccc'>";
    echo nl2br($contenu);
    echo "</div>";
}
?>