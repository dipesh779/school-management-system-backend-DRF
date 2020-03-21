def create_response(success, data=None, item=None, items=None, err_name=None,
                    err_message=None):
    if success:
        if data is not None:
            return {
                "success": True,
                "response": data
            }
        elif item is not None:
            return {
                "success": True,
                "response": {
                    "item": item
                }
            }
        elif items is not None:
            return {
                "success": True,
                "response": {
                    "items": items
                }
            }
    else:
        return {
            "success": False,
            "error": {
                "name": err_name,
                "message": err_message
            }
        }