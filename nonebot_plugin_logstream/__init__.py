import nonebot
import asyncio
from pathlib import Path
from fastapi import FastAPI
from ansi2html import Ansi2HTMLConverter
from nonebot.plugin import PluginMetadata
from loguru import logger as loguru_logger
from starlette.responses import HTMLResponse
from sse_starlette.sse import EventSourceResponse


# 插件元数据信息
__plugin_meta__ = PluginMetadata(
    name="SSE日志输出流",
    description="NoneBot 网页终端实时log显示/输出插件",
    usage="详见文档",
    type="application",
    homepage="https://github.com/KiKi-XC/nonebot_plugin_logstream",
    supported_adapters=None,
)

# 初始化FastAPI应用
router: FastAPI = nonebot.get_app()

# 初始化日志队列和ANSI转HTML的转换器
log_queue = asyncio.Queue(maxsize=1000)  # 设置日志队列的最大大小
conv = Ansi2HTMLConverter(inline=True)


# 通过Server-Sent Events (SSE)流式传输日志
@router.get("/logs/sse")
async def log_sse():
    """
    通过Server-Sent Events (SSE)流式传输日志。

    Returns:
        EventSourceResponse: SSE响应对象
    """

    async def log_generator():
        """
        生成日志数据的异步生成器。
        """
        while True:
            log = await log_queue.get()
            html_log = conv.convert(log, full=False)
            yield {"data": html_log}

    return EventSourceResponse(
        log_generator(),
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream"
        }
    )


# 获取日志页面
@router.get("/logs")
async def get_log_page():
    """
    获取日志页面。

    Returns:
        HTMLResponse: 日志页面的HTML响应
    """
    config_file = Path(__file__).resolve().parents[0] / 'View/log.html'
    with open(config_file, 'r', encoding='utf8') as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


# 添加日志到队列
def add_log(logs: str):
    """
    添加日志到队列，并检查是否超出最大容量。

    Args:
        logs (str): 要添加的日志字符串
    """
    try:
        log_queue.put_nowait(logs)
    except asyncio.QueueFull:
        log_queue.get_nowait()  # 移除队列中的最旧日志
        log_queue.put_nowait(logs)


# 过滤日志记录
def filter_logs(record):
    """
    过滤日志记录。

    Args:
        record (dict): 日志记录

    Returns:
        bool: 是否过滤该日志记录
    """
    return "/logs" not in record["message"]


# 配置logger使用add_log函数处理日志
loguru_logger.add(add_log, colorize=True, level="INFO", filter=filter_logs)
