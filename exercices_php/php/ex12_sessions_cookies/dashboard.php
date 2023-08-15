<?php
session_start();
if (!isset($_SESSION['user'])) {
    header("Location: login.php?error=access_denied");
    exit();
}

// Compteur de visites dans la session
if (!isset($_SESSION['visites'])) {
    $_SESSION['visites'] = 0;
}
$_SESSION['visites']++;

?>
<!DOCTYPE html>
<html>
<body>
    <h1>Bienvenue <?php echo htmlspecialchars($_SESSION['user']); ?></h1>
    <p>C'est votre <?php echo $_SESSION['visites']; ?>e page vue cette session.</p>
    
    <?php if (isset($_COOKIE['login_pref'])): ?>
        <p><small>On se souvient de vous via cookie.</small></p>
    <?php endif; ?>
    
    <a href="logout.php">Se déconnecter</a>
</body>
</html>