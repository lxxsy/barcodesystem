/**
 * Created by LILI on 2018/7/10.
 */


$(function () {
    $.get('/production/select_product1', function (data) {
        $.each(JSON.parse(data.cpml_list) ,function (index, item) {
            $('#cpid').append('<option>'+item.pk+'</option>')
        });
        select_product();
    });
    function select_product() {
        var cpid = $('#cpid').val();
        $.get('/production/select_product2', {cpid: cpid}, function (data) {
            if (data.product_null){
                alert('Not found');
            }
            $('.cpbh').val(data.cpbh);
            $('.cpmc').val(data.cpmc);
            $('.pfbh').val(data.pfbh);
            $('.pfmc').val(data.pfmc);
        });
    };
});
