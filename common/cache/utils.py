from django.core.cache import cache

# When calling cache.get(key), the following queries are executed:
# 1. SELECT "cache_key", "value", "expires" FROM "cache" WHERE "cache_key" IN (':1:canteen_statistics_2024')
CACHE_GET_QUERY_COUNT = 1


# When calling cache.set(key, value, timeout), the following queries are executed:
# 1. SELECT "cache_key", "value", "expires" FROM "cache" WHERE "cache_key" IN (':1:canteen_statistics_2024')
# 2. SELECT COUNT(*) FROM "cache"
# 3. SAVEPOINT "s123199703347200_x22"
# 4. SELECT "cache_key", "expires" FROM "cache" WHERE "cache_key" = ':1:canteen_statistics_2024'
# 5. INSERT INTO "cache" ("cache_key", "value", "expires") VALUES (':1:canteen_statistics_2024', 'gAWVtQEAAAAAAAB9lCiMDGNhbnRlZW5Db3VudJRLBIwQc2VjdG9yQ2F0ZWdvcmllc5R9lCiMDmFkbWluaXN0cmF0aW9ulEsAjAplbnRlcnByaXNllEsCjAllZHVjYXRpb26USwKMBmhlYWx0aJRLAIwGc29jaWFslEsAjAdsZWlzdXJllEsAjAZhdXRyZXOUSwCMB2luY29ubnWUSwJ1jA9tYW5hZ2VtZW50VHlwZXOUfZQojAZkaXJlY3SUSwKMCGNvbmNlZGVklEsCaAtLAHWMD3Byb2R1Y3Rpb25UeXBlc5R9lCiMB2NlbnRyYWyUSwGMDmNlbnRyYWxTZXJ2aW5nlEsBjARzaXRllEsBjBNzaXRlQ29va2VkRWxzZXdoZXJllEsBaAtLAHWMDmVjb25vbWljTW9kZWxzlH2UKIwGcHVibGljlEsCjAdwcml2YXRllEsCaAtLAHWMFXRlbGVkZWNsYXJhdGlvbnNDb3VudJRLAIwKYmlvUGVyY2VudJRLAIwSc3VzdGFpbmFibGVQZXJjZW50lEsAjA1lZ2FsaW1QZXJjZW50lEsAjAxhcHByb1BlcmNlbnSUSwB1Lg==', '2025-07-12T08:32:45+00:00'::timestamptz)
# 6. RELEASE SAVEPOINT "s123199703347200_x22"
CACHE_SET_QUERY_COUNT = 6


CACHE_TIMEOUT_1_day = 60 * 60 * 24
CACHE_TIMEOUT_7_days = 60 * 60 * 24 * 7
CACHE_TIMEOUT_30_days = 60 * 60 * 24 * 30


def get_or_set_cache(cache_key, compute_value, timeout):
    """
    Return the cached value for `cache_key`, computing and storing it via
    `compute_value()` on a cache miss.
    """
    value = cache.get(cache_key)
    if value is None:
        value = compute_value()
        cache.set(cache_key, value, timeout=timeout)
    return value
