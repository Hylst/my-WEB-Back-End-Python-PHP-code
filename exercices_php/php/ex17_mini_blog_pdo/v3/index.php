<?php
session_start();
require 'db.php';

// Génération token pour la session
if (empty($_SESSION['token'])) {
    $_SESSION['token'] = bin2hex(random_bytes(32));
}

// ... récupération articles ...
?>
<!-- ... dans la boucle foreach ... -->
<a href="delete.php?id=<?= $a['id'] ?>&token=<?= $_SESSION['token'] ?>" onclick="return confirm('Confirmer ?')">Supprimer clean</a>