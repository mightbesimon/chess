# @mightbesimon
RED_DARK    = (230, 170, 155)
RED_LIGHT   = (240, 230, 215)
RED_MEAN    = (235, 200, 185)
# JohnPablok Cburnett Chess set
GREY_DARK   = ( 54,  54,  54)
GREY_LIGHT  = ( 89,  89,  89)
# chess.com board colours
GREEN_DARK  = (118, 149,  89)	#769559
GREEN_LIGHT = (235, 236, 209)	#EBECD1

# old colours
SOFT_RED    = (255, 198, 198)	#FFC6C6
DARK        = ( 15,  16,  10)	#0F100A
SNOW        = (255, 251, 251)	#FFFBFB
# FLAME     = (250,  24,  16)	#FA1810
# FIRE      = (248, 200,  10)	#F8C80A


# change all colours to hex
for colour in dir():
	if '__' in colour: continue
	globals()[colour] = '#%02x%02x%02x' % globals()[colour]
