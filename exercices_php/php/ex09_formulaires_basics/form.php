<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        input { margin-bottom: 10px; padding: 5px; }
        button { background: #333; color: white; padding: 5px 10px; border:none; }
    </style>
</head>
<body>
    <h2>Formulaire d'inscription (ou presque)</h2>
    <form action="traitement.php" method="POST">
        <label>Nom :</label> <input type="text" name="nom" placeholder="Ton nom"><br>
        <label>Age :</label> <input type="number" name="age" placeholder="Ton âge"><br>
        <label>Ville :</label> <input type="text" name="ville"><br>
        <button type="submit">Envoyer</button>
    </form>
</body>
</html>