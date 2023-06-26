import os
import traceback

import requests
import urllib.request


def get_serie_name(p):
    # \"seriePath\":\"franceinter/podcasts/serie-heracles-super-heros-chez-les-grecs\",
    res = ""
    try:
        if "seriePath" in p:
            s = p.split("seriePath")
            serie = s[1].split(",")[0]
            res = serie.split("/")[-1].replace("\\", "").replace('"', "")
        else:
            res = "__"
    except:
        pass
    return res


def replace_special_chars(res):
    res = res.replace(r"\xe2\x80\x99", "'")
    res = res.replace(r"\xc3\xa8", "è")
    res = res.replace(r"\xc3\xa9", "é")
    res = res.replace(r"\xc3\xaa", "ê")
    res = res.replace(r"\xc3\xa0", "à")
    res = res.replace(r"\xc3\xaf", "ï")
    res = res.replace(r"\xc3\x89", "É")
    res = res.replace(r"\xc3\xa0", " ")
    res = res.replace(r"\xc2\xa0", "?")
    res = res.replace(r"\xc3\x", "_")
    res = res.replace(r"/", "_")
    res = res.replace(r":", "_")
    res = res.replace(r"?", "_")
    res = res.replace(r"*", "_")
    res = res.replace(r"<", "_")
    res = res.replace("\\", "_")
    res = res.replace('"', "_")
    res = res.replace('|', "_")
    return res


def get_episode_name(p):
    # \"serieEpisodeTitle\":\"6 : L’arc transmis à Philoctète\",
    # \"episodeSerieTitle\":\"Héraclès, super-héros chez les Grecs 6/6 : L’arc transmis à Philoctète\",
    res = ""
    serie = ""
    s = p.split("episodeSerieTitle")
    if len(s) > 1:
        serie = s[1].split('"')[2]
        res = serie.replace("\\\\", "")
        res = replace_special_chars(res)
    else:
        res = "_"
    return res


def get_title(p):
    res = ""
    serie = ""
    s = p.split("title")
    if len(s) > 1:
        serie = s[1].split('"')[2]
        res = serie.replace("\\\\", "")
        res = replace_special_chars(res)
    else:
        res = "_"
    return res


if not os.path.exists("podcasts"):
    os.makedirs("podcasts")

for page in range(1, 50):
    # print(f"------ page {page} -------")
    if page == 1:
        the_page = ""
    else:
        the_page = f"p={page}"

    url = f"https://www.radiofrance.fr/franceinter/podcasts/quand-les-dieux-rodaient-sur-la-terre?{the_page}"

    print(f"Trying to retrieve {url}...")
    page = requests.get(url)
    data_content = str(page.content).split('https://media.radiofrance-podcast.net')
    for p in data_content:
        podcast = p.split(".mp3")
        if "podcast" in podcast[0]:
            url_podcast = f'https://media.radiofrance-podcast.net{podcast[0]}.mp3'
            try:
                print(url_podcast)
                serie = ""
                episode = ""
                title = ""
                serie = get_serie_name(p)
                if serie != "__":
                    episode = get_episode_name(p)
                    if not os.path.exists(f"podcasts/{serie}"):
                        os.makedirs(f"podcasts/{serie}")
                    if not os.path.exists(f'podcasts/{serie}/{episode}.mp3'):
                        urllib.request.urlretrieve(url_podcast, f'podcasts/{serie}/{episode}.mp3')
                else:
                    title = get_title(p)
                    if not os.path.exists(f'podcasts/{title}.mp3'):
                        urllib.request.urlretrieve(url_podcast, f'podcasts/{title}.mp3')
            except Exception as e:
                print(f">> Error found at {serie} / {episode} ({title} - {url_podcast}")
                print(str(e))
                traceback.print_exc()
