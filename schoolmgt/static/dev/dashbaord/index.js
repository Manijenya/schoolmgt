/**
 * This file is getting roles and enter mark list
 */
var subject_len,student_len;
$.ajax({
	type  : 'GET',
	url   : 'student_list/'	
}).done( function(jsondata) {
	var data = JSON.parse(jsondata);
	console.log(data.subject)
	if (data.status == 'Success'){
		var subject_arr = [];
		sub_len = data.subject.length;
		let html_str = '<tr><th width="150px">S.No</th><th width="150px">Name</th>';
		for(let i=0; i<sub_len; i++){
			html_str += '<th width="150px">'+data.subject[i]['subject_name']+'</th>';
			subject_arr.push(data.subject[i]['subject_name'])
		}
		html_str += '</tr>'
			$('#mark_table_id').append(html_str);
		let html_str_m = '<tr>';
		student_len = data.students.length;
		for(let j=0; j<student_len; j++){
			for(let i=0; i<sub_len+2; i++){
				if( i == 0){
					html_str_m += '<td width="150px">'+(j+1)+'</td>'
				}else if(i == 1){
					html_str_m += '<td width="150px">'+data.students[j]['student_name']+'</td>'
				}else{
					var dat_index = ''
					if($('#user_name').text() != 'admin'){
						dat_index = (subject_arr.indexOf(data.role_data[0]['subject_name']) + 2)
					}
					let st_id = subject_arr[i-2]+[i-2]+'_'+(data.students[j]['id']).toString();
					if(dat_index == i){
						html_str_m += '<td width="150px"><input id="'+st_id+'" '
						html_str_m += 'class="numberValidate" value="0" name="'+st_id+'" Placehodler="Enter Marks" type="number" min="0" ></td>'
					}else{
						if($('#user_name').text() == 'admin'){
							html_str_m += '<td width="150px"><input id="'+st_id+'" class="numberValidate" value="0" name="'+st_id+'" Placehodler="Enter Marks" type="number" min="0" ></td>'
						}else{
							html_str_m += '<td width="150px"><input id="'+st_id+'" class="numberValidate" value="0" name="'+st_id+'" Placehodler="Enter Marks" type="number" min="0" readonly></td>'
						}
					}
				}
			}
			html_str_m += '</tr>'
		}		

		$('#mark_table_id').append(html_str_m);
		$('.numberValidate').on('keypress', function(key) {
			if(key.charCode < 48 || key.charCode > 57) {
				return false;
			}
		});		
		mark_data = data.mark_data
		let mark_len = data.mark_data.length;
		for(let k=0; k<mark_len; k++){
			id = mark_data[k]['subject_name']+(mark_data[k]['subject_id_id']-1)+'_'+(mark_data[k]['student_id_id'])
			$("#" + id).val(mark_data[k]['mark']).trigger("change");
		}

	}else {
		alert("Please Enter All Field.");
	}
	
	$('#total_student').text(student_len);
});


/**
 * Submit Marks
 * @returns
 */

$('#submit_data').click(function(e){
	var datas = getFormValues("#mark_form");
	datas['subject_len'] = subject_len;
	datas['student_len'] = student_len;
	var csrf_data = getCookie('csrf_token');
	$.ajax({
		type  : 'POST',
		url   : 'student_list/',
		data: {
			'datas': JSON.stringify(datas),
			csrfmiddlewaretoken: csrf_data
		},
	}).done( function(jsondata) {
		var data = JSON.parse(jsondata);
		if (data.status == 'Success'){
			alert("Success")
		}else{
			alert("Error")
		}

	});
});


/*
 * Genearte Rank List
 */
function rankList(){
	$.ajax({
		type  : 'GET',
		url   : 'student_list/'	
	}).done( function(jsondata) {
		var data = JSON.parse(jsondata);
		if (data.status == 'Success'){
			var prev_mark = '';
			let rank_html = '<tr>';
			var rank_count = 0, temp_count = 0,pass_student = 0, fail_student = 0;
			for(let j=0; j<data.rank.length; j++){
				curr_mark = data.rank[j]['student_total']
				pass_fail = data.rank[j]['student_pass_fail']
				if(pass_fail){
					if(curr_mark != prev_mark){
						prev_mark = curr_mark
						rank_count ++;
						rank_html += '<td>'+data.rank[j]['student_name']+'</td><td>'+curr_mark+'</td><td>'+(rank_count+temp_count)+'</td><td>Pass</td>';
						temp_count = 0;
					}
					else{
						rank_html += '<td>'+data.rank[j]['student_name']+'</td><td>'+curr_mark+'</td><td>'+(rank_count)+'</td><td>Pass</td>';
						temp_count++
					}
					rank_html += '</tr>';
					pass_student++;
				}else{
					rank_html += '<tr><td>'+data.rank[j]['student_name']+'</td><td>'+curr_mark+'</td><td>-</td><td>Fail</td></tr>';
					fail_student ++;
				}
			}

			$('#rank_table_id').html('').append(rank_html);
			$('#pass_student').text(pass_student);
			$('#fail_student').text(fail_student);
			$('#percentage').text((pass_student/student_len)*100+' %');
			
		}else {
			alert("Error.");
		}
	})
}



/**
 * Get CSRF Cookie Forbidden for POST Method
 * @param name	-	Cookie Name ex: CSRF
 * @returns	Cookie Value of CSRF token
 */
//using jQuery
function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		let cookies = document.cookie.split(';');
		for (let i = 0; i < cookies.length; i++) {
			let cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}



//Form fields clear function 
function form_inputs_clear (form_id){
	var $inputs = $(''+form_id+' :input');// get the form id value
	$inputs.each(function() {
		if (this.name != "csrfmiddlewaretoken") {
			$("#"+this.name).val('').trigger("change");
		} 
	});
	$(form_id).find("select").val(0).trigger('change');
	$(form_id).trigger("reset");
}
//Form value get Function
function getFormValues(formId) {
	var formData= $(formId).serializeArray()
	var form_result_data ={} 
	formData.map(function(data) {
		form_result_data[data['name']] =$.trim(data['value'])})
		return form_result_data
}



