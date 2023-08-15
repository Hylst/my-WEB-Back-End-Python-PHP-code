<?php
session_start();
require 'db.php';

// Protection CSRF Basique
if (!isset($_GET['token']) || $_GET['token'] !== $_SESSION['token']) {
    die("Token de sécurité invalide ! Tentative de CSRF bloquée.");
}

$id = (int)$_GET['id']; // Cast explicite

if ($id > 0) {
    // Suppression
    $stmt = $pdo->prepare("DELETE FROM articles WHERE id = ?");
    $stmt->execute([$id]);
    $_SESSION['flash'] = "Article supprimé.";
}

header("Location: index.php");
?>