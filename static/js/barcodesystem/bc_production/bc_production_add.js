/**
 * Created by LILI on 2018/7/10.
 */
$(function () {
    var error_spl = false;
    var error_scrq = false;
    var error_cpid = false;
    var error_cpname = false;
    var error_sl = false;
    var error_cs = false;
    var error_bc = false;
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
    $.get('/production/query_production1', function (data) {
        $.each(JSON.parse(data.cpml_list) ,function (index, item) {
            $('#cpid').append('<option value='+item.pk+'>'+item.pk+'</option>');
            $('#cpname').append('<option value='+item.fields.cpmc+'>'+item.fields.cpmc+'</option>');
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
    $('.data_production_cpid').change(function () {
        data_production_cpid_judge();
    });
     /*
        产品名称失去焦点后触发
     */
    $('.data_production_cpname').change(function () {
        data_production_cpname_judge();
    });
    /*
        生产数量失去焦点触发，判断输入的值是否合理
     */
    $('#sl').blur(function () {
        sl_judge();
    });
    /*
        批次数失去焦点触发，判断输入的值是否合理
     */
    $('#cs').blur(function () {
        cs_judge();
    });
    /*
        班次失去焦点触发，判断输入的值是否合理
     */
    $('#bc').blur(function () {
        bc_judge();
    });
    /*
        提交表单触发，判断表单内容是否合理，合理提交到后台
     */
    $('#form_submit').submit(function () {
        spl_judge();
        scrq_judge();
        submit_cpid_judge();
        sl_judge();
        cs_judge();
        bc_judge();
        if(error_cpid === true && error_cpname === true && error_spl === true && error_scrq === true && error_sl === true &&
            error_cs === true && error_bc === true){
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
                $.get('/production/query_production3', {spl: spl}, function (data) {
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
            $('#scrq').next().text('请正确填写年份').show();
            error_scrq = false;
        }else if(arry[1] < month){
            $('#scrq').next().text('请正确填写月份').show();
            error_scrq = false;
        }else if(arry[2] < day){
            $('#scrq').next().text('请正确填写日期').show();
            error_scrq = false;
        }else {
            $('#scrq').next().hide();
            error_scrq = true;
        };
    };
    /*
        功能：当提交表单时触发此函数判断原料代码，和输入框判断不同
     */
    function submit_cpid_judge() {
        var cpid = $('.data_production_cpid').val();
        $.ajax({
            url:'/production/query_production5',
            data:{cpid: cpid},
            type:"get",
            async:false,
            success:function(data){
                if (data.cpid_bool === 0){
                    $('.data_production_cpid').next().text('产品编号不能为空').show();
                    error_cpid = false;
                    error_cpname = false;
                }else {
                    $('.data_production_cpid').next().hide();
                    error_cpid = true;
                    error_cpname = true;
                };
            }
        });
    };
    /*
        功能：判断产品编号的输入是否合理
     */
    function data_production_cpid_judge() {
        $('.data_production_cpid').next().hide();
        $('.data_production_cpname').next().hide();
        var cpid = $('.data_production_cpid').val();
        $.ajax({
            url:'/production/query_production5',
            data:{cpid: cpid},
            type:"get",
            async:false,
            success:function(data){
                $('.data_production_cpname').val(data.cpmc);
                if (data.cpid_bool === 0){
                    $('.data_production_cpid').next().text('产品不存在').show();
                    error_cpid = false;
                }else{
                    $('.data_production_cpid').next().hide();
                    error_cpid = true;
                };
            }
        });
    };
    /*
        功能：判断产品名称的输入是否合理
     */
    function data_production_cpname_judge() {
        $('.data_production_cpid').next().hide();
        $('.data_production_cpname').next().hide();
        var cpname = $('.data_production_cpname').val();
        $.ajax({
            url:'/production/query_production6',
            data:{cpname: cpname},
            type:"get",
            async:false,
            success:function(data){
                $('.data_production_cpid').val(data.cpid);
                if (data.cpname_bool === 0){
                    $('.data_production_cpname').next().text('产品不存在').show();
                    error_cpname = false;
                }else{
                    $('.data_production_cpname').next().hide();
                    error_cpname = true;
                };
            }
        });
    };
    /*
        功能： 判断生产数量的输入是否合理
     */
    function sl_judge() {
        var sl = $('#sl').val();
        var re = /^[0-9]+\.?[0-9]*$/;
        var two_re = /^0+\.?0*$/;
        if (re.test(sl)){
            if (two_re.test(sl)){
                $('#sl').next().text('格式不正确或没有正确输入数字!').show();
                error_sl = false;
            }else {
                $('#sl').next().hide();
                error_sl = true;
            };
        }else {
            $('#sl').next().text('格式不正确或没有正确输入数字！').show();
            error_sl = false;
        };
    };
    /*
        功能： 判断批次数的输入是否合理
     */
    function cs_judge() {
        var cs = $('#cs').val();
        var re = /^[1-9][0-9]?$/;
        if (re.test(cs)){
            $('#cs').next().hide();
            error_cs = true;
        }else {
            $('#cs').next().text('至多为2位数字或没有正确输入整数！').show();
            error_cs = false;
        };
    };
    /*
        功能： 判断班次的输入是否合理
     */
    function bc_judge() {
        var bc = $('#bc').val();
        var re = /^[1-9][0-9]?$/;
        if (re.test(bc)){
            $('#bc').next().text('格式不正确或没有正确输入整数!').show();
            error_bc = false;
        }else {
            $('#bc').next().hide();
            error_bc = true;
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