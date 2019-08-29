
$(function () {
    var error_ylid = false;
    var error_ylname = false;
    var error_piedw = false;
    var error_zf = false;
    var error_stockid = false;
    /*
        获取要修改的原料id，请求视图加载模板并渲染数据
     */
    var ylinfo_id = $('#ylinfo_id').val();
    $.ajax({
        url:'/rmaterial/update_rmaterial',
        data:{"ylinfo_id":ylinfo_id},
        type:"get",
        async:false,
        success:function(data){
            /*
            template.defaults.imports.dateFormat = function(date, format){
                return date;
            };*/
            if (data.bool === 1){
                $('#form_submit').html(template('ylinfo', {ylid: data.ylid, ylname: data.ylname, dw: data.dw,
                    piedw: data.piedw, zbq: data.zbq, goodzbq: data.goodzbq, park: data.park, pieprice: data.pieprice,
                    minsl: data.minsl, maxsl: data.maxsl, zf_name: data.zf_name, zf_id: data.zf_id,
                    stockid_name: data.stockid_name, stockid: data.stockid, tymc: data.tymc,
                    ysbz: data.ysbz, barcode: data.barcode, bz: data.bz, ylzt: data.ylzt}));
            }else {
                alert('出现异常情况');
            };
        }
    });
    /*
        获取页面上的原料ID与原料名称，称为原内容。目的是修改以后会拿原内容与新内容做比较，如果新内容和原内容相同则表示没有做修改
     */
    var Original = $('#ylid').val();
    var Original_name = $('#ylname').val();
    /*
        获取原料分类与仓库并填充：首先获取已存在分类与仓库，进行填充时首先排除已存在的分类与仓库
     */
    $.get('/rmaterial/query_rmaterial1', function (data) {
        var zf = $('#zf').val();
        var stockid = $('#stockid').val();
        $.each(JSON.parse(data.ylfl_list) ,function (index, item) {
            if (item.pk != zf) {
                $('#zf').append('<option value='+item.pk+'>'+item.fields.flmc+'</option>');
            };
        });
        $.each(JSON.parse(data.stockinfo_list) ,function (index, item) {
            if (item.pk != stockid){
                $('#stockid').append('<option value='+item.pk+'>'+item.fields.stockname+'</option>');
            };
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
        // var re = /\W+/;
        if (ylid.length===0){
            $('#ylid').next().text('原料代码不能为空！').show();
            error_ylid = false;
        }else{
            $.ajax({
                url:'/rmaterial/query_rmaterial2',
                data:{Original: Original, ylid: ylid},
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
     /*
        功能: 判断原料名称
     */
   function ylname_judge() {
        var ylname = $('#ylname').val();
        //var re = /\s+|-+|\++|\?+/;
        if (ylname.length === 0){
            $('#ylname').next().text('原料名称不能为空!').show();
            error_ylname = false;
        }else {
            $.ajax({
                url:'/rmaterial/query_rmaterial3',
                data:{Original_name: Original_name, ylname: ylname},
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