import discord
from flask import jsonify, request

from helpers.exceptions import WrongInputException
from helpers.module_pages import has_permissions
from helpers.tools import make_linear_gradient, html_color
from webserver import Page

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import StoreModule


async def get_store(module: 'StoreModule',
                    guild: discord.Guild,
                    member: discord.Member):
    store = []
    for offer in module.bot.db.get_store(guild.id):
        from_foreground_color = make_linear_gradient(offer[2].foreground_color)
        from_background_color = make_linear_gradient(offer[2].background_color)
        to_foreground_color = make_linear_gradient(offer[4].foreground_color)
        to_background_color = make_linear_gradient(offer[4].background_color)
        store.append({
            'id': offer[0].id,
            'from_item_amount': offer[0].from_item_amount,
            'to_item_amount': offer[0].to_item_amount,
            'from_item_id': offer[1].id,
            'from_item_type': offer[1],
            'to_item_id': offer[3].id,
            'to_item_type': offer[3],
            'from_foreground_color_html': html_color(from_foreground_color[0], from_foreground_color[1]),
            'from_background_color_html': html_color(from_background_color[0], from_background_color[1]),
            'to_foreground_color_html': html_color(to_foreground_color[0], to_foreground_color[1]),
            'to_background_color_html': html_color(to_background_color[0], to_background_color[1]),
        })
    return jsonify({'msg': 'success', 'store': store}), 200


async def buy_offer(module: 'StoreModule',
                    guild: discord.Guild,
                    member: discord.Member):
    json = request.get_json()
    if json is None or 'offer_id' not in json or 'amount' not in json:
        raise WrongInputException('offer_id or amount not given')

    await module.buy_offer(member, json['offer_id'], json['amount'])
    return jsonify({'msg': 'success'}), 200


@has_permissions(administrator=True)
async def set_store(module: 'StoreModule',
                    guild: discord.Guild,
                    member: discord.Member):
    json = request.get_json()
    if json is None or 'store' not in json:
        raise WrongInputException('store not given')
    module.bot.db.set_store(guild.id, json['store'])
    return jsonify({'msg': 'success'}), 200


API_PAGES = [
    Page(path='set-store', view_func=set_store, methods=['POST']),
    Page(path='get-store', view_func=get_store),
    Page(path='buy-offer', view_func=buy_offer, methods=['POST']),
]
