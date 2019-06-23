<?php

$host    = "127.0.0.1";

$port    = 5555;
if (isset($_GET['ra']) && $_GET['dec']){

$message = '2 '.$_GET['ra'].' '.$_GET['dec'].' ' ;

#echo "Message To server :".$message;

// create socket

$socket = socket_create(AF_INET, SOCK_STREAM, 0) or die("Could not create socket\n");

// connect to server

$result = socket_connect($socket, $host, $port) or die("Could not connect to server\n");  

// send string to server

socket_write($socket, $message, strlen($message)) or die("Could not send data to server\n");
}
// get server response
$result = socket_connect($socket, $host, $port) or die("Could not connect to server\n");


socket_close($socket);
?>
