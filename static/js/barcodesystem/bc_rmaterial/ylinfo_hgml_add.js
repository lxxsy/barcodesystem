$(function () {
    var error_ylid = false;
    var error_ylname = false;
    var error_gyscode = false;
    var error_gysname = false;
    /*
        页面加载完毕后获取原料与供应商信息
     */
    $.get('/rmaterial/query_ylinfo_hgml1', function (data) {
        $.each(JSON.parse(data.ylinfo_list), function (index, item) {
            $('#ylid').append('<option value='+item.pk+'>'+item.pk+'</option>');
            $('#ylname').append('<option value='+item.fields.ylname+'>'+item.fields.ylname+'</option>');
        });
        $.each(JSON.parse(data.gys_list), function (index, item) {
            $('#gyscode').append('<option value='+item.pk+'>'+item.pk+'</option>');
            $('#gysname').append('<option value='+item.fields.gysname+'>'+item.fields.gysname+'</option>');
        });
    });
    /*
        原料代码失去焦点后触发
     */
    $('.data_ylinfo_hgml_ylid').change(function () {
        data_ylinfo_hgml_ylid_judge();
    });
    /*
        原料名称失去焦点后触发
     */
    $('.data_ylinfo_hgml_ylname').change(function () {
        data_ylinfo_hgml_ylname_judge();
    });
    /*
        供应商代码失去焦点后触发
     */
    $('.data_ylinfo_hgml_gyscode').change(function () {
        data_ylinfo_hgml_gyscode_judge();
    });
    /*
        供应商名称失去焦点后触发
     */
    $('.data_ylinfo_hgml_gysname').change(function () {
        data_ylinfo_hgml_gysname_judge();
    });
    /*
        提交表单后触发
     */
    $('#form_submit').submit(function () {
        data_ylinfo_hgml_ylid_judge();
        if (error_ylid === false){
            return false
        };
        data_ylinfo_hgml_ylname_judge();
         if (error_ylname === false){
            return false
        };
        data_ylinfo_hgml_gyscode_judge();
         if (error_gyscode === false){
            return false
        };
        data_ylinfo_hgml_gysname_judge();
         if (error_gysname === false){
            return false
        };
        if (error_ylid === true && error_ylname === true && error_gyscode === true && error_gysname === true){
            return true;
        }else{
            return false;
        };
    });
    /*
        功能: 判断原料代码
     */
     function data_ylinfo_hgml_ylid_judge() {
        $('.data_ylinfo_hgml_ylid').next().hide();
        $('.data_ylinfo_hgml_ylname').next().hide();
        $('.data_ylinfo_hgml_gyscode').next().hide();
        $('.data_ylinfo_hgml_gysname').next().hide();
        var ylid = $('.data_ylinfo_hgml_ylid').val();
        var gyscode = $('.data_ylinfo_hgml_gyscode').val();
        $.ajax({
            url:'/rmaterial/query_ylinfo_hgml2',
            data:{ylid: ylid, gyscode: gyscode},
            type:"get",
            async:false,
            success:function(data){
                $('.data_ylinfo_hgml_ylname').val(data.ylname);
                if (data.ylid_bool === 0){
                    $('.data_ylinfo_hgml_ylid').next().text('原料不存在').show();
                    error_ylid = false;
                }else if (data.ylinfo_hgml_bool === 1){
                    $('.data_ylinfo_hgml_ylid').next().text('此数据已存在，请更换原料或供应商').show();
                    error_ylid = false;
                }else{
                    error_ylid = true;
                };
            }
        });
    };
    /*
        功能: 判断原料名称
     */
    function data_ylinfo_hgml_ylname_judge() {
        $('.data_ylinfo_hgml_ylid').next().hide();
        $('.data_ylinfo_hgml_ylname').next().hide();
        $('.data_ylinfo_hgml_gyscode').next().hide();
        $('.data_ylinfo_hgml_gysname').next().hide();
        var ylname = $('.data_ylinfo_hgml_ylname').val();
        var gyscode = $('.data_ylinfo_hgml_gyscode').val();
        $.ajax({
            url:'/rmaterial/query_ylinfo_hgml3',
            data:{ylname: ylname, gyscode: gyscode},
            type:"get",
            async:false,
            success:function(data){
                $('.data_ylinfo_hgml_ylid').val(data.ylid);
                if (data.ylname_bool === 0){
                    $('.data_ylinfo_hgml_ylname').next().text('原料不存在').show();
                    error_ylname = false;
                }else if (data.ylinfo_hgml_bool === 1){
                    $('.data_ylinfo_hgml_ylname').next().text('此数据已存在，请更换原料或供应商').show();
                    error_ylname = false;
                }else{
                    error_ylname = true;
                };
            }
        });
    };
    /*
        功能: 判断供应商代码
     */
    function data_ylinfo_hgml_gyscode_judge() {
        $('.data_ylinfo_hgml_gyscode').next().hide();
        $('.data_ylinfo_hgml_gysname').next().hide();
        $('.data_ylinfo_hgml_ylid').next().hide();
        $('.data_ylinfo_hgml_ylname').next().hide();
        var gyscode = $('.data_ylinfo_hgml_gyscode').val();
        var ylid = $('.data_ylinfo_hgml_ylid').val();
        $.ajax({
            url:'/rmaterial/query_ylinfo_hgml4',
            data:{gyscode: gyscode, ylid: ylid},
            type:"get",
            async:false,
            success:function(data){
                $('.data_ylinfo_hgml_gysname').val(data.gysname);
                if (data.gyscode_bool === 0){
                    $('.data_ylinfo_hgml_gyscode').next().text('供应商不存在').show();
                    error_gyscode = false;
                }else if (data.ylinfo_hgml_bool === 1){
                    $('.data_ylinfo_hgml_gyscode').next().text('此数据已存在，请更换原料或供应商').show();
                    error_gyscode = false;
                }else{
                    error_gyscode = true;
                };
            }
        });
    };
    /*
        功能: 判断供应商名称
     */
    function data_ylinfo_hgml_gysname_judge() {
        $('.data_ylinfo_hgml_gyscode').next().hide();
        $('.data_ylinfo_hgml_gysname').next().hide();
        $('.data_ylinfo_hgml_ylid').next().hide();
        $('.data_ylinfo_hgml_ylname').next().hide();
        var gysname = $('.data_ylinfo_hgml_gysname').val();
        var ylid = $('.data_ylinfo_hgml_ylid').val();
        $.ajax({
            url:'/rmaterial/query_ylinfo_hgml5',
            data:{gysname: gysname, ylid: ylid},
            type:"get",
            async:false,
            success:function(data){
                $('.data_ylinfo_hgml_gyscode').val(data.gyscode);
                if (data.gysname_bool === 0){
                    $('.data_ylinfo_hgml_gysname').next().text('供应商不存在').show();
                    error_gysname = false;
                }else if (data.ylinfo_hgml_bool === 1){
                    $('.data_ylinfo_hgml_gysname').next().text('此数据已存在，请更换原料或供应商').show();
                    error_gysname = false;
                }else{
                    error_gysname = true;
                };
            }
        });
    };
});