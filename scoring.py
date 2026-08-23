def append_scores(data_dict, sid):
    if data_dict.get("Content") is None:
        data_dict.update(
            {
                "positive": None,
                "negative": None,
                "neutral": None,
                "compound": None,
            }
        )
        return data_dict

    content = data_dict["Title"] + " - " + data_dict["Content"]

    sentiment_dict = sid.polarity_scores(content)

    data_dict.update(
        {
            "positive": sentiment_dict["pos"],
            "negative": sentiment_dict["neg"],
            "neutral": sentiment_dict["neu"],
            "compound": sentiment_dict["compound"],
        }
    )

    return data_dict
