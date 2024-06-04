from common import response_html
async def mainHandle(request):
    return response_html('index.html')

async def loginHandle(request):
    print("로그인 핸들러 호출됨")
    return response_html('login.html')

async def inventory_chart_Handle(request):
    return response_html('inventory_chart.html')

async def temp_Handle(request):
    return response_html('temp.html')

async def rt_inventory_status_Handle(request):
    return response_html('rt_inventory_status.html')
