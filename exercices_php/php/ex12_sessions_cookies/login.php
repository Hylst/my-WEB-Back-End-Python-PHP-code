<?php
session_start();

if (isset($_POST['user'])) {
    $_SESSION['user'] = $_POST['user'];
    // Un petit cookie pour se souvenir
    setcookie("login_pref", $_POST['user'], time() + (86400 * 30), "/");
    header("Location: dashboard.php");
    exit();
}
?>
<form method="post">
    Login : <input type="text" name="user" value="<?php echo isset($_COOKIE['login_pref']) ? $_COOKIE['login_pref'] : ''; ?>">
    <button type="submit">Entrer</button>
</form>