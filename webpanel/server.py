from pathlib import Path
from pprint import pformat, pprint
from sys import stderr
from typing import TYPE_CHECKING

from aiohttp import web
from aiohttp.web_request import Request
from multidict._multidict import MultiDictProxy

from utils import FormattedMatrix

# if TYPE_CHECKING:
#     from ..utils import RGBMatrix

_MATRIX: "FormattedMatrix" = ...


def find_page(name: str) -> str:
    name = name.lstrip("/")
    path = Path(__file__).parent / "pages" / name

    if not path.exists():  # people don't really add .html to urls
        path = Path(__file__).parent / "pages" / f"{name}.html"

        if not path.exists():  # No file found
            print(f"Path {path} was not found!", file=stderr)
            raise web.HTTPNotFound()

    with open(path) as f:
        return f.read()


routes = web.RouteTableDef()

################
# Image routes #
################


@routes.get("/images/{name:.*}")
async def get_images(request: Request):
    """fetch any image, different path from normal pages"""
    name = request.match_info["name"]
    path = Path(__file__).parent / "images" / name

    if path.is_file():
        return web.FileResponse(path)

    if not path.is_dir():
        raise web.HTTPNotFound()

    # for when they travel to a folder
    res = "\n".join(
        f"<a href={path.name}/{child.name}>{child.name}</a>" for child in path.iterdir()
    )
    res = f"<head></head><body>{res}</body>"

    return web.Response(content_type="text/html", text=res)


@routes.get("/images")
async def get_images_root(request: Request):
    """this is dumb, it's missing a single slash"""
    raise web.HTTPFound("/images/")


@routes.get("/display")
async def display(request: Request):
    images = (Path(__file__).parent / "images").iterdir()
    button_format = (
        "<button type='submit' value={image_name}><img src='{image_path}'></button>"
    )

    buttons = "\n".join(
        button_format.format(
            image_path=f"/images/{image.name}",
            image_name=image.name,
        )
        for image in images
        if image.is_file()
    )

    page = find_page("/display").format(buttons=buttons)

    return web.Response(content_type="text/html", text=page)


@routes.get("/display_select")
async def display_select(request: Request):
    images = (Path(__file__).parent / "images").iterdir()
    select_format = "<option value={image_name}>{image_name}</option>"

    select_options = "\n".join(
        select_format.format(
            # image_path=f"/images/{image.name}",
            image_name=image.name,
        )
        for image in images
        if image.is_file()
    )
    print(select_options)
    page = find_page("/display_select").format(select_options=select_options)

    return web.Response(content_type="text/html", text=page)


@routes.post("/display_select")
async def display_select_post(request: Request):
    print(request.can_read_body)
    data = await request.post()
    print(data)
    print(_MATRIX)
    _MATRIX.display(f"webpanel/images/{data['select']}")
    print("bang")

    # print([f"{key:10}:{value}" for key, value, in request.query.items()])
    # pprint(request.__dict__)
    # print(request.query)
    # print(f"{request.body_exists = }")


@routes.post("/display")
async def display_post(request: Request):
    print("b")
    # for attr in dir(request):
    #     try:
    #         print(f"{attr}: {getattr(request, attr)}")
    #     except:
    #         print(f"{attr} messed up")
    # print(await request.text())
    print([f"{key:10}:{value}" for key, value, in request.items()])
    data = [*(await request.post()).values()]
    # print(data)
    # print(dict.__repr__(request))
    # for attr in dir(data):
    #     try:
    #         print(f"{attr}: {getattr(data, attr)}")
    #     except:
    #         print(f"{attr} messed up")
    # print([f"{key:10}:{value}" for key, value, in data.items()])


@routes.get(r"/{name:.*}")
async def fallback(request: Request):
    """The fall-through case for any request"""

    name = request.match_info["name"]
    if not name:
        raise web.HTTPFound("/index.html")

    return web.Response(text=find_page(name))


def start_server(matrix, port=8080):
    global _MATRIX
    _MATRIX = matrix
    print(_MATRIX)
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, port=port, host="localhost")
