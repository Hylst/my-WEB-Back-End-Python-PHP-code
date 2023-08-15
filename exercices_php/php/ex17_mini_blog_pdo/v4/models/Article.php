<?php
// Classe Entité (Mapping objet)
class Article {
    private $id;
    private $titre;
    private $contenu;
    
    // Getters
    public function getId() { return $this->id; }
    public function getTitre() { return $this->titre; }
    public function getContenu() { return $this->contenu; }
    
    // Setters
    public function setTitre($t) { $this->titre = $t; }
    public function setContenu($c) { $this->contenu = $c; }
    
    // Helper pour affichage
    public function getExcerpt() {
        return substr($this->contenu, 0, 50) . '...';
    }
}
?>