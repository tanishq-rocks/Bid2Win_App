let successfully = () => {
    // alert("Success");
    $container.empty().append(`<div class="alert alert-primary alert-dismissible fade show" role="alert">Thanks for using our service
    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
    <span aria-hidden="true">&times;</span>
  </button></div>`);
  temp1();
}

let failure = () => {
    $container.empty().append(`<div class="alert alert-primary alert-dismissible fade show" role="alert">Sorry for Inconvenience, for any query mail us
    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
    <span aria-hidden="true">&times;</span>
  </button></div>`
	)
	temp1();
}