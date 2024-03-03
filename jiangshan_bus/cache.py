from dogpile.cache import make_region

# 使用内存作为缓存后端
cache_config = {
    'backend': 'dogpile.cache.memory',
}

cache = make_region().configure(**cache_config)
