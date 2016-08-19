"""
integrations.groupme
--------

Groupme creation
TODO: wrap in Python


# TOKEN
b2c06f30d9850133234707112866f5b3

# UPLOAD IMAGE
curl -F "file=@vegas_2016.png" "https://image.groupme.com/pictures?access_token=b2c06f30d9850133234707112866f5b3"

# NEW GROUP
curl -X POST -H "Content-Type: application/json" -d '{"name": "Vegas Mixer Pod!", "share": true, "image_url": "https://i.groupme.com/851x315.png.dbc01f59b4e24e368b26a4344154bb5b"}' https://api.groupme.com/v3/groups?token=b2c06f30d9850133234707112866f5b3

>>
{"meta":{"code":201},
"response":
    {"id":"20930602",
    "group_id":"20930602",
    "name":"Twine with Image",
    "phone_number":"+1 5303843507",
    "type":"private",
    "description":null,
    "image_url":"https://i.groupme.com/851x315.png.dbc01f59b4e24e368b26a4344154bb5b",
    "creator_user_id":"36589956",
    "created_at":1459439889,
    "updated_at":1459439889,
    "office_mode":false,
    "share_url":"https://app.groupme.com/join_group/20930602/BPESOB",
    "members":[{"id":"146885218","user_id":"36589956","nickname":"Twine","muted":false,"image_url":null,"autokicked":false}],
    "max_memberships":200,
    "max_members":200,
    "messages":{"count":0,"last_message_id":null,"last_message_created_at":null,"preview":{"nickname":null,"text":null,"image_url":null,"attachments":[]}}
}}

test
https://app.groupme.com/join_group/20940107/aTnPKe

real
https://app.groupme.com/join_group/20940870/qTch0j
https://app.groupme.com/join_group/20940876/7JC5BI
https://app.groupme.com/join_group/20940885/KooqBO
"""

