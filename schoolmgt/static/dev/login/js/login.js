/**
 * This function for get all details from login form
 * @param formId form div ID
 * @returns key and value result 
 */
function getFormValues(formId) {
	var formData = $(formId).serializeArray();
	var form_result_data = {}; 
	formData.map(data => {form_result_data[data['name']] = data['value'] })
	return form_result_data;
}

/**
 * Login Form Submit funciton
 * @param event
 * @returns
 */
$("#login_form").submit(function( event ) {
	event.preventDefault();
	var datas = getFormValues("#login_form");
	console.log(datas)
	var	csrf_data = datas.csrfmiddlewaretoken;
	//if (login_form_validation()){
		var actionurl = window.location.href;
		console.log("actionurl",actionurl)
		$.ajax({
			type  : 'POST',
			url   : actionurl,
			async : false,
			data: {
				'datas': JSON.stringify(datas),
				csrfmiddlewaretoken: csrf_data
			},
		}).done( function(jsondata) {
			var data = JSON.parse(jsondata);
			console.log(data)
			if (data.status == 'Success'){
				//localStorage.setItem('username', data.username);
				//localStorage.setItem('role_name', data.role_name);
				window.location.href = '/School/';
			}else {
				alert("User name or Password Doesn't match.");
			}
		});
});



/**
 * Login Form Validation 
 * @returns true or false
 */
function login_form_validation(){
	return $('#login_form').valid();
}

/**
 * Jquery valdiation for login
 */
$("#login_form").validate({
	rules: {
		username:{
			required: true,
		},
		password:{
			required: true,
		},
	},
	//For custom messages
	messages: {
		username:{
			required:"Please Enter User Name",
		},
		password:{
			required:"Please Enter Password",
		},
	},
	errorElement: 'div',
	errorPlacement: function(error, element) {
		var placement = $(element).data('error');
		if (placement) {
			$(placement).append(error);
		} else {
			error.insertAfter(element);
		}
	}
});