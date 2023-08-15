<?php
// Petite bibliothèque de fonctions utiles
function dd($var) {
    echo "<pre style='background:#222;color:#0f0;padding:10px;'>";
    var_dump($var);
    echo "</pre>";
    die(); // Dump and Die
}

function e($string) {
    return htmlspecialchars($string, ENT_QUOTES);
}

function redirect($url) {
    header("Location: $url");
    exit();
}
?>