
$(function () {
    var error_pbbh = false;
    var error_pbname = false;
    var error_scsx = false;
    var error_scxh = false;
    var error_ylid = false;
    var error_ylname = false;
    var error_bzgl = false;
    var error_topz = false;
    var error_lowz = false;
    var error_jno = false;
    var plno_num = 0;  // 此值为配方明细序号字段的值，默认为0，页面加载完毕后动态获取最大序号值赋值给此变量
    var pb_bh = $('#pb_bh').val(); // 如果是点击修改页面，val值会存在
    if (pb_bh){
        $.ajax({
            url:'/formula/update_formula',
            data:{"pb_bh":pb_bh},
            type:"get",
            async:false,
            success:function(data){
                template.defaults.imports.dateFormat = function(date, format){
                    return date;
                };
                $('#form_submit').html(template('pb', {pbbh: data.pbbh, pbname: data.pbname, pftype: data.pftype,
                    scsx: data.scsx, scxh: data.scxh, yx: data.yx, bz: data.bz, pbf_list: JSON.parse(data.pbf_list)}));
            }
        });
    };
    /*
        页面加载完毕后，判断配方明细副表的行数，如果只有一行那么就不提供删除副表行数功能
     */
    if ($('.f_delete').length === 1){
        $('.f_delete').hide();
    };
    /*
        页面加载完毕后，获取配方明细序号的最大值,plno_num默认值为0
     */
    $('.bodytr').each(function () {
        plno_num = parseInt($(this).find('.plno').val());
    });
    /*
        页面加载完毕触发ajax请求，获取所有的原料id，渲染到原料代码表单控件中
     */
    $.get('/formula/query_formula1', function (data) {
        $.each(JSON.parse(data.ylinfo) ,function (index, item) {
            $('#ylid').append('<option value='+item.pk+'>'+item.pk+'</option>');
            $('#ylname').append('<option value='+item.fields.ylname+'>'+item.fields.ylname+'</option>');
        });
    });
    /*
        配方编号失去焦点触发，判断输入的值是否合理
     */
    $('#pbbh').blur(function () {
        pbbh_judge();
    });
    /*
        配方名称失去焦点触发，判断输入的值是否合理
     */
    $('#pbname').blur(function () {
        pbname_judge();
    });
    /*
        生产顺序失去焦点触发，判断输入的值是否合理
     */
    $('#scsx').blur(function () {
        scsx_judge();
    });
    /*
        默认生产线失去焦点触发，判断输入的值是否合理
     */
    $('#scxh').blur(function () {
        scxh_judge();
    });
    /*
        判断配方副表的原料代码是否合理
     */
    $('.tbody').on('change', '.datas', function () {
        var $this_ylid = $(this);
        var ylid = $(this).val();
        ylid_judge($this_ylid, ylid);
    });
    /*
        判断配方副表的原料名称是否合理
     */
    $('.tbody').on('change', '.data_name', function () {
        var $this_ylname = $(this);
        var ylname = $(this).val();
        ylname_judge($this_ylname, ylname);
    });
    /*
        判断配方副表的标准值是否合理
     */
    $('.tbody').on('blur', '.bzgl', function () {
        var $this_bzgl = $(this);
        var bzgl = $(this).val();
        bzgl_judge($this_bzgl, bzgl);
    });
    /*
        判断配方副表的上限是否合理
     */
    $('.tbody').on('blur', '.topz', function () {
        var $this_topz = $(this);
        var topz = $(this).val();
        topz_judge($this_topz, topz);
    });
    /*
        判断配方副表的下限是否合理
     */
    $('.tbody').on('blur', '.lowz', function () {
        var $this_lowz = $(this);
        var lowz = $(this).val();
        lowz_judge($this_lowz, lowz);
    });
    /*
        判断配方副表的投料顺序是否合理
     */
    $('.tbody').on('blur', '.jno', function () {
        var $this_jno = $(this);
        var jno = $(this).val();
        jno_judge($this_jno, jno);
    });
    /*
        点击增加配方明细副表时触发，追加一行表格
     */
    $('.add-detailed').click(function () {
        tbody_append();
        $('.f_delete').show();
    });
    /*
        点击副表删除按钮触发，搜寻此按钮的tr父级，然后删除
     */
    $('.tbody').on('click', '.f_delete', function () {
        $(this).parents('tr').remove();
        plno_num -= 1;
        $('.bodytr').each(function () {
            $(this).find('.plno').val($(this).index()+1);
        });
        if ($('.f_delete').length === 1){
            $('.f_delete').hide();
        };
    });
    /*
        点击副表称零头或追溯时触发，判断是否选中此框
     */
    $('.tbody').on('click', '.lt, .zs', function () {
        if ($(this).prop('checked')){
            $(this).next().val('1');
        }else {
            $(this).next().val('0');
        };
    });
    /*
        提交表单触发，判断表单内容是否合理，合理提交到后台
     */
    $('#form_submit').submit(function () {
        pbbh_judge();
        pbname_judge();
        scsx_judge();
        scxh_judge();
        $('.tbody tr').each(function () {
            var $this_ylid = $(this).find('.datas');
            var $this_ylname = $(this).find('.data_name');
            var $this_bzgl = $(this).find('.bzgl');
            var $this_topz = $(this).find('.topz');
            var $this_lowz = $(this).find('.lowz');
            var $this_jno = $(this).find('.jno');
            var ylid = $(this).find('.datas').val();
            var ylname = $(this).find('.data_name').val();
            var bzgl = $(this).find('.bzgl').val();
            var topz = $(this).find('.topz').val();
            var lowz = $(this).find('.lowz').val();
            var jno = $(this).find('.jno').val();
            if ($(this).find('.lt').prop('checked')){
                $(this).find('.hlt').val('1');
            }else {
                $(this).find('.hlt').val('0');
            };
            if ($(this).find('.zs').prop('checked')){
                $(this).find('.hzs').val('1');
            }else {
                $(this).find('.hzs').val('0');
            };
            ylid_judge($this_ylid, ylid);
            if (error_ylid === false){
                return false;
            };
            ylname_judge($this_ylname, ylname);
            if (error_ylname === false){
                return false;
            };
            bzgl_judge($this_bzgl, bzgl);
            if (error_bzgl === false){
                return false;
            };
            topz_judge($this_topz, topz);
            if (error_topz === false){
                return false;
            };
            lowz_judge($this_lowz, lowz);
            if (error_lowz === false){
                return false;
            };
            jno_judge($this_jno, jno);
            if (error_jno === false){
                return false;
            };
        });
        console.log('a');
        if (parseInt($('#pftype').val()) === 2){
            var num = 0;
            $.each($('.bzgl'), function (index, item) {
                num += parseFloat(item.value);
            });
            if (num != parseFloat(100)){
                alert('配方明细比例不满足100%');
                return false;
            };
        };
        if(error_pbbh === true && error_pbname === true && error_scsx === true && error_scxh === true &&
            error_ylid === true && error_ylname === true && error_bzgl === true &&
            error_topz === true && error_lowz === true && error_jno === true){
            return true;
        }else {
            return false;
        };
    });
    /*
        功能： 判断配方编号的输入是否合理
     */
    function pbbh_judge() {
        var pbbh = $('#pbbh').val();
        // var re = /\W+/;
        if (pbbh.length===0){
            $('#pbbh').next().text('配方编号不能为空！').show();
            error_pbbh = false;
        }else{
            $.ajax({
                url:'/formula/query_formula2',
                data:{Original: pb_bh, pbbh: pbbh},
                type:"get",
                async:false,
                success:function(data){
                    if (data.bool === 0){
                        $('#pbbh').next().text('配方编号已存在!').show();
                        error_pbbh = false;
                    }else {
                        $('#pbbh').next().hide();
                        error_pbbh = true;
                    };
                }
            });
        };
    };
     /*
        功能： 判断配方名称的输入是否合理
     */
    function pbname_judge() {
        var pbname = $('#pbname').val();
        //var re = /\s+|-+|\++|\?+/;
        if (pbname.length === 0){
            $('#pbname').next().text('配方名称不能为空!').show();
            error_pbname = false;
        }else {
            $('#pbname').next().hide();
            error_pbname = true;
        };
    };
    /*
        功能： 判断生产顺序的输入是否合理
     */
    function scsx_judge() {
        var scsx = $('#scsx').val();
        var re = /^[1-9][0-9]?$/;
        if (re.test(scsx)){
            $('#scsx').next().hide();
            error_scsx = true;
        }else {
            $('#scsx').next().text('格式不正确或没有正确输入整数!').show();
            error_scsx = false;
        };
    };
    /*
        功能： 判断默认生产线的输入是否合理
     */
    function scxh_judge() {
        var scxh = $('#scxh').val();
        var re = /^[1-9][0-9]?$/;
        if (re.test(scxh)){
            $('#scxh').next().hide();
            error_scxh = true;
        }else {
            $('#scxh').next().text('格式不正确或没有正确输入整数!').show();
            error_scxh = false;
        };
    };
   /*
        功能： 判断配方副表原料代码的输入是否合理
     */
    function ylid_judge($this_ylid, ylid) {
        $('.datas').next().hide();
        $('.data_name').next().hide();
        $.ajax({
            url:'/formula/query_formula4',
            data:{current_value: ylid},
            type:"get",
            async:false,
            success:function(data){
                $($this_ylid).parent().next().find('input').val(data.ylname);
                if (data.ylid_bool === 0){
                    $($this_ylid).next().text('没有此原料!').show();
                    error_ylid = false;
                }else {
                    $.each($('.datas').not($($this_ylid)) ,function (index, item) {
                        if (ylid === item.value){
                            $($this_ylid).next().text('原料已存在').show();
                            error_ylid = false;
                            return false;
                        }else{
                            error_ylid = true;
                        };
                    });
                };
            }
        });
    };
    /*
        功能： 判断配方副表原料代码的输入是否合理
     */
    function ylname_judge($this_ylname, ylname) {
        $('.datas').next().hide();
        $('.data_name').next().hide();
        $.ajax({
            url:'/formula/query_formula5',
            data:{current_value: ylname},
            type:"get",
            async:false,
            success:function(data){
                $($this_ylname).parent().prev().find('input').val(data.ylid);
                if (data.ylname_bool === 0){
                    $($this_ylname).next().text('没有此原料!').show();
                    error_ylname = false;
                }else {
                    $.each($('.data_name').not($($this_ylname)) ,function (index, item) {
                        if (ylname === item.value){
                            $($this_ylname).next().text('原料已存在').show();
                            error_ylname = false;
                            return false;
                        }else{
                            error_ylname = true;
                        };
                    });
                };
            }
        });
    };
    /*
        功能： 判断配方副表的标准值输入是否合理
     */
    function bzgl_judge($this_bzgl, bzgl) {
        $($this_bzgl).parent('td').siblings().eq(3).find('span').hide();
        $($this_bzgl).parent('td').siblings().eq(4).find('span').hide();
        var re = /^\d+\.?\d*$/;
        var topz = $($this_bzgl).parent('td').siblings().eq(3).find('input').val();
        var lowz = $($this_bzgl).parent('td').siblings().eq(4).find('input').val();
        if (topz != ''){
            if (bzgl > topz){
                $($this_bzgl).next().text('不能大于上限').show();
                error_bzgl = false;
                return false;
            };
        };
        if (lowz != ''){
            if (bzgl < lowz){
                $($this_bzgl).next().text('不能小于下限').show();
                error_bzgl = false;
                return false;
            };
        };
        if (re.test(bzgl)){
            $($this_bzgl).next().hide();
            error_bzgl = true;
        }else{
            $($this_bzgl).next().text('请输入正确数字').show();
            error_bzgl = false;
        };
    };
    /*
        功能： 判断配方副表的上限输入是否合理
     */
    function topz_judge($this_topz, topz) {
        $($this_topz).parent('td').siblings().eq(3).find('span').hide();
        var re = /^\d+\.?\d*$/;
        var bzgl = $($this_topz).parent('td').siblings().eq(3).find('input').val();
        if (bzgl != ''){
            if (topz < bzgl){
                $($this_topz).next().text('不能小于标准值').show();
                error_topz = false;
                return false;
            };
        };
        if (re.test(topz)){
            $($this_topz).next().hide();
            error_topz = true;
        }else{
            $($this_topz).next().text('请输入正确数字').show();
            error_topz = false;
        };
    };
    /*
        功能： 判断配方副表的下限输入是否合理
     */
    function lowz_judge($this_lowz, lowz) {
        $($this_lowz).parent('td').siblings().eq(3).find('span').hide();
        var re = /^\d+\.?\d*$/;
        var bzgl = $($this_lowz).parent('td').siblings().eq(3).find('input').val();
        if (bzgl != ''){
            if (lowz > bzgl){
                $($this_lowz).next().text('不能大于标准值').show();
                error_lowz = false;
                return false;
            };
        };
        if (re.test(lowz)){
            $($this_lowz).next().hide();
            error_lowz = true;
        }else{
            $($this_lowz).next().text('请输入正确数字').show();
            error_lowz = false;
        };
    };
    /*
        功能： 判断配方副表的投料顺序输入是否合理
     */
    function jno_judge($this_jno, jno) {
        $('.jno').next().hide();
        var re = /\.+/;
        var judge = 0;
        $.each($('.jno').not($($this_jno)) ,function (index, item) {
            if (jno === item.value){
                $($this_jno).next().text('顺序号已存在').show();
                error_jno = false;
                judge = 1;
                return false;
            };
        });
        if (judge === 1){
            return false;
        };
        if(jno.length === 0){
            $($this_jno).next().text('请输入正确数字').show();
            error_jno = false;
        }else if(jno <= 0){
            $($this_jno).next().text('不能小于或等于0').show();
            error_jno = false;
        }else if(re.test(jno)){
            $($this_jno).next().text('不能为小数').show();
            error_jno = false;
        }else {
            $($this_jno).next().hide();
            error_jno = true;
        };
    };
    /*
        增加配方明细
     */
    function tbody_append(){
        plno_num += 1;
        $('.tbody').append('<tr class="bodytr">'+
                    '<td><input type="text" name="plno" class="plno" value='+plno_num+' readonly><span class="tips"></span></td>'+
                    '<td><input list="data" name="datas" class="form-control datas" autocomplete="off" value="">' +
                        '<span class="tips"></span><datalist id="data"><select name="ylid" id="ylid"></select></datalist></td>'+
                    '<td><input list="data_name" name="data_name" class="form-control data_name" autocomplete="off" value="">' +
                        '<span class="tips"></span><datalist id="data_name"><select name="ylname" id="ylname"></select></datalist></td>'+
                    '<td><input type="text" name="bzgl" class="bzgl"><span class="tips"></span></td>'+
                    '<td><input type="text" name="topz" class="topz"><span class="tips"></span></td>'+
                    '<td><input type="text" name="lowz" class="lowz"><span class="tips"></span></td>'+
                    '<td><select class="form-control dw" name="dw"><option value="1">kg</option><option value="2">g</option></select></td>'+
                    '<td><input type="number" name="jno" class="jno"><span class="tips"></span></td>'+
                    '<td><input type="checkbox" name="lt" checked="checked" class="lt" value="1"><input type="hidden" name="hlt" value="1" class="hlt"></td>'+
                    '<td><input type="checkbox" name="zs" checked="checked" class="zs" value="1"><input type="hidden" name="hzs" value="1" class="hzs"></td>'+
                    '<td><a href="javascript:;" class="glyphicon glyphicon-remove f_delete"></a></td>'+
                '</tr>');
    };
});