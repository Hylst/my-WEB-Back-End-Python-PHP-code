<?php
// Petit script pour tester la co sans tout casser
require 'config.php';

echo "Test de connexion vers " . DB_NAME . "...<br>";

try {
    $dsn = "mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=utf8";
    $pdo = new PDO($dsn, DB_USER, DB_PASS, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
    
    echo "<span style='color:green'>Connexion OK !</span><br>";
    
    // Test version MySQL
    $version = $pdo->query("SELECT VERSION()")->fetchColumn();
    echo "Version MySQL : " . $version;
    
} catch (PDOException $e) {
    echo "<span style='color:red'>Erreur critique : " . $e->getMessage() . "</span>";
}
?>