$(function () {
    var error_gyscode = false;
    var error_gysname = false;
    var error_tel = false;
    var error_email = false;
    var error_web = false;
    /*
        获取要修改的原料id，请求视图加载模板并渲染数据
     */
    var gys_id = $('#gys_id').val();
    $.ajax({
        url:'/rmaterial/update_gys',
        data:{"gys_id":gys_id},
        type:"get",
        async:false,
        success:function(data){
            if (data.bool === 1){
                $('#form_submit').html(template('gys', {gyscode: data.gyscode, gysname: data.gysname, addr: data.addr,
                    tel: data.tel, fax: data.fax, men: data.men, email: data.email, web: data.web,
                    bz: data.bz, scdz: data.scdz, yyzzbh: data.yyzzbh}));
            }else {
                alert('异常');
            };
        }
    });
    /*
        获取页面上的供应商ID与供应商名称，称为原内容。目的是修改以后会拿原内容与新内容做比较，如果新内容和原内容相同则表示没有做修改
      */
    var Original = $('#gyscode').val();
    var Original_name = $('#gysname').val();
    /*
        供应商代码失去焦点后触发
     */
    $('#gyscode').blur(function () {
        gyscode_judge();
    });
    /*
        供应商名称失去焦点后触发
     */
    $('#gysname').blur(function () {
        gysname_judge();
    });
    /*
        电话失去焦点后触发
     */
    $('#tel').blur(function () {
        tel_judge();
    });
    /*
        邮箱失去焦点后触发
     */
    $('#email').blur(function () {
        email_judge();
    });
    /*
        网址失去焦点后触发
     */
    $('#web').blur(function () {
        web_judge();
    });
    /*
        提交表单后触发
     */
    $('#form_submit').submit(function () {
        gyscode_judge();
        if (error_gyscode === false){
            return false;
        };
        gysname_judge();
        if (error_gysname === false){
            return false;
        };
        tel_judge();
        email_judge();
        web_judge();
        if (error_gyscode === true && error_gysname === true && error_tel === true && error_email === true &&
            error_web === true)
        {
            return true
        }else{
            return false
        };
    });
    /*
        功能: 判断供应商代码
     */
    function gyscode_judge() {
        var gyscode = $('#gyscode').val();
        if (gyscode.length === 0){
            $('#gyscode').next().text('不能为空').show();
            error_gyscode = false;
        }else{
            $.ajax({
                url:'/rmaterial/query_gys1',
                data:{gyscode: gyscode, Original: Original},
                type:"get",
                async:false,
                success:function(data){
                    if (data.bool === 0){
                        $('#gyscode').next().text('供应商代码已存在!').show();
                        error_gyscode = false;
                    }else {
                        $('#gyscode').next().hide();
                        error_gyscode = true;
                    };
                }
            });
        }
    };
    /*
        功能: 判断供应商名称
     */
    function gysname_judge() {
        var gysname = $('#gysname').val();
        if (gysname.length === 0){
            $('#gysname').next().text('不能为空').show();
            error_gysname = false;
        }else{
            $.ajax({
                url:'/rmaterial/query_gys2',
                data:{gysname: gysname, Original_name: Original_name},
                type:"get",
                async:false,
                success:function(data){
                    if (data.bool === 0){
                        $('#gysname').next().text('供应商名称已存在!').show();
                        error_gysname = false;
                    }else {
                        $('#gysname').next().hide();
                        error_gysname = true;
                    };
                }
            });
        }
    };
    /*
        功能: 判断电话输入是否合理
     */
    function tel_judge() {
        var tel = $('#tel').val();
        var re = /^1[345789]\d{9}$/;
        if (tel.length === 0){
            $('#tel').next().hide();
            error_tel = true;
            return false;
        };
        if (re.test(tel)){
            $('#tel').next().hide();
            error_tel = true;
        }else{
            $('#tel').next().text('手机号码有误，请重填').show();
            error_tel = false;
        };
    };
    /*
        功能: 判断邮箱输入是否合理
     */
    function email_judge() {
        var email = $('#email').val();
        var re = /^[a-z0-9][\w\.-]*@[\w\-]+(\.[a-z]{2,5}){1}$/i;
        if (email.length === 0){
            $('#email').next().hide();
            error_email = true;
            return false;
        };
        if (re.test(email)){
            $('#email').next().hide();
            error_email = true;
        }else{
            $('#email').next().text('你输入的邮箱格式不正确').show();
            error_email = false;
        };
    };
    /*
        功能: 判断网址输入是否合理
     */
    function web_judge() {
        var web = $('#web').val();
        var re = /^(https?|ftp|file):\/\/[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]$/;
        if (web.length === 0){
            $('#web').next().hide();
            error_web = true;
            return false;
        };
        if (re.test(web)){
            $('#web').next().hide();
            error_web = true;
        }else{
            $('#web').next().text('你输入的网址格式不正确').show();
            error_web = false;
        };
    };
});