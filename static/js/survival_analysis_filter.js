$(document).ready(function(){
    var pattern = /["\[\]\s]/g;
    var gene_list = document.getElementById('data').textContent.replaceAll(pattern, "").split(',');
    // console.log(gene_list);
    $('#header_search3').addClass('active');
    // $('#header_search3').addClass('active');
    $('#header_search3').css({'background-color':'#a94442'});
    function makeid(){
        var text = "";
        var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

        for (var i = 0; i < 10; i++)
            text += possible.charAt(Math.floor(Math.random() * possible.length));
        return text;
    }
    var random_id = makeid();

    $('#send').click(function(){
        // open a new tab
        // window.open("https://example.com", "_blank");
        var input_elements = document.querySelectorAll('[name="input_element"]');
        var input_value = [];
        for(var i=0; i<input_elements.length; i++) {
            input_value.push(input_elements[i].value);
        }
        var primary_check_elements = document.querySelectorAll('[name="primary_check_element"]');
        var primary_check_value = [];
        for (var i=0;i<primary_check_elements.length;i++){
            if ( primary_check_elements[i].checked ) {
            primary_check_value.push(primary_check_elements[i].value);
            }
        }

        if((input_value[0] == 'genes' && gene_list.indexOf(input_value[1]) != -1) || (input_value[0] == 'isoforms' && transcript_list.indexOf(input_value[1]) != -1)){
            if(primary_check_value.length > 0){
                // if(stage_check_value.length > 0){
                    $.ajax({
                        url:'query_by_gene2/',
                        data :  {

                            'input_value[]':input_value,
                            'primary_check_value[]':primary_check_value,
                            // 'stage_check_value[]':stage_check_value,
                            'random_id':random_id,

                            csrfmiddlewaretoken: '{{ csrf_token }}'
                        },
                        type:'POST',

                        datatype : 'text',

                                            
                        success:function(data){
                            clearInterval(tID);
                            delete tID
                            swal.close();
                            $('#output').html(data);
                            $('html,body').animate({scrollTop:$('#output').offset().top},800);

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

                                
                        error:function(xhr, ajaxOptions, thrownError){ 
                            clearInterval(tID);
                            delete tID
                            swal.close();
                            swal('error')
                        }    
                    });  
            }
            else{
                swal('Please select one cancer!')
            } 
        }
        else{
            if(input_value[0] == 'genes'){
                swal('Invalid gene symbol!')
            }
            else{
                swal('Invalid transcript name!')
            }
        }                                                                                                       
    });

    // var gene_list = {{gene_list|safe}}; 
    // var transcript_list = {{transcript_list|safe}};
    $("#GT_input").autocomplete({  
        source: gene_list,
        minLength: 3,autoFocus: true,delay: 0
    });

    $("#GT_select").change(function() {
        var sel = $(this).find(':selected').data('title');
        var placeholder = $(this).find(':selected').data('placeholder');
        $('#GT_input').val("");
        $('#GT_input').prop("placeholder", placeholder);

        if(sel == 'genes'){
            $("#GT_input").autocomplete({  
                source: gene_list,
                minLength: 2,autoFocus: true,delay: 0

            });
        }
        else{
            $("#GT_input").autocomplete("destroy").removeData('autocomplete');
            $("#GT_input").autocomplete({  
                source: transcript_list,
                minLength: 9,autoFocus: true,delay: 0

            });
        }
    });

    // checkbox js
    $('.button-checkbox').each(function () {

        // Settings
        var $widget = $(this),
            $button = $widget.find('button'),
            $checkbox = $widget.find('input:checkbox'),
            color = $button.data('color'),
            settings = {
                on: {
                    icon: 'glyphicon glyphicon-check'
                },
                off: {
                    icon: 'glyphicon glyphicon-unchecked'
                }
            };

        // Event Handlers
        $button.on('click', function () {
            $checkbox.prop('checked', !$checkbox.is(':checked'));
            $checkbox.triggerHandler('change');
            updateDisplay();
        });
        $checkbox.on('change', function () {
            updateDisplay();
        });

        // Actions
        function updateDisplay() {
            var isChecked = $checkbox.is(':checked');

            // Set the button's state
            $button.data('state', (isChecked) ? "on" : "off");

            // Set the button's icon
            $button.find('.state-icon')
                .removeClass()
                .addClass('state-icon ' + settings[$button.data('state')].icon);

            // Update the button's color
            if (isChecked) {
                $button
                    .removeClass('btn-default')
                    .addClass('btn-' + color + ' active');
            }
            else {
                $button
                    .removeClass('btn-' + color + ' active')
                    .addClass('btn-default');
            }
        }

        // Initialization
        function init() {

            updateDisplay();

            // Inject the icon if applicable
            if ($button.find('.state-icon').length == 0) {
                $button.prepend('<i class="state-icon ' + settings[$button.data('state')].icon + '"></i> ');
            }
        }
        init();
    });

    $("[name='primary_check_element']").click(function(){

        $('#primary_site_table > tbody > tr').css({'background-color':''});
        $(this).closest('tr').css({'background-color':'#eee'});

        $('#primary_site_table > tbody > tr').find(':button').prop('disabled', true);
        $('#primary_site_table > tbody > tr').find(':checkbox').prop('checked',false);
        $(this).closest('tr').find(':button').prop('disabled', false);

        $('#primary_site_table > tbody > tr').find(':button').removeClass('btn-success active').addClass('btn-default');
        $('#primary_site_table > tbody > tr').find(':button').find('i').removeClass('glyphicon-check').addClass('glyphicon-unchecked');

    })

    $('#primary_site_table').DataTable({
        "aaSorting": [ [1, 'asc']],
        "sScrollX": "100%",
        "scrollY": "50vh",
        "scrollCollapse": true,
        "paging":         false,
        "columnDefs": [ 
            {
                "targets": [0,2],
                "orderable": false
            },
        ],
    })
})