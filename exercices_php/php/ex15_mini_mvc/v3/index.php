<?php
define('ROOT', __DIR__);
require 'functions.php';
require 'controller.php';

$action = $_GET['action'] ?? 'index';

// Refacto : routage un peu plus dynamique
if (function_exists($action)) {
    $action();
} else {
    http_response_code(404);
    echo "Action inconnue.";
}
?>