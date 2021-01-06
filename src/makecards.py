from PIL import ImageFont, ImageDraw, Image
import numpy as np
import random
import uuid
import string

import cv2
import json
import os

#print (CARD_RATIO)

CHIP_WD_INCH = 0.4591
CARD_WD_INCH = 0.37 + CHIP_WD_INCH + 2.56

CHIP_HT_INCH = .3692
CARD_HT_INCH = 0.72 + CHIP_HT_INCH + 1.06

CARD_RATIO = CARD_HT_INCH / CARD_WD_INCH

CARD_WD = 300
CARD_HT = round(CARD_WD * CARD_RATIO)

H_MARGIN = round(CARD_WD / 100)
V_MARGIN = round(CARD_HT / 100)

CHIP_DIM_WD = round( (CHIP_WD_INCH / CARD_WD_INCH) * CARD_WD)
CHIP_DIM_HT = round( (CHIP_HT_INCH / CARD_HT_INCH) * CARD_HT)

CHIP_V_POS =  round((0.6875 / CARD_HT_INCH) * CARD_HT)
CHIP_H_POS =  round((0.3125 / CARD_WD_INCH) * CARD_WD)

LOGO_DIM_RATIO = 9/21
LOGO_DIM_WD = round(CARD_WD / 5)
LOGO_DIM_HT = round(LOGO_DIM_WD * LOGO_DIM_RATIO)

destdir = "C:\\mrk\\ml\\card\\credit-card-number-detector\\output\\"
CWD = "C:\\mrk\\ml\\card\\credit-card-number-detector\\"

#print ( "CARD_WD = ", CARD_WD, " CARD_HT = ", CARD_HT, " CHIP_V_POS = ", CHIP_V_POS, " CHIP_H_POS = ", CHIP_H_POS )

card_bg_dir = CWD + 'images\\card_bg\\'
card_bg_lst = os.listdir(card_bg_dir)


card_brands_lst = os.listdir(CWD + 'images\\cardbrands\\')

ax_dir = CWD + 'images\\cardbrands\\amex\\'
ax_lst = os.listdir(ax_dir)

cb_dir = CWD + 'images\\cardbrands\\cartebleue\\'
cb_lst = os.listdir(cb_dir)

di_dir = CWD + 'images\\cardbrands\\diners\\'
di_lst = os.listdir(di_dir)

jcb_dir = CWD + 'images\\cardbrands\\jcb\\'
jcb_lst = os.listdir(jcb_dir)

mc_dir = CWD + 'images\\cardbrands\\mastercard\\'
mc_lst = os.listdir(mc_dir)

rp_dir = CWD + 'images\\cardbrands\\rupay\\'
rp_lst = os.listdir(rp_dir)

up_dir = CWD + 'images\\cardbrands\\unionpay\\'
up_lst = os.listdir(up_dir)

vi_dir = CWD + 'images\\cardbrands\\visa\\'
vi_lst = os.listdir(vi_dir)

cobrand_dir = CWD + 'images\\cobrand\\'
cobrand_lst = os.listdir(cobrand_dir)

card_brands = [ax_lst, cb_lst, di_lst, jcb_lst, mc_lst, rp_lst, up_lst, vi_lst]
#print (random.choice(card_bg_lst) ) 

CHIP_dir = CWD + 'images\\chip\\'
CHIP_lst = os.listdir(CHIP_dir)

font_dir = CWD + 'fonts\\'


RB_VT = CARD_HT - V_MARGIN - LOGO_DIM_HT
RB_VB = CARD_HT - V_MARGIN
RB_HL = CARD_WD - H_MARGIN - LOGO_DIM_WD
RB_HR = CARD_WD - H_MARGIN


TL_VT =  V_MARGIN
TL_VB =  V_MARGIN + LOGO_DIM_HT
TL_HL = H_MARGIN
TL_HR = H_MARGIN + LOGO_DIM_WD

TR_VT =  V_MARGIN
TR_VB =  V_MARGIN + LOGO_DIM_HT
TR_HL = CARD_WD - H_MARGIN - LOGO_DIM_WD
TR_HR = CARD_WD - H_MARGIN

#logo_cobrand_pos = [( img[CARD_HT - V_MARGIN - LOGO_DIM_HT:CARD_HT - V_MARGIN, CARD_WD - H_MARGIN - LOGO_DIM_WD: CARD_WD - H_MARGIN]  ),]

#COLOR_SCHEME = cv2.COLOR_BGR2BGRA
COLOR_SCHEME = cv2.COLOR_BGR2RGB

colors_lst = [cv2.COLOR_BGR2RGB, cv2.COLOR_BGR2BGRA]

CARDNO_POS_T = CHIP_V_POS + CHIP_DIM_HT + 20
CARDNO_POS_L = 35

TEXT_SIZE = 25

EXPIRY_POS_T = CHIP_V_POS + CHIP_DIM_HT + 40
EXPIRY_POS_L = CARDNO_POS_L

NAME_POS_T = CHIP_V_POS + CHIP_DIM_HT + 55
NAME_POS_L = CARDNO_POS_L

def addChip(img):
    #print ("CHIP_lst = " , CHIP_lst)
    rndfile = CHIP_dir + random.choice(CHIP_lst)
    #print ("rndfile = " , rndfile)
    chipImg = cv2.imread(rndfile, COLOR_SCHEME)
    #print (" (CHIP_DIM_WD, CHIP_DIM_HT) ", (CHIP_DIM_WD, CHIP_DIM_HT))
    chipImg = cv2.resize(chipImg, (CHIP_DIM_WD, CHIP_DIM_HT) )
    img[CHIP_V_POS:CHIP_V_POS+chipImg.shape[0], CHIP_H_POS:CHIP_H_POS+chipImg.shape[1]] = chipImg
    #cv2.imshow("CHIP ", chipImg)
    #cv2.waitKey(0)
    return img

def addCardLogo(img):
    #print ("card brand = " , card_brands[0])
    rndfile = vi_dir + random.choice(vi_lst)
    print ("rndfile = " , rndfile)
    cardLogoImg = cv2.imread(rndfile, COLOR_SCHEME)
    print (" (LOGO_DIM_WD, LOGO_DIM_HT) ", (LOGO_DIM_WD, LOGO_DIM_HT))
    cardLogoImg = cv2.resize(cardLogoImg, (LOGO_DIM_WD, LOGO_DIM_HT) )
    print (' cardLogoImg.shape[0] = ' , cardLogoImg.shape[0] , "  ||| cardLogoImg.shape[1] = ", cardLogoImg.shape[1])
    #print ( " RB_VT ",RB_VT  , " RB_VB" ,RB_VB , "  RB_HL" , RB_HL,  "  RB_HR", RB_HR)
    #img[RB_VT :RB_VB, RB_HL : RB_HR] = cardLogoImg
    #img[TL_VT:TL_VB, TL_HL: TL_HR] = cardLogoImg
    img[TR_VT:TR_VB, TR_HL: TR_HR] = cardLogoImg
    #cv2.imshow("CHIP ", cardLogoImg)
    #cv2.waitKey(0)
    return img

def addCobrandLogo(img):
    #print ("card brand = " , card_brands[0])
    rndfile = cobrand_dir  + random.choice(cobrand_lst)
    print ("rndfile = " , rndfile)
    cardLogoImg = cv2.imread(rndfile, COLOR_SCHEME)
    print (" (LOGO_DIM_WD, LOGO_DIM_HT) ", (LOGO_DIM_WD, LOGO_DIM_HT))
    cardLogoImg = cv2.resize(cardLogoImg, (LOGO_DIM_WD, LOGO_DIM_HT) )
    #img[CARD_HT - V_MARGIN - LOGO_DIM_HT :CARD_HT - V_MARGIN - LOGO_DIM_HT + cardLogoImg.shape[0], CARD_WD - H_MARGIN - LOGO_DIM_WD : CARD_WD - H_MARGIN - LOGO_DIM_WD + cardLogoImg.shape[1]] = cardLogoImg
    img[CARD_HT - V_MARGIN - LOGO_DIM_HT:CARD_HT - V_MARGIN, CARD_WD - H_MARGIN - LOGO_DIM_WD: CARD_WD - H_MARGIN] = cardLogoImg
    #cv2.imshow("CHIP ", cardLogoImg)
    #cv2.waitKey(0)
    return img

def makeImg():
    try:
        imgpath = card_bg_dir + random.choice(card_bg_lst)
        #imgpath =  'C:\\mrk\\ml\\card\\credit-card-number-detector\\zebra-1196712.jpg'
        #print (" imagp atjh" , imgpath)
        img = cv2.imread(imgpath, COLOR_SCHEME)
        img = cv2.resize(img, (CARD_WD, CARD_HT))
        img = addChip(img)
        img = addCardLogo(img)

        #get filename
        #import uuid
        filename = uuid.uuid4().hex
        print ("filename =", filename)

        filename = destdir + filename

        #cv2.imwrite( filename + ".jpeg", img )
        cardno1 = "{:0>4d}".format(random.randint(1000, 9999))
        cardno2 = "{:0>4d}".format(random.randint(0, 9999))
        cardno3 = "{:0>4d}".format(random.randint(0, 9999))
        cardno4 = "{:0>4d}".format(random.randint(0, 9999))

        fontcolor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

################

        # Convert the image to RGB (OpenCV uses BGR)
        cv2_im_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Pass the image to PIL
        pil_im = Image.fromarray(cv2_im_rgb)

        draw = ImageDraw.Draw(pil_im)
        # use a truetype font
        font = ImageFont.truetype(font_dir + "micrenc.ttf", 25)

        # Draw the text
        draw.text((35, CHIP_V_POS+CHIP_DIM_HT + 20), str(cardno1) + " " + str(cardno2) + " " + str(cardno3) + " " + str(cardno4), font=font
                  , fill=fontcolor)
        #draw.text((0, 0) + 100,fill =128)

        # Get back the image to OpenCV
        cv2_im_processed = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)
        img = cv2_im_processed
###############

        # cv2.putText(img, str(cardno1) + " " + str(cardno2) + " " + str(cardno3) + " " + str(cardno4) ,
        #             (35,CHIP_V_POS+CHIP_DIM_HT + 20), fontFace=cv2.FONT_HERSHEY_TRIPLEX,
        #    fontScale=.6,
        #    color= fontcolor)
        #
        # cv2.putText(img, str("{:0>2d}".format(random.randint(1, 12))) + "/" + str("{:0>2d}".format(random.randint(1, 99))),
        #             (35, CHIP_V_POS + CHIP_DIM_HT + 45), fontFace=cv2.FONT_HERSHEY_TRIPLEX,
        #             fontScale=.6,
        #             color=fontcolor)
        #
        # cv2.putText(img, get_rand_name(),
        #             (35, CHIP_V_POS + CHIP_DIM_HT + 65), fontFace=cv2.FONT_HERSHEY_TRIPLEX,
        #             fontScale=.5,
        #             color=fontcolor)

        cards =   {
                    "cards" :
                        [
                            {
                                "is_card": "1",
                                "cardtype" : "vi",
                                "name" : "Mohammad Khan",
                                "expiry_month" : "01",
                                "expiry_year": "25",
                                "is_chip" : "1",
                                "path" :  filename + ".jpeg"
                            },

                            {
                                "iscard": "0",
                                "cardtype": "NA",
                                "name": "NA",
                                "expiry_month": "02",
                                "expiry_year": "26",
                                "is_chip": "NA",
                                "path":  filename + "1" + ".jpeg"
                            }
                        ]

                }


        with open(destdir + "cards.json", "w") as cards_file:
            json.dump(cards, cards_file, indent=2)


        return img
    except Exception as e:
        print (str(e))


#print ( "CARD_WD = ", CARD_WD, " CARD_HT = ", CARD_HT, " CHIP_V_POS = ", CHIP_V_POS, " CHIP_H_POS = ", CHIP_H_POS ) 


VOWELS = "aeiou"
CONSONANTS = "".join(set(string.ascii_lowercase) - set(VOWELS))


def get_rand_name():
    first = ""
    last = ""
    for i in range(random.randint(2, 10)):
        if i % 2 == 0:
            first += random.choice(CONSONANTS)
        else:
            first += random.choice(VOWELS)

    for i in range(random.randint(2, 10)):
        if i % 2 == 0:
            last += random.choice(CONSONANTS)
        else:
            last += random.choice(VOWELS)

    return first + " " + last

def makeAllimgs():
    try:
        count = 0
        for card_bg in card_bg_lst:
            for chip in CHIP_lst:
                for cardbrand in card_brands_lst:
                    for cardlogofile in os.listdir(CWD + 'images\\cardbrands\\' + cardbrand + '\\' ):
                        for colorscale in colors_lst:
                                for font in os.listdir(font_dir):
                                    count += 1

                                    cardno1 = "{:0>4d}".format(random.randint(1000, 9999))
                                    cardno2 = "{:0>4d}".format(random.randint(0, 9999))
                                    cardno3 = "{:0>4d}".format(random.randint(0, 9999))
                                    cardno4 = "{:0>4d}".format(random.randint(0, 9999))

                                    fontcolor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

                                    print ( " card_bg =", card_bg, " chip =", chip, " cardbrand =", cardbrand , " cardlogofile = ", cardlogofile, " color = ", colorscale, " cardno1 =", cardno1, " font=", font, " count= ", count)

                                    print(" CWD" , CWD, "  card_bg=", card_bg)

                                    imgpath = CWD + "images\\" + card_bg
                                    print(" imgpath", imgpath)

                                    img = cv2.imread(imgpath, cv2.COLOR_BGR2RGB)
                                    img = cv2.resize(img, (CARD_WD, CARD_HT))

                                    print(" 1111")

                                    cv2_im_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                                    # Pass the image to PIL
                                    pil_im = Image.fromarray(cv2_im_rgb)

                                    draw = ImageDraw.Draw(pil_im)
                                    # use a truetype font
                                    font = ImageFont.truetype(font_dir + font, TEXT_SIZE)

                                    # Draw the card no
                                    draw.text((CARDNO_POS_L, CARDNO_POS_T ),
                                              str(cardno1) + " " + str(cardno2) + " " + str(cardno3) + " " + str(
                                                  cardno4), font=font
                                              , fill=fontcolor)
                                    # Draw expiry
                                    draw.text((35, CHIP_V_POS + CHIP_DIM_HT + 20),
                                              str("{:0>2d}".format(random.randint(1, 12))) + "/" + str(
                                                  "{:0>2d}".format(random.randint(1, 99))), font=font
                                              , fill=fontcolor)

                                    # Draw Name
                                    draw.text((35, CHIP_V_POS + CHIP_DIM_HT + 20),
                                              get_rand_name(), font=font
                                              , fill=fontcolor)


                                    # Get back the image to OpenCV
                                    cv2_im_processed = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)
                                    img = cv2_im_processed

                                    print(" 2222")

                                    # Draw chip
                                    chipImg = cv2.imread( CHIP_dir + chip, COLOR_SCHEME)
                                    # print (" (CHIP_DIM_WD, CHIP_DIM_HT) ", (CHIP_DIM_WD, CHIP_DIM_HT))
                                    chipImg = cv2.resize(chipImg, (CHIP_DIM_WD, CHIP_DIM_HT))
                                    img[CHIP_V_POS:CHIP_V_POS + CHIP_DIM_HT, CHIP_H_POS:CHIP_H_POS + CHIP_DIM_WD] = chipImg

                                    print(" 333")
                                    cardLogoImg = cv2.imread( CWD + 'images\\cardbrands\\' + cardbrand + '\\' + cardlogofile, COLOR_SCHEME)
                                    cardLogoImg = cv2.resize(cardLogoImg, (LOGO_DIM_WD, LOGO_DIM_HT))
                                    img[TR_VT:TR_VB, TR_HL: TR_HR] = cardLogoImg

                                    print(" 4444")


                                    break
                                    #
                                    # #for i in range (9):
                                    #     i = 5
                                    #     if i == 0:
                                    #         #TL, TR
                                    #         # img[RB_VT :RB_VB, RB_HL : RB_HR] = cardLogoImg
                                    #         # img[TL_VT:TL_VB, TL_HL: TL_HR] = cardLogoImg
                                    #         img[TR_VT:TR_VB, TR_HL: TR_HR] = cardLogoImg
                                    #     elif i == 1 :
                                    #         TL, RB
                                    #     elif i == 2:
                                    #         TR, TL
                                    #     elif i == 3:
                                    #         TR, R
                                    #     elif i == 4:
                                    #         RB, TL
                                    #     elif i == 5:
                                    #         RB , TR
                                    #     elif i == 6:
                                    #         TL
                                    #     elif i == 7:
                                    #         TR
                                    #     elif i == 8:
                                    #         RB



    except Exception as e:
        print (str(e))


if __name__ == "__main__":
    # img = makeImg()
    # cv2.imshow("Gen Img", img)
    # cv2.waitKey(0)
    makeAllimgs()
