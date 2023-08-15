<?php
require_once 'Database.php';
require_once 'Article.php'; // Si autoloader galère avec les dossiers

class ArticleManager {
    private $pdo;
    
    public function __construct() {
        $this->pdo = Database::getPdo();
    }
    
    // Récupération sous forme d'objets Article
    public function getAllObjects() {
        $stmt = $this->pdo->query("SELECT * FROM articles");
        // FETCH_CLASS magique de PDO
        return $stmt->fetchAll(PDO::FETCH_CLASS, 'Article');
    }
}
?>