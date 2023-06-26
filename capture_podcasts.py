import os

import requests
import urllib.request


def get_serie_name(p):
    # \"seriePath\":\"franceinter/podcasts/serie-heracles-super-heros-chez-les-grecs\",
    s = p.split("seriePath")
    serie = s[1].split(",")[0]
    res = serie.split("/")[-1].replace("\\","").replace('"',"")
    return res


def replace_special_chars(res):
    res = res.replace(r"\xe2\x80\x99", "'")
    res = res.replace(r"\xc3\xa8", "è")
    res = res.replace(r"\xc3\xa9", "é")
    res = res.replace(r"\xc3\xaa", "ê")
    res = res.replace(r"\xc3\xa0", "à")
    res = res.replace(r"\xc3\xaf", "ï")
    res = res.replace(r"\xc3\x89", "É")
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
    s = p.split("episodeSerieTitle")
    serie = s[1].split('"')[2]
    res = serie.replace("\\\\", "")
    res = replace_special_chars(res)
    return res


for page in range(1, 50):
    print(f"------ page {page} -------")
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
                serie = get_serie_name(p)
                episode = get_episode_name(p)
                if not os.path.exists(serie):
                    os.makedirs(serie)
                urllib.request.urlretrieve(url_podcast, f'{serie}\\{episode}.mp3')
            except Exception as e:
                print(str(e))
