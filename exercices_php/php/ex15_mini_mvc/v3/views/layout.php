<!DOCTYPE html>
<html>
<head>
    <title><?= $titre ?? 'Mon Site MVC' ?></title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; max-width: 800px; margin: auto; padding: 20px; }
        nav { background: #333; padding: 10px; margin-bottom: 20px; }
        nav a { color: white; text-decoration: none; margin-right: 15px; }
        footer { margin-top: 50px; font-size: 0.8em; color: #777; border-top: 1px solid #ddd; padding-top: 10px; }
    </style>
</head>
<body>
    <nav>
        <a href="index.php?action=index">Accueil</a>
        <a href="index.php?action=contact">Contact</a>
    </nav>
    
    <div class="content">
        <?= $content ?>
    </div>

    <footer>
        MVC fait maison - <?= date('Y') ?>
    </footer>
</body>
</html>