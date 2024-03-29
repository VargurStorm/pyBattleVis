import time

from modules.models.wreck import Wreck
from modules.config import logger
from modules.graphics.graphics_engine import GraphicsEngine
from modules.config.constants import Constants

logger = logger.setup_logging()


def create_mgl_textures_from_wreck_list(app: GraphicsEngine, tex_type: str, wreck_list: list[Wreck]):
    """
    Create ModernGL textures from wreck list. Updates directly in the app.mesh.texture.textures dictionary
    :param app: GraphicsEngine
    :param tex_type: str
    :param wreck_list: list[Wreck]
    :return: None
    """

    if tex_type == 'ship':
        texture_dict = app.mesh.texture.textures
        for wreck in wreck_list:
            image_download(wreck, tex_type, Constants.IMG_DOWNLOAD_RETIRES, Constants.IMG_DOWNLOAD_SLEEP_TIME)
            if wreck.ship_img_path:
                ship_id = wreck.ship_id
                mgl_texture = app.mesh.texture.get_texture(wreck.ship_img_path)
                texture_dict[ship_id] = mgl_texture

    if tex_type == 'char':
        texture_dict = app.mesh.texture.textures
        for wreck in wreck_list:
            image_download(wreck, tex_type, Constants.IMG_DOWNLOAD_RETIRES, Constants.IMG_DOWNLOAD_SLEEP_TIME)
            if wreck.char_img_path:
                char_id = wreck.char_id
                mgl_texture = app.mesh.texture.get_texture(wreck.char_img_path)
                texture_dict[char_id] = mgl_texture

    else:
        logger.error(f"Texture type {tex_type} not recognized")


def image_download(wreck: Wreck, image_type: str, retries: int, sleep_time: float):
    if image_type == 'ship':
        for i in range(retries):
            wreck.populate_ship_img()
            time.sleep(sleep_time)
            if wreck.ship_img_path:
                break
    elif image_type == 'char':
        for i in range(retries):
            wreck.populate_char_img()
            time.sleep(sleep_time)
            if wreck.char_img_path:
                break
    else:
        logger.error(f"Image type {image_type} not recognized")
        return
