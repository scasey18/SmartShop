  $(document).ready(function () {
    $('#same-address').change(function () {
      if (this.checked) {
        $('#billingAddressDiv').hide();
        $('#billingInfoDiv').hide();
		$('#billingZip').removeAttr("required");
      } else {
        $('#billingAddressDiv').show();
        $('#billingInfoDiv').show();
      }
    });
  });
