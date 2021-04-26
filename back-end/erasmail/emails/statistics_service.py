def get_emails_stats_ids():
    return [
        "total",
        "received",
        "read",
        "unread",
        "older_3Y",
        "older_3Y_carbon",
        "larger_1MB",
        "larger_1MB_carbon",
    ]

def get_newsletters_stats_ids():
    return [
        "newsletters_count",
        "unsubscribed_newsletters",
        "subscribed",
        "emails_count",
        "carbon",
    ]

def get_threads_stats_ids():
    return [
        "total",
        "carbon",
        "carbon_yearly_forecast",
        "attachments",
    ]

def get_erasmail_stats_ids():
    return [
        "deleted_emails_older_filter",
        "deleted_emails_larger_filter",
        "deleted_emails_useless_filter",
        "deleted_emails_threads_feature",
        "deleted_attachments",
        "deleted_emails_newsletters_feature",
        "shared_badges",
        "shared_stats",
    ]