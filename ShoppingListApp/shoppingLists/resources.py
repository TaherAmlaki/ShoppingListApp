from flask_restful import Resource, reqparse
from flask import session, url_for
import urllib.parse as urlparse
from urllib.parse import parse_qs


help_msg = "Modifying shopping list without '{}' is not possible."

modify_parser = reqparse.RequestParser(bundle_errors=True)
modify_parser.add_argument('action', type=str, required=True, help=help_msg.format("action"))
modify_parser.add_argument('url', type=str, required=True, help=help_msg.format("url"))
modify_parser.add_argument('form', type=dict, required=True, help=help_msg.format("form"))
modify_parser.add_argument('itemIndex', type=str, required=False)


class ModifyShoppingListResource(Resource):
    @classmethod
    def post(cls):
        data = modify_parser.parse_args()        
        action, url, form_data, item_index = data["action"], data["url"], data["form"], data.get("itemIndex", None)
        
        parsed = urlparse.urlparse(url)
        if action == "add":
            items = int(parse_qs(parsed.query).get('items', [0])[0]) + 1
        elif action == "remove":
            items = max(int(parse_qs(parsed.query).get('items', [0])[0]) - 1, 0)
        else:
            items = int(parse_qs(parsed.query).get('items', [0])[0])
        form_data['action'] = action
        form_data['itemIndex'] = item_index
        session["AddShoppingListData"] = form_data
        return {"url": url_for("shopping_list_views.add_shopping_list", items=items)}
