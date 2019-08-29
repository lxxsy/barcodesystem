
$(function () {
    /*
        点击库存查询时，触发
     */
    $('#stock_query').click(function () {
        $('#stockinfo_ul').empty();
        $('#stock_tbody').empty();
        $.get('/rmaterial/query_stock1', function (data) {
            $.each(JSON.parse(data.stockinfo_list) ,function (index, item) {
                if (index === 0){
                    $('#stockinfo_ul').append('<li class="stockinfo_ul_display"><a href="javascript:;"><i class="glyphicon glyphicon-triangle-right"></i>'+item.fields.stockname+'</a></li>');
                }else{
                    $('#stockinfo_ul').append('<li class=""><a href="javascript:;"><i class="glyphicon glyphicon-triangle-right"></i>'+item.fields.stockname+'</a></li>');
                };
            });
            $.each(JSON.parse(data.stock_list) ,function (index, item) {
                $('#stock_tbody').append('<tr><td class="tbody-td">'+item.fields.ylid+'</td>' +
                    '<td class="tbody-td">'+item.fields.ylname+'</td>' +
                    '<td class="tbody-td">'+item.fields.quantity+'</td>' +
                    '<td class="tbody-td">'+item.fields.qcsl+'</td>' +
                    '<td class="tbody-td">'+item.fields.qa_hg+'</td></tr>');
            });
        });
        $('#changelist-form').remove();
        $('#pagination').remove();
        $('#stockinfo_div').css('display', 'block');
        $('#stock_div').css('display', 'inline-block');
    });
    /*
        点击库存查询中具体的仓库名字时触发
     */
    $('#stockinfo_ul').delegate('a', 'click', function () {
        $('#stock_tbody').empty();
        $(this).parent().addClass('stockinfo_ul_display').siblings().removeClass('stockinfo_ul_display');
        var stockinfo_name = $(this).text();
        $.get('/rmaterial/query_stock2', {stockinfo_name: stockinfo_name}, function (data) {
            $.each(JSON.parse(data.stock_list) ,function (index, item) {
                $('#stock_tbody').append('<tr><td class="tbody-td">'+item.fields.ylid+'</td>' +
                    '<td class="tbody-td">'+item.fields.ylname+'</td>' +
                    '<td class="tbody-td">'+item.fields.quantity+'</td>' +
                    '<td class="tbody-td">'+item.fields.qcsl+'</td>' +
                    '<td class="tbody-td">'+item.fields.qa_hg+'</td></tr>');
            });
        });
    });
});