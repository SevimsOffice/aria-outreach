"""
SMTP sender — Instantly'nin yerini alan doğrudan gönderim katmanı.
Hostinger (veya herhangi bir standart SMTP) mailbox'ından, warmup/açılma
takibi OLMADAN düz metin gönderir. Instantly'nin devraldığı iş burada:
sıralama, hız sınırlama ve durum takibi run_send_smtp.py'de yapılır — bu
modül yalnızca tek bir e-postayı güvenilir şekilde gönderir.
"""

import logging
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

logger = logging.getLogger(__name__)


class SMTPSender:
    def __init__(self, host: str, port: int, user: str, password: str, from_name: str = ""):
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._from_name = from_name or user

    def send(self, to: str, subject: str, body: str) -> bool:
        """
        Tek bir düz-metin e-posta gönderir. Başarılıysa True, herhangi bir
        SMTP/bağlantı hatasında False döner (exception fırlatmaz — çağıran
        script ardışık hataları sayıp durabilsin diye).
        """
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = formataddr((self._from_name, self._user))
        msg["To"] = to
        msg["Reply-To"] = self._user
        msg["List-Unsubscribe"] = f"<mailto:{self._user}?subject=unsubscribe>"

        try:
            with smtplib.SMTP_SSL(self._host, self._port, timeout=20) as server:
                server.login(self._user, self._password)
                server.sendmail(self._user, [to], msg.as_string())
            logger.info(f"SMTP: gönderildi ✓ {to}")
            return True
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP kimlik doğrulama hatası — SMTP_USER/SMTP_PASS kontrol et: {e}")
            return False
        except (smtplib.SMTPException, OSError) as e:
            logger.error(f"SMTP gönderim hatası {to}: {e}")
            return False
