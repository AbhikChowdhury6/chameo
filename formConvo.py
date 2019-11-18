#!/usr/bin/env python3.7

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes

# imported to get type check and IDE completion
from hermes_python.ontology.dialogue.intent import IntentMessage

CONFIG_INI = "config.ini"

# if this skill is supposed to run on the satellite,
# please get this mqtt connection info from <config.ini>
#
# hint: MQTT server is always running on the master device
address = "http://127.0.0.1/lastConvo/"

class Template:
    """class used to wrap action code with mqtt connection
       please change the name referring to your application
    """

    def __init__(self):
        # get the configuration if needed
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except Exception:
            self.config = None

        # start listening to MQTT
        self.start_blocking()

    @staticmethod
    def intent_1_callback(hermes: Hermes,
                          intent_message: IntentMessage):

        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print('[Received] intent: {}'.format(
            intent_message.intent.intent_name))

        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(
            intent_message.site_id,
            "Action 1", "")

    @staticmethod
    def intent_2_callback(hermes: Hermes,
                          intent_message: IntentMessage):

        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print('[Received] intent: {}'.format(
            intent_message.intent.intent_name))

        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(
            intent_message.site_id,
            "Action 2", "")

    # register callback function to its intent and start listen to MQTT bus
    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intent('intent_1', self.intent_1_callback)\
            .subscribe_intent('intent_2', self.intent_2_callback)\
            .loop_forever()

    # --> Sub callback function, one per intent
    def askJoke_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        good_category = requests.get(address).json()

        category = None
        if intent_message.slots.category:
            category = intent_message.slots.category.first().value
            # check if the category is valide
            if category.encode("utf-8") not in good_category:
                category = None

        data = {'b64': category}
        feedback_msg = str(requests.post(url=address, data=data))

        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, feedback_msg, "Joke_Tuto_APP")


if __name__ == "__main__":
    Template()