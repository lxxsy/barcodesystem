
$(function () {
    var error_pbbh = true;
    var error_pbname = true;
    var error_scsx = true;
    var error_scxh = true;
    var error_plno = true;
    var error_ylid = true;
    var error_bzgl = true;
    var error_topz = true;
    var error_lowz = true;
    var error_jno = true;
    /*
        页面加载完毕触发ajax请求，获取所有的产品id，渲染到产品编号表单控件中，接着运行函数使计划副表产品与配方信息渲染出来
     */
    $.get('/formula/query_formula1', function (data) {
        $.each(JSON.parse(data.ylinfo) ,function (index, item) {
            $('#ylid').append('<option value='+item.pk+'>'+item.pk+'</option>');
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
        判断配方副表的序号是否合理
     */
    $('.tbody').on('blur', '.plno', function () {
        var $this_plno = $(this);
        var plno = $(this).val();
        plno_judge($this_plno, plno);
    });
    /*
        判断配方副表的原料代码是否合理
     */
    $('.tbody').on('blur', '.datas', function () {
        var $this_ylid = $(this);
        var ylid = $(this).val();
        ylid_judge($this_ylid, ylid);
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
    });
    /*
        点击副表删除按钮触发，搜寻此按钮的tr父级，然后删除
     */
    $('.tbody').on('click', '.f_delete', function () {
        $(this).parents('tr').remove();
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
        scsx_judge();
        $('.tbody tr').each(function () {
            var $this_plno = $(this).find('.plno');
            var $this_ylid = $(this).find('.datas');
            var $this_bzgl = $(this).find('.bzgl');
            var $this_topz = $(this).find('.topz');
            var $this_lowz = $(this).find('.lowz');
            var $this_jno = $(this).find('.jno');
            var plno = $(this).find('.plno').val();
            var ylid = $(this).find('.datas').val();
            var bzgl = $(this).find('.bzgl').val();
            var topz = $(this).find('.topz').val();
            var lowz = $(this).find('.lowz').val();
            var jno = $(this).find('.jno').val();
            plno_judge($this_plno, plno);
            if (error_plno === false){
                return false;
            };
            ylid_judge($this_ylid, ylid);
            if (error_ylid === false){
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
        if(error_pbbh === true && error_pbname === true && error_scsx === true && error_scxh === true &&
            error_plno === true && error_ylid === true && error_bzgl === true && error_topz === true &&
            error_lowz === true && error_jno === true){
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
        var re = /\W+/;
        if (pbbh.length===0){
            $('#pbbh').next().text('配方编号不能为空！').show();
            error_pbbh = false;
        }else{
            if (re.test(pbbh)){
                $('#pbbh').next().text('配方编号含有不允许符号!').show();
                error_pbbh = false;
            }else{
                $.get('/formula/query_formula2', {pbbh: pbbh}, function (data) {
                    if (data.bool === 0){
                        $('#pbbh').next().text('配方编号已存在!').show();
                        error_pbbh = false;
                    }else {
                        $('#pbbh').next().hide();
                        error_pbbh = true;
                    };
                });
            };
        };
    };
     /*
        功能： 判断配方名称的输入是否合理
     */
    function pbname_judge() {
        var pbname = $('#pbname').val();
        var re = /\s+|-+|\++|\?+/;
        if (pbname.length === 0){
            $('#pbname').next().text('配方名称不能为空!').show();
            error_pbname = false;
        }else if(re.test(pbname)){
            $('#pbname').next().text('配方名称含有不允许符号!').show();
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
        var re = /\.+/;
        if(scsx.length === 0){
            $('#scsx').next().text('请输入正确数字').show();
            error_scsx = false;
        }else if(scsx <= 0){
            $('#scsx').next().text('不能小于或等于0').show();
            error_scsx = false;
        }else if(re.test(scsx)){
            $('#scsx').next().text('不能为小数').show();
            error_scsx = false;
        }else {
            $('#scsx').next().hide();
            error_scsx = true;
        };
    };
    /*
        功能： 判断默认生产线的输入是否合理
     */
    function scxh_judge() {
        var scxh = $('#scxh').val();
        var re = /\.+/;
        if (scxh.length === 0){
            $('#scxh').next().text('请输入正确数字').show();
            error_scxh = false;
        }else if(scxh <= 0){
            $('#scxh').next().text('不能小于或等于0').show();
            error_scxh = false;
        }else if(re.test(scxh)){
            $('#scxh').next().text('不能为小数').show();
            error_scxh = false;
        }else {
            $('#scxh').next().hide();
            error_scxh = true;
        };
    };
    /*
        功能： 判断配方副表序号的输入是否合理
     */
    function plno_judge($this_plno, plno) {
        $('.plno').next().hide();
        var re = /\.+/;
        var judge = 0;
        $.each($('.plno').not($($this_plno)) ,function (index, item) {
            if (plno === item.value){
                $($this_plno).next().text('序号已存在').show();
                error_plno = false;
                judge = 1;
                return false;
            };
        });
        if (judge === 1){
            return false;
        };
        if (plno.length === 0){
            $($this_plno).next().text('请输入正确数字').show();
            error_plno = false;
        }else if(plno <= 0) {
            $($this_plno).next().text('不能小于或等于0').show();
            error_plno = false;
        }else {
            if (re.test(plno)){
                $($this_plno).next().text('不能为小数').show();
                error_plno = false;
            }else {
                $.ajax({
                    url:'/formula/query_formula3',
                    data:{"plno": plno},
                    type:"get",
                    traditional:true,
                    success:function(data){
                        if (data.plno_bool === 0){
                            $($this_plno).next().text('序号已存在').show();
                            error_plno = false;
                        }else {
                            $($this_plno).next().hide();
                            error_plno = true;
                        };
                    }
                });
            };
        };
    };
    /*
        功能： 判断配方副表原料代码的输入是否合理
     */
    function ylid_judge($this_ylid, ylid) {
        $('.datas').next().hide();
        var judge = 0;
        $.each($('.datas').not($($this_ylid)) ,function (index, item) {
            if (ylid === item.value){
                $($this_ylid).next().text('原料代码已存在').show();
                error_ylid = false;
                judge = 1;
                return false;
            };
        });
        if (judge === 1){
            return false;
        };
        if (ylid === ''){
            $($this_ylid).next().text('原料代码不能为空!').show();
            error_ylid = false;
        }else {
            $.get('/formula/query_formula4', {current_value: ylid}, function (data) {
                if (data.ylid_bool === 0){
                    $($this_ylid).next().text('没有此原料代码!').show();
                    error_ylid = false;
                }else {
                    $($this_ylid).next().hide();
                    error_ylid = true;
                };
            });
        };
    };
      /*
        功能： 判断配方副表的标准值输入是否合理
     */
    function bzgl_judge($this_bzgl, bzgl) {
        var re = /^\d+\.?\d+$/;
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
        var re = /^\d+\.?\d+$/;
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
        var re = /^\d+\.?\d+$/;
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
        $('.tbody').append('<tr>'+
                    '<td><input type="number" name="plno" class="plno"><span class="tips"></span></td>'+
                    '<td><input list="data" name="datas" class="form-control datas" autocomplete="off">' +
                        '<span class="tips"></span><datalist id="data"><select name="ylid" id="ylid"></select></datalist></td>'+
                    '<td><input type="text" name="bzgl" class="bzgl"><span class="tips"></span></td>'+
                    '<td><input type="text" name="topz" class="topz"><span class="tips"></span></td>'+
                    '<td><input type="text" name="lowz" class="lowz"><span class="tips"></span></td>'+
                    '<td><select class="form-control dw" name="dw"><option value="kg">kg</option><option value="g">g</option></select></td>'+
                    '<td><input type="number" name="jno" class="jno"><span class="tips"></span></td>'+
                    '<td><input type="checkbox" name="lt" checked="checked" class="lt" value="1"><input type="hidden" name="hlt" value="1" class="hlt"></td>'+
                    '<td><input type="checkbox" name="zs" checked="checked" class="zs" value="1"><input type="hidden" name="hzs" value="1" class="hzs"></td>'+
                    '<td><a href="javascript:;" class="glyphicon glyphicon-remove f_delete"></a></td>'+
                '</tr>');
    };
});
