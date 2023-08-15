<?php
// On définit des constantes, ça fait plus sérieux
define('DS', DIRECTORY_SEPARATOR);
define('ROOT', __DIR__);
define('PAGES', ROOT . DS . 'pages');

$page = $_GET['page'] ?? 'home';

// Sécurité : on nettoie le chemin pour éviter ../../etc/passwd
$page = str_replace(['/', '.'], '', $page);

$file = PAGES . DS . $page . '.php';

if (file_exists($file)) {
    // On pourrait bufferiser ici aussi mais gardons ça simple pour la v2
    include $file;
} else {
    http_response_code(404);
    echo "<h1>Page introuvable ($page)</h1>";
}
?>