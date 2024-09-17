<p align="center">
  <a href="https://nonebot.dev/"><img src="https://nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# nonebot-plugin-logstream

_✨ NoneBot 网页终端实时log显示/输出插件 ✨_ 
<br>
_✨ 基于SSE(Server-Sent Events) ✨_


</div>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
</p>

# 使用方式
在Nonebot项目的pyproject.toml文件plugins字样添加`nonebot_plugin_logstream`

或者pull项目到Nonebot插件目录

查看实时log网页:

- 运行Nonebot实例
- 浏览器访问 http://127.0.0.1:你的Nonebot端口/logs 

查看log输出流(SSE):

- 运行Nonebot实例
- 浏览器访问 http://127.0.0.1:你的Nonebot端口/logs/sse

# 贡献与支持

如果觉得此项目还有点用处请点个 `Star`谢谢喵

有意见或者建议欢迎提交 [Issues](https://github.com/KiKi-XC/nonebot_plugin_logstream/issues)
和 [Pull requests](https://github.com/KiKi-XC/nonebot_plugin_logstream/pulls)。

# 提示
KiKi-XC的第一个Nonebot插件,有代码不规范的地方,欢迎PR和指正!

SSE发送Log的频率为2秒刷新一次

`SSE(Server-Sent Events)`可能不兼容某些远古浏览器,例如 `IE`

输出流已经将ANSI颜色字符转换为HTML标签了,因此可以直接显示在网页上,可参考 `View/log.html`

# 许可证

本项目使用 [MIT](./LICENSE) 作为开源许可证。
