import random

class Namer:
	first = ["A","Ada","Aki","Al","Ali","Alo","Ana","Ani","Ba","Be","Bo","Bra","Bro","Cha","Chi","Da","De","Do","Dra","Dro","Eki","Eko","Ele","Eli","Elo","Er","Ere","Eri","Ero","Fa","Fe","Fi","Fo","Fra","Gla","Gro","Ha","He","Hi","Illia","Ira","Ja","Jo","Ka","Ki","Kra","La","Le","Lo","Ma","Me","Mi","Mo","Na","Ne","No","O","Ol","Or","Pa","Pe","Pi","Po","Pra","Qua","Qui","Quo","Ra","Re","Ro","Sa","Sca","Sco","Se","Sha","She","Sho","So","Sta","Ste","Sti","Stu","Ta","Tha","The","Tho","Ti","To","Tra","Tri","Tru","Ul","Ur","Va","Vo","Wra","Xa","Xi","Zha","Zho"]
	second = ["bb","bl","bold","br","bran","can","carr","ch","cinn","ck","ckl","ckr","cks","dd","dell","dr","ds","fadd","fall","farr","ff","fill","fl","fr","genn","gg","gl","gord","gr","gs","h","hall","hark","hill","hork","jenn","kell","kill","kk","kl","klip","kr","krack","ladd","land","lark","ld","ldr","lind","ll","ln","lord","ls","matt","mend","mm","ms","nd","nett","ng","nk","nn","nodd","ns","nt","part","pelt","pl","pp","ppr","pps","rand","rd","resh","rn","rp","rr","rush","salk","sass","sc","sh","sp","ss","st","tall","tend","told","v","vall","w","wall","wild","will","x","y","yang","yell","z","zenn",]
	third = ["a","ab","ac","ace","ach","ad","adle","af","ag","ah","ai","ak","aker","al","ale","am","an","and","ane","ar","ard","ark","art","ash","at","ath","ave","ea","eb","ec","ech","ed","ef","eh","ek","el","elle","elton","em","en","end","ent","enton","ep","er","esh","ess","ett","ic","ich","id","if","ik","il","im","in","ion","ir","is","ish","it","ith","ive","ob","och","od","odin","oe","of","oh","ol","olen","omir","or","orb","org","ort","os","osh","ot","oth","ottle","ove","ow","ox","ud","ule","umber","un","under","undle","unt","ur","us","ust","ut","","","","","",]

	def random():
		return random.choice(Namer.first) + random.choice(Namer.second) + random.choice(Namer.third) 

