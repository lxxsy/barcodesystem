/**
 * Created by LILI on 2018/8/17.
 */

$(function () {
    var error_scph = true;
    var error_scrq = true;
    var error_cpid = true;
    var error_sl = true;
    var Original = $('#scph').val();
    var date = new Date();
    var year = date.getFullYear();
    var month = date.getMonth()+1;
    var day = date.getDate();
    if (month.toString().length === 1){
        month = '0'+month;
    };
    if (day.toString().length === 1){
        day = '0'+day;
    };
     /*
        页面加载完毕触发ajax请求，获取所有的产品id，渲染到产品编号表单控件中
     */
    $.get('/production/select_product1', function (data) {
        var cpid = $('#cpid').val();
        $.each(JSON.parse(data.cpml_list), function (index, item) {
            if (item.pk != cpid){
                $('#cpid').append('<option value='+item.pk+'>'+item.pk+'</option>');
            };
        });
    });
    /*
        产品编号输入框的值发生变化时触发，根据值使副表的产品及配方信息发生变化
     */
    $('#cpid').change(function () {
        select_product();
    });
    /*
        生产批号失去焦点触发，判断输入的值是否合理
     */
    $('#scph').blur(function () {
        scph_judge(Original);
    });
    /*
        日期失去焦点触发，判断输入的值是否合理
     */
    $('#scrq').blur(function () {
        scrq_judge();
    });
     /*
        数量失去焦点触发，判断输入的值是否合理
     */
    $('#sl').blur(function () {
        sl_judge();
    });
     /*
        提交表单触发，判断表单内容是否合理，合理提交到后台
     */
    $('#form_submit').submit(function () {
        if ($('#cpid').val() === ''){
            error_cpid = false;
        };
        scph_judge(Original);
        scrq_judge();
        sl_judge();
        if(error_cpid === true && error_scph === true && error_scrq === true && error_sl === true){
            return true;
        }else {
            return false;
        };
    });
     /*
        功能：操作计划明细表的产品，配方输入框的值
     */
    function select_product() {
        var cpid = $('#cpid').val();
        $.get('/production/select_product2', {cpid: cpid}, function (data) {
            if (data.product_null){
                alert('Not found');
            }else{
                $('#cpname').val(data.cpmc);
                $('#pbbh').val(data.pfbh);
                $('#pbname').val(data.pfmc);
            };
        });
    };
    /*
        功能： 判断生产批号的输入是否合理
     */
    function scph_judge(Original) {
        var scph = $('#scph').val();
        var re = /\w+/;
        if (scph.length===0){
            $('#scph').next().text('不能为空').show();
            error_scph = false;
        }else{
            if (re.test(scph)){
                $.get('/production/select_product3', {scph: scph, Original: Original}, function (data) {
                    if (data.bool === 0){
                        $('#scph').next().text('计划单号已存在').show();
                        error_scph = false;
                    }else {
                        $('#scph').next().hide();
                        error_scph = true;
                    };
                });
            }else{
                $('#scph').next().text('至少需要一位字符或数字').show();
                error_scph = false;
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
            $('#scrq').next().text('请正确填写年份').show();
            error_scrq = false;
        }else if(arry[1] < month){
            $('#scrq').next().text('请正确填写月份').show();
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
        功能： 判断数量的输入是否合理
     */
    function sl_judge() {
        var sl = $('#sl').val();
        var re = /\.+/;
        if (sl[0] === '0'){
            $('#sl').next().text('第一位数字不能为0').show();
            error_sl = false;
        }else if(sl < 0){
            $('#sl').next().text('不能小于0').show();
            error_sl = false;
        }else if(sl === ''){
            $('#sl').next().text('不能为空或不是一个数字').show();
            error_sl = false;
        }else if(re.test(sl)){
            $('#sl').next().text('不能为小数').show();
            error_sl = false;
        }else {
            $('#sl').next().hide();
            error_sl = true;
        };
    };
});