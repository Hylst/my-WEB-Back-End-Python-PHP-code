<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title><?php echo isset($titre) ? $titre : "Mon Site"; ?></title>
</head>
<body>
    <header style="background:#eee; padding:10px;">
        <h1><?php echo isset($titre) ? $titre : "Titre"; ?></h1>
        <nav>
            <a href="index.php">Accueil</a> | <a href="contact.php">Contact</a>
        </nav>
    </header>