<?php
session_start();
require 'db.php';

// Gestion des messages flash
$flash = $_SESSION['flash'] ?? null;
unset($_SESSION['flash']);

$stmt = $pdo->query("SELECT * FROM articles");
$articles = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>
<!DOCTYPE html>
<html>
<body>
    <?php if($flash): ?>
        <div style="background: #d4edda; color: #155724; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
            <?= $flash ?>
        </div>
    <?php endif; ?>
    
    <a href="add.php">Ajouter un article</a>
    
    <!-- Liste des articles... -->
</body>
</html>