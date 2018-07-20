/**
 * Created by LILI on 2018/7/10.
 */


$(function () {
    $('.add-detailed').click(function () {
        var number = $('.tbody').children('tr').length;  // 把类为.tbody的元素下的tr子元素的数量统计出来
        alert(number);
        location.href = '/production/detailed_list?number='+number; // 然后发送一个请求并附带一个a参数，目的是上后台知道tr的元素个数
    });
});
