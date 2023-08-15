<?php
class Database {
    private static $instance = null;
    
    public static function getPdo() {
        if (self::$instance === null) {
            try {
                self::$instance = new PDO('mysql:host=localhost;dbname=blog;charset=utf8', 'root', '', [
                    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
                ]);
            } catch(PDOException $e) {
                die('Erreur SQL : ' . $e->getMessage());
            }
        }
        return self::$instance;
    }
}
?>