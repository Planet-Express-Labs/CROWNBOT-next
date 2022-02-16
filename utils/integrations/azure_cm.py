import os.path
from pprint import pprint
from io import BytesIO
import sys
from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from azure.cognitiveservices.vision.contentmoderator.models import Screen, Evaluate
from msrest.authentication import CognitiveServicesCredentials
from zoidberg.config import SUBSCRIPTION_KEY, CONTENT_MODERATOR_ENDPOINT

# Add your Azure Content Moderator subscription key to your environment variables.
# SUBSCRIPTION_KEY = os.environ['CONTENT_MODERATOR_SUBSCRIPTION_KEY']

TEXT_FOLDER = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "text_files")

# The number of minutes to delay after updating the search index before
# performing image match operations against the list.
LATENCY_DELAY = 0.5
client = ContentModeratorClient(
    endpoint=CONTENT_MODERATOR_ENDPOINT,
    # Add your Content Moderator endpoint to your environment variables.
    credentials=CognitiveServicesCredentials(SUBSCRIPTION_KEY)
)


def text_moderation(text):
    """TextModeration.
    This will moderate a given long text.
    """
    text = bytes(text, "utf-8")
    text_bytes = BytesIO(text)

    screen = client.text_moderation.screen_text(
        text_content_type="text/plain",
        text_content=text_bytes,
        language="eng",
        autocorrect=True,
        pii=True
    )

    assert isinstance(screen, Screen)
    pprint(screen.as_dict())
    return screen.as_dict()


def image_moderation(image_url):
    """
    Takes an image url and returns a dictionary of potential objectionable content.

    Args:
        image_url ([string]): [URL of the image to be evaluated]

    Returns:
        [dict]: [Azure's evaluation of the image]
    """
    evaluation = client.image_moderation.evaluate_url_input(
        content_type="application/json",
        cache_image=True,
        data_representation="URL",
        value=image_url
    )
    assert isinstance(evaluation, Evaluate)
    return evaluation.as_dict()


if __name__ == "__main__":
    sys.path.append(
        os.path.abspath(
            os.path.join(
                __file__,
                "../..",
                "..",
                "..")))
