from random import randrange as rr

colors = {
	"white": (255,255,255),
	"red": (255,0,0),
	"blue": (0,0,255),
	"black": (0,0,0)
}

def random_color():
	return (rr(0,255), rr(0,255), rr(0,255))
