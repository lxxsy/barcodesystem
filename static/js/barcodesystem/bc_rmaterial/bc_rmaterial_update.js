
$(function () {
    var error_ylid = true;
    var error_ylname = true;
    var error_piedw = true;
    var error_zf = true;
    var error_stockid = true;
    var ylinfo_id = $('#ylinfo_id').val();
    /*
        获取要修改的原料id，请求视图加载模板并渲染数据
     */
    $.ajax({
        url:'/rmaterial/update_rmaterial',
        data:{"ylinfo_id":ylinfo_id},
        type:"get",
        async:false,
        success:function(data){
            template.defaults.imports.dateFormat = function(date, format){
                return date;
            };
            if (data.bool === 1){
                $('#form_submit').html(template('ylinfo', {ylid: data.ylid, ylname: data.ylname, dw: data.dw,
                    piedw: data.piedw, zbq: data.zbq, goodzbq: data.goodzbq, park: data.park, pieprice: data.pieprice,
                    minsl: data.minsl, maxsl: data.maxsl, zf: data.zf, stockid: data.stockid, tymc: data.tymc,
                    ysbz: data.ysbz, barcode: data.barcode, bz: data.bz, ylzt: data.ylzt}));
            }else {
                alert('出现异常情况');
            };
        }
    });
    var Original = $('#ylid').val();
    /*
        加载原料分类与仓库
     */
    $.get('/rmaterial/query_rmaterial1', function (data) {
        var zf = $('#zf').val();
        var stockid = $('#stockid').val();
        $.each(JSON.parse(data.ylfl_list) ,function (index, item) {
            if (item.pk != zf) {
                $('#zf').append('<option value=' + item.pk + '>' + item.pk + '</option>');
            };
        });
        $.each(JSON.parse(data.stockinfo_list) ,function (index, item) {
            if (item.pk != stockid){
                $('#stockid').append('<option value='+item.pk+'>'+item.pk+'</option>');
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
        if ($('#zf').val() === ''){
            error_zf = false;
        };
        if ($('#stockid').val() === ''){
            error_stockid = false;
        };
        ylid_judge();
        ylname_judge();
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
                $.get('/rmaterial/query_rmaterial2', {Original: Original, ylid: ylid}, function (data) {
                    if (data.bool === 0){
                        $('#ylid').next().text('原料代码已存在!').show();
                        error_ylid = false;
                    }else {
                        $('#ylid').next().hide();
                        error_ylid = true;
                    };
                });
            };
        };
    };
     /*
        功能: 判断原料代码
     */
    function ylname_judge() {
        var ylname = $('#ylname').val();
        var re = /\s+|-+|\++|\?+/;
        if (ylname.length === 0){
            $('#ylname').next().text('原料名称不能为空!').show();
            error_ylname = false;
        }else if(re.test(ylname)){
            $('#ylname').next().text('原料名称含有不允许符号!').show();
            error_ylname = false;
        }else {
            $('#ylname').next().hide();
            error_ylname = true;
        };
    };
    /*
        功能: 判断单包重量
     */
    function piedw_judge() {
        var piedw = $('#piedw').val();
        var re = /\.+/;
        if (piedw.length === 0){
            $('#piedw').siblings('span').text('请输入正确数字').show();
            error_piedw = false;
        }else if(piedw <= 0){
            $('#piedw').siblings('span').text('不能小于或等于0').show();
            error_piedw = false;
        }else if(re.test(piedw)){
            $('#piedw').siblings('span').text('不能为小数').show();
            error_piedw = false;
        }else {
            $('#piedw').siblings('span').hide();
            error_piedw = true;
        };
    };
});