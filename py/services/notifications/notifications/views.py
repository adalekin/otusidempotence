from aiohttp import web


async def liveness(request):
    return web.Response()
