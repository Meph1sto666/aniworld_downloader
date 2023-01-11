import json
l:dict = json.load(open("paths.json"))

def createPath(k:str) -> dict:
	s:dict = l.get(k)
	if s == None: return s
	path = []
	i = True
	while i:
		if not s.get("sub"): 
			path.reverse();
			p:list = list(s.get("path"))
			p.reverse()
			path.extend(p)
			path.reverse()
		if s.get("parent") == None: i = False
		s = l.get(s.get("parent"))
	r = { "path": path };
	if l.get(k).get("sub"):
		r["sub"] = True
	return r

def getContent(data, k:str):
	pathData = createPath(k)
	try:
		for p in pathData.get("path"):
			data = data[p]
	except:
		return None
	return data