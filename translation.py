import requests


def translate_dataframe(df, api_key, target_language='en'):
    """
    Translates all string items in a DataFrame to the specified language (default: English) using the Google Translate API.
    """

    def translate_text(text, target_language, api_key):
        """
        Translates a single string using the Google Translate API.
        """
        if not isinstance(text, str):
            return text

        url = "https://translation.googleapis.com/language/translate/v2"


        params = {
            "q": text,
            "target": target_language,
            "key": api_key
        }

        response = requests.post(url, data=params)
        if response.status_code == 200:
            return response.json()['data']['translations'][0]['translatedText']
        else:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

    translated_columns = [translate_text(col, target_language, api_key) for col in df.columns]

    translated_df = df.apply(lambda col: col.map(lambda x: translate_text(x, target_language, api_key)))

    translated_df.columns = translated_columns  # CHANGE

    return translated_df


