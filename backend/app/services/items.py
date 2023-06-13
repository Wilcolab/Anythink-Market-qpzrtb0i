from slugify import slugify

from app.db.errors import EntityDoesNotExist
from app.db.repositories.items import ItemsRepository
from app.models.domain.items import Item
from app.models.domain.users import User


async def check_item_exists(items_repo: ItemsRepository, slug: str) -> bool:
    try:
        await items_repo.get_item_by_slug(slug=slug)
    except EntityDoesNotExist:
        return False

    return True


def get_slug_for_item(title: str) -> str:
    return slugify(title)


def check_user_can_modify_item(item: Item, user: User) -> bool:
    return item.seller.username == user.username

def get_image_for_title(title: str, size: str) -> str:
    try:
        response = openai.Image.create(prompt=title, n=1, size=size)
        image_url = response['data'][0]['url']
        return image_url
    except openai.error.OpenAIError as e:
        print(e.http_status)
        print(e.error)
        return None
