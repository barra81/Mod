# WTP: DEBUG LOG - what is called when the city banner is clicked (file WTP_BannerLog.txt in the game folder). To be removed again.
import time

iLines = 0

def log(szMsg):
	global iLines
	try:
		if iLines > 4000:
			return
		iLines += 1
		f = open("WTP_BannerLog.txt", "a")
		f.write("%.2f %s\n" % (time.time() % 1000, szMsg))
		f.close()
	except:
		pass
