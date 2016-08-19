"""
integrations.qualtrics
--------

Scripts to build Qualtrics surveys.
"""


import os
import io

S_PREFIX = """<div><img height="150" src="https://raw.githubusercontent.com/nsrivast/imgs/master/crop_"""

S_SUFFIX = """.png" width="150"></div><div><br></div><div>How well do you know this LF?</div>

<b>Super well.</b> Life story, secret tattoos, everything.
<b>Pretty well.</b> We stop for conversations in Huntsman and have hung out a few times.
<b>Okay.</b> We smile and say "hi" but I'm not 100% sure on last name?
<b>Who?</b> Pretty sure that's not an LF ..."""

def survey():
    s = ""
    n = 40
    for i in range(n):
        s_i = str(i+1) + ". " + S_PREFIX + str(i) + S_SUFFIX + "\n\n"

        if (i % 10 == 0):
            p = i / 10
            s_i = "[[Block:Page " + str(p+1) + " of 4]]\n\n" + s_i

        if (i % 10 == 9 and i != (n-1)):
            p = i / 10
            s_i = s_i + "[[PageBreak]]\n\n"

        s += s_i
    return s

if __name__ == '__main__':

    os.chdir("/Users/ns/Dropbox (Personal)/twine/Algo/")

    s_final = survey()

    f = open('applications/LF/results/survey.txt', 'w')
    f.write(s_final)
    f.close()
