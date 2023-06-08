# FishEase

一个简单的，用于摸鱼的小工具。

是[Game-Resize](https://github.com/ZeroJehovah/Game-Resize)的Python实现，并添加了调整音量等功能。

ChatGPT依然提供了大量帮助，这次名字也是它起的。


# 基本功能

> 简单来说，方便于游戏挂机摸鱼

配置一个或多个软件窗口，本程序会持续寻找其是否存在

发现目标窗口后，持续监测它的焦点获取情况，并且对目标窗口执行以下操作：

> 失去焦点时：缩小尺寸、窗口置顶、减小音量
>
> 获取焦点时：恢复原始尺寸、窗口取消置顶、恢复原始音量


# 适用范围

- 窗口化显示

- 窗口标题固定

- 同一时间只存在一个窗口


# 使用方法

下载[最新版本](https://github.com/ZeroJehovah/FishEase/releases)并解压

完成基础配置（详见下一章节）

运行```FishEase.exe```


# 配置文件

本程序配置文件路径为```config/app.ini```

> 配置文件将在运行程序后自动创建，如需手动创建，请注意使用```UTF-8```编码

配置文件格式参考：

```ini
[StarRail]
title = 崩坏：星穹铁道
classname = UnityWndClass
small-client-width = 320
```

这是一组配置的完整示例，如果要监测多个软件窗口，则应有多组配置

第一行为本组配置的名称，用方括号括起来，只能包含英文字母，各组配置的名称不应重复

```title``` 必填，待监测窗口标题

```classname``` 选填，待监测窗口的类名，可通过[Window Detective](https://windowdetective.sourceforge.io/)等工具获取

> 如果此项为空，本程序将使用效率更低的方式寻找窗口，并且结果可能不准确

```small-client-width``` 选填，窗口缩小后的宽度

> 如果此项为空，则禁用失去焦点时的“缩小尺寸”功能


# 常见问题

无法运行/出现报错

> 本程序是在win11上开发和测试的，如有条件，可[升级系统](https://www.microsoft.com/zh-cn/windows/get-windows-11)后使用

源码无法编译

> 本程序基于[Python3.8.0](https://www.python.org/downloads/release/python-380/)开发

控制某些软件窗口时出现奇怪的bug

> 本程序仅对[崩坏：星穹铁道](https://sr.mihoyo.com/)这款游戏做了测试，如果实际使用效果不理想，请选择其它程序

无法调整尺寸

> 如使用失去焦点时的”缩小尺寸”功能，目标软件界面应当设置为窗口化

窗口缩小后的尺寸比例不正常/无法调整窗口缩小后的大小

> 缩小后的窗口尺寸会在本程序第一次发现该窗口时初始化
> 
> 如调整了配置文件```small-client-width```选项，或改变了窗口原始尺寸比例，应在```config/form.ini```里删除这个软件的配置，然后重新启动程序

怎么调整缩小后窗口的位置

> 窗口尺寸缩小后，可按住```Alt```然后拖动窗口，或者在系统托盘图标的右键菜单里取消“调节尺寸”勾选

配置并打开了多个软件窗口，但只有一个会被控制

> 是的，本程序只会监测第一个发现的窗口，当前监测的窗口名可在系统托盘图标的右键菜单里查看

能不能添加xx功能

> 一般不能，本程序已基本满足我的需求，其它未实现的功能，以后大概率不会有

能不能把代码拿去用

> 可以，如果觉得有用，请随意拿去使用或者二次开发
