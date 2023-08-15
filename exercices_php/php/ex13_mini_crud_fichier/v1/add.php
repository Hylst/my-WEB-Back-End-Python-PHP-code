<?php
if ($_POST) {
    file_put_contents("data.txt", $_POST['item'] . "\n", FILE_APPEND);
    echo "Ajouté !";
}
?>
<form method="post"><input name="item"><button>Ajouter</button></form>