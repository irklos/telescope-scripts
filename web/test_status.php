<?php

$host    = "127.0.0.1";

$port    = 5555;

$message = "3";

#echo "Message To server :".$message;

// create socket

$socket = socket_create(AF_INET, SOCK_STREAM, 0) or die("Could not create socket\n");

// connect to server

$result = socket_connect($socket, $host, $port) or die("Could not connect to server\n");  

// send string to server

socket_write($socket, $message, strlen($message)) or die("Could not send data to server\n");

// get server response

$result = socket_read ($socket, 30) or die("Could not read server response\n");
$array = explode(" ", $result);
if (isset($_GET['val'])){
if ($_GET['val']=='ra') 
echo $array[1];
if ($_GET['val']=='dec')
echo $array[2];
}

//echo " planetarium.addPointer({
//                'ra':"+$array[2]+",
//                'dec':"+$array[3]+",
//                'label':'Telescope',
//                'colour':'rgb(255,220,220)'
//        })"


// close socket

socket_close($socket);
?>
