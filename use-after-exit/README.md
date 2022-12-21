# Use After Exit

## Description
Author: @carlopolop#3938

It's as easy as it looks, isn't it?

Press the Start button on the top-right to begin this challenge.

Special thank you to Snyk for sponsoring NahamCon EU CTF 2022! This challenge is dedicated to them as a token of gratitude. 

## Solve
The following PHP code is runing on the server:
```php
 <?php
error_reporting(0);
if (isset($_POST['submit'])) {
    $file_name = urldecode($_FILES['file']['name']);
    $tmp_path = $_FILES['file']['tmp_name'];
    if(strpos($file_name, ".jpg") == false){
        echo "Invalid file name";
        exit(1);
    }
    $content = file_get_contents($tmp_path);
    $all_content = '<?php exit(0);'. $content . '?>';
    $handle = fopen($file_name, "w");
    fwrite($handle, $all_content);
    fclose($handle);
    echo "Done.";
}
else{
    show_source(__FILE__);
}
?> 
```

## Flag