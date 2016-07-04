
config = {
    "log_name": "updates_esr45",
    "repo": {
        "repo": "https://hg.mozilla.org/users/raliiev_mozilla.com/tools",
        "revision": "default",
        "dest": "tools",
        "vcs": "hg",
    },
    "push_dest": "ssh://hg.mozilla.org/users/raliiev_mozilla.com/tools",
    "shipped-locales-url": "https://hg.mozilla.org/projects/jamun/raw-file/{revision}/browser/locales/shipped-locales",
    "ignore_no_changes": True,
    "ssh_user": "ffxbld",
    "ssh_key": "~/.ssh/ffxbld_rsa",
    "archive_domain": "ftp.stage.mozaws.net",
    "archive_prefix": "https://ftp.stage.mozaws.net/pub",
    "previous_archive_prefix": "https://archive.mozilla.org/pub",
    "download_domain": "download.mozilla.org",
    "balrog_url": "http://ec2-54-241-39-23.us-west-1.compute.amazonaws.com",
    "balrog_username": "stage-ffxbld",
    "update_channels": {
        "esr": {
            "version_regex": r".*",
            "requires_mirrors": True,
            "patcher_config": "mozEsr45-branch-patcher2.cfg",
            "update_verify_channel": "esr-localtest",
            "mar_channel_ids": [],
            "channel_names": ["esr", "esr-localtest", "esr-cdntest"],
            "rules_to_update": ["esr45-cdntest", "esr45-localtest"],
            "publish_rules": ["esr"],
        },
    },
    "balrog_use_dummy_suffix": False,
}
