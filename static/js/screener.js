function construct_prediction_datatable(name, search_type, data, sur_cor, high_percentile, low_percentile, stage, cancer, switch_dict, selected_miRNA, DE_info_dict)
{
    //// Dynamically add/remove datatable column&data using ajax.
    // without if condition will raise error about reinitialise(Cannot read property 'aDataSort' of undefined)
    if ( $.fn.DataTable.isDataTable( `#${name}` ) ) {
        $(`#${name}`).DataTable().destroy();
        $(`#${name}`).empty();
    };
    // colspan column
    var headers = '<thead><tr><th colspan="1">Name</th>'
    // <th colspan="2">Title</th><th colspan="2">1</th><th colspan="2">2</th><th colspan="2">3</th><th colspan="2">4</th><th colspan="2">5</th><th colspan="2">6</th><th colspan="2">7</th><th colspan="2">8</th></tr>';
    // default columns
    var columns = [{ title:`${search_type}`, data: "name"}];
    var columnDefs = []
    var target_index = 1;
    // create survival analysis columns and columnDefs
    if(switch_dict.survival == true){
        headers += '<th colspan="2">survival analysis</th>';
        if(sur_cor == "None"){
            columns.push({ title:"survival analysis logrank p-value", data: "logrank_p_value"})
        }
        else{
            columns.push({ title:`${sur_cor} correction p-value`, data: `${sur_cor}`})
        }
        columns.push(
            { title:"survival analysis detail"},
        );
        columnDefs.push(
            {
                // 指定第一列，從0開始，0表示第一列，1表示第二列……
                targets: target_index ,
                autoWidth: true,
                render: function(data, type, row, meta) {
                    // console.log(typeof data);
                    if (type === 'display' && typeof data === 'number') {
                        return Number(data.toFixed(4)).toExponential(3);
                    }
                    return data;
                },
            },
            // {
            //     // 指定第一列，從0開始，0表示第一列，1表示第二列……
            //     targets: target_index + 1 ,

            //     autoWidth: true,
            //     render: function(data, type, row, meta) {
            //         // console.log(typeof data);
            //         if (type === 'display' && typeof data === 'number') {
            //             return Number(data.toFixed(6)).toExponential();
            //         }
            //         return data;
            //     },
            // },
            {
                // 指定第一列，從0開始，0表示第一列，1表示第二列……
                targets: target_index + 1,
                autoWidth: true,
                render: function(data, type, row, meta) {
                    // if id has space or : or . it can not be use
                    // var title = meta.settings.aoColumns[meta.col-2].sTitle;
                    // console.log(title)
                    // var name = row[title];
                    var name = row["name"]; // 後面的key是用data:後的名稱
                    return `<a href="/survival_analysis/detail/?cancer=${cancer}&type=${search_type}&name=${name}&hp=${high_percentile}&lp=${low_percentile}&stage=${stage}" target="_blank">view</a>`
                },
            },
        );
        target_index += 2;
    }
    // create miRNA columns and columnDefs
    if(switch_dict.miRNA == true){
        headers += `<th colspan="${selected_miRNA.length}">miRNA</th>`;
        selected_miRNA.forEach((miRNA) => {
            columns.push(
                { title:`${miRNA}`, data: `${miRNA}`}
            );
        });
        target_index += selected_miRNA.length;
    }
    // create DE columns and columnDefs
    if(switch_dict.DE == true){
        headers += `<th colspan="4">DE</th>`;
        columns.push(
            { title:`${DE_info_dict["condition2"]} Avg FPKM(cond2)`, data: `avg_s_FPKM`},
            { title:`${DE_info_dict["condition1"]} Avg FPKM(cond1)`, data: `avg_f_FPKM`},
            { title:`Fold Change(cond2/cond1)`, data: `foldchange`},
            { title:`q-value`, data: `q-value`},
        );
        columnDefs.push(
            {
                // 指定第一列，從0開始，0表示第一列，1表示第二列……
                targets: target_index +3,
                autoWidth: true,
                render: function(data, type, row, meta) {
                    // console.log(typeof data);
                    if (type === 'display' && typeof data === 'number') {
                        return Number(data.toFixed(4)).toExponential(3);
                    }
                    return data;
                },
            },
        );
        target_index += 4;
        data.forEach(item => {
            item.avg_s_FPKM = item.avg_s_FPKM.toFixed(5);
            item.avg_f_FPKM = item.avg_f_FPKM.toFixed(5);
            item.foldchange = item.foldchange.toFixed(5);
            item['q-value'] = item['q-value'].toFixed(5);
        });
    }
    // $(`#${name}`).append(headers);
    $(`#${name}`).DataTable({
        // 'scrollX':true, will split header and data, it will cause header and data misalign
        // datatable size will auto Resizes with the window
        "initComplete": function (settings, json) {  
            $(`#${name}`).wrap("<div style='overflow:auto; width:100%;position:relative;'></div>");            
        },
        // bSort: false,
        order: [[0, 'asc']],
        destroy : true,
        data: data,
        columns: columns,
        columnDefs: columnDefs,
        dom: 'Bfrtip',
        buttons: [{
            extend: 'csv',
            text: 'Export CSV',
            title: `${cancer}_${search_type}_${stage}_${high_percentile}_${low_percentile}`,
            exportOptions: {
                columns: [0, 1]
                // columns: [0]
            }
        }],
        
    });
}

function select_function(){
	var select_test = document.getElementById("TEST_select").value;
	var test_state = document.getElementById("TESTstates_select");
	if(select_test=='Cuffdiff DE test'){
		test_state[0].style.display="none";
		test_state[1].style.display="none";
		test_state[2].style.removeProperty('display');
		test_state[2].selected = 'selected';
	}
	else{
		test_state[0].selected = 'selected';
		test_state[0].style.removeProperty('display');
		test_state[1].style.removeProperty('display');
		test_state[2].style.display="none";
	}
}

function getSelectedCheckboxes(area) {
    var checkboxes = document.querySelectorAll(`${area} .checkbox`);
    var selectedCheckboxes = [];
    checkboxes.forEach(function(checkbox) {
        if (checkbox.checked) {
            selectedCheckboxes.push(checkbox.value);
        }
    });
    // alert('Selected Checkboxes: ' + selectedCheckboxes.join(', '));
    return selectedCheckboxes;
}

function redirectToPostWithData() {
    var form = document.createElement('form');
    form.method = 'post';
    form.action = 'http://plantpan.itps.ncku.edu.tw/plantpan4/TFBS_search_results.php';  // 服务端处理数据的 URL

    var input1 = document.createElement('seq');
    input1.type = 'hidden';
    input1.name = 'TF';
    input1.value = 'TFlocus';

    var input2 = document.createElement('input');
    input2.type = 'hidden';
    input2.name = 'keyword';
    input2.value = 'AT4G17500';

    // 添加其他需要传递的参数...

    form.appendChild(input1);
    form.appendChild(input2);

    // 将表单添加到 body 中
    document.body.appendChild(form);

    // 提交表单
    form.submit();
}

function redirectToPostWithData() {
    var form = document.createElement('form');
    form.method = 'post';
    form.action = 'http://plantpan.itps.ncku.edu.tw/plantpan4/TFBS_search_results.php';  // 服务端处理数据的 URL

    var input1 = document.createElement('seq');
    input1.type = 'hidden';
    input1.name = 'TF';
    input1.value = 'TFlocus';

    var input2 = document.createElement('input');
    input2.type = 'hidden';
    input2.name = 'keyword';
    input2.value = 'AT4G17500';

    // 添加其他需要传递的参数...

    form.appendChild(input1);
    form.appendChild(input2);

    // 将表单添加到 body 中
    document.body.appendChild(form);

    // 提交表单
    form.submit();
}

function Tag_len_to_adjust_set() {
    var previousLength = 0;
    // Set up an interval to check the length at regular intervals (every 1000 milliseconds)
    var intervalId = setInterval(function() {
        var currentLength = $('#miRNA_input_area').jsonTagEditor('getTags')[0].tags.length;
        // Check if the length has changed
        if (currentLength !== previousLength) {
            if (currentLength < 2) {
                $("#set_operation_area").css("display", "none"); 
            } else {
                $("#set_operation_area").css("display", "block");
                if(currentLength != 2){
                    // alert('Please input 2 miRNA');
                    // c2_select.find("option[value='" + selectedValueC1 + "']").prop("disabled", true);
                    $(".diff_set").hide();
                    // $("#miRNA_difference2_1").hide();
                    $("#miRNA_union").prop("checked", true);
                }
                else{
                    $(".diff_set").show();
                    // $("#miRNA_difference1_2").show();
                    // $("#miRNA_difference2_1").show();
                }
            }
            // Update the previous length for the next check
            previousLength = currentLength;
        }
    }, 200); // Adjust the interval time as needed (e.g., every second)
}

$(document).ready(function(){
    $('#Result_table').hide();
    Tag_len_to_adjust_set();
    $('#header_search1').addClass('active');
    $('#header_search1').css({'background-color':'#a94442'});
    function makeid(){
        var text = "";
        var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
        for (var i = 0; i < 10; i++)
            text += possible.charAt(Math.floor(Math.random() * possible.length));
        return text;
    }
    var random_id = makeid();
    // for miRNA screener autocomplete data
    var homo_miRNA_list = document.getElementById('homo_miRNA_list').getAttribute('data-json').replace(/[\[\]\'()]/g, '').split(",");
    var miRNA_type = "homo";
    var miRNA_list;
    // miRNA type switch
    switch (miRNA_type) {
        case 'homo':
            miRNA_list = homo_miRNA_list;
            break;
        default:
            alert('沒有符合的條件');
    }

    // miRNA screener setting
    $('#miRNA_input_area').jsonTagEditor({
        autocomplete: {
            minLength: 7,
            delay: 0, // show suggestions immediately
            position: { collision: 'flip' }, // automatic menu position up/down
            source: miRNA_list
        },
        forceLowercase: false,
        placeholder: 'miRNA name(s)'
    });
    $('#search_btn').click(function(){
        $('#output_div').hide()
        $('#user_input_miRNA_screener').hide()
        $('#user_input_survival_analysis').hide()
        $('#user_input_de_screener').hide()
        $('#enrichment_analysis_user_input').hide()
        // get input type
        var search_type = document.querySelector('input[name="type"]:checked').value;
        // get input cancer
        var select_elements = document.querySelectorAll('[name="select_element"]');
        var select_cancer = [];
        for(var i=0; i<select_elements.length; i++) {
            select_cancer.push(select_elements[i].value);
            console.log(i,select_elements[i].value);
        }
        
        //// p-value screener
        var survival_switch = $("#switch_survival").prop('checked'); //true or false
        // get stage
        var stage = document.getElementById("stage_select").value;
        // get percentile
        var high_percent = document.getElementById("high_percentile").value;
        var low_percent = document.getElementById("low_percentile").value;
        // get input pvalue
        var p_value = document.getElementById("p_value").value; 
        // get correction method
        var sur_cor = document.getElementById("c_type_sur").value;
        //// miRNA screener
        var miRNA_switch = $("#switch_miRNA").prop('checked');
        $('#miRNA_input_area').jsonTagEditor('getTags')[0].tags.length;
        var selected_miRNA = [];
        for(var i = 0; i < $('#miRNA_input_area').jsonTagEditor('getTags')[0].tags.length; i++){
            selected_miRNA.push($('#miRNA_input_area').jsonTagEditor('getTags')[0].tags[i].value);
        }
        // selected_miRNA = getSelectedCheckboxes('#miRNA_checkbox');
        var miRNA_set = document.querySelector('input[name="miRNA_set"]:checked').value;
        //// DE screener
        var DE_switch = $('#switch_DE').prop('checked');
        // var DE_condition = document.querySelector('input[name="DE_tmp"]:checked').value;
        var DE_filter_elements = document.querySelectorAll('[name="DE_filter_elements"]');
        var DE_filter = [];
        for(var i=0; i<DE_filter_elements.length; i++) {
            DE_filter.push(DE_filter_elements[i].value);
            console.log(i,DE_filter_elements[i].value);
        }
        var DE_info_dict = new Object();
        DE_info_dict.condition1 = document.getElementById("condition1_pre").value.split('|')[0];
        DE_info_dict.condition2 = document.getElementById("condition2_pre").value.split('|')[0];
        console.log(DE_info_dict.condition1, DE_info_dict.condition2);
        // var DE_filter = select_cancer.concat(DE_filter);

        var switch_dict = new Object();
        console.log(survival_switch, miRNA_switch, DE_switch);
        switch_dict.survival = survival_switch;
        switch_dict.miRNA = miRNA_switch;
        switch_dict.DE = DE_switch;
        var switch_string = JSON.stringify(switch_dict)

        // let result_table = `
        //     <div class="centered">
        //         <p style="font-weight: bold; font-size: 20px;"> Search Conditon </p>
        //     </div>
        //     <div class="checkbox-container">
        //         <p style="font-weight: bold;">Search Type</p><p>`+search_type +`</p>
        //     </div>
        //     <hr>
        //     <div class="checkbox-container">
        //         <p style="font-weight: bold;">The Seleted Cancer</p><p>`+select_cancer[1]+`</p>
        //     </div>
        //     <hr>
        //     <div class="checkbox-container">
        //     <p style="font-weight: bold;">The Seleted Stage </p><p>`+stage+`</p>
        //     </div>
        //     <hr>
        //     <div class="checkbox-container">
        //         <p style="font-weight: bold;">High Percentile</p><p>`+high_percent+`</p>
        //     </div>
        //     <hr>
        //     <div class="checkbox-container">
        //         <p style="font-weight: bold;">Low Percentile</p><p>`+low_percent+`</p>
        //     </div>
        //     <hr>
        //     <div class="checkbox-container">
        //         <p style="font-weight: bold;">P-Valus Threshold</p><p>`+p_value+`</p>
        //     </div>
        //     <hr>`
        if( survival_switch==false && miRNA_switch==false && DE_switch==false){
            swal('Please open at least 1 screener');
        }
        else if(select_cancer.includes('') == false ){
            $.ajax({
                headers: { 'X-CSRFToken': csrf_token },
                type: 'POST',
                // url:'/survival_analysis/cal_pvalue/',
                url:'/screener/screener_cal_result_gene/',
                dataType : 'json',
                data : {
                    'switch_dict':switch_string,
                    'type':search_type,
                    'cancer':select_cancer[0],
                    // p value
                    'stage': stage,
                    'high_percent': high_percent,
                    'low_percent': low_percent,
                    "pvalue":p_value,
                    "cor_method_sur":sur_cor,
                    // miRNA
                    'selected_miRNA[]':selected_miRNA,
                    'miRNA_set':miRNA_set,
                    // DE
                    'DE_filter[]':DE_filter,
                    // 'DE_condition':DE_condition,
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
                success:function(response){
                    // console.log(response)
                    // document.getElementById('result_table').innerHTML = result_table;
                    clearInterval(tID);
                    delete tID
                    swal.close();
                    $('#output_div').show()
                    $('#Result_table').toggle();
                    $(`#output_table`).html();
                    $('#gap').html('<br><br><br>')
                    // $('#output').html(data);
                    // $('html,body').animate({scrollTop:$('#output').offset().top},800);
                    console.log(response.result);
                    construct_prediction_datatable(
                        "output_table", search_type, response.result, sur_cor,
                        high_percent, low_percent, stage, 
                        select_cancer[0], switch_dict, selected_miRNA ,DE_info_dict);
                    $('#stage_td').text(stage);
                    $('#correction_td').text(sur_cor);
                    $('#input_type_td').text(search_type);
                    $('#primary_site_td').text(select_cancer[0]);
                    $('#high_percent_td').text(high_percent + "%");
                    $('#low_percent_td').text(low_percent + "%");
                    $('#input_pvalue_td').text(p_value);
                    $('#output_message').text(`${response.result.length} ${search_type} met the input criteria`);
                    $('#screener_type_td').text(response.screener_type);
                    $('#selected_miRNA_td').text(selected_miRNA);
                    $('#miRNA_set_td').text(miRNA_set);
                    $('#condition2_td').text(DE_info_dict.condition1);
                    $('#condition1_td').text(DE_info_dict.condition2);
                    $('#fold_change_td').text(DE_filter[2] + DE_filter[3]);
                    $('#test_td').text(DE_filter[4]);
                    $('#direction_td').text(DE_filter[5]);
                    $('#de_correction_td').text(DE_filter[6]);
                    $('#q-value_td').text(DE_filter[7]);
                    if(survival_switch == true){
                        $('#user_input_survival_analysis').show()
                    }

                    if(miRNA_switch == true){
                        $('#user_input_miRNA_screener').show()
                    }
                    
                    if(DE_switch == true){
                        $('#user_input_de_screener').show()
                    }

                    // var resultElement = document.getElementById('result_block');
                    // resultElement.style.display = 'block';
                },
                error:function(xhr, ajaxOptions, thrownError){ 
                    alert(thrownError);
                    clearInterval(tID);
                    delete tID
                    swal.close();
                    swal('error')
                }       
            });    
        }
        else{
            swal('Input Error!')
        }                                                                                                       
    });

    //// enrichment jump btn
    // $('#btn_cal').on('click', function () {
    //     var dataTable = $('#output_table').DataTable(); // 假設 DataTable 的 ID 是 'example'
    //     // var data_seq = dataTable.column('gene_name').data().toArray();
    //     // var data_seq_str = data_seq.join(',');
    //     var data_seq_str = dataTable.column('name:name').data();
    //     var cor_type = $('#c_type').val();
    //     var p_limit = $('#p-value_enrich').val();
    //     console.log(data_seq_str, cor_type, p_limit)
    //     var form = document.createElement('form');
    //     form.method = 'post';
    //     // form.action = '/enrichment_app/'; 
    //     form.action = 'www.google.com'; 
    //     var input1 = document.createElement('input');
    //     input1.type = 'hidden';
    //     input1.name = 'seq';
    //     input1.value = data_seq_str;
    //     var input2 = document.createElement('input');
    //     input2.type = 'hidden';
    //     input2.name = 'cor_type';
    //     input2.value = cor_type;
    //     var input3 = document.createElement('input');
    //     input3.type = 'hidden';
    //     input3.name = 'p_limit';
    //     input3.value = p_limit;
    //     form.appendChild(input1);
    //     form.appendChild(input2);
    //     form.appendChild(input3);
    //     form.submit();
    //     //// 使用 XMLHttpRequest 進行 POST 請求
    //     // var xhr = new XMLHttpRequest();
    //     // var url = '/enrichment_app/';
    //     // // 設置 POST 請求
    //     // xhr.open('POST', url, true);
    //     // xhr.setRequestHeader('Content-Type', 'application/json');
    //     // // 將資料以 JSON 字串的形式發送
    //     // xhr.send(JSON.stringify({ data_seq_str: data_seq_str, cor_type: cor_type, p_limit: p_limit }));
    //     // // 如果需要在請求完成後執行某些操作，可以添加以下事件監聽器
    //     // xhr.onload = function () {
    //     //     console.log('POST request completed');
    //     // };
    // });
    

    //// switch for every screener
    $('#switch_survival').change(function() {
        if ($(this).prop('checked')) {
            $(".survival_analysis").css("display", "block");
        } else {
            $(".survival_analysis").css("display", "none"); 
        }
    });

    $('#switch_miRNA').change(function() {
        if ($(this).prop('checked')) {
            $(".miRNA_screener").css("display", "block");
            // console.log();
        } else {
            $(".miRNA_screener").css("display", "none");
        }
    });

    $('#switch_DE').change(function() {
        if ($(this).prop('checked')) {
            $(".DE_screener").css("display", "block");
        } else {
            $(".DE_screener").css("display", "none"); 
        }
    });
    ////


    // $('.json-tag-editor.ui-sortable').change(function() {
    //     setTimeout(function() {
    //         // alert($('#miRNA_input_area').jsonTagEditor('getTags')[0].tags.length);
    //         // console.log($('#miRNA_input_area').jsonTagEditor('getTags')[0].tags);
    //         // alert("change");
    //         if ($('#miRNA_input_area').jsonTagEditor('getTags')[0].tags.length < 2) {
    //             $("#set_operation_area").css("display", "none"); 
    //         } else {
    //             $("#set_operation_area").css("display", "block");
    //             if($('#miRNA_input_area').jsonTagEditor('getTags')[0].tags.length != 2){
    //                 alert('Please input 2 miRNA');
    //                 // c2_select.find("option[value='" + selectedValueC1 + "']").prop("disabled", true);
    //                 $("#miRNA_difference").prop("disabled", true);
    //                 // $("miRNA_difference").prop("disabled", true);
    //             }
    //             else{
    //                 $("#miRNA_difference").prop("disabled", false);
    //             }
    //             // if($('#miRNA_input_area').jsonTagEditor('getTags')[0].tags.length == 2){
    //             //     // $("#set_operation_area").css("display", "none"); 
    //             //     c1_select.find("option[value='" + selectedValueC2 + "']").prop("disabled", true);
    //             // }
    //         }
    //         console.log("Change event handled, waiting for 1 second.");
    //     }, 10);
        
    // });

    

    $("#clear").on("click", function () { 
        $('#condition2_pre,#condition1_pre').val(null).trigger("change");  //c1
    });


    $("#log2FC_checkbox").click(function() {
        if($("#log2FC_checkbox").prop("checked")) {
            $("#log2FC_input").prop("disabled",false).val('2')  
            $("#FC_select").prop("disabled",false).val('≥').css({"background-color":"#FFFFF"})
        }
        else {
            $("#log2FC_input").prop("disabled",true).val('')  
            $("#FC_select").prop("disabled",true).val('').css({"background-color":"#eee"})
        }
    });

    $("#TEST_checkbox").click(function() {
        if($("#TEST_checkbox").prop("checked")) {
            $("#TEST_input").prop("disabled",false).val('0.05')
            $("#TEST_select").prop("disabled",false).val('T test').css({"background-color":"#FFFFF"})
            $("#TESTstates_select").prop("disabled",false).val('Greater (Condition2 > Condition1)').css({"background-color":"#FFFFF"})
        }
        else {
            $("#TEST_input").prop("disabled",true).val('')       
            $("#TEST_select").prop("disabled",true).val('').css({"background-color":"#eee"})
            $("#TESTstates_select").prop("disabled",true).val('').css({"background-color":"#eee"})
        }
    });

    function checkbox_value(checkboxname){//數checkbox2[]有勾選幾個
        var feature_value = new Array();
        $("input:checkbox:checked[name='"+checkboxname+"']").each(function(i) { 
            feature_value[i] = this.value; 
        });
        return feature_value;
    }

    $('#radioBtn a').on('click', function(){
        var sel = $(this).data('title');
        var tog = $(this).data('toggle');
        $('#'+tog).prop('value', sel);
        
        $('a[data-toggle="'+tog+'"]').not('[data-title="'+sel+'"]').removeClass('active').addClass('notActive');
        $('a[data-toggle="'+tog+'"][data-title="'+sel+'"]').removeClass('notActive').addClass('active');
    })
});

