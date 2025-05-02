<?php
$data = file_get_contents("php://input");
file_put_contents("procesos.txt", $data);
?>
