<?php
require 'Autoloader.php';
Autoloader::register();

// On suppose que l'autoloader trouve ArticleManager et Database à la racine
// et Article dans models/ (faudrait améliorer l'autoloader pour les dossiers, mais bon pour l'instant je déplace Article à la racine pour faire simple ou je modifie le require)

// Simplification : tout à la racine pour v4
$manager = new ArticleManager();
// On récupère en mode objet maintenant !
$articles = $manager->getAllObjects(); 
?>
<h1>Blog Objet V4</h1>
<?php foreach($articles as $article): ?>
    <article>
        <h2><?= htmlspecialchars($article->getTitre()) ?></h2>
        <p><?= htmlspecialchars($article->getExcerpt()) ?></p>
    </article>
<?php endforeach; ?>