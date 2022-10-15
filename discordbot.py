# 環境変数用 標準ライブラリなのでインストール不要
import os
import subprocess
# 文字エンコード
import json
# 正規表現
import re
# インストールした discord.py を読み込む
import discord

# Botのアクセストークン 環境変数から
TOKEN = os.environ['CRAFTBOT_TOKEN']

# 接続に必要なオブジェクトを生成
client = discord.Client()

# 日本語のクラフタースキル名の読み込み
def read_CraftSkillsName_JP():
    # ファイルを読み込んで行毎にリストに格納
    with open('CraftSkills_JP.txt', mode='r',encoding="utf-8") as f:
        CraftSkills = f.readlines()
    # 改行を取り除く
    for i , CraftSkill in enumerate(CraftSkills):
        CraftSkills[i] = CraftSkill.replace('\n','')
    return CraftSkills

# 英語のクラフタースキル名の読み込み
def read_CraftSkillsName_EN():
    # ファイルを読み込んで行毎にリストに格納
    with open('CraftSkills_EN.txt', mode='r',encoding="utf-8") as f:
        CraftSkills = f.readlines()
    # 改行を取り除く
    for i , CraftSkill in enumerate(CraftSkills):
        CraftSkills[i] = CraftSkill.replace('\n','')
    return CraftSkills

def read_CraftSkills_Wait():
    # ファイルを読み込んで行毎にリストに格納
    with open('CraftSkills_Wait.txt', mode='r',encoding="utf-8") as f:
        CraftSkills = f.readlines()
    # 改行を取り除く
    for i , CraftSkill in enumerate(CraftSkills):
        CraftSkills[i] = CraftSkill.replace('\n','')
    return CraftSkills


def extract_action(receive_message):
    # 行ごとに分ける
    split_messages = receive_message.splitlines()
    #クラフターのマクロかどうかの判定
    judge = "NONE"
    # 空のマクロリスト
    actions = []

    #JPマクロ
    CraftSkills_JP = read_CraftSkillsName_JP()
    for split_message in split_messages:
        for index in range(len(CraftSkills_JP)):
            pattern = re.compile(r"^/ac " + CraftSkills_JP[index])
            if bool(pattern.search(split_message)):
                actions.append(index)
                judge = "JP_MACRO"
                break

    #ENマクロ
    if(judge == "NONE"):
        CraftSkills_EN = read_CraftSkillsName_EN()
        for split_message in split_messages:
            for index in range(len(CraftSkills_EN)):
                pattern = re.compile(r"^/ac " + CraftSkills_EN[index])
                if bool(pattern.search(split_message)):
                    actions.append(index)
                    judge = "EN_MACRO"
                    break

    if (judge == "NONE"):
        extract = "NONE"
    else:
        extract = actions
    return extract

#通常の日本語マクロ
def convert_message_JP_normal(actions):
    CraftSkills_JP  = read_CraftSkillsName_JP()
    CraftWaits      = read_CraftSkills_Wait()
    macro_page      = 0

    res_message = "***日本語マクロ（通常）***\n"
    # アクションの数が15*nでない場合
    if(len(actions)%15 != 0):
        # アクションの数を15で割った数+1がマクロのページ数
        res_message += str(len(actions)) + "actions" + str(int(len(actions)/15) + 1) + "macro\n"
        # 15で割った数が1以上なら、ページ数は2ページ以上
        if(int(len(actions)/15) > 0):
            res_message += "**page1**\n"
    # アクションの数が15*nの場合
    else:
        # アクションの数を15で割った数がマクロのページ数
        res_message += str(len(actions)) + "actions" + str(int(len(actions)/15)) + "macro\n"
        # 15で割った数-1が1以上なら、ページ数は2ページ以上
        if(int(len(actions)/15)-1 > 0):
            res_message += "**page1**\n"
    res_message += "```\n"
    for index in range(len(actions)):
        if(int(index/15) != macro_page):
            macro_page = int(index/15)
            res_message += "```\n"
            res_message += "**page" + str(macro_page + 1) + "**\n"
            res_message += "```\n"
        res_message += "/ac " + CraftSkills_JP[actions[index]] + " <wait." + CraftWaits[actions[index]] + ">"  + "\n"
    res_message += "```"

    return res_message



#SND+AutoCrafter
def convert_message_JP_snd(actions):
    CraftSkills_JP  = read_CraftSkillsName_JP()
    CraftWaits      = read_CraftSkills_Wait()

    res_message = "***wait抜き日本語マクロ***\n"
    res_message += "***（SomethingNeedDoing+AutoCrafter用）***\n"
    res_message += str(len(actions)) + "actions\n"
    res_message += "```\n"
    res_message += "/waitaddon \"Synthesis\" <maxwait.5>\n"
    for index in range(len(actions)):
        res_message += "/ac " + CraftSkills_JP[actions[index]] + "\n"
    res_message += "```"

    return res_message

# 英語マクロ（通常？）
def convert_message_EN_normal(actions):
    CraftSkills_EN = read_CraftSkillsName_EN()
    CraftWaits      = read_CraftSkills_Wait()
    macro_page      = 0

    res_message = "***英語マクロ（通常？）***\n"
    # アクションの数が15*nでない場合
    if(len(actions)%15 != 0):
        # アクションの数を15で割った数+1がマクロのページ数
        res_message += str(len(actions)) + "actions" + str(int(len(actions)/15) + 1) + "macro\n"
        # 15で割った数が1以上なら、ページ数は2ページ以上
        if(int(len(actions)/15) > 0):
            res_message += "**page1**\n"
    # アクションの数が15*nの場合
    else:
        # アクションの数を15で割った数がマクロのページ数
        res_message += str(len(actions)) + "actions" + str(int(len(actions)/15)) + "macro\n"
        # 15で割った数-1が1以上なら、ページ数は2ページ以上
        if(int(len(actions)/15)-1 > 0):
            res_message += "**page1**\n"
    res_message += "```\n"
    for index in range(len(actions)):
        if(int(index/15) != macro_page):
            macro_page = int(index/15)
            res_message += "```\n"
            res_message += "**page" + str(macro_page + 1) + "**\n"
            res_message += "```\n"
        res_message += "/ac " + CraftSkills_EN[actions[index]] + " <wait." + CraftWaits[actions[index]] + ">"  + "\n"
    res_message += "```"

    return res_message


# 英語マクロ（MasterCraft）
def convert_message_EN_mastercraft(actions):
    CraftSkills_EN = read_CraftSkillsName_EN()
    CraftWaits      = read_CraftSkills_Wait()

    res_message = "***英語マクロ(MasterCraft用)***\n"
    res_message += str(len(actions)) + "actions\n"
    res_message += "```\n"
    for index in range(len(actions)):
        res_message += "/ac \"" + CraftSkills_EN[actions[index]] + "\"\n"
    res_message += "```"

    return res_message


# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    if message.content == "/clear":
        await message.channel.purge()
        await message.channel.send("履歴を全て削除しました。")

    else:
        res_actions = extract_action(message.content)
        if (res_actions != "NONE"):
            res = convert_message_JP_normal(res_actions)
            await message.channel.send(res)
            res = convert_message_JP_snd(res_actions)
            await message.channel.send(res)
            res = convert_message_EN_normal(res_actions)
            await message.channel.send(res)
            res = convert_message_EN_mastercraft(res_actions)
            await message.channel.send(res)


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
