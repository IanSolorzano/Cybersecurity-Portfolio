import re
import tldextract
import whois

def extract_features_from_url(url):
    try:
        features = []

        features.append(len(url))

        features.append(1 if re.match(r"http[s]?://\d+\.\d+\.\d+\.\d+", url) else 0)

        ext = tldextract.extract(url)
        features.append(len(ext.subdomain.split('.')) if ext.subdomain else 0)

        features.append(1 if "@" in url else 0)

        features.append(1 if "-" in url else 0)

        features.append(1 if "=" in url else 0)

        domain = ext.domain + "." + ext.suffix
        w = whois.whois(domain)

        created = w.creation_date
        expires = w.expiration_date

        # Si son listas, tomar el primer elemento
        if isinstance(created, list):
            created = created[0]
        if isinstance(expires, list):
            expires = expires[0]

        if created and expires:
            age = (expires - created).days
        else:
            age = 0

        features.append(age)

        return features
    except Exception as e:
        print("Error al extraer características:", e)
        return None
