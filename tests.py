import asyncio
import random
import unittest

from bot import DiscordBot
from helpers.db import Database
from helpers.dummys import GuildDummy, MemberDummy
from helpers.i18n_manager import I18nManager
from modules.inventory import InventoryModule
from modules.wheelspin import WheelspinModule


class Tests(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.bot = DiscordBot(
            Database(''),
            I18nManager(data={})
        )

    async def test_activate_module(self):
        g = GuildDummy()
        await self.bot.module_manager.activate_module(g.id, 'messaging', sync=False)
        self.assertListEqual(['general', 'messaging'], self.bot.module_manager.get_activated_modules(g.id))
        await self.bot.module_manager.deactivate_module(g.id, 'messaging', sync=False)
        self.assertListEqual(['general'], self.bot.module_manager.get_activated_modules(g.id))

    async def test_wheelspin(self):
        g = GuildDummy()
        m = MemberDummy()
        g.member_join(m)
        await self.bot.module_manager.activate_module(g.id, 'inventory', sync=False)
        inventory: InventoryModule = self.bot.module_manager.get('inventory')
        await inventory.add_rarity(g, 'Epic', '(255,255,255)', '(0,0,0)')
        for i in range(10):
            await inventory.create_item_type(g, {
                'item_name': 'Item{}'.format(i + 1),
                'item_rarity': 1,
                'item_always_visible': False,
                'item_tradable': False,
                'item_useable': 1,
                'item_action': '',
            })
        await self.bot.module_manager.activate_module(g.id, 'wheelspin', sync=False)
        wheelspin: WheelspinModule = self.bot.module_manager.get('wheelspin')
        random.seed(0)
        await wheelspin.set_wheelspin(g, [
            {
                'item_type_id': i * 2,
                'probability': 1,
                'amount': 0,
                'sound': False
            } for i in range(5)
        ])
        res = await wheelspin.spin_wheel(m)
        self.assertEqual(5, res.WheelspinProbability.id)


if __name__ == '__main__':
    unittest.main()
