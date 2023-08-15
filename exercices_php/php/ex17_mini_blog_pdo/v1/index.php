<?php
require 'db.php';
$stmt = $pdo->query("SELECT * FROM articles ORDER BY id DESC"); // Plus récent en premier
$articles = $stmt->fetchAll(PDO::FETCH_ASSOC);

// Formatter de date 'intl' (plus propre que date())
$fmt = new IntlDateFormatter('fr_FR', IntlDateFormatter::LONG, IntlDateFormatter::NONE);
?>
<!DOCTYPE html>
<html>
<head>
    <style>
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
        .card { border: 1px solid #ddd; padding: 15px; border-radius: 8px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
        h2 { margin-top: 0; }
        .date { font-size: 0.8em; color: #666; }
    </style>
</head>
<body>
    <h1>Mon Blog V1 (Grid CSS)</h1>
    <div class="grid">
        <?php foreach($articles as $a): ?>
            <div class="card">
                <h2><?php echo htmlspecialchars($a['titre']); ?></h2>
                <p class="date">Publié le <?php echo $fmt->format(new DateTime($a['date_creation'] ?? 'now')); ?></p>
                <p><?php echo nl2br(htmlspecialchars(substr($a['contenu'], 0, 100))) . '...'; ?></p>
            </div>
        <?php endforeach; ?>
    </div>
</body>
</html>