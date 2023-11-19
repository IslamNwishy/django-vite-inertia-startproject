# Django Imports
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template import loader


class SendEmailMixin:
    email_subject = None
    email_subject_template = None
    email_template_name = None
    from_email = None
    html_email_template_name = None

    def get_email_context(self, **kwargs):
        return self.get_context_data(**kwargs)

    def get_email_subject(self, context={}):
        if self.email_subject_template is not None:
            subject = loader.render_to_string(self.email_subject_template, context)
            # Email subject *must not* contain newlines
            subject = "".join(subject.splitlines())
        else:
            subject = self.email_subject

        return subject

    def get_email_body(self, context={}):
        body = loader.render_to_string(self.email_template_name, context)

        html_body = body
        if self.html_email_template_name is not None:
            html_body = loader.render_to_string(self.html_email_template_name, context)

        return body, html_body

    def get_message(self, to_emails, context={}):
        subject = self.get_email_subject(context)
        body, html_body = self.get_email_body(context)
        email_message = EmailMultiAlternatives(subject, body, self.from_email, to_emails)
        email_message.attach_alternative(html_body, "text/html")
        return email_message

    def send_emails(self, to_emails=[], fail_silently=False):
        context = self.get_email_context()
        self.get_message(to_emails, context)
        return self.get_message(to_emails, context).send(fail_silently=fail_silently)

    def send_mass_emails(self, to_emails=[], per_email_context={}, fail_silently=False):
        if not to_emails:
            return 0

        connection = get_connection(fail_silently=fail_silently)
        messages = []
        for email in to_emails:
            context = self.get_email_context(**per_email_context.get(email, {}))
            messages.append(self.get_message([email], context))

        return connection.send_messages(messages)
