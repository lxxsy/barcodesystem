
$(function () {
    var error_ylid = false;
    var error_ylname = false;
    var error_piedw = false;
    var error_zf = false;
    var error_stockid = false;
    /*
        获取原料分类与仓库并填充
     */
    $.get('/rmaterial/query_rmaterial1', function (data) {
        $.each(JSON.parse(data.ylfl_list) ,function (index, item) {
            $('#zf').append('<option value='+item.pk+'>'+item.fields.flmc+'</option>');
        });
        $.each(JSON.parse(data.stockinfo_list) ,function (index, item) {
            $('#stockid').append('<option value='+item.pk+'>'+item.fields.stockname+'</option>');
        });
    });
    /*
        原料代码失去焦点后触发
     */
    $('#ylid').blur(function () {
        ylid_judge();
    });
    /*
        原料名称失去焦点后触发
     */
    $('#ylname').blur(function () {
        ylname_judge();
    });
    /*
        单包重量失去焦点后触发
     */
    $('#piedw').blur(function () {
        piedw_judge();
    });
    /*
        提交表单触发
     */
    $('#form_submit').submit(function () {
        if ($('#zf').val() != ''){
            error_zf = true;
        };
        if ($('#stockid').val() != ''){
            error_stockid = true;
        };
        ylid_judge();
        if (error_ylid === false){
            return false;
        };
        ylname_judge();
        if (error_ylname === false){
            return false;
        };
        piedw_judge();
        if (error_zf === true && error_stockid === true && error_ylid === true && error_ylname === true && error_piedw === true){
            return true;
        }else {
            return false;
        };
    });
    /*
        功能: 判断原料代码
     */
    function ylid_judge() {
        var ylid = $('#ylid').val();
        var re = /\W+/;
        if (ylid.length===0){
            $('#ylid').next().text('原料代码不能为空！').show();
            error_ylid = false;
        }else{
            if (re.test(ylid)){
                $('#ylid').next().text('原料代码含有不允许符号!').show();
                error_ylid = false;
            }else{
                $.ajax({
                    url:'/rmaterial/query_rmaterial2',
                    data:{ylid: ylid},
                    type:"get",
                    async:false,
                    success:function(data){
                        if (data.bool === 0){
                            $('#ylid').next().text('原料代码已存在!').show();
                            error_ylid = false;
                        }else {
                            $('#ylid').next().hide();
                            error_ylid = true;
                        };
                    }
                });
            };
        };
    };
    /*
        功能: 判断原料名称
     */
    function ylname_judge() {
        var ylname = $('#ylname').val();
        var re = /\s+|-+|\++|\?+/;
        if (ylname.length === 0){
            $('#ylname').next().text('原料名称不能为空!').show();
            error_ylname = false;
        }else {
            if(re.test(ylname)){
                $('#ylname').next().text('原料名称含有不允许符号!').show();
                error_ylname = false;
            }else {
                $.ajax({
                    url:'/rmaterial/query_rmaterial3',
                    data:{ylname: ylname},
                    type:"get",
                    async:false,
                    success:function(data){
                        if (data.bool === 0){
                            $('#ylname').next().text('原料名称已存在!').show();
                            error_ylname = false;
                        }else {
                            $('#ylname').next().hide();
                            error_ylname = true;
                        };
                    }
                });
            };
        };
    };
    /*
        功能: 判断单包重量
     */
    function piedw_judge() {
        var piedw = $('#piedw').val();
        var re = /^[0-9]+\.?[0-9]*$/;
        var two_re = /^0+\.?0*$/;
        if (re.test(piedw)){
            if (two_re.test(piedw)){
                $('#piedw').siblings('span').text('格式不正确或没有正确输入数字!').show();
                error_piedw = false;
            }else {
                $('#piedw').siblings('span').hide();
                error_piedw = true;
            };
        }else {
            $('#piedw').siblings('span').text('格式不正确或没有正确输入数字!').show();
            error_piedw = false;
        };

    };
});