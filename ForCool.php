<?php
include_once 'ConnDB.php';
$db = new DB_Class();

if($_GET) {
  //Quer your data base
  $query = "SELECT DATE_FORMAT(date_time,'%c-%e %H:%i')
           as date_time, measure
            FROM tandd
            WHERE name = 'cool'
            ORDER BY date_time
            ASC";

    $result = mysql_query( $query );
    $rows = array();

    while( $row = mysql_fetch_array( $result ) ) {
        $rows[] = array( '0' => $row['0'] , '1' => $row['1'] );
    }
//change to the required json format
    echo json_encode($rows, JSON_NUMERIC_CHECK);
}
?>
