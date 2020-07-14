
function showCustForm() {
	document.getElementById('AddCustForm').hidden = false;
	document.getElementById('AddCustButton').hidden = true;
}

function showProdForm() {
	document.getElementById('AddProdForm').hidden = false;
	document.getElementById('AddProdButton').hidden = true;
}

function editProd(rownum){
	document.getElementsByName("Product")[0].value = "Update";
	document.getElementsByName("Pid")[0].value = document.getElementById("Pid"+rownum).textContent;
	document.getElementsByName("name")[0].value = document.getElementById("name"+rownum).textContent;
	document.getElementsByName("price")[0].value = document.getElementById("price"+rownum).textContent;
	document.getElementsByName("stock")[0].value = document.getElementById("curinv"+rownum).textContent;
	document.getElementsByName("desc")[0].value = "";
	showProdForm();
}

function editCust(rownum){
	document.getElementsByName("Customer")[0].value = "Update";
	document.getElementsByName("id")[0].value = document.getElementById("id"+rownum).textContent;
	document.getElementsByName("fname")[0].value = document.getElementById("fName"+rownum).textContent;
	document.getElementsByName("lname")[0].value = document.getElementById("lName"+rownum).textContent;
	document.getElementsByName("email")[0].value = document.getElementById("emailAdr"+rownum).textContent;
	showCustForm();
}

function cancelCust() {
	cancelForm("Cust");
}

function cancelProd() {
	cancelForm("Prod");
}

function cancelForm(val){
	var fields = document.getElementsByClassName(val);
	for (var i = 1; i < fields.length; i++){
		fields[i].value = "";
	};
	document.getElementsByName("Customer")[0].value = "Add";
	document.getElementById('Add'+val+'Form').hidden = true;
	document.getElementById('Add'+val+'Button').hidden = false;
}