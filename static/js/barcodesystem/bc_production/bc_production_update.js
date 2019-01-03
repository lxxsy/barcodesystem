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
    var error_scph = true;
    var error_jhrq = true;
    var error_ScsxRwcs = true;
    var error_scsl = true;
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
    var scjhb_bh = $('#scjhb_bh').val(); // 如果是点击修改页面，val值会存在
     /*
        获取要修改的生产计划id，请求视图加载模板并渲染数据
     */
    if (scjhb_bh){
        $.ajax({
            url:'/production/update_production',
            data:{"scjhb_bh":scjhb_bh},
            type:"get",
            async:false,
            success:function(data){
                template.defaults.imports.dateFormat = function(date, format){
                    return date;
                };
                $('#form_submit').html(template('scjhb', {spl: data.spl, scrq: data.scrq, cpid: data.cpid, username: data.username,
                    sl: data.sl, cs: data.cs, dw: data.dw, zt: data.zt, bz: data.bz, bc: data.bc, cpname: data.cpname,
                    todaywork_list: JSON.parse(data.todaywork_list)}));
            }
        });
        var Original = $('#spl').val(); // 页面加载完毕，获取计划单号值，有值则为修改，ajax判断该值
        var arr = [];
        $('.scph').each(function () {
            arr.push($(this).val());
        });
    };
    /*
        页面加载完毕触发ajax请求，获取所有的产品id，渲染到产品编号表单控件中，接着运行函数使计划副表产品与配方信息渲染出来
     */
    $.get('/production/query_production1', function (data) {
        $.each(JSON.parse(data.cpml_list) ,function (index, item) {
            $('#cpid').append('<option value='+item.pk+'>'+item.pk+'</option>');
            $('#cpname').append('<option value='+item.fields.cpmc+'>'+item.fields.cpmc+'</option>');
        });
    });
     /*
        点击增加生产计划副表时触发，追加一行表格
     */
    $('.add-detailed').click(function () {
        $('#cs').val(parseInt($('#cs').val()) + 1);
        $('.tbody').append('<tr>'+
                    '<td><input type="text" name="scph" class="scph"><span class="tips"></span></td>'+
                    '<td><input type="date" name="jhrq" class="jhrq"><span class="tips"></span></td>'+
                    '<td><input type="number" name="scsx" class="scsx"><span class="tips"></span></td>'+
                    '<td><input type="text" name="cpbh" class="cpbh" readonly></td>'+
                    '<td><input type="text" name="cpmc" class="cpmc" readonly></td>'+
                    '<td><input type="text" name="pfbh" class="pfbh" readonly></td>'+
                    '<td><input type="text" name="pfmc" class="pfmc" readonly></td>'+
                    '<td><input type="number" name="rwcs" class="rwcs" value="1"><span class="tips"></span></td>'+
                    '<td><input type="text" name="scsl" class="scsl"><span class="tips"></span></td>'+
                    '<td><input type="number" name="scxh" class="scxh"></td>'+
                    '<td><input type="text" name="scbz" class="scbz"></td>'+
                    '<td><input type="checkbox" name="sczt" checked="checked" class="sczt" value="1" disabled></td>'+
                    '<td><a href="javascript:;" class="glyphicon glyphicon-remove f_delete"></a></td>'+
                '</tr>');
        var judge = 1;  // 当新增计划明细时，该值等于1，说明
        select_product(judge);
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
        产品编号失去焦点触发，判断输入的值是否合理
     */
    $('#datas').change(function () {
        var judge = 0;
        datas_judge();
        select_product(judge);
    });
    /*
        数量失去焦点触发，判断输入的值是否合理
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
        $('#cs').val(parseInt($('#cs').val()) - 1);
        $(this).parents('tr').remove();
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
        判断计划明细表的生产数量是否合理
     */
    $('.tbody').on('blur', '.scsl', function () {
        var $this_scsl = $(this);
        var scsl = $(this).val();
        scsl_judge($this_scsl, scsl);
    });
    /*
        提交表单触发，判断表单内容是否合理，合理提交到后台
     */
    $('#form_submit').submit(function () {
        spl_judge();
        scrq_judge();
        datas_judge();
        sl_judge();
        $('.tbody tr').each(function () {
            var $this_scph = $(this).find('.scph');
            var $this_jhrq = $(this).find('.jhrq');
            var $this_scsx = $(this).find('.scsx');
            var $this_rwcs = $(this).find('.rwcs');
            var $this_scsl = $(this).find('.scsl');
            var scph = $(this).find('.scph').val();
            var jhrq = $(this).find('.jhrq').val();
            var scsx = $(this).find('.scsx').val();
            var rwcs = $(this).find('.rwcs').val();
            var scsl = $(this).find('.scsl').val();
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
            scsl_judge($this_scsl, scsl);
            if (error_scsl === false){
                return false;
            };
        });
        if(error_cpid === true && error_spl === true && error_scrq === true && error_sl === true &&
            error_cs === true && error_scph === true && error_jhrq === true && error_ScsxRwcs === true && error_scsl === true){
            return true;
        }else {
            return false;
        };
    });
     /*
        功能： 判断产品编号的输入是否合理
     */
    function datas_judge() {
        var current_value = $('#datas').val();
        if (current_value === ''){
            $('#datas').next().text('产品编号不能为空!').show();
            error_cpid = false;
        }else {
            $.get('/production/query_production5', {current_value: current_value}, function (data) {
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
        功能：操作计划明细表的产品，配方输入框的值
     */
    function select_product(judge) {
        var cpid = $('#datas').val();
        $.get('/production/query_production2', {cpid: cpid}, function (data) {
            if (data.product_null != ''){
                $('.cpbh').val(data.cpbh);
                $('.cpmc').val(data.cpmc);
                $('.pfbh').val(data.pfbh);
                $('.pfmc').val(data.pfmc);
                $('.scxh').val(data.pfsc);
                if (judge === 1){
                    $('.jhrq').eq(-1).val(year+'-'+month+'-'+day);
                };
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
                $('#spl').next().text('计划单号含有不允许符号!').show();
                error_spl = false;
            }else{
                $.get('/production/query_production3', {Original: Original, spl: spl}, function (data) {
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
        var re = /^\d+\.?\d*$/;
        if (sl <= 0){
            $('#sl').next().text('不能小于或等于0').show();
            error_sl = false;
        }else if (re.test(sl)){
            $('#sl').next().hide();
            error_sl = true;
        }else{
            $('#sl').next().text('请输入正确数字').show();
            error_sl = false;
        };
    };
     /*
        功能： 判断批次的输入是否合理
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
    /*
        功能： 判断计划明细表生产批号的输入是否合理
     */
    function scph_judge($this_scph, scph) {
        $('.scph').next().hide();
        var re = /\W+/;
        var judge = 0;
        $.each($('.scph').not($($this_scph)) ,function (index, item) {
            if (scph === item.value){
                $($this_scph).next().text('生产批号已存在').show();
                error_scph = false;
                judge = 1;
                return false;
            };
        });
        if (judge === 1){
            return false;
        };
        if (scph === ''){
            $($this_scph).next().text('生产批号不能为空！').show();
            error_scph = false;
        }else {
            if (re.test(scph)){
                $($this_scph).next().text('生产批号含有不允许符号!').show();
                error_scph = false;
            }else {
                $.ajax({
                    url:'/production/query_production4',
                    data:{"arr":arr, "scph": scph},
                    type:"get",
                    traditional:true,
                    async:false,
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
        if(ScsxRwcs.length === 0){
            $($this_ScsxRwcs).next().text('请输入正确数字').show();
            error_ScsxRwcs = false;
        }else if(ScsxRwcs <= 0){
            $($this_ScsxRwcs).next().text('不能小于或等于0').show();
            error_ScsxRwcs = false;
        }else if(re.test(ScsxRwcs)){
            $($this_ScsxRwcs).next().text('不能为小数').show();
            error_ScsxRwcs = false;
        }else {
            $($this_ScsxRwcs).next().hide();
            error_ScsxRwcs = true;
        };
    };
    /*
        功能： 判断计划明细表生产数量的输入是否合理
     */
    function scsl_judge($this_scsl, scsl) {
        $('.scsl').next().hide();
        var sl = $('#sl').val(); // 100
        var re = /^\d+\.?\d*$/;
        var num = 0;
        $.each($('.scsl'), function (index, item) {
            num += parseFloat(item.value);
        });
        console.log(num);
        if (num > sl){
            console.log('a');
            $($this_scsl).next().text('数量已超出').show();
            error_scsl = false;
            return false;
        };
        if (scsl <= 0){
            $($this_scsl).next().text('不能小于或等于0').show();
            error_scsl = false;
        }else if (re.test(scsl)){
            $($this_scsl).next().hide();
            error_scsl = true;
        }else{
            $($this_scsl).next().text('请输入正确数字').show();
            error_scsl = false;
        };
    };
});