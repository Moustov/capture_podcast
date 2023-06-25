import requests
import urllib.request

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
            print(url_podcast)
            # \"serieEpisodeTitle\":\"6 : L’arc transmis à Philoctète\",
            # \"episodeSerieTitle\":\"Héraclès, super-héros chez les Grecs 6/6 : L’arc transmis à Philoctète\",
            # \"seriePath\":\"franceinter/podcasts/serie-heracles-super-heros-chez-les-grecs\",
            podcast_title = "test"
            try:
                # r = requests.get(url_podcast, allow_redirects=True)
                # open(f'{podcast_title}.mp3', 'wb').write(r.content)
                urllib.request.urlretrieve(url_podcast, f'{podcast_title}.mp3')
                # song.extract_song_from_url(url_song)
                # song.store_song("c:/chords")
            except Exception as e:
                print(str(e))
