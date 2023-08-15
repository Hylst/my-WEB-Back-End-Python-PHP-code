<?php
$msg = "";
$msg_class = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Un peu de sécu quand même
    $nom = htmlspecialchars(trim($_POST['nom'])); // Trim c'est mieux
    $email = filter_input(INPUT_POST, 'email', FILTER_VALIDATE_EMAIL);
    
    // Regex simple pour verifier que le nom n'a pas de chiffres
    if (!preg_match("/^[a-zA-Z-' ]*$/", $nom)) {
        $msg = "Seuls les lettres et espaces sont autorisés dans le nom !";
        $msg_class = "error";
    } elseif ($nom && $email) {
        $msg = "Reçu 5 sur 5, $nom. Email valide.";
        $msg_class = "success";
    } else {
        $msg = "Données invalides.";
        $msg_class = "error";
    }
}
?>
<!DOCTYPE html>
<html>
<head>
    <style>
        .error { color: red; font-weight: bold; }
        .success { color: green; }
    </style>
</head>
<body>
    <h1>Formulaire V2 (Secure)</h1>
    <?php if ($msg) echo "<p class='$msg_class'>$msg</p>"; ?>
    
    <form method="POST">
        Nom : <input type="text" name="nom" required value="<?php echo isset($nom) ? $nom : ''; ?>"><br>
        Email : <input type="email" name="email" required value="<?php echo isset($email) ? $email : ''; ?>"><br>
        <button type="submit">Go</button>
    </form>
</body>
</html>