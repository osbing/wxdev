# -*- coding:utf-8-*-
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from django.http import HttpResponse
from wechatpy import WeChatClient
from django.views.decorators.csrf import csrf_exempt

token = 'helloworld'

@csrf_exempt # 关闭csrf验证，允许跨域访问
def handle_wx(request):
    if request.method == 'GET':
        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echo_str = request.GET.get('echostr', '')
        try:
            check_signature(token, signature, timestamp, nonce)
        except InvalidSignatureException:
            echo_str = '错误的请求'
        response = HttpResponse(echo_str)
        return response

#自定义菜单的创建接口
# 1、自定义菜单最多包括3个一级菜单，每个一级菜单最多包含5个二级菜单。 3*5=15
# 2、一级菜单最多4个汉字，二级菜单最多7个汉字，多出来的部分将会以“...”代替。
# 3、创建自定义菜单后，菜单的刷新策略是，在用户进入公众号会话页或公众号profile页时，如果发现上一次拉取菜单的请求在5分钟以前，就会拉取一下菜单，如果菜单有更新，就会刷新客户端的菜单。测试时可以尝试取消关注公众账号后再次关注，则可以看到创建后的效果。


# 可实现多种类型按钮
# 事件 click view scancode_push scancode_waitmsg pic_sysphoto pic_photo_or_album pic_weixin location_select media_id view_limited
# media_id view_limited
# 1、click：点击推事件用户点击click类型按钮后，微信服务器会通过消息接口推送消息类型为event的结构给开发者（参考消息接口指南），并且带上按钮中开发者填写的key值，开发者可以通过自定义的key值与用户进行交互；
# 2、view：跳转URL用户点击view类型按钮后，微信客户端将会打开开发者在按钮中填写的网页URL，可与网页授权获取用户基本信息接口结合，获得用户基本信息。
# 3、scancode_push：扫码推事件用户点击按钮后，微信客户端将调起扫一扫工具，完成扫码操作后显示扫描结果（如果是URL，将进入URL），且会将扫码的结果传给开发者，开发者可以下发消息。
# 4、scancode_waitmsg：扫码推事件且弹出“消息接收中”提示框用户点击按钮后，微信客户端将调起扫一扫工具，完成扫码操作后，将扫码的结果传给开发者，同时收起扫一扫工具，然后弹出“消息接收中”提示框，随后可能会收到开发者下发的消息。
# 5、pic_sysphoto：弹出系统拍照发图用户点击按钮后，微信客户端将调起系统相机，完成拍照操作后，会将拍摄的相片发送给开发者，并推送事件给开发者，同时收起系统相机，随后可能会收到开发者下发的消息。
# 6、pic_photo_or_album：弹出拍照或者相册发图用户点击按钮后，微信客户端将弹出选择器供用户选择“拍照”或者“从手机相册选择”。用户选择后即走其他两种流程。
# 7、pic_weixin：弹出微信相册发图器用户点击按钮后，微信客户端将调起微信相册，完成选择操作后，将选择的相片发送给开发者的服务器，并推送事件给开发者，同时收起相册，随后可能会收到开发者下发的消息。
# 8、location_select：弹出地理位置选择器用户点击按钮后，微信客户端将调起地理位置选择工具，完成选择操作后，将选择的地理位置发送给开发者的服务器，同时收起位置选择工具，随后可能会收到开发者下发的消息。
# 9、media_id：下发消息（除文本消息）用户点击media_id类型按钮后，微信服务器会将开发者填写的永久素材id对应的素材下发给用户，永久素材类型可以是图片、音频、视频、图文消息。请注意：永久素材id必须是在“素材管理/新增永久素材”接口上传后获得的合法id。
# 10、view_limited：跳转图文消息URL用户点击view_limited类型按钮后，微信客户端将打开开发者在按钮中填写的永久素材id对应的图文消息URL，永久素材类型只支持图文消息。请注意：永久素材id必须是在“素材管理/新增永久素材”接口上传后获得的合法id。

#自定义菜单的创建接口
def create_menu(request):
	# 第一个参数是公众号里面的appID，第二个参数是appsecret
    client = WeChatClient("wx058a1e6adf42dede", "d4631adb81c598c1f9acddfb4bc2ba10")
    client.menu.create({
        "button": [
            {
                "name": "扫码", 
                "key": "V1001_TODAY_MUSIC", 
                "sub_button": [ 
                    {   
                        "type": "scancode_push", 
                        "name": "扫码推事件", 
                        "key": "V1001_1",
                        "sub_button": [ ]
                    },
                    {   
                        "type": "scancode_waitmsg", 
                        "name": "扫码带提示", 
                        "key": "V1001_2",
                        "sub_button": [ ]
                    }
                ]
            },
            {
                "name": "发图",  
                "sub_button": [ 
                    {   
                        "type": "pic_sysphoto", 
                        "name": "系统拍照发图", 
                        "key": "V1002_1",
                        "sub_button": [ ]
                    },
                    {   
                        "type": "pic_photo_or_album", 
                        "name": "拍照或者相册发图", 
                        "key": "V1002_2",
                        "sub_button": [ ]
                    },
                    {   
                        "type": "pic_weixin", 
                        "name": "微信相册发图", 
                        "key": "V1002_3",
                        "sub_button": [ ]
                    }
                ]
            },        
            {
                "name": "发送位置", 
                "type": "location_select", 
                "key": "rselfmenu_2_0"
            }

        ]     
        # "matchrule": {
        #     "group_id": "2",
        #     "sex": "1",
        #     "country": "中国",
        #     "province": "广东",
        #     "city": "广州",
        #     "client_platform_type": "2"
        # }
    })
    return HttpResponse('ok')