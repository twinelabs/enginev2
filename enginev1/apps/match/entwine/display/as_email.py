"""
display.as_email
--------

Scripts to display matching results in email formats.

"""

import os


import csv


def load_csv(fname):
    """Loads csv file as list of lists"""

    with open(fname, "rb") as f:
        reader = csv.reader(f)
        res = list(reader)

    return res


def email_text(cluster_data, i):
    dd = cluster_data[1:]
    firsts = [x[6] for x in dd]
    lasts = [x[7] for x in dd]
    years = [x[23] for x in dd]
    cc = [x[25] for x in dd]
    linkedins = [x[26] for x in dd]
    emails = [x[8] for x in dd] + ["classmatematch+r3" + str(i) + "@gmail.com"]

    ambassador_emails = ["smessick@wharton.upenn.edu", "chiaoh@wharton.upenn.edu", "weirongc@wharton.upenn.edu", "anambiar@wharton.upenn.edu", "brandenw@wharton.upenn.edu", "ikwong@wharton.upenn.edu", "jasschew@wharton.upenn.edu", "jellin@wharton.upenn.edu", "jsoto@wharton.upenn.edu", "chunjohn@wharton.upenn.edu", "josephtq@wharton.upenn.edu", "jamesonk@wharton.upenn.edu", "luhussey@wharton.upenn.edu", "mijinkim@wharton.upenn.edu", "nsri@wharton.upenn.edu", "rbrazer@wharton.upenn.edu", "shayaan@wharton.upenn.edu"]
    intersecting_emails = [e for e in ambassador_emails if e in emails]
    if len(intersecting_emails) > 1:
        print("WARNING (multiple ambassadors in c" + str(i) + "): " + ", ".join(intersecting_emails))

    musics = [x[59] for x in dd]
    musics = list(set(musics))

    industries = [x[28:38] for x in dd]
    industries = [item for sublist in industries for item in sublist]
    industries = list(set(industries))[1:]

    desc_lines = [f + ' ' + l + ' (' + y + ', ' + c + ')' for f, l, y, c in zip(firsts, lasts, years, cc)]
    name_lines = [f + ' ' + l + ('' if li == '' else ' (' + li + ')') for f, l, li in zip(firsts, lasts, linkedins)]

    s = ", ".join(emails) + "\n\n"  + \
        "[ClassmateMatch] ... " + ", ".join(firsts[:-1]) + " and " + firsts[-1] + \
        "\n\nHello, Hello, Hello!\n\n" + \
        "WELCOME to ClassmateMatch, where everybody is looking forward to MEET!\n\n" + \
        "With a pool of over 900 enthusiastic & motivated students, we were able to select " + \
        "classmates whom you might not currently know ... but could soon become business partners " + \
        "or lifelong friends who will make the special effort to attend your wedding years from now.\n\n" + \
        "Without further ado, here's your \"Pod\" (all copied on this email):\n\n" + \
        "\n".join(["\t" + str(i+1) + ". " + nl for i, nl in enumerate(name_lines)]) + "\n\n" + \
        "WAIT, who are these people?! I thought I knew most people at Wharton!\n" + \
        "Well, apparently not. But let's start by breaking the ice.\n\n" + \
        "Among the members of this Pod, you represent professional experience across:\n" + \
        ", ".join(industries[:-1]) + " and " + industries[-1] + ". Impressive.\n\n" + \
        "Y'all also have some pretty sweet music tastes:" + \
        "\n" + ", ".join(musics[:-1]) + ", and" + musics[-1] + ".\n\n" + \
        "We're sure you'll be able to figure out who's who after the meetup. And if you needed more reasons to hang out, we have 10 bottles of champagne hanging out in our fridges right now that we want to give out. More details will come later this week...\n\n" + \
        "But we're all Wharton MBAs! So busy...\n" + \
        "A great way to kickstart the new friendship would be to dedicate your most valuable resource, your time :) As a starting point, we'd like to propose 4 potential options for meeting up.\n\n" + \
        "If these 4 great options do not work, we suggest when2meet.com. As long as most of your group is available, you should go ahead and meet up to snag those motivational beverages for a future meeting with the rest.\n\n" + \
        "With that, enough talking from us, time to go meet some new friends! Groups that drive contact in the first 24 hours have a much higher chance of meeting up. Once again, thank you for participating in ClassmateMatch. We hope you'll enjoy the experience.\n\n" + \
        "Happy Meeting,\nJoseph, Jass, Nikhil"

    return s

def manual_adj():
    import glob
    clusters = glob.glob("./results/msd_r3_elim/clusters/*.csv")
    ss = ""

    c_is = io.load_csv("./results/msd_r3_elim/cluster_indices.csv")
    c_is_dict = {}
    for c_i in c_is:
        c_is_dict[c_i[0]] = c_i[1]

    email_map = {}
    name_map = {}
    for i, c in enumerate(clusters):
        cdata = io.load_csv(c)
        for x in cdata[1:]:
            dd = { 'first': x[6], 'last': x[7], 'i': i, 'fname': c_is_dict[str(i)] }
            email_map[x[8]] = dd
            name_map[x[6] + ' ' + x[7]] = dd

        names = ['Zanoschi', 'Rosensweig', 'Windle', 'Friedman', 'Le Normand', 'Miller', 'Aronson', 'Chen', 'Bouskela', 'Mullaney', 'Chang']
        if x[7] in names:
            print(dd)

    pdb.set_trace()

ACTIVITIES = ['Your new Vegas Pod', 'EDM at Club XS', 'Casino', 'Theatre and Performances', 'Encore Beach Club', 'Hip hop and House at Drais Nightclub']

def email_text_vegas(pod_data, groupme_links):

    dd = pod_data[1:]
    pods = [int(x[0]) for x in dd]

    ss = []
    for i_pod in range(max(pods) + 1):

        pod_rows = [row for row, pod in enumerate(pods) if pod == i_pod]
        pd = [row for i, row in enumerate(dd) if i in pod_rows]

        firsts = [x[1] for x in pd]
        lasts = [x[2] for x in pd]
        groupmes = [x[9] for x in pd]
        leaders = [x[48] for x in pd]
        name_lines = [f + ' ' + l + ('' if gm == '' else ' (' + gm + ')') + ('- **Pod Leader' if ld.lower() == 'yes' else '') for f, l, gm, ld in zip(firsts, lasts, groupmes, leaders)]

        emails = [x[11] for x in pd] + ["twinelabs+pv" + str(i_pod) + "@gmail.com"]

        musics = list(set([x[39] for x in pd if x[39] != '']))
        cuisines = list(set([x[40] for x in pd if x[40] != '']))

        industries = [x[14:24] for x in pd]
        industries = [item for sublist in industries for item in sublist]
        industries = list(set(industries))[1:]

        activity_ranks = [x[3:9] for x in pd]
        activity_ranks = [['3.5' if val == '' else val for val in row] for row in activity_ranks]
        activity_ranks = numpy.array(activity_ranks).astype('float')
        pod_ranks = numpy.mean(activity_ranks, axis=0)
        pod_top3 = numpy.argsort(pod_ranks)[:3]
        activities = [ACTIVITIES[i] for i in pod_top3]

        s = ", ".join(emails) + """

Dear Vegas Attendees,

Get excited!! The 5th Annual Inter-MBA Las Vegas Mixer 2016 is happening in a week!!

Introducing your Vegas Pod 2016!
You asked for more inter-school networking - and this is your answer. With over 400 enthusiastic MBA students, alums, and friends from across the top business schools and professional backgrounds signed up for Pods, we were able to select people whom you might not currently know, but could soon become your best buddies.

Introducing your "Pod" ... *drumrolls*:

Name (GroupMe ID)
""" + "\n".join([str(i+1) + ". " + nl for i, nl in enumerate(name_lines)]) + """

** The Pod leader has been politely nominated by the committee to ensure everyone in the Pod goes to Vegas in high spirits, including adding each other up on Facebook!! You can have a drink of us if you did your job well!
There have been some ticket transfers and if anyone on this list is no longer going, please let the group know, and add the person who is taking over your ticket.

Not another random grouping?
Remember that survey you took? Every single answer was considered in putting this group together. We hope you'll get to know each other really well by the end of the event - but in the meantime, here are some teasers:

Among the members of this Pod, you have professional experience across:
""" +  ", ".join(industries[:-1]) + " and " + industries[-1] + """

Y'all also have some pretty sweet music tastes:
""" +  ", ".join(musics[:-1]) + ", and " + musics[-1] + "." + """

Top Food preferences:
""" + ", ".join(cuisines[:-1]) + ", and " + cuisines[-1] + "." + """

Here are the activities you are most looking forward to:
""" + "\n".join([str(i+1) + ". " + act for i, act in enumerate(activities)]) + """

What's Next?
A great way to get these new friendships flowing would be to start getting to know each other over the next week and solidify these newfound relationships in Vegas.

What you should do:

1. Join this customized GroupMe link (""" + groupme_links[i_pod][0] + """) created for your Pod ASAP and start getting to know each other! Introduce yourself - school, hobbies, personal & professional MBA goals, and share how you plan to spend the weekend.
2. Decide upon a time and a place for dinner on Friday night (4/8) - we've attached a set of suggested restaurants for you to try, with an easy link to make reservations!
3. Any last minute logistics, What time you arrive, rooms, where to meet for late-comers, etc
4. Check out the the pre-club mingles together, introduce each other to your circle of friends, and have a great time at XS on Friday night
5. Saturday afternoon plans - we've deliberately kept it flexible for you this time around, but we have included Marquee Dayclub in our suggested itinerary that we recommend you check out with your Pod!

With that, we are looking forward to welcoming you at Vegas!! Please reach out to waaamvegas@gmail.com with any queries.

Regards,

Jass, on behalf of the Vegas Planning committee
"""
        ss.append(s)

    return ss


def email_text_LF(pod_data, when2meets):

    dd = pod_data[1:]
    pods = [int(x[0]) for x in dd]

    ss = []
    for i_pod in range(max(pods) + 1):

        pod_rows = [row for row, pod in enumerate(pods) if pod == i_pod]
        pd = [row for i, row in enumerate(dd) if i in pod_rows]

        firsts = [x[3] for x in pd]
        lasts = [x[4] for x in pd]
        emails = [x[1][:-1] + 'wharton.upenn.edu' for x in pd]

        name_lines = [f + ' ' + l for f, l in zip(firsts, lasts)]

        s = ", ".join(emails) + """

Hey LFs,

Thanks for filling out the survey with everyone's headshots!

I used the data to put people into groups of 5-6 that are least likely to know each other. (The optimization was global, so you may have 1 or 2 here you still know well).

""" + "\n".join([str(i+1) + ". " + nl for i, nl in enumerate(name_lines)]) + """

Will leave it to everyone to coordinate a meet-up, but if it's helpful - here's a when2meet for afternoons + evenings over the next week:

""" + str(when2meets[i_pod][0]) + """

Given that it's the end of the year, I'd recommend meeting up even if you can only find a time that fits 3 or 4 people.

Happy entwining!
Nikhil
"""
        ss.append(s)

    return ss

def map_dem(s):
    DEMS = {
        'Hillary Clinton': 'Hillary',
        'Really, Hillary Clinton!': 'Hillary',
        'Bernie Sanders': 'Bernie',
        'Lincoln Chafee': 'Lincoln Chafee',
        'Jim Webb': 'Jim Webb'
    }
    return DEMS[s]

def map_rep(s):
    REPS = {
        'Donald Trump': 'Trump',
        'John Kasich': 'John Kasich',
        'Marco Rubio': 'Marco Rubio',
        'Ted Cruz': 'Ted Cruz'
    }
    return REPS[s]



def email_text_DNC(pod_data):

    dd = pod_data[1:]
    pods = [int(x[0]) for x in dd]

    ss = []
    for i_pod in range(max(pods) + 1):

        pod_rows = [row for row, pod in enumerate(pods) if pod == i_pod]
        pd = [row for i, row in enumerate(dd) if i in pod_rows]
        n = len(pd)

        names = [x[3] for x in pd]
        emails = [x[4] for x in pd]
        dems = [x[5] for x in pd]
        reps = [x[6] for x in pd]
        issues = [x[7] for x in pd]

        namelines = []
        for i in range(n):
            nameline = str(i+1) + ". " + names[i] + " (" + emails[i] + "), "
            nameline += "favorite Democratic candidate: " + map_dem(dems[i]) + ", "
            nameline += "fave Republican candidate: " + map_rep(reps[i])
            namelines.append(nameline)


        issue_string = issues[0]
        if len(issues) > 1:
            if issues[0] != issues[1]:
                issue_string += " and " + issues[1]

        s = ", ".join(emails) + """

""" + "Pod # - " + str(i_pod) + """

SUBJECT: Twine - Meet your 2016 DNC match!

Hello!

Thanks for filling out the Twine DNC survey! We think you'll click with this fellow DNC-goer:

""" + "\n".join(namelines) + """

You both care about """ + issue_string + """.

If you'd like to coordinate a conversation (or even meet up), 'reply all' to this email!

Happy Twining!
www.twinelabs.com
"""
        ss.append(s)

    return ss


if __name__ == '__main__':

    f_path = "/Users/ns/Dropbox/twine/Customer Engagements/DNC/AlgoData/results/"
    os.chdir(f_path)
    pod_data = load_csv("results_ns.csv")

    ss = email_text_DNC(pod_data)
    emails_text = '\n\n\n'.join(ss)

    f = open('emails_ns.txt', 'w')
    f.write(emails_text)
    f.close()
