# Copyright 2021 Planet Express Labs
# All rights reserved.
# The only reason for taking full copyright is because of a few bad actors.
# As long as you are using my code in good faith, we will probably not
# have an issue with it.
import httpx


class Match:
    def __init__(self, match_dict):
        self.replacements = match_dict.get('replacements')
        self.offset = match_dict.get('offset')
        self.errorLength = match_dict.get('length')


async def get_matches(text, lang="en-US"):
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.languagetoolplus.com/v2/check",
                                    params={"text": text, "language": lang}, verify=False)
    query_dict = response.json()
    return [Match(match) for match in query_dict['matches']
            if match.get('replacements')]


def correct(text, matches):
    text_list = list(text)
    errors = [text_list[match.offset:match.offset + match.errorLength]
              for match in matches]
    offset = 0
    for i, match in enumerate(matches):
        f = offset + match.offset
        t = f + match.errorLength
        if text_list[f:t] != errors[i]:
            continue
        replacement = list(f"**{match.replacements[0]['value']}**")
        text_list[f:t] = replacement
        offset += len(replacement) - t + f
    return "".join(text_list)
