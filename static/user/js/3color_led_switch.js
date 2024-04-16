$(function () {
    $('.rgb-3color-led-switch').bootstrapSwitch();
    // 스위치 상태 변경 이벤트 핸들러 등록
    $('.rgb-3color-led-switch').on('switchChange.bootstrapSwitch', function (event, state) {
        if (state) {
            console.log("스위치가 ON 상태입니다.");
            // 스위치가 켜진 상태일 때 수행할 작업
            socket.emit('set_3color_led', {'data':'on'});
        } else {
            console.log("스위치가 OFF 상태입니다.");
            // 스위치가 꺼진 상태일 때 수행할 작업
            socket.emit('set_3color_led', {'data':'off'});
        }
    });
    socket.emit('get_3color_led', {});
    socket.on('ret_3color_led', function(data) {
        console.log("스위치 상태", data);
        if (data.state) {
            $('.rgb-3color-led-switch').bootstrapSwitch('state', true, true);  // 스위치를 ON 상태로 설정
        } else {
            $('.rgb-3color-led-switch').bootstrapSwitch('state', false, true); // 스위치를 OFF 상태로 설정
        }
    });    
});