from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
from SelenPyTest.pyselenium.models.logs import Log
from SelenPyTest.pyselenium.untils.function import get_passwd, unregister
from SelenPyTest.common.error import EmailAddressInvaild
import smtplib
import os
import re

# see 2.2.2. Structured Header Field Bodies
WSP = r'[ \t]'
# see 2.2.3. Long Header Fields
CRLF = r'(?:\r\n)'
# see 3.2.1. Primitive Tokens
NO_WS_CTL = r'\x01-\x08\x0b\x0c\x0f-\x1f\x7f'
# see 3.2.2. Quoted characters
QUOTED_PAIR = r'(?:\\.)'
FWS = r'(?:(?:' + WSP + r'*' + CRLF + r')?' + \
      WSP + \
    r'+)'                                            # see 3.2.3. Folding white space and comments
CTEXT = r'[' + NO_WS_CTL + \
        r'\x21-\x27\x2a-\x5b\x5d-\x7e]'              # see 3.2.3
CCONTENT = r'(?:' + CTEXT + r'|' + \
           QUOTED_PAIR + \
    r')'                        # see 3.2.3 (NB: The RFC includes COMMENT here
# as well, but that would be circular.)
COMMENT = r'\((?:' + FWS + r'?' + CCONTENT + \
          r')*' + FWS + r'?\)'                       # see 3.2.3
CFWS = r'(?:' + FWS + r'?' + COMMENT + ')*(?:' + \
       FWS + '?' + COMMENT + '|' + FWS + ')'         # see 3.2.3
ATEXT = r'[\w!#$%&\'\*\+\-/=\?\^`\{\|\}~]'           # see 3.2.4. Atom
ATOM = CFWS + r'?' + ATEXT + r'+' + CFWS + r'?'      # see 3.2.4
DOT_ATOM_TEXT = ATEXT + r'+(?:\.' + ATEXT + r'+)*'   # see 3.2.4
DOT_ATOM = CFWS + r'?' + DOT_ATOM_TEXT + CFWS + r'?'  # see 3.2.4
QTEXT = r'[' + NO_WS_CTL + \
        r'\x21\x23-\x5b\x5d-\x7e]'                   # see 3.2.5. Quoted strings
QCONTENT = r'(?:' + QTEXT + r'|' + \
           QUOTED_PAIR + r')'                        # see 3.2.5
QUOTED_STRING = CFWS + r'?' + r'"(?:' + FWS + \
    r'?' + QCONTENT + r')*' + FWS + \
    r'?' + r'"' + CFWS + r'?'
LOCAL_PART = r'(?:' + DOT_ATOM + r'|' + \
             QUOTED_STRING + \
    r')'                    # see 3.4.1. Addr-spec specification
DTEXT = r'[' + NO_WS_CTL + r'\x21-\x5a\x5e-\x7e]'    # see 3.4.1
DCONTENT = r'(?:' + DTEXT + r'|' + \
           QUOTED_PAIR + r')'                        # see 3.4.1
DOMAIN_LITERAL = CFWS + r'?' + r'\[' + \
    r'(?:' + FWS + r'?' + DCONTENT + \
    r')*' + FWS + r'?\]' + CFWS + r'?'  # see 3.4.1
DOMAIN = r'(?:' + DOT_ATOM + r'|' + \
         DOMAIN_LITERAL + r')'                       # see 3.4.1
ADDR_SPEC = LOCAL_PART + r'@' + DOMAIN               # see 3.4.1

# A valid address will match exactly the 3.4.1 addr-spec.
VALID_ADDRESS_REGEXP = '^' + ADDR_SPEC + '$'

class Email:

    def __init__(self,
        server='10.10.1.3',
        usr='',
        pwd=None,
        port=25,
        encoding='utf-8',
        email_validation=True
        ):
        self.logger = Log().get_logger()
        self.smtp = smtplib.SMTP()
        self.is_close = False
        self.server = server
        self.port = port
        self.usr = usr
        self.pwd = pwd
        self.encoding = encoding
        self.email_validation = email_validation

        if self.email_validation is True:
            self.validate_email_with_regex(self.usr)


    def validate_email_with_regex(self, email_address):
        if not re.match(VALID_ADDRESS_REGEXP, email_address):
            emsg = '邮箱地址 "{}" 不符合 RFC 2822 标准'.format(email_address)
            raise EmailAddressInvaild(emsg)
        # apart from the standard, I personally do not trust email addresses without dot.
        if "." not in email_address and "localhost" not in email_address.lower():
            raise EmailAddressInvaild("邮箱地址可能少了一个点")

    def __enter__(self):
        return self

    def __exit__(self):
        if not self.is_close:
            self.close()

    def __del__(self):
        if not self.is_close:
            self.close()

    def _login(self, pwd):
        if pwd is None:
            pwd = get_passwd(self.usr, self.pwd)
        self.smtp.connect(self.server, self.port)
        self.smtp.login(self.usr, pwd)

    # recipients attachment 可以是一个字符串 或者 字符串列表
    def send(self,
        subject=None,
        content=None,
        recipients='',
        attachments=None
        ):
        if isinstance(recipients, str):
            recipients = [recipients]

        if self.email_validation is True:
            for email_address in recipients:
                self.validate_email_with_regex(email_address)
        try:
            self._login(self.pwd)
            msg = self.message(subject, content, recipients, attachments)
            self.smtp.sendmail(self.usr, recipients, msg.as_string())
        except (smtplib.SMTPAuthenticationError, smtplib.SMTPRecipientsRefused) as e:
            self.logger.exception('用户名密码验证失败！%s', e)
            if self.pwd is None:
                print('登陆失败{}'.format(self.usr))
                if unregister(usr=self.usr):
                    print('清除{}的密码成功'.format(self.usr))
        else:
            print('"{}"邮件发送给{}成功'.format(subject, recipients))
        self.logger.info("邮件发送给 %s", recipients)

    def message(self, subject, content, recipients, attachments):

        if isinstance(attachments, str):
            attachments = [attachments]
        attachlist = []
        if attachments is not None:
            for attr in attachments:
                if not os.path.isfile(attr):
                    raise TypeError("'{}' 不是一个有效的文件路径".format(attr))
                attachlist.append(self._get_attach(self._open(attr),
                    os.path.basename(attr)))
        if content is not None:
            if os.path.isfile(content):
                #判断文件类型是html还是普通文本
                type = 'html' if content.strip().endswith('html') else 'plain'
                self.logger.info('email content:%s is file, type: %s', content, type)
                attachlist.append(MIMEText(self._open(content), type, self.encoding))
            else:
                attachlist.append(MIMEText(content, 'plain', self.encoding))

        #创建一个带附件的实例
        #mixed related
        message = MIMEMultipart('mixed')
        self._add_subject_header(message, subject)
        self._add_recipients_header(message, recipients)

        for att in attachlist:
            message.attach(att)

        return message

    def _add_recipients_header(self, message, recipients):
        message['From'] = Header(self.usr, self.encoding)
        if isinstance(recipients, list):
            recipients = '; '.join(recipients)
        message['To'] = Header(recipients, self.encoding)

    def _add_subject_header(self, message, subject):
        if not subject:
            self.logger.info('Email No subject')
            return
        if isinstance(subject, list):
            subject = " ".join(list)
        message['Subject'] = Header(subject, self.encoding)

    def _get_attach(self, attach_content, attach_name):
        attach = MIMEApplication(attach_content)
        attach.add_header('Content-Disposition', 'attachment', filename=attach_name)
        return attach

    def _open(self, file):
        if not os.path.isfile(file):
            raise TypeError("'{}' 不是一个有效的文件路径".format(file))
        with open(file, 'rb') as f:
            file_content = f.read()
        return file_content


    def close(self):
        self.is_close = True
        try:
            self.smtp.quit()
        except (TypeError, AttributeError, smtplib.SMTPServerDisconnected):
            pass
