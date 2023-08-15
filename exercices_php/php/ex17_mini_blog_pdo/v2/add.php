<?php
session_start();
require 'db.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $titre = trim($_POST['titre']);
    $contenu = trim($_POST['contenu']);
    $erreurs = [];

    if (strlen($titre) < 5) $erreurs[] = "Le titre est trop court.";
    if (empty($contenu)) $erreurs[] = "Le contenu ne peut pas être vide.";

    if (empty($erreurs)) {
        $sql = "INSERT INTO articles (titre, contenu, date_creation) VALUES (?, ?, NOW())";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([$titre, $contenu]);
        
        $_SESSION['flash'] = "Article publié avec succès !";
        header("Location: index.php");
        exit;
    }
}
?>
<!DOCTYPE html>
<html>
<body>
    <h1>Nouvel Article</h1>
    <?php if (!empty($erreurs)): ?>
        <div style="color:red">
            <?php foreach($erreurs as $e) echo "<p>$e</p>"; ?>
        </div>
    <?php endif; ?>
    
    <form method="post">
        <input name="titre" placeholder="Titre (min 5 chars)" value="<?= $_POST['titre'] ?? '' ?>"><br>
        <textarea name="contenu" placeholder="Contenu..."><?= $_POST['contenu'] ?? '' ?></textarea><br>
        <button>Publier</button>
    </form>
</body>
</html>