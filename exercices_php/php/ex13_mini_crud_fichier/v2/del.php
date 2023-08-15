<?php
$id = $_GET['id'];
$lignes = file("../v1/data.txt"); // oups chemin
// TODO : gérer la suppression... c'est galère en fichier texte
unset($lignes[$id]);
file_put_contents("data.txt", implode("", $lignes));
echo "Supprimé.";
?>