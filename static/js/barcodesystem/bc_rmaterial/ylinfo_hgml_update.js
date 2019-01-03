$(function () {
    var error_ylid = false;
    var error_ylname = false;
    var error_gyscode = false;
    var error_gysname = false;
    /*
        获取要修改的原料id，请求视图加载模板并渲染数据
     */
    var ylinfo_hgml_id = $('#ylinfo_hgml_id').val();
    $.ajax({
        url:'/rmaterial/update_ylinfo_hgml',
        data:{"ylinfo_hgml_id":ylinfo_hgml_id},
        type:"get",
        async:false,
        success:function(data){
            if (data.bool === 1){
                $('#form_submit').html(template('ylinfo_hgml', {ylid: data.ylid, ylname: data.ylname, gyscode: data.gyscode,
                    gysname: data.gysname, scxkzh: data.scxkzh, cppzwh: data.cppzwh, cpbzbh: data.cpbzbh,
                    jkcpdjz: data.jkcpdjz, bz: data.bz}));
            }else {
                alert('异常');
            };
        }
    });
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
        获取页面上的供应商ID与供应商名称，称为原内容。目的是修改以后会拿原内容与新内容做比较，如果新内容和原内容相同则表示没有做修改
      */
    var Original_ylid = $('.data_ylinfo_hgml_ylid').val();
    var Original_ylname = $('.data_ylinfo_hgml_ylname').val();
    var Original_gyscode = $('.data_ylinfo_hgml_gyscode').val();
    var Original_gysname = $('.data_ylinfo_hgml_gysname').val();
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
            data:{ylid: ylid, gyscode: gyscode, Original_ylid: Original_ylid},
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
            data:{ylname: ylname, gyscode: gyscode, Original_ylname: Original_ylname},
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
            data:{gyscode: gyscode, ylid: ylid, Original_gyscode: Original_gyscode},
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
            data:{gysname: gysname, ylid: ylid, Original_gysname: Original_gysname},
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