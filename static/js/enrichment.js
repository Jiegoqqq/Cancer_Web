// $.ajaxSetup({
// 	headers: { 'X-CSRFToken': csrf_token },
// 	type: 'POST',
// });

$(document).ready(function(){
	console.log('enrichment.js');
	$("#comparison_table").hide();
	document.addEventListener('DOMContentLoaded', function () {
		// 獲取 POST 參數
		var data = decodeURIComponent(window.location.search.split('seq=')[1]);
		var corMethod = decodeURIComponent(window.location.search.split('cor_type=')[1]);
		var pValue = decodeURIComponent(window.location.search.split('p_limit=')[1]);
		// 做其他的處理，例如顯示資料
		console.log('Data:', data);
		console.log('Correlation Method:', corMethod);
		console.log('P-Value:', pValue);
	});

    $("#btn_cal").click(function(){
        // var seq = $("#input_seq_content").val();
        var dataTable = $('#output_table').DataTable(); // 假設 DataTable 的 ID 是 'example'
        var seq = dataTable.column(0, {page: 'all'}).data().toArray();
		var seq = seq.join(',');
		console.log(seq);

        var Correction = $("#c_type_enrich").val();
        var p_limit = $("#p-value_enrich").val();
		var c_type = $("#c_type").val();

        $.ajax({
			headers: { 'X-CSRFToken': csrf_token },
			url: '/enrichment_app/enrichment_ajax/',
			type: 'POST',
			dataType: "json",
			data: {
				"seq":seq,
                "Correction":Correction,
                "p_limit":p_limit,
			},
            beforeSend:function(){
                var count=0
                tID= setInterval(timedCount , 50);
                    function timedCount() {
                    count=count+0.05;
                    swal({
                        title: "Running...",
                        text: "It may take several minutes.\nPlease be patient.\n \nRunning time: "+parseInt(count)+" seconds\nClick anywhere of the page \nif the running time does not change",                       
                        button: false,
                    });
                };
            }, 
			success: function(response){
                clearInterval(tID);
                delete tID
                swal.close();
                data = response.enrichment_result
				$("#relate_table").DataTable({
					destroy : true,
					data: data,
					columns:[
						{ title: 'mirna_name', data: 'mirna_name' },
						{ title: '-log10(corrected P-value)' },
						{ title: 'FDR' , data: 'FDR'},
						{ title: 'Bonferroni', data: 'Bonferroni'},
						{ title: 'Expected Ratio'},
						{ title: 'Observed Ratio'},
						{ title: 'Fold Enrichment'},						
					],
					columnDefs: [
						{
							// 指定第一列，從0開始，0表示第一列，1表示第二列……
							targets: 1,
							render: function(data, type, row, meta) {
								return -Math.log10(row['P-value']).toFixed(4);
							},
						},
                        {
							// 指定第一列，從0開始，0表示第一列，1表示第二列……
							targets: 4,
							render: function(data, type, row, meta) {
								return `${row['C']} / ${row['D']} = ${row['expected_ratio'].toFixed(4)}`
							},
						},
                        {
							// 指定第一列，從0開始，0表示第一列，1表示第二列……
							targets: 5,
							render: function(data, type, row, meta) {
								return `${row['A']} / ${row['B']} = ${row['observed_ratio'].toFixed(4)}`
							},
						},
						{
							// 指定第一列，從0開始，0表示第一列，1表示第二列……
							targets: 6,
							render: function(data, type, row, meta) {
								var value = row['observed_ratio'] / row['expected_ratio']
								return Number(value.toFixed(4));
							},
						},
					],
				});

				//只出現自己選擇的過濾評分項
				if(c_type == "FDR"){
					$("#relate_table").DataTable().column(1).visible(false);
					$("#relate_table").DataTable().column(2).visible(true);
					$("#relate_table").DataTable().column(3).visible(false);
				}
				else if(c_type == "Bonferroni"){
					$("#relate_table").DataTable().column(1).visible(false);
					$("#relate_table").DataTable().column(2).visible(false);
					$("#relate_table").DataTable().column(3).visible(true);
				}
				else{
					$("#relate_table").DataTable().column(1).visible(true);
					$("#relate_table").DataTable().column(2).visible(false);
					$("#relate_table").DataTable().column(3).visible(false);
				}
            },
            error: function(xhr, ajaxOptions, thrownError){
				alert(thrownError);
				clearInterval(tID);
				delete tID
				swal.close();
				swal('error')
			},
        });
    });
});