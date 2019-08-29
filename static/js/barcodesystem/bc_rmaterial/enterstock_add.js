
$(function () {
    var error_ylid = false;
    var error_ylname = false;
    var error_gyscode = false;
    var error_gysname = false;
    var error_zl = false;
    var error_scrq = false;
    var error_check1no = false;
    var date = new Date();   // 返回当前日期和时间
    var year = date.getFullYear();  // 获取当前日期的年份
    var month = date.getMonth()+1;  // 获取当前日期的月份，因默认月份是0-11，所以获取到数值后需要加1
    var day = date.getDate();  // 获取某个月份的某一天
    //console.log(typeof year.toString());
    /*
        将月份转化为字符串，并通过字符串方法length获取长度，长度为1说明月份是1-9，需要在它前面手动加个0.以达到两位数的要求
     */
    if (month.toString().length === 1){
        month = '0'+month;
    };
    if (day.toString().length === 1){
        day = '0'+day;
    }
    /*
        页面加载完毕后获取原料基础信息与原料仓库信息
     */
    $.get('/rmaterial/query_enterstock1', function (data) {
        $.each(JSON.parse(data.ylinfo_list), function (index, item) {
            $('#ylid').append('<option value='+item.pk+'>'+item.pk+'</option>');
            $('#ylname').append('<option value='+item.fields.ylname+'>'+item.fields.ylname+'</option>');
        });
        $.each(JSON.parse(data.stockinfo_list), function (index, item) {
            $('#rkck').append('<option value='+item.fields.stockname+'>'+item.fields.stockname+'</option>');
        });
    });
    $('#rdate').val(year+'-'+month+'-'+day); // 格式要求为2018-12-12，所以需要拼接，渲染到入库日期输入框中
    $('#scrq').val(year+'-'+month+'-'+day); // 格式要求为2018-12-12，所以需要拼接，渲染到生产日期输入框中
    $('#clph').val(year.toString()+month.toString()+day.toString()); // 格式要求为20181212,所以要转为字符串后接着拼接
    /*
        原料代码失去焦点后触发
     */
    $('.data_enterstock_ylid').change(function () {
        data_enterstock_ylid_judge();
    });
    /*
        原料名称失去焦点后触发
     */
    $('.data_enterstock_ylname').change(function () {
        data_enterstock_ylname_judge();
    });
    /*
        供应商代码失去焦点后触发
     */
    $('#gyscode').change(function () {
        gyscode_judge();
    });
    /*
        供应商名称失去焦点后触发
     */
    $('#gysname').change(function () {
        gysname_judge();
    });
    /*
        入库重量失去焦点后触发
     */
    $('#zl').blur(function () {
        zl_judge();
    });
    /*
        生产日期失去焦点后触发
     */
    $('#scrq').blur(function () {
        scrq_judge();
    });
    /*
        检验报告编号失去焦点后触发
     */
    $('#check1no').blur(function () {
        check1no_judge();
    });
    /*
        提交表单后触发
     */
    $('#form_submit').submit(function () {
        submit_ylid_judge();
        gyscode_judge();
        gysname_judge();
        zl_judge();
        scrq_judge();
        check1no_judge();
        if (error_ylid === true && error_ylname === true && error_gyscode === true && error_gysname === true
            && error_zl === true && error_scrq === true && error_check1no === true){
            return true;
        }else{
            return false;
        };
    });
    /*
        功能：当提交表单时触发此函数判断原料代码，和输入框判断不同
     */
    function submit_ylid_judge() {
        let ylid = $('.data_enterstock_ylid').val();
        $.ajax({
            url:'/rmaterial/query_enterstock2',
            data:{ylid: ylid},
            type:"get",
            async:false,
            success:function(data){
                if (data.ylid_bool === 0){
                    console.log('aaa');
                    $('.data_enterstock_ylid').next().text('原料不存在').show();
                    error_ylid = false;
                    error_ylname = false;
                }else {
                    $('.data_enterstock_ylid').next().hide();
                    error_ylid = true;
                    error_ylname = true;
                };
            }
        });
    };
    /*
        功能: 当用户点击输入框选择原料代码时触发此函数，提交表单时不会触发此函数
     */
     function data_enterstock_ylid_judge() {
        $('.data_enterstock_ylid').next().hide();
        $('.data_enterstock_ylname').next().hide();
        $('#gyscode').empty(); // 清空供应商信息
        $('#gysname').empty();
        var ylid = $('.data_enterstock_ylid').val();
        $.ajax({
            url:'/rmaterial/query_enterstock2',
            data:{ylid: ylid},
            type:"get",
            async:false,
            success:function(data){
                $('.data_enterstock_ylname').val(data.ylname);
                $('#dbz').val(data.piedw);
                $('.data_enterstock_stockinfo').val(data.stockname);
                if (data.ylid_bool === 0){
                    $('.data_enterstock_ylid').next().text('原料不存在').show();
                    error_ylid = false;
                }else if (data.ylinfo_hgml_bool === 0){
                    $('.data_enterstock_ylid').next().text('原料不存在合格供应商').show();
                    error_ylid = false;
                }else{
                    $.each(JSON.parse(data.ylinfo_hgml), function (index, item) {
                        $('#gyscode').append('<option value='+item.fields.gyscode+'>'+item.fields.gyscode+'</option>');
                        $('#gysname').append('<option value='+item.fields.gysname+'>'+item.fields.gysname+'</option>');
                    });
                    error_ylid = true;
                };
            }
        });
    };
    /*
        功能: 判断原料名称
     */
    function data_enterstock_ylname_judge() {
        $('.data_enterstock_ylid').next().hide();
        $('.data_enterstock_ylname').next().hide();
        $('#gyscode').empty();
        $('#gysname').empty();
        var ylname = $('.data_enterstock_ylname').val();
        $.ajax({
            url:'/rmaterial/query_enterstock3',
            data:{ylname: ylname},
            type:"get",
            async:false,
            success:function(data){
                $('.data_enterstock_ylid').val(data.ylid);
                $('#dbz').val(data.piedw);
                $('.data_enterstock_stockinfo').val(data.stockname);
                if (data.ylname_bool === 0){
                    $('.data_enterstock_ylname').next().text('原料不存在').show();
                    error_ylname = false;
                }else if (data.ylinfo_hgml_bool === 0){
                    $('.data_enterstock_ylname').next().text('原料不存在合格供应商').show();
                    error_ylname = false;
                }else{
                    $.each(JSON.parse(data.ylinfo_hgml), function (index, item) {
                        $('#gyscode').append('<option value='+item.fields.gyscode+'>'+item.fields.gyscode+'</option>');
                        $('#gysname').append('<option value='+item.fields.gysname+'>'+item.fields.gysname+'</option>');
                    });
                    error_ylname = true;
                };
            }
        });
    };
    /*
        功能: 判断供应商代码
     */
    function gyscode_judge() {
        var gyscode = $('#gyscode').val();
        $.ajax({
            url:'/rmaterial/query_enterstock4',
            data:{gyscode: gyscode},
            type:"get",
            async:false,
            success:function(data){
                if (data.gyscode_bool === 0){
                    error_gyscode = false;
                }else{
                    $('#gysname').find("[value='"+data.gysname+"']").remove(); //将对应的供应商名称找到并删除
                    $('#gysname').prepend('<option value='+data.gysname+'>'+data.gysname+'</option>'); // 删除后接着在最前面插入
                    $('#gysname').val(data.gysname); // 最后将输入框的值改掉
                    $('#gyscode').next().hide();
                    error_gyscode = true;
                };
            }
        });
    };
    /*
        功能: 判断供应商名称
     */
    function gysname_judge() {
        var gysname = $('#gysname').val();
        $.ajax({
            url:'/rmaterial/query_enterstock5',
            data:{gysname: gysname},
            type:"get",
            async:false,
            success:function(data){
                if (data.gysname_bool === 0){
                    error_gysname = false;
                }else{
                    $('#gyscode').find("[value='"+data.gyscode+"']").remove();
                    $('#gyscode').prepend('<option value='+data.gyscode+'>'+data.gyscode+'</option>');
                    $('#gyscode').val(data.gyscode);
                    $('#gysname').next().hide();
                    error_gysname = true;
                };
            }
        });
    };
    /*
        功能：判断入库重量
     */
    function zl_judge() {
        var zl = $('#zl').val();
        var re = /^[0-9]+\.?[0-9]*$/;
        var two_re = /^0+\.?0*$/;
        if (re.test(zl)){
            if (two_re.test(zl)){
                $('#zl').next().text('格式不正确或没有正确输入数字!').show();
                error_zl = false;
            }else {
                $('#zl').next().hide();
                error_zl = true;
            };
        }else {
            $('#zl').next().text('格式不正确或没有正确输入数字！').show();
            error_zl = false;
        };
    };
    /*
        功能：判断生产日期
     */
    function scrq_judge() {
        var scrq = $('#scrq').val().split('-');
        var rdate = $('#rdate').val().split('-');
        if (scrq[0] > rdate[0]){
            $('#scrq').next().text('生产日期不能大于入库日期！').show();
            error_scrq = false;
        }else if (scrq[1] > rdate[1]){
            $('#scrq').next().text('生产日期不能大于入库日期！').show();
            error_scrq = false;
        }else if (scrq[2] > rdate[2]){
            $('#scrq').next().text('生产日期不能大于入库日期！').show();
            error_scrq = false;
        }else{
            $('#scrq').next().hide();
            error_scrq = true;
        };
    };
    /*
        功能：判断检验报告编号
     */
    function check1no_judge() {
        var check1no = $('#check1no').val();
        if (check1no.length === 0){
            $('#check1no').next().text('请输入有效的报告编号').show();
            error_check1no = false;
        }else {
            $('#check1no').next().hide();
            error_check1no = true;
        };
    };
});