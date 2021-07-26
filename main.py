import base64

from src.twitter_for_event import TwitterForEvent
from src.twitter_for_player import TwitterForPlayer


def entrypoint(event, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
         event (dict):  The dictionary with data specific to this type of
                        event. The `@type` field maps to
                         `type.googleapis.com/google.pubsub.v1.PubsubMessage`.
                        The `data` field maps to the PubsubMessage data
                        in a base64-encoded string. The `attributes` field maps
                        to the PubsubMessage attributes if any is present.
         context (google.cloud.functions.Context): Metadata of triggering event
                        including `event_id` which maps to the PubsubMessage
                        messageId, `timestamp` which maps to the PubsubMessage
                        publishTime, `event_type` which maps to
                        `google.pubsub.topic.publish`, and `resource` which is
                        a dictionary that describes the service API endpoint
                        pubsub.googleapis.com, the triggering topic's name, and
                        the triggering event type
                        `type.googleapis.com/google.pubsub.v1.PubsubMessage`.
    """

    data = base64.b64decode(event['data']).decode('utf-8')
    attributes = event.get('attributes', {})
    school = attributes.get('school', None)
    event = attributes.get('event', None)
    print(f'Incoming Data: {data}')
    if school:
        TwitterForPlayer(school=school, content=data).send_tweet()
    elif event:
        TwitterForEvent(attributes=attributes).find_retweet()
