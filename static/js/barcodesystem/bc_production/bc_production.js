/**
 * Created by LILI on 2018/7/10.
 */
$(function () {
    var Original = $('#spl').val();
    var arr = [];
    $('.scph').each(function () {
        arr.push($(this).val());
    });
    var error_spl = true;
    var error_scrq = true;
    var error_cpid = true;
    var error_sl = true;
    var error_scph = true;
    var error_jhrq = true;
    var error_ScsxRwcs = true;
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
        页面加载完毕触发ajax请求，获取所有的产品id，渲染到产品编号表单控件中，接着运行函数使计划副表产品与配方信息渲染出来
     */
    $.get('/production/select_product1', function (data) {
        var cpid = $('#cpid').val();
        $.each(JSON.parse(data.cpml_list) ,function (index, item) {
            if (item.pk != cpid){
                $('#cpid').append('<option value='+item.pk+'>'+item.pk+'</option>');
            };
        });
        select_product();
    });
    $('#scrq').val(year+'-'+month+'-'+day);
    /*
        点击增加生产计划副表时触发，追加一行表格
     */
    $('.add-detailed').click(function () {
        $('.tbody').append('<tr>'+
                    '<td><input type="text" name="scph" class="scph"><span class="tips"></span></td>'+
                    '<td><input type="date" name="jhrq" class="jhrq"><span class="tips"></span></td>'+
                    '<td><input type="number" name="scsx" class="scsx"><span class="tips"></span></td>'+
                    '<td><input type="text" name="cpbh" class="cpbh" readonly></td>'+
                    '<td><input type="text" name="cpmc" class="cpmc" readonly></td>'+
                    '<td><input type="text" name="pfbh" class="pfbh" readonly></td>'+
                    '<td><input type="text" name="pfmc" class="pfmc" readonly></td>'+
                    '<td><input type="number" name="rwcs" class="rwcs" value="1"><span class="tips"></span></td>'+
                    '<td><input type="number" name="scsl" class="scsl"></td>'+
                    '<td><input type="number" name="scxh" class="scxh"></td>'+
                    '<td><input type="text" name="scbz" class="scbz"></td>'+
                    '<td><input type="text" name="scbc" class="scbc"></td>'+
                    '<td><input type="checkbox" name="sczt" checked="checked" class="sczt" value="1" disabled></td>'+
                    '<td><a href="javascript:;" class="glyphicon glyphicon-remove f_delete"></a></td>'+
                '</tr>');
        select_product();
    });
    /*
        产品编号输入框的值发生变化时触发，根据值使副表的产品及配方信息发生变化
     */
    $('#cpid').change(function () {
        select_product();
    });
    /*
        点击主表启用触发，判断此控件是勾选还是未勾选，得到判断值后使所有的多选框控件变成这个判断值
     */
    $('#zt').click(function () {
        var bool = $(this).prop('checked');
        $(':checkbox').prop('checked', bool);
    });
    /*
        点击副表删除按钮触发，搜寻此按钮的tr父级，然后删除
     */
    $('.tbody').on('click', '.f_delete', function () {
        $(this).parents('tr').remove();
    });
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
        数量失去焦点触发，判断输入的值是否合理
     */
    $('#sl').blur(function () {
        sl_judge();
    });
    /*
        判断计划明细表的生产批号是否合理
     */
    $('.tbody').on('blur', '.scph', function () {
        var $this_scph = $(this);
        var scph = $(this).val();
        scph_judge($this_scph, scph);
    });
    /*
        判断计划明细表的计划日期是否合理
     */
    $('.tbody').on('blur', '.jhrq', function () {
        var $this_jhrq = $(this);
        var jhrq = $(this).val();
        jhrq_judge($this_jhrq, jhrq);
    });
    /*
        判断计划表明细生产顺序或任务次数是否合理
     */
    $('.tbody').on('blur', '.scsx, .rwcs', function () {
        var $this_ScsxRwcs = $(this);
        var ScsxRwcs = $(this).val();
        ScsxRwcs_judge($this_ScsxRwcs, ScsxRwcs);
    });
    /*
        提交表单触发，判断表单内容是否合理，合理提交到后台
     */
    $('#form_submit').submit(function () {
        if ($('#cpid').val() === ''){
            error_cpid = false;
        };
        spl_judge();
        scrq_judge();
        sl_judge();
        $('.tbody tr').each(function () {
            var $this_scph = $(this).find('.scph');
            var $this_jhrq = $(this).find('.jhrq');
            var $this_scsx = $(this).find('.scsx');
            var $this_rwcs = $(this).find('.rwcs');
            var scph = $(this).find('.scph').val();
            var jhrq = $(this).find('.jhrq').val();
            var scsx = $(this).find('.scsx').val();
            var rwcs = $(this).find('.rwcs').val();
            scph_judge($this_scph, scph);
            if (error_scph === false){
                return false;
            };
            jhrq_judge($this_jhrq, jhrq);
            if (error_jhrq === false){
                return false;
            };
            ScsxRwcs_judge($this_scsx, scsx);
            if (error_ScsxRwcs === false){
                return false;
            };
            ScsxRwcs_judge($this_rwcs, rwcs);
            if (error_ScsxRwcs === false){
                return false;
            };
        });
        if(error_cpid === true && error_spl === true && error_scrq === true && error_sl === true && error_scph === true
            && error_jhrq === true && error_ScsxRwcs === true){
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
                $('.cpbh').val(data.cpbh);
                $('.cpmc').val(data.cpmc);
                $('.pfbh').val(data.pfbh);
                $('.pfmc').val(data.pfmc);
                $('.jhrq').val(year+'-'+month+'-'+day);
            };
        });
    };
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
                $('#cpid').next().text('计划单号含有不允许符号!').show();
                error_spl = false;
            }else{
                $.get('/production/select_product3', {Original: Original, spl: spl}, function (data) {
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
    /*
        功能： 判断计划明细表生产批号的输入是否合理
     */
    function scph_judge($this_scph, scph) {
        var re = /\W+/;
        if (scph === ''){
            $($this_scph).next().text('生产批号不能为空！').show();
            error_scph = false;
        }else {
            if (re.test(scph)){
                $($this_scph).next().text('生产批号含有不允许符号!').show();
                error_scph = false;
            }else {
                $.ajax({
                    url:'/production/select_product4',
                    data:{"arr":arr, "scph": scph},
                    type:"get",
                    traditional:true,
                    success:function(data){
                        if (data.scph_bool === 0){
                            $($this_scph).next().text('生产批号已存在').show();
                            error_scph = false;
                        }else {
                            $($this_scph).next().hide();
                            error_scph = true;
                        };
                    }
                });
            };
        };
    };
    /*
        功能： 判断计划明细表计划日期的输入是否合理
     */
    function jhrq_judge($this_jhrq, jhrq) {
        var scrq = $('#scrq').val();
        var scrq_arry = scrq.split('-');
        var jhrq_arry = jhrq.split('-');
        if (scrq === '' || jhrq === ''){
            $($this_jhrq).next().text('请把生产计划表或明细表日期填写完整').show();
            error_jhrq = false;
        }else {
            if (scrq_arry[0].length != 4 || jhrq_arry[0].length != 4){
                $($this_jhrq).next().text('请正确填写年份').show();
                error_jhrq = false;
            }else if(jhrq_arry[0] < scrq_arry[0]){
                $($this_jhrq).next().text('计划明细表年份不能小于计划年份').show();
                error_jhrq = false;
            }else if(jhrq_arry[0] > scrq_arry[0]){
                $($this_jhrq).next().hide();
                error_jhrq = true;
            }else if(jhrq_arry[1] < scrq_arry[1]){
                $($this_jhrq).next().text('计划明细表月份不能小于计划月份').show();
                error_jhrq = false;
            }else if(jhrq_arry[2] < scrq_arry[2]){
                $($this_jhrq).next().text('计划明细表日期不能小于计划日期').show();
                error_jhrq = false;
            }else {
                $($this_jhrq).next().hide();
                error_jhrq = true;
            };
        };
    };
    /*
        功能： 判断计划明细表生产顺序或任务次数的输入是否合理，因判断逻辑一样
     */
    function ScsxRwcs_judge($this_ScsxRwcs, ScsxRwcs) {
        var re = /\./;
        if (ScsxRwcs === ''){
            $($this_ScsxRwcs).next().text('不能为空或不是数字').show();
            error_ScsxRwcs = false;
        }else if(ScsxRwcs < '0'){
            $($this_ScsxRwcs).next().text('不能小于0').show();
            error_ScsxRwcs = false
        }else if(re.test(ScsxRwcs)){
            $($this_ScsxRwcs).next().text('不能为小数').show();
            error_ScsxRwcs = false;
        }else {
            $($this_ScsxRwcs).next().hide();
            error_ScsxRwcs = true;
        };
    };
});

