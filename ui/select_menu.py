import disnake

from disnake.ui import Select, View
from ui.embeds import registration_confirm_embed


# dropdown list with role
class DropdownRoleMenu(Select):
    def __init__(self, username: str, bank_card: int, user_id: int):
        self.username = username
        self.bank_card = bank_card
        self.user_id = user_id

        options = [
            disnake.SelectOption(label="програміст", description="написання коду", emoji="👨🏽‍💻"),
            disnake.SelectOption(label="дизайнер", description="UI/UX дизайн", emoji="🎨"),
            disnake.SelectOption(label="художник", description="", emoji="🖌"),
            disnake.SelectOption(label="аніматор", description="", emoji="🎬"),
            disnake.SelectOption(label="звукорежисер", description="", emoji="🎧"),
            disnake.SelectOption(label="сценаристи", description="", emoji="✍️"),
            disnake.SelectOption(label="перекладачі", description="", emoji="🌍"),
            disnake.SelectOption(label="тестувальники", description="", emoji="🧪"),
        ]
        super().__init__(
            placeholder="Вибери роль/ролі",
            min_values=1,
            max_values=3,
            options=options,
        )

    async def callback(self, inter: disnake.MessageInteraction):
        from ui.buttons import ConfirmBtn
        await inter.response.defer()
        view = ConfirmBtn(self.username, self.bank_card, self.values, self.user_id)
        embed = registration_confirm_embed(self.username, self.bank_card, self.values)
        await inter.followup.send(embed=embed, view=view, ephemeral=True)



# revision list with role    
class DropdownRoleView(View):
    def __init__(self, username: str, bank_card: int, user_id: int):
        super().__init__(timeout=300.0)
        self.add_item(DropdownRoleMenu(username, bank_card, user_id))