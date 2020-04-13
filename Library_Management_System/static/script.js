$(document).ready(function () {
     $('#showpwd').on('click', function () {
          if ($('#pwd').attr('type') == 'password') {
               $('#pwd').attr('type', 'text');
          }
          else {
               $('#pwd').attr('type', 'password');
          }
     })
});