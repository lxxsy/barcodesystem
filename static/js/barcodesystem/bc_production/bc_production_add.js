/**
 * Created by LILI on 2018/7/10.
 */
$(function () {
    var error_spl = true;
    var error_scrq = true;
    var error_cpid = true;
    var error_sl = true;
    var error_cs = true;
    var date = new Date();
    var year = date.getFullYear();
    var month = date.getMonth()+1;
    var day = date.getDate();
    if (month.toString().length === 1){
        month = '0'+month;
    };
    if (day.toString().length === 1){
        day = '0'+day;
    }
    /*
        页面加载完毕触发ajax请求，获取所有的产品id，渲染到产品编号表单控件中，接着运行函数使计划副表产品与配方信息渲染出来
     */
    $.get('/production/select_product1', function (data) {
        $.each(JSON.parse(data.cpml_list) ,function (index, item) {
            $('#cpid').append('<option value='+item.pk+'>'+item.pk+'</option>');
        });
    });
    $('#scrq').val(year+'-'+month+'-'+day); // 获取当前日期并渲染到计划日期输入框中

    /*
        计划单号失去焦点触发，判断输入的值是否合理
     */
    $('#spl').blur(function () {
        spl_judge();
    });
    /*
        日期失去焦点触发，判断输入的值是否合理
     */
    $('#scrq').blur(function () {
        scrq_judge();
    });
    /*
        产品编号失去焦点后触发
     */
    $('#datas').blur(function () {
        datas_judge();
    });
    /*
        数量失去焦点触发，判断输入的值是否合理
     */
    $('#sl').blur(function () {
        sl_judge();
        /*
        var bool = true;
        var sl = $(this).val();
        var cs = $('#cs').val();
        var re = /^[0-9]+$/;
        if (re.test(cs) && re.test(sl)){
            select_product(cs, bool);
        };*/
    });
    /*
        批次数失去焦点触发，判断输入的值是否合理
     */
    $('#cs').blur(function () {
        cs_judge();
        /*
        $('.tbody').children().remove();
        var re = /^[0-9]+$/;
        var bool = true;
        var cs = $(this).val();
        var sl = $('#sl').val();
        if (re.test(cs) && (re.test(sl) || sl === '')){
            for (var i = 0; i<cs; i++){
                tbody_append(bool);
            };
        };*/
    });
    /*
        提交表单触发，判断表单内容是否合理，合理提交到后台
     */
    $('#form_submit').submit(function () {
        spl_judge();
        scrq_judge();
        datas_judge();
        sl_judge();
        cs_judge();
        if(error_cpid === true && error_spl === true && error_scrq === true && error_sl === true &&
            error_cs === true){
            return true;
        }else {
            return false;
        };
    });
    /*
        功能： 判断计划单号的输入是否合理
     */
    function spl_judge() {
        var spl = $('#spl').val();
        var re = /\W+/;
        if (spl.length===0){
            $('#spl').next().text('计划单号不能为空！').show();
            error_spl = false;
        }else{
            if (re.test(spl)){
                $('#spl').next().text('计划单号含有不允许符号!').show();
                error_spl = false;
            }else{
                $.get('/production/select_product3', {spl: spl}, function (data) {
                    if (data.bool === 0){
                        $('#spl').next().text('计划单号已存在!').show();
                        error_spl = false;
                    }else {
                        $('#spl').next().hide();
                        error_spl = true;
                    };
                });
            };
        };
    };
    /*
        功能：判断日期的输入是否合理
     */
    function scrq_judge() {
        var scrq = $('#scrq').val();
        var arry = scrq.split('-');
        if (scrq === ''){
            $('#scrq').next().text('请输入准确的日期格式').show();
            error_scrq = false;
        }else if(arry[0] < year || arry[0].length != 4){
            $('#scrq').next().text('请填写正确年份').show();
            error_scrq = false;
        }else if(arry[1] < month){
            $('#scrq').next().text('请填写正确月份').show();
            error_scrq = false;
        }else if(arry[2] < day){
            $('#scrq').next().text('填写的日期小于当前日期').show();
            error_scrq = false;
        }else {
            $('#scrq').next().hide();
            error_scrq = true;
        };
    };
     /*
        功能：判断产品编号的输入是否合理
     */
    function datas_judge() {
        var current_value = $('#datas').val();
        if (current_value === ''){
            $('#datas').next().text('产品编号不能为空!').show();
            error_cpid = false;
        }else {
            $.get('/production/select_product5', {current_value: current_value}, function (data) {
                if (data.cpml_bool === 0){
                    $('#datas').next().text('没有此产品编号!').show();
                    error_cpid = false;
                }else {
                    $('#datas').next().hide();
                    error_cpid = true;
                };
            });
        };
    };
    /*
        功能： 判断数量的输入是否合理
     */
    function sl_judge() {
        var sl = $('#sl').val();
        var re = /\.+/;
        if(sl.length === 0){
            $('#sl').next().text('请输入正确数字').show();
            error_sl = false;
        }else if(sl <= 0){
            $('#sl').next().text('不能小于或等于0').show();
            error_sl = false;
        }else if(re.test(sl)){
            $('#sl').next().text('不能为小数').show();
            error_sl = false;
        }else {
            $('#sl').next().hide();
            error_sl = true;
        };
    };
    /*
        功能： 判断批次数的输入是否合理
     */
    function cs_judge() {
        var cs = $('#cs').val();
        var re = /\.+/;
        if(cs.length === 0){
            $('#cs').next().text('请输入正确数字').show();
            error_cs = false;
        }else if(cs <= 0){
            $('#cs').next().text('不能小于或等于0').show();
            error_cs = false;
        }else if(re.test(cs)){
            $('#cs').next().text('不能为小数').show();
            error_cs = false;
        }else {
            $('#cs').next().hide();
            error_cs = true;
        };
    };
});
    /*
        功能：操作计划明细表的产品，配方输入框的值

    function select_product(cs, bool) {
        var cpid = $('#cpid').val();
        var sl = $('#sl').val();
        var num = parseInt(sl/cs);
        $.get('/production/select_product2', {cpid: cpid}, function (data) {
            if (data.product_null != ''){
                $('.cpbh').val(data.cpbh);
                $('.cpmc').val(data.cpmc);
                $('.pfbh').val(data.pfbh);
                $('.pfmc').val(data.pfmc);
                $('.scxh').val(data.pfsc);
                if (bool === false){
                    $('.jhrq').eq(-1).val(year+'-'+month+'-'+day);
                }else {
                    $('.jhrq').val(year+'-'+month+'-'+day);
                };
                $('.scsl').val(num);
            };
        });
    };*/