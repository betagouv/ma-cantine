from api.permissions import IsAuthenticatedOrTokenHasResourceScope


def ma_cantine_preprocessing_hook(endpoints):
    """
    Includes only endpoints accessible through OAuth2 or those that have
    property "include_in_documentation" set to True
    """
    filtered_endpoints = []
    for (path, path_regex, method, callback) in endpoints:
        accessible_through_oauth2 = (
            hasattr(callback.cls, "permission_classes")
            and IsAuthenticatedOrTokenHasResourceScope in callback.cls.permission_classes
        )
        include_in_documentation = (
            hasattr(callback.cls, "include_in_documentation") and callback.cls.include_in_documentation
        )
        if accessible_through_oauth2 or include_in_documentation:
            filtered_endpoints.append((path, path_regex, method, callback))
    return filtered_endpoints
