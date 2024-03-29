import deltachat
import logging
import os
import sys
import pkg_resources


class AutoReplyPlugin:
    @deltachat.account_hookimpl
    def ac_incoming_message(self, message: deltachat.Message):
        avatar = pkg_resources.resource_filename(__name__, "avatar.jpg")
        message.account.set_avatar(avatar)
        message.create_chat()
        replytext = "Sorry, sending messages to other servers than try.webxdc.org is not " \
            "supported on this server. If you want to try out Delta Chat, just create" \
            " another try.webxdc.org account to send messages back and forth. If you " \
            "have questions, please ask around at https://support.delta.chat."
        reply = deltachat.message.Message.new_empty(message.account, "text")
        reply.quote = message
        reply.set_text(replytext)
        message.chat.send_msg(reply)
        logging.info("Sent isolation warning to " + message.get_sender_contact().addr)


def main(argv=None):
    logging.basicConfig(level=logging.INFO)


    if argv == None:
        argv = sys.argv
    if not ("--password") in argv:
        argv.append("--password")
        argv.append(os.environ.get("DELTACHAT_PASSWORD"))
    if not ("--email") in argv:
        argv.append("--email")
        argv.append(os.environ.get("DELTACHAT_ADDR"))

    deltachat.run_cmdline(argv=argv, account_plugins=[AutoReplyPlugin()])


if __name__ == "__main__":
    main()
