from dotenv import load_dotenv
from packages import anime
load_dotenv();

# a = anime.Anime("https://aniworld.to/anime/stream/arifureta-from-commonplace-to-worlds-strongest")
# a = anime.Anime("https://aniworld.to/anime/stream/the-eminence-in-shadow")
# a.save()
a = anime.load(1582)

# print(a.SEASONS[0].EPISODES[0].streamFilter("vidoza","ger-sub")[0].getVideoUrl())
# print(a.SEASONS[0].EPISODES[1].download("vidoza","ger-sub"))
# a.SEASONS[-1].EPISODES[-1].STREAMS[-1].getVideoUrl()
# print(a.__str__())
# a.save()
for i in range(0,10):
	print(a.SEASONS[0].EPISODES[i].STREAMS[0].getVideoUrl())