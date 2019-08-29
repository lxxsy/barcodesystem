/**
 * Created by LILI on 2018/7/10.
 */
$(function () {
    var error_scrq = false, error_cpid = false, error_cpname = false, error_sl = false;
    var error_bc = false, error_ScsxRwcs = false, error_scsl = false, sl_judge_submit = 0;
    var date = new Date(), year = date.getFullYear(), month = date.getMonth()+1, day = date.getDate();
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
                $('#form_submit').html(template('scjhb', {spl: data.spl, scrq: data.scrq, cpid: data.cpid, user_id: data.user_id,
                    sl: data.sl, cs: data.cs, dw: data.dw, zt: data.zt, bz: data.bz, bc: data.bc, cpname: data.cpname,
                    todaywork_list: JSON.parse(data.todaywork_list)}));
            }
        });
    };
    /*
        打印预览功能，转向RDP预览页面
     */
    $('#btnPreview').click(function () {
        let cpid = $('.data_production_cpid').val();
        let spl = $('#spl').val();
        $.ajax({
            url: '/production/request_data',
            type: 'get',
            data: {cpid: cpid, spl: spl},
            async:false,
            success: function (data) {
                location.href="http://localhost:8080/RDP-SERVER/rdppage/main/976d4e53fd140bd323c1d92657f6daec?spl="+data.spl+"&cpid="+data.cpid;
                /*location.href="http://localhost:8080/RDP-SERVER/rdppage/main/aec846ee60e81578f3feb5a8eca89c4d?spl="+data.spl+"&cpid="+data.cpid;*/
                },
            error: function () {
                alert(data.errors);
            }
        });
    });
    /*
        页面加载完毕后，判断计划明细副表的行数，如果只有一行那么就不提供删除副表行数功能
     */
    if ($('.f_delete').length === 1){
        $('.f_delete').hide();
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
        sl_judge_submit = 1;
        sl_judge(sl_judge_submit);
    });
    /*
        班次失去焦点触发，判断输入的值是否合理
     */
    $('#bc').blur(function () {
        bc_judge();
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
        if ($('.f_delete').length === 1){
            $('.f_delete').hide();
        };
    });
    /*
        判断计划表明细生产顺序或任务次数是否合理---'.scsx, .rwcs'任务次数的判断暂时取消
     */
    $('.tbody').on('blur', '.scsx', function () {
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
        当点击删除按钮时触发
     */
    $('.scjhb_delete').click(function () {
        scjhb_delete();
    });
    /*
        提交表单触发，判断表单内容是否合理，合理提交到后台
     */
    $('#form_submit').submit(function () {
        scrq_judge();
        submit_cpid_judge();
        sl_judge_submit = 0;
        sl_judge(sl_judge_submit);
        bc_judge();
        $('.tbody tr').each(function () {
            var $this_scsx = $(this).find('.scsx');
            var $this_scsl = $(this).find('.scsl');
            var scsx = $(this).find('.scsx').val();
            var scsl = $(this).find('.scsl').val();
            ScsxRwcs_judge($this_scsx, scsx);
            if (error_ScsxRwcs === false){
                return false;
            };
            scsl_judge($this_scsl, scsl);
            if (error_scsl === false){
                return false;
            };
        });
        if(error_cpid === true && error_cpname === true && error_scrq === true && error_sl === true && error_bc === true &&
            error_ScsxRwcs === true && error_scsl === true){
            return true;
        }else {
            return false;
        };
    });
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
            $('.jhrq').val(scrq);
        };
    };
    /*
        功能：当提交表单时触发此函数判断产品代码，和输入框判断不同
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
                    $('.data_production_cpid').next().text('产品不存在').show();
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
                $('.cpbh').val(data.cpbh);
                $('.cpmc').val(data.cpmc);
                $('.pfbh').val(data.pfbh);
                $('.pfmc').val(data.pfmc);
                $('.scxh').val(data.pfsc);
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
                $('.cpbh').val(data.cpid);
                $('.cpmc').val(data.cpmc);
                $('.pfbh').val(data.pfbh);
                $('.pfmc').val(data.pfmc);
                $('.scxh').val(data.pfsc);
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
        功能： 判断生产数量的输入是否合理,参数的作用为：判断是提交表单还是事件，为1那么就修改计划明细的数量，为0说明是提交表单
                ，则不用修改计划明细的数量
     */
    function sl_judge(sl_judge_submit) {
        $('.scsl').next().hide();
        var sl = $('#sl').val();
        var cs = $('#cs').val();
        var re = /^[0-9]+\.?[0-9]*$/;
        var two_re = /^0+\.?0*$/;
        if (re.test(sl)){
            if (two_re.test(sl)){
                $('#sl').next().text('格式不正确或没有正确输入数字!').show();
                error_sl = false;
            }else {
                $('#sl').next().hide();
                error_sl = true;
                if (sl_judge_submit === 1){
                    // 修改后，将明细的数量修改一下
                    $('.scsl').val((parseFloat(sl)/parseFloat(cs)).toFixed(2));
                }
            };
        }else {
            $('#sl').next().text('格式不正确或没有正确输入数字！').show();
            error_sl = false;
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
    /*
        功能： 判断计划明细表生产顺序或任务次数的输入是否合理，因判断逻辑一样
     */
    function ScsxRwcs_judge($this_ScsxRwcs, ScsxRwcs) {
        $('.scsx').next().hide();
        var re = /^[1-9][0-9]{0,2}$/;
        var judge = 0;
        $.each($('.scsx').not($($this_ScsxRwcs)) ,function (index, item) {
            if (ScsxRwcs === item.value){
                $($this_ScsxRwcs).next().text('顺序号已存在').show();
                error_ScsxRwcs = false;
                judge = 1;
                return false;
            };
        });
        if (judge === 1){
            return false;
        };
        if (re.test(ScsxRwcs)){
            $($this_ScsxRwcs).next().hide();
            error_ScsxRwcs = true;
        }else {
            $($this_ScsxRwcs).next().text('格式不正确').show();
            error_ScsxRwcs = false;
        };
    };
    /*
        功能： 判断计划明细表生产数量的输入是否合理
     */
    function scsl_judge($this_scsl, scsl) {
        $('.scsl').next().hide();
        var sl = $('#sl').val(); // 100
        var re = /^[0-9]+\.?[0-9]*$/;
        var two_re = /^0+\.?0*$/;
        var num = 0;
        if (re.test(sl)){
            if (two_re.test(sl)){
                return false;
            }else {
                $.each($('.scsl'), function (index, item) {
                    num += parseFloat(item.value);
                });
                if (re.test(scsl)){
                    if (two_re.test(scsl)){
                        $($this_scsl).next().text('格式不正确或没有正确输入数字!').show();
                        error_scsl = false;
                    }else {
                        if (num > parseFloat(sl)){
                            $($this_scsl).next().text('已超出生产数量总数').show();
                            error_scsl = false;
                        }else if (num < parseFloat(sl)){
                            $($this_scsl).next().text('已低于生产数量总数').show();
                            error_scsl = false;
                        }else {
                            $($this_scsl).next().hide();
                            error_scsl = true;
                        };
                    };
                }else {
                    $($this_scsl).next().text('格式不正确或没有正确输入数字!').show();
                    error_scsl = false;
                };
            };
        }else {
            return false;
        };
    };
    /*
        功能：删除选中的生产计划
     */
    function scjhb_delete() {
        var scjhb_spl = $('#proof').val();
        var answer = confirm('确定要删除吗?');
        if (answer){
            $.ajax({
                url:'/production/query_production7',
                data:{scjhb_spl: scjhb_spl},
                type:"get",
                success:function(data){
                    if (data.bool === 0){
                        alert('不允许删除');
                    }else{
                        location.href='/admin/bc_production/scjhb/';
                    };
                }
            });
        }
    };
});