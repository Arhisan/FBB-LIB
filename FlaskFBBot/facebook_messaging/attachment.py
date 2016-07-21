class FBAttachment():
    class File():
        image = 'image'
        audio = 'audio'
        video = 'video'
        file = 'file'

    def button_postback(title, postback):
        return {
            'type': 'postback',
            'title': title,
            'payload': postback
        }

    def button_web_url(title, url):
        return {
            'type': 'web_url',
            'title': title,
            'url': url
        }

    def quick_reply(title):
        return {
            'content_type':'text',
            'title': title,
            'payload': title
        }