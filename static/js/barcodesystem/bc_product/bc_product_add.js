
$(function () {
    var error_cpid = false;
    var error_cpmc = false;
    var error_dbz = false;
    var error_pbbh = false;
    var error_pbname = false;
    var error_cpsx = false;
    var error_cpxx = false;
    var error_zbq = false;
    var error_cppic = false;
    var error_cpsm = false;
    var error_tempname = false;
    /*
        页面加载完毕后，获取所有配方信息
     */
    $.get('/product/query_product1', function (data) {
        $.each(JSON.parse(data.pb_list), function (index, item) {
            $('#pbbh').append('<option value='+item.pk+'>'+item.pk+'</option>');
            $('#pbname').append('<option value='+item.fields.pbname+'>'+item.fields.pbname+'</option>');
        });
    });
    /*
        产品编号失去焦点后触发
     */
    $('#cpid').blur(function () {
        cpid_judge();
    });
    /*
        产品名称失去焦点后触发
     */
    $('#cpmc').blur(function () {
        cpmc_judge();
    });
    /*
        单包重失去焦点后触发
     */
    $('#dbz').blur(function () {
        dbz_judge();
    });
    /*
        配方编号失去焦点后触发
     */
    $('.data_cpml_pbbh').change(function () {
        data_cpml_pbbh_judge();
    });
    /*
        配方名称失去焦点后触发
     */
    $('.data_cpml_pbname').change(function () {
        data_cpml_pbname_judge();
    });
    /*
        包装上限失去焦点后触发
     */
    $('#cpsx').blur(function () {
        cpsx_judge();
    });
    /*
        包装下限失去焦点后触发
     */
    $('#cpxx').blur(function () {
        cpxx_judge();
    });
    /*
        保质期失去焦点后触发
     */
    $('#zbq').blur(function () {
        zbq_judge();
    });
    /*
        产品图片内容变化后触发
     */
    $('#cppic').change(function () {
        cppic_judge();
    });
    /*
        产品说明内容变化后触发
     */
    $('#cpsm').change(function () {
        cpsm_judge();
    });
    /*
        成品标签模板内容变化后触发
     */
    $('#tempname').change(function () {
        tempname_judge();
    });
    /*
        提交表单进行判断
     */
    $('#form_submit').submit(function () {
        cpid_judge();
        cpmc_judge();
        dbz_judge();
        submit_pbbh_judge();
        cpsx_judge();
        cpxx_judge();
        zbq_judge();
        cppic_judge();
        cpsm_judge();
        tempname_judge();
        if (error_cpid === true && error_cpmc === true && error_dbz === true && error_pbbh === true && error_pbname === true
            && error_cpsx === true && error_cpxx === true && error_zbq === true && error_cppic === true
            && error_cpsm === true && error_tempname === true){
            return true;
        }else{
            return false;
        };
    });
    /*
        功能： 判断产品编号的输入是否合理
     */
    function cpid_judge() {
        var cpid = $('#cpid').val();
        if (cpid.length===0){
            $('#cpid').next().text('产品编号不能为空!').show();
            error_cpid = false;
        }else{
            $.ajax({
                url:'/product/query_product2',
                data:{cpid: cpid},
                type:"get",
                async:false,
                success:function(data){
                    if (data.bool === 0){
                        $('#cpid').next().text('产品编号已存在!').show();
                        error_cpid = false;
                    }else {
                        $('#cpid').next().hide();
                        error_cpid = true;
                    };
                }
            });
        };
    };
    /*
        功能： 判断产品名称的输入是否合理
     */
    function cpmc_judge() {
        var cpmc = $('#cpmc').val();
        if (cpmc.length === 0){
            $('#cpmc').next().text('产品名称不能为空').show();
            error_cpmc = false;
        }else{
            $.ajax({
                url:'/product/query_product3',
                data:{cpmc: cpmc},
                type:"get",
                async:false,
                success:function(data){
                    if (data.bool === 0){
                        $('#cpmc').next().text('产品名称已存在!').show();
                        error_cpmc = false;
                    }else {
                        $('#cpmc').next().hide();
                        error_cpmc = true;
                    };
                }
            });
        };
    };
    /*
        功能： 判断单包重的输入是否合理
     */
    function dbz_judge() {
        var dbz = $('#dbz').val();
        var re = /^[0-9]+\.?[0-9]*$/;
        var two_re = /^0+\.?0*$/;
        if (dbz.length === 0){
            $('#dbz').next().hide();
            error_dbz = true;
        }else {
            if (re.test(dbz)){
                if (two_re.test(dbz)){
                    $('#dbz').next().text('格式不正确或没有正确输入数字!').show();
                    error_dbz = false;
                }else {
                    $('#dbz').next().hide();
                    error_dbz = true;
                };
            }else {
                $('#dbz').next().text('格式不正确或没有正确输入数字！').show();
                error_dbz = false;
            };
        };
    };
    /*
        功能：当提交表单时触发此函数判断原料代码，和输入框判断不同
     */
    function submit_pbbh_judge() {
        var pbbh = $('.data_cpml_pbbh').val();
        $.ajax({
            url:'/product/query_product4',
            data:{pbbh: pbbh},
            type:"get",
            async:false,
            success:function(data){
                if (data.pb_bool === 0){
                    $('.data_cpml_pbbh').next().text('配方不存在').show();
                    error_pbbh = false;
                    error_pbname = false;
                }else if (data.pb_bool === 2){
                    $('.data_cpml_pbbh').next().text('配方以使用').show();
                    error_pbbh = false;
                    error_pbname = false;
                }else {
                    $('.data_cpml_pbbh').next().hide();
                    error_pbbh = true;
                    error_pbname = true;
                };
            }
        });
    };
    /*
        功能: 当用户点击输入框选择配方编号时触发此函数，提交表单时不会触发此函数
     */
    function data_cpml_pbbh_judge() {
        $('.data_cpml_pbbh').next().hide();
        $('.data_cpml_pbname').next().hide();
        var pbbh = $('.data_cpml_pbbh').val();
        $.ajax({
            url:'/product/query_product4',
            data:{pbbh: pbbh},
            type:"get",
            async:false,
            success:function(data){
                $('.data_cpml_pbname').val(data.pbname);
                if (data.pb_bool === 0){
                    $('.data_cpml_pbbh').next().text('配方不存在').show();
                    error_pbbh = false;
                }else if (data.pb_bool === 2){
                    $('.data_cpml_pbbh').next().text('配方已使用').show();
                    error_pbbh = false;
                }else {
                    $('.data_cpml_pbbh').next().hide();
                    error_pbbh = true;
                };
            }
        });
    };
     /*
        功能: 当用户点击输入框选择配方名称时触发此函数，提交表单时不会触发此函数
     */
    function data_cpml_pbname_judge() {
        $('.data_cpml_pbbh').next().hide();
        $('.data_cpml_pbname').next().hide();
        var pbname = $('.data_cpml_pbname').val();
        $.ajax({
            url:'/product/query_product5',
            data:{pbname: pbname},
            type:"get",
            async:false,
            success:function(data){
                $('.data_cpml_pbbh').val(data.pbbh);
                if (data.pb_bool === 0){
                    $('.data_cpml_pbname').next().text('配方不存在').show();
                    error_pbname = false;
                }else if (data.pb_bool === 2){
                    $('.data_cpml_pbname').next().text('配方以使用').show();
                    error_pbname = false;
                }else {
                    $('.data_cpml_pbname').next().hide();
                    error_pbname = true;
                };
            }
        });
    };
    /*
        功能： 判断包装上限的输入是否合理
     */
    function cpsx_judge() {
        var cpsx = $('#cpsx').val();
        var re = /^[0-9]+\.?[0-9]*$/;
        var two_re = /^0+\.?0*$/;
        if (cpsx.length === 0){
            $('#cpsx').next().hide();
            error_cpsx = true;
        }else {
            if (re.test(cpsx)){
                if (two_re.test(cpsx)){
                    $('#cpsx').next().text('格式不正确或没有正确输入数字!').show();
                    error_cpsx = false;
                }else {
                    $('#cpsx').next().hide();
                    error_cpsx = true;
                };
            }else {
                $('#cpsx').next().text('格式不正确或没有正确输入数字！').show();
                error_cpsx = false;
            };
        };
    };
      /*
        功能： 判断包装下限的输入是否合理
     */
    function cpxx_judge() {
        var cpxx = $('#cpxx').val();
        var re = /^[0-9]+\.?[0-9]*$/;
        var two_re = /^0+\.?0*$/;
        if (cpxx.length === 0){
            $('#cpxx').next().hide();
            error_cpxx = true;
        }else {
            if (re.test(cpxx)){
                if (two_re.test(cpxx)){
                    $('#cpxx').next().text('格式不正确或没有正确输入数字!').show();
                    error_cpxx = false;
                }else {
                    $('#cpxx').next().hide();
                    error_cpxx = true;
                };
            }else {
                $('#cpxx').next().text('格式不正确或没有正确输入数字！').show();
                error_cpxx = false;
            };
        };
    };
     /*
        功能： 判断保质期的输入是否合理
     */
    function zbq_judge() {
        var zbq = $('#zbq').val();
        var re = /^[1-9][0-9]{1,2}$/;
        if (zbq.length === 0){
            $('#zbq').next().hide();
            error_zbq = true;
        }else {
            if (re.test(zbq)){
                $('#zbq').next().hide();
                error_zbq = true;
            }else {
                $('#zbq').next().text('格式不正确或没有正确输入整数!').show();
                error_zbq = false;
            };
        };
    };
    /*
        功能： 判断产品图片的输入是否合理
     */
    function cppic_judge() {
        if ($('#cppic').val() === ''){
            // $('#cppic').next().text('产品图片不能为空').show();
            $('#cppic').next().hide();
            error_cppic = true;
        }else{
            var cppic_dict = document.getElementById('cppic').files[0];
            var cppic_name = cppic_dict.name.toLowerCase().split('.');
            var cppic_type = cppic_name[cppic_name.length-1];
            var cppic_size = cppic_dict.size;
            if (cppic_type != 'png' && cppic_type != 'jpg' && cppic_type != 'gif') {
                $('#cppic').next().text('请上传一个二进制文件').show();
                error_cppic = false;
            }else if (cppic_size > 5000000){
                $('#cppic').next().text('请上传不超过5M大小的图片').show();
                error_cppic = false;
            }else{
                $('#cppic').next().hide();
                error_cppic = true;
            };
        };
    };
    /*
        功能： 判断产品说明的输入是否合理
     */
    function cpsm_judge() {
        if ($('#cpsm').val() === ''){
            // $('#cpsm').next().text('产品说明文件不能为空').show();
            $('#cpsm').next().hide();
            error_cpsm = true;
        }else{
            console.log(document.getElementById('cpsm'));
            var cpsm_dict = document.getElementById('cpsm').files[0];
            console.log(cpsm_dict);
            var cpsm_name = cpsm_dict.name.toLowerCase().split('.');
            console.log(cpsm_name);
            var cpsm_type = cpsm_name[cpsm_name.length-1];
            console.log(cpsm_type);
            var cpsm_size = cpsm_dict.size;
            console.log(cpsm_size);
            if (cpsm_type === 'png' || cpsm_type === 'jpg' || cpsm_type === 'gif') {
                $('#cpsm').next().text('请上传文本文件').show();
                error_cpsm = false;
            }else if (cpsm_size > 5000000){
                $('#cpsm').next().text('请上传不超过5M大小的文件').show();
                error_cpsm = false;
            }else{
                $('#cpsm').next().hide();
                error_cpsm = true;
            };
        };
    };
    /*
        功能： 判断成品模板的输入是否合理
     */
    function tempname_judge() {
        if ($('#tempname').val() === ''){
            $('#tempname').next().text('成品标签文件不能为空').show();
            error_tempname = false;
        }else{
            var tempname_dict = document.getElementById('tempname').files[0];
            var tempname_name = tempname_dict.name.toLowerCase().split('.');
            var tempname_type = tempname_name[tempname_name.length-1];
            var tempname_size = tempname_dict.size;
            console.log(tempname_dict.name);
            if (tempname_type === 'png' || tempname_type === 'jpg' || tempname_type === 'gif') {
                // $('#tempname').next().text('文件格式必须是htm,html,xml的一种').show();
                $('#tempname').next().text('请上传一个文本文件').show();
                error_tempname = false;
            }else if (tempname_size > 5000000){
                $('#tempname').next().text('请上传不超过5M的文件').show();
                error_tempname = false;
            }else{
                $('#tempname').next().hide();
                error_tempname = true;
            };
        };
    };
});
/*
    function gg_judge() {
        var gg = $('#gg').val();
        if (gg.length === 0){
            $('#gg').next().text('产品规格不能为空!').show();
            error_gg = false;
        }else {
            $('#gg').next().hide();
            error_gg = true;
        };
    };
 */