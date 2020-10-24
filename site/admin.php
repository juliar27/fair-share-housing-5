 <!DOCTYPE html>
<html lang="en">

  <head>

   <meta charset="utf-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
        <meta name="description" content="" />
        <meta name="author" content="" />
        <title>mapFSH: Admin</title>
        <link rel='icon' href='static/images/favicon.ico' type='image/x-icon' >
        <link href="static/css/styles-admin.css" rel="stylesheet" />
        <link href="https://fonts.googleapis.com/css?family=Nunito+Sans:200,300,400,600,700,800,900&display=swap" rel="stylesheet">
        <link href="https://cdn.datatables.net/1.10.20/css/dataTables.bootstrap4.min.css" rel="stylesheet" crossorigin="anonymous" />
        <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.13.0/js/all.min.js" crossorigin="anonymous"></script>

      </head>


    <body class="sb-nav-fixed">

     <nav class="sb-topnav navbar navbar-expand navbar-dark bg-dark">
            <a class="navbar-brand" href="/">mapFSH</a>
            <button class="btn btn-link btn-sm order-1 order-lg-0" id="sidebarToggle" href="#"><i class="fas fa-bars"></i></button>
            <!-- Navbar Search-->
            <form class="d-none d-md-inline-block form-inline ml-auto mr-0 mr-md-3 my-2 my-md-0">
                <div class="input-group">
                    <input class="form-control" type="text" placeholder="Search for..." aria-label="Search" aria-describedby="basic-addon2" />
                    <div class="input-group-append">
                        <button class="btn btn-primary" type="button"><i class="fas fa-search"></i></button>
                    </div>
                </div>
            </form>
            <!-- Navbar-->
            <ul class="navbar-nav ml-auto ml-md-0">
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" id="userDropdown" href="#" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><i class="fas fa-user fa-fw"></i></a>
                    <div class="dropdown-menu dropdown-menu-right" aria-labelledby="userDropdown">
                        <a class="dropdown-item" href="#">Settings</a>
                        <a class="dropdown-item" href="#">Activity Log</a>
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item" href="login">Logout</a>
                    </div>
                </li>
            </ul>
        </nav>
        <div id="layoutSidenav">
            <div id="layoutSidenav_nav">
                <nav class="sb-sidenav accordion sb-sidenav-dark" id="sidenavAccordion">
                    <div class="sb-sidenav-menu">
                        <div class="nav">
                            <div class="sb-sidenav-menu-heading">Core</div>
                            <a class="nav-link" href="admin">
                                <div class="sb-nav-link-icon"><i class="fas fa-tachometer-alt"></i></div>
                                Dashboard
                            </a>
                            <div class="sb-sidenav-menu-heading">Data</div>
                            <a class="nav-link" href="upload">
                                <div class="sb-nav-link-icon"><i class="fas fa-upload"></i></div>
                                Upload Data
                            </a>
                            <a class="nav-link" href="add">
                                <div class="sb-nav-link-icon"><i class="fas fa-edit"></i></div>
                                Add Data
                            </a>
                            <a class="nav-link" href="tables">
                                <div class="sb-nav-link-icon"><i class="fas fa-table"></i></div>
                                Edit Data
                            </a>
                            <a class="nav-link" href="download">
                                <div class="sb-nav-link-icon"><i class="fas fa-download"></i></div>
                                Download Data
                            </a>
                        </div>
                    </div>
                    <div class="sb-sidenav-footer">
                        <div class="small">Logged in as:</div>
                        Test User
                    </div>
                </nav>
            </div>
            <div id="layoutSidenav_content">
                <main>

 <?php

// session_start();
// if (!isset($_SESSION['count'])) {
//  $_SESSION['count'] = 0;
// }
// $_SESSION['count']++;
//
// echo "Hello #" . $_SESSION['count'];

require 'SharedConfigurations.php';

// This example demonstrates how to leverage Predis to save PHP sessions on Redis.
//
// The value of `session.gc_maxlifetime` in `php.ini` will be used by default as the
// the TTL for keys holding session data on Redis, but this value can be overridden
// when creating the session handler instance with the `gc_maxlifetime` option.
//
// Note that this class needs PHP >= 5.4 but can be used on PHP 5.3 if a polyfill for
// SessionHandlerInterface (see http://www.php.net/class.sessionhandlerinterface.php)
// is provided either by you or an external package like `symfony/http-foundation`.

if (!interface_exists('SessionHandlerInterface')) {
    die("ATTENTION: the session handler implemented by Predis needs PHP >= 5.4.0 or a polyfill ".
        "for \SessionHandlerInterface either provided by you or an external package.\n");
}

// Instantiate a new client just like you would normally do. We'll prefix our session keys here.
$client = new Predis\Client($single_server, array('prefix' => 'sessions:'));

// Set `gc_maxlifetime` so that a session will be expired after 5 seconds since last access.
$handler = new Predis\Session\SessionHandler($client, array('gc_maxlifetime' => 5));

// Register our session handler (it uses `session_set_save_handler()` internally).
$handler->register();

// Set a fixed session ID just for the sake of our example.
session_id('example_session_id');

session_start();

if (isset($_SESSION['foo'])) {
    echo "Session has `foo` set to {$_SESSION['foo']}\n";
} else {
    $_SESSION['foo'] = $value = mt_rand();
    echo "Empty session, `foo` has been set with $value\n";
}

?>

                </main>
                <footer class="py-4 bg-light mt-auto">
                    <div class="container-fluid">
                        <div class="d-flex align-items-center justify-content-between small">
                            <div class="text-muted">Copyright &copy; Your Website 2020</div>
                            <div>
                                <a href="#">Privacy Policy</a>
                                &middot;
                                <a href="#">Terms &amp; Conditions</a>
                            </div>
                        </div>
                    </div>


</footer>
            </div>
        </div>
        <script src="https://code.jquery.com/jquery-3.5.1.min.js" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.bundle.min.js" crossorigin="anonymous"></script>
        <script src="static/js/scripts-admin.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.min.js" crossorigin="anonymous"></script>
        <script src="static/assets/demo/chart-area-demo.js"></script>
        <script src="static/assets/demo/chart-bar-demo.js"></script>
        <script src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js" crossorigin="anonymous"></script>
        <script src="https://cdn.datatables.net/1.10.20/js/dataTables.bootstrap4.min.js" crossorigin="anonymous"></script>
        <script src="static/assets/demo/datatables-demo.js"></script>


    </body>
</html>