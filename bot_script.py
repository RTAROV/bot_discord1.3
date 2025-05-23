import discord
from discord.ext import commands
from discord.ui import View, Select
from datetime import datetime

from myserver import server_on

import json
import os

# --- Intents ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- ข้อมูลผู้ใช้แบบรวม ---
user_data = {}  # {user_id: {"item": str, "money": int, "total_online": int, "last_online": str}}

# --- โหลดข้อมูล ---
def load_data():
    if os.path.exists("user_data.json"):
        with open("user_data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# --- บันทึกข้อมูล ---
def save_data():
    with open("user_data.json", "w", encoding="utf-8") as f:
        json.dump(user_data, f, ensure_ascii=False, indent=4)

# --- เมื่อบอทเริ่มทำงาน ---
@bot.event
async def on_ready():
    global user_data
    user_data = load_data()
    print(f"Logged in as {bot.user.name}")

# --- ตอบคำถามอัตโนมัติ ---
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    faq = {
        "how to verify": "กรุณาตรวจสอบอีเมลของคุณเพื่อยืนยันตัวตน.",
    "what is your name": "ชื่อของฉันคือ AuthBot.",
    "help": "กรุณาถามคำถามที่ต้องการ, ฉันจะตอบให้!",
    "มิเชล": "ว่างัยคะ?",
    "สวัสดี": "สวัสดีค่ะ! ยินดีต้อนรับสู่เซิร์ฟเวอร์ของเรา!",
    "คุณชื่ออะไร": "ชื่อของฉันคือ มิเชลค่ะ!",
    "คุณทำอะไรได้บ้าง": "ฉันสามารถช่วยตอบคำถามทั่วไปเกี่ยวกับเซิร์ฟเวอร์นี้ได้ค่ะ!",
    "คุณช่วยอะไรได้บ้าง": "ฉันสามารถช่วยตอบคำถามทั่วไปเกี่ยวกับเซิร์ฟเวอร์นี้ได้ค่ะ!",
    "คุณเป็นใคร": "ฉันคือบอทที่ช่วยตอบคำถามเกี่ยวกับเซิร์ฟเวอร์นี้ค่ะ!",
    "คุณอยู่ที่ไหน": "ฉันอยู่ในเซิร์ฟเวอร์นี้ค่ะ!",
    "มิเชลคับ": "ค่ะ! มีอะไรให้ช่วยไหมคะ?",
    "มิเชลครับ": "ค่ะ! มีอะไรให้ช่วยไหมคะ?",
    "มิเชลมีแฟนไหใหม": "มีแล้วคะชื่อชิริวค่ะ",
    "มิเชลมีแฟนไหม": "มีแล้วคะชื่อชิริวค่ะ",
    "มิเชลมีแฟนหรือยัง": "มีแล้วคะชื่อชิริวค่ะ",
    "มิเชลมีแฟนหรือยังคะ": "มีแล้วคะชื่อชิริวค่ะ",
    "มิเชลมีแฟนหรือยังครับ": "มีแล้วคะชื่อชิริวค่ะ",
    "มิเชลมีแฟนหรือยัง": "มีแล้วคะชื่อชิริวค่ะ",
    "มิเชลชอบกินอะไร": "ชอบกินเค้กค่ะ",
    "มิเชลชอบกินอะไรคะ": "ชอบกินเค้กค่ะ",
    "มิเชลชอบกินอะไรครับ": "ชอบกินเค้กค่ะ",
    "มิเชลชอบกินอะไรไหม": "ชอบกินเค้กค่ะ",
    "มิเชลชอบไปเหน": "ชอบไปทะเลค่ะ",
    "มิเชลชอบไปไหน": "ชอบไปทะเลค่ะ",
    "มิเชลชอบไปไหนคะ": "ชอบไปทะเลค่ะ",
    "มิเชลชอบไปไหนครับ": "ชอบไปทะเลค่ะ",
    "มิเชลชอบไปไหนไหม": "ชอบไปทะเลค่ะ",
    "มิเชลชอบไปไหนหรอ": "ชอบไปทะเลค่ะ",
    "แม่เตชื่อไร": "บุ๋มไงค่ะ",
    "แม่เตชื่ออะไร": "บุ๋มไงค่ะ",
    "แม่เตชื่ออะไรคะ": "บุ๋มไงค่ะ",
    "แม่เตชื่ออะไรครับ": "บุ๋มไงค่ะ",
    "แม่เตชื่ออะไรหรอ": "บุ๋มไงค่ะ",
    "ใครหล่อที่สุด": "Poomคะหล่อมากๆหล่อที่สุดเลยค่ะ",
    "ใครหล่อที่สุดคะ": "Poomคะหล่อมากๆหล่อที่สุดเลยค่ะ",
    "ใครหล่อที่สุดครับ": "Poomคะหล่อมากๆหล่อที่สุดเลยค่ะ",
    "ใครหล่อที่สุดหรอ": "Poomคะหล่อมากๆหล่อที่สุดเลยค่ะ",
    "ต่อยกันไหม": "ไม่อยากต่อยกับหมาคะ",
    "ต่อยกันไหมคะ": "ไม่อยากต่อยกับหมาคะ",
    "ต่อยกันไหมครับ": "ไม่อยากต่อยกับหมาคะ",
    "ขอเป็นแฟนได้ไหม": "ได้คะถ้าหล่อๆ",
    "ขอเป็นแฟนได้ไหมคะ": "ได้คะถ้าหล่อๆ",
    "ขอเป็นแฟนได้ไหมครับ": "ได้คะถ้าหล่อๆ",
    "ขอเป็นแฟนได้ไหมหรอ": "ได้คะถ้าหล่อๆ",
    "ขอเป็นแฟนได้ไหมหรอคะ": "ได้คะถ้าหล่อๆ",
    "ขอเป็นแฟนได้ไหมครับ": "ได้คะถ้าหล่อๆ",
    "มีไรให้ช่วยด่าตี๋ให้หน่อย": "อย่าไปด่าหมาเลยคะแต่ขอมาก็ได้คะไอ้ตี๋ไอ้เบียว",
    "มีไรให้ช่วยด่าตี๋ให้หน่อยคะ": "อย่าไปด่าหมาเลยคะแต่ขอมาก็ได้คะไอ้ตี๋ไอ้เบียว",
    "มีไรให้ช่วยด่าตี๋ให้หน่อยครับ": "อย่าไปด่าหมาเลยคะแต่ขอมาก็ได้คะไอ้ตี๋ไอ้เบียว",
    "ด่าตี๋หน่อย": "อย่าไปด่าหมาเลยคะแต่ขอมาก็ได้คะไอ้ตี๋ไอ้เบียว",
    "ด่าตี๋หน่อยคะ": "อย่าไปด่าหมาเลยคะแต่ขอมาก็ได้คะไอ้ตี๋ไอ้เบียว",
    "มิเชลคับ": "ว่างัยคะ?",
    "มิเชลครับ": "ว่างัยคะ?",
    "ควย" : "ควยไรไอ้สัส",
    "ควยไร" : "ควยไรไอ้สัส",
        "มีผัวยัง": "มีแล้วคะชื่อชิริวค่ะ",
    "มีผัวไหม": "มีแล้วคะชื่อชิริวค่ะ",
    "เราเท่ป่าว": "เท่มากคะ",
    "เราเท่ไหม": "เท่มากคะ",
    "เราสวยไหม": "สวยมากคะ",
    "เราสวยป่าว": "สวยมากคะ",
    "มีแฟนยัง": "มีแล้วคะชื่อชิริวค่ะ",
    "ขอตอกได้มั้ย" : "ได้คะถ้าหล่อๆได้ก็ต้อง56ได้คะ",
    "มีแฟนยัง" : "มีแล้วคะชื่อชิริวค่ะ",
    "มีแฟนไหม" : "มีแล้วคะชื่อชิริวค่ะ",
    "ขอตบได้ไหมครับ" : "เจอได้คะ",
    "ขอดูนมหน่อย" : "ได้คะส่งควยมาก่อน",
    "ขอดูนมได้ไหม" : "ได้คะส่งควยมาก่อน",
    "ขอดูหีหน่อย" : "ไปขอแฟนมึงนะคะอ๋อไม่มีแฟนหรอ",
    "อยากเป็นแฟนกับมิเชล" : "ได้คะถ้าหล่อๆ",
    "แฟนเก่ามิเชลชื่อไร" : "ชื่อรุจคะ",
    "แฟนเก่ามิเชลชื่ออะไร" : "ชื่อรุจคะ",
    "แฟนเก่ามิเชลชื่ออะไรคะ" : "ชื่อรุจคะ",
    "แฟนเก่ามิเชลชื่ออะไรครับ" : "ชื่อรุจคะ",
    "แฟนเก่ามิเชลชื่ออะไรหรอ" : "ชื่อรุจคะ",
    "ทำไมถึงเลิกกับรุจ" : "เพราะว่าควยเล็กคะ",
    "ทำไมถึงเลิกกับรุจคะ" : "เพราะว่าควยเล็กคะ",
    "ทำไมถึงเลิกกับรุจครับ" : "เพราะว่าควยเล็กคะ",
    "คิดถึงเราไหม" : "คิดถึงคะ",
    "คิดถึงเรามั้ย" : "คิดถึงคะ",
    "คิดถึงเรามั้ยคะ" : "คิดถึงคะ",
    "คิดถึงเรามั้ยครับ" : "คิดถึงคะ",
    "คิดถึงเราหรอ" : "คิดถึงคะ",
    "คิดถึงเราหรอคะ" : "คิดถึงคะ",
    "เฟิสร์หล่อไหม" : "ถามพี่จ๋าดู",
    "เฟิสร์หล่อมั้ย" : "ถามพี่จ๋าดู",
    "เฟิสร์หล่อมั้ยคะ" : "ถามพี่จ๋าดู",
    "กินไรดี" : "กินข้าวคะ",
    "กินไรดีคะ" : "กินข้าวคะ",
    "กินไรดีครับ" : "กินข้าวคะ",
    "กินไรดีหรอ" : "กินข้าวคะ",
    "เราหล่อไหม" : "หล่อก็ได้คะ",
    "เราหล่อป่าว" : "หล่อก็ได้คะ",
    "เราหล่อมั้ย" : "หล่อก็ได้คะ",
    "เราหล่อมั้ยคะ" : "หล่อก็ได้คะ",
    "เราหล่อมั้ยครับ" : "หล่อก็ได้คะ",
    "เราหล่อมั้ยหรอ" : "หล่อก็ได้คะ",
    "เราหล่อมั้ยหรอคะ" : "หล่อก็ได้คะ",
    "เราน่ารักไหม" : "น่ารักคะ",
    "เราน่ารักป่าว" : "น่ารักคะ",
    "เราน่ารักมั้ย" : "น่ารักคะ",
    "เราน่ารักมั้ยคะ" : "น่ารักคะ",
    "เราน่ารักมั้ยครับ" : "น่ารักคะ",
    "วิวน่ารักไหม" : "น่ารักคะ",
    "วิวน่ารักป่าว" : "น่ารักคะ",
    "วิวน่ารักมั้ย" : "น่ารักคะ",
    "ทำไรดี" : "เล่นเกมคะ",
    "ทำไรดีคะ" : "เล่นเกมคะ",
    "ทำไรดีครับ" : "เล่นเกมคะ",
    "ทำไรดีหรอ" : "เล่นเกมคะ",
    }

    content = message.content.lower()
    if content in faq:
        await message.channel.send(faq[content])
    else:
        await bot.process_commands(message)

# --- เมนูเลือกสถานะ ---
class ItemSelect(Select):
    def __init__(self, user_id):
        self.user_id = str(user_id)
        options = [
            discord.SelectOption(label="มีแฟน", emoji="❤️"),
            discord.SelectOption(label="มีคนคุย", emoji="😊"),
            discord.SelectOption(label="โสดเว้ย", emoji="🧪")
        ]
        super().__init__(placeholder="เลือกสถานะ...", options=options)

    async def callback(self, interaction: discord.Interaction):
        uid = self.user_id
        if uid not in user_data:
            user_data[uid] = {"item": "", "money": 0, "total_online": 0, "last_online": None}
        user_data[uid]["item"] = self.values[0]
        save_data()
        await interaction.response.send_message(f"✅ คุณเลือก: **{self.values[0]}**", ephemeral=True)

class ItemView(View):
    def __init__(self, user_id):
        super().__init__()
        self.add_item(ItemSelect(user_id))

@bot.command()
async def โชว์โปรไฟล์(ctx):
    view = ItemView(ctx.author.id)
    await ctx.send("กรุณาเลือกสถานะของคุณ:", view=view)

@bot.command()
async def เช็คโปรไฟล์(ctx):
    uid = str(ctx.author.id)
    user = user_data.get(uid, {"item": "ยังไม่ได้เลือก", "money": 0, "total_online": 0})

    total_seconds = user.get("total_online", 0)
    if user.get("last_online"):
        last_time = datetime.fromisoformat(user["last_online"])
        total_seconds += int((datetime.utcnow() - last_time).total_seconds())

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    time_str = f"{hours} ชั่วโมง {minutes} นาที"

    embed = discord.Embed(
        title=f"โปรไฟล์ของ {ctx.author.name}",
        color=discord.Color.green()
    )
    embed.add_field(name="สถานะ", value=user.get("item", "ยังไม่ได้เลือก"), inline=False)
    embed.add_field(name="🕒 เวลาที่ออนไลน์รวม", value=time_str, inline=False)
    embed.add_field(name="💰 เงิน", value=f'{user.get("money", 0)} เหรียญ', inline=False)
    embed.set_thumbnail(url=ctx.author.display_avatar.url)

    await ctx.send(embed=embed)

# --- ติดตามสถานะออนไลน์ ---
@bot.event
async def on_presence_update(before, after):
    uid = str(after.id)
    now = datetime.utcnow()

    if uid not in user_data:
        user_data[uid] = {"item": "", "money": 0, "total_online": 0, "last_online": None}

    if after.status == discord.Status.online:
        user_data[uid]["last_online"] = now.isoformat()
    elif after.status != discord.Status.online and user_data[uid].get("last_online"):
        last_online = datetime.fromisoformat(user_data[uid]["last_online"])
        online_time = int((now - last_online).total_seconds())
        user_data[uid]["total_online"] += online_time
        user_data[uid]["last_online"] = None
        save_data()

server_on()

bot.run(os.getenv('TOKEN'))
