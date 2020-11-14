
$(document).ready(function() {
  var t = $('#dataTable').DataTable({
    "scrollY": "50vh",
    "paging": false,
    "sScrollX":"100%",
    "bInfo":false,
    "scrollCollapse": true
  });
  var counter = t.column(0).data().length + 1;
  $("#add-row").click(function () {
    t.row.add([
      " <form action='/deleted?id=" + counter + "' method='POST' id='" + counter + "' onsubmit=\"return confirm('Are you sure you want to delete this listing? This action cannot be undone.');\"></form><button form='" + counter + "' class='btn btn-primary'>Delete</button>",
      "<textarea placeholder='" + counter +"' form='main' name='" + counter + ";0' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'>" + counter + "</textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";1' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";2' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";3' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";4' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";5' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";6' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";7' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";8' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";9' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";10' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";11' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";12' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";13' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";14' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";15' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";16' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";17' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";18' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";19' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";20; style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";21' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";22' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";23' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";24' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";25' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";26' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";27' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";28' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";29' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";30' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";31' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";32' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";33' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>",
      "<textarea placeholder='Your text here' form='main' name='" + counter + ";34' style='text-align-last:center;resize:none;border:none;overflow:hidden' rows = 2 cols=20 name='bob' oninput='this.style.height = this.scrollHeight + \"px\"'></textarea>"
    ]
    ).draw();
    counter++;
  });
});


