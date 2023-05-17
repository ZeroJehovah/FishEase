# FishEase
一个简单的，用于摸鱼的小工具。  
是[Game-Resize](https://github.com/ZeroJehovah/Game-Resize)项目的Python实现，并添加了调整音量的功能。  
ChatGPT依然提供了大量帮助，这次名字也是它起的。
# 作用
当目标窗口失去焦点，使其缩小并置顶，同时将音量调小；当恢复焦点，使其回复原尺寸，并恢复音量。
# 使用方法
1. 下载[最新版本](https://github.com/ZeroJehovah/FishEase/releases)并解压；
2. 配置```config/app.ini```：
   > title: 必填，需要控制的窗口的标题  
   > classname: 选填，需要控制的窗口的类名，如果为空的话可能查找窗口不准确，可通过[Window Detective](https://windowdetective.sourceforge.io/)等工具获取  
   > small-client-width: 缩小后的宽度，为空时不会调整窗口尺寸
3. 运行```FishEase.exe```
# 常见问题
1. 本程序是在win11上开发和测试的,如果遇到无法运行/缺少依赖/奇奇怪怪的bug，可尝试[升级](https://www.microsoft.com/zh-cn/windows/get-windows-11)后使用
2. 本程序仅对[崩坏：星穹铁道](https://sr.mihoyo.com/)这款游戏做了测试，如果对你想控制的软件支持不理想，可以考虑其它程序。
3. 如使用失去焦点自动缩小的功能，需要将程序设置为窗口化。
4. 在缩小显示时，可按住```Alt```拖动窗口。
5. 可在配置文件中配置多个程序窗口信息，但是只有第一个监测到的会生效。
   > 如需配置第二个程序，把第一个程序的所有配置，包括方括号那一行，都复制一份，方括号的名字需更改，以此类推。
6. 本程序已基本满足我的需求，下面的功能现在没有，以后大概率也不会有：
   > 多系统兼容、自动检测程序窗口、缩放时动画、开机自启动、自动更新等
7. 本程序仅几百行代码，欢迎二次开发。