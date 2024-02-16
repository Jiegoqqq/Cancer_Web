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