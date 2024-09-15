import nonebot
import asyncio
from typing import List
from pathlib import Path
from fastapi import FastAPI
from loguru import logger as loguru_logger
from ansi2html import Ansi2HTMLConverter
from starlette.responses import HTMLResponse
from sse_starlette.sse import EventSourceResponse


# 初始化FastAPI应用
router: FastAPI = nonebot.get_app()

# 初始化日志缓冲区和ANSI转HTML的转换器
log_buffer: List[str] = []
conv = Ansi2HTMLConverter(inline=True)


@router.get("/logs/sse")
async def log_sse():
    """
    通过Server-Sent Events (SSE)流式传输日志。

    参数:
    - request: 当前的请求对象

    返回值:
    - EventSourceResponse: 用于SSE的数据流响应
    """

    async def log_generator():
        """生成日志数据的异步生成器。"""
        last_sent_index = 0
        while True:
            if last_sent_index < len(log_buffer):
                for i in range(last_sent_index, len(log_buffer)):
                    html_log = conv.convert(log_buffer[i], full=False)
                    yield {"data": html_log}
                last_sent_index = len(log_buffer)
            else:
                yield {"data": "heartbeat"}
            await asyncio.sleep(2)

    return EventSourceResponse(
        log_generator(),
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream"
        }
    )


@router.get("/logs")
async def get_log_page():
    """
    获取日志页面。

    参数:
    - request: 当前的请求对象

    返回值:
    - HTMLResponse: 包含日志页面HTML内容的响应
    """
    config_file = Path(__file__).resolve().parents[0] / 'View/log.html'
    with open(config_file, 'r', encoding='utf8') as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


def add_log(logs: str):
    """
    添加日志到缓冲区。

    参数:
    - logs: 待添加的日志字符串
    """
    log_buffer.append(logs)


def filter_logs(record):
    """
    过滤日志记录，排除包含"/logs"的记录,因为他在实际体验太烦了（

    参数:
    - record: 日志记录对象

    返回值:
    - bool: 是否允许该日志记录通过
    """
    return "/logs" not in record["message"]


# 配置logger使用add_log函数处理日志，支持日志着色和设定日志级别
loguru_logger.add(add_log, colorize=True, level="INFO", filter=filter_logs)
