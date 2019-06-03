/**
 * This file is getting roles and enter mark list
 */
$.ajax({
	type  : 'GET',
	url   : 'student_list/'	
}).done( function(jsondata) {
	var data = JSON.parse(jsondata);
	console.log(data.subject)
	if (data.status == 'Success'){
		var subject_arr = [];
		let sub_len = data.subject.length;
		let html_str = '<tr><th width="150px">S.No</th><th width="150px">Name</th>';
		for(let i=0; i<sub_len; i++){
			html_str += '<th width="150px">'+data.subject[i]['subject_name']+'</th>';
			subject_arr.push(data.subject[i]['subject_name'])
		}
		html_str += '</tr>'
			$('#mark_table_id').append(html_str);
		let html_str_m = '<tr>';
		for(let j=0; j<data.students.length; j++){
			for(let i=0; i<sub_len+2; i++){
				if( i == 0){
					html_str_m += '<td width="150px">'+(j+1)+'</td>'
				}else if(i == 1){
					html_str_m += '<td width="150px">'+data.students[j]['student_name']+'</td>'
				}else{
					console.log(data )
					var dat_index = (subject_arr.indexOf(data.role_data[0]['subject_name']) + 2)
					if(dat_index == i){
						html_str_m += '<td width="150px"><input id="'+subject_arr[i-2]+j+'" class="numberValidate" name="'+subject_arr[i-2]+j+'" Placehodler="Enter Marks" type="number" min="1" ></td>'
					}else{
						html_str_m += '<td width="150px"><input id="'+subject_arr[i-2]+j+'" class="numberValidate" name="'+subject_arr[i-2]+j+'" Placehodler="Enter Marks" type="number" min="1" readonly></td>'
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
		
	}else {
		alert("Error.");
	}
});

/**
 * Submit Marks
 * @returns
 */
function submitMarks(){
	var datas = getFormValues("#mark_form");
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
}

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
			var rank_count = 0, temp_count = 0
			for(let j=0; j<data.rank.length; j++){
				curr_mark = data.rank[j]['student_total']
				if(curr_mark != prev_mark){
					prev_mark = curr_mark
					rank_count ++;
					rank_html += '<td>'+data.rank[j]['student_name']+'</td><td>'+curr_mark+'</td><td>'+(rank_count+temp_count)+'</td>';
					temp_count = 0;
				}
				else{
					rank_html += '<td>'+data.rank[j]['student_name']+'</td><td>'+curr_mark+'</td><td>'+(rank_count)+'</td>';
					temp_count++
				}
				rank_html += '</tr>';
			}

			$('#rank_table_id').append(rank_html);
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



