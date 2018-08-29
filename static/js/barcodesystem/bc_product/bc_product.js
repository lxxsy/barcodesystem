/**
 * Created by LILI on 2018/8/29.
 */

$(function () {
    var error_cpid = true;
    var error_cpmc = true;
    var error_pbbh = true;
    var error_cpgg = true;
    var error_cpsm = true;
    var error_tempname = true;
    var Original = $('#cpid').val();
    $.get('/product/product_query1', function (data) {
        var pbbh = $('#pbbh').val();
        $.each(JSON.parse(data.pb_list), function (index, item) {
            if (item.pk != pbbh){
                $('#pbbh').append('<option value='+item.pk+'>'+item.pk+'</option>');
            };
        });
    });
    $('#cpid').blur(function () {
        cpid_judge();
    });
    $('#cpmc').blur(function () {
        cpmc_judge();
    });
    $('#cpgg').blur(function () {
        cpgg_judge();
    });
    $('#cpsm').change(function () {
        cpsm_judge();
    });
    $('#tempname').change(function () {
        tempname_judge();
    });

    $('#form_submit').submit(function () {
        if ($('#pbbh').val().length === 0){
            error_pbbh = false;
        };
        cpid_judge();
        cpmc_judge();
        cpgg_judge();
        cpsm_judge();
        tempname_judge();
        if (error_cpid === true && error_cpmc === true && error_pbbh === true && error_cpgg === true &&
            error_cpsm === true && error_tempname === true){
            return true;
        }else{
            return false;
        };
    });
    /*
        功能： 判断产品编号的输入是否合理
     */
    function cpid_judge() {
        var cpid = $('#cpid').val();
        var re = /\W+/;
        if (cpid.length===0){
            $('#cpid').next().text('产品编号不能为空!').show();
            error_cpid = false;
        }else{
            if (re.test(cpid)){
                $('#cpid').next().text('产品编号含有不允许符号!').show();
                error_cpid = false;
            }else{
                $.get('/product/product_query2', {Original: Original, cpid: cpid}, function (data) {
                    if (data.bool === 0){
                        $('#cpid').next().text('产品编号已存在!').show();
                        error_cpid = false;
                    }else {
                        $('#cpid').next().hide();
                        error_cpid = true;
                    };
                });
            };
        };
    };
    function cpmc_judge() {
        var cpmc = $('#cpmc').val();
        var re = /\s+|-+|\++|\?+/;
        if (cpmc.length === 0){
            $('#cpmc').next().text('产品名称不能为空!').show();
            error_cpmc = false;
        }else if(re.test(cpmc)){
            $('#cpmc').next().text('产品名称含有不允许符号!').show();
            error_cpmc = false;
        }else {
            $('#cpmc').next().hide();
            error_cpmc = true;
        };
    };
    function cpgg_judge() {
        var cpgg = $('#cpgg').val();
        if (cpgg.length === 0){
            $('#cpgg').next().text('产品规格不能为空!').show();
            error_cpgg = false;
        }else {
            $('#cpgg').next().hide();
            error_cpgg = true;
        };
    };
    function cpsm_judge() {
        if ($('#cpsm').val() === ''){
            $('#cpsm').next().text('产品说明文件不能为空').show();
            error_cpsm = false;
        }else{
            var cpsm_dict = document.getElementById('cpsm').files[0];
            var cpsm_name = cpsm_dict.name.toLowerCase().split('.');
            var cpsm_type = cpsm_name[cpsm_name.length-1];
            var cpsm_size = cpsm_dict.size;
            if (cpsm_type != 'docx' && cpsm_type != 'doc' && cpsm_type != 'eddx'){
                $('#cpsm').next().text('文件格式必须是docx,doc,xls的一种').show();
                error_cpsm = false;
            }else if (cpsm_size > 5000000){
                $('#cpsm').next().text('请上传不超过5M的文件').show();
                error_cpsm = false;
            }else{
                $('#cpsm').next().hide();
                error_cpsm = true;
            };
        };
    };
    function tempname_judge() {
        if ($('#tempname').val() === ''){
            $('#tempname').next().text('成品标签文件不能为空').show();
            error_tempname = false;
        }else{
            var tempname_dict = document.getElementById('tempname').files[0];
            var tempname_name = tempname_dict.name.toLowerCase().split('.');
            var tempname_type = tempname_name[tempname_name.length-1];
            var tempname_size = tempname_dict.size;
            if (tempname_type != 'docx' && tempname_type != 'doc' && tempname_type != 'eddx'){
                $('#tempname').next().text('文件格式必须是docx,doc,xls的一种').show();
                error_tempname = false;
            }else if (tempname_size > 5000000){
                $('#tempname').next().text('请上传不超过5M的文件').show();
                error_tempname = false;
            }else{
                $('#tempname').next().hide();
                error_tempname = true;
            };
        };
    };
});