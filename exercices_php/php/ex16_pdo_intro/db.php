<?php
require 'config.php';

$dsn = "mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=utf8";
$options = [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
];

try {
    $pdo = new PDO($dsn, DB_USER, DB_PASS, $options);
    echo "Connexion réussie à la BDD.";
} catch (PDOException $e) {
    // On log l'erreur mais on affiche un message propre au user
    error_log($e->getMessage());
    die("Erreur de connexion (voir logs)");
}
?>