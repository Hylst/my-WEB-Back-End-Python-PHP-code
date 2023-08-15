<?php
class Article {
    // Les propriétés doivent correspondre aux colonnes DB pour que FETCH_CLASS marche direct
    public $id;
    public $titre;
    public $contenu;
    public $date_creation;
    
    public function getExcerpt() {
        return substr($this->contenu, 0, 100) . '...';
    }
    
    public function getTitre() {
        return strtoupper($this->titre);
    }
}
?>