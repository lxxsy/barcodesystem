
$(function () {
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
});