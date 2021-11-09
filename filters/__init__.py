from loader import dp
from .is_private import IsPrivate, IsAdmin
from .is_group_join import IsGroupJoin, IsNotSub
from .groups_filters import ServicesChat

if __name__ == "filters":
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(IsGroupJoin)
    dp.filters_factory.bind(IsNotSub)
    dp.filters_factory.bind(ServicesChat)

