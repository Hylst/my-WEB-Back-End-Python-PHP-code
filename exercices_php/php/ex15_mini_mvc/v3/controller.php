<?php
function render($view, $data = []) {
    extract($data);
    
    // On capture le contenu de la vue
    ob_start();
    include "views/$view.php";
    $content = ob_get_clean();
    
    // On l'injecte dans le layout
    include "views/layout.php";
}

function index() {
    render('home', ["titre" => "Accueil - MVC"]);
}

function contact() {
    render('contact', ["titre" => "Contactez-nous"]);
}
?>