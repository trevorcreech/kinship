SLACK_RESPONSE = [
    {
        "color": "674b1b",
        "deleted": False,
        "has_2fa": True,
        "id": "U01AA1AAA",
        "is_admin": True,
        "is_app_user": False,
        "is_bot": False,
        "is_owner": True,
        "is_primary_owner": False,
        "is_restricted": False,
        "is_ultra_restricted": False,
        "name": "bigbird",
        "profile": {
            "avatar_hash": "889e9da5a8aa",
            "display_name": "bigbird",
            "display_name_normalized": "bigbird",
            "email": "bigbird@opendoor.com",
            "first_name": "Big",
            "image_1024": "https://avatars.slack-edge.com/2017-06-07/195277861718_889e9da5a8aa51267ccf_1024.jpg",
            "image_192": "https://avatars.slack-edge.com/2017-06-07/195277861718_889e9da5a8aa51267ccf_192.jpg",
            "image_24": "https://avatars.slack-edge.com/2017-06-07/195277861718_889e9da5a8aa51267ccf_24.jpg",
            "image_32": "https://avatars.slack-edge.com/2017-06-07/195277861718_889e9da5a8aa51267ccf_32.jpg",
            "image_48": "https://avatars.slack-edge.com/2017-06-07/195277861718_889e9da5a8aa51267ccf_48.jpg",
            "image_512": "https://avatars.slack-edge.com/2017-06-07/195277861718_889e9da5a8aa51267ccf_512.jpg",
            "image_72": "https://avatars.slack-edge.com/2017-06-07/195277861718_889e9da5a8aa51267ccf_72.jpg",
            "image_original": "https://avatars.slack-edge.com/2017-06-07/195277861718_889e9da5a8aa51267ccf_original.jpg",
            "is_custom_image": True,
            "last_name": "Bird",
            "phone": "",
            "real_name": "Big Bird",
            "real_name_normalized": "Big Bird",
            "skype": "",
            "status_emoji": "",
            "status_expiration": 0,
            "status_text": "",
            "status_text_canonical": "",
            "team": "T01111AAA",
            "title": "Silly Title On Slack",
        },
        "real_name": "Big Bird",
        "team_id": "T01111AAA",
        "two_factor_type": "app",
        "tz": "America/Los_Angeles",
        "tz_label": "Pacific Standard Time",
        "tz_offset": -28800,
        "updated": 1548203272,
    },
    {
        "color": "bd9336",
        "deleted": False,
        "has_2fa": True,
        "id": "UB2BB22B2",
        "is_admin": False,
        "is_app_user": False,
        "is_bot": False,
        "is_owner": False,
        "is_primary_owner": False,
        "is_restricted": False,
        "is_ultra_restricted": False,
        "name": "cookie.monster",
        "profile": {
            "avatar_hash": "a75a609651e7",
            "display_name": "",
            "display_name_normalized": "",
            "email": "cookie.monster@opendoor.com",
            "first_name": "Cookie",
            "image_1024": "https://avatars.slack-edge.com/2018-08-10/414748558389_a75a609651e7f16ad043_1024.png",
            "image_192": "https://avatars.slack-edge.com/2018-08-10/414748558389_a75a609651e7f16ad043_192.png",
            "image_24": "https://avatars.slack-edge.com/2018-08-10/414748558389_a75a609651e7f16ad043_24.png",
            "image_32": "https://avatars.slack-edge.com/2018-08-10/414748558389_a75a609651e7f16ad043_32.png",
            "image_48": "https://avatars.slack-edge.com/2018-08-10/414748558389_a75a609651e7f16ad043_48.png",
            "image_512": "https://avatars.slack-edge.com/2018-08-10/414748558389_a75a609651e7f16ad043_512.png",
            "image_72": "https://avatars.slack-edge.com/2018-08-10/414748558389_a75a609651e7f16ad043_72.png",
            "image_original": "https://avatars.slack-edge.com/2018-08-10/414748558389_a75a609651e7f16ad043_original.png",
            "is_custom_image": True,
            "last_name": "Monster",
            "phone": "222-222-2222",
            "real_name": "Cookie Monster",
            "real_name_normalized": "Cookie Monster",
            "skype": "",
            "status_emoji": "",
            "status_expiration": 0,
            "status_text": "",
            "status_text_canonical": "",
            "team": "T02835DET",
            "title": "Chief of Cookie",
        },
        "real_name": "Cookie Monster (Slack Name With Garbage)",
        "team_id": "T01111AAA",
        "two_factor_type": "sms",
        "tz": "America/Los_Angeles",
        "tz_label": "Pacific Standard Time",
        "tz_offset": -28800,
        "updated": 1546901624,
    },
]

WORKDAY_RESPONSE = {
    "Report_Entry": [
        {
            "Employee_ID": "001000",
            "Preferred_Name": "Big Bird",
            "businessTitle": "Overridden Title From Workday",
            "Team_Member_s_Manager": "Big Bird",
            "Team_Member_Type": "Employee",
            "Worker_Status": "Active",
            "Hire_Date": "2014-01-01",
            "Date_of_Birth_without_Year": "11/01",
            "primaryWorkEmail1": "bigbird@opendoor.com",
            "location": "San Francisco, CA",
            "Cost_Center_-_ID": "8000",
            "Cost_Center_-_Name": "Management",
            "Team_Member_s_Manager_group": [
                {"Employee_ID1": "001000", "primaryWorkEmail": "bigbird@opendoor.com"}
            ],
            "Cost_Center_Hierarchy_group": [
                {
                    "Level_01_from_the_Top": "All Opendoor",
                    "Level_02_from_the_Top": "G&A",
                    "Level_03_from_the_Top": "Office of the CEO",
                    "Level_04_from_the_Top": "Executive Team",
                }
            ],
        },
        {
            "Employee_ID": "002000",
            "Preferred_Name": "Cookie Monster (Workday)",
            "businessTitle": "Chief of Cookie",
            "Team_Member_s_Manager": "Big Bird",
            "Team_Member_Type": "Employee",
            "Worker_Status": "Active",
            "Hire_Date": "2016-09-06",
            "Date_of_Birth_without_Year": "02/22",
            "primaryWorkEmail1": "cookie@opendoor.com",
            "location": "San Francisco, CA",
            "Cost_Center_-_ID": "8000",
            "Cost_Center_-_Name": "Management",
            "Team_Member_s_Manager_group": [
                {"Employee_ID1": "001000", "primaryWorkEmail": "bigbird@opendoor.com"}
            ],
            "Cost_Center_Hierarchy_group": [
                {
                    "Level_01_from_the_Top": "All Opendoor",
                    "Level_02_from_the_Top": "G&A",
                    "Level_03_from_the_Top": "Office of the CEO",
                    "Level_04_from_the_Top": "Executive Team",
                }
            ],
        },
    ]
}
