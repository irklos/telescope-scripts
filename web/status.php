<?php

  $output = shell_exec("ps ax | grep mount.py | wc -l ");

  echo "$output";

?>
