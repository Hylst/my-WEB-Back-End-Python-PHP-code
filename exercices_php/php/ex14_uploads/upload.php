<?php
$msg = "";
if (isset($_FILES['fichier'])) {
    $dossier = 'uploads/';
    if (!is_dir($dossier)) mkdir($dossier);
    
    $fichier = basename($_FILES['fichier']['name']);
    $taille_max = 2000000; // 2Mo
    $taille = $_FILES['fichier']['size'];
    $ext = strtolower(pathinfo($fichier, PATHINFO_EXTENSION));
    
    $extensions_autorisees = ['jpg', 'jpeg', 'png', 'gif', 'pdf'];
    
    if (in_array($ext, $extensions_autorisees)) {
        if ($taille <= $taille_max) {
             // On renomme pour éviter les écrasements
             $nouveau_nom = uniqid() . '.' . $ext;
             if (move_uploaded_file($_FILES['fichier']['tmp_name'], $dossier . $nouveau_nom)) {
                $msg = "Upload réussi : <a href='$dossier$nouveau_nom' target='_blank'>Voir le fichier</a>";
            } else {
                $msg = "Echec de l'upload.";
            }
        } else {
            $msg = "Fichier trop gros ! (Max 2Mo)";
        }
    } else {
        $msg = "Format interdit ! (Uniquement images et PDF)";
    }
}
?>
<!DOCTYPE html>
<html>
<body>
    <h1>Upload de fichiers</h1>
    <?php if($msg) echo "<p>$msg</p>"; ?>
    <form method="post" enctype="multipart/form-data">
        Fichier (Max 2Mo, img/pdf) : <br>
        <input type="file" name="fichier"><br><br>
        <button>Envoyer</button>
    </form>
</body>
</html>