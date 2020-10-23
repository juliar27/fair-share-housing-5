// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').DataTable({
    "scrollY": "500px",
    "paging": false,
    "sScrollX":"100%",
    "scrollCollapse": true
  });
});
