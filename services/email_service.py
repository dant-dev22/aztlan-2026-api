"""
Envío de correos con Gmail (SMTP).
Se usa para: bienvenida al registrar (con aztlan_id) y notificación de pago aprobado.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import GMAIL_USER, GMAIL_APP_PASSWORD, EMAIL_ENABLED


def _get_smtp():
    """Conexión SMTP a Gmail."""
    if not EMAIL_ENABLED or not GMAIL_USER or not GMAIL_APP_PASSWORD:
        return None
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        return server
    except Exception:
        return None


def _send(to: str, subject: str, body_html: str, body_plain: str) -> bool:
    """Envía un correo. Devuelve True si se envió correctamente."""
    if not EMAIL_ENABLED or not GMAIL_USER or not GMAIL_APP_PASSWORD:
        return False
    server = _get_smtp()
    if not server:
        return False
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = GMAIL_USER
        msg["To"] = to
        msg.attach(MIMEText(body_plain, "plain", "utf-8"))
        msg.attach(MIMEText(body_html, "html", "utf-8"))
        server.sendmail(GMAIL_USER, to, msg.as_string())
        return True
    except Exception:
        return False
    finally:
        try:
            server.quit()
        except Exception:
            pass


def send_email_registro_iniciado(to_email: str, nombre: str, aztlan_id: str) -> bool:
    """
    Envía correo cuando el usuario inicia su registro (se le asigna aztlan_id).
    Cuerpo motivante.
    """
    subject = "¡Bienvenido al Torneo Aztlan 26! — Tu registro ha comenzado"
    body_plain = f"""Hola {nombre},

¡Bienvenido al Torneo Aztlan 26!

Tu registro ha sido recibido correctamente. Tu identificador único es:

  {aztlan_id}

Guarda este ID; lo necesitarás para subir tu comprobante de pago y completar tu inscripción.

Siguiente paso: envía tu comprobante de pago usando tu aztlan_id en la plataforma. Cuando el equipo lo revise y apruebe, recibirás una confirmación por correo.

¡Nos vemos en el tatami!

— Equipo Aztlan 26
"""
    body_html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: sans-serif; max-width: 560px; margin: 0 auto; padding: 20px;">
  <p>Hola <strong>{nombre}</strong>,</p>
  <p>¡Bienvenido al <strong>Torneo Aztlan 26</strong>!</p>
  <p>Tu registro ha sido recibido correctamente. Tu identificador único es:</p>
  <p style="background: #f0f0f0; padding: 12px; border-radius: 8px; font-family: monospace; font-size: 1.1em;"><strong>{aztlan_id}</strong></p>
  <p>Guarda este ID; lo necesitarás para subir tu comprobante de pago y completar tu inscripción.</p>
  <p><strong>Siguiente paso:</strong> envía tu comprobante de pago usando tu aztlan_id en la plataforma. Cuando el equipo lo revise y apruebe, recibirás una confirmación por correo.</p>
  <p>¡Nos vemos en el tatami!</p>
  <p>— Equipo Aztlan 26</p>
</body>
</html>"""
    return _send(to_email, subject, body_html, body_plain)


def send_email_pago_aprobado(to_email: str, nombre: str) -> bool:
    """
    Envía correo cuando el admin aprueba el comprobante de pago.
    """
    subject = "Torneo Aztlan 26 — Tu pago ha sido aprobado"
    body_plain = f"""Hola {nombre},

Tu comprobante de pago ha sido revisado y aprobado.

Tu inscripción al Torneo Aztlan 26 está completa. Nos vemos en el evento.

— Equipo Aztlan 26
"""
    body_html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: sans-serif; max-width: 560px; margin: 0 auto; padding: 20px;">
  <p>Hola <strong>{nombre}</strong>,</p>
  <p>Tu comprobante de pago ha sido revisado y <strong>aprobado</strong>.</p>
  <p>Tu inscripción al Torneo Aztlan 26 está completa. Nos vemos en el evento.</p>
  <p>— Equipo Aztlan 26</p>
</body>
</html>"""
    return _send(to_email, subject, body_html, body_plain)
