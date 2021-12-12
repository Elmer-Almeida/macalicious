from newsletter.forms import NewsletterShortForm


def newsletter_form(request):
    return {
        'newsletter_form': NewsletterShortForm(),
    }
