<?php
// Router artisanal v1 amélioré
// J'ai lu que le switch était plus propre que 50 if/elseif

$page = $_GET['page'] ?? 'home';

// Validons que la page est autorisée (sécurité de base)
$authorized = ['home', 'contact', 'about'];

if (in_array($page, $authorized)) {
    echo "<!DOCTYPE html><html><head><title>MVC V1 - $page</title></head><body>";
    echo "<nav><a href='?page=home'>Home</a> <a href='?page=contact'>Contact</a></nav>";
    echo "<hr>";
    
    switch ($page) {
        case 'home':
            echo "<h1>Accueil</h1><p>Bienvenue sur mon routeur switché.</p>";
            break;
        case 'contact':
            echo "<h1>Contact</h1><p>Pas de formulaire ici, juste du test.</p>";
            break;
        case 'about':
            echo "<h1>A propos</h1><p>C'est moi qui ai fait ce code.</p>";
            break;
    }
    echo "</body></html>";
} else {
    http_response_code(404);
    echo "<h1>404 - Perdu dans les limbes</h1>";
    echo "<a href='?page=home'>Retour maison</a>";
}
?>